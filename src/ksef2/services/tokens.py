from __future__ import annotations

import time
from typing import final

from ksef2.core import exceptions
from ksef2.core import middleware
from ksef2.domain.models.tokens import (
    GenerateTokenResponse,
    TokenPermission,
    TokenStatus,
    TokenStatusResponse,
)
from ksef2.endpoints.tokens import (
    GenerateTokenEndpoint,
    RevokeTokenEndpoint,
    TokenStatusEndpoint,
)
from ksef2.infra.mappers.tokens import GenerateTokenMapper, TokenStatusMapper


@final
class TokenService:
    def __init__(self, transport: middleware.KSeFProtocol) -> None:
        self._generate_ep = GenerateTokenEndpoint(transport)
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
                    f"Token activation failed: status={result.status.value}",
                )
            time.sleep(poll_interval)

        raise exceptions.KSeFApiError(
            0,
            f"Token activation polling timed out after {max_attempts} attempts",
        )
