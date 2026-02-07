from __future__ import annotations

import pytest

from ksef_sdk import Environment, KsefClient

pytestmark = pytest.mark.integration


class TestTokenAuth:
    """Tests for token-based authentication (require KSEF_TEST_TOKEN)."""

    def test_authenticate(self, ksef_nip: str, ksef_token: str | None) -> None:
        """Full auth flow: challenge -> init -> poll -> redeem."""
        if ksef_token is None:
            pytest.skip("KSEF_TEST_TOKEN not set")
        with KsefClient(nip=ksef_nip, token=ksef_token, env=Environment.TEST) as client:
            client.authenticate()
            assert client._http._access_token is not None

    def test_refresh_token(self, ksef_nip: str, ksef_token: str | None) -> None:
        """Authenticate then refresh the access token."""
        if ksef_token is None:
            pytest.skip("KSEF_TEST_TOKEN not set")
        with KsefClient(nip=ksef_nip, token=ksef_token, env=Environment.TEST) as client:
            client.authenticate()
            old_token = client._http._access_token
            client.refresh_access_token()
            assert client._http._access_token is not None
            assert client._http._access_token != old_token


class TestXadesAuth:
    """Tests for XAdES certificate-based authentication (no token needed)."""

    def test_authenticate_xades(self, ksef_nip: str) -> None:
        """XAdES auth flow: challenge -> sign XML -> submit -> poll -> redeem."""
        with KsefClient(nip=ksef_nip, env=Environment.TEST) as client:
            client.authenticate_xades()
            assert client._http._access_token is not None
            assert client._refresh_token is not None

    def test_xades_then_refresh(self, ksef_nip: str) -> None:
        """Authenticate via XAdES, then refresh the access token."""
        with KsefClient(nip=ksef_nip, env=Environment.TEST) as client:
            client.authenticate_xades()
            old_token = client._http._access_token
            client.refresh_access_token()
            assert client._http._access_token is not None
            assert client._http._access_token != old_token

    def test_xades_generate_and_revoke_token(self, ksef_nip: str) -> None:
        """Authenticate via XAdES, generate a KSeF token, then revoke it."""
        with KsefClient(nip=ksef_nip, env=Environment.TEST) as client:
            client.authenticate_xades()

            resp = client.generate_ksef_token(
                ["InvoiceRead", "InvoiceWrite"],
                "Integration test token",
            )
            assert resp.token
            assert resp.referenceNumber

            status = client.get_ksef_token_status(resp.referenceNumber)
            assert status.status == "Active"

            client.revoke_ksef_token(resp.referenceNumber)
