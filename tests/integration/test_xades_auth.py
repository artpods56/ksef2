from __future__ import annotations

import pytest

from ksef2.core.exceptions import KSeFApiError
from ksef2.domain.models.auth import AuthTokens
from ksef2.domain.models.tokens import GenerateTokenResponse, TokenPermission


@pytest.mark.integration
def test_xades_auth_with_self_signed_cert(xades_authenticated_context):
    """Authenticate using XAdES with self-signed certificate (TEST env only).

    This test verifies that:
    - Self-signed certificates work for authentication on TEST environment
    - Access and refresh tokens are returned
    - Tokens have valid expiration times
    """
    client, tokens = xades_authenticated_context

    assert isinstance(tokens, AuthTokens)
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None
    assert tokens.access_token.token != tokens.refresh_token.token
    assert tokens.access_token.valid_until is not None
    assert tokens.refresh_token.valid_until is not None

    print("\n\n=== KSEF TOKEN (add to .env.test as KSEF_TEST_KSEF_TOKEN) ===")
    print(tokens.access_token.token[:50] + "...")  # Just show a hint
    print("=========================================================\n")


@pytest.mark.integration
def test_generate_ksef_token(xades_authenticated_context):
    """Generate a new KSeF token after XAdES authentication.

    This creates a KSeF token that can be used for future authenticate_token() calls
    instead of XAdES authentication.

    Note: This may fail if the authenticated entity doesn't have CredentialsManage
    permission. The testdata API requires granting permissions to a person (PESEL),
    not a subject (NIP).
    """
    client, tokens = xades_authenticated_context

    try:
        ksef_token_response = client.tokens.generate(
            access_token=tokens.access_token.token,
            permissions=[
                TokenPermission.INVOICE_WRITE,
                TokenPermission.INVOICE_READ,
            ],
            description="Integration test KSeF token",
        )

        assert isinstance(ksef_token_response, GenerateTokenResponse)
        assert ksef_token_response.token is not None
        assert ksef_token_response.reference_number is not None
    except KSeFApiError as e:
        if "401" in str(e) or "credentials" in str(e).lower():
            pytest.skip("Token generation requires CredentialsManage permission")
        raise
