from __future__ import annotations

from ksef_sdk.domain.models import KSeFBaseModel


class SendInvoiceResponse(KSeFBaseModel):
    """Response from ``POST /sessions/online/{ref}/invoices``."""

    reference_number: str
