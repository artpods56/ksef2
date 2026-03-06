from enum import Enum
from functools import singledispatch
from typing import assert_never, overload

from pydantic import BaseModel

from ksef2.domain.models.permissions import (
    AuthorizationGrantDetail,
    AuthorizationPermissionType,
    AuthorizationPermissionsQueryResponse,
    AuthorizationSubjectIdentifierType,
    CertificateSubjectIdentifierType,
    EntityIdentifierType,
    EntityRole,
    EntityRoleType,
    EntityRolesResponse,
)
from ksef2.infra.schema.api import spec


def _cert_subject_identifier_from_value(
    value: str,
) -> CertificateSubjectIdentifierType:
    match value:
        case "Nip":
            return "nip"
        case "Pesel":
            return "pesel"
        case "Fingerprint":
            return "fingerprint"
        case _:
            raise ValueError(f"Unknown certificate subject identifier type: {value!r}")


def _map_entity_role(response: spec.EntityRoleType) -> EntityRoleType:
    match response:
        case spec.EntityRoleType.CourtBailiff:
            return "court_bailiff"
        case spec.EntityRoleType.EnforcementAuthority:
            return "enforcement_authority"
        case spec.EntityRoleType.LocalGovernmentUnit:
            return "local_government_unit"
        case spec.EntityRoleType.LocalGovernmentSubUnit:
            return "local_government_sub_unit"
        case spec.EntityRoleType.VatGroupUnit:
            return "vat_group_unit"
        case spec.EntityRoleType.VatGroupSubUnit:
            return "vat_group_sub_unit"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


@overload
def entity_from_spec(response: spec.EntityRole) -> EntityRole: ...


@overload
def entity_from_spec(
    response: spec.CertificateSubjectIdentifierType,
) -> CertificateSubjectIdentifierType: ...


@overload
def entity_from_spec(
    response: spec.EntityAuthorizationsAuthorIdentifierType,
) -> CertificateSubjectIdentifierType: ...


@overload
def entity_from_spec(
    response: spec.EntityAuthorizationPermissionsSubjectIdentifierType,
) -> AuthorizationSubjectIdentifierType: ...


@overload
def entity_from_spec(
    response: spec.EntityAuthorizationsAuthorizedEntityIdentifierType,
) -> AuthorizationSubjectIdentifierType: ...


@overload
def entity_from_spec(
    response: spec.EntityAuthorizationsAuthorizingEntityIdentifierType,
) -> EntityIdentifierType: ...


@overload
def entity_from_spec(
    response: spec.EntityRolesParentEntityIdentifierType,
) -> EntityIdentifierType: ...


@overload
def entity_from_spec(
    response: spec.EntityAuthorizationGrant,
) -> AuthorizationGrantDetail: ...


@overload
def entity_from_spec(
    response: spec.QueryEntityRolesResponse,
) -> EntityRolesResponse: ...


@overload
def entity_from_spec(
    response: spec.QueryEntityAuthorizationPermissionsResponse,
) -> AuthorizationPermissionsQueryResponse: ...


def entity_from_spec(response: BaseModel | Enum) -> object:
    return _from_spec(response)


@singledispatch
def _from_spec(response: BaseModel | Enum) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(response).__name__}. "
        f"Register one with @_from_spec.register"
    )


def _map_authorization_permission(
    response: spec.InvoicePermissionType,
) -> AuthorizationPermissionType:
    match response:
        case spec.InvoicePermissionType.SelfInvoicing:
            return "self_invoicing"
        case spec.InvoicePermissionType.RRInvoicing:
            return "rr_invoicing"
        case spec.InvoicePermissionType.TaxRepresentative:
            return "tax_representative"
        case spec.InvoicePermissionType.PefInvoicing:
            return "pef_invoicing"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def _authorization_subject_identifier_from_value(
    value: str,
) -> AuthorizationSubjectIdentifierType:
    match value:
        case "Nip":
            return "nip"
        case "PeppolId":
            return "peppol_id"
        case _:
            raise ValueError(f"Unknown authorization subject identifier type: {value!r}")


def _entity_identifier_from_value(
    value: str,
) -> EntityIdentifierType:
    match value:
        case "Nip":
            return "nip"
        case _:
            raise ValueError(f"Unknown entity identifier type: {value!r}")


@_from_spec.register
def _(response: spec.CertificateSubjectIdentifierType) -> CertificateSubjectIdentifierType:
    return _cert_subject_identifier_from_value(response.value)


@_from_spec.register
def _(
    response: spec.EntityAuthorizationsAuthorIdentifierType,
) -> CertificateSubjectIdentifierType:
    return _cert_subject_identifier_from_value(response.value)


@_from_spec.register
def _(
    response: spec.EntityAuthorizationPermissionsSubjectIdentifierType,
) -> AuthorizationSubjectIdentifierType:
    return _authorization_subject_identifier_from_value(response.value)


@_from_spec.register
def _(
    response: spec.EntityAuthorizationsAuthorizedEntityIdentifierType,
) -> AuthorizationSubjectIdentifierType:
    return _authorization_subject_identifier_from_value(response.value)


@_from_spec.register
def _(
    response: spec.EntityAuthorizationsAuthorizingEntityIdentifierType,
) -> EntityIdentifierType:
    return _entity_identifier_from_value(response.value)


@_from_spec.register
def _(response: spec.EntityRolesParentEntityIdentifierType) -> EntityIdentifierType:
    return _entity_identifier_from_value(response.value)


@_from_spec.register
def _(response: spec.EntityAuthorizationGrant) -> AuthorizationGrantDetail:
    entity_full_name = None
    if response.subjectEntityDetails:
        entity_full_name = response.subjectEntityDetails.fullName
    return AuthorizationGrantDetail(
        id=response.id,
        author_type=entity_from_spec(response.authorIdentifier.type)
        if response.authorIdentifier
        else None,
        author_value=response.authorIdentifier.value
        if response.authorIdentifier
        else None,
        authorized_entity_type=entity_from_spec(
            response.authorizedEntityIdentifier.type
        ),
        authorized_entity_value=response.authorizedEntityIdentifier.value,
        authorizing_entity_type=entity_from_spec(
            response.authorizingEntityIdentifier.type
        ),
        authorizing_entity_value=response.authorizingEntityIdentifier.value,
        authorization_scope=_map_authorization_permission(response.authorizationScope),
        description=response.description,
        entity_full_name=entity_full_name,
        start_date=response.startDate,
    )


@_from_spec.register
def _(response: spec.EntityRole) -> EntityRole:
    parent_type = None
    parent_value = None
    if response.parentEntityIdentifier:
        parent_type = entity_from_spec(response.parentEntityIdentifier.type)
        parent_value = response.parentEntityIdentifier.value
    return EntityRole(
        role=_map_entity_role(response.role),
        description=response.description,
        start_date=response.startDate,
        parent_entity_id_type=parent_type,
        parent_entity_id_value=parent_value,
    )


@_from_spec.register
def _(
    response: spec.QueryEntityRolesResponse,
) -> EntityRolesResponse:
    return EntityRolesResponse(
        roles=[entity_from_spec(role) for role in response.roles],
        has_more=response.hasMore,
    )


@_from_spec.register
def _(
    response: spec.QueryEntityAuthorizationPermissionsResponse,
) -> AuthorizationPermissionsQueryResponse:
    return AuthorizationPermissionsQueryResponse(
        authorization_grants=[
            entity_from_spec(g) for g in response.authorizationGrants
        ],
        has_more=response.hasMore,
    )
