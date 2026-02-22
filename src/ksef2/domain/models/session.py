from __future__ import annotations

import base64
from datetime import datetime
from enum import Enum, StrEnum
from typing import Self

from pydantic import AwareDatetime, Field, field_validator

from ksef2.domain.models.base import KSeFBaseModel, KSeFBaseParams


class FormSchema(Enum):
    """Supported form schemas for online sessions."""

    FA2 = ("FA (2)", "1-0E", "FA")
    FA3 = ("FA (3)", "1-0E", "FA")
    PEF3 = ("PEF (3)", "2-1", "PEF")
    PEF_KOR3 = ("PEF_KOR (3)", "2-1", "PEF")

    def __init__(self, system_code: str, schema_version: str, schema_value: str):
        self.system_code = system_code
        self.schema_version = schema_version
        self.schema_value = schema_value


class SessionType(StrEnum):
    ONLINE = "Online"
    BATCH = "Batch"


class SessionStatus(StrEnum):
    IN_PROGRESS = "InProgress"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class ListSessionsQuery(KSeFBaseParams):
    page_size: int = Field(default=10, ge=1, le=100)
    session_type: SessionType
    reference_number: str | None = None
    date_created_from: datetime | None = None
    date_created_to: datetime | None = None
    date_closed_from: datetime | None = None
    date_closed_to: datetime | None = None
    date_modified_from: datetime | None = None
    date_modified_to: datetime | None = None
    statuses: list[SessionStatus] | None = None


class StatusInfo(KSeFBaseModel):
    code: int
    description: str
    details: list[str] | None = None


class SessionSummary(KSeFBaseModel):
    reference_number: str
    status: StatusInfo
    date_created: AwareDatetime
    date_updated: AwareDatetime
    valid_until: AwareDatetime | None = None
    total_invoice_count: int
    successful_invoice_count: int
    failed_invoice_count: int


class ListSessionsResponse(KSeFBaseModel):
    continuation_token: str | None = None
    sessions: list[SessionSummary]


class BaseSessionState(KSeFBaseModel):
    """Base class for session state with common fields.

    This class contains fields shared between online and batch sessions.
    It provides serialization/deserialization support and helper methods
    for accessing the encryption keys.
    """

    reference_number: str
    """Reference number of the session."""

    aes_key: str
    """AES key for encrypting data, Base64 encoded."""

    iv: str
    """Initialization vector for AES encryption, Base64 encoded."""

    access_token: str
    """Bearer token for API authentication."""

    form_code: FormSchema
    """Invoice schema used for this session."""

    @field_validator("form_code", mode="before")
    @classmethod
    def _coerce_form_code(cls, value: list[str] | tuple[str, ...]) -> object:
        """
        Pydantic serializes Enum values that are tuples as JSON arrays (lists).
        On restore, convert list -> tuple so Enum validation succeeds.
        Also accept enum names as a convenience ("FA3", etc.).
        """
        if isinstance(value, list):
            return tuple(value)
        if isinstance(value, str):
            try:
                return FormSchema[value]
            except KeyError:
                return value
        return value

    def get_aes_key_bytes(self) -> bytes:
        """Get the AES key as raw bytes."""
        return base64.b64decode(self.aes_key)

    def get_iv_bytes(self) -> bytes:
        """Get the initialization vector as raw bytes."""
        return base64.b64decode(self.iv)


class OnlineSessionState(BaseSessionState):
    """Serializable state of an online session.

    This class holds all information needed to resume an online session.
    Can be serialized to JSON for persistence.
    """

    valid_until: AwareDatetime
    """Expiration time of the session."""

    @classmethod
    def from_encoded(
        cls,
        reference_number: str,
        aes_key: bytes,
        iv: bytes,
        access_token: str,
        valid_until: AwareDatetime,
        form_code: FormSchema,
    ) -> Self:
        """Create state from raw bytes (aes_key, iv).

        Args:
            reference_number: Session reference number.
            aes_key: Raw AES key bytes.
            iv: Raw initialization vector bytes.
            access_token: Bearer token for authentication.
            valid_until: Session expiration time.
            form_code: Invoice schema for this session.

        Returns:
            SessionState with Base64-encoded key and IV.
        """
        return cls(
            reference_number=reference_number,
            aes_key=base64.b64encode(aes_key).decode(),
            iv=base64.b64encode(iv).decode(),
            access_token=access_token,
            valid_until=valid_until,
            form_code=form_code,
        )
