"""Tests for auth endpoint classes — URL correctness, HTTP method, headers."""

from __future__ import annotations

from tests.unit.conftest import FakeTransport, _REF, _TOKEN


# ---------------------------------------------------------------------------
# ChallengeEndpoint
# ---------------------------------------------------------------------------


class TestChallengeEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.auth import ChallengeEndpoint

        ep = ChallengeEndpoint(FakeTransport())
        assert ep.url == "/auth/challenge"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.auth import ChallengeEndpoint

        fake_transport.enqueue(
            {
                "challenge": "a" * 36,
                "timestamp": "2025-07-11T12:00:00+00:00",
                "timestampMs": 1720699200000,
            }
        )
        ep = ChallengeEndpoint(fake_transport)
        ep.send()

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/auth/challenge"


# ---------------------------------------------------------------------------
# TokenAuthEndpoint
# ---------------------------------------------------------------------------


class TestTokenAuthEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.auth import TokenAuthEndpoint

        ep = TokenAuthEndpoint(FakeTransport())
        assert ep.url == "/auth/ksef-token"

    def test_send_posts_json_body(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.auth import TokenAuthEndpoint

        fake_transport.enqueue(
            {
                "referenceNumber": _REF,
                "authenticationToken": {
                    "token": "jwt-token",
                    "validUntil": "2025-07-11T13:00:00+00:00",
                },
            }
        )
        ep = TokenAuthEndpoint(fake_transport)

        body = {
            "challenge": "c" * 36,
            "contextIdentifier": {"type": "Nip", "value": "1234567890"},
            "encryptedToken": "base64data==",
        }
        ep.send(body)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/auth/ksef-token"
        assert call.json == body


# ---------------------------------------------------------------------------
# XAdESAuthEndpoint
# ---------------------------------------------------------------------------


class TestXAdESAuthEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.auth import XAdESAuthEndpoint

        ep = XAdESAuthEndpoint(FakeTransport())
        assert ep.url == "/auth/xades-signature"

    def test_get_url_default(self) -> None:
        from ksef_sdk.endpoints.auth import XAdESAuthEndpoint

        ep = XAdESAuthEndpoint(FakeTransport())
        assert ep.get_url() == "/auth/xades-signature?verifyCertificateChain=false"

    def test_get_url_verify_chain_true(self) -> None:
        from ksef_sdk.endpoints.auth import XAdESAuthEndpoint

        ep = XAdESAuthEndpoint(FakeTransport())
        assert (
            ep.get_url(verify_chain=True)
            == "/auth/xades-signature?verifyCertificateChain=true"
        )

    def test_send_posts_xml_content(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.auth import XAdESAuthEndpoint

        fake_transport.enqueue(
            {
                "referenceNumber": _REF,
                "authenticationToken": {
                    "token": "jwt-token",
                    "validUntil": "2025-07-11T13:00:00+00:00",
                },
            }
        )
        ep = XAdESAuthEndpoint(fake_transport)

        signed_xml = b"<SignedXML/>"
        ep.send(signed_xml, verify_chain=False)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert "verifyCertificateChain=false" in call.path
        assert call.content == signed_xml
        assert call.headers == {"Content-Type": "application/xml"}


# ---------------------------------------------------------------------------
# AuthStatusEndpoint
# ---------------------------------------------------------------------------


class TestAuthStatusEndpoint:
    def test_url_contains_reference_number(self) -> None:
        from ksef_sdk.endpoints.auth import AuthStatusEndpoint

        ep = AuthStatusEndpoint(FakeTransport())
        assert _REF in ep.get_url(reference_number=_REF)

    def test_send_gets_with_bearer_header(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.auth import AuthStatusEndpoint

        fake_transport.enqueue(
            {
                "startDate": "2025-07-11T12:00:00+00:00",
                "authenticationMethod": "Token",
                "status": {"code": 200, "description": "OK"},
            }
        )
        ep = AuthStatusEndpoint(fake_transport)

        ep.send(bearer_token=_TOKEN, reference_number=_REF)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert _REF in call.path
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


# ---------------------------------------------------------------------------
# RedeemTokenEndpoint
# ---------------------------------------------------------------------------


class TestRedeemTokenEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.auth import RedeemTokenEndpoint

        ep = RedeemTokenEndpoint(FakeTransport())
        assert ep.url == "/auth/token/redeem"

    def test_send_posts_with_bearer_header(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.auth import RedeemTokenEndpoint

        fake_transport.enqueue(
            {
                "accessToken": {
                    "token": "access-jwt",
                    "validUntil": "2025-07-11T14:00:00+00:00",
                },
                "refreshToken": {
                    "token": "refresh-jwt",
                    "validUntil": "2025-07-12T12:00:00+00:00",
                },
            }
        )
        ep = RedeemTokenEndpoint(fake_transport)

        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/auth/token/redeem"
        assert call.headers == {"Authorization": f"Bearer {_TOKEN}"}


# ---------------------------------------------------------------------------
# RefreshTokenEndpoint
# ---------------------------------------------------------------------------


class TestRefreshTokenEndpoint:
    def test_url(self) -> None:
        from ksef_sdk.endpoints.auth import RefreshTokenEndpoint

        ep = RefreshTokenEndpoint(FakeTransport())
        assert ep.url == "/auth/token/refresh"

    def test_send_posts_with_bearer_header(self, fake_transport: FakeTransport) -> None:
        from ksef_sdk.endpoints.auth import RefreshTokenEndpoint

        fake_transport.enqueue(
            {
                "accessToken": {
                    "token": "new-access-jwt",
                    "validUntil": "2025-07-11T15:00:00+00:00",
                },
            }
        )
        ep = RefreshTokenEndpoint(fake_transport)

        ep.send(bearer_token="refresh-token")

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/auth/token/refresh"
        assert call.headers == {"Authorization": "Bearer refresh-token"}
