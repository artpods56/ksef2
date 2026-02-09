"""Tests for HttpTransport — uses respx to mock httpx."""

from __future__ import annotations

import pytest
import respx
import httpx

from ksef2.config import Environment
from ksef2.core import exceptions
from ksef2.core.http import HttpTransport


BASE = Environment.TEST.base_url


@pytest.fixture
def transport() -> HttpTransport:
    return HttpTransport(Environment.TEST)


class TestGet:
    @respx.mock
    def test_returns_response(self, transport: HttpTransport) -> None:
        respx.get(f"{BASE}/test-path").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )

        resp = transport.get("/test-path")

        assert resp.status_code == 200
        assert resp.json() == {"ok": True}

    @respx.mock
    def test_passes_headers(self, transport: HttpTransport) -> None:
        route = respx.get(f"{BASE}/h").mock(return_value=httpx.Response(200))

        transport.get("/h", headers={"X-Custom": "val"})

        assert route.calls[0].request.headers["X-Custom"] == "val"


class TestPost:
    @respx.mock
    def test_sends_json_body(self, transport: HttpTransport) -> None:
        route = respx.post(f"{BASE}/data").mock(
            return_value=httpx.Response(201, json={})
        )

        transport.post("/data", json={"key": "value"})

        assert route.calls[0].request.content != b""

    @respx.mock
    def test_passes_headers(self, transport: HttpTransport) -> None:
        route = respx.post(f"{BASE}/data").mock(return_value=httpx.Response(200))

        transport.post("/data", headers={"SessionToken": "tok"})

        assert route.calls[0].request.headers["SessionToken"] == "tok"


class TestDelete:
    @respx.mock
    def test_sends_delete(self, transport: HttpTransport) -> None:
        route = respx.delete(f"{BASE}/resource/123").mock(
            return_value=httpx.Response(200)
        )

        resp = transport.delete("/resource/123")

        assert resp.status_code == 200
        assert route.called

    @respx.mock
    def test_passes_headers(self, transport: HttpTransport) -> None:
        route = respx.delete(f"{BASE}/r").mock(return_value=httpx.Response(200))

        transport.delete("/r", headers={"SessionToken": "abc"})

        assert route.calls[0].request.headers["SessionToken"] == "abc"


class TestErrorHandling:
    @respx.mock
    def test_429_raises_rate_limit_error(self, transport: HttpTransport) -> None:
        respx.get(f"{BASE}/limited").mock(
            return_value=httpx.Response(429, headers={"Retry-After": "30"}, json={})
        )

        with pytest.raises(exceptions.KSeFRateLimitError) as exc_info:
            transport.get("/limited")

        assert exc_info.value.retry_after == 30

    @respx.mock
    def test_429_without_retry_after(self, transport: HttpTransport) -> None:
        respx.get(f"{BASE}/limited").mock(return_value=httpx.Response(429, json={}))

        with pytest.raises(exceptions.KSeFRateLimitError) as exc_info:
            transport.get("/limited")

        assert exc_info.value.retry_after is None

    @respx.mock
    def test_200_does_not_raise(self, transport: HttpTransport) -> None:
        respx.get(f"{BASE}/ok").mock(return_value=httpx.Response(200, json={}))

        resp = transport.get("/ok")

        assert resp.status_code == 200
