"""Tests for TokenService — generate, status, revoke, polling."""

from __future__ import annotations

import pytest

from ksef_sdk.core import exceptions
from ksef_sdk.domain.models.tokens import (
    GenerateTokenResponse,
    TokenPermission,
    TokenStatus,
    TokenStatusResponse,
)
from ksef_sdk.services.tokens import TokenService

from tests.unit.conftest import FakeTransport, _REF


_TOKEN = "fake-access-token"
_KSEF_TOKEN = "generated-ksef-token-value"


def _token_status_response(
    *,
    ref: str = _REF,
    status: str = "Active",
) -> dict:
    return {
        "referenceNumber": ref,
        "authorIdentifier": {"type": "Nip", "value": "1234567890"},
        "contextIdentifier": {"type": "Nip", "value": "1234567890"},
        "description": "test token",
        "requestedPermissions": ["InvoiceRead"],
        "dateCreated": "2025-07-11T12:00:00+00:00",
        "status": status,
    }


def _build_service(transport: FakeTransport) -> TokenService:
    return TokenService(transport)  # type: ignore[arg-type]


class TestGenerate:
    def test_sends_correct_request(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _REF, "token": _KSEF_TOKEN})
        fake_transport.enqueue(_token_status_response(status="Active"))
        svc = _build_service(fake_transport)

        result = svc.generate(
            access_token=_TOKEN,
            permissions=[TokenPermission.INVOICE_READ, TokenPermission.INVOICE_WRITE],
            description="Test token",
            poll_interval=0,
        )

        # POST /tokens
        post_call = fake_transport.calls[0]
        assert post_call.method == "POST"
        assert post_call.path == "/tokens"
        assert post_call.json == {
            "permissions": ["InvoiceRead", "InvoiceWrite"],
            "description": "Test token",
        }
        assert post_call.headers == {"SessionToken": _TOKEN}

    def test_returns_generate_response(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _REF, "token": _KSEF_TOKEN})
        fake_transport.enqueue(_token_status_response(status="Active"))
        svc = _build_service(fake_transport)

        result = svc.generate(
            access_token=_TOKEN,
            permissions=[TokenPermission.INVOICE_READ],
            description="Test token",
            poll_interval=0,
        )

        assert isinstance(result, GenerateTokenResponse)
        assert result.reference_number == _REF
        assert result.token == _KSEF_TOKEN

    def test_polls_until_active(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _REF, "token": _KSEF_TOKEN})
        fake_transport.enqueue(_token_status_response(status="Pending"))
        fake_transport.enqueue(_token_status_response(status="Pending"))
        fake_transport.enqueue(_token_status_response(status="Active"))
        svc = _build_service(fake_transport)

        result = svc.generate(
            access_token=_TOKEN,
            permissions=[TokenPermission.INVOICE_READ],
            description="Test token",
            poll_interval=0,
        )

        assert result.token == _KSEF_TOKEN
        # 1 POST + 3 GETs (Pending, Pending, Active)
        assert len(fake_transport.calls) == 4

    def test_raises_on_failed_status(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _REF, "token": _KSEF_TOKEN})
        fake_transport.enqueue(_token_status_response(status="Failed"))
        svc = _build_service(fake_transport)

        with pytest.raises(exceptions.KSeFApiError, match="Failed"):
            svc.generate(
                access_token=_TOKEN,
                permissions=[TokenPermission.INVOICE_READ],
                description="Test token",
                poll_interval=0,
            )

    def test_raises_on_revoked_status(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _REF, "token": _KSEF_TOKEN})
        fake_transport.enqueue(_token_status_response(status="Revoked"))
        svc = _build_service(fake_transport)

        with pytest.raises(exceptions.KSeFApiError, match="Revoked"):
            svc.generate(
                access_token=_TOKEN,
                permissions=[TokenPermission.INVOICE_READ],
                description="Test token",
                poll_interval=0,
            )

    def test_raises_on_timeout(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _REF, "token": _KSEF_TOKEN})
        fake_transport.enqueue(_token_status_response(status="Pending"))
        fake_transport.enqueue(_token_status_response(status="Pending"))
        svc = _build_service(fake_transport)

        with pytest.raises(exceptions.KSeFApiError, match="timed out"):
            svc.generate(
                access_token=_TOKEN,
                permissions=[TokenPermission.INVOICE_READ],
                description="Test token",
                poll_interval=0,
                max_poll_attempts=2,
            )


class TestStatus:
    def test_returns_status_response(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(_token_status_response(status="Active"))
        svc = _build_service(fake_transport)

        result = svc.status(access_token=_TOKEN, reference_number=_REF)

        assert isinstance(result, TokenStatusResponse)
        assert result.reference_number == _REF
        assert result.status == TokenStatus.ACTIVE

    def test_sends_get_request(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(_token_status_response())
        svc = _build_service(fake_transport)

        svc.status(access_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _REF in call.path
        assert call.headers == {"SessionToken": _TOKEN}

    def test_maps_all_statuses(self, fake_transport: FakeTransport) -> None:
        for status in TokenStatus:
            fake_transport.enqueue(_token_status_response(status=status.value))

        svc = _build_service(fake_transport)

        for status in TokenStatus:
            result = svc.status(access_token=_TOKEN, reference_number=_REF)
            assert result.status == status


class TestRevoke:
    def test_sends_delete_request(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=200)
        svc = _build_service(fake_transport)

        svc.revoke(access_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "DELETE"
        assert _REF in call.path
        assert call.headers == {"SessionToken": _TOKEN}
