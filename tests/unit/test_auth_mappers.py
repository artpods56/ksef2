"""Tests for auth mapper classes."""

from __future__ import annotations

from datetime import datetime, timezone

from ksef_sdk.domain.models.auth import (
    AuthenticationMethod,
    ContextIdentifierType,
)
from ksef_sdk.infra.mappers.auth import (
    AuthInitMapper,
    AuthStatusMapper,
    AuthTokensMapper,
    ChallengeMapper,
    RefreshTokenMapper,
)
from ksef_sdk.infra.schema import model as spec


_TS = datetime(2025, 7, 11, 12, 0, 0, tzinfo=timezone.utc)
_TS_MS = 1720699200000
_REF = "20250625-SO-2C3E6C8000-B675CF5D68-07"


class TestChallengeMapper:
    def test_maps_fields(self) -> None:
        dto = spec.AuthenticationChallengeResponse(
            challenge="a" * 36,
            timestamp=_TS,
            timestampMs=_TS_MS,
        )

        result = ChallengeMapper.map_response(dto)

        assert result.challenge == "a" * 36
        assert result.timestamp == _TS
        assert result.timestamp_ms == _TS_MS


class TestAuthInitMapper:
    def test_map_token_request_nip(self) -> None:
        result = AuthInitMapper.map_token_request(
            challenge="c" * 36,
            context_type=ContextIdentifierType.NIP,
            context_value="1234567890",
            encrypted_token="encrypted==",
        )

        assert isinstance(result, spec.InitTokenAuthenticationRequest)
        assert result.challenge == "c" * 36
        assert result.contextIdentifier.type == "Nip"
        assert result.contextIdentifier.value == "1234567890"
        assert result.encryptedToken == "encrypted=="

    def test_map_token_request_internal_id(self) -> None:
        result = AuthInitMapper.map_token_request(
            challenge="c" * 36,
            context_type=ContextIdentifierType.INTERNAL_ID,
            context_value="ID-123",
            encrypted_token="enc==",
        )

        assert result.contextIdentifier.type == "InternalId"

    def test_map_response(self) -> None:
        dto = spec.AuthenticationInitResponse(
            referenceNumber=_REF,
            authenticationToken=spec.TokenInfo(
                token="jwt-auth-token",
                validUntil=_TS,
            ),
        )

        result = AuthInitMapper.map_response(dto)

        assert result.reference_number == _REF
        assert result.authentication_token.token == "jwt-auth-token"
        assert result.authentication_token.valid_until == _TS


class TestAuthStatusMapper:
    def test_maps_success_status(self) -> None:
        dto = spec.AuthenticationOperationStatusResponse(
            startDate=_TS,
            authenticationMethod="Token",
            status=spec.StatusInfo(code=200, description="OK"),
        )

        result = AuthStatusMapper.map_response(dto)

        assert result.start_date == _TS
        assert result.authentication_method == AuthenticationMethod.TOKEN
        assert result.status_code == 200
        assert result.status_description == "OK"
        assert result.status_details is None
        assert result.is_token_redeemed is None

    def test_maps_with_details_and_redeemed(self) -> None:
        dto = spec.AuthenticationOperationStatusResponse(
            startDate=_TS,
            authenticationMethod="QualifiedSeal",
            status=spec.StatusInfo(
                code=415, description="Failed", details=["No permissions"]
            ),
            isTokenRedeemed=True,
        )

        result = AuthStatusMapper.map_response(dto)

        assert result.authentication_method == AuthenticationMethod.QUALIFIED_SEAL
        assert result.status_code == 415
        assert result.status_details == ["No permissions"]
        assert result.is_token_redeemed is True


class TestAuthTokensMapper:
    def test_maps_both_tokens(self) -> None:
        later = datetime(2025, 7, 12, 12, 0, 0, tzinfo=timezone.utc)
        dto = spec.AuthenticationTokensResponse(
            accessToken=spec.TokenInfo(token="access-jwt", validUntil=_TS),
            refreshToken=spec.TokenInfo(token="refresh-jwt", validUntil=later),
        )

        result = AuthTokensMapper.map_response(dto)

        assert result.access_token.token == "access-jwt"
        assert result.access_token.valid_until == _TS
        assert result.refresh_token.token == "refresh-jwt"
        assert result.refresh_token.valid_until == later


class TestRefreshTokenMapper:
    def test_maps_access_token(self) -> None:
        dto = spec.AuthenticationTokenRefreshResponse(
            accessToken=spec.TokenInfo(token="new-access", validUntil=_TS),
        )

        result = RefreshTokenMapper.map_response(dto)

        assert result.access_token.token == "new-access"
        assert result.access_token.valid_until == _TS
