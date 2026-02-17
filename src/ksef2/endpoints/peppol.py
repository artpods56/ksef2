"""Peppol endpoints for querying Peppol service providers."""

from typing import final, TypedDict, NotRequired, Unpack, Any
from urllib.parse import urlencode

from pydantic import TypeAdapter

from ksef2.core import codecs, protocols
from ksef2.domain.models.pagination import PaginationQueryParams
from ksef2.infra.schema.api import spec as spec


QueryPeppolProvidersQueryParams = TypedDict(
    "QueryPeppolProvidersQueryParams",
    {
        "pageOffset": NotRequired[int | None],
        "pageSize": NotRequired[int | None],
    },
)


@final
class QueryPeppolProvidersEndpoint:
    """Endpoint for querying Peppol service providers.

    This endpoint is public and does not require authentication.
    """

    url: str = "/peppol/query"

    _adapter = TypeAdapter(QueryPeppolProvidersQueryParams)

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, params: dict[str, Any]) -> str:
        return f"{self.url}?{urlencode(params)}"

    def send(
        self, **params: Unpack[PaginationQueryParams]
    ) -> spec.QueryPeppolProvidersResponse:
        path = self.get_url({**self._adapter.validate_python(params)})

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path),
            spec.QueryPeppolProvidersResponse,
        )
