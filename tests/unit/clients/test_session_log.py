from polyfactory import BaseFactory

import pytest

from ksef2.clients.session_log import InvoiceSessionLogClient
from ksef2.core.routes import SessionRoutes
from ksef2.domain.models.pagination import ListSessionsQuery
from ksef2.domain.models.session import ListSessionsResponse
from ksef2.infra.schema.api import spec
from tests.unit.fakes.transport import FakeTransport


class TestInvoiceSessionLogClient:
    def test_query(
        self,
        session_log_client: InvoiceSessionLogClient,
        fake_transport: FakeTransport,
        session_list_resp: BaseFactory[spec.SessionsQueryResponse],
    ) -> None:
        response = session_list_resp.build(continuationToken=None)
        fake_transport.enqueue(response.model_dump(mode="json"))

        result = session_log_client.query(session_type="online")

        assert isinstance(result, ListSessionsResponse)
        assert fake_transport.calls[0].method == "GET"
        assert fake_transport.calls[0].path == SessionRoutes.LIST_SESSIONS
        assert dict(fake_transport.calls[0].params) == {
            "pageSize": "10",
            "sessionType": "Online",
        }

    def test_query_uses_explicit_params(
        self,
        session_log_client: InvoiceSessionLogClient,
        fake_transport: FakeTransport,
        session_list_resp: BaseFactory[spec.SessionsQueryResponse],
    ) -> None:
        fake_transport.enqueue(session_list_resp.build().model_dump(mode="json"))
        params = ListSessionsQuery(page_size=25, session_type="Online")

        _ = session_log_client.query(session_type="online", params=params)

        assert dict(fake_transport.calls[0].params) == {
            "pageSize": "25",
            "sessionType": "Online",
        }

    def test_all(
        self,
        session_log_client: InvoiceSessionLogClient,
        fake_transport: FakeTransport,
        session_list_resp: BaseFactory[spec.SessionsQueryResponse],
    ) -> None:
        fake_transport.enqueue(
            session_list_resp.build(continuationToken="next-token").model_dump(mode="json")
        )
        fake_transport.enqueue(
            session_list_resp.build(continuationToken=None).model_dump(mode="json")
        )

        results = list(session_log_client.all(session_type="online"))

        assert len(results) == 2
        assert all(isinstance(result, ListSessionsResponse) for result in results)
        assert fake_transport.calls[1].headers == {"x-continuation-token": "next-token"}

    def test_query_rejects_invalid_session_type(
        self,
        session_log_client: InvoiceSessionLogClient,
    ) -> None:
        with pytest.raises(ValueError, match="Invalid session type"):
            session_log_client.query(session_type="invalid")  # type: ignore[arg-type]
