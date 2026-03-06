from __future__ import annotations

from enum import Enum
from functools import singledispatch
from typing import assert_never, overload

from pydantic import BaseModel

from ksef2.domain.models.permissions import (
    AuthorizationPermissionsQuery,
    EuEntityPermissionsQuery,
    EuEntityQueryPermissionTypeEnum,
    IdentifierTypeEnum,
    IndirectTargetIdentifierTypeEnum,
    PermissionStateEnum,
    PersonalPermissionsQuery,
    PersonPermissionsQuery,
    PersonPermissionsQueryTypeEnum,
    QueryTypeEnum,
    SubordinateEntityRolesQuery,
    SubunitPermissionsQuery,
)
from ksef2.infra.mappers.permissions.requests import shared
from ksef2.infra.schema.api import spec


def author_identifier_from_literal(
    value: str,
) -> spec.PersonPermissionsAuthorIdentifierType:
    match value:
        case "nip":
            return spec.PersonPermissionsAuthorIdentifierType.Nip
        case "pesel":
            return spec.PersonPermissionsAuthorIdentifierType.Pesel
        case "fingerprint":
            return spec.PersonPermissionsAuthorIdentifierType.Fingerprint
        case "system":
            return spec.PersonPermissionsAuthorIdentifierType.System
        case _:
            raise ValueError(f"Unknown author identifier type: {value!r}")


def author_identifier_type_from_enum(
    request: IdentifierTypeEnum,
) -> spec.PersonPermissionsAuthorIdentifierType:
    match request:
        case IdentifierTypeEnum.NIP:
            return spec.PersonPermissionsAuthorIdentifierType.Nip
        case IdentifierTypeEnum.PESEL:
            return spec.PersonPermissionsAuthorIdentifierType.Pesel
        case IdentifierTypeEnum.FINGERPRINT:
            return spec.PersonPermissionsAuthorIdentifierType.Fingerprint
        case IdentifierTypeEnum.SYSTEM:
            return spec.PersonPermissionsAuthorIdentifierType.System
        case IdentifierTypeEnum.INTERNAL_ID:
            raise ValueError("Identifier type 'internal_id' is not valid for authors")
        case IdentifierTypeEnum.ALL_PARTNERS:
            raise ValueError("Identifier type 'all_partners' is not valid for authors")
        case IdentifierTypeEnum.PEPPOL_ID:
            raise ValueError("Identifier type 'peppol_id' is not valid for authors")
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def authorizing_entity_identifier_from_literal(
    value: str,
) -> spec.EntityAuthorizationsAuthorizingEntityIdentifierType:
    match value:
        case "nip":
            return spec.EntityAuthorizationsAuthorizingEntityIdentifierType.Nip
        case _:
            raise ValueError(f"Unknown authorizing entity identifier type: {value!r}")


def authorization_permission_query_from_literal(
    value: str,
) -> spec.InvoicePermissionType:
    match value:
        case "self_invoicing":
            return spec.InvoicePermissionType.SelfInvoicing
        case "rr_invoicing":
            return spec.InvoicePermissionType.RRInvoicing
        case "tax_representative":
            return spec.InvoicePermissionType.TaxRepresentative
        case "pef_invoicing":
            return spec.InvoicePermissionType.PefInvoicing
        case _:
            raise ValueError(f"Unknown authorization permission type: {value!r}")


def authorization_subject_identifier_from_literal(
    value: str,
) -> spec.EntityAuthorizationPermissionsSubjectIdentifierType:
    match value:
        case "nip":
            return spec.EntityAuthorizationPermissionsSubjectIdentifierType.Nip
        case "peppol_id":
            return spec.EntityAuthorizationPermissionsSubjectIdentifierType.PeppolId
        case _:
            raise ValueError(
                f"Unknown authorization subject identifier type: {value!r}"
            )


def context_identifier_from_literal(
    value: str,
) -> spec.PersonPermissionsContextIdentifierType:
    match value:
        case "nip":
            return spec.PersonPermissionsContextIdentifierType.Nip
        case "internal_id":
            return spec.PersonPermissionsContextIdentifierType.InternalId
        case _:
            raise ValueError(f"Unknown context identifier type: {value!r}")


def eu_query_permission_from_literal(
    value: str,
) -> spec.EuEntityPermissionsQueryPermissionType:
    match value:
        case "vat_ue_manage":
            return spec.EuEntityPermissionsQueryPermissionType.VatUeManage
        case "invoice_write":
            return spec.EuEntityPermissionsQueryPermissionType.InvoiceWrite
        case "invoice_read":
            return spec.EuEntityPermissionsQueryPermissionType.InvoiceRead
        case "introspection":
            return spec.EuEntityPermissionsQueryPermissionType.Introspection
        case _:
            raise ValueError(f"Unknown EU query permission type: {value!r}")


def eu_query_permission_from_enum(
    request: EuEntityQueryPermissionTypeEnum,
) -> spec.EuEntityPermissionsQueryPermissionType:
    match request:
        case EuEntityQueryPermissionTypeEnum.VAT_UE_MANAGE:
            return spec.EuEntityPermissionsQueryPermissionType.VatUeManage
        case EuEntityQueryPermissionTypeEnum.INVOICE_WRITE:
            return spec.EuEntityPermissionsQueryPermissionType.InvoiceWrite
        case EuEntityQueryPermissionTypeEnum.INVOICE_READ:
            return spec.EuEntityPermissionsQueryPermissionType.InvoiceRead
        case EuEntityQueryPermissionTypeEnum.INTROSPECTION:
            return spec.EuEntityPermissionsQueryPermissionType.Introspection
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def indirect_target_identifier_from_enum(
    request: IndirectTargetIdentifierTypeEnum,
) -> spec.IndirectPermissionsTargetIdentifierType:
    match request:
        case IndirectTargetIdentifierTypeEnum.NIP:
            return spec.IndirectPermissionsTargetIdentifierType.Nip
        case IndirectTargetIdentifierTypeEnum.ALL_PARTNERS:
            return spec.IndirectPermissionsTargetIdentifierType.AllPartners
        case IndirectTargetIdentifierTypeEnum.INTERNAL_ID:
            return spec.IndirectPermissionsTargetIdentifierType.InternalId
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def permission_state_from_literal(value: str) -> spec.PermissionState:
    match value:
        case "active":
            return spec.PermissionState.Active
        case "inactive":
            return spec.PermissionState.Inactive
        case _:
            raise ValueError(f"Unknown permission state: {value!r}")


def permission_state_from_enum(request: PermissionStateEnum) -> spec.PermissionState:
    match request:
        case PermissionStateEnum.ACTIVE:
            return spec.PermissionState.Active
        case PermissionStateEnum.INACTIVE:
            return spec.PermissionState.Inactive
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def personal_permission_scope_from_literal(
    value: str,
) -> spec.PersonalPermissionScope:
    match value:
        case "invoice_read":
            return spec.PersonalPermissionScope.InvoiceRead
        case "invoice_write":
            return spec.PersonalPermissionScope.InvoiceWrite
        case "introspection":
            return spec.PersonalPermissionScope.Introspection
        case "credentials_read":
            return spec.PersonalPermissionScope.CredentialsRead
        case "credentials_manage":
            return spec.PersonalPermissionScope.CredentialsManage
        case "enforcement_operations":
            return spec.PersonalPermissionScope.EnforcementOperations
        case "subunit_manage":
            return spec.PersonalPermissionScope.SubunitManage
        case "vat_ue_manage":
            return spec.PersonalPermissionScope.VatUeManage
        case _:
            raise ValueError(f"Unknown personal permission type: {value!r}")


def person_permission_scope_from_literal(
    value: str,
) -> spec.PersonPermissionScope:
    match value:
        case "invoice_read":
            return spec.PersonPermissionScope.InvoiceRead
        case "invoice_write":
            return spec.PersonPermissionScope.InvoiceWrite
        case "introspection":
            return spec.PersonPermissionScope.Introspection
        case "credentials_read":
            return spec.PersonPermissionScope.CredentialsRead
        case "credentials_manage":
            return spec.PersonPermissionScope.CredentialsManage
        case "enforcement_operations":
            return spec.PersonPermissionScope.EnforcementOperations
        case "subunit_manage":
            return spec.PersonPermissionScope.SubunitManage
        case _:
            raise ValueError(f"Unknown person permission type: {value!r}")


def person_query_type_from_literal(value: str) -> spec.PersonPermissionsQueryType:
    match value:
        case "in_context":
            return spec.PersonPermissionsQueryType.PermissionsInCurrentContext
        case "granted_in_context":
            return spec.PersonPermissionsQueryType.PermissionsGrantedInCurrentContext
        case _:
            raise ValueError(f"Unknown person query type: {value!r}")


def person_query_type_from_enum(
    request: PersonPermissionsQueryTypeEnum,
) -> spec.PersonPermissionsQueryType:
    match request:
        case PersonPermissionsQueryTypeEnum.IN_CONTEXT:
            return spec.PersonPermissionsQueryType.PermissionsInCurrentContext
        case PersonPermissionsQueryTypeEnum.GRANTED_IN_CONTEXT:
            return spec.PersonPermissionsQueryType.PermissionsGrantedInCurrentContext
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def query_type_from_literal(value: str) -> spec.QueryType:
    match value:
        case "granted":
            return spec.QueryType.Granted
        case "received":
            return spec.QueryType.Received
        case _:
            raise ValueError(f"Unknown query type: {value!r}")


def query_type_from_enum(request: QueryTypeEnum) -> spec.QueryType:
    match request:
        case QueryTypeEnum.GRANTED:
            return spec.QueryType.Granted
        case QueryTypeEnum.RECEIVED:
            return spec.QueryType.Received
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def subunit_context_identifier_from_literal(
    value: str,
) -> spec.SubunitPermissionsContextIdentifierType:
    match value:
        case "nip":
            return spec.SubunitPermissionsContextIdentifierType.Nip
        case "internal_id":
            return spec.SubunitPermissionsContextIdentifierType.InternalId
        case _:
            raise ValueError(f"Unknown subunit identifier type: {value!r}")


@overload
def to_spec(request: PersonPermissionsQuery) -> spec.PersonPermissionsQueryRequest: ...


@overload
def to_spec(
    request: AuthorizationPermissionsQuery,
) -> spec.EntityAuthorizationPermissionsQueryRequest: ...


@overload
def to_spec(
    request: PersonalPermissionsQuery,
) -> spec.PersonalPermissionsQueryRequest: ...


@overload
def to_spec(
    request: EuEntityPermissionsQuery,
) -> spec.EuEntityPermissionsQueryRequest: ...


@overload
def to_spec(
    request: SubordinateEntityRolesQuery,
) -> spec.SubordinateEntityRolesQueryRequest: ...


@overload
def to_spec(
    request: SubunitPermissionsQuery,
) -> spec.SubunitPermissionsQueryRequest: ...


def to_spec(request: BaseModel | Enum) -> object:
    return _to_spec(request)


@singledispatch
def _to_spec(request: BaseModel | Enum) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(request).__name__}. "
        f"Register one with @_to_spec.register"
    )


@_to_spec.register
def _(request: PersonPermissionsQuery) -> spec.PersonPermissionsQueryRequest:
    author_id = None
    if request.author_type and request.author_value:
        author_id = spec.PersonPermissionsAuthorIdentifier(
            type=author_identifier_from_literal(request.author_type),
            value=request.author_value,
        )

    authorized_id = None
    if request.authorized_type and request.authorized_value:
        authorized_id = spec.PersonPermissionsAuthorizedIdentifier(
            type=shared.cert_subject_identifier_from_literal(request.authorized_type),
            value=request.authorized_value,
        )

    context_id = None
    if request.context_type and request.context_value:
        context_id = spec.PersonPermissionsContextIdentifier(
            type=context_identifier_from_literal(request.context_type),
            value=request.context_value,
        )

    target_id = None
    if request.target_type and request.target_value:
        target_id = spec.PersonPermissionsTargetIdentifier(
            type=shared.indirect_target_identifier_from_literal(request.target_type),
            value=request.target_value,
        )

    return spec.PersonPermissionsQueryRequest(
        authorIdentifier=author_id,
        authorizedIdentifier=authorized_id,
        contextIdentifier=context_id,
        targetIdentifier=target_id,
        permissionTypes=[
            person_permission_scope_from_literal(p) for p in request.permission_types
        ]
        if request.permission_types
        else None,
        permissionState=permission_state_from_literal(request.permission_state)
        if request.permission_state
        else None,
        queryType=person_query_type_from_literal(request.query_type),
    )


@_to_spec.register
def _(
    request: AuthorizationPermissionsQuery,
) -> spec.EntityAuthorizationPermissionsQueryRequest:
    authorizing_id = None
    if request.authorizing_type and request.authorizing_value:
        authorizing_id = spec.EntityAuthorizationsAuthorizingEntityIdentifier(
            type=authorizing_entity_identifier_from_literal(request.authorizing_type),
            value=request.authorizing_value,
        )

    authorized_id = None
    if request.authorized_type and request.authorized_value:
        authorized_id = spec.EntityAuthorizationsAuthorizedEntityIdentifier(
            type=authorization_subject_identifier_from_literal(request.authorized_type),
            value=request.authorized_value,
        )

    return spec.EntityAuthorizationPermissionsQueryRequest(
        authorizingIdentifier=authorizing_id,
        authorizedIdentifier=authorized_id,
        queryType=query_type_from_literal(request.query_type),
        permissionTypes=[
            authorization_permission_query_from_literal(p)
            for p in request.permission_types
        ]
        if request.permission_types
        else None,
    )


@_to_spec.register
def _(request: PersonalPermissionsQuery) -> spec.PersonalPermissionsQueryRequest:
    context_id = None
    if request.context_type and request.context_value:
        context_id = spec.PersonalPermissionsContextIdentifier(
            type=context_identifier_from_literal(request.context_type),
            value=request.context_value,
        )

    target_id = None
    if request.target_type and request.target_value:
        target_id = spec.PersonalPermissionsTargetIdentifier(
            type=shared.indirect_target_identifier_from_literal(request.target_type),
            value=request.target_value,
        )

    return spec.PersonalPermissionsQueryRequest(
        contextIdentifier=context_id,
        targetIdentifier=target_id,
        permissionTypes=[
            personal_permission_scope_from_literal(p) for p in request.permission_types
        ]
        if request.permission_types
        else None,
        permissionState=permission_state_from_literal(request.permission_state)
        if request.permission_state
        else None,
    )


@_to_spec.register
def _(request: EuEntityPermissionsQuery) -> spec.EuEntityPermissionsQueryRequest:
    return spec.EuEntityPermissionsQueryRequest(
        vatUeIdentifier=request.vat_ue_identifier,
        authorizedFingerprintIdentifier=request.authorized_fingerprint_identifier,
        permissionTypes=[
            eu_query_permission_from_literal(p) for p in request.permission_types
        ]
        if request.permission_types
        else None,
    )


@_to_spec.register
def _(request: SubordinateEntityRolesQuery) -> spec.SubordinateEntityRolesQueryRequest:
    sub_id = None
    if request.subordinate_nip:
        sub_id = spec.EntityPermissionsSubordinateEntityIdentifier(
            type=authorizing_entity_identifier_from_literal("nip"),
            value=request.subordinate_nip,
        )
    return spec.SubordinateEntityRolesQueryRequest(
        subordinateEntityIdentifier=sub_id,
    )


@_to_spec.register
def _(request: SubunitPermissionsQuery) -> spec.SubunitPermissionsQueryRequest:
    sub_id = None
    if request.subunit_nip:
        sub_id = spec.SubunitPermissionsSubunitIdentifier(
            type=subunit_context_identifier_from_literal("nip"),
            value=request.subunit_nip,
        )
    return spec.SubunitPermissionsQueryRequest(
        subunitIdentifier=sub_id,
    )
