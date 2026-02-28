from ksef2.infra.schema.api import spec
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="perm_grant_person_req")
class PersonPermissionsGrantRequestFactory(
    ModelFactory[spec.PersonPermissionsGrantRequest]
): ...


@register_fixture(name="perm_grant_entity_req")
class EntityPermissionsGrantRequestFactory(
    ModelFactory[spec.EntityPermissionsGrantRequest]
): ...


@register_fixture(name="perm_grant_auth_req")
class EntityAuthorizationPermissionsGrantRequestFactory(
    ModelFactory[spec.EntityAuthorizationPermissionsGrantRequest]
): ...


@register_fixture(name="perm_grant_indirect_req")
class IndirectPermissionsGrantRequestFactory(
    ModelFactory[spec.IndirectPermissionsGrantRequest]
): ...


@register_fixture(name="perm_grant_subunit_req")
class SubunitPermissionsGrantRequestFactory(
    ModelFactory[spec.SubunitPermissionsGrantRequest]
): ...


@register_fixture(name="perm_grant_eu_admin_req")
class EuEntityAdministrationPermissionsGrantRequestFactory(
    ModelFactory[spec.EuEntityAdministrationPermissionsGrantRequest]
): ...


@register_fixture(name="perm_grant_eu_entity_req")
class EuEntityPermissionsGrantRequestFactory(
    ModelFactory[spec.EuEntityPermissionsGrantRequest]
): ...


@register_fixture(name="perm_op_resp")
class PermissionsOperationResponseFactory(
    ModelFactory[spec.PermissionsOperationResponse]
): ...


@register_fixture(name="perm_query_personal_req")
class PersonalPermissionsQueryRequestFactory(
    ModelFactory[spec.PersonalPermissionsQueryRequest]
): ...


@register_fixture(name="perm_query_personal_resp")
class QueryPersonalPermissionsResponseFactory(
    ModelFactory[spec.QueryPersonalPermissionsResponse]
): ...


@register_fixture(name="perm_attachment_status_resp")
class CheckAttachmentPermissionStatusResponseFactory(
    ModelFactory[spec.CheckAttachmentPermissionStatusResponse]
): ...


@register_fixture(name="perm_query_auth_req")
class EntityAuthorizationPermissionsQueryRequestFactory(
    ModelFactory[spec.EntityAuthorizationPermissionsQueryRequest]
): ...


@register_fixture(name="perm_query_auth_resp")
class QueryEntityAuthorizationPermissionsResponseFactory(
    ModelFactory[spec.QueryEntityAuthorizationPermissionsResponse]
): ...


@register_fixture(name="perm_query_eu_entity_req")
class EuEntityPermissionsQueryRequestFactory(
    ModelFactory[spec.EuEntityPermissionsQueryRequest]
): ...


@register_fixture(name="perm_query_eu_entity_resp")
class QueryEuEntityPermissionsResponseFactory(
    ModelFactory[spec.QueryEuEntityPermissionsResponse]
): ...


@register_fixture(name="perm_query_person_req")
class PersonPermissionsQueryRequestFactory(
    ModelFactory[spec.PersonPermissionsQueryRequest]
): ...


@register_fixture(name="perm_query_person_resp")
class QueryPersonPermissionsResponseFactory(
    ModelFactory[spec.QueryPersonPermissionsResponse]
): ...


@register_fixture(name="perm_query_subordinate_req")
class SubordinateEntityRolesQueryRequestFactory(
    ModelFactory[spec.SubordinateEntityRolesQueryRequest]
): ...


@register_fixture(name="perm_query_subordinate_resp")
class QuerySubordinateEntityRolesResponseFactory(
    ModelFactory[spec.QuerySubordinateEntityRolesResponse]
): ...


@register_fixture(name="perm_query_subunit_req")
class SubunitPermissionsQueryRequestFactory(
    ModelFactory[spec.SubunitPermissionsQueryRequest]
): ...


@register_fixture(name="perm_query_subunit_resp")
class QuerySubunitPermissionsResponseFactory(
    ModelFactory[spec.QuerySubunitPermissionsResponse]
): ...


@register_fixture(name="perm_op_status_resp")
class PermissionsOperationStatusResponseFactory(
    ModelFactory[spec.PermissionsOperationStatusResponse]
): ...


@register_fixture(name="perm_entity_roles_resp")
class QueryEntityRolesResponseFactory(ModelFactory[spec.QueryEntityRolesResponse]): ...
