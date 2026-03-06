from datetime import datetime
from enum import StrEnum
from typing import Literal

from ksef2.domain.models.base import KSeFBaseModel

type IdentifierType = Literal["nip", "pesel", "fingerprint"]
type RevocationReason = Literal["unspecified", "superseded", "key_compromise"]
type CertificateType = Literal["authentication", "offline"]
type CertificateStatus = Literal["active", "blocked", "revoked", "expired"]


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
    type: IdentifierTypeEnum
    value: str


class Certificate(KSeFBaseModel):
    base64_encoded_certificate: str
    name: str
    serial_number: str
    certificate_type: CertificateType


class RetrievedCertificatesList(KSeFBaseModel):
    certificates: list[Certificate]


class CertificateInfo(KSeFBaseModel):
    # certificate
    serial_number: str
    name: str
    common_name: str
    type: CertificateType
    status: CertificateStatus

    # issued for
    subject_identifier: SubjectIdentifier

    # date
    valid_from: datetime
    valid_to: datetime
    last_use_date: datetime | None = None
    request_date: datetime


class CertificatesInfoList(KSeFBaseModel):
    certificates: list[CertificateInfo]
    has_more: bool


class CertificateEnrollmentData(KSeFBaseModel):
    common_name: str
    name: str | None = None
    surname: str | None = None
    iso_country_code: str
    serial_number: str | None = None
    unique_identifier: str | None = None
    organization_name: str | None = None
    organization_identifier: str | None = None


class CertificateEnrollmentResponse(KSeFBaseModel):
    reference_number: str
    timestamp: datetime


class CertificateEnrollmentStatusResponse(KSeFBaseModel):
    request_date: datetime
    status_code: int
    status_description: str
    status_details: list[str] | None = None
    certificate_serial_number: str | None = None


class CertificateLimitsResponse(KSeFBaseModel):
    can_request: bool
    enrollment_limit: int
    enrollment_remaining: int
    certificate_limit: int
    certificate_remaining: int


# --- Request models ---


class EnrollCertificateRequest(KSeFBaseModel):
    certificate_name: str
    certificate_type: CertificateType
    csr: str
    valid_from: datetime | str | None = None


class RetrieveCertificatesRequest(KSeFBaseModel):
    certificate_serial_numbers: list[str]


class RevokeCertificateRequest(KSeFBaseModel):
    revocation_reason: RevocationReason | None = None


class QueryCertificatesRequest(KSeFBaseModel):
    certificate_serial_number: str | None = None
    name: str | None = None
    certificate_type: CertificateType | None = None
    status: CertificateStatus | None = None
    expires_after: datetime | str | None = None
