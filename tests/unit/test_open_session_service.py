"""Tests for AuthenticatedClient.online_session — session opening flow."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pytest

from ksef2.clients.authenticated import AuthenticatedClient
from ksef2.clients.online import OnlineSessionClient
from ksef2.core import exceptions
from ksef2.core.stores import CertificateStore
from ksef2.domain.models.auth import AuthTokens, TokenCredentials
from ksef2.domain.models.encryption import CertUsage
from ksef2.domain.models.session import FormSchema

from tests.unit.conftest import (
    FakeTransport,
    make_certificate,
    _REF,
)


_NOW = datetime.now(tz=timezone.utc)
_VALID_UNTIL = (_NOW + timedelta(hours=1)).isoformat()
_REFRESH_UNTIL = (_NOW + timedelta(days=7)).isoformat()


def _open_session_response(
    ref: str = _REF,
    valid_until: str = _VALID_UNTIL,
) -> dict[str, str]:
    return {"referenceNumber": ref, "validUntil": valid_until}


def _make_auth_tokens() -> AuthTokens:
    return AuthTokens(
        access_token=TokenCredentials(
            token="tok", valid_until=_NOW + timedelta(hours=1)
        ),
        refresh_token=TokenCredentials(
            token="refresh", valid_until=_NOW + timedelta(days=7)
        ),
    )


def _build_client(
    transport: FakeTransport,
    store: CertificateStore | None = None,
) -> AuthenticatedClient:
    return AuthenticatedClient(
        transport=transport,
        auth_tokens=_make_auth_tokens(),
        certificate_store=store or CertificateStore(),
    )


# ---------------------------------------------------------------------------
# A real RSA cert is needed for encrypt_symmetric_key.
# We generate one once for all tests in this module.
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
                usage=[CertUsage.SYMMETRIC_KEY_ENCRYPTION],
            )
        ]
    )
    return store


# ---------------------------------------------------------------------------
# online_session
# ---------------------------------------------------------------------------


class TestOnlineSession:
    def test_returns_online_session_client(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_open_session_response())  # POST /sessions/online

        result = _build_client(fake_transport, loaded_store).online_session(
            form_code=FormSchema.FA3,
        )

        assert isinstance(result, OnlineSessionClient)

    def test_fetches_certificates_when_store_is_empty(
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
                    "usage": ["SymmetricKeyEncryption"],
                }
            ]
        )  # GET /security/public-key-certificates
        fake_transport.enqueue(_open_session_response())  # POST /sessions/online

        empty_store = CertificateStore()
        _build_client(fake_transport, empty_store).online_session(
            form_code=FormSchema.FA3,
        )

        assert fake_transport.calls[0].method == "GET"
        assert len(empty_store.all()) == 1

    def test_skips_fetch_when_store_has_certs(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_open_session_response())

        _build_client(fake_transport, loaded_store).online_session(
            form_code=FormSchema.FA3,
        )

        # Only one call (POST to open session), no GET for certificates
        assert len(fake_transport.calls) == 1
        assert fake_transport.calls[0].method == "POST"

    def test_raises_when_no_valid_cert(self, fake_transport: FakeTransport) -> None:
        store = CertificateStore()
        store.load(
            [
                make_certificate(
                    usage=[CertUsage.KSEF_TOKEN_ENCRYPTION],  # wrong usage
                )
            ]
        )

        with pytest.raises(exceptions.NoCertificateAvailableError):
            _build_client(fake_transport, store).online_session(
                form_code=FormSchema.FA3,
            )

    def test_sends_session_token_header(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_open_session_response())

        _build_client(fake_transport, loaded_store).online_session(
            form_code=FormSchema.FA3,
        )

        call = fake_transport.calls[0]
        assert call.headers == {"Authorization": "Bearer tok"}

    def test_request_body_contains_form_and_encryption(
        self,
        fake_transport: FakeTransport,
        loaded_store: CertificateStore,
    ) -> None:
        fake_transport.enqueue(_open_session_response())

        _build_client(fake_transport, loaded_store).online_session(
            form_code=FormSchema.FA3,
        )

        body = fake_transport.calls[0].json
        assert body is not None
        assert "formCode" in body
        assert body["formCode"]["systemCode"] == "FA (3)"
        assert body["formCode"]["schemaVersion"] == "1-0E"
        assert body["formCode"]["value"] == "FA"
        assert "encryption" in body
        assert "encryptedSymmetricKey" in body["encryption"]
        assert "initializationVector" in body["encryption"]
