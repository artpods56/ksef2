from __future__ import annotations

from ksef2.domain.models._deprecated.auth import (
    AuthInitResponse,
    AuthStatusResponse,
    AuthTokens,
    ChallengeResponse,
    PublicKeyCertificateInfo,
    RefreshedToken,
)
from ksef2.infra.schema import model as spec


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
    def map_request(
        challenge: str,
        nip: str,
        encrypted_token: str,
    ) -> spec.InitTokenAuthenticationRequest:
        return spec.InitTokenAuthenticationRequest.model_construct(
            challenge=challenge,
            contextIdentifier=spec.AuthenticationContextIdentifier(
                type="Nip", value=nip
            ),
            encryptedToken=encrypted_token,
        )

    @staticmethod
    def map_response(r: spec.AuthenticationInitResponse) -> AuthInitResponse:
        return AuthInitResponse(
            reference_number=r.referenceNumber,
            authentication_token=r.authenticationToken.token,
            authentication_token_valid_until=r.authenticationToken.validUntil,
        )


class AuthStatusMapper:
    @staticmethod
    def map_response(
        r: spec.AuthenticationOperationStatusResponse,
    ) -> AuthStatusResponse:
        return AuthStatusResponse(
            start_date=r.startDate,
            authentication_method=r.authenticationMethod,
            status_code=r.status.code,
            status_description=r.status.description,
        )


class AuthTokensMapper:
    @staticmethod
    def map_response(r: spec.AuthenticationTokensResponse) -> AuthTokens:
        return AuthTokens(
            access_token=r.accessToken.token,
            access_token_valid_until=r.accessToken.validUntil,
            refresh_token=r.refreshToken.token,
            refresh_token_valid_until=r.refreshToken.validUntil,
        )


class RefreshedTokenMapper:
    @staticmethod
    def map_response(r: spec.AuthenticationTokenRefreshResponse) -> RefreshedToken:
        return RefreshedToken(
            access_token=r.accessToken.token,
            access_token_valid_until=r.accessToken.validUntil,
        )


class PublicKeyCertificateMapper:
    @staticmethod
    def map_response(r: spec.PublicKeyCertificate) -> PublicKeyCertificateInfo:
        return PublicKeyCertificateInfo(
            certificate=r.certificate,
            valid_from=r.validFrom,
            valid_to=r.validTo,
            usage=r.usage,
        )

    @staticmethod
    def map_response_list(
        items: list[spec.PublicKeyCertificate],
    ) -> list[PublicKeyCertificateInfo]:
        return [PublicKeyCertificateMapper.map_response(i) for i in items]
