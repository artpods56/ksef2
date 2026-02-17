from typing import final, TYPE_CHECKING

from ksef2.clients.session import OnlineSessionClient
from ksef2.clients.encryption import EncryptionClient
from ksef2.core import exceptions
from ksef2.core.crypto import (
    generate_session_key,
    encrypt_symmetric_key,
)
from ksef2.core import protocols
from ksef2.core.stores import CertificateStore
from ksef2.domain.models import FormSchema, BatchSessionState
from ksef2.domain.models.batch import BatchFileInfo
from ksef2.domain.models.encryption import CertUsage
from ksef2.domain.models.session import OnlineSessionState, QuerySessionsList
from ksef2.endpoints.invoices import ListSessionsEndpoint
from ksef2.endpoints.session import OpenSessionEndpoint, OpenBatchSessionEndpoint
from ksef2.infra.mappers.batch import BatchSessionMapper
from ksef2.infra.mappers.session import OpenOnlineSessionMapper
from ksef2.infra.schema.api import spec as spec

if TYPE_CHECKING:
    from ksef2.clients.batch import BatchSessionClient


@final
class OpenSessionService:
    def __init__(
        self,
        transport: protocols.Middleware,
        certificate_store: CertificateStore,
    ):
        self._transport = transport
        self._certificates = EncryptionClient(transport)
        self._open_session = OpenSessionEndpoint(transport)
        self._open_batch_ep = OpenBatchSessionEndpoint(transport)
        self._list_sessions_ep = ListSessionsEndpoint(transport)
        self._certificate_store = certificate_store

    def open_online(
        self,
        *,
        access_token: str,
        form_code: FormSchema,
    ) -> OnlineSessionClient:
        if not self._certificate_store.all():
            self._certificate_store.load(self._certificates.get_certificates())

        symmetric_key_cert = self._certificate_store.get_valid(
            CertUsage.SYMMETRIC_KEY_ENCRYPTION
        )
        if symmetric_key_cert is None:
            raise exceptions.NoCertificateAvailableError(
                "No valid certificate for SymmetricKeyEncryption found."
            )
        aes_key, iv = generate_session_key()

        encrypted_key = encrypt_symmetric_key(
            key=aes_key, cert_b64=symmetric_key_cert.certificate
        )

        body = OpenOnlineSessionMapper.map_request(encrypted_key, iv, form_code)

        session_data = OpenOnlineSessionMapper.map_response(
            self._open_session.send(access_token=access_token, body=body.model_dump())
        )

        state = OnlineSessionState.from_encoded(
            reference_number=session_data.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=access_token,
            valid_until=session_data.valid_until,
            form_code=form_code,
        )

        return OnlineSessionClient(transport=self._transport, state=state)

    def list(
        self, *, access_token: str, query: QuerySessionsList
    ) -> spec.SessionsQueryResponse:
        return self._list_sessions_ep.send(
            access_token=access_token,
            **query.model_dump(by_alias=True, exclude_none=True),
        )

    def resume(self, state: OnlineSessionState) -> "OnlineSessionClient":
        return OnlineSessionClient(transport=self._transport, state=state)

    def open_batch(
        self,
        *,
        access_token: str,
        batch_file: BatchFileInfo,
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
    ) -> "BatchSessionClient":
        """Open a batch session for uploading invoices in bulk.

        Args:
            access_token: Bearer token for authentication.
            batch_file: Information about the batch file to upload.
            form_code: Invoice schema to use. Defaults to FA3.
            offline_mode: Whether offline invoicing mode is declared.

        Returns:
            BatchSessionClient for managing the batch session.

        Raises:
            NoCertificateAvailableError: If no valid encryption certificate is found.
        """
        # Lazy import to avoid circular dependency
        from ksef2.clients.batch import BatchSessionClient

        if not self._certificate_store.all():
            self._certificate_store.load(self._certificates.get_certificates())

        symmetric_key_cert = self._certificate_store.get_valid(
            CertUsage.SYMMETRIC_KEY_ENCRYPTION
        )
        if symmetric_key_cert is None:
            raise exceptions.NoCertificateAvailableError(
                "No valid certificate for SymmetricKeyEncryption found."
            )

        aes_key, iv = generate_session_key()
        encrypted_key = encrypt_symmetric_key(
            key=aes_key, cert_b64=symmetric_key_cert.certificate
        )

        body = BatchSessionMapper.map_request(
            encrypted_key=encrypted_key,
            iv=iv,
            batch_file=batch_file,
            form_code=form_code,
            offline_mode=offline_mode,
        )

        response = self._open_batch_ep.send(
            access_token=access_token,
            body=body.model_dump(),
        )

        session_response = BatchSessionMapper.map_response(response)

        state = BatchSessionState.from_encoded(
            reference_number=session_response.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=access_token,
            form_code=form_code,
            part_upload_requests=session_response.part_upload_requests,
        )

        return BatchSessionClient(
            transport=self._transport,
            state=state,
        )

    def resume_batch(self, state: BatchSessionState) -> "BatchSessionClient":
        """Resume a batch session from saved state.

        Args:
            state: Previously saved BatchSessionState.

        Returns:
            BatchSessionClient for managing the batch session.
        """
        from ksef2.clients.batch import BatchSessionClient

        return BatchSessionClient(transport=self._transport, state=state)
