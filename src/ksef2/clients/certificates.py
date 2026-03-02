from datetime import datetime
from typing import final

from ksef2.core.protocols import Middleware
from ksef2.domain.models.certificates import (
    CertificateEnrollmentData,
    CertificateLimitsResponse,
    CertificateEnrollmentStatusResponse,
    RetrievedCertificatesList,
    CertificatesInfoList,
    CertificateType,
    CertificateStatus,
    RevocationReason,
    CertificateEnrollmentResponse,
)
from ksef2.domain.models.pagination import OffsetPaginationParams
from ksef2.endpoints.certificates import CertificatesEndpoints

from ksef2.infra.mappers.requests.certificates import (
    CertificatesMapper,
)


@final
class CertificatesClient:
    def __init__(self, transport: Middleware) -> None:
        self._endpoints = CertificatesEndpoints(transport)

    def get_limits(self) -> CertificateLimitsResponse:
        return CertificatesMapper.map_get_limits_response(self._endpoints.get_limits())

    def get_enrollment_data(self) -> CertificateEnrollmentData:
        return CertificatesMapper.map_get_enrolment_data_response(
            self._endpoints.get_enrollment_data()
        )

    def enroll(
        self,
        *,
        certificate_name: str,
        certificate_type: CertificateType,
        csr: str,
        valid_from: datetime | str | None = None,
    ) -> CertificateEnrollmentResponse:
        body = CertificatesMapper.map_entroll_request(
            certificate_name=certificate_name,
            certificate_type=certificate_type,
            csr=csr,
            valid_from=valid_from,
        )
        return CertificatesMapper.map_cert_enrollment_response(
            self._endpoints.enroll(body=body)
        )

    def get_enrollment_status(
        self,
        *,
        reference_number: str,
    ) -> CertificateEnrollmentStatusResponse:
        return CertificatesMapper.map_get_enrollment_status_response(
            self._endpoints.get_enrollment_status(
                reference_number=reference_number,
            )
        )

    def retrieve(
        self,
        *,
        certificate_serial_numbers: list[str],
    ) -> RetrievedCertificatesList:
        body = CertificatesMapper.map_retrieve_certificates_request(
            certificate_serial_numbers
        )
        return CertificatesMapper.map_retrieve_certificates_response(
            self._endpoints.retrieve(body=body)
        )

    def revoke(
        self,
        *,
        certificate_serial_number: str,
        reason: RevocationReason | None = None,
    ) -> None:

        body = CertificatesMapper.map_revoke_request(reason)
        self._endpoints.revoke(
            certificate_serial_number=certificate_serial_number,
            body=body,
        )

    def query(
        self,
        *,
        certificate_serial_number: str | None = None,
        name: str | None = None,
        certificate_type: CertificateType | None = None,
        status: CertificateStatus | None = None,
        expiration_date: datetime | str | None = None,
        params: OffsetPaginationParams | None = None,
    ) -> CertificatesInfoList:
        parameters = params or OffsetPaginationParams()
        body = CertificatesMapper.map_query_request(
            certificate_serial_number,
            name,
            certificate_type,
            status,
            expiration_date,
        )
        spec_resp = self._endpoints.query(body=body, **parameters.to_query_params())
        return CertificatesMapper.map_query_response(spec_resp)
