from ksef2.infra.schema.api.supp.testdata import (
    BlockContextRequest,
    CreatePersonRequest,
    CreateSubjectRequest,
    DeletePersonRequest,
    DeleteSubjectRequest,
    EnableAttachmentsRequest,
    GrantPermissionsRequest,
    RevokeAttachmentsRequest,
    RevokePermissionsRequest,
    UnblockContextRequest,
)
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="td_create_subject_req")
class CreateSubjectRequestFactory(ModelFactory[CreateSubjectRequest]): ...


@register_fixture(name="td_delete_subject_req")
class DeleteSubjectRequestFactory(ModelFactory[DeleteSubjectRequest]): ...


@register_fixture(name="td_create_person_req")
class CreatePersonRequestFactory(ModelFactory[CreatePersonRequest]): ...


@register_fixture(name="td_delete_person_req")
class DeletePersonRequestFactory(ModelFactory[DeletePersonRequest]): ...


@register_fixture(name="td_grant_permissions_req")
class GrantPermissionsRequestFactory(ModelFactory[GrantPermissionsRequest]): ...


@register_fixture(name="td_revoke_permissions_req")
class RevokePermissionsRequestFactory(ModelFactory[RevokePermissionsRequest]): ...


@register_fixture(name="td_enable_attachments_req")
class EnableAttachmentsRequestFactory(ModelFactory[EnableAttachmentsRequest]): ...


@register_fixture(name="td_revoke_attachments_req")
class RevokeAttachmentsRequestFactory(ModelFactory[RevokeAttachmentsRequest]): ...


@register_fixture(name="td_block_context_req")
class BlockContextRequestFactory(ModelFactory[BlockContextRequest]): ...


@register_fixture(name="td_unblock_context_req")
class UnblockContextRequestFactory(ModelFactory[UnblockContextRequest]): ...
