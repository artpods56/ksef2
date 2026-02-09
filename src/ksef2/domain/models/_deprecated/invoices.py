from __future__ import annotations

from datetime import datetime

from ksef2.domain.models._deprecated._base import KSeFBaseModel


class InvoiceQueryFilters(KSeFBaseModel):
    """Filters for querying invoice metadata."""

    date_from: datetime | None = None
    date_to: datetime | None = None
    subject_nip: str | None = None
    invoice_type: str | None = None


class InvoiceQueryRequest(KSeFBaseModel):
    """Request body for invoice metadata queries."""

    filters: InvoiceQueryFilters


class InvoiceMetadata(KSeFBaseModel):
    """Metadata for a single invoice returned by query."""

    ksef_number: str
    subject_nip: str | None = None
    invoice_date: datetime | None = None
    gross_value: str | None = None
    invoice_type: str | None = None


class InvoiceMetadataResponse(KSeFBaseModel):
    """Response from invoice metadata query."""

    invoices: list[InvoiceMetadata]
    continuation_token: str | None = None
