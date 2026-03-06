from datetime import datetime
from enum import StrEnum
from typing import Literal

from ksef2.domain.models.base import KSeFBaseModel

type TokenPermission = Literal[
    "invoice_read",
    "invoice_write",
    "credentials_read",
    "credentials_manage",
    "subunit_manage",
    "enforcement_operations",
]

type TokenStatus = Literal["pending", "active", "revoking", "revoked", "failed"]

type TokenAuthorIdentifierType = Literal["nip", "pesel", "fingerprint"]

type TokenContextIdentifierType = Literal[
    "nip", "internal_id", "nip_vat_ue", "peppol_id"
]


class TokenPermissionEnum(StrEnum):
    INVOICE_READ = "invoice_read"
    INVOICE_WRITE = "invoice_write"
    CREDENTIALS_READ = "credentials_read"
    CREDENTIALS_MANAGE = "credentials_manage"
    SUBUNIT_MANAGE = "subunit_manage"
    ENFORCEMENT_OPERATIONS = "enforcement_operations"


class TokenStatusEnum(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    REVOKING = "revoking"
    REVOKED = "revoked"
    FAILED = "failed"


class TokenAuthorIdentifierTypeEnum(StrEnum):
    NIP = "nip"
    PESEL = "pesel"
    FINGERPRINT = "fingerprint"


class TokenContextIdentifierTypeEnum(StrEnum):
    NIP = "nip"
    INTERNAL_ID = "internal_id"
    NIP_VAT_UE = "nip_vat_ue"
    PEPPOL_ID = "peppol_id"


class TokenAuthorIdentifier(KSeFBaseModel):
    type: TokenAuthorIdentifierTypeEnum
    value: str


class TokenContextIdentifier(KSeFBaseModel):
    type: TokenContextIdentifierTypeEnum
    value: str


class GenerateTokenResponse(KSeFBaseModel):
    reference_number: str
    token: str


class TokenStatusResponse(KSeFBaseModel):
    reference_number: str
    status: TokenStatus


class TokenInfo(KSeFBaseModel):
    reference_number: str
    author_identifier: TokenAuthorIdentifier
    context_identifier: TokenContextIdentifier
    description: str
    requested_permissions: list[TokenPermission]
    date_created: datetime
    last_use_date: datetime | None
    status: TokenStatus
    status_details: list[str] | None


class QueryTokensResponse(KSeFBaseModel):
    continuation_token: str | None
    tokens: list[TokenInfo]


class GenerateTokenRequest(KSeFBaseModel):
    permissions: list[TokenPermission]
    description: str


class QueryTokensRequest(KSeFBaseModel):
    status: list[TokenStatus] | None = None
    description: str | None = None
    author_identifier: TokenAuthorIdentifier | None = None
    page_size: int | None = None
