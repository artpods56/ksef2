"""Tests for invoice query/export endpoint classes — URL, HTTP method, headers."""

from __future__ import annotations

from ksef2.endpoints.invoices import SortOrder
from tests.unit.conftest import FakeTransport, _TOKEN

_EXPORT_REF = "12345678-1234-1234-1234-123456789012"


# ---------------------------------------------------------------------------
# QueryInvoicesMetadataEndpoint
# ---------------------------------------------------------------------------


class TestQueryInvoicesMetadataEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.invoices import QueryInvoicesMetadataEndpoint

        ep = QueryInvoicesMetadataEndpoint(FakeTransport())
        assert ep.url == "/invoices/query/metadata"

    def test_send_posts_with_bearer_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import QueryInvoicesMetadataEndpoint

        fake_transport.enqueue(
            {
                "hasMore": False,
                "isTruncated": False,
                "permanentStorageHwmDate": None,
                "invoices": [],
            }
        )
        ep = QueryInvoicesMetadataEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, body={"subjectType": "Subject1"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}

    def test_send_includes_query_params(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import QueryInvoicesMetadataEndpoint

        fake_transport.enqueue(
            {
                "hasMore": False,
                "isTruncated": False,
                "permanentStorageHwmDate": None,
                "invoices": [],
            }
        )
        ep = QueryInvoicesMetadataEndpoint(fake_transport)

        sort_order = SortOrder.ASC

        ep.send(
            access_token=_TOKEN,
            body={},
            sortOrder=sort_order,
            pageOffset=0,
            pageSize=10,
        )

        call = fake_transport.calls[0]
        assert "sortOrder=Asc" in call.path
        assert "pageOffset=0" in call.path
        assert "pageSize=10" in call.path

    def test_send_forwards_body(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import QueryInvoicesMetadataEndpoint

        fake_transport.enqueue(
            {
                "hasMore": False,
                "isTruncated": False,
                "permanentStorageHwmDate": None,
                "invoices": [],
            }
        )
        ep = QueryInvoicesMetadataEndpoint(fake_transport)

        body = {"subjectType": "Subject1", "dateRange": {"dateType": "Issue"}}
        ep.send(access_token=_TOKEN, body=body)

        call = fake_transport.calls[0]
        assert call.json == body


# ---------------------------------------------------------------------------
# ExportInvoicesEndpoint
# ---------------------------------------------------------------------------


class TestExportInvoicesEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.invoices import ExportInvoicesEndpoint

        ep = ExportInvoicesEndpoint(FakeTransport())
        assert ep.url == "/invoices/exports"

    def test_send_posts_with_bearer_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import ExportInvoicesEndpoint

        fake_transport.enqueue({"referenceNumber": _EXPORT_REF})
        ep = ExportInvoicesEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, body={"filters": {}, "encryption": {}})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/invoices/exports"
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}

    def test_send_forwards_body(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import ExportInvoicesEndpoint

        fake_transport.enqueue({"referenceNumber": _EXPORT_REF})
        ep = ExportInvoicesEndpoint(fake_transport)

        body = {"filters": {"subjectType": "Subject1"}, "encryption": {"key": "abc"}}
        ep.send(access_token=_TOKEN, body=body)

        call = fake_transport.calls[0]
        assert call.json == body


# ---------------------------------------------------------------------------
# GetExportStatusEndpoint
# ---------------------------------------------------------------------------


class TestGetExportStatusEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef2.endpoints.invoices import GetExportStatusEndpoint

        ep = GetExportStatusEndpoint(FakeTransport())
        url = ep.get_url(reference_number=_EXPORT_REF)
        assert _EXPORT_REF in url

    def test_send_gets_with_bearer_header(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.invoices import GetExportStatusEndpoint

        fake_transport.enqueue(
            {
                "status": {"code": 200, "description": "OK"},
                "completedDate": None,
                "packageExpirationDate": None,
                "package": None,
            }
        )
        ep = GetExportStatusEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_EXPORT_REF)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _EXPORT_REF in call.path
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}
