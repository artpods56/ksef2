from __future__ import annotations

import pytest

from ksef2 import Client
from ksef2.core.exceptions import KSeFAuthError
from ksef2.domain.models.auth import AuthTokens


@pytest.mark.integration
def test_full_auth_flow(authenticated_context):
    """Full token authentication flow against real KSeF TEST API.

    Flow: Challenge → Encrypt Token → Init Auth → Poll Status → Redeem Tokens

    Verifies:
        - Access token is returned
        - Refresh token is returned
        - Tokens are different (not the same JWT)
    """
    client, tokens = authenticated_context

    assert isinstance(tokens, AuthTokens)
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None
    assert tokens.access_token.token != tokens.refresh_token.token
    assert tokens.access_token.valid_until is not None
    assert tokens.refresh_token.valid_until is not None


@pytest.mark.integration
def test_invalid_ksef_token_fails(real_client: Client, ksef_credentials):
    """Verify proper error when using invalid KSeF token."""
    with pytest.raises(KSeFAuthError):
        real_client.auth.authenticate_token(
            ksef_token="invalid-token-that-does-not-exist",
            nip=ksef_credentials.subject_nip,
        )
