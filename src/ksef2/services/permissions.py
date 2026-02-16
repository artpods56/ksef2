from typing import final

from ksef2.core import protocols
from ksef2.domain.models.invoices import PaginationParams
from ksef2.domain.models.permissions import (
    AttachmentPermissionStatus,
    AuthorizationPermissionsQueryRequest,
    AuthorizationPermissionsQueryResponse,
    AuthorizationPermissionType,
    AuthorizationSubjectIdentifierType,
    EntityPermission,
    EntityRolesResponse,
    EuEntityAdminContextIdentifierType,
    EuEntityPermissionsQueryRequest,
    EuEntityPermissionsQueryResponse,
    EuEntityPermissionType,
    GrantPermissionsResponse,
    IndirectPermissionType,
    IndirectTargetIdentifierType,
    PermissionOperationStatusResponse,
    PersonalPermissionsQueryRequest,
    PersonalPermissionsQueryResponse,
    PersonPermissionsQueryRequest,
    PersonPermissionsQueryResponse,
    SubordinateEntityRolesQueryRequest,
    SubordinateEntityRolesQueryResponse,
    SubunitIdentifierType,
    SubunitPermissionsQueryRequest,
    SubunitPermissionsQueryResponse,
)
from ksef2.domain.models.session import SessionState
from ksef2.domain.models.testdata import IdentifierType, PermissionType
from ksef2.endpoints.permissions import (
    GetAttachmentPermissionStatusEndpoint,
    GetEntityRolesEndpoint,
    GetPermissionOperationStatusEndpoint,
    GrantAuthorizationPermissionsEndpoint,
    GrantEntityPermissionsEndpoint,
    GrantEuEntityAdministrationPermissionsEndpoint,
    GrantEuEntityPermissionsEndpoint,
    GrantIndirectPermissionsEndpoint,
    GrantPersonPermissionsEndpoint,
    GrantSubunitPermissionsEndpoint,
    QueryAuthorizationsPermissionsEndpoint,
    QueryEuEntitiesPermissionsEndpoint,
    QueryPersonalPermissionsEndpoint,
    QueryPersonsPermissionsEndpoint,
    QuerySubordinateEntitiesRolesEndpoint,
    QuerySubunitsPermissionsEndpoint,
    RevokeAuthorizationPermissionsEndpoint,
    RevokeCommonPermissionsEndpoint,
)
from ksef2.infra.mappers.permissions import PermissionsMapper


@final
class PermissionsService:
    def __init__(self, transport: protocols.Middleware, state: SessionState) -> None:
        self._state = state
        self._person_ep = GrantPersonPermissionsEndpoint(transport)
        self._entity_ep = GrantEntityPermissionsEndpoint(transport)
        self._authorization_ep = GrantAuthorizationPermissionsEndpoint(transport)
        self._indirect_ep = GrantIndirectPermissionsEndpoint(transport)
        self._subunit_ep = GrantSubunitPermissionsEndpoint(transport)
        self._eu_entity_ep = GrantEuEntityPermissionsEndpoint(transport)
        self._eu_entity_admin_ep = GrantEuEntityAdministrationPermissionsEndpoint(
            transport
        )
        self._revoke_authorization_ep = RevokeAuthorizationPermissionsEndpoint(
            transport
        )
        self._revoke_common_ep = RevokeCommonPermissionsEndpoint(transport)
        self._attachment_status_ep = GetAttachmentPermissionStatusEndpoint(transport)
        self._operation_status_ep = GetPermissionOperationStatusEndpoint(transport)
        self._entity_roles_ep = GetEntityRolesEndpoint(transport)
        self._query_authorizations_ep = QueryAuthorizationsPermissionsEndpoint(
            transport
        )
        self._query_eu_entities_ep = QueryEuEntitiesPermissionsEndpoint(transport)
        self._query_personal_ep = QueryPersonalPermissionsEndpoint(transport)
        self._query_persons_ep = QueryPersonsPermissionsEndpoint(transport)
        self._query_subordinate_entities_ep = QuerySubordinateEntitiesRolesEndpoint(
            transport
        )
        self._query_subunits_ep = QuerySubunitsPermissionsEndpoint(transport)

    def grant_person(
        self,
        *,
        subject_identifier: IdentifierType,
        subject_value: str,
        permissions: list[PermissionType],
        description: str,
        first_name: str,
        last_name: str,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_person_grant_request(
            subject_identifier=subject_identifier,
            subject_value=subject_value,
            permissions=permissions,
            description=description,
            first_name=first_name,
            last_name=last_name,
        )
        spec_resp = self._person_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def grant_entity(
        self,
        *,
        subject_value: str,
        permissions: list[EntityPermission],
        description: str,
        entity_name: str,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_entity_grant_request(
            subject_value=subject_value,
            permissions=permissions,
            description=description,
            entity_name=entity_name,
        )
        spec_resp = self._entity_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def grant_authorization(
        self,
        *,
        subject_type: AuthorizationSubjectIdentifierType,
        subject_value: str,
        permission: AuthorizationPermissionType,
        description: str,
        entity_name: str,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_authorization_grant_request(
            subject_type=subject_type,
            subject_value=subject_value,
            permission=permission,
            description=description,
            entity_name=entity_name,
        )
        spec_resp = self._authorization_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def grant_indirect(
        self,
        *,
        subject_identifier: IdentifierType,
        subject_value: str,
        permissions: list[IndirectPermissionType],
        description: str,
        first_name: str,
        last_name: str,
        target_identifier: IndirectTargetIdentifierType | None = None,
        target_value: str | None = None,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_indirect_grant_request(
            subject_identifier=subject_identifier,
            subject_value=subject_value,
            permissions=permissions,
            description=description,
            first_name=first_name,
            last_name=last_name,
            target_identifier=target_identifier,
            target_value=target_value,
        )
        spec_resp = self._indirect_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def grant_subunit(
        self,
        *,
        subject_identifier: IdentifierType,
        subject_value: str,
        context_identifier: SubunitIdentifierType,
        context_value: str,
        description: str,
        first_name: str,
        last_name: str,
        subunit_name: str | None = None,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_subunit_grant_request(
            subject_identifier=subject_identifier,
            subject_value=subject_value,
            context_identifier=context_identifier,
            context_value=context_value,
            description=description,
            first_name=first_name,
            last_name=last_name,
            subunit_name=subunit_name,
        )
        spec_resp = self._subunit_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def grant_eu_entity(
        self,
        *,
        subject_value: str,
        permissions: list[EuEntityPermissionType],
        description: str,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_eu_entity_grant_request(
            subject_value=subject_value,
            permissions=permissions,
            description=description,
        )
        spec_resp = self._eu_entity_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def grant_eu_entity_administration(
        self,
        *,
        subject_value: str,
        context_identifier: EuEntityAdminContextIdentifierType,
        context_value: str,
        description: str,
        eu_entity_name: str,
    ) -> GrantPermissionsResponse:
        body = PermissionsMapper.map_eu_entity_admin_grant_request(
            subject_value=subject_value,
            context_identifier=context_identifier,
            context_value=context_value,
            description=description,
            eu_entity_name=eu_entity_name,
        )
        spec_resp = self._eu_entity_admin_ep.send(
            access_token=self._state.access_token,
            body=body.model_dump(),
        )
        return PermissionsMapper.map_response(spec_resp)

    def revoke_authorization(
        self,
        *,
        permission_id: str,
    ) -> GrantPermissionsResponse:
        spec_resp = self._revoke_authorization_ep.send(
            access_token=self._state.access_token,
            permission_id=permission_id,
        )
        return PermissionsMapper.map_response(spec_resp)

    def revoke_common(
        self,
        *,
        permission_id: str,
    ) -> GrantPermissionsResponse:
        spec_resp = self._revoke_common_ep.send(
            access_token=self._state.access_token,
            permission_id=permission_id,
        )
        return PermissionsMapper.map_response(spec_resp)

    def get_attachment_permission_status(self) -> AttachmentPermissionStatus:
        spec_resp = self._attachment_status_ep.send(
            access_token=self._state.access_token,
        )
        return PermissionsMapper.map_attachment_status_response(spec_resp)

    def get_operation_status(
        self,
        *,
        reference_number: str,
    ) -> PermissionOperationStatusResponse:
        spec_resp = self._operation_status_ep.send(
            access_token=self._state.access_token,
            reference_number=reference_number,
        )
        return PermissionsMapper.map_operation_status_response(spec_resp)

    def get_entity_roles(
        self,
        *,
        page_offset: int = 0,
        page_size: int = 10,
    ) -> EntityRolesResponse:
        spec_resp = self._entity_roles_ep.send(
            access_token=self._state.access_token,
            page_offset=page_offset,
            page_size=page_size,
        )
        return PermissionsMapper.map_entity_roles_response(spec_resp)

    def query_authorizations(
        self,
        *,
        query: AuthorizationPermissionsQueryRequest,
        params: PaginationParams | None = None,
    ) -> AuthorizationPermissionsQueryResponse:
        spec_resp = self._query_authorizations_ep.send(
            access_token=self._state.access_token,
            body=PermissionsMapper.map_authorizations_query_request(query).model_dump(),
            **params.to_api_params() if params else PaginationParams().to_api_params(),
        )
        return PermissionsMapper.map_authorizations_query_response(spec_resp)

    def query_eu_entities(
        self,
        *,
        query: EuEntityPermissionsQueryRequest,
        params: PaginationParams | None = None,
    ) -> EuEntityPermissionsQueryResponse:
        spec_resp = self._query_eu_entities_ep.send(
            access_token=self._state.access_token,
            body=PermissionsMapper.map_eu_entities_query_request(query).model_dump(),
            **params.to_api_params() if params else PaginationParams().to_api_params(),
        )
        return PermissionsMapper.map_eu_entities_query_response(spec_resp)

    def query_personal(
        self,
        *,
        query: PersonalPermissionsQueryRequest,
        params: PaginationParams | None = None,
    ) -> PersonalPermissionsQueryResponse:
        spec_resp = self._query_personal_ep.send(
            access_token=self._state.access_token,
            body=PermissionsMapper.map_personal_query_request(query).model_dump(),
            **params.to_api_params() if params else PaginationParams().to_api_params(),
        )
        return PermissionsMapper.map_personal_query_response(spec_resp)

    def query_persons(
        self,
        *,
        query: PersonPermissionsQueryRequest,
        params: PaginationParams | None = None,
    ) -> PersonPermissionsQueryResponse:
        spec_resp = self._query_persons_ep.send(
            access_token=self._state.access_token,
            body=PermissionsMapper.map_person_query_request(query).model_dump(),
            **params.to_api_params() if params else PaginationParams().to_api_params(),
        )
        return PermissionsMapper.map_person_permissions_query_response(spec_resp)

    def query_subordinate_entities(
        self,
        *,
        query: SubordinateEntityRolesQueryRequest,
        params: PaginationParams | None = None,
    ) -> SubordinateEntityRolesQueryResponse:
        spec_resp = self._query_subordinate_entities_ep.send(
            access_token=self._state.access_token,
            body=PermissionsMapper.map_subordinate_entities_query_request(
                query
            ).model_dump(),
            **params.to_api_params() if params else PaginationParams().to_api_params(),
        )
        return PermissionsMapper.map_subordinate_entities_query_response(spec_resp)

    def query_subunits(
        self,
        *,
        query: SubunitPermissionsQueryRequest,
        params: PaginationParams | None = None,
    ) -> SubunitPermissionsQueryResponse:
        spec_resp = self._query_subunits_ep.send(
            access_token=self._state.access_token,
            body=PermissionsMapper.map_subunits_query_request(query).model_dump(),
            **params.to_api_params() if params else PaginationParams().to_api_params(),
        )
        return PermissionsMapper.map_subunits_query_response(spec_resp)
