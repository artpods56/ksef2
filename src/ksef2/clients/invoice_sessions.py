from collections.abc import Iterator
from typing import final

from ksef2.core.protocols import Middleware
from ksef2.domain.models.pagination import ListSessionsQuery
from ksef2.domain.models.session import ListSessionsResponse, SessionTypeEnum
from ksef2.endpoints.session import SessionEndpoints
from ksef2.infra.mappers.sessions import from_spec


@final
class InvoiceSessionsClient:
    """Browse historical online and batch invoice sessions.

    This client wraps the ``/sessions`` history endpoint for invoice-processing
    sessions. It does not manage authentication sessions from ``/auth/sessions``.
    """

    def __init__(self, transport: Middleware) -> None:
        self._endpoints = SessionEndpoints(transport)

    @staticmethod
    def _coerce_session_type(session_type: str) -> SessionTypeEnum:
        """Normalize user-friendly session type strings into enum values."""
        try:
            return SessionTypeEnum[session_type.upper()]
        except KeyError as exc:
            raise ValueError(
                f"Invalid session type: {session_type}. "
                f"Valid session types are: {', '.join(SessionTypeEnum.__members__)}"
            ) from exc

    def query(
        self,
        *,
        session_type: str,
        continuation_token: str | None = None,
        params: ListSessionsQuery | None = None,
        statuses: list[str] | None = None,
    ) -> ListSessionsResponse:
        """Fetch one page of invoice session history for the chosen session type.

        Args:
            session_type: Invoice session family to browse, such as ``"online"``
                or ``"batch"``.
            continuation_token: Cursor returned by a previous page.
            params: Optional query object with pagination and filter settings.
            statuses: Optional list of status filters applied on top of ``params``.

        Returns:
            One page of historical invoice sessions.
        """
        parameters = params or ListSessionsQuery(
            session_type=self._coerce_session_type(session_type),
        )
        if statuses is not None:
            parameters = parameters.model_copy(update={"statuses": list(statuses)})

        return from_spec(
            self._endpoints.list_sessions(
                continuation_token=continuation_token,
                **parameters.to_query_params(),
            )
        )

    def all(
        self,
        *,
        session_type: str,
        params: ListSessionsQuery | None = None,
    ) -> Iterator[ListSessionsResponse]:
        """Iterate through all pages of invoice session history.

        Args:
            session_type: Invoice session family to browse, such as ``"online"``
                or ``"batch"``.
            params: Optional query object with pagination and filter settings.

        Yields:
            Successive pages of historical invoice sessions until KSeF stops
            returning a continuation token.
        """
        parameters = params or ListSessionsQuery(
            session_type=self._coerce_session_type(session_type),
        )

        response = self.query(
            session_type=session_type,
            params=parameters,
        )
        yield response

        while continuation_token := response.continuation_token:
            response = self.query(
                session_type=session_type,
                continuation_token=continuation_token,
                params=parameters,
            )
            yield response
