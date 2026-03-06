"""Token endpoints for managing access tokens."""

from typing import NotRequired, TypedDict, Unpack, final

from pydantic import TypeAdapter

from ksef2.core import routes
from ksef2.endpoints.base import BaseEndpoints
from ksef2.infra.schema.api import spec

ListTokensQueryParams = TypedDict(
    "ListTokensQueryParams",
    {
        "status": NotRequired[list[str] | None],
        "description": NotRequired[str | None],
        "authorIdentifier": NotRequired[str | None],
        "authorIdentifierType": NotRequired[str | None],
        "pageSize": NotRequired[int | None],
    },
)
_LIST_TOKENS_PARAMS = TypeAdapter(ListTokensQueryParams)


@final
class TokenEndpoints(BaseEndpoints):
    def generate_token(
        self, body: spec.GenerateTokenRequest
    ) -> spec.GenerateTokenResponse:
        return self._parse(
            self._transport.post(
                path=routes.TokenRoutes.GENERATE_TOKEN,
                json=body.model_dump(mode="json", by_alias=True),
            ),
            spec.GenerateTokenResponse,
        )

    def list_tokens(
        self,
        continuation_token: str | None = None,
        **params: Unpack[ListTokensQueryParams],
    ) -> spec.QueryTokensResponse:
        headers = (
            {"x-continuation-token": continuation_token} if continuation_token else None
        )

        return self._parse(
            self._transport.get(
                path=routes.TokenRoutes.LIST_TOKENS,
                params=self.build_params(params, _LIST_TOKENS_PARAMS),
                headers=headers,
            ),
            spec.QueryTokensResponse,
        )

    def token_status(self, reference_number: str) -> spec.TokenStatusResponse:
        return self._parse(
            self._transport.get(
                path=routes.TokenRoutes.TOKEN_STATUS.format(
                    referenceNumber=reference_number
                ),
            ),
            spec.TokenStatusResponse,
        )

    def revoke_token(self, reference_number: str) -> None:
        self._transport.delete(
            path=routes.TokenRoutes.REVOKE_TOKEN.format(
                referenceNumber=reference_number
            ),
        )
