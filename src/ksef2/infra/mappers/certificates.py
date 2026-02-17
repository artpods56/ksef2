from __future__ import annotations

from datetime import datetime

from ksef2.domain.models.certificates import (
    CertificateEnrollmentData,
    CertificateEnrollmentStatus,
    CertificateInfo,
    CertificateLimit,
    CertificateLimitsResponse,
    CertificateRevocationReason,
    CertificateStatus,
    CertificateSubjectIdentifier,
    CertificateSubjectIdentifierType,
    CertificateType,
    EnrollCertificateResponse,
    QueryCertificatesResponse,
    RetrieveCertificatesResponse,
    RetrievedCertificate,
    StatusInfo,
)
from ksef2.infra.schema.api import spec


class CertificateLimitsMapper:
    @staticmethod
    def map_response(r: spec.CertificateLimitsResponse) -> CertificateLimitsResponse:
        return CertificateLimitsResponse(
            can_request=r.canRequest,
            enrollment=CertificateLimit(
                limit=r.enrollment.limit,
                remaining=r.enrollment.remaining,
            ),
            certificate=CertificateLimit(
                limit=r.certificate.limit,
                remaining=r.certificate.remaining,
            ),
        )


class CertificateEnrollmentDataMapper:
    @staticmethod
    def map_response(
        r: spec.CertificateEnrollmentDataResponse,
    ) -> CertificateEnrollmentData:
        return CertificateEnrollmentData(
            common_name=r.commonName,
            country_name=r.countryName,
            given_name=r.givenName,
            surname=r.surname,
            serial_number=r.serialNumber,
            unique_identifier=r.uniqueIdentifier,
            organization_name=r.organizationName,
            organization_identifier=r.organizationIdentifier,
        )


class EnrollCertificateMapper:
    @staticmethod
    def map_request(
        certificate_name: str,
        certificate_type: CertificateType,
        csr: str,
        valid_from: datetime | None = None,
    ) -> spec.EnrollCertificateRequest:
        return spec.EnrollCertificateRequest(
            certificateName=certificate_name,
            certificateType=spec.KsefCertificateType(certificate_type.value),
            csr=csr,
            validFrom=valid_from,
        )

    @staticmethod
    def map_response(r: spec.EnrollCertificateResponse) -> EnrollCertificateResponse:
        return EnrollCertificateResponse(
            reference_number=r.referenceNumber,
            timestamp=r.timestamp,
        )


class CertificateEnrollmentStatusMapper:
    @staticmethod
    def map_response(
        r: spec.CertificateEnrollmentStatusResponse,
    ) -> CertificateEnrollmentStatus:
        return CertificateEnrollmentStatus(
            request_date=r.requestDate,
            status=StatusInfo(
                code=r.status.code,
                description=r.status.description,
                details=r.status.details,
            ),
            certificate_serial_number=r.certificateSerialNumber,
        )


class RetrieveCertificatesMapper:
    @staticmethod
    def map_request(
        certificate_serial_numbers: list[str],
    ) -> spec.RetrieveCertificatesRequest:
        return spec.RetrieveCertificatesRequest(
            certificateSerialNumbers=certificate_serial_numbers,
        )

    @staticmethod
    def map_response(
        r: spec.RetrieveCertificatesResponse,
    ) -> RetrieveCertificatesResponse:
        return RetrieveCertificatesResponse(
            certificates=[
                RetrievedCertificate(
                    certificate=c.certificate,
                    certificate_name=c.certificateName,
                    certificate_serial_number=c.certificateSerialNumber,
                    certificate_type=CertificateType(c.certificateType.value),
                )
                for c in r.certificates
            ],
        )


class RevokeCertificateMapper:
    @staticmethod
    def map_request(
        revocation_reason: CertificateRevocationReason | None = None,
    ) -> spec.RevokeCertificateRequest:
        if revocation_reason is None:
            return spec.RevokeCertificateRequest()
        return spec.RevokeCertificateRequest(
            revocationReason=spec.CertificateRevocationReason(revocation_reason.value),
        )


class QueryCertificatesMapper:
    @staticmethod
    def map_request(
        certificate_serial_number: str | None = None,
        name: str | None = None,
        certificate_type: CertificateType | None = None,
        status: CertificateStatus | None = None,
        expires_after: datetime | None = None,
    ) -> spec.QueryCertificatesRequest:
        return spec.QueryCertificatesRequest(
            certificateSerialNumber=certificate_serial_number,
            name=name,
            type=(
                spec.KsefCertificateType(certificate_type.value)
                if certificate_type
                else None
            ),
            status=(spec.CertificateListItemStatus(status.value) if status else None),
            expiresAfter=expires_after,
        )

    @staticmethod
    def map_response(r: spec.QueryCertificatesResponse) -> QueryCertificatesResponse:
        return QueryCertificatesResponse(
            certificates=[
                QueryCertificatesMapper._map_certificate_info(c) for c in r.certificates
            ],
            has_more=r.hasMore,
        )

    @staticmethod
    def _map_certificate_info(c: spec.CertificateListItem) -> CertificateInfo:
        return CertificateInfo(
            certificate_serial_number=c.certificateSerialNumber,
            name=c.name,
            type=CertificateType(c.type.value),
            common_name=c.commonName,
            status=CertificateStatus(c.status.value),
            subject_identifier=CertificateSubjectIdentifier(
                type=CertificateSubjectIdentifierType(c.subjectIdentifier.type.value),
                value=c.subjectIdentifier.value,
            ),
            valid_from=c.validFrom,
            valid_to=c.validTo,
            last_use_date=c.lastUseDate,
            request_date=c.requestDate,
        )
