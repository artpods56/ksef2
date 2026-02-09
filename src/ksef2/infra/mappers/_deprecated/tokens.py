from __future__ import annotations

from typing import Sequence

from ksef2.domain.models._deprecated.tokens import (
    GenerateTokenResponse,
    TokenStatusResponse,
)
from ksef2.infra.schema import model as spec


class GenerateTokenMapper:
    @staticmethod
    def map_request(
        permissions: Sequence[str],
        description: str,
    ) -> spec.GenerateTokenRequest:
        return spec.GenerateTokenRequest(
            permissions=list(permissions),
            description=description,
        )

    @staticmethod
    def map_response(r: spec.GenerateTokenResponse) -> GenerateTokenResponse:
        return GenerateTokenResponse(
            reference_number=r.referenceNumber,
            token=r.token,
        )


class TokenStatusMapper:
    @staticmethod
    def map_response(r: spec.TokenStatusResponse) -> TokenStatusResponse:
        return TokenStatusResponse(
            reference_number=r.referenceNumber,
            status=r.status,
            token=None,  # spec TokenStatusResponse doesn't expose the token value
        )
