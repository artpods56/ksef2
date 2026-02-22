from __future__ import annotations

import time
from collections.abc import Iterator
from typing import final

from ksef2.core import exceptions
from ksef2.core import protocols
from ksef2.domain.models.tokens import (
    GenerateTokenResponse,
    QueryTokensResponse,
    TokenAuthorIdentifier,
    TokenPermission,
    TokenStatus,
    TokenStatusResponse,
)
from ksef2.endpoints.tokens import (
    GenerateTokenEndpoint,
    ListTokensEndpoint,
    RevokeTokenEndpoint,
    TokenStatusEndpoint,
)
from ksef2.infra.mappers.requests.tokens import (
    GenerateTokenMapper,
    QueryTokensMapper,
    TokenStatusMapper,
)


@final
class TokenService:
    """Service for managing KSeF authorization tokens.

    This service manages tokens used for KSeF authentication. It stores
    the access_token internally, so you don't need to pass it to every method.

    Typical usage:
        auth = client.auth.authenticate_xades(nip=nip, cert=cert, private_key=key)

        # Generate a new KSeF token
        result = auth.tokens.generate(
            permissions=[TokenPermission.INVOICE_READ],
            description="My API token",
        )

        # List tokens
        tokens = auth.tokens.list()

        # Check status
        status = auth.tokens.status(reference_number=result.reference_number)

        # Revoke a token
        auth.tokens.revoke(reference_number=result.reference_number)
    """

    def __init__(self, transport: protocols.Middleware, access_token: str) -> None:
        self._access_token = access_token
        self._generate_ep = GenerateTokenEndpoint(transport)
        self._list_ep = ListTokensEndpoint(transport)
        self._status_ep = TokenStatusEndpoint(transport)
        self._revoke_ep = RevokeTokenEndpoint(transport)

    def generate(
        self,
        *,
        permissions: list[TokenPermission],
        description: str,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> GenerateTokenResponse:
        """Generate a new KSeF authorization token.

        Args:
            permissions: List of permissions to grant to the token.
            description: Human-readable description for the token.
            poll_interval: Seconds between status polls (default: 1.0).
            max_poll_attempts: Maximum polling attempts (default: 60).

        Returns:
            GenerateTokenResponse with the token details.

        Raises:
            KSeFApiError: If token generation or activation fails.
        """
        body = GenerateTokenMapper.map_request(permissions, description)
        spec_resp = self._generate_ep.send(
            access_token=self._access_token,
            body=body.model_dump(),
        )
        result = GenerateTokenMapper.map_response(spec_resp)

        _ = self._poll_until_active(
            reference_number=result.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )
        return result

    def list_page(
        self,
        *,
        status: list[TokenStatus] | None = None,
        description: str | None = None,
        author_filter: TokenAuthorIdentifier | None = None,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> QueryTokensResponse:
        """List KSeF authorization tokens.

        Args:
            status: Filter by token status(es).
            description: Filter by description substring.
            author_filter: Filter by token author identifier.
            page_size: Number of results per page.
            continuation_token: Token for fetching next page.

        Returns:
            QueryTokensResponse with the list of tokens.
        """
        spec_resp = self._list_ep.send(
            access_token=self._access_token,
            status=[s.value for s in status] if status else None,
            description=description,
            author_identifier=author_filter.value if author_filter else None,
            author_identifier_type=author_filter.type.value if author_filter else None,
            page_size=page_size,
            continuation_token=continuation_token,
        )
        return QueryTokensMapper.map_response(spec_resp)

    def list(
        self,
        *,
        page_size: int | None = None,
    ) -> Iterator[QueryTokensResponse]:
        response = self.list_page(page_size=page_size)
        yield response

        while ct := response.continuation_token:
            response = self.list_page(page_size=page_size, continuation_token=ct)
            yield response

    def status(
        self,
        *,
        reference_number: str,
    ) -> TokenStatusResponse:
        """Check the status of a KSeF token.

        Args:
            reference_number: The token's reference number.

        Returns:
            TokenStatusResponse with current status.
        """
        spec_resp = self._status_ep.send(
            access_token=self._access_token,
            reference_number=reference_number,
        )
        return TokenStatusMapper.map_response(spec_resp)

    def revoke(
        self,
        *,
        reference_number: str,
    ) -> None:
        """Revoke a KSeF authorization token.

        Args:
            reference_number: The token's reference number.
        """
        self._revoke_ep.send(
            access_token=self._access_token,
            reference_number=reference_number,
        )

    def _poll_until_active(
        self,
        *,
        reference_number: str,
        poll_interval: float,
        max_attempts: int,
    ) -> TokenStatusResponse:
        for _ in range(max_attempts):
            result = self.status(
                reference_number=reference_number,
            )
            if result.status == TokenStatus.ACTIVE:
                return result
            if result.status in (TokenStatus.FAILED, TokenStatus.REVOKED):
                raise exceptions.KSeFApiError(
                    0,
                    exceptions.ExceptionCode.UNKNOWN_ERROR,
                    f"Token activation failed: status={result.status.value}",
                )
            time.sleep(poll_interval)

        raise exceptions.KSeFApiError(
            0,
            exceptions.ExceptionCode.UNKNOWN_ERROR,
            f"Token activation polling timed out after {max_attempts} attempts",
        )
