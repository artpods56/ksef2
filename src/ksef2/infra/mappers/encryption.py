from ksef2.infra.schema.api import spec as spec

from ksef2.domain.models import encryption


class PublicKeyCertificateMapper:
    @staticmethod
    def map_response(
        response: list[spec.PublicKeyCertificate],
    ) -> list[encryption.PublicKeyCertificate]:
        return [
            encryption.PublicKeyCertificate(
                certificate=item.certificate,
                valid_from=item.validFrom,
                valid_to=item.validTo,
                usage=[encryption.CertUsage(usage) for usage in item.usage],
            )
            for item in response
        ]
