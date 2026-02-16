import base64
from datetime import datetime
from enum import Enum, StrEnum

from pydantic import AwareDatetime, field_validator, Field

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


class QuerySessionsList(KSeFBaseParams):
    page_size: int = Field(default=10, ge=1, le=100)
    session_type: SessionType
    reference_number: str | None = None
    date_created_from: datetime | None = None
    date_created_to: datetime | None = None
    date_closed_from: datetime | None = None
    date_closed_to: datetime | None = None
    date_modified_from: datetime | None = None
    date_modified_to: datetime | None = None
    statuses: list[SessionStatus] = Field(default_factory=list)


class SessionState(KSeFBaseModel):
    reference_number: str
    aes_key: str  # base64 encoded
    iv: str  # base64 encoded
    access_token: str
    valid_until: AwareDatetime
    form_code: FormSchema

    @field_validator("form_code", mode="before")
    @classmethod
    def _coerce_form_code(cls, value):
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

    @classmethod
    def from_encoded(
        cls,
        reference_number: str,
        aes_key: bytes,
        iv: bytes,
        access_token: str,
        valid_until: AwareDatetime,
        form_code: FormSchema,
    ):
        return cls(
            reference_number=reference_number,
            aes_key=base64.b64encode(aes_key).decode(),
            iv=base64.b64encode(iv).decode(),
            access_token=access_token,
            valid_until=valid_until,
            form_code=form_code,
        )
