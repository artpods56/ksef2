from enum import Enum

from pydantic import AwareDatetime
from ksef2.domain.models.base import KSeFBaseModel


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


class SessionState(KSeFBaseModel):
    reference_number: str
    aes_key: bytes
    iv: bytes
    access_token: str
    valid_until: AwareDatetime
    form_code: FormSchema
