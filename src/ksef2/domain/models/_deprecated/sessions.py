from __future__ import annotations

from datetime import datetime

from pydantic import AwareDatetime

from ksef2.domain.models._deprecated._base import KSeFBaseModel


class OpenOnlineSessionResponse(KSeFBaseModel):
    """Response from ``POST /sessions/online``."""

    reference_number: str
    valid_until: AwareDatetime


class OpenBatchSessionResponse(KSeFBaseModel):
    """Response from ``POST /sessions/batch``."""

    reference_number: str
    parts: list[PartUploadRequest]


class PartUploadRequest(KSeFBaseModel):
    """Upload endpoint info for a batch session part."""

    ordinal_number: int
    method: str
    url: str
    headers: dict[str, str]


class SessionStatus(KSeFBaseModel):
    """Response from ``GET /sessions/{referenceNumber}``."""

    status_code: int
    status_description: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    valid_until: datetime | None = None


class SessionInvoiceStatus(KSeFBaseModel):
    """Status of a single invoice within a session."""

    reference_number: str
    ksef_number: str | None = None
    status_code: int
    status_description: str | None = None


class SessionInvoicesResponse(KSeFBaseModel):
    """Response from ``GET /sessions/{referenceNumber}/invoices``."""

    invoices: list[SessionInvoiceStatus]
    continuation_token: str | None = None


class SessionListResponse(KSeFBaseModel):
    """Response from listing active sessions."""

    sessions: list[SessionStatus]


class UpoInfo(KSeFBaseModel):
    """UPO (Official Proof of Receipt) metadata."""

    reference_number: str
    upo_reference: str | None = None
