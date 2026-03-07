from collections.abc import Iterator
from datetime import datetime
from typing import final

from ksef2.core.protocols import Middleware
from ksef2.domain.models.certificates import (
    CertificateEnrollmentData,
    CertificateEnrollmentResponse,
    CertificateEnrollmentStatusResponse,
    CertificateInfo,
    CertificateLimitsResponse,
    CertificatesInfoList,
    CertificateStatusValue,
    CertificateTypeValue,
    EnrollCertificateRequest,
    QueryCertificatesRequest,
    RetrieveCertificatesRequest,
    RetrievedCertificatesList,
    RevocationReason,
    RevokeCertificateRequest,
)
from ksef2.domain.models.pagination import OffsetPaginationParams
from ksef2.endpoints.certificates import CertificatesEndpoints

from ksef2.infra.mappers.certificates import from_spec, to_spec


@final
class CertificatesClient:
    def __init__(self, transport: Middleware) -> None:
        self._endpoints = CertificatesEndpoints(transport)

    def get_limits(self) -> CertificateLimitsResponse:
        return from_spec(self._endpoints.get_limits())

    def get_enrollment_data(self) -> CertificateEnrollmentData:
        return from_spec(self._endpoints.get_enrollment_data())

    def enroll(
        self,
        *,
        certificate_name: str,
        certificate_type: CertificateTypeValue,
        csr: str,
        valid_from: datetime | str | None = None,
    ) -> CertificateEnrollmentResponse:
        request = EnrollCertificateRequest(
            certificate_name=certificate_name,
            certificate_type=certificate_type,
            csr=csr,
            valid_from=valid_from,
        )
        body = to_spec(request)
        return from_spec(self._endpoints.enroll(body=body))

    def get_enrollment_status(
        self,
        *,
        reference_number: str,
    ) -> CertificateEnrollmentStatusResponse:
        return from_spec(
            self._endpoints.get_enrollment_status(
                reference_number=reference_number,
            )
        )

    def retrieve(
        self,
        *,
        certificate_serial_numbers: list[str],
    ) -> RetrievedCertificatesList:
        request = RetrieveCertificatesRequest(
            certificate_serial_numbers=certificate_serial_numbers,
        )
        body = to_spec(request)
        return from_spec(self._endpoints.retrieve(body=body))

    def revoke(
        self,
        *,
        certificate_serial_number: str,
        reason: RevocationReason | None = None,
    ) -> None:

        request = RevokeCertificateRequest(revocation_reason=reason)
        body = to_spec(request)
        self._endpoints.revoke(
            certificate_serial_number=certificate_serial_number,
            body=body,
        )

    def query(
        self,
        *,
        name: str | None = None,
        certificate_serial_number: str | None = None,
        certificate_type: CertificateTypeValue | None = None,
        status: CertificateStatusValue | None = None,
        expires_after: datetime | str | None = None,
        params: OffsetPaginationParams | None = None,
    ) -> CertificatesInfoList:
        parameters = params or OffsetPaginationParams()

        request = QueryCertificatesRequest(
            certificate_serial_number=certificate_serial_number,
            name=name,
            certificate_type=certificate_type,
            status=status,
            expires_after=expires_after,
        )
        body = to_spec(request)
        spec_resp = self._endpoints.query(body=body, **parameters.to_query_params())
        return from_spec(spec_resp)

    def all(
        self,
        *,
        certificate_serial_number: str | None = None,
        name: str | None = None,
        certificate_type: CertificateTypeValue | None = None,
        status: CertificateStatusValue | None = None,
        expires_after: datetime | str | None = None,
        params: OffsetPaginationParams | None = None,
    ) -> Iterator[CertificateInfo]:
        current_params = params or OffsetPaginationParams()

        while True:
            response = self.query(
                name=name,
                certificate_serial_number=certificate_serial_number,
                certificate_type=certificate_type,
                status=status,
                expires_after=expires_after,
                params=current_params,
            )
            yield from response.certificates

            if not response.has_more:
                break

            current_params = current_params.next_page()
