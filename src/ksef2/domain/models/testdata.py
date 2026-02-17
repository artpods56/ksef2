from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import AwareDatetime

from ksef2.domain.models.base import KSeFBaseModel


class SubjectType(StrEnum):
    ENFORCEMENT_AUTHORITY = "EnforcementAuthority"
    VAT_GROUP = "VatGroup"
    JST = "JST"


class IdentifierType(StrEnum):
    NIP = "Nip"
    PESEL = "Pesel"
    FINGERPRINT = "Fingerprint"
    System = "System"


class AuthContextIdentifierType(StrEnum):
    NIP = "Nip"
    INTERNAL_ID = "InternalId"
    NIP_VAT_UE = "NipVatUe"
    PEPPOL_ID = "PeppolId"


class PermissionType(StrEnum):
    INVOICE_READ = "InvoiceRead"
    INVOICE_WRITE = "InvoiceWrite"
    PEF_INVOICE_WRITE = "PefInvoiceWrite"
    INTROSPECTION = "Introspection"
    CREDENTIALS_READ = "CredentialsRead"
    CREDENTIALS_MANAGE = "CredentialsManage"
    ENFORCEMENT_OPERATIONS = "EnforcementOperations"
    SUBUNIT_MANAGE = "SubunitManage"
    VAT_UE_MANAGE = "VatUeManage"


class SubUnit(KSeFBaseModel):
    subject_nip: str
    description: str


class Identifier(KSeFBaseModel):
    type: IdentifierType
    value: str


class AuthContextIdentifier(KSeFBaseModel):
    type: AuthContextIdentifierType
    value: str


class Permission(KSeFBaseModel):
    type: PermissionType
    description: str


class CreateSubjectRequest(KSeFBaseModel):
    subject_nip: str
    subject_type: SubjectType
    description: str
    subunits: list[SubUnit] | None = None
    created_date: AwareDatetime | None = None


class RevokeAttachmentsRequest(KSeFBaseModel):
    nip: str
    expected_end_date: date | None = None
