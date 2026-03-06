from typing import final

from ksef2.core.protocols import Middleware
from ksef2.domain.models.encryption import CertUsage, PublicKeyCertificate
from ksef2.endpoints.encryption import EncryptionEndpoints
from ksef2.infra.mappers.encryption import from_spec, to_spec


@final
class EncryptionClient:
    def __init__(self, transport: Middleware) -> None:
        self._endpoints = EncryptionEndpoints(transport)

    def get_certificates(
        self,
        *,
        usage: list[CertUsage] | None = None,
    ) -> list[PublicKeyCertificate]:
        certificates = [
            from_spec(cert) for cert in self._endpoints.fetch_public_certificates()
        ]

        if usage is None:
            return certificates

        requested = {to_spec(value) for value in usage}
        return [
            cert
            for cert in certificates
            if any(to_spec(cert_usage) in requested for cert_usage in cert.usage)
        ]
