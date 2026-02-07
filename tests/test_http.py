from __future__ import annotations

import httpx
import pytest
import respx

from ksef_sdk._environments import Environment
from ksef_sdk._generated.model import AuthenticationChallengeResponse
from ksef_sdk._http import HttpTransport
from ksef_sdk.exceptions import KsefApiError, KsefAuthError, KsefRateLimitError


@pytest.fixture()
def transport():
    t = HttpTransport(Environment.TEST)
    yield t
    t.close()


class TestRequest:
    @respx.mock
    def test_get_deserializes(self, transport):
        respx.get(
            "https://api-test.ksef.mf.gov.pl/api/v2/auth/challenge",
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "challenge": "a" * 36,
                    "timestamp": "2025-01-01T00:00:00+00:00",
                    "timestampMs": 1735689600000,
                },
            )
        )
        resp = transport.get(
            "/auth/challenge",
            response_model=AuthenticationChallengeResponse,
        )
        assert resp.challenge == "a" * 36
        assert resp.timestampMs == 1735689600000

    @respx.mock
    def test_post_serializes_body(self, transport):
        from ksef_sdk._generated.model import (
            InitTokenAuthenticationRequest,
            AuthenticationContextIdentifier,
        )

        route = respx.post(
            "https://api-test.ksef.mf.gov.pl/api/v2/auth/ksef-token",
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "referenceNumber": "r" * 36,
                    "authenticationToken": {
                        "token": "jwt.token.here",
                        "validUntil": "2025-01-02T00:00:00+00:00",
                    },
                },
            )
        )

        from ksef_sdk._generated.model import AuthenticationInitResponse

        body = InitTokenAuthenticationRequest(
            challenge="c" * 36,
            contextIdentifier=AuthenticationContextIdentifier(
                type="Nip", value="1234567890"
            ),
            encryptedToken="ZW5jcnlwdGVk",  # base64 of "encrypted"
        )
        resp = transport.post(
            "/auth/ksef-token",
            body=body,
            response_model=AuthenticationInitResponse,
        )
        assert resp.referenceNumber == "r" * 36

        # Verify the body was serialized with camelCase keys
        sent = route.calls[0].request
        import json

        sent_json = json.loads(sent.content)
        assert "contextIdentifier" in sent_json
        assert "encryptedToken" in sent_json


class TestBearerToken:
    @respx.mock
    def test_sets_auth_header(self, transport):
        route = respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(200)
        )

        transport.set_access_token("my-jwt")
        transport.request("GET", "/test")

        assert route.calls[0].request.headers["Authorization"] == "Bearer my-jwt"

    @respx.mock
    def test_clears_auth_header(self, transport):
        route = respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(200)
        )

        transport.set_access_token("my-jwt")
        transport.clear_access_token()
        transport.request("GET", "/test")

        assert "Authorization" not in route.calls[0].request.headers


class TestErrorMapping:
    @respx.mock
    def test_401_raises_auth_error(self, transport):
        respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(
                401,
                json={
                    "exception": {
                        "serviceName": "auth",
                        "serviceCtx": "unauthorized",
                        "exceptionDetailList": [
                            {
                                "exceptionCode": 401,
                                "exceptionDescription": "Invalid token",
                            }
                        ],
                    }
                },
            )
        )
        with pytest.raises(KsefAuthError) as exc_info:
            transport.get("/test", response_model=AuthenticationChallengeResponse)
        assert exc_info.value.status_code == 401

    @respx.mock
    def test_403_raises_auth_error(self, transport):
        respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(403, text="Forbidden")
        )
        with pytest.raises(KsefAuthError) as exc_info:
            transport.get("/test", response_model=AuthenticationChallengeResponse)
        assert exc_info.value.status_code == 403

    @respx.mock
    def test_429_raises_rate_limit_error(self, transport):
        respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(
                429,
                text="Too Many Requests",
                headers={"Retry-After": "30"},
            )
        )
        with pytest.raises(KsefRateLimitError) as exc_info:
            transport.get("/test", response_model=AuthenticationChallengeResponse)
        assert exc_info.value.retry_after == 30

    @respx.mock
    def test_500_raises_api_error(self, transport):
        respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )
        with pytest.raises(KsefApiError) as exc_info:
            transport.get("/test", response_model=AuthenticationChallengeResponse)
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_structured_exception_parsed(self, transport):
        respx.get("https://api-test.ksef.mf.gov.pl/api/v2/test").mock(
            return_value=httpx.Response(
                400,
                json={
                    "exception": {
                        "serviceName": "TestService",
                        "serviceCtx": "validation",
                        "exceptionDetailList": [
                            {
                                "exceptionCode": 1,
                                "exceptionDescription": "field X invalid",
                            },
                            {
                                "exceptionCode": 2,
                                "exceptionDescription": "field Y missing",
                            },
                        ],
                    }
                },
            )
        )
        with pytest.raises(KsefApiError) as exc_info:
            transport.get("/test", response_model=AuthenticationChallengeResponse)
        assert exc_info.value.response is not None
        assert exc_info.value.response.exception is not None
