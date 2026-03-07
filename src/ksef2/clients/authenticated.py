from functools import cached_property
from typing import final

from ksef2.clients.batch import BatchSessionClient
from ksef2.clients.certificates import CertificatesClient
from ksef2.clients.invoices import InvoicesClient
from ksef2.clients.limits import LimitsClient
from ksef2.clients.online import OnlineSessionClient
from ksef2.clients.permissions import PermissionsClient
from ksef2.clients.session_log import InvoiceSessionLogClient
from ksef2.clients.session_management import SessionManagementClient
from ksef2.clients.tokens import TokensClient
from ksef2.core.crypto import generate_session_key, encrypt_symmetric_key
from ksef2.core.protocols import Middleware
from ksef2.core.middlewares.auth import BearerTokenMiddleware
from ksef2.core.stores import CertificateStore
from ksef2.domain.models import (
    BatchFileInfo,
    BatchSessionState,
    OpenBatchSessionRequest,
)
from ksef2.domain.models.auth import AuthTokens
from ksef2.domain.models.session import (
    FormSchema,
    OpenOnlineSessionRequest,
    OnlineSessionState,
)
from ksef2.infra.mappers.encryption import from_spec as encryption_from_spec
from ksef2.infra.mappers.sessions import from_spec as session_from_spec
from ksef2.infra.mappers.sessions import to_spec as session_to_spec
from ksef2.endpoints import encryption, session
from ksef2.services.invoices import InvoicesService


@final
class AuthenticatedClient:
    """Authenticated entry point for KSeF operations that require bearer tokens."""

    def __init__(
        self,
        transport: Middleware,
        auth_tokens: AuthTokens,
        certificate_store: CertificateStore,
    ) -> None:
        self._transport = transport
        self._auth_tokens = auth_tokens
        self._certificate_store = certificate_store
        self._authed_transport = BearerTokenMiddleware(
            transport, auth_tokens.access_token.token
        )

        self._session_eps = session.SessionEndpoints(self._authed_transport)
        self._encryption_eps = encryption.EncryptionEndpoints(self._transport)

    @property
    def auth_tokens(self) -> AuthTokens:
        return self._auth_tokens

    @property
    def access_token(self) -> str:
        return self._auth_tokens.access_token.token

    def _ensure_encryption_certificates_loaded(self) -> None:
        """Load public encryption certificates on first use."""
        if self._certificate_store.all():
            return

        self._certificate_store.load(
            [
                encryption_from_spec(cert)
                for cert in self._encryption_eps.fetch_public_certificates()
            ]
        )

    @property
    def refresh_token(self) -> str:
        return self._auth_tokens.refresh_token.token

    def get_encryption_key(self) -> tuple[bytes, bytes, bytes]:
        """Generate a session AES key, IV, and encrypted symmetric key payload."""
        self._ensure_encryption_certificates_loaded()

        cert = self._certificate_store.get_valid("symmetric_key_encryption")

        aes_key, iv = generate_session_key()
        encrypted_key = encrypt_symmetric_key(key=aes_key, cert_b64=cert.certificate)

        return aes_key, iv, encrypted_key

    def online_session(self, *, form_code: FormSchema) -> OnlineSessionClient:
        """Open a new online invoice session and return a bound session client."""
        aes_key, iv, encrypted_key = self.get_encryption_key()

        request = OpenOnlineSessionRequest(
            encrypted_key=encrypted_key,
            iv=iv,
            form_code=form_code,
        )
        session_data = session_from_spec(
            self._session_eps.open_online(session_to_spec(request))
        )

        state = OnlineSessionState.from_encoded(
            reference_number=session_data.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=self.access_token,
            valid_until=session_data.valid_until,
            form_code=form_code,
        )
        return OnlineSessionClient(transport=self._authed_transport, state=state)

    def batch_session(
        self,
        *,
        batch_file: BatchFileInfo,
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
    ) -> BatchSessionClient:
        """Open a new batch session and return a bound batch client."""
        aes_key, iv, encrypted_key = self.get_encryption_key()

        request = OpenBatchSessionRequest(
            encrypted_key=encrypted_key,
            iv=iv,
            batch_file=batch_file,
            form_code=form_code,
            offline_mode=offline_mode,
        )
        session_response = session_from_spec(
            self._session_eps.open_batch(body=session_to_spec(request))
        )

        state = BatchSessionState.from_encoded(
            reference_number=session_response.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=self.access_token,
            form_code=form_code,
            part_upload_requests=session_response.part_upload_requests,
        )
        return BatchSessionClient(transport=self._authed_transport, state=state)

    def resume_online_session(self, state: OnlineSessionState) -> OnlineSessionClient:
        """Rebind an existing serialized online session state to this client."""
        return OnlineSessionClient(transport=self._authed_transport, state=state)

    def resume_batch_session(self, state: "BatchSessionState") -> BatchSessionClient:
        """Rebind an existing serialized batch session state to this client."""
        return BatchSessionClient(transport=self._authed_transport, state=state)

    @cached_property
    def limits(self) -> LimitsClient:
        return LimitsClient(self._authed_transport)

    @cached_property
    def tokens(self) -> TokensClient:
        return TokensClient(self._authed_transport)

    @cached_property
    def certificates(self) -> CertificatesClient:
        return CertificatesClient(self._authed_transport)

    @cached_property
    def sessions(self) -> SessionManagementClient:
        return SessionManagementClient(self._authed_transport)

    @cached_property
    def session_log(self) -> InvoiceSessionLogClient:
        return InvoiceSessionLogClient(self._authed_transport)

    @cached_property
    def permissions(self) -> PermissionsClient:
        return PermissionsClient(self._authed_transport)

    @cached_property
    def invoices(self) -> InvoicesService:
        """Return the invoices service with encryption support configured."""
        return InvoicesService(
            self._authed_transport,
            self._certificate_store,
            client=InvoicesClient(self._authed_transport),
            ensure_encryption_certificates_loaded=(
                self._ensure_encryption_certificates_loaded
            ),
        )
