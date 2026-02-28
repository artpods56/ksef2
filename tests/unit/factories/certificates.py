from base64 import b64encode

from ksef2.infra.schema.api import spec
from ksef2.infra.schema.api.spec.models import RetrieveCertificatesListItem
from ksef2.infra.schema.api.supp.invoices import (
    EnrollCertificateRequest,
    QueryCertificatesRequest,
    RetrieveCertificatesRequest,
    RevokeCertificateRequest,
)
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

_VALID_BASE64 = b64encode(b"polyfactory-test-certificate-data").decode()


@register_fixture(name="cert_limits_resp")
class CertificateLimitsResponseFactory(
    ModelFactory[spec.CertificateLimitsResponse]
): ...


@register_fixture(name="cert_enrollment_data_resp")
class CertificateEnrollmentDataResponseFactory(
    ModelFactory[spec.CertificateEnrollmentDataResponse]
): ...


@register_fixture(name="cert_enroll_req")
class EnrollCertificateRequestFactory(ModelFactory[EnrollCertificateRequest]): ...


@register_fixture(name="cert_enroll_resp")
class EnrollCertificateResponseFactory(
    ModelFactory[spec.EnrollCertificateResponse]
): ...


@register_fixture(name="cert_enrollment_status_resp")
class CertificateEnrollmentStatusResponseFactory(
    ModelFactory[spec.CertificateEnrollmentStatusResponse]
): ...


@register_fixture(name="cert_retrieve_req")
class RetrieveCertificatesRequestFactory(ModelFactory[RetrieveCertificatesRequest]): ...


class RetrieveCertificatesListItemFactory(ModelFactory[RetrieveCertificatesListItem]):
    certificate = _VALID_BASE64


@register_fixture(name="cert_retrieve_resp")
class RetrieveCertificatesResponseFactory(
    ModelFactory[spec.RetrieveCertificatesResponse]
):
    @classmethod
    def certificates(cls) -> list[RetrieveCertificatesListItem]:
        return [RetrieveCertificatesListItemFactory.build()]


@register_fixture(name="cert_revoke_req")
class RevokeCertificateRequestFactory(ModelFactory[RevokeCertificateRequest]): ...


@register_fixture(name="cert_query_req")
class QueryCertificatesRequestFactory(ModelFactory[QueryCertificatesRequest]): ...


@register_fixture(name="cert_query_resp")
class QueryCertificatesResponseFactory(
    ModelFactory[spec.QueryCertificatesResponse]
): ...
