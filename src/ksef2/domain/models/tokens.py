from __future__ import annotations

from datetime import datetime
from enum import Enum

from ksef2.domain.models.base import KSeFBaseModel


class TokenPermission(Enum):
    INVOICE_READ = "InvoiceRead"
    INVOICE_WRITE = "InvoiceWrite"
    CREDENTIALS_READ = "CredentialsRead"
    CREDENTIALS_MANAGE = "CredentialsManage"
    SUBUNIT_MANAGE = "SubunitManage"
    ENFORCEMENT_OPERATIONS = "EnforcementOperations"


class TokenStatus(Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    REVOKING = "Revoking"
    REVOKED = "Revoked"
    FAILED = "Failed"


class TokenAuthorIdentifierType(Enum):
    NIP = "Nip"
    PESEL = "Pesel"
    FINGERPRINT = "Fingerprint"


class TokenContextIdentifierType(Enum):
    NIP = "Nip"
    INTERNAL_ID = "InternalId"
    NIP_VAT_UE = "NipVatUe"
    PEPPOL_ID = "PeppolId"


class TokenAuthorIdentifier(KSeFBaseModel):
    type: TokenAuthorIdentifierType
    value: str


class TokenContextIdentifier(KSeFBaseModel):
    type: TokenContextIdentifierType
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
