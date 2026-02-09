from __future__ import annotations

from ksef_sdk.domain.models._deprecated._base import KSeFBaseModel


class ContextLimits(KSeFBaseModel):
    """Limits for the current authentication context."""

    max_invoices_per_session: int | None = None
    max_sessions: int | None = None


class ApiRateLimits(KSeFBaseModel):
    """API rate limit information."""

    requests_per_minute: int | None = None
    requests_remaining: int | None = None
