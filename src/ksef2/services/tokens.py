from __future__ import annotations

import time
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
from ksef2.infra.mappers.tokens import (
    GenerateTokenMapper,
    QueryTokensMapper,
    TokenStatusMapper,
)


@final
class TokenService:
    def __init__(self, transport: protocols.Middleware) -> None:
        self._generate_ep = GenerateTokenEndpoint(transport)
        self._list_ep = ListTokensEndpoint(transport)
        self._status_ep = TokenStatusEndpoint(transport)
        self._revoke_ep = RevokeTokenEndpoint(transport)

    def generate(
        self,
        *,
        access_token: str,
        permissions: list[TokenPermission],
        description: str,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> GenerateTokenResponse:
        body = GenerateTokenMapper.map_request(permissions, description)
        spec_resp = self._generate_ep.send(
            access_token=access_token,
            body=body.model_dump(),
        )
        result = GenerateTokenMapper.map_response(spec_resp)

        _ = self._poll_until_active(
            access_token=access_token,
            reference_number=result.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )
        return result

    def list(
        self,
        *,
        access_token: str,
        status: list[TokenStatus] | None = None,
        description: str | None = None,
        author_filter: TokenAuthorIdentifier | None = None,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> QueryTokensResponse:
        spec_resp = self._list_ep.send(
            access_token=access_token,
            status=[s.value for s in status] if status else None,
            description=description,
            author_identifier=author_filter.value if author_filter else None,
            author_identifier_type=author_filter.type.value if author_filter else None,
            page_size=page_size,
            continuation_token=continuation_token,
        )
        return QueryTokensMapper.map_response(spec_resp)

    def status(
        self,
        *,
        access_token: str,
        reference_number: str,
    ) -> TokenStatusResponse:
        spec_resp = self._status_ep.send(
            access_token=access_token,
            reference_number=reference_number,
        )
        return TokenStatusMapper.map_response(spec_resp)

    def revoke(
        self,
        *,
        access_token: str,
        reference_number: str,
    ) -> None:
        self._revoke_ep.send(
            access_token=access_token,
            reference_number=reference_number,
        )

    def _poll_until_active(
        self,
        *,
        access_token: str,
        reference_number: str,
        poll_interval: float,
        max_attempts: int,
    ) -> TokenStatusResponse:
        for _ in range(max_attempts):
            result = self.status(
                access_token=access_token,
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
