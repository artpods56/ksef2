"""Authenticated client for operations requiring only a bearer token."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, final

from ksef2.clients.batch import BatchSessionClient
from ksef2.clients.online import OnlineSessionClient
from ksef2.core import exceptions
from ksef2.core.crypto import generate_session_key, encrypt_symmetric_key
from ksef2.core.stores import CertificateStore
from ksef2.domain.models.auth import AuthTokens
from ksef2.domain.models.encryption import CertUsage
from ksef2.domain.models.session import FormSchema, OnlineSessionState
from ksef2.endpoints.encryption import CertificateEndpoint
from ksef2.endpoints.session import OpenSessionEndpoint, OpenBatchSessionEndpoint
from ksef2.infra.mappers.requests.batch import BatchSessionMapper
from ksef2.infra.mappers.requests.encryption import PublicKeyCertificateMapper
from ksef2.infra.mappers.requests.sessions import OpenOnlineSessionMapper
from ksef2.services import PermissionsService
from ksef2.services.certificates import CertificateService
from ksef2.services.limits import LimitsService
from ksef2.services.session import InvoiceSessionQueryService
from ksef2.services.session_management import SessionManagementService
from ksef2.services.tokens import TokenService

if TYPE_CHECKING:
    from ksef2.core import protocols
    from ksef2.domain.models import BatchSessionState
    from ksef2.domain.models.batch import BatchFileInfo


@final
class AuthenticatedClient:
    """Client for authenticated operations.

    This client holds authentication tokens and provides access to services
    that need authentication, and methods for opening invoice sessions.

    Typical usage:
        auth = client.auth.authenticate_xades(nip=nip, cert=cert, private_key=key)

        # Access limits without opening a session
        limits = auth.limits.get_context_limits()

        # Open an online session directly — no manual token passing
        with auth.online_session(form_code=FormSchema.FA3) as session:
            session.send_invoice(invoice_xml=xml_bytes)

        # Open a batch session
        batch = auth.batch_session(batch_file=batch_file)
    """

    def __init__(
        self,
        transport: "protocols.Middleware",
        auth_tokens: AuthTokens,
        certificate_store: CertificateStore,
    ) -> None:
        self._transport = transport
        self._auth_tokens = auth_tokens
        self._certificate_store = certificate_store
        self._certificates_ep = CertificateEndpoint(transport)
        self._open_session_ep = OpenSessionEndpoint(transport)
        self._open_batch_ep = OpenBatchSessionEndpoint(transport)

    @property
    def auth_tokens(self) -> AuthTokens:
        """Get the full authentication tokens (for backward compatibility)."""
        return self._auth_tokens

    @property
    def access_token(self) -> str:
        """Get the access token string for this authenticated context."""
        return self._auth_tokens.access_token.token

    @property
    def refresh_token(self) -> str:
        """Get the refresh token string."""
        return self._auth_tokens.refresh_token.token

    def get_encryption_key(self) -> tuple[bytes, bytes, bytes]:
        """Generate AES session key and encrypt it with the server certificate.

        Returns:
            Tuple of (aes_key, iv, encrypted_key).
        """
        # if certstore is empty, fetch certificates from server
        if not self._certificate_store.all():
            self._certificate_store.load(
                PublicKeyCertificateMapper.map_response(self._certificates_ep.fetch())
            )

        cert = self._certificate_store.get_valid(CertUsage.SYMMETRIC_KEY_ENCRYPTION)

        if cert is None:
            raise exceptions.NoCertificateAvailableError(
                "No valid certificate for SymmetricKeyEncryption found."
            )

        aes_key, iv = generate_session_key()
        encrypted_key = encrypt_symmetric_key(key=aes_key, cert_b64=cert.certificate)

        return aes_key, iv, encrypted_key

    def online_session(self, *, form_code: FormSchema) -> OnlineSessionClient:
        """Open an online invoice session.

        The returned client can be used as a context manager to automatically
        terminate the session on exit.

        Args:
            form_code: Invoice schema to use (e.g. FormSchema.FA3).

        Returns:
            OnlineSessionClient for sending invoices and managing the session.
        """
        aes_key, iv, encrypted_key = self.get_encryption_key()

        body = OpenOnlineSessionMapper.map_request(encrypted_key, iv, form_code)
        session_data = OpenOnlineSessionMapper.map_response(
            self._open_session_ep.send(
                access_token=self.access_token, body=body.model_dump()
            )
        )

        state = OnlineSessionState.from_encoded(
            reference_number=session_data.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=self.access_token,
            valid_until=session_data.valid_until,
            form_code=form_code,
        )
        return OnlineSessionClient(transport=self._transport, state=state)

    def batch_session(
        self,
        *,
        batch_file: "BatchFileInfo",
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
    ) -> BatchSessionClient:
        """Open a batch session for uploading invoices in bulk.

        Args:
            batch_file: Information about the batch file to upload.
            form_code: Invoice schema to use. Defaults to FA3.
            offline_mode: Whether offline invoicing mode is declared.

        Returns:
            BatchSessionClient for managing the batch session.
        """

        aes_key, iv, encrypted_key = self.get_encryption_key()

        body = BatchSessionMapper.map_request(
            encrypted_key=encrypted_key,
            iv=iv,
            batch_file=batch_file,
            form_code=form_code,
            offline_mode=offline_mode,
        )
        response = self._open_batch_ep.send(
            access_token=self.access_token, body=body.model_dump()
        )
        session_response = BatchSessionMapper.map_response(response)

        state = BatchSessionState.from_encoded(
            reference_number=session_response.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=self.access_token,
            form_code=form_code,
            part_upload_requests=session_response.part_upload_requests,
        )
        return BatchSessionClient(transport=self._transport, state=state)

    def resume_online_session(self, state: OnlineSessionState) -> OnlineSessionClient:
        """Resume an online session from saved state."""
        return OnlineSessionClient(transport=self._transport, state=state)

    def resume_batch_session(self, state: "BatchSessionState") -> BatchSessionClient:
        """Resume a batch session from saved state."""
        return BatchSessionClient(transport=self._transport, state=state)

    # -- Authenticated service accessors ---------------------------------------

    @cached_property
    def limits(self) -> LimitsService:
        """Access limits service for querying and modifying API limits."""
        return LimitsService(self._transport, self.access_token)

    @cached_property
    def tokens(self) -> TokenService:
        """Access token service for managing KSeF authorization tokens."""
        return TokenService(self._transport, self.access_token)

    @cached_property
    def certificates(self) -> CertificateService:
        """Access certificate service for managing KSeF certificates."""
        return CertificateService(self._transport, self.access_token)

    @cached_property
    def sessions(self) -> SessionManagementService:
        """Access session management service for listing/terminating auth sessions."""
        return SessionManagementService(self._transport, self.access_token)

    @cached_property
    def session_log(self) -> InvoiceSessionQueryService:
        """Query invoice processing history (online and batch sessions)."""
        return InvoiceSessionQueryService(self._transport, self.access_token)

    @cached_property
    def permissions(self) -> PermissionsService:
        """Access permissions service for managing KSeF permissions."""
        return PermissionsService(self._transport, self.access_token)
