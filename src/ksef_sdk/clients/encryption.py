from typing import final
from ksef_sdk.core.http import HttpTransport
from ksef_sdk.domain.models.encryption import PublicKeyCertificate
from ksef_sdk.endpoints import encryption
from ksef_sdk.infra.mappers.encryption import PublicKeyCertificateMapper


@final
class EncryptionClient:
    def __init__(self, transport: HttpTransport):
        self._cert_endpoint = encryption.CertificateEndpoint(transport)

    def get_certificates(self) -> list[PublicKeyCertificate]:
        return PublicKeyCertificateMapper.map_response(self._cert_endpoint.fetch())
