from collections.abc import Iterator
from typing import final

from ksef2.core.protocols import Middleware
from ksef2.domain.models.pagination import OffsetPaginationParams
from ksef2.domain.models.peppol import ListPeppolProvidersResponse, PeppolProvider
from ksef2.endpoints.peppol import PeppolEndpoints
from ksef2.infra.mappers.peppol import from_spec


@final
class PeppolClient:
    """Service for querying Peppol service providers.

    This service provides access to the list of Peppol service providers
    registered in the KSeF system. All endpoints in this service are
    public and do not require authentication.
    """

    def __init__(self, transport: Middleware):
        self._transport = transport
        self._endpoints = PeppolEndpoints(transport)

    def query(
        self,
        *,
        params: OffsetPaginationParams | None = None,
    ) -> ListPeppolProvidersResponse:
        """Query Peppol service providers.

        Args:
            params: Pagination parameters.

        Returns:
            QueryPeppolProvidersResponse containing the list of providers
            and pagination info.
        """
        params = params or OffsetPaginationParams()

        response = self._endpoints.query_providers(**params.to_query_params())
        return from_spec(response)

    def all(
        self, *, params: OffsetPaginationParams | None = None
    ) -> Iterator[PeppolProvider]:
        """Iterate over all Peppol service providers.

        This method handles pagination internally.

        Args:
            params: Pagination parameters.

        Returns:
            Iterator over PeppolProvider objects.
        """
        current_params = params or OffsetPaginationParams()

        while True:
            response = self.query(params=current_params)
            yield from response.providers

            if not response.has_more:
                break

            current_params = current_params.next_page()
