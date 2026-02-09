"""Tests for EncryptionClient."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

from ksef2.clients.encryption import EncryptionClient
from ksef2.domain.models.encryption import CertUsage, PublicKeyCertificate

from tests.unit.conftest import FakeTransport


class TestGetCertificates:
    def test_returns_domain_models(self, fake_transport: FakeTransport) -> None:
        now = datetime.now(tz=timezone.utc)
        fake_transport.enqueue(
            [
                {
                    "certificate": "AAAA",
                    "validFrom": (now - timedelta(days=10)).isoformat(),
                    "validTo": (now + timedelta(days=10)).isoformat(),
                    "usage": ["SymmetricKeyEncryption"],
                },
            ]
        )

        client = EncryptionClient(fake_transport)
        result = client.get_certificates()

        assert len(result) == 1
        assert isinstance(result[0], PublicKeyCertificate)
        assert CertUsage.SYMMETRIC_KEY_ENCRYPTION in result[0].usage

    def test_returns_empty_list(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue([])

        client = EncryptionClient(fake_transport)
        result = client.get_certificates()

        assert result == []

    def test_maps_multiple_certificates(self, fake_transport: FakeTransport) -> None:
        now = datetime.now(tz=timezone.utc)
        certs = [
            {
                "certificate": "AAAA",
                "validFrom": (now - timedelta(days=10)).isoformat(),
                "validTo": (now + timedelta(days=10)).isoformat(),
                "usage": ["SymmetricKeyEncryption"],
            },
            {
                "certificate": "BBBB",
                "validFrom": (now - timedelta(days=5)).isoformat(),
                "validTo": (now + timedelta(days=5)).isoformat(),
                "usage": ["KsefTokenEncryption"],
            },
        ]
        fake_transport.enqueue(certs)

        client = EncryptionClient(fake_transport)
        result = client.get_certificates()

        assert len(result) == 2
        assert result[0].certificate == "AAAA"
        assert result[1].certificate == "BBBB"

    def test_sends_get_to_correct_url(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue([])

        client = EncryptionClient(fake_transport)
        client.get_certificates()

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.path == "/security/public-key-certificates"
