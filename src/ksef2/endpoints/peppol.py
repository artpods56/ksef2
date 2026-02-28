"""Peppol endpoints for querying Peppol service providers."""

from typing import final, Unpack

from ksef2.core import routes
from ksef2.endpoints.base import OffsetPaginationQueryParams
from ksef2.endpoints.base import BaseEndpoints
from ksef2.infra.schema.api import spec


@final
class PeppolEndpoints(BaseEndpoints):
    def query_providers(
        self,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryPeppolProvidersResponse:
        return self._parse(
            self._transport.get(
                path=routes.PeppolRoutes.QUERY_PROVIDERS,
                params=self.build_params(params),
            ),
            spec.QueryPeppolProvidersResponse,
        )
