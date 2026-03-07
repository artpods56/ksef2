"""Domain models for KSeF certificate management."""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from ksef2.domain.models.base import KSeFBaseModel

type IdentifierType = Literal["nip", "pesel", "fingerprint"]
type RevocationReason = Literal["unspecified", "superseded", "key_compromise"]
type CertificateTypeValue = Literal["authentication", "offline"]
type CertificateStatusValue = Literal["active", "blocked", "revoked", "expired"]


class CertificateTypeEnum(StrEnum):
    AUTHENTICATION = "authentication"
    OFFLINE = "offline"


class CertificateStatusEnum(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    REVOKED = "revoked"
    EXPIRED = "expired"


class IdentifierTypeEnum(StrEnum):
    NIP = "nip"
    PESEL = "pesel"
    FINGERPRINT = "fingerprint"


class RevocationReasonEnum(StrEnum):
    UNSPECIFIED = "unspecified"
    SUPERSEDED = "superseded"
    KEY_COMPROMISE = "key_compromise"


class SubjectIdentifier(KSeFBaseModel):
    """Identifier of the subject the certificate was issued for."""

    type: IdentifierType
    value: str


class Certificate(KSeFBaseModel):
    base64_encoded_certificate: str
    name: str
    serial_number: str
    certificate_type: CertificateTypeValue


class RetrievedCertificatesList(KSeFBaseModel):
    """Certificates returned by the retrieval endpoint."""

    certificates: list[Certificate]


class CertificateQuota(KSeFBaseModel):
    limit: int
    remaining: int


class CertificateInfo(KSeFBaseModel):
    """Metadata for one certificate visible in certificate queries."""

    # certificate
    serial_number: str
    name: str
    common_name: str
    type: CertificateTypeValue
    status: CertificateStatusValue

    # issued for
    subject_identifier: SubjectIdentifier

    # date
    valid_from: datetime
    valid_to: datetime
    last_use_date: datetime | None = None
    request_date: datetime


class CertificatesInfoList(KSeFBaseModel):
    """One page of certificate query results."""

    certificates: list[CertificateInfo]
    has_more: bool


class CertificateEnrollmentData(KSeFBaseModel):
    """Subject data that should be embedded in a certificate enrollment CSR."""

    common_name: str
    name: str | None = None
    surname: str | None = None
    iso_country_code: str
    serial_number: str | None = None
    unique_identifier: str | None = None
    organization_name: str | None = None
    organization_identifier: str | None = None

    @property
    def country_name(self) -> str:
        return self.iso_country_code


class CertificateEnrollmentResponse(KSeFBaseModel):
    reference_number: str
    timestamp: datetime


class CertificateEnrollmentStatusResponse(KSeFBaseModel):
    """Current status of a certificate enrollment request."""

    request_date: datetime
    status_code: int
    status_description: str
    status_details: list[str] | None = None
    certificate_serial_number: str | None = None


class CertificateLimitsResponse(KSeFBaseModel):
    """Effective enrollment and certificate quotas for the current subject."""

    can_request: bool
    enrollment_limit: int
    enrollment_remaining: int
    certificate_limit: int
    certificate_remaining: int

    @property
    def enrollment(self) -> CertificateQuota:
        return CertificateQuota(
            limit=self.enrollment_limit,
            remaining=self.enrollment_remaining,
        )

    @property
    def certificate(self) -> CertificateQuota:
        return CertificateQuota(
            limit=self.certificate_limit,
            remaining=self.certificate_remaining,
        )


# --- Request models ---


class EnrollCertificateRequest(KSeFBaseModel):
    """Payload used to request a new certificate enrollment."""

    certificate_name: str
    certificate_type: CertificateTypeValue
    csr: str
    valid_from: datetime | str | None = None


class RetrieveCertificatesRequest(KSeFBaseModel):
    """Payload used to download issued certificates by serial number."""

    certificate_serial_numbers: list[str]


class RevokeCertificateRequest(KSeFBaseModel):
    """Payload used to revoke a certificate when a reason is provided."""

    revocation_reason: RevocationReason | None = None


class QueryCertificatesRequest(KSeFBaseModel):
    """Optional filters for certificate search."""

    certificate_serial_number: str | None = None
    name: str | None = None
    certificate_type: CertificateTypeValue | None = None
    status: CertificateStatusValue | None = None
    expires_after: datetime | str | None = None


QueryCertificatesResponse = CertificatesInfoList
