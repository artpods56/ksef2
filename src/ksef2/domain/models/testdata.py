from __future__ import annotations

from enum import Enum

from ksef2.domain.models._deprecated._base import KSeFBaseModel


class SubjectType(Enum):
    ENFORCEMENT_AUTHORITY = "EnforcementAuthority"
    VAT_GROUP = "VatGroup"
    JST = "JST"


class IdentifierType(Enum):
    NIP = "Nip"
    PESEL = "Pesel"
    FINGERPRINT = "Fingerprint"


class PermissionType(Enum):
    INVOICE_READ = "InvoiceRead"
    INVOICE_WRITE = "InvoiceWrite"
    INTROSPECTION = "Introspection"
    CREDENTIALS_READ = "CredentialsRead"
    CREDENTIALS_MANAGE = "CredentialsManage"
    ENFORCEMENT_OPERATIONS = "EnforcementOperations"
    SUBUNIT_MANAGE = "SubunitManage"


class Subunit(KSeFBaseModel):
    nip: str
    description: str


class Identifier(KSeFBaseModel):
    type: IdentifierType
    value: str


class Permission(KSeFBaseModel):
    type: PermissionType
    description: str
