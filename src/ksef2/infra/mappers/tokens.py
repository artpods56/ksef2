from __future__ import annotations

from ksef2.domain.models.tokens import (
    GenerateTokenResponse,
    QueryTokensResponse,
    TokenAuthorIdentifier,
    TokenAuthorIdentifierType,
    TokenContextIdentifier,
    TokenContextIdentifierType,
    TokenInfo,
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
            permissions=[spec.TokenPermissionType(p.value) for p in permissions],
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


class QueryTokensMapper:
    @staticmethod
    def map_response(r: spec.QueryTokensResponse) -> QueryTokensResponse:
        return QueryTokensResponse(
            continuation_token=r.continuationToken,
            tokens=[QueryTokensMapper._map_token_info(t) for t in r.tokens],
        )

    @staticmethod
    def _map_token_info(t: spec.QueryTokensResponseItem) -> TokenInfo:
        return TokenInfo(
            reference_number=t.referenceNumber,
            author_identifier=TokenAuthorIdentifier(
                type=TokenAuthorIdentifierType(t.authorIdentifier.type.value),
                value=t.authorIdentifier.value,
            ),
            context_identifier=TokenContextIdentifier(
                type=TokenContextIdentifierType(t.contextIdentifier.type.value),
                value=t.contextIdentifier.value,
            ),
            description=t.description,
            requested_permissions=[
                TokenPermission(p.value) for p in t.requestedPermissions
            ],
            date_created=t.dateCreated,
            last_use_date=t.lastUseDate,
            status=TokenStatus(t.status.value),
            status_details=t.statusDetails,
        )
