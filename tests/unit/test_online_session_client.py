"""Tests for OnlineSessionClient — send_invoice, terminate, context manager."""

from __future__ import annotations

import pytest

from ksef2.clients.session import OnlineSessionClient
from ksef2.domain.models.invoices import SendInvoiceResponse

from tests.unit.conftest import (
    FakeTransport,
    make_session_state,
    _REF,
    _TOKEN,
    _INVOICE_REF,
)


SAMPLE_XML = b"<Invoice><Total>100.00</Total></Invoice>"


def _build_client(
    transport: FakeTransport,
    **state_overrides,
) -> OnlineSessionClient:
    state = make_session_state(**state_overrides)
    return OnlineSessionClient(transport=transport, state=state)


# ---------------------------------------------------------------------------
# send_invoice
# ---------------------------------------------------------------------------


class TestSendInvoice:
    def test_returns_send_invoice_response(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(
            {"referenceNumber": _INVOICE_REF},
            status_code=202,
        )
        client = _build_client(fake_transport)

        result = client.send_invoice(SAMPLE_XML)

        assert isinstance(result, SendInvoiceResponse)
        assert result.reference_number == _INVOICE_REF

    def test_posts_to_correct_url(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _INVOICE_REF})
        client = _build_client(fake_transport)

        client.send_invoice(SAMPLE_XML)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert _REF in call.path
        assert "/invoices" in call.path

    def test_sends_session_token_header(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue({"referenceNumber": _INVOICE_REF})
        client = _build_client(fake_transport)

        client.send_invoice(SAMPLE_XML)

        call = fake_transport.calls[0]
        assert call.headers == {"SessionToken": _TOKEN}

    def test_request_body_contains_required_fields(
        self, fake_transport: FakeTransport
    ) -> None:
        fake_transport.enqueue({"referenceNumber": _INVOICE_REF})
        client = _build_client(fake_transport)

        client.send_invoice(SAMPLE_XML)

        body = fake_transport.calls[0].json
        assert body is not None
        assert "invoiceHash" in body
        assert "invoiceSize" in body
        assert "encryptedInvoiceHash" in body
        assert "encryptedInvoiceSize" in body
        assert "encryptedInvoiceContent" in body

    def test_invoice_size_matches_xml_length(
        self, fake_transport: FakeTransport
    ) -> None:
        fake_transport.enqueue({"referenceNumber": _INVOICE_REF})
        client = _build_client(fake_transport)

        client.send_invoice(SAMPLE_XML)

        body = fake_transport.calls[0].json
        assert body["invoiceSize"] == len(SAMPLE_XML)

    def test_encrypted_size_differs_from_plain(
        self, fake_transport: FakeTransport
    ) -> None:
        fake_transport.enqueue({"referenceNumber": _INVOICE_REF})
        client = _build_client(fake_transport)

        client.send_invoice(SAMPLE_XML)

        body = fake_transport.calls[0].json
        assert body["encryptedInvoiceSize"] >= body["invoiceSize"]


# ---------------------------------------------------------------------------
# download_invoice
# ---------------------------------------------------------------------------


class TestDownloadInvoice:
    def test_returns_raw_bytes(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(content=SAMPLE_XML)
        client = _build_client(fake_transport)

        result = client.download_invoice("1234567890-INV-001")

        assert isinstance(result, bytes)
        assert result == SAMPLE_XML

    def test_sends_get_to_correct_url(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(content=SAMPLE_XML)
        client = _build_client(fake_transport)

        client.download_invoice("1234567890-INV-001")

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert "1234567890-INV-001" in call.path

    def test_sends_session_token_header(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(content=SAMPLE_XML)
        client = _build_client(fake_transport)

        client.download_invoice("1234567890-INV-001")

        call = fake_transport.calls[0]
        assert call.headers == {"SessionToken": _TOKEN}


# ---------------------------------------------------------------------------
# terminate
# ---------------------------------------------------------------------------


class TestTerminate:
    def test_sends_delete_request(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=200)
        client = _build_client(fake_transport)

        client.terminate()

        call = fake_transport.calls[0]
        assert call.method == "DELETE"

    def test_delete_url_contains_reference_number(
        self, fake_transport: FakeTransport
    ) -> None:
        fake_transport.enqueue(status_code=200)
        client = _build_client(fake_transport)

        client.terminate()

        call = fake_transport.calls[0]
        assert _REF in call.path

    def test_sends_session_token_header(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=200)
        client = _build_client(fake_transport)

        client.terminate()

        call = fake_transport.calls[0]
        assert call.headers == {"SessionToken": _TOKEN}


# ---------------------------------------------------------------------------
# Context Manager
# ---------------------------------------------------------------------------


class TestContextManager:
    def test_enter_returns_self(self, fake_transport: FakeTransport) -> None:
        client = _build_client(fake_transport)

        assert client.__enter__() is client

    def test_exit_calls_terminate(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=200)
        client = _build_client(fake_transport)

        with client:
            pass

        assert len(fake_transport.calls) == 1
        assert fake_transport.calls[0].method == "DELETE"

    def test_exit_calls_terminate_on_exception(
        self, fake_transport: FakeTransport
    ) -> None:
        fake_transport.enqueue(status_code=200)
        client = _build_client(fake_transport)

        with pytest.raises(ValueError, match="boom"):
            with client:
                raise ValueError("boom")

        assert len(fake_transport.calls) == 1
        assert fake_transport.calls[0].method == "DELETE"

    def test_with_block_allows_sending_then_terminates(
        self, fake_transport: FakeTransport
    ) -> None:
        fake_transport.enqueue({"referenceNumber": _INVOICE_REF})  # send_invoice
        fake_transport.enqueue(status_code=200)  # terminate
        client = _build_client(fake_transport)

        with client as session:
            session.send_invoice(SAMPLE_XML)

        assert len(fake_transport.calls) == 2
        assert fake_transport.calls[0].method == "POST"
        assert fake_transport.calls[1].method == "DELETE"
