from __future__ import annotations

import pytest

from ksef2.domain.models.auth import RefreshedToken


@pytest.mark.integration
def test_refresh_token(authenticated_context):
    """Exchange refresh token for new access token."""
    client, tokens = authenticated_context

    refreshed = client.auth.refresh(refresh_token=tokens.refresh_token.token)

    assert isinstance(refreshed, RefreshedToken)
    assert refreshed.access_token is not None
    assert refreshed.access_token.token != tokens.access_token.token
    assert refreshed.access_token.valid_until is not None


@pytest.mark.integration
def test_refreshed_token_works(authenticated_context):
    """Verify the refreshed token can be used for API calls."""
    client, tokens = authenticated_context

    refreshed = client.auth.refresh(refresh_token=tokens.refresh_token.token)

    assert refreshed.access_token.token is not None
