from __future__ import annotations

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


class GenerateTokenResponse(KSeFBaseModel):
    reference_number: str
    token: str


class TokenStatusResponse(KSeFBaseModel):
    reference_number: str
    status: TokenStatus
