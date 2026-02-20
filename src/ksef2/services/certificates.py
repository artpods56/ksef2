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
from ksef2.infra.mappers.requests.certificates import (
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
    """Service for managing KSeF certificates.

    This service handles certificate enrollment, retrieval, revocation, and querying.
    It stores the access_token internally, so you don't need to pass it to every method.

    Typical usage:
        auth = client.auth.authenticate_xades(nip=nip, cert=cert, private_key=key)

        # Check certificate limits
        limits = auth.certificates.get_limits()

        # Get data for CSR generation
        enrollment_data = auth.certificates.get_enrollment_data()

        # Enroll a new certificate
        result = auth.certificates.enroll(
            certificate_name="My Certificate",
            certificate_type=CertificateType.AUTHENTICATION,
            csr=base64_csr,
        )

        # Query certificates
        certs = auth.certificates.query(status=CertificateStatus.ACTIVE)
    """

    def __init__(self, transport: protocols.Middleware, access_token: str) -> None:
        self._access_token = access_token
        self._limits_ep = CertificateLimitsEndpoint(transport)
        self._enrollment_data_ep = CertificateEnrollmentDataEndpoint(transport)
        self._enroll_ep = EnrollCertificateEndpoint(transport)
        self._enrollment_status_ep = CertificateEnrollmentStatusEndpoint(transport)
        self._retrieve_ep = RetrieveCertificatesEndpoint(transport)
        self._revoke_ep = RevokeCertificateEndpoint(transport)
        self._query_ep = QueryCertificatesEndpoint(transport)

    def get_limits(self) -> CertificateLimitsResponse:
        """Get certificate limits for the authenticated subject.

        Returns information about certificate limits and whether the user
        can request a new KSeF certificate.
        """
        spec_resp = self._limits_ep.send(self._access_token)
        return CertificateLimitsMapper.map_response(spec_resp)

    def get_enrollment_data(self) -> CertificateEnrollmentData:
        """Get data required for preparing a PKCS#10 certificate signing request.

        The data is returned based on the certificate used in the authentication
        process and identifies the subject making the certificate request.
        """
        spec_resp = self._enrollment_data_ep.send(self._access_token)
        return CertificateEnrollmentDataMapper.map_response(spec_resp)

    def enroll(
        self,
        *,
        certificate_name: str,
        certificate_type: CertificateType,
        csr: str,
        valid_from: datetime | None = None,
    ) -> EnrollCertificateResponse:
        """Submit a certificate enrollment request.

        Args:
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
            access_token=self._access_token,
            body=body.model_dump(exclude_none=True),
        )
        return EnrollCertificateMapper.map_response(spec_resp)

    def get_enrollment_status(
        self,
        *,
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
            access_token=self._access_token,
            reference_number=reference_number,
        )
        return CertificateEnrollmentStatusMapper.map_response(spec_resp)

    def retrieve(
        self,
        *,
        certificate_serial_numbers: list[str],
    ) -> RetrieveCertificatesResponse:
        """Retrieve certificates by their serial numbers.

        Args:
            certificate_serial_numbers: List of certificate serial numbers
                                       (1-10 items, hex format).

        Returns:
            Certificates in DER format encoded as Base64.
        """
        body = RetrieveCertificatesMapper.map_request(certificate_serial_numbers)
        spec_resp = self._retrieve_ep.send(
            access_token=self._access_token,
            body=body.model_dump(),
        )
        return RetrieveCertificatesMapper.map_response(spec_resp)

    def revoke(
        self,
        *,
        certificate_serial_number: str,
        revocation_reason: CertificateRevocationReason | None = None,
    ) -> None:
        """Revoke a certificate by its serial number.

        Args:
            certificate_serial_number: Serial number of the certificate (hex format).
            revocation_reason: Optional reason for revocation.
        """
        body = RevokeCertificateMapper.map_request(revocation_reason)
        self._revoke_ep.send(
            access_token=self._access_token,
            certificate_serial_number=certificate_serial_number,
            body=body.model_dump(exclude_none=True),
        )

    def query(
        self,
        *,
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
            access_token=self._access_token,
            body=body.model_dump(exclude_none=True),
            page_size=page_size,
            page_offset=page_offset,
        )
        return QueryCertificatesMapper.map_response(spec_resp)
