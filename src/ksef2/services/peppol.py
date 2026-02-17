"""Peppol service for querying Peppol service providers."""

from typing import final

from ksef2.core import protocols
from ksef2.domain.models.peppol import QueryPeppolProvidersResponse
from ksef2.endpoints.peppol import QueryPeppolProvidersEndpoint
from ksef2.infra.mappers.peppol import PeppolProviderMapper


@final
class PeppolService:
    """Service for querying Peppol service providers.

    This service provides access to the list of Peppol service providers
    registered in the KSeF system. All endpoints in this service are
    public and do not require authentication.
    """

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport
        self._query_endpoint = QueryPeppolProvidersEndpoint(transport)

    def query(
        self,
        *,
        page_offset: int = 0,
        page_size: int = 10,
    ) -> QueryPeppolProvidersResponse:
        """Query Peppol service providers.

        Args:
            page_offset: Page number (0-indexed). Defaults to 0.
            page_size: Number of results per page (10-100). Defaults to 10.

        Returns:
            QueryPeppolProvidersResponse containing the list of providers
            and pagination info.
        """
        response = self._query_endpoint.send(
            page_offset=page_offset,
            page_size=page_size,
        )
        return PeppolProviderMapper.map_response(response)
