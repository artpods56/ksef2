"""Mapper for Peppol API responses to domain models."""

from ksef2.domain.models.peppol import (
    PeppolProvider,
    ListPeppolProvidersResponse,
)
from ksef2.infra.schema.api import spec as spec


class PeppolProviderMapper:
    """Maps Peppol API responses to domain models."""

    @staticmethod
    def map_response(
        response: spec.QueryPeppolProvidersResponse,
    ) -> ListPeppolProvidersResponse:
        """Map query response from spec to domain model."""
        return ListPeppolProvidersResponse(
            providers=[
                PeppolProvider(
                    id=provider.id,
                    name=provider.name,
                    date_created=provider.dateCreated,
                )
                for provider in response.peppolProviders
            ],
            has_more=response.hasMore,
        )
