from enum import Enum
from functools import singledispatch
from typing import assert_never, overload

from pydantic import BaseModel

from ksef2.domain.models.permissions import (
    IdentifierType,
    SubordinateEntityRoleDetail,
    SubordinateEntityRolesQueryResponse,
    SubordinateEntityRoleType,
)
from ksef2.infra.schema.api import spec


def _entity_identifier_from_value(value: str) -> IdentifierType:
    match value:
        case "Nip":
            return "nip"
        case _:
            raise ValueError(f"Unknown entity identifier type: {value!r}")


def _map_subordinate_role(
    response: spec.SubordinateEntityRoleType,
) -> SubordinateEntityRoleType:
    match response:
        case spec.SubordinateEntityRoleType.LocalGovernmentSubUnit:
            return "local_government_sub_unit"
        case spec.SubordinateEntityRoleType.VatGroupSubUnit:
            return "vat_group_sub_unit"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


@overload
def subordinate_roles_from_spec(
    response: spec.SubordinateEntityRole,
) -> SubordinateEntityRoleDetail: ...


@overload
def subordinate_roles_from_spec(
    response: spec.EntityAuthorizationsAuthorizingEntityIdentifierType,
) -> IdentifierType: ...


@overload
def subordinate_roles_from_spec(
    response: spec.SubordinateRoleSubordinateEntityIdentifierType,
) -> IdentifierType: ...


@overload
def subordinate_roles_from_spec(
    response: spec.QuerySubordinateEntityRolesResponse,
) -> SubordinateEntityRolesQueryResponse: ...


def subordinate_roles_from_spec(response: BaseModel | Enum) -> object:
    return _from_spec(response)


@singledispatch
def _from_spec(response: BaseModel | Enum) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(response).__name__}. "
        f"Register one with @_from_spec.register"
    )


@_from_spec.register
def _(
    response: spec.EntityAuthorizationsAuthorizingEntityIdentifierType,
) -> IdentifierType:
    return _entity_identifier_from_value(response.value)


@_from_spec.register
def _(
    response: spec.SubordinateRoleSubordinateEntityIdentifierType,
) -> IdentifierType:
    return _entity_identifier_from_value(response.value)


@_from_spec.register
def _(response: spec.SubordinateEntityRole) -> SubordinateEntityRoleDetail:
    return SubordinateEntityRoleDetail(
        subordinate_entity_type=subordinate_roles_from_spec(
            response.subordinateEntityIdentifier.type
        ),
        subordinate_entity_value=response.subordinateEntityIdentifier.value,
        role=_map_subordinate_role(response.role),
        description=response.description,
        start_date=response.startDate,
    )


@_from_spec.register
def _(
    response: spec.QuerySubordinateEntityRolesResponse,
) -> SubordinateEntityRolesQueryResponse:
    return SubordinateEntityRolesQueryResponse(
        roles=[subordinate_roles_from_spec(role) for role in response.roles],
        has_more=response.hasMore,
    )
