from ksef2.infra.schema.api import spec
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="token_generate_req")
class GenerateTokenRequestFactory(ModelFactory[spec.GenerateTokenRequest]): ...


@register_fixture(name="token_generate_resp")
class GenerateTokenResponseFactory(ModelFactory[spec.GenerateTokenResponse]): ...


@register_fixture(name="token_status_resp")
class TokenStatusResponseFactory(ModelFactory[spec.TokenStatusResponse]): ...


@register_fixture(name="token_list_resp")
class QueryTokensResponseFactory(ModelFactory[spec.QueryTokensResponse]): ...
