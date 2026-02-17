"""Peppol service for querying Peppol service providers."""

from typing import final

from ksef2.core import protocols
from ksef2.domain.models.pagination import PaginationParams
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

    def query_providers(
        self,
        *,
        params: PaginationParams | None = None,
    ) -> QueryPeppolProvidersResponse:
        """Query Peppol service providers.

        Args:
            params: Pagination parameters.

        Returns:
            QueryPeppolProvidersResponse containing the list of providers
            and pagination info.
        """
        response = self._query_endpoint.send(
            **params.to_api_params() if params else PaginationParams().to_api_params()
        )
        return PeppolProviderMapper.map_response(response)
