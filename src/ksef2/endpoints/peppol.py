"""Peppol endpoints for querying Peppol service providers."""

from typing import final, TypedDict, NotRequired
from urllib.parse import urlencode

from pydantic import TypeAdapter

from ksef2.core import codecs, protocols
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

    def send(
        self,
        *,
        page_offset: int | None = None,
        page_size: int | None = None,
    ) -> spec.QueryPeppolProvidersResponse:
        params: QueryPeppolProvidersQueryParams = {
            "pageOffset": page_offset,
            "pageSize": page_size,
        }
        valid_params = self._adapter.validate_python(params)
        # Filter out None values
        filtered_params = {k: v for k, v in valid_params.items() if v is not None}
        query_string = urlencode(filtered_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path),
            spec.QueryPeppolProvidersResponse,
        )
