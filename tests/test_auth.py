from __future__ import annotations

import httpx
import pytest
import respx

from ksef_sdk._auth import (
    init_token_auth,
    poll_auth_status,
    redeem_token,
    request_challenge,
)
from ksef_sdk._environments import Environment
from ksef_sdk._http import HttpTransport
from ksef_sdk.exceptions import KsefAuthError


BASE = "https://ksef-test.mf.gov.pl/api"


@pytest.fixture()
def transport():
    t = HttpTransport(Environment.TEST)
    yield t
    t.close()


class TestRequestChallenge:
    @respx.mock
    def test_returns_challenge(self, transport):
        respx.post(f"{BASE}/auth/challenge").mock(
            return_value=httpx.Response(200, json={
                "challenge": "c" * 36,
                "timestamp": "2025-01-01T00:00:00+00:00",
                "timestampMs": 1735689600000,
            })
        )
        resp = request_challenge(transport)
        assert resp.challenge == "c" * 36


class TestInitTokenAuth:
    @respx.mock
    def test_posts_encrypted_token(self, transport, sample_certificates):
        route = respx.post(f"{BASE}/auth/ksef-token").mock(
            return_value=httpx.Response(200, json={
                "referenceNumber": "r" * 36,
                "authenticationToken": {
                    "token": "jwt.token",
                    "validUntil": "2025-01-02T00:00:00+00:00",
                },
            })
        )

        from ksef_sdk._generated.model import AuthenticationChallengeResponse
        from datetime import datetime, timezone

        challenge = AuthenticationChallengeResponse(
            challenge="c" * 36,
            timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
            timestampMs=1735689600000,
        )

        resp = init_token_auth(
            transport,
            nip="1234567890",
            token="my-secret-token",
            challenge=challenge,
            certificates=sample_certificates,
        )
        assert resp.referenceNumber == "r" * 36

        # Verify the request body contained encrypted token
        import json
        sent = json.loads(route.calls[0].request.content)
        assert sent["challenge"] == "c" * 36
        assert sent["contextIdentifier"]["type"] == "Nip"
        assert sent["contextIdentifier"]["value"] == "1234567890"
        assert "encryptedToken" in sent


class TestPollAuthStatus:
    @respx.mock
    def test_returns_on_success(self, transport):
        respx.get(f"{BASE}/auth/abc").mock(
            return_value=httpx.Response(200, json={
                "startDate": "2025-01-01T00:00:00+00:00",
                "authenticationMethod": "Token",
                "status": {
                    "code": 200,
                    "description": "OK",
                },
            })
        )
        result = poll_auth_status(transport, "abc", poll_interval=0)
        assert result.status.code == 200

    @respx.mock
    def test_raises_on_failure(self, transport):
        respx.get(f"{BASE}/auth/abc").mock(
            return_value=httpx.Response(200, json={
                "startDate": "2025-01-01T00:00:00+00:00",
                "authenticationMethod": "Token",
                "status": {
                    "code": 450,
                    "description": "Invalid token",
                },
            })
        )
        with pytest.raises(KsefAuthError, match="Authentication failed"):
            poll_auth_status(transport, "abc", poll_interval=0)

    @respx.mock
    def test_polls_until_success(self, transport):
        responses = [
            httpx.Response(200, json={
                "startDate": "2025-01-01T00:00:00+00:00",
                "authenticationMethod": "Token",
                "status": {"code": 100, "description": "In progress"},
            }),
            httpx.Response(200, json={
                "startDate": "2025-01-01T00:00:00+00:00",
                "authenticationMethod": "Token",
                "status": {"code": 200, "description": "OK"},
            }),
        ]
        respx.get(f"{BASE}/auth/abc").mock(side_effect=responses)
        result = poll_auth_status(transport, "abc", poll_interval=0, max_attempts=5)
        assert result.status.code == 200

    @respx.mock
    def test_timeout_raises(self, transport):
        respx.get(f"{BASE}/auth/abc").mock(
            return_value=httpx.Response(200, json={
                "startDate": "2025-01-01T00:00:00+00:00",
                "authenticationMethod": "Token",
                "status": {"code": 100, "description": "In progress"},
            })
        )
        with pytest.raises(KsefAuthError, match="timed out"):
            poll_auth_status(transport, "abc", poll_interval=0, max_attempts=2)


class TestRedeemToken:
    @respx.mock
    def test_returns_tokens(self, transport):
        route = respx.post(f"{BASE}/auth/token/redeem").mock(
            return_value=httpx.Response(200, json={
                "accessToken": {
                    "token": "access-jwt",
                    "validUntil": "2025-01-02T00:00:00+00:00",
                },
                "refreshToken": {
                    "token": "refresh-jwt",
                    "validUntil": "2025-02-01T00:00:00+00:00",
                },
            })
        )
        resp = redeem_token(transport, "auth-jwt-token")
        assert resp.accessToken.token == "access-jwt"
        assert resp.refreshToken.token == "refresh-jwt"
        # Verify auth token was sent as Bearer
        assert route.calls[0].request.headers["Authorization"] == "Bearer auth-jwt-token"
