from __future__ import annotations

import httpx
import json
import pytest
import respx

from ksef_sdk._environments import Environment
from ksef_sdk._http import HttpTransport
from ksef_sdk._sessions import OnlineSession
from ksef_sdk.exceptions import KsefSessionError
from tests.conftest import SAMPLE_INVOICE_XML


BASE = "https://api-test.ksef.mf.gov.pl/api/v2"
REF = "s" * 36


@pytest.fixture()
def transport():
    t = HttpTransport(Environment.TEST)
    t.set_access_token("test-access-token")
    yield t
    t.close()


@pytest.fixture()
def mock_open():
    """Mock the open-session endpoint."""
    return respx.post(f"{BASE}/sessions/online").mock(
        return_value=httpx.Response(
            200,
            json={
                "referenceNumber": REF,
                "validUntil": "2025-01-01T01:00:00+00:00",
            },
        )
    )


class TestOnlineSessionOpen:
    @respx.mock
    def test_open_sends_encryption_info(
        self, transport, sample_certificates, mock_open
    ):
        session = OnlineSession(transport, sample_certificates)
        resp = session.open()

        assert resp.referenceNumber == REF
        assert session.is_open
        assert session.reference_number == REF

        # Verify the request body
        sent = json.loads(mock_open.calls[0].request.content)
        assert "formCode" in sent
        assert "encryption" in sent
        assert "encryptedSymmetricKey" in sent["encryption"]
        assert "initializationVector" in sent["encryption"]

    @respx.mock
    def test_open_twice_raises(self, transport, sample_certificates, mock_open):
        session = OnlineSession(transport, sample_certificates)
        session.open()
        with pytest.raises(KsefSessionError, match="already open"):
            session.open()


class TestOnlineSessionSendInvoice:
    @respx.mock
    def test_send_invoice(self, transport, sample_certificates, mock_open):
        respx.post(f"{BASE}/sessions/online/{REF}/invoices").mock(
            return_value=httpx.Response(
                200,
                json={
                    "referenceNumber": "i" * 36,
                },
            )
        )

        session = OnlineSession(transport, sample_certificates)
        session.open()
        resp = session.send_invoice(SAMPLE_INVOICE_XML)
        assert resp.referenceNumber == "i" * 36

    def test_send_before_open_raises(self, transport, sample_certificates):
        session = OnlineSession(transport, sample_certificates)
        with pytest.raises(KsefSessionError, match="not been opened"):
            session.send_invoice(SAMPLE_INVOICE_XML)


class TestOnlineSessionClose:
    @respx.mock
    def test_close(self, transport, sample_certificates, mock_open):
        respx.post(f"{BASE}/sessions/online/{REF}/close").mock(
            return_value=httpx.Response(200)
        )

        session = OnlineSession(transport, sample_certificates)
        session.open()
        session.close()
        assert not session.is_open

    @respx.mock
    def test_close_idempotent(self, transport, sample_certificates):
        session = OnlineSession(transport, sample_certificates)
        # closing without opening is a no-op
        session.close()
        assert not session.is_open


class TestOnlineSessionContextManager:
    @respx.mock
    def test_context_manager_opens_and_closes(
        self, transport, sample_certificates, mock_open
    ):
        respx.post(f"{BASE}/sessions/online/{REF}/close").mock(
            return_value=httpx.Response(200)
        )

        with OnlineSession(transport, sample_certificates) as session:
            assert session.is_open
            assert session.reference_number == REF

        assert not session.is_open

    @respx.mock
    def test_context_manager_closes_on_exception(
        self, transport, sample_certificates, mock_open
    ):
        respx.post(f"{BASE}/sessions/online/{REF}/close").mock(
            return_value=httpx.Response(200)
        )

        with pytest.raises(RuntimeError):
            with OnlineSession(transport, sample_certificates) as session:
                raise RuntimeError("boom")

        assert not session.is_open


class TestOnlineSessionStatus:
    @respx.mock
    def test_status(self, transport, sample_certificates, mock_open):
        respx.get(f"{BASE}/sessions/{REF}").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": {"code": 100, "description": "Open"},
                    "dateCreated": "2025-01-01T00:00:00+00:00",
                    "dateUpdated": "2025-01-01T00:00:00+00:00",
                    "validUntil": "2025-01-01T01:00:00+00:00",
                },
            )
        )

        session = OnlineSession(transport, sample_certificates)
        session.open()
        status = session.status()
        assert status.status.code == 100
