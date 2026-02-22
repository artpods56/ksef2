from collections.abc import Iterator
from datetime import datetime
from typing import final

from ksef2.core import protocols
from ksef2.domain.models.session import (
    ListSessionsQuery,
    ListSessionsResponse,
    SessionStatus,
    SessionType,
)
from ksef2.endpoints.session import ListSessionsEndpoint
from ksef2.infra.mappers.requests.sessions import QuerySessionsMapper


@final
class InvoiceSessionQueryService:
    def __init__(
        self,
        transport: protocols.Middleware,
        access_token: str,
    ):
        self._list_sessions_ep = ListSessionsEndpoint(transport)
        self._access_token = access_token

    def list_page(
        self,
        *,
        session_type: SessionType,
        page_size: int = 10,
        reference_number: str | None = None,
        date_created_from: datetime | None = None,
        date_created_to: datetime | None = None,
        date_closed_from: datetime | None = None,
        date_closed_to: datetime | None = None,
        date_modified_from: datetime | None = None,
        date_modified_to: datetime | None = None,
        statuses: list[SessionStatus] | None = None,
        continuation_token: str | None = None,
    ) -> ListSessionsResponse:
        query = ListSessionsQuery(
            page_size=page_size,
            session_type=session_type,
            reference_number=reference_number,
            date_created_from=date_created_from,
            date_created_to=date_created_to,
            date_closed_from=date_closed_from,
            date_closed_to=date_closed_to,
            date_modified_from=date_modified_from,
            date_modified_to=date_modified_to,
            statuses=statuses,
        )
        return QuerySessionsMapper.map_response(
            self._list_sessions_ep.send(
                access_token=self._access_token,
                continuation_token=continuation_token,
                **query.model_dump(by_alias=True, exclude_none=True),
            )
        )

    def list(
        self,
        *,
        session_type: SessionType,
        page_size: int = 10,
        reference_number: str | None = None,
        date_created_from: datetime | None = None,
        date_created_to: datetime | None = None,
        date_closed_from: datetime | None = None,
        date_closed_to: datetime | None = None,
        date_modified_from: datetime | None = None,
        date_modified_to: datetime | None = None,
        statuses: list[SessionStatus] | None = None,
    ) -> Iterator[ListSessionsResponse]:
        kwargs = dict(
            session_type=session_type,
            page_size=page_size,
            reference_number=reference_number,
            date_created_from=date_created_from,
            date_created_to=date_created_to,
            date_closed_from=date_closed_from,
            date_closed_to=date_closed_to,
            date_modified_from=date_modified_from,
            date_modified_to=date_modified_to,
            statuses=statuses,
        )

        response = self.list_page(**kwargs)
        yield response

        while continuation_token := response.continuation_token:
            response = self.list_page(**kwargs, continuation_token=continuation_token)
            yield response
