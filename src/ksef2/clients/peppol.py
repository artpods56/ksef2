from collections.abc import Iterator
from typing import final

from ksef2.core import protocols
from ksef2.domain.models.pagination import PaginationParams
from ksef2.domain.models.peppol import ListPeppolProvidersResponse, PeppolProvider
from ksef2.endpoints.peppol import QueryPeppolProvidersEndpoint
from ksef2.infra.mappers.requests.peppol import PeppolProviderMapper


@final
class PeppolClient:
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
        params: PaginationParams | None = None,
    ) -> ListPeppolProvidersResponse:
        """Query Peppol service providers.

        Args:
            params: Pagination parameters.

        Returns:
            QueryPeppolProvidersResponse containing the list of providers
            and pagination info.
        """
        params = params or PaginationParams()

        response = self._query_endpoint.send(
            **params.to_api_params()
        )
        return PeppolProviderMapper.map_response(response)



    def all(self, *, params: PaginationParams | None = None) -> Iterator[PeppolProvider]:
        """Iterate over all Peppol service providers.

        This method handles pagination internally.

        Args:
            params: Pagination parameters.

        Returns:
            Iterator over PeppolProvider objects.
        """
        current_params = params or PaginationParams()

        while True:
            response = self.query(params=current_params)
            yield from response.providers
            
            if not response.has_more:
                break

            current_params = current_params.next_page()
            
