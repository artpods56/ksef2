from __future__ import annotations

import time
from typing import Sequence

from ksef2.clients._deprecated._base import BaseSubClient
from ksef2.core.exceptions import KSeFApiError
from ksef2.domain.models._deprecated.tokens import (
    GenerateTokenResponse,
    TokenStatusResponse,
)
from ksef2.infra.mappers._deprecated.tokens import (
    GenerateTokenMapper,
    TokenStatusMapper,
)
from ksef2.infra.schema.model import (
    GenerateTokenResponse as SpecGenerateTokenResponse,
    TokenStatusResponse as SpecTokenStatusResponse,
)


class TokensClient(BaseSubClient):
    """Sub-client for KSeF token management."""

    def generate(
        self,
        access_token: str,
        permissions: Sequence[str],
        description: str,
        *,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> GenerateTokenResponse:
        """Generate a new KSeF token and wait for it to become active."""
        body = GenerateTokenMapper.map_request(permissions, description)
        spec_resp = self._http.post(
            "/tokens",
            body=body,
            response_model=SpecGenerateTokenResponse,
            token=access_token,
        )
        domain_resp = GenerateTokenMapper.map_response(spec_resp)

        self._poll_status(
            access_token,
            domain_resp.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )
        return domain_resp

    def status(self, access_token: str, reference_number: str) -> TokenStatusResponse:
        """``GET /tokens/{referenceNumber}``"""
        spec_resp = self._http.get(
            f"/tokens/{reference_number}",
            response_model=SpecTokenStatusResponse,
            token=access_token,
        )
        return TokenStatusMapper.map_response(spec_resp)

    def revoke(self, access_token: str, reference_number: str) -> None:
        """``DELETE /tokens/{referenceNumber}``"""
        self._http.delete(
            f"/tokens/{reference_number}",
            token=access_token,
        )

    def _poll_status(
        self,
        access_token: str,
        reference_number: str,
        *,
        poll_interval: float = 1.0,
        max_attempts: int = 60,
    ) -> TokenStatusResponse:
        for _ in range(max_attempts):
            result = self.status(access_token, reference_number)
            if result.status == "Active":
                return result
            if result.status in ("Failed", "Revoked"):
                raise KSeFApiError(
                    0, f"Token activation failed: status={result.status}"
                )
            time.sleep(poll_interval)

        raise KSeFApiError(
            0, f"Token activation polling timed out after {max_attempts} attempts"
        )
