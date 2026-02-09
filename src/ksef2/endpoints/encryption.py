from typing import final
from ksef2.core.http import HttpTransport
from ksef2.core.codecs import JsonResponseCodec
from ksef2.infra.schema import model as spec


@final
class CertificateEndpoint:
    """Endpoint for fetching public-key certificates.

    API Documentation:
        `https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Certyfikaty-klucza-publicznego/paths/~1security~1public-key-certificates/get`
    """

    url: str = "/security/public-key-certificates"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def fetch(
        self,
    ) -> list[spec.PublicKeyCertificate]:
        return JsonResponseCodec.parse_list(
            self._transport.get(
                self.url,
            ),
            spec.PublicKeyCertificate,
        )
