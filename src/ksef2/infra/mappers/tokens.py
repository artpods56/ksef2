from __future__ import annotations

from ksef2.domain.models.tokens import (
    GenerateTokenResponse,
    TokenPermission,
    TokenStatus,
    TokenStatusResponse,
)
from ksef2.infra.schema.api import spec as spec


class GenerateTokenMapper:
    @staticmethod
    def map_request(
        permissions: list[TokenPermission],
        description: str,
    ) -> spec.GenerateTokenRequest:
        return spec.GenerateTokenRequest(
            permissions=[p.value for p in permissions],
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
            status=TokenStatus(r.status),
        )
