from __future__ import annotations

from datetime import datetime
from enum import Enum

from ksef2.domain.models.base import KSeFBaseModel


class CertificateType(Enum):
    """Type of KSeF certificate."""

    AUTHENTICATION = "Authentication"
    OFFLINE = "Offline"


class CertificateStatus(Enum):
    """Status of a certificate."""

    ACTIVE = "Active"
    BLOCKED = "Blocked"
    REVOKED = "Revoked"
    EXPIRED = "Expired"


class CertificateRevocationReason(Enum):
    """Reason for certificate revocation."""

    UNSPECIFIED = "Unspecified"
    SUPERSEDED = "Superseded"
    KEY_COMPROMISE = "KeyCompromise"


class CertificateSubjectIdentifierType(Enum):
    """Type of certificate subject identifier."""

    NIP = "Nip"
    PESEL = "Pesel"
    FINGERPRINT = "Fingerprint"


class CertificateSubjectIdentifier(KSeFBaseModel):
    """Certificate subject identifier."""

    type: CertificateSubjectIdentifierType
    value: str


class CertificateLimit(KSeFBaseModel):
    """Certificate limit info."""

    limit: int
    remaining: int


class CertificateLimitsResponse(KSeFBaseModel):
    """Response with certificate limits for the authenticated subject."""

    can_request: bool
    enrollment: CertificateLimit
    certificate: CertificateLimit


class CertificateEnrollmentData(KSeFBaseModel):
    """Data required for preparing a PKCS#10 certificate signing request."""

    common_name: str
    country_name: str
    given_name: str | None = None
    surname: str | None = None
    serial_number: str | None = None
    unique_identifier: str | None = None
    organization_name: str | None = None
    organization_identifier: str | None = None


class StatusInfo(KSeFBaseModel):
    """Generic status info with code and description."""

    code: int
    description: str
    details: list[str] | None = None


class EnrollCertificateResponse(KSeFBaseModel):
    """Response from certificate enrollment submission."""

    reference_number: str
    timestamp: datetime


class CertificateEnrollmentStatus(KSeFBaseModel):
    """Status of a certificate enrollment request."""

    request_date: datetime
    status: StatusInfo
    certificate_serial_number: str | None = None


class CertificateInfo(KSeFBaseModel):
    """Certificate metadata returned from query."""

    certificate_serial_number: str
    name: str
    type: CertificateType
    common_name: str
    status: CertificateStatus
    subject_identifier: CertificateSubjectIdentifier
    valid_from: datetime
    valid_to: datetime
    last_use_date: datetime | None = None
    request_date: datetime


class QueryCertificatesResponse(KSeFBaseModel):
    """Response from certificates query."""

    certificates: list[CertificateInfo]
    has_more: bool


class RetrievedCertificate(KSeFBaseModel):
    """Retrieved certificate with DER data."""

    certificate: str  # Base64 encoded DER
    certificate_name: str
    certificate_serial_number: str
    certificate_type: CertificateType


class RetrieveCertificatesResponse(KSeFBaseModel):
    """Response from retrieve certificates request."""

    certificates: list[RetrievedCertificate]
