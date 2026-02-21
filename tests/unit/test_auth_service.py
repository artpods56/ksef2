"""Tests for AuthService — token auth, XAdES auth, refresh, polling."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any
from unittest.mock import patch, MagicMock

import pytest

from ksef2.clients.authenticated import AuthenticatedClient
from ksef2.core import exceptions
from ksef2.core.stores import CertificateStore
from ksef2.domain.models.auth import RefreshedToken
from ksef2.domain.models.encryption import CertUsage
from ksef2.services.auth import AuthService

from tests.unit.conftest import (
    FakeTransport,
    make_certificate,
    _REF,
)


_NOW = datetime.now(tz=timezone.utc)
_VALID_UNTIL = (_NOW + timedelta(hours=1)).isoformat()
_REFRESH_UNTIL = (_NOW + timedelta(days=7)).isoformat()


def _challenge_response() -> dict[str, Any]:
    return {
        "challenge": "c" * 36,
        "timestamp": _NOW.isoformat(),
        "timestampMs": int(_NOW.timestamp() * 1000),
    }


def _init_response(ref: str = _REF) -> dict[str, Any]:
    return {
        "referenceNumber": ref,
        "authenticationToken": {
            "token": "auth-jwt",
            "validUntil": _VALID_UNTIL,
        },
    }


def _status_response(code: int = 200, description: str = "OK") -> dict[str, Any]:
    return {
        "startDate": _NOW.isoformat(),
        "authenticationMethod": "Token",
        "authenticationMethodInfo": {
            "category": "Token",
            "code": "Token",
            "displayName": "Token KSeF",
        },
        "status": {"code": code, "description": description},
    }


def _tokens_response() -> dict[str, Any]:
    return {
        "accessToken": {"token": "access-jwt", "validUntil": _VALID_UNTIL},
        "refreshToken": {"token": "refresh-jwt", "validUntil": _REFRESH_UNTIL},
    }


def _refresh_response() -> dict[str, Any]:
    return {
        "accessToken": {"token": "new-access-jwt", "validUntil": _VALID_UNTIL},
    }


def _build_service(
    transport: FakeTransport,
    store: CertificateStore | None = None,
) -> AuthService:
    return AuthService(
        transport=transport,
        certificate_store=store or CertificateStore(),
    )


# ---------------------------------------------------------------------------
# A real RSA cert is needed for encrypt_token.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def rsa_cert_b64() -> str:
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    import base64

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "test")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime(2020, 1, 1, tzinfo=timezone.utc))
        .not_valid_after(datetime(2030, 1, 1, tzinfo=timezone.utc))
        .sign(key, hashes.SHA256())
    )
    return base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode()


@pytest.fixture
def loaded_store(rsa_cert_b64: str) -> CertificateStore:
    store = CertificateStore()
    store.load(
        [
            make_certificate(
                certificate=rsa_cert_b64,
                usage=[CertUsage.KSEF_TOKEN_ENCRYPTION],
            )
        ]
    )
    return store


# ---------------------------------------------------------------------------
# authenticate_token
# ---------------------------------------------------------------------------


class TestAuthenticateToken:
    def test_full_flow_returns_auth_tokens(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_challenge_response())  # POST /auth/challenge
        fake_transport.enqueue(_init_response())  # POST /auth/ksef-token
        fake_transport.enqueue(_status_response(200))  # GET /auth/{ref}
        fake_transport.enqueue(_tokens_response())  # POST /auth/token/redeem

        result = _build_service(fake_transport, loaded_store).authenticate_token(
            ksef_token="my-ksef-token",
            nip="1234567890",
            poll_interval=0,
        )

        assert isinstance(result, AuthenticatedClient)
        assert result.access_token == "access-jwt"
        assert result.refresh_token == "refresh-jwt"

    def test_fetches_certificates_when_store_empty(
        self,
        fake_transport: FakeTransport,
        rsa_cert_b64: str,
    ) -> None:
        now = datetime.now(tz=timezone.utc)
        fake_transport.enqueue(
            [
                {
                    "certificate": rsa_cert_b64,
                    "validFrom": (now - timedelta(days=30)).isoformat(),
                    "validTo": (now + timedelta(days=30)).isoformat(),
                    "usage": ["KsefTokenEncryption"],
                }
            ]
        )  # GET /security/public-key-certificates
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        fake_transport.enqueue(_status_response(200))
        fake_transport.enqueue(_tokens_response())

        empty_store = CertificateStore()
        _build_service(fake_transport, empty_store).authenticate_token(
            ksef_token="tok",
            nip="1234567890",
            poll_interval=0,
        )

        assert fake_transport.calls[0].method == "GET"
        assert len(empty_store.all()) == 1

    def test_polls_until_success(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        fake_transport.enqueue(_status_response(100, "In progress"))  # poll 1
        fake_transport.enqueue(_status_response(100, "In progress"))  # poll 2
        fake_transport.enqueue(_status_response(200, "OK"))  # poll 3
        fake_transport.enqueue(_tokens_response())

        result = _build_service(fake_transport, loaded_store).authenticate_token(
            ksef_token="tok",
            nip="1234567890",
            poll_interval=0,
        )

        assert isinstance(result, AuthenticatedClient)
        # 2 (challenge + init) + 3 (polls) + 1 (redeem) = 6
        assert len(fake_transport.calls) == 6

    def test_raises_on_auth_failure(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        fake_transport.enqueue(_status_response(450, "Invalid token"))

        with pytest.raises(exceptions.KSeFAuthError):
            _build_service(fake_transport, loaded_store).authenticate_token(
                ksef_token="invalid-token",
                nip="1234567890",
                poll_interval=0,
            )

    def test_raises_on_timeout(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        # Only enqueue "in progress" responses - fewer than max_poll_attempts
        for _ in range(3):
            fake_transport.enqueue(_status_response(100, "In progress"))

        with pytest.raises(exceptions.KSeFAuthError, match="timed out"):
            _build_service(fake_transport, loaded_store).authenticate_token(
                ksef_token="tok",
                nip="1234567890",
                poll_interval=0,
                max_poll_attempts=3,
            )


# ---------------------------------------------------------------------------
# authenticate_xades
# ---------------------------------------------------------------------------


class TestAuthenticateXades:
    @patch("ksef2.core.xades.sign_xades", return_value=b"<SignedXML/>")
    @patch(
        "ksef2.core.xades.build_auth_token_request_xml",
        return_value=b"<AuthTokenRequest/>",
    )
    def test_full_flow_returns_auth_tokens(
        self,
        mock_build: MagicMock,
        mock_sign: MagicMock,
        fake_transport: FakeTransport,
    ) -> None:
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        fake_transport.enqueue(_status_response(200))
        fake_transport.enqueue(_tokens_response())

        cert_mock = MagicMock()
        key_mock = MagicMock()

        result = _build_service(fake_transport).authenticate_xades(
            nip="1234567890",
            cert=cert_mock,
            private_key=key_mock,
            poll_interval=0,
        )

        assert isinstance(result, AuthenticatedClient)
        mock_build.assert_called_once_with("c" * 36, "1234567890")
        mock_sign.assert_called_once_with(b"<AuthTokenRequest/>", cert_mock, key_mock)

    @patch("ksef2.core.xades.sign_xades", return_value=b"<SignedXML/>")
    @patch(
        "ksef2.core.xades.build_auth_token_request_xml",
        return_value=b"<AuthTokenRequest/>",
    )
    def test_does_not_load_certificates(
        self,
        mock_build: MagicMock,
        mock_sign: MagicMock,
        fake_transport: FakeTransport,
    ) -> None:
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        fake_transport.enqueue(_status_response(200))
        fake_transport.enqueue(_tokens_response())

        _build_service(fake_transport).authenticate_xades(
            nip="1234567890",
            cert=MagicMock(),
            private_key=MagicMock(),
            poll_interval=0,
        )

        # No GET for certificates — only POST challenge, POST xades, GET status, POST redeem
        methods = [c.method for c in fake_transport.calls]
        assert "GET" not in methods[:2]  # first two calls should be POST

    @patch("ksef2.core.xades.sign_xades", return_value=b"<SignedXML/>")
    @patch(
        "ksef2.core.xades.build_auth_token_request_xml",
        return_value=b"<AuthTokenRequest/>",
    )
    def test_sends_xml_content(
        self,
        mock_build: MagicMock,
        mock_sign: MagicMock,
        fake_transport: FakeTransport,
    ) -> None:
        fake_transport.enqueue(_challenge_response())
        fake_transport.enqueue(_init_response())
        fake_transport.enqueue(_status_response(200))
        fake_transport.enqueue(_tokens_response())

        _build_service(fake_transport).authenticate_xades(
            nip="1234567890",
            cert=MagicMock(),
            private_key=MagicMock(),
            poll_interval=0,
        )

        # The XAdES endpoint call goes through request() which records content
        xades_call = fake_transport.calls[1]  # second call (after challenge)
        assert xades_call.content == b"<SignedXML/>"


# ---------------------------------------------------------------------------
# sign_xades — EC key support
# ---------------------------------------------------------------------------


class TestSignXadesEC:
    @pytest.fixture(scope="class")
    def ec_cert_and_key(self):
        import datetime
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import hashes
        from cryptography import x509
        from cryptography.x509.oid import NameOID

        key = ec.generate_private_key(ec.SECP256R1())
        subject = issuer = x509.Name(
            [x509.NameAttribute(NameOID.COMMON_NAME, "EC Test")]
        )
        now = datetime.datetime.now(datetime.timezone.utc)
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(hours=1))
            .not_valid_after(now + datetime.timedelta(days=365))
            .sign(key, hashes.SHA256())
        )
        return cert, key

    def test_sign_xades_ec_does_not_raise(self, ec_cert_and_key) -> None:
        from ksef2.core.xades import build_auth_token_request_xml, sign_xades

        cert, key = ec_cert_and_key
        xml_bytes = build_auth_token_request_xml("c" * 36, "1234567890")
        signed = sign_xades(xml_bytes, cert, key)
        assert signed is not None
        assert b"<" in signed

    def test_sign_xades_ec_produces_ecdsa_signature(self, ec_cert_and_key) -> None:
        from ksef2.core.xades import build_auth_token_request_xml, sign_xades

        cert, key = ec_cert_and_key
        xml_bytes = build_auth_token_request_xml("c" * 36, "1234567890")
        signed = sign_xades(xml_bytes, cert, key)
        assert b"ecdsa-sha256" in signed.lower() or b"ECDSA" in signed


# ---------------------------------------------------------------------------
# load_certificate_and_key_from_p12 — EC key
# ---------------------------------------------------------------------------


class TestLoadP12EC:
    @pytest.fixture(scope="class")
    def ec_p12_bytes(self):
        import datetime
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.serialization import pkcs12
        from cryptography import x509
        from cryptography.x509.oid import NameOID

        key = ec.generate_private_key(ec.SECP256R1())
        subject = issuer = x509.Name(
            [x509.NameAttribute(NameOID.COMMON_NAME, "EC P12 Test")]
        )
        now = datetime.datetime.now(datetime.timezone.utc)
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(hours=1))
            .not_valid_after(now + datetime.timedelta(days=365))
            .sign(key, hashes.SHA256())
        )
        return pkcs12.serialize_key_and_certificates(
            name=b"ec-test",
            key=key,
            cert=cert,
            cas=None,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def test_loads_ec_key_from_p12(self, ec_p12_bytes: bytes) -> None:
        from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
        from ksef2.core.xades import load_certificate_and_key_from_p12

        cert, key = load_certificate_and_key_from_p12(ec_p12_bytes)
        assert isinstance(key, EllipticCurvePrivateKey)

    def test_ec_key_from_p12_can_sign(self, ec_p12_bytes: bytes) -> None:
        from ksef2.core.xades import (
            build_auth_token_request_xml,
            load_certificate_and_key_from_p12,
            sign_xades,
        )

        cert, key = load_certificate_and_key_from_p12(ec_p12_bytes)
        xml_bytes = build_auth_token_request_xml("c" * 36, "1234567890")
        signed = sign_xades(xml_bytes, cert, key)
        assert signed is not None
        assert b"<" in signed


# ---------------------------------------------------------------------------
# refresh
# ---------------------------------------------------------------------------


class TestRefresh:
    def test_returns_refreshed_token(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(_refresh_response())

        result = _build_service(fake_transport).refresh(refresh_token="refresh-jwt")

        assert isinstance(result, RefreshedToken)
        assert result.access_token.token == "new-access-jwt"

    def test_sends_bearer_header(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(_refresh_response())

        _build_service(fake_transport).refresh(refresh_token="my-refresh-token")

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/auth/token/refresh"
        assert call.headers == {"Authorization": "Bearer my-refresh-token"}
