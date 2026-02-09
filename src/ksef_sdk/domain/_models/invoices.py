"""
Defines enums and models related to KSeF online sessions and session statuses.

This module contains the `FormSchema` enum for supported form schemas in online sessions and the 
`SessionStatus` model for tracking the status of an open KSeF session. These components enable handling 
of session data and its validation.

Classes:
    - FormSchema: Enum representing supported form schemas for online sessions.
    - SessionStatus: Model representing the status of an open KSeF session.
    
Documentation:

"""
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import field_validator

from ksef_sdk.domain.models import KSeFBaseModel

class FormSchema(Enum):
    """Supported form schemas for online sessions.

    Documentation:
        `https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Wysylka-interaktywna/paths/~1sessions~1online/post`
    """

    FA2 = ("FA (2)", "1-0E", "FA")
    FA3 = ("FA (3)", "1-0E", "FA")
    PEF3 = ("PEF (3)", "2-1", "PEF")
    PEF_KOR3 = ("PEF_KOR (3)", "2-1", "PEF")

    def __init__(self, system_code: str, schema_version: str, schema_value: str):
        self.system_code = system_code
        self.schema_version = schema_version
        self.schema_value = schema_value

class SessionStatus(KSeFBaseModel):
    """Status of an open KSeF session.

    Allows for rehydration of a session from its reference number and timestamp.

    Documentation:


    """

    reference_number: str
    timestamp: datetime

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_ksef_timestamp(cls, v: Any) -> datetime:
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v



