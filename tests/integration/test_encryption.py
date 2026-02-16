"""Integration tests for the encryption client (public key certificates).

Run with:
    uv run pytest tests/integration/test_encryption.py -v -m integration
"""

from __future__ import annotations

import pytest

from ksef2 import Client
from ksef2.domain.models.encryption import PublicKeyCertificate, CertUsage


@pytest.mark.integration
def test_get_certificates(real_client: Client):
    """Fetch public key certificates from KSeF."""
    certs = real_client.encryption.get_certificates()

    assert isinstance(certs, list)
    assert len(certs) > 0

    cert = certs[0]
    assert isinstance(cert, PublicKeyCertificate)
    assert cert.certificate
    assert cert.valid_from is not None
    assert cert.valid_to is not None
    assert len(cert.usage) > 0
    assert all(isinstance(u, CertUsage) for u in cert.usage)
