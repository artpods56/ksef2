from ksef2.domain.models.auth import InitTokenAuthenticationRequest
from ksef2.infra.mappers.auth import from_spec, to_spec
from ksef2.infra.schema.api import spec
from ksef2.infra.schema.api.supp.auth import (
    InitTokenAuthenticationRequest as SuppInitTokenAuthenticationRequest,
)


class ChallengeMapper:
    @staticmethod
    def map_response(
        response: spec.AuthenticationChallengeResponse,
    ):
        return from_spec(response)


class AuthInitMapper:
    @staticmethod
    def map_token_request(
        challenge: str,
        context_type: str,
        context_value: str,
        encrypted_token: str,
    ) -> SuppInitTokenAuthenticationRequest:
        return to_spec(
            InitTokenAuthenticationRequest(
                challenge=challenge,
                context_type=context_type,
                context_value=context_value,
                encrypted_token=encrypted_token,
            )
        )

    @staticmethod
    def map_response(response: spec.AuthenticationInitResponse):
        return from_spec(response)


class AuthStatusMapper:
    @staticmethod
    def map_response(response: spec.AuthenticationOperationStatusResponse):
        return from_spec(response)


class AuthTokensMapper:
    @staticmethod
    def map_response(response: spec.AuthenticationTokensResponse):
        return from_spec(response)


class RefreshTokenMapper:
    @staticmethod
    def map_response(response: spec.AuthenticationTokenRefreshResponse):
        return from_spec(response)
