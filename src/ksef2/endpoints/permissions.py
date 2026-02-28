from typing import final, Unpack

from ksef2.core import routes
from ksef2.endpoints.base import OffsetPaginationQueryParams
from ksef2.endpoints.base import BaseEndpoints
from ksef2.infra.schema.api import spec


@final
class PermissionsGrantEndpoints(BaseEndpoints):
    def grant_person(
        self,
        request: spec.PersonPermissionsGrantRequest,
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_PERSON,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )

    def grant_entity(
        self, request: spec.EntityPermissionsGrantRequest
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_ENTITY,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )

    def grant_authorization(
        self, request: spec.EntityAuthorizationPermissionsGrantRequest
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_AUTHORIZATION,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )

    def grant_indirect(
        self, request: spec.IndirectPermissionsGrantRequest
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_INDIRECT,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )

    def grant_subunit(
        self, request: spec.SubunitPermissionsGrantRequest
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_SUBUNITS,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )

    def grant_administered_eu_entity(
        self, request: spec.EuEntityAdministrationPermissionsGrantRequest
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_ADMINISTERED_EU_ENTITY,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )

    def grant_eu_entity(
        self, request: spec.EuEntityPermissionsGrantRequest
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.post(
                path=routes.GrantPermissionsRoutes.GRANT_EU_ENTITY,
                json=request.model_dump(mode="json"),
            ),
            spec.PermissionsOperationResponse,
        )


@final
class RevokePermissionsEndpoints(BaseEndpoints):
    def revoke_person(self, permission_id: str) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.delete(
                path=routes.RevokePermissionsRoutes.REVOKE_PERMISSION.format(
                    permissionId=permission_id
                ),
            ),
            spec.PermissionsOperationResponse,
        )

    def revoke_authorization(
        self, permission_id: str
    ) -> spec.PermissionsOperationResponse:
        return self._parse(
            self._transport.delete(
                path=routes.RevokePermissionsRoutes.REVOKE_AUTHORIZATION_PERMISSION.format(
                    permissionId=permission_id
                ),
            ),
            spec.PermissionsOperationResponse,
        )


@final
class QueryPermissionsEndpoints(BaseEndpoints):
    def query_personal_grants(
        self,
        request: spec.PersonalPermissionsQueryRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryPersonalPermissionsResponse:
        return self._parse(
            self._transport.post(
                path=routes.QueryPermissionsRoutes.QUERY_PERSONAL_GRANTS,
                params=self.build_params(params),
                json=request.model_dump(mode="json"),
            ),
            spec.QueryPersonalPermissionsResponse,
        )

    def query_attachments_status(self) -> spec.CheckAttachmentPermissionStatusResponse:
        return self._parse(
            self._transport.get(
                path=routes.QueryPermissionsRoutes.QUERY_ATTACHMENTS_STATUS,
            ),
            spec.CheckAttachmentPermissionStatusResponse,
        )

    def query_authorizations_grants(
        self,
        request: spec.EntityAuthorizationPermissionsQueryRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryEntityAuthorizationPermissionsResponse:
        return self._parse(
            self._transport.post(
                path=routes.QueryPermissionsRoutes.QUERY_AUTHORIZATIONS_GRANTS,
                params=self.build_params(params),
                json=request.model_dump(mode="json"),
            ),
            spec.QueryEntityAuthorizationPermissionsResponse,
        )

    def query_eu_entities_grants(
        self,
        request: spec.EuEntityPermissionsQueryRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryEuEntityPermissionsResponse:
        return self._parse(
            self._transport.post(
                path=routes.QueryPermissionsRoutes.QUERY_EU_ENTITIES_GRANTS,
                params=self.build_params(params),
                json=request.model_dump(mode="json"),
            ),
            spec.QueryEuEntityPermissionsResponse,
        )

    def query_persons_grants(
        self,
        request: spec.PersonPermissionsQueryRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryPersonPermissionsResponse:
        return self._parse(
            self._transport.post(
                path=routes.QueryPermissionsRoutes.QUERY_PERSONS_GRANTS,
                params=self.build_params(params),
                json=request.model_dump(mode="json"),
            ),
            spec.QueryPersonPermissionsResponse,
        )

    def query_subordinate_entities_roles(
        self,
        request: spec.SubordinateEntityRolesQueryRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QuerySubordinateEntityRolesResponse:
        return self._parse(
            self._transport.post(
                path=routes.QueryPermissionsRoutes.QUERY_SUBORDINATE_ENTITIES_ROLES,
                params=self.build_params(params),
                json=request.model_dump(mode="json"),
            ),
            spec.QuerySubordinateEntityRolesResponse,
        )

    def query_subunits_grants(
        self,
        request: spec.SubunitPermissionsQueryRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QuerySubunitPermissionsResponse:
        return self._parse(
            self._transport.post(
                path=routes.QueryPermissionsRoutes.QUERY_SUBUNITS_GRANTS,
                params=self.build_params(params),
                json=request.model_dump(mode="json"),
            ),
            spec.QuerySubunitPermissionsResponse,
        )


@final
class GetPermissionsEndpoints(BaseEndpoints):
    def query_operation_status(
        self,
        reference_number: str,
    ) -> spec.PermissionsOperationStatusResponse:
        return self._parse(
            self._transport.get(
                path=routes.QueryPermissionsRoutes.QUERY_OPERATIONS_STATUS.format(
                    referenceNumber=reference_number
                ),
            ),
            spec.PermissionsOperationStatusResponse,
        )

    def query_entity_roles(
        self,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryEntityRolesResponse:
        return self._parse(
            self._transport.get(
                path=routes.QueryPermissionsRoutes.QUERY_ENTITY_ROLES,
                params=self.build_params(params),
            ),
            spec.QueryEntityRolesResponse,
        )
