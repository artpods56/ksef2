"""Authenticated client for operations requiring only a bearer token."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, final

from ksef2.domain.models.auth import AuthTokens
from ksef2.services import PermissionsService
from ksef2.services.certificates import CertificateService
from ksef2.services.limits import LimitsService
from ksef2.services.session_management import SessionManagementService
from ksef2.services.tokens import TokenService

if TYPE_CHECKING:
    from ksef2.core import protocols


@final
class AuthenticatedClient:
    """Client for authenticated operations that don't require a full session.

    This lightweight client holds authentication tokens and provides access to
    services that only need authentication, not a full invoice session.

    Typical usage:
        auth = client.auth.authenticate_xades(nip=nip, cert=cert, private_key=key)

        # Access limits without opening a session
        limits = auth.limits.get_context_limits()

        # Manage KSeF authorization tokens
        result = auth.tokens.generate(
            permissions=[TokenPermission.INVOICE_READ],
            description="My API token",
        )

        # Access token for opening sessions
        session = client.sessions.open_online(
            access_token=auth.access_token,
            form_code=FormSchema.FA3,
        )

        # For backward compatibility, auth_tokens is also exposed
        token_str = auth.auth_tokens.access_token.token
    """

    def __init__(
        self,
        transport: "protocols.Middleware",
        auth_tokens: AuthTokens,
    ) -> None:
        self._transport = transport
        self._auth_tokens = auth_tokens

    @property
    def auth_tokens(self) -> AuthTokens:
        """Get the full authentication tokens (for backward compatibility)."""
        return self._auth_tokens

    @property
    def access_token(self) -> str:
        """Get the access token string for this authenticated context."""
        return self._auth_tokens.access_token.token

    @property
    def refresh_token(self) -> str:
        """Get the refresh token string."""
        return self._auth_tokens.refresh_token.token

    @cached_property
    def limits(self) -> LimitsService:
        """Access limits service for querying and modifying API limits."""
        return LimitsService(self._transport, self.access_token)

    @cached_property
    def tokens(self) -> TokenService:
        """Access token service for managing KSeF authorization tokens."""
        return TokenService(self._transport, self.access_token)

    @cached_property
    def certificates(self) -> CertificateService:
        """Access certificate service for managing KSeF certificates."""
        return CertificateService(self._transport, self.access_token)

    @cached_property
    def sessions(self) -> SessionManagementService:
        """Access session management service for listing/terminating auth sessions."""
        return SessionManagementService(self._transport, self.access_token)

    @cached_property
    def permissions(self) -> PermissionsService:
        """Access permissions service for managing KSeF permissions."""
        return PermissionsService(self._transport, self.access_token)
