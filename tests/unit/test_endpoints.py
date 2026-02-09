"""Tests for endpoint classes — URL building, HTTP method, headers."""

from __future__ import annotations

from tests.unit.conftest import FakeTransport, _REF, _TOKEN


class TestOpenSessionEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.session import OpenSessionEndpoint

        ep = OpenSessionEndpoint(FakeTransport())
        assert ep.url == "/sessions/online"

    def test_send_posts_with_correct_headers(
        self, fake_transport: FakeTransport
    ) -> None:
        from ksef_sdk.endpoints.session import OpenSessionEndpoint

        fake_transport.enqueue(
            {
                "referenceNumber": _REF,
                "validUntil": "2025-07-11T12:00:00+00:00",
            }
        )
        ep = OpenSessionEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, body={"formCode": {}, "encryption": {}})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/sessions/online"
        assert call.headers == {"SessionToken": _TOKEN}


class TestTerminateSessionEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef_sdk.endpoints.session import TerminateSessionEndpoint

        ep = TerminateSessionEndpoint(FakeTransport())
        assert _REF in ep.get_url(reference_number=_REF)

    def test_send_deletes(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.session import TerminateSessionEndpoint

        fake_transport.enqueue(status_code=200)
        ep = TerminateSessionEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "DELETE"
        assert _REF in call.path
        assert call.headers == {"SessionToken": _TOKEN}


class TestDownloadInvoiceEndpoint:
    def test_url_contains_ksef_number(self) -> None:
        from ksef_sdk.endpoints.invoices import DownloadInvoiceEndpoint

        ep = DownloadInvoiceEndpoint(FakeTransport())
        url = ep.get_url(ksef_number="INV-123")

        assert "INV-123" in url

    def test_send_gets(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.invoices import DownloadInvoiceEndpoint

        fake_transport.enqueue(content=b"<Invoice/>")
        ep = DownloadInvoiceEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, ksef_number="INV-123")

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert "INV-123" in call.path
        assert call.headers == {"SessionToken": _TOKEN}


class TestSendingInvoicesEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef_sdk.endpoints.invoices import SendingInvoicesEndpoint

        ep = SendingInvoicesEndpoint(FakeTransport())
        url = ep.get_url(reference_number=_REF)

        assert _REF in url
        assert url.endswith("/invoices")

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.invoices import SendingInvoicesEndpoint

        fake_transport.enqueue({"referenceNumber": _REF})
        ep = SendingInvoicesEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF, body={"test": True})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.headers == {"SessionToken": _TOKEN}


class TestCertificateEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.encryption import CertificateEndpoint

        ep = CertificateEndpoint(FakeTransport())
        assert ep.url == "/security/public-key-certificates"

    def test_fetch_sends_get(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.encryption import CertificateEndpoint

        fake_transport.enqueue([])
        ep = CertificateEndpoint(fake_transport)

        ep.fetch()

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.path == "/security/public-key-certificates"
