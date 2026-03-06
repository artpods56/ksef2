from ksef2.infra.mappers.certificates.overloads import from_spec
from ksef2.infra.schema.api.spec import CertificateLimitsResponse, CertificateLimit

x = CertificateLimitsResponse(
    canRequest=True,
    enrollment=CertificateLimit(remaining=10, limit=100),
    certificate=CertificateLimit(remaining=10, limit=100),
)

translated = from_spec(x)
print(translated.model_dump_json(indent=2))
