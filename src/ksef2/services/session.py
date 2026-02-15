from typing import final

from ksef2.clients.session import OnlineSessionClient
from ksef2.clients.encryption import EncryptionClient
from ksef2.core import exceptions
from ksef2.core.crypto import (
    generate_session_key,
    encrypt_symmetric_key,
)
from ksef2.core import protocols
from ksef2.core.stores import CertificateStore
from ksef2.domain.models import FormSchema
from ksef2.domain.models.encryption import CertUsage
from ksef2.domain.models.session import SessionState
from ksef2.endpoints.session import OpenSessionEndpoint
from ksef2.infra.mappers.session import OpenOnlineSessionMapper


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

        state = SessionState.from_encoded(
            reference_number=session_data.reference_number,
            aes_key=aes_key,
            iv=iv,
            access_token=access_token,
            valid_until=session_data.valid_until,
            form_code=form_code,
        )

        return OnlineSessionClient(transport=self._transport, state=state)

    def resume(self, state: SessionState) -> "OnlineSessionClient":
        return OnlineSessionClient(transport=self._transport, state=state)
