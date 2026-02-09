"""Shared factories and fakes for unit tests."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any

import httpx
import pytest

from ksef_sdk.domain.models.encryption import CertUsage, PublicKeyCertificate
from ksef_sdk.domain.models.session import FormSchema, SessionState


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------

_REF = "20250625-SO-2C3E6C8000-B675CF5D68-07"
_INVOICE_REF = "20250625-EE-319D7EE000-B67F415CDC-2C"
_TOKEN = "fake-access-token"


def make_session_state(
    *,
    reference_number: str = _REF,
    aes_key: bytes | None = None,
    iv: bytes | None = None,
    access_token: str = _TOKEN,
    valid_until: datetime | None = None,
    form_code: FormSchema = FormSchema.FA3,
) -> SessionState:
    return SessionState(
        reference_number=reference_number,
        aes_key=aes_key or os.urandom(32),
        iv=iv or os.urandom(16),
        access_token=access_token,
        valid_until=valid_until or datetime.now(tz=timezone.utc) + timedelta(hours=1),
        form_code=form_code,
    )


def make_certificate(
    *,
    certificate: str = "AAAA",
    usage: list[CertUsage] | None = None,
    valid_from: datetime | None = None,
    valid_to: datetime | None = None,
) -> PublicKeyCertificate:
    now = datetime.now(tz=timezone.utc)
    return PublicKeyCertificate(
        certificate=certificate,
        valid_from=valid_from or now - timedelta(days=30),
        valid_to=valid_to or now + timedelta(days=30),
        usage=usage or [CertUsage.SYMMETRIC_KEY_ENCRYPTION],
    )


# ---------------------------------------------------------------------------
# Fake HttpTransport
# ---------------------------------------------------------------------------


@dataclass
class RecordedCall:
    method: str
    path: str
    headers: dict[str, str] | None
    json: dict[str, Any] | None
    content: bytes | None = None


@dataclass
class FakeTransport:
    """Duck-typed replacement for HttpTransport.

    Queue responses via ``enqueue`` before calling ``get``/``post``/``delete``.
    All calls are recorded in ``calls`` for assertions.
    """

    calls: list[RecordedCall] = field(default_factory=list)
    _responses: list[httpx.Response] = field(default_factory=list)

    def enqueue(
        self,
        json_body: Any = None,
        *,
        status_code: int = 200,
        content: bytes | None = None,
    ) -> None:
        if content is not None:
            resp = httpx.Response(status_code=status_code, content=content)
        else:
            resp = httpx.Response(status_code=status_code, json=json_body)
        self._responses.append(resp)

    def _next_response(self) -> httpx.Response:
        if not self._responses:
            raise RuntimeError("FakeTransport: no more queued responses")
        return self._responses.pop(0)

    def get(
        self, path: str, *, headers: dict[str, str] | None = None
    ) -> httpx.Response:
        self.calls.append(RecordedCall("GET", path, headers, None))
        return self._next_response()

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        self.calls.append(RecordedCall("POST", path, headers, json))
        return self._next_response()

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response:
        self.calls.append(RecordedCall(method, path, headers, json, content))
        return self._next_response()

    def delete(
        self, path: str, *, headers: dict[str, str] | None = None
    ) -> httpx.Response:
        self.calls.append(RecordedCall("DELETE", path, headers, None))
        return self._next_response()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_transport() -> FakeTransport:
    return FakeTransport()


@pytest.fixture
def session_state() -> SessionState:
    return make_session_state()
