"""Service for managing authentication sessions."""

from __future__ import annotations

from typing import TYPE_CHECKING, final

from ksef2.endpoints.auth import (
    ListActiveSessionsEndpoint,
    TerminateAuthSessionEndpoint,
    TerminateCurrentSessionEndpoint,
)
from ksef2.infra.schema.api import spec as spec

if TYPE_CHECKING:
    from ksef2.core import protocols


@final
class SessionManagementService:
    """Service for listing and terminating authentication sessions.

    This service manages authentication sessions (not invoice sessions).
    It allows you to list active sessions and terminate them.

    Typical usage:
        auth = client.auth.authenticate_xades(nip=nip, cert=cert, private_key=key)

        # List active sessions
        sessions = auth.sessions.list()

        # Terminate current session
        auth.sessions.terminate_current()

        # Terminate specific session
        auth.sessions.terminate(reference_number="20250217-...")
    """

    def __init__(self, transport: "protocols.Middleware", access_token: str) -> None:
        self._access_token = access_token
        self._list_ep = ListActiveSessionsEndpoint(transport)
        self._terminate_current_ep = TerminateCurrentSessionEndpoint(transport)
        self._terminate_ep = TerminateAuthSessionEndpoint(transport)

    def list(
        self,
        *,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> spec.AuthenticationListResponse:
        """List active authentication sessions.

        Args:
            page_size: Number of results per page.
            continuation_token: Token for fetching next page.

        Returns:
            AuthenticationListResponse with the list of sessions.
        """
        return self._list_ep.send(
            bearer_token=self._access_token,
            page_size=page_size,
            continuation_token=continuation_token,
        )

    def terminate_current(self) -> None:
        """Terminate the current authentication session."""
        self._terminate_current_ep.send(bearer_token=self._access_token)

    def terminate(self, *, reference_number: str) -> None:
        """Terminate a specific authentication session.

        Args:
            reference_number: The session's reference number.
        """
        self._terminate_ep.send(
            bearer_token=self._access_token,
            reference_number=reference_number,
        )
