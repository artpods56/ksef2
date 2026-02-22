"""Tests for invoice status and UPO endpoint classes — URL, HTTP method, headers."""

from __future__ import annotations

from tests.unit.conftest import FakeTransport, _REF, _TOKEN

_INVOICE_REF = "20250625-EE-319D7EE000-B67F415CDC-2C"
_KSEF_NUMBER = "9999999999-20250101-AABBCC-DDEEFF-01"


# ---------------------------------------------------------------------------
# ListSessionsEndpoint
# ---------------------------------------------------------------------------


class TestListSessionsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.session import ListSessionsEndpoint

        ep = ListSessionsEndpoint(FakeTransport())
        assert ep.url == "/sessions"

    def test_send_gets_with_session_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.session import ListSessionsEndpoint

        fake_transport.enqueue({"continuationToken": None, "sessions": []})
        ep = ListSessionsEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, sessionType="Online", statuses=[])

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert "sessionType=Online" in call.path
        assert call.headers is not None
        assert call.headers["Authorization"] == f"Bearer {_TOKEN}"

    def test_send_includes_query_params(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.session import ListSessionsEndpoint

        fake_transport.enqueue({"continuationToken": None, "sessions": []})
        ep = ListSessionsEndpoint(fake_transport)

        ep.send(
            access_token=_TOKEN,
            sessionType="Batch",
            statuses=["InProgress", "Succeeded"],
        )

        call = fake_transport.calls[0]
        assert "sessionType=Batch" in call.path
        assert "InProgress" in call.path
        assert "Succeeded" in call.path

    def test_send_includes_continuation_token_header(
        self, fake_transport: FakeTransport
    ) -> None:
        from ksef2.endpoints.session import ListSessionsEndpoint

        fake_transport.enqueue({"continuationToken": None, "sessions": []})
        ep = ListSessionsEndpoint(fake_transport)

        ep.send(
            access_token=_TOKEN,
            sessionType="Online",
            statuses=[],
            continuation_token="abc123",
        )

        call = fake_transport.calls[0]
        assert call.headers is not None
        assert call.headers["x-continuation-token"] == "abc123"


# ---------------------------------------------------------------------------
# GetSessionStatusEndpoint
# ---------------------------------------------------------------------------


class TestGetSessionStatusEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef2.endpoints.invoices import GetSessionStatusEndpoint

        ep = GetSessionStatusEndpoint(FakeTransport())
        assert _REF in ep.get_url(reference_number=_REF)

    def test_send_gets_with_session_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import GetSessionStatusEndpoint

        fake_transport.enqueue(
            {
                "status": {"code": 200, "description": "OK"},
                "dateCreated": "2025-09-18T15:00:30+00:00",
                "dateUpdated": "2025-09-18T15:01:20+00:00",
            }
        )
        ep = GetSessionStatusEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _REF in call.path
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


# ---------------------------------------------------------------------------
# ListSessionInvoicesEndpoint
# ---------------------------------------------------------------------------


class TestListSessionInvoicesEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef2.endpoints.invoices import ListSessionInvoicesEndpoint

        ep = ListSessionInvoicesEndpoint(FakeTransport())
        assert _REF in ep.get_url(reference_number=_REF)

    def test_send_gets_with_session_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import ListSessionInvoicesEndpoint

        fake_transport.enqueue({"continuationToken": None, "invoices": []})
        ep = ListSessionInvoicesEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF, page_size=20)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _REF in call.path
        assert "pageSize=20" in call.path
        assert call.headers is not None
        assert call.headers["Authorization"] == f"Bearer {_TOKEN}"

    def test_send_includes_continuation_token_header(
        self, fake_transport: FakeTransport
    ) -> None:
        from ksef2.endpoints.invoices import ListSessionInvoicesEndpoint

        fake_transport.enqueue({"continuationToken": None, "invoices": []})
        ep = ListSessionInvoicesEndpoint(fake_transport)

        ep.send(
            access_token=_TOKEN,
            reference_number=_REF,
            continuation_token="tok123",
            page_size=20,
        )

        call = fake_transport.calls[0]
        assert call.headers is not None
        assert call.headers["x-continuation-token"] == "tok123"


# ---------------------------------------------------------------------------
# GetSessionInvoiceStatusEndpoint
# ---------------------------------------------------------------------------


class TestGetSessionInvoiceStatusEndpoint:
    def test_url_contains_both_references(self) -> None:
        from ksef2.endpoints.invoices import GetSessionInvoiceStatusEndpoint

        ep = GetSessionInvoiceStatusEndpoint(FakeTransport())
        url = ep.get_url(
            reference_number=_REF,
            invoice_reference_number=_INVOICE_REF,
        )
        assert _REF in url
        assert _INVOICE_REF in url

    def test_send_gets_with_session_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import GetSessionInvoiceStatusEndpoint

        fake_transport.enqueue(
            {
                "ordinalNumber": 1,
                "referenceNumber": _INVOICE_REF,
                "invoiceHash": "WO86CC+1Lef11wEosItld/NPwxGN8tobOMLqk9PQjgs=",
                "invoicingDate": "2025-09-18T15:00:30+00:00",
                "status": {"code": 200, "description": "Sukces"},
            }
        )
        ep = GetSessionInvoiceStatusEndpoint(fake_transport)

        ep.send(
            access_token=_TOKEN,
            reference_number=_REF,
            invoice_reference_number=_INVOICE_REF,
        )

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _REF in call.path
        assert _INVOICE_REF in call.path
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


# ---------------------------------------------------------------------------
# ListFailedSessionInvoicesEndpoint
# ---------------------------------------------------------------------------


class TestListFailedSessionInvoicesEndpoint:
    def test_url_contains_failed(self) -> None:
        from ksef2.endpoints.invoices import ListFailedSessionInvoicesEndpoint

        ep = ListFailedSessionInvoicesEndpoint(FakeTransport())
        url = ep.get_url(reference_number=_REF)
        assert "/invoices/failed" in url
        assert _REF in url

    def test_send_gets_with_session_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import ListFailedSessionInvoicesEndpoint

        fake_transport.enqueue({"continuationToken": None, "invoices": []})
        ep = ListFailedSessionInvoicesEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF, page_size=10)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert "/invoices/failed" in call.path
        assert call.headers is not None
        assert call.headers["Authorization"] == f"Bearer {_TOKEN}"


# ---------------------------------------------------------------------------
# GetInvoiceUpoByKsefNumberEndpoint
# ---------------------------------------------------------------------------


class TestGetInvoiceUpoByKsefNumberEndpoint:
    def test_url_contains_ksef_number(self) -> None:
        from ksef2.endpoints.invoices import GetInvoiceUpoByKsefNumberEndpoint

        ep = GetInvoiceUpoByKsefNumberEndpoint(FakeTransport())
        url = ep.get_url(reference_number=_REF, ksef_number=_KSEF_NUMBER)
        assert _REF in url
        assert _KSEF_NUMBER in url
        assert "/upo" in url

    def test_send_returns_bytes(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import GetInvoiceUpoByKsefNumberEndpoint

        upo_xml = b"<UPO>content</UPO>"
        fake_transport.enqueue(content=upo_xml)
        ep = GetInvoiceUpoByKsefNumberEndpoint(fake_transport)

        result = ep.send(
            access_token=_TOKEN,
            reference_number=_REF,
            ksef_number=_KSEF_NUMBER,
        )

        assert result == upo_xml
        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


# ---------------------------------------------------------------------------
# GetInvoiceUpoByReferenceEndpoint
# ---------------------------------------------------------------------------


class TestGetInvoiceUpoByReferenceEndpoint:
    def test_url_contains_references(self) -> None:
        from ksef2.endpoints.invoices import GetInvoiceUpoByReferenceEndpoint

        ep = GetInvoiceUpoByReferenceEndpoint(FakeTransport())
        url = ep.get_url(
            reference_number=_REF,
            invoice_reference_number=_INVOICE_REF,
        )
        assert _REF in url
        assert _INVOICE_REF in url
        assert "/upo" in url

    def test_send_returns_bytes(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import GetInvoiceUpoByReferenceEndpoint

        upo_xml = b"<UPO>content</UPO>"
        fake_transport.enqueue(content=upo_xml)
        ep = GetInvoiceUpoByReferenceEndpoint(fake_transport)

        result = ep.send(
            access_token=_TOKEN,
            reference_number=_REF,
            invoice_reference_number=_INVOICE_REF,
        )

        assert result == upo_xml
        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}
