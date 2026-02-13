from __future__ import annotations

import pytest


@pytest.mark.integration
def test_list_active_sessions(xades_authenticated_context):
    """List active authentication sessions."""
    client, tokens = xades_authenticated_context

    response = client.auth.list_active_sessions(
        access_token=tokens.access_token.token,
    )

    assert response is not None
    assert hasattr(response, "items")
    assert hasattr(response, "continuationToken")


@pytest.mark.integration
def test_list_active_sessions_with_pagination(xades_authenticated_context):
    """List active sessions with pagination."""
    client, tokens = xades_authenticated_context

    response = client.auth.list_active_sessions(
        access_token=tokens.access_token.token,
        page_size=5,
    )

    assert response is not None
    assert len(response.items) <= 5


@pytest.mark.integration
def test_terminate_current_session(xades_authenticated_context):
    """Terminate the current authentication session."""
    client, tokens = xades_authenticated_context

    client.auth.terminate_current_session(
        access_token=tokens.access_token.token,
    )


@pytest.mark.integration
def test_terminate_specific_session(xades_authenticated_context):
    """Terminate a specific authentication session by reference number."""
    client, tokens = xades_authenticated_context

    sessions_response = client.auth.list_active_sessions(
        access_token=tokens.access_token.token,
    )

    if sessions_response.items:
        ref_to_delete = sessions_response.items[0].referenceNumber

        client.auth.terminate_session(
            access_token=tokens.access_token.token,
            reference_number=ref_to_delete,
        )
