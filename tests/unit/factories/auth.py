from ksef2.infra.schema.api import spec
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="auth_challenge_resp")
class AuthenticationChallengeResponseFactory(
    ModelFactory[spec.AuthenticationChallengeResponse]
): ...


@register_fixture(name="auth_init_resp")
class AuthenticationInitResponseFactory(
    ModelFactory[spec.AuthenticationInitResponse]
): ...


@register_fixture(name="auth_status_resp")
class AuthenticationOperationStatusResponseFactory(
    ModelFactory[spec.AuthenticationOperationStatusResponse]
): ...


@register_fixture(name="auth_tokens_resp")
class AuthenticationTokensResponseFactory(
    ModelFactory[spec.AuthenticationTokensResponse]
): ...


@register_fixture(name="auth_refresh_resp")
class AuthenticationTokenRefreshResponseFactory(
    ModelFactory[spec.AuthenticationTokenRefreshResponse]
): ...


@register_fixture(name="auth_list_resp")
class AuthenticationListResponseFactory(
    ModelFactory[spec.AuthenticationListResponse]
): ...


@register_fixture(name="auth_init_req")
class InitTokenAuthenticationRequestFactory(
    ModelFactory[spec.InitTokenAuthenticationRequest]
): ...
