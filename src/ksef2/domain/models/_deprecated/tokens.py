from __future__ import annotations

from ksef2.domain.models._deprecated._base import KSeFBaseModel


class GenerateTokenResponse(KSeFBaseModel):
    """Response from ``POST /tokens``."""

    reference_number: str
    token: str


class TokenStatusResponse(KSeFBaseModel):
    """Response from ``GET /tokens/{referenceNumber}``."""

    reference_number: str
    status: str
    token: str | None = None
