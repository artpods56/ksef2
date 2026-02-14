from typing import final
from ksef2.core import protocols
from ksef2.domain.models.encryption import PublicKeyCertificate
from ksef2.endpoints import encryption
from ksef2.infra.mappers.encryption import PublicKeyCertificateMapper


@final
class EncryptionClient:
    def __init__(self, transport: protocols.Middleware):
        self._cert_endpoint = encryption.CertificateEndpoint(transport)

    def get_certificates(self) -> list[PublicKeyCertificate]:
        return PublicKeyCertificateMapper.map_response(self._cert_endpoint.fetch())
