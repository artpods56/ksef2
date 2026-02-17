from __future__ import annotations

from datetime import datetime
from typing import final

from ksef2.core import protocols
from ksef2.domain.models.certificates import (
    CertificateEnrollmentData,
    CertificateEnrollmentStatus,
    CertificateLimitsResponse,
    CertificateRevocationReason,
    CertificateStatus,
    CertificateType,
    EnrollCertificateResponse,
    QueryCertificatesResponse,
    RetrieveCertificatesResponse,
)
from ksef2.endpoints.certificates import (
    CertificateEnrollmentDataEndpoint,
    CertificateEnrollmentStatusEndpoint,
    CertificateLimitsEndpoint,
    EnrollCertificateEndpoint,
    QueryCertificatesEndpoint,
    RetrieveCertificatesEndpoint,
    RevokeCertificateEndpoint,
)
from ksef2.infra.mappers.certificates import (
    CertificateEnrollmentDataMapper,
    CertificateEnrollmentStatusMapper,
    CertificateLimitsMapper,
    EnrollCertificateMapper,
    QueryCertificatesMapper,
    RetrieveCertificatesMapper,
    RevokeCertificateMapper,
)


@final
class CertificateService:
    """Service for managing KSeF certificates."""

    def __init__(self, transport: protocols.Middleware) -> None:
        self._limits_ep = CertificateLimitsEndpoint(transport)
        self._enrollment_data_ep = CertificateEnrollmentDataEndpoint(transport)
        self._enroll_ep = EnrollCertificateEndpoint(transport)
        self._enrollment_status_ep = CertificateEnrollmentStatusEndpoint(transport)
        self._retrieve_ep = RetrieveCertificatesEndpoint(transport)
        self._revoke_ep = RevokeCertificateEndpoint(transport)
        self._query_ep = QueryCertificatesEndpoint(transport)

    def get_limits(
        self,
        *,
        access_token: str,
    ) -> CertificateLimitsResponse:
        """Get certificate limits for the authenticated subject.

        Returns information about certificate limits and whether the user
        can request a new KSeF certificate.
        """
        spec_resp = self._limits_ep.send(access_token)
        return CertificateLimitsMapper.map_response(spec_resp)

    def get_enrollment_data(
        self,
        *,
        access_token: str,
    ) -> CertificateEnrollmentData:
        """Get data required for preparing a PKCS#10 certificate signing request.

        The data is returned based on the certificate used in the authentication
        process and identifies the subject making the certificate request.
        """
        spec_resp = self._enrollment_data_ep.send(access_token)
        return CertificateEnrollmentDataMapper.map_response(spec_resp)

    def enroll(
        self,
        *,
        access_token: str,
        certificate_name: str,
        certificate_type: CertificateType,
        csr: str,
        valid_from: datetime | None = None,
    ) -> EnrollCertificateResponse:
        """Submit a certificate enrollment request.

        Args:
            access_token: The bearer access token.
            certificate_name: Custom name for the certificate (5-100 chars).
            certificate_type: Type of certificate (Authentication or Offline).
            csr: The PKCS#10 CSR in DER format, encoded as Base64.
            valid_from: Optional validity start date. If not provided,
                       the certificate will be valid from issuance.

        Returns:
            Reference number and timestamp of the enrollment request.
        """
        body = EnrollCertificateMapper.map_request(
            certificate_name=certificate_name,
            certificate_type=certificate_type,
            csr=csr,
            valid_from=valid_from,
        )
        spec_resp = self._enroll_ep.send(
            access_token=access_token,
            body=body.model_dump(exclude_none=True),
        )
        return EnrollCertificateMapper.map_response(spec_resp)

    def get_enrollment_status(
        self,
        *,
        access_token: str,
        reference_number: str,
    ) -> CertificateEnrollmentStatus:
        """Get the status of a certificate enrollment request.

        Status codes:
        - 100: Request accepted for processing
        - 200: Request processed (certificate generated)
        - 400: Request rejected
        - 500: Unknown error
        - 550: Operation cancelled by system
        """
        spec_resp = self._enrollment_status_ep.send(
            access_token=access_token,
            reference_number=reference_number,
        )
        return CertificateEnrollmentStatusMapper.map_response(spec_resp)

    def retrieve(
        self,
        *,
        access_token: str,
        certificate_serial_numbers: list[str],
    ) -> RetrieveCertificatesResponse:
        """Retrieve certificates by their serial numbers.

        Args:
            access_token: The bearer access token.
            certificate_serial_numbers: List of certificate serial numbers
                                       (1-10 items, hex format).

        Returns:
            Certificates in DER format encoded as Base64.
        """
        body = RetrieveCertificatesMapper.map_request(certificate_serial_numbers)
        spec_resp = self._retrieve_ep.send(
            access_token=access_token,
            body=body.model_dump(),
        )
        return RetrieveCertificatesMapper.map_response(spec_resp)

    def revoke(
        self,
        *,
        access_token: str,
        certificate_serial_number: str,
        revocation_reason: CertificateRevocationReason | None = None,
    ) -> None:
        """Revoke a certificate by its serial number.

        Args:
            access_token: The bearer access token.
            certificate_serial_number: Serial number of the certificate (hex format).
            revocation_reason: Optional reason for revocation.
        """
        body = RevokeCertificateMapper.map_request(revocation_reason)
        self._revoke_ep.send(
            access_token=access_token,
            certificate_serial_number=certificate_serial_number,
            body=body.model_dump(exclude_none=True),
        )

    def query(
        self,
        *,
        access_token: str,
        certificate_serial_number: str | None = None,
        name: str | None = None,
        certificate_type: CertificateType | None = None,
        status: CertificateStatus | None = None,
        expires_after: datetime | None = None,
        page_size: int | None = None,
        page_offset: int | None = None,
    ) -> QueryCertificatesResponse:
        """Query certificates matching the specified criteria.

        All filter parameters are optional. If no criteria are provided,
        returns all certificates for the authenticated subject.

        Args:
            access_token: The bearer access token.
            certificate_serial_number: Exact match on serial number.
            name: Partial match on certificate name (contains).
            certificate_type: Filter by certificate type.
            status: Filter by certificate status.
            expires_after: Filter certificates expiring after this date.
            page_size: Number of results per page (10-50, default 10).
            page_offset: Page number (0-indexed, default 0).

        Returns:
            List of certificates and pagination info.
        """
        body = QueryCertificatesMapper.map_request(
            certificate_serial_number=certificate_serial_number,
            name=name,
            certificate_type=certificate_type,
            status=status,
            expires_after=expires_after,
        )
        spec_resp = self._query_ep.send(
            access_token=access_token,
            body=body.model_dump(exclude_none=True),
            page_size=page_size,
            page_offset=page_offset,
        )
        return QueryCertificatesMapper.map_response(spec_resp)
