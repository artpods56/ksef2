from ksef2.infra.schema.api import spec
from ksef2.infra.schema.api.supp.session import (
    OpenOnlineSessionRequest,
    OpenBatchSessionRequest,
)
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="session_open_online_req")
class OpenOnlineSessionRequestFactory(ModelFactory[OpenOnlineSessionRequest]): ...


@register_fixture(name="session_open_online_resp")
class OpenOnlineSessionResponseFactory(
    ModelFactory[spec.OpenOnlineSessionResponse]
): ...


@register_fixture(name="session_open_batch_req")
class OpenBatchSessionRequestFactory(ModelFactory[OpenBatchSessionRequest]): ...


@register_fixture(name="session_open_batch_resp")
class OpenBatchSessionResponseFactory(ModelFactory[spec.OpenBatchSessionResponse]): ...


@register_fixture(name="session_list_resp")
class SessionsQueryResponseFactory(ModelFactory[spec.SessionsQueryResponse]): ...
