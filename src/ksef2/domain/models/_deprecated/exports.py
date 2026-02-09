from __future__ import annotations

from datetime import datetime

from ksef2.domain.models._deprecated._base import KSeFBaseModel


class ExportResponse(KSeFBaseModel):
    """Response from starting an export."""

    reference_number: str


class ExportStatusResponse(KSeFBaseModel):
    """Response from polling export status."""

    reference_number: str
    status: str
    finished_at: datetime | None = None


class ExportPackage(KSeFBaseModel):
    """Metadata for an export package ready for download."""

    reference_number: str
    url: str | None = None
