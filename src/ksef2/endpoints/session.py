"""Session management endpoints."""

from typing import Literal, NotRequired, TypedDict, Unpack, final

from pydantic import TypeAdapter

from ksef2.core import routes
from ksef2.endpoints.base import BaseEndpoints
from ksef2.infra.schema.api import spec
from ksef2.infra.schema.api.supp.batch import OpenBatchSessionRequest
from ksef2.infra.schema.api.supp.session import OpenOnlineSessionRequest

ListSessionsQueryParams = TypedDict(
    "ListSessionsQueryParams",
    {
        "pageSize": NotRequired[int | None],
        "sessionType": Literal["Online", "Batch"],
        "referenceNumber": NotRequired[str | None],
        "dateCreatedFrom": NotRequired[str | None],
        "dateCreatedTo": NotRequired[str | None],
        "dateClosedFrom": NotRequired[str | None],
        "dateClosedTo": NotRequired[str | None],
        "dateModifiedFrom": NotRequired[str | None],
        "dateModifiedTo": NotRequired[str | None],
        "statuses": NotRequired[
            list[Literal["InProgress", "Succeeded", "Failed", "Cancelled"]] | None
        ],
    },
)
_LIST_SESSIONS_PARAMS = TypeAdapter(ListSessionsQueryParams)


@final
class SessionEndpoints(BaseEndpoints):
    def open_online(
        self, body: OpenOnlineSessionRequest
    ) -> spec.OpenOnlineSessionResponse:
        return self._parse(
            self._transport.post(
                path=routes.SessionRoutes.OPEN_ONLINE,
                json=body.model_dump(mode="json", by_alias=True),
            ),
            spec.OpenOnlineSessionResponse,
        )

    def terminate_online(self, reference_number: str) -> None:
        _ = self._transport.post(
            path=routes.SessionRoutes.TERMINATE_ONLINE.format(
                referenceNumber=reference_number
            ),
        )

    def open_batch(
        self, body: OpenBatchSessionRequest
    ) -> spec.OpenBatchSessionResponse:
        return self._parse(
            self._transport.post(
                path=routes.SessionRoutes.OPEN_BATCH,
                json=body.model_dump(mode="json", by_alias=True),
            ),
            spec.OpenBatchSessionResponse,
        )

    def close_batch(self, reference_number: str) -> None:
        _ = self._transport.post(
            path=routes.SessionRoutes.CLOSE_BATCH.format(
                referenceNumber=reference_number
            ),
        )

    def get_session_upo(
        self,
        reference_number: str,
        upo_reference_number: str,
    ) -> bytes:
        return self._transport.get(
            path=routes.SessionRoutes.GET_SESSION_UPO.format(
                referenceNumber=reference_number,
                upoReferenceNumber=upo_reference_number,
            ),
        ).content

    def list_sessions(
        self,
        continuation_token: str | None = None,
        **params: Unpack[ListSessionsQueryParams],
    ) -> spec.SessionsQueryResponse:
        headers = (
            {"x-continuation-token": continuation_token} if continuation_token else None
        )

        return self._parse(
            self._transport.get(
                path=routes.SessionRoutes.LIST_SESSIONS,
                params=self.build_params(params, _LIST_SESSIONS_PARAMS),
                headers=headers,
            ),
            spec.SessionsQueryResponse,
        )
