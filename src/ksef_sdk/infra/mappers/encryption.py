from ksef_sdk.infra.schema import model as spec

from ksef_sdk.domain.models import encryption


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
