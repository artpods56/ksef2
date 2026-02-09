from __future__ import annotations

from ksef2.domain.models import KSeFBaseModel


class SendInvoiceResponse(KSeFBaseModel):
    """Response from ``POST /sessions/online/{ref}/invoices``."""

    reference_number: str
