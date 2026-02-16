"""Tests for token endpoint classes — URL correctness and HTTP method."""

from __future__ import annotations

from tests.unit.conftest import FakeTransport, _TOKEN, _REF


class TestGenerateTokenEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.tokens import GenerateTokenEndpoint

        ep = GenerateTokenEndpoint(FakeTransport())
        assert ep.url == "/tokens"

    def test_send_posts_with_correct_headers(
        self, fake_transport: FakeTransport
    ) -> None:
        from ksef2.endpoints.tokens import GenerateTokenEndpoint

        fake_transport.enqueue({"referenceNumber": _REF, "token": "tok123"})
        ep = GenerateTokenEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, body={"permissions": [], "description": "test"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/tokens"
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


class TestTokenStatusEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef2.endpoints.tokens import TokenStatusEndpoint

        ep = TokenStatusEndpoint(FakeTransport())
        assert _REF in ep.get_url(reference_number=_REF)

    def test_send_gets_with_correct_headers(
        self, fake_transport: FakeTransport
    ) -> None:
        from ksef2.endpoints.tokens import TokenStatusEndpoint

        fake_transport.enqueue(
            {
                "referenceNumber": _REF,
                "authorIdentifier": {"type": "Nip", "value": "1234567890"},
                "contextIdentifier": {"type": "Nip", "value": "1234567890"},
                "description": "test token",
                "requestedPermissions": ["InvoiceRead"],
                "dateCreated": "2025-07-11T12:00:00+00:00",
                "status": "Active",
            }
        )
        ep = TokenStatusEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _REF in call.path
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


class TestRevokeTokenEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef2.endpoints.tokens import RevokeTokenEndpoint

        ep = RevokeTokenEndpoint(FakeTransport())
        assert _REF in ep.get_url(reference_number=_REF)

    def test_send_deletes(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.tokens import RevokeTokenEndpoint

        fake_transport.enqueue(status_code=200)
        ep = RevokeTokenEndpoint(fake_transport)

        ep.send(access_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "DELETE"
        assert _REF in call.path
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}
