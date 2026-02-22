from __future__ import annotations


import pytest

from ksef2 import Client
from ksef2.clients.authenticated import AuthenticatedClient


@pytest.mark.integration
def test_list_active_sessions(
    xades_authenticated_context: tuple[Client, AuthenticatedClient],
):
    """List active authentication sessions."""
    client, auth = xades_authenticated_context

    response = auth.sessions.list_page()

    assert response is not None
    assert hasattr(response, "items")
    assert hasattr(response, "continuationToken")


@pytest.mark.integration
def test_list_active_sessions_with_pagination(xades_authenticated_context):
    """List active sessions with pagination."""
    client, auth = xades_authenticated_context

    response = auth.sessions.list_page(page_size=15)  # must be between 10 and 100

    assert response is not None
    assert len(response.items) <= 15


@pytest.mark.integration
def test_terminate_current_session(xades_authenticated_context):
    """Terminate the current authentication session."""
    client, auth = xades_authenticated_context

    auth.sessions.terminate_current()


@pytest.mark.integration
def test_terminate_specific_session(xades_authenticated_context):
    """Terminate a specific authentication session by reference number."""
    client, auth = xades_authenticated_context

    sessions_response = auth.sessions.list_page()

    if sessions_response.items:
        ref_to_delete = sessions_response.items[0].referenceNumber

        auth.sessions.close(reference_number=ref_to_delete)
