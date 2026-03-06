from enum import Enum
from functools import singledispatch
from typing import assert_never, overload

from pydantic import BaseModel

from ksef2.domain.models.permissions import (
    CertificateSubjectIdentifierType,
    PersonPermissionScope,
    SubunitIdentifierType,
    SubunitPermission,
    SubunitPermissionsQueryResponse,
)
from ksef2.infra.schema.api import spec


def _map_cert_subject_identifier_type(
    response: spec.CertificateSubjectIdentifierType,
) -> CertificateSubjectIdentifierType:
    match response:
        case spec.CertificateSubjectIdentifierType.Nip:
            return "nip"
        case spec.CertificateSubjectIdentifierType.Pesel:
            return "pesel"
        case spec.CertificateSubjectIdentifierType.Fingerprint:
            return "fingerprint"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def _map_subunit_context_identifier_type(
    response: spec.SubunitPermissionsContextIdentifierType,
) -> SubunitIdentifierType:
    match response:
        case spec.SubunitPermissionsContextIdentifierType.Nip:
            return "nip"
        case spec.SubunitPermissionsContextIdentifierType.InternalId:
            return "internal_id"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


def _map_subunit_permission_scope(
    response: spec.SubunitPermissionScope,
) -> PersonPermissionScope:
    match response:
        case spec.SubunitPermissionScope.CredentialsManage:
            return "credentials_manage"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


@singledispatch
def _from_spec(response: BaseModel | Enum) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(response).__name__}. "
        f"Register one with @_from_spec.register"
    )


@overload
def subunit_from_spec(response: spec.SubunitPermission) -> SubunitPermission: ...


@overload
def subunit_from_spec(
    response: spec.QuerySubunitPermissionsResponse,
) -> SubunitPermissionsQueryResponse: ...


def subunit_from_spec(response: BaseModel | Enum) -> object:
    return _from_spec(response)


@_from_spec.register
def _(response: spec.SubunitPermission) -> SubunitPermission:
    person_first_name = None
    person_last_name = None
    entity_first_name = None
    entity_last_name = None
    if response.subjectPersonDetails:
        person_first_name = response.subjectPersonDetails.firstName
        person_last_name = response.subjectPersonDetails.lastName

    return SubunitPermission(
        id=response.id,
        author_type=_map_cert_subject_identifier_type(response.authorIdentifier.type),
        author_value=response.authorIdentifier.value,
        authorized_type=_map_cert_subject_identifier_type(
            response.authorizedIdentifier.type
        ),
        authorized_value=response.authorizedIdentifier.value,
        permission_type=_map_subunit_permission_scope(response.permissionScope),
        description=response.description,
        start_date=response.startDate,
        subject_first_name=person_first_name,
        subject_last_name=person_last_name,
        entity_first_name=entity_first_name,
        entity_last_name=entity_last_name,
        subunit_name=response.subunitName,
        subunit_type=_map_subunit_context_identifier_type(
            response.subunitIdentifier.type
        ),
        subunit_value=response.subunitIdentifier.value,
    )


@_from_spec.register
def _(
    response: spec.QuerySubunitPermissionsResponse,
) -> SubunitPermissionsQueryResponse:
    return SubunitPermissionsQueryResponse(
        permissions=[subunit_from_spec(p) for p in response.permissions],
        has_more=response.hasMore,
    )
