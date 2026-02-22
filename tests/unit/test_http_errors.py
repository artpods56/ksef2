"""Tests for HttpTransport error body parsing."""

from __future__ import annotations

import pytest
import respx
import httpx

from ksef2.config import Environment
from ksef2.core import exceptions
from ksef2.core.http import HttpTransport
from ksef2.core.middleware import KSeFProtocol
from ksef2.infra.schema.api.spec import (
    ExceptionResponse,
    TooManyRequestsResponse,
)


BASE = Environment.TEST.base_url
VALID_REF = "a1b2c3d4-e5f6-4789-ab12-cd34ef567890"


@pytest.fixture
def transport() -> KSeFProtocol:
    return KSeFProtocol(HttpTransport(httpx.Client(base_url=BASE)))


class Test429Errors:
    @respx.mock
    def test_429_parses_body(self, transport: KSeFProtocol) -> None:
        error_body = '{"status": {"code": 429, "description": "Too Many Requests", "details": ["Try again later"]}}'
        respx.get(f"{BASE}/limited").mock(
            return_value=httpx.Response(
                429,
                headers={"Retry-After": "30", "Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFRateLimitError) as exc_info:
            transport.get("/limited")

        assert exc_info.value.retry_after == 30
        assert exc_info.value.response is not None
        assert isinstance(exc_info.value.response, TooManyRequestsResponse)
        assert exc_info.value.response.status.code == 429
        assert exc_info.value.response.status.description == "Too Many Requests"

    @respx.mock
    def test_429_with_malformed_body(self, transport: KSeFProtocol) -> None:
        respx.get(f"{BASE}/limited").mock(
            return_value=httpx.Response(
                429,
                headers={"Retry-After": "45", "Content-Type": "application/json"},
                content=b"not json",
            )
        )

        with pytest.raises(exceptions.KSeFRateLimitError) as exc_info:
            transport.get("/limited")

        assert exc_info.value.retry_after == 45
        assert exc_info.value.response is None

    @respx.mock
    def test_429_without_retry_after(self, transport: KSeFProtocol) -> None:
        error_body = '{"status": {"code": 429, "description": "Too Many Requests", "details": []}}'
        respx.get(f"{BASE}/limited").mock(
            return_value=httpx.Response(
                429,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFRateLimitError) as exc_info:
            transport.get("/limited")

        assert exc_info.value.retry_after is None
        assert exc_info.value.response is not None


class Test400Errors:
    @respx.mock
    def test_400_parses_exception_response(self, transport: KSeFProtocol) -> None:
        error_body = f'''{{
            "exception": {{
                "exceptionDetailList": [{{"exceptionCode": 21405, "exceptionDescription": "Validation error", "details": ["Invalid NIP"]}}],
                "referenceNumber": "{VALID_REF}",
                "serviceCode": "srvABC",
                "serviceCtx": "ctx123",
                "serviceName": "TestService",
                "timestamp": "2025-10-11T12:23:56.0154302+00:00"
            }}
        }}'''
        respx.get(f"{BASE}/bad-request").mock(
            return_value=httpx.Response(
                400,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFApiError) as exc_info:
            transport.get("/bad-request")

        assert exc_info.value.status_code == 400
        assert exc_info.value.response is not None
        assert isinstance(exc_info.value.response, ExceptionResponse)
        assert exc_info.value.response.exception is not None
        assert exc_info.value.response.exception.referenceNumber == VALID_REF
        assert exc_info.value.response.exception.exceptionDetailList is not None
        assert (
            exc_info.value.response.exception.exceptionDetailList[0].exceptionCode
            == 21405
        )

    @respx.mock
    def test_400_with_malformed_body(self, transport: KSeFProtocol) -> None:
        respx.get(f"{BASE}/bad-request").mock(
            return_value=httpx.Response(
                400, headers={"Content-Type": "application/json"}, content=b"not json"
            )
        )

        with pytest.raises(exceptions.KSeFApiError) as exc_info:
            transport.get("/bad-request")

        assert exc_info.value.status_code == 400
        assert exc_info.value.response is None

    @respx.mock
    def test_400_with_extra_fields(self, transport: KSeFProtocol) -> None:
        error_body = f'''{{
            "exception": {{
                "exceptionDetailList": [],
                "referenceNumber": "{VALID_REF}",
                "unknownField": "should be ignored"
            }}
        }}'''
        respx.get(f"{BASE}/bad-request").mock(
            return_value=httpx.Response(
                400,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFApiError) as exc_info:
            transport.get("/bad-request")

        assert exc_info.value.status_code == 400
        assert exc_info.value.response is not None
        assert isinstance(exc_info.value.response, ExceptionResponse)
        assert exc_info.value.response.exception.referenceNumber == VALID_REF


class TestAuthErrors:
    @respx.mock
    def test_401_raises_auth_error(self, transport: KSeFProtocol) -> None:
        error_body = f'{{"exception": {{"referenceNumber": "{VALID_REF}"}}}}'
        respx.get(f"{BASE}/unauthorized").mock(
            return_value=httpx.Response(
                401,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFAuthError) as exc_info:
            transport.get("/unauthorized")

        assert exc_info.value.status_code == 401
        assert exc_info.value.response is not None
        assert isinstance(exc_info.value.response, ExceptionResponse)

    @respx.mock
    def test_403_raises_auth_error(self, transport: KSeFProtocol) -> None:
        error_body = f'{{"exception": {{"referenceNumber": "{VALID_REF}"}}}}'
        respx.get(f"{BASE}/forbidden").mock(
            return_value=httpx.Response(
                403,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFAuthError) as exc_info:
            transport.get("/forbidden")

        assert exc_info.value.status_code == 403
        assert exc_info.value.response is not None

    @respx.mock
    def test_401_with_malformed_body(self, transport: KSeFProtocol) -> None:
        respx.get(f"{BASE}/unauthorized").mock(
            return_value=httpx.Response(
                401, headers={"Content-Type": "application/json"}, content=b"not json"
            )
        )

        with pytest.raises(exceptions.KSeFAuthError) as exc_info:
            transport.get("/unauthorized")

        assert exc_info.value.status_code == 401
        assert exc_info.value.response is None


class TestOtherErrors:
    @respx.mock
    def test_404_raises_api_error(self, transport: KSeFProtocol) -> None:
        error_body = f'{{"exception": {{"referenceNumber": "{VALID_REF}"}}}}'
        respx.get(f"{BASE}/missing").mock(
            return_value=httpx.Response(
                404,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFApiError) as exc_info:
            transport.get("/missing")

        assert exc_info.value.status_code == 404
        assert exc_info.value.response is not None

    @respx.mock
    def test_500_raises_api_error(self, transport: KSeFProtocol) -> None:
        respx.get(f"{BASE}/error").mock(
            return_value=httpx.Response(
                500,
                headers={"Content-Type": "application/json"},
                content=b"Internal Server Error",
            )
        )

        with pytest.raises(exceptions.KSeFApiError) as exc_info:
            transport.get("/error")

        assert exc_info.value.status_code == 500
        assert exc_info.value.response is None

    @respx.mock
    def test_500_with_exception_response(self, transport: KSeFProtocol) -> None:
        error_body = f'{{"exception": {{"referenceNumber": "{VALID_REF}"}}}}'
        respx.get(f"{BASE}/error").mock(
            return_value=httpx.Response(
                500,
                headers={"Content-Type": "application/json"},
                content=error_body.encode(),
            )
        )

        with pytest.raises(exceptions.KSeFApiError) as exc_info:
            transport.get("/error")

        assert exc_info.value.status_code == 500
        assert exc_info.value.response is not None
