from ksef_sdk.domain.models.auth import (
    AuthInitResponse,
    AuthOperationStatus,
    AuthenticationMethod,
    AuthTokens,
    ChallengeResponse,
    ContextIdentifierType,
    RefreshedToken,
    TokenCredentials,
)
from ksef_sdk.infra.schema import model as spec


class ChallengeMapper:
    @staticmethod
    def map_response(r: spec.AuthenticationChallengeResponse) -> ChallengeResponse:
        return ChallengeResponse(
            challenge=r.challenge,
            timestamp=r.timestamp,
            timestamp_ms=r.timestampMs,
        )


class AuthInitMapper:
    @staticmethod
    def map_token_request(
        challenge: str,
        context_type: ContextIdentifierType,
        context_value: str,
        encrypted_token: str,
    ) -> spec.InitTokenAuthenticationRequest:
        return spec.InitTokenAuthenticationRequest.model_construct(
            challenge=challenge,
            contextIdentifier=spec.AuthenticationContextIdentifier(
                type=context_type.value,
                value=context_value,
            ),
            encryptedToken=encrypted_token,
        )

    @staticmethod
    def map_response(r: spec.AuthenticationInitResponse) -> AuthInitResponse:
        return AuthInitResponse(
            reference_number=r.referenceNumber,
            authentication_token=TokenCredentials(
                token=r.authenticationToken.token,
                valid_until=r.authenticationToken.validUntil,
            ),
        )


class AuthStatusMapper:
    @staticmethod
    def map_response(
        r: spec.AuthenticationOperationStatusResponse,
    ) -> AuthOperationStatus:
        return AuthOperationStatus(
            start_date=r.startDate,
            authentication_method=AuthenticationMethod(r.authenticationMethod),
            status_code=r.status.code,
            status_description=r.status.description,
            status_details=r.status.details,
            is_token_redeemed=r.isTokenRedeemed,
        )


class AuthTokensMapper:
    @staticmethod
    def map_response(r: spec.AuthenticationTokensResponse) -> AuthTokens:
        return AuthTokens(
            access_token=TokenCredentials(
                token=r.accessToken.token,
                valid_until=r.accessToken.validUntil,
            ),
            refresh_token=TokenCredentials(
                token=r.refreshToken.token,
                valid_until=r.refreshToken.validUntil,
            ),
        )


class RefreshTokenMapper:
    @staticmethod
    def map_response(r: spec.AuthenticationTokenRefreshResponse) -> RefreshedToken:
        return RefreshedToken(
            access_token=TokenCredentials(
                token=r.accessToken.token,
                valid_until=r.accessToken.validUntil,
            ),
        )
