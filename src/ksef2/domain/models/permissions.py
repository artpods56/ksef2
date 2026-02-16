from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from ksef2.domain.models.testdata import Identifier, PermissionType
from ksef2.domain.models.base import KSeFBaseModel


class EntityPermissionType(StrEnum):
    INVOICE_READ = "InvoiceRead"
    INVOICE_WRITE = "InvoiceWrite"


class AuthorizationPermissionType(StrEnum):
    SELF_INVOICING = "SelfInvoicing"
    RR_INVOICING = "RRInvoicing"
    TAX_REPRESENTATIVE = "TaxRepresentative"
    PEF_INVOICING = "PefInvoicing"


class AuthorizationSubjectIdentifierType(StrEnum):
    NIP = "Nip"
    PEPPOL_ID = "PeppolId"


class IndirectPermissionType(StrEnum):
    INVOICE_READ = "InvoiceRead"
    INVOICE_WRITE = "InvoiceWrite"


class IndirectTargetIdentifierType(StrEnum):
    NIP = "Nip"
    ALL_PARTNERS = "AllPartners"
    INTERNAL_ID = "InternalId"


class SubunitIdentifierType(StrEnum):
    NIP = "Nip"
    INTERNAL_ID = "InternalId"


class EuEntityPermissionType(StrEnum):
    INVOICE_READ = "InvoiceRead"
    INVOICE_WRITE = "InvoiceWrite"


class EuEntityAdminContextIdentifierType(StrEnum):
    NIP_VAT_UE = "NipVatUe"


class EntityRoleType(StrEnum):
    COURT_BAILIFF = "CourtBailiff"
    ENFORCEMENT_AUTHORITY = "EnforcementAuthority"
    LOCAL_GOVERNMENT_UNIT = "LocalGovernmentUnit"
    LOCAL_GOVERNMENT_SUB_UNIT = "LocalGovernmentSubUnit"
    VAT_GROUP_UNIT = "VatGroupUnit"
    VAT_GROUP_SUB_UNIT = "VatGroupSubUnit"


class PermissionState(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class EntityPermission(KSeFBaseModel):
    type: EntityPermissionType
    can_delegate: bool = False


class GrantPermissionsResponse(KSeFBaseModel):
    reference_number: str


class OperationStatusCode(StrEnum):
    ACCEPTED = "100"
    SUCCESS = "200"
    FAILED = "400"
    IDENTIFIERS_MISMATCH = "410"
    CREDENTIALS_NO_PERMISSION = "420"
    CONTEXT_MISMATCH = "430"
    FORBIDDEN_RELATION = "440"
    FORBIDDEN_IDENTIFIER = "450"
    UNKNOWN_ERROR = "500"
    CANCELLED = "550"


class OperationStatus(KSeFBaseModel):
    code: OperationStatusCode
    description: str


class PermissionOperationStatusResponse(KSeFBaseModel):
    status: OperationStatus


class AttachmentPermissionStatus(KSeFBaseModel):
    is_attachment_allowed: bool
    revoked_date: datetime | None = None


class EntityRole(KSeFBaseModel):
    role: EntityRoleType
    description: str
    start_date: datetime
    parent_entity_identifier_type: str | None = None
    parent_entity_identifier_value: str | None = None


class EntityRolesResponse(KSeFBaseModel):
    roles: list[EntityRole]
    has_more: bool


class PermissionsQueryType(StrEnum):
    PERMISSIONS_IN_CURRENT_CONTEXT = "PermissionsInCurrentContext"
    PERMISSIONS_GRANTED_IN_CURRENT_CONTEXT = "PermissionsGrantedInCurrentContext"


class PersonPermissionsBase(KSeFBaseModel):
    """Shared identifier/filter fields for person permissions."""

    author_identifier: Identifier | None = None
    authorized_identifier: Identifier | None = None
    context_identifier: Identifier | None = None
    target_identifier: Identifier | None = None
    permission_state: PermissionState | None = None


class PersonPermissionsQueryRequest(PersonPermissionsBase):
    """Query request — adds filter and query type fields."""

    permission_types: list[PermissionType] | None = None
    query_type: PermissionsQueryType


class SubjectPersonDetails(KSeFBaseModel):
    first_name: str
    last_name: str


class SubjectEntityDetails(KSeFBaseModel):
    full_name: str


class PersonPermissionDetail(PersonPermissionsBase):
    """Single permission result — adds result-specific fields."""

    id: Annotated[str, Field(max_length=36, min_length=36)]
    permission_type: PermissionType
    description: str
    start_date: datetime
    can_delegate: bool
    subject_person_details: SubjectPersonDetails | None = None
    subject_entity_details: SubjectEntityDetails | None = None


class PersonPermissionsQueryResponse(KSeFBaseModel):
    """Paginated query response."""

    permissions: list[PersonPermissionDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# Query type enum (shared by authorizations, eu_entities, personal, subunits)
# ---------------------------------------------------------------------------


class QueryType(StrEnum):
    GRANTED = "Granted"
    RECEIVED = "Received"


class SubordinateEntityRoleType(StrEnum):
    LOCAL_GOVERNMENT_SUB_UNIT = "LocalGovernmentSubUnit"
    VAT_GROUP_SUB_UNIT = "VatGroupSubUnit"


class EuEntityQueryPermissionType(StrEnum):
    VAT_UE_MANAGE = "VatUeManage"
    INVOICE_WRITE = "InvoiceWrite"
    INVOICE_READ = "InvoiceRead"
    INTROSPECTION = "Introspection"


# ---------------------------------------------------------------------------
# 1. query_authorizations
# ---------------------------------------------------------------------------


class AuthorizationPermissionsQueryRequest(KSeFBaseModel):
    authorizing_identifier: Identifier | None = None
    authorized_identifier: Identifier | None = None
    query_type: QueryType
    permission_types: list[AuthorizationPermissionType] | None = None


class AuthorizationGrantDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    author_identifier: Identifier | None = None
    authorized_entity_identifier: Identifier
    authorizing_entity_identifier: Identifier
    authorization_scope: AuthorizationPermissionType
    description: str
    subject_entity_details: SubjectEntityDetails | None = None
    start_date: datetime


class AuthorizationPermissionsQueryResponse(KSeFBaseModel):
    authorization_grants: list[AuthorizationGrantDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# 2. query_personal
# ---------------------------------------------------------------------------


class PersonalPermissionsQueryRequest(KSeFBaseModel):
    context_identifier: Identifier | None = None
    target_identifier: Identifier | None = None
    permission_types: list[PermissionType] | None = None
    permission_state: PermissionState | None = None


class PersonalPermissionDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    context_identifier: Identifier | None = None
    authorized_identifier: Identifier | None = None
    target_identifier: Identifier | None = None
    permission_type: PermissionType
    description: str
    subject_person_details: SubjectPersonDetails | None = None
    subject_entity_details: SubjectEntityDetails | None = None
    permission_state: PermissionState
    start_date: datetime
    can_delegate: bool


class PersonalPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[PersonalPermissionDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# 3. query_eu_entities
# ---------------------------------------------------------------------------


class EuEntityDetails(KSeFBaseModel):
    full_name: str
    address: str | None = None


class EuEntityPermissionsQueryRequest(KSeFBaseModel):
    vat_ue_identifier: str | None = None
    authorized_fingerprint_identifier: str | None = None
    permission_types: list[EuEntityQueryPermissionType] | None = None


class EuEntityPermissionDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    author_identifier: Identifier
    vat_ue_identifier: str
    eu_entity_name: str
    authorized_fingerprint_identifier: str
    permission_type: EuEntityQueryPermissionType
    description: str
    subject_person_details: SubjectPersonDetails | None = None
    subject_entity_details: SubjectEntityDetails | None = None
    eu_entity_details: EuEntityDetails | None = None
    start_date: datetime


class EuEntityPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[EuEntityPermissionDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# 4. query_subordinate_entities
# ---------------------------------------------------------------------------


class SubordinateEntityRolesQueryRequest(KSeFBaseModel):
    subordinate_entity_identifier: Identifier | None = None


class SubordinateEntityRoleDetail(KSeFBaseModel):
    subordinate_entity_identifier: Identifier
    role: SubordinateEntityRoleType
    description: str
    start_date: datetime


class SubordinateEntityRolesQueryResponse(KSeFBaseModel):
    roles: list[SubordinateEntityRoleDetail]
    has_more: bool


# ---------------------------------------------------------------------------
# 5. query_subunits
# ---------------------------------------------------------------------------


class SubunitPermissionsQueryRequest(KSeFBaseModel):
    subunit_identifier: Identifier | None = None


class SubunitPermissionDetail(KSeFBaseModel):
    id: Annotated[str, Field(max_length=36, min_length=36)]
    authorized_identifier: Identifier
    subunit_identifier: Identifier
    author_identifier: Identifier
    permission_type: PermissionType
    description: str
    subject_person_details: SubjectPersonDetails | None = None
    subunit_name: str | None = None
    start_date: datetime


class SubunitPermissionsQueryResponse(KSeFBaseModel):
    permissions: list[SubunitPermissionDetail]
    has_more: bool
