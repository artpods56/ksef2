from collections.abc import Iterator
from typing import final

from ksef2.domain.models.auth import AuthenticationSessionsResponse
from ksef2.endpoints.auth import AuthEndpoints
from ksef2.core.protocols import Middleware
from ksef2.infra.mappers.auth import from_spec


@final
class SessionManagementClient:
    def __init__(self, transport: Middleware) -> None:
        self._auth_ep = AuthEndpoints(transport)

    def list_page(
        self,
        *,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> AuthenticationSessionsResponse:
        return from_spec(
            self._auth_ep.list_sessions(
                continuation_token=continuation_token,
                pageSize=page_size,
            )
        )

    def list(
        self,
        *,
        page_size: int | None = None,
    ) -> Iterator[AuthenticationSessionsResponse]:
        response = self.list_page(page_size=page_size)
        yield response

        while ct := response.continuation_token:
            response = self.list_page(page_size=page_size, continuation_token=ct)
            yield response

    def terminate_current(self) -> None:
        self._auth_ep.terminate_current_session()

    def close(self, *, reference_number: str) -> None:
        self._auth_ep.terminate_auth_session(
            reference_number=reference_number,
        )
