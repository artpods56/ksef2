import time
from collections.abc import Iterator
from typing import final

from ksef2.core import exceptions
from ksef2.core.protocols import Middleware
from ksef2.domain.models.pagination import TokenListParams
from ksef2.domain.models.tokens import (
    GenerateTokenRequest,
    GenerateTokenResponse,
    QueryTokensResponse,
    TokenPermission,
    TokenStatusResponse,
)
from ksef2.endpoints.tokens import TokenEndpoints

from ksef2.infra.mappers.tokens import from_spec, to_spec


@final
class TokensClient:
    def __init__(self, transport: Middleware) -> None:
        self._endpoints = TokenEndpoints(transport)

    def generate(
        self,
        *,
        permissions: list[TokenPermission],
        description: str,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> GenerateTokenResponse:
        request = GenerateTokenRequest(
            permissions=permissions,
            description=description,
        )
        body = to_spec(request)
        spec_resp = self._endpoints.generate_token(body=body)
        result = from_spec(spec_resp)

        _ = self._poll_until_active(
            reference_number=result.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )
        return result

    def list_page(
        self,
        *,
        continuation_token: str | None = None,
        params: TokenListParams | None = None,
    ) -> QueryTokensResponse:
        parameters = params or TokenListParams()
        spec_resp = self._endpoints.list_tokens(
            continuation_token=continuation_token, **parameters.to_query_params()
        )
        return from_spec(spec_resp)

    def list_all(
        self, *, params: TokenListParams | None = None
    ) -> Iterator[QueryTokensResponse]:
        parameters = params or TokenListParams()
        response = self.list_page(params=parameters)
        yield response

        while ct := response.continuation_token:
            response = self.list_page(params=parameters, continuation_token=ct)
            yield response

    def status(
        self,
        *,
        reference_number: str,
    ) -> TokenStatusResponse:
        spec_resp = self._endpoints.token_status(reference_number=reference_number)
        return from_spec(spec_resp)

    def revoke(
        self,
        *,
        reference_number: str,
    ) -> None:
        self._endpoints.revoke_token(reference_number=reference_number)

    def _poll_until_active(
        self,
        *,
        reference_number: str,
        poll_interval: float,
        max_attempts: int,
    ) -> TokenStatusResponse:
        for _ in range(max_attempts):
            result = self.status(reference_number=reference_number)
            if result.status == "active":
                return result
            if result.status in ("failed", "revoked"):
                raise exceptions.KSeFApiError(
                    0,
                    exceptions.ExceptionCode.UNKNOWN_ERROR,
                    f"Token activation failed: status={result.status}",
                )
            time.sleep(poll_interval)

        raise exceptions.KSeFApiError(
            0,
            exceptions.ExceptionCode.UNKNOWN_ERROR,
            f"Token activation polling timed out after {max_attempts} attempts",
        )
