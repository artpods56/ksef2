from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field, BaseModel

from ksef2.domain.models.base import KSeFBaseModel

# ---------------------------------------------------------------------------
# Type aliases (replace StrEnums)
# ---------------------------------------------------------------------------

type IdentifierType = Literal[
    "nip", "pesel", "fingerprint", "system", "internal_id", "all_partners", "peppol_id"
]

type CertificateSubjectIdentifierType = Literal["nip", "pesel", "fingerprint"]

type PersonAuthorIdentifierType = Literal["nip", "pesel", "fingerprint", "system"]

type PersonContextIdentifierType = Literal["nip", "internal_id"]

type EntityIdentifierType = Literal["nip"]

type PersonPermissionScope = Literal[
    "invoice_read",
    "invoice_write",
    "pef_invoice_write",
    "introspection",
    "credentials_read",
    "credentials_manage",
    "enforcement_operations",
    "subunit_manage",
    "vat_ue_manage",
]

type EntityPermissionType = Literal["invoice_read", "invoice_write"]

type AuthorizationPermissionType = Literal[
    "self_invoicing", "rr_invoicing", "tax_representative", "pef_invoicing"
]

type AuthorizationSubjectIdentifierType = Literal["nip", "peppol_id"]

type IndirectPermissionType = Literal["invoice_read", "invoice_write"]

type IndirectTargetIdentifierType = Literal["nip", "all_partners", "internal_id"]

type SubunitIdentifierType = Literal["nip", "internal_id"]

type EuEntityPermissionType = Literal["invoice_read", "invoice_write"]

type EuEntityAdminContextIdentifierType = Literal["nip_vat_ue"]

type EntityRoleType = Literal[
    "court_bailiff",
    "enforcement_authority",
    "local_government_unit",
    "local_government_sub_unit",
    "vat_group_unit",
    "vat_group_sub_unit",
]

type PermissionState = Literal["active", "inactive"]

type OperationStatusCode = Literal[100, 200, 400, 410, 420, 430, 440, 450, 500, 550]

type QueryType = Literal["granted", "received"]

type PersonPermissionsQueryType = Literal["in_context", "granted_in_context"]

type SubordinateEntityRoleType = Literal[
    "local_government_sub_unit", "vat_group_sub_unit"
]

type EuEntityQueryPermissionType = Literal[
    "vat_ue_manage", "invoice_write", "invoice_read", "introspection"
]


class IdentifierTypeEnum(StrEnum):
    NIP = "nip"
    PESEL = "pesel"
    FINGERPRINT = "fingerprint"
    SYSTEM = "system"
    INTERNAL_ID = "internal_id"
    ALL_PARTNERS = "all_partners"
    PEPPOL_ID = "peppol_id"


class PersonPermissionTypeEnum(StrEnum):
    INVOICE_READ = "invoice_read"
    INVOICE_WRITE = "invoice_write"
    PEF_INVOICE_WRITE = "pef_invoice_write"
    INTROSPECTION = "introspection"
    CREDENTIALS_READ = "credentials_read"
    CREDENTIALS_MANAGE = "credentials_manage"
    ENFORCEMENT_OPERATIONS = "enforcement_operations"
    SUBUNIT_MANAGE = "subunit_manage"
    VAT_UE_MANAGE = "vat_ue_manage"


class EntityPermissionTypeEnum(StrEnum):
    INVOICE_READ = "invoice_read"
    INVOICE_WRITE = "invoice_write"


class AuthorizationPermissionTypeEnum(StrEnum):
    SELF_INVOICING = "self_invoicing"
    RR_INVOICING = "rr_invoicing"
    TAX_REPRESENTATIVE = "tax_representative"
    PEF_INVOICING = "pef_invoicing"


class AuthorizationSubjectIdentifierTypeEnum(StrEnum):
    NIP = "nip"
    PEPPOL_ID = "peppol_id"


class IndirectPermissionTypeEnum(StrEnum):
    INVOICE_READ = "invoice_read"
    INVOICE_WRITE = "invoice_write"


class IndirectTargetIdentifierTypeEnum(StrEnum):
    NIP = "nip"
    ALL_PARTNERS = "all_partners"
    INTERNAL_ID = "internal_id"


class SubunitIdentifierTypeEnum(StrEnum):
    NIP = "nip"
    INTERNAL_ID = "internal_id"


class EuEntityPermissionTypeEnum(StrEnum):
    INVOICE_READ = "invoice_read"
    INVOICE_WRITE = "invoice_write"


class EuEntityAdminContextIdentifierTypeEnum(StrEnum):
    NIP_VAT_UE = "nip_vat_ue"


class EntityRoleTypeEnum(StrEnum):
    COURT_BAILIFF = "court_bailiff"
    ENFORCEMENT_AUTHORITY = "enforcement_authority"
    LOCAL_GOVERNMENT_UNIT = "local_government_unit"
    LOCAL_GOVERNMENT_SUB_UNIT = "local_government_sub_unit"
    VAT_GROUP_UNIT = "vat_group_unit"
    VAT_GROUP_SUB_UNIT = "vat_group_sub_unit"


class PermissionStateEnum(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class QueryTypeEnum(StrEnum):
    GRANTED = "granted"
    RECEIVED = "received"


class PersonPermissionsQueryTypeEnum(StrEnum):
    IN_CONTEXT = "in_context"
    GRANTED_IN_CONTEXT = "granted_in_context"


class SubordinateEntityRoleTypeEnum(StrEnum):
    LOCAL_GOVERNMENT_SUB_UNIT = "local_government_sub_unit"
    VAT_GROUP_SUB_UNIT = "vat_group_sub_unit"


class EuEntityQueryPermissionTypeEnum(StrEnum):
    VAT_UE_MANAGE = "vat_ue_manage"
    INVOICE_WRITE = "invoice_write"
    INVOICE_READ = "invoice_read"
    INTROSPECTION = "introspection"


class ScopeLiteralEnum(StrEnum):
    INVOICE_READ = "invoice_read"
    INVOICE_WRITE = "invoice_write"


# ---------------------------------------------------------------------------
# Grant models
# ---------------------------------------------------------------------------


class EntityPermission(KSeFBaseModel):
    type: EntityPermissionType
    can_delegate: bool = False


class GrantPermissionsResponse(KSeFBaseModel):
    reference_number: str


class GrantPersonPermissionsRequest(KSeFBaseModel):
    subject_type: CertificateSubjectIdentifierType
    subject_value: str
    permissions: list[PersonPermissionScope]
    description: str
    first_name: str
    last_name: str


class GrantEntityPermissionsRequest(KSeFBaseModel):
    subject_value: str
    permissions: list[EntityPermission]
    description: str
    entity_name: str


class GrantAuthorizationPermissionsRequest(KSeFBaseModel):
    subject_type: AuthorizationSubjectIdentifierType
    subject_value: str
    permission: AuthorizationPermissionType
    description: str
    entity_name: str


class GrantIndirectPermissionsRequest(KSeFBaseModel):
    subject_type: CertificateSubjectIdentifierType
    subject_value: str
    permissions: list[IndirectPermissionType]
    description: str
    first_name: str
    last_name: str
    target_type: IndirectTargetIdentifierType | None = None
    target_value: str | None = None


class GrantSubunitPermissionsRequest(KSeFBaseModel):
    subject_type: CertificateSubjectIdentifierType
    subject_value: str
    context_type: SubunitIdentifierType
    context_value: str
    description: str
    first_name: str
    last_name: str
    subunit_name: str | None = None


class GrantEuEntityPermissionsRequest(KSeFBaseModel):
    subject_value: str
    permissions: list[EuEntityPermissionType]
    description: str


class GrantEuEntityAdministrationRequest(KSeFBaseModel):
    subject_value: str
    context_type: EuEntityAdminContextIdentifierType
    context_value: str
    description: str
    eu_entity_name: str


# ---------------------------------------------------------------------------
# Status models
# ---------------------------------------------------------------------------


class OperationStatus(KSeFBaseModel):
    code: OperationStatusCode
    description: str


class PermissionOperationStatusResponse(KSeFBaseModel):
    status: OperationStatus


class AttachmentPermissionStatus(KSeFBaseModel):
    is_attachment_allowed: bool
    revoked_date: datetime | None = None


# ---------------------------------------------------------------------------
# Entity roles
# ---------------------------------------------------------------------------


class EntityRole(KSeFBaseModel):
    role: EntityRoleType
    description: str
    start_date: datetime
    parent_entity_id_type: EntityIdentifierType | None = None
    parent_entity_id_value: str | None = None


class EntityRolesResponse(KSeFBaseModel):
    roles: list[EntityRole]
    has_more: bool


# ---------------------------------------------------------------------------
# Query: persons
# ---------------------------------------------------------------------------


class PersonPermissionsQuery(KSeFBaseModel):
    query_type: PersonPermissionsQueryType
    permission_types: list[PersonPermissionScope] | None = None
    permission_state: PermissionState | None = None
    author_type: PersonAuthorIdentifierType | None = None
    author_value: str | None = None
    authorized_type: CertificateSubjectIdentifierType | None = None
    authorized_value: str | None = None
    context_type: PersonContextIdentifierType | None = None
    context_value: str | None = None
    target_type: IndirectTargetIdentifierType | None = None
    target_value: str | None = None


class PersonPermissionDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    author_type: PersonAuthorIdentifierType | None = None
    author_value: str | None = None
    authorized_type: CertificateSubjectIdentifierType | None = None
    authorized_value: str | None = None
    context_type: PersonContextIdentifierType | None = None
    context_value: str | None = None
    target_type: IndirectTargetIdentifierType | None = None
    target_value: str | None = None
    permission_state: PermissionState
    permission_type: PersonPermissionScope
    description: str
    start_date: datetime
    can_delegate: bool
    person_first_name: str | None = None
    person_last_name: str | None = None
    entity_first_name: str | None = None
    entity_last_name: str | None = None


class PersonPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[PersonPermissionDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# Query: authorizations
# ---------------------------------------------------------------------------


class AuthorizationPermissionsQuery(KSeFBaseModel):
    query_type: QueryType
    permission_types: list[AuthorizationPermissionType] | None = None
    authorizing_type: EntityIdentifierType | None = None
    authorizing_value: str | None = None
    authorized_type: AuthorizationSubjectIdentifierType | None = None
    authorized_value: str | None = None


class AuthorizationGrantDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    author_type: CertificateSubjectIdentifierType | None = None
    author_value: str | None = None
    authorized_entity_type: AuthorizationSubjectIdentifierType
    authorized_entity_value: str
    authorizing_entity_type: EntityIdentifierType
    authorizing_entity_value: str
    authorization_scope: AuthorizationPermissionType
    description: str
    entity_full_name: str | None = None
    start_date: datetime


class AuthorizationPermissionsQueryResponse(KSeFBaseModel):
    authorization_grants: list[AuthorizationGrantDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# Query: personal
# ---------------------------------------------------------------------------


class PersonalPermissionsQuery(KSeFBaseModel):
    permission_types: list[PersonPermissionScope] | None = None
    permission_state: PermissionState | None = None
    context_type: PersonContextIdentifierType | None = None
    context_value: str | None = None
    target_type: IndirectTargetIdentifierType | None = None
    target_value: str | None = None


class PersonalPermissionDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    context_type: PersonContextIdentifierType | None = None
    context_value: str | None = None
    authorized_type: CertificateSubjectIdentifierType | None = None
    authorized_value: str | None = None
    target_type: IndirectTargetIdentifierType | None = None
    target_value: str | None = None
    permission_type: PersonPermissionScope
    description: str
    subject_first_name: str | None = None
    subject_last_name: str | None = None
    entity_first_name: str | None = None
    entity_address: str | None = None
    permission_state: PermissionState
    start_date: datetime
    can_delegate: bool


class PersonalPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[PersonalPermissionDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# Query: EU entities
# ---------------------------------------------------------------------------


class EuEntityPermissionsQuery(KSeFBaseModel):
    vat_ue_identifier: str | None = None
    authorized_fingerprint_identifier: str | None = None
    permission_types: list[EuEntityQueryPermissionType] | None = None


class EuEntityPermission(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    author_type: CertificateSubjectIdentifierType
    author_value: str
    vat_ue_identifier: str
    eu_entity_name: str
    authorized_fingerprint_identifier: str
    permission_type: EuEntityQueryPermissionType
    description: str
    subject_first_name: str | None = None
    subject_last_name: str | None = None
    entity_full_name: str | None = None
    entity_address: str | None = None
    start_date: datetime


class EuEntityPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[EuEntityPermission]
    has_more: bool


# ---------------------------------------------------------------------------
# Query: subordinate entities
# ---------------------------------------------------------------------------


class SubordinateEntityRolesQuery(KSeFBaseModel):
    subordinate_nip: str | None = None


class SubordinateEntityRoleDetail(KSeFBaseModel):
    subordinate_entity_type: EntityIdentifierType
    subordinate_entity_value: str
    role: SubordinateEntityRoleType
    description: str
    start_date: datetime


class SubordinateEntityRolesQueryResponse(KSeFBaseModel):
    roles: list[SubordinateEntityRoleDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# Query: subunits
# ---------------------------------------------------------------------------


class SubunitPermissionsQuery(KSeFBaseModel):
    subunit_nip: str | None = None


class SubunitPermission(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    authorized_type: CertificateSubjectIdentifierType
    authorized_value: str
    subunit_type: SubunitIdentifierType
    subunit_value: str
    author_type: CertificateSubjectIdentifierType
    author_value: str
    permission_type: PersonPermissionScope
    description: str
    subject_first_name: str | None = None
    subject_last_name: str | None = None
    entity_first_name: str | None = None
    entity_last_name: str | None = None
    subunit_name: str | None = None
    start_date: datetime


class SubunitPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[SubunitPermission]
    has_more: bool


class ItemsListResponse[ItemT: BaseModel](KSeFBaseModel):
    items: list[ItemT]
    has_more: bool
