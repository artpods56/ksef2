from __future__ import annotations

from typing import Literal

from ksef2.domain.models._deprecated._base import KSeFBaseModel


class StatusInfo(KSeFBaseModel):
    """Common status object returned by many KSeF endpoints."""

    code: int
    description: str | None = None


# Type aliases for clarity
SubjectType = Literal["EnforcementAuthority", "VatGroup", "JST"]
IdentifierType = Literal["Nip", "Pesel", "Fingerprint"]
DateType = str  # ISO-8601 date string
InvoiceType = Literal["FA", "PEF", "PEF_KOR"]
