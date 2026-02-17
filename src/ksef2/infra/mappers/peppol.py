"""Mapper for Peppol API responses to domain models."""

from ksef2.domain.models.peppol import (
    PeppolProvider,
    QueryPeppolProvidersResponse,
)
from ksef2.infra.schema.api import spec as spec


class PeppolProviderMapper:
    """Maps Peppol API responses to domain models."""

    @staticmethod
    def map_provider(provider: spec.PeppolProvider) -> PeppolProvider:
        """Map a single Peppol provider from spec to domain model."""
        return PeppolProvider(
            id=provider.id,
            name=provider.name,
            date_created=provider.dateCreated,
        )

    @staticmethod
    def map_response(
        response: spec.QueryPeppolProvidersResponse,
    ) -> QueryPeppolProvidersResponse:
        """Map query response from spec to domain model."""
        return QueryPeppolProvidersResponse(
            providers=[
                PeppolProviderMapper.map_provider(p) for p in response.peppolProviders
            ],
            has_more=response.hasMore,
        )
