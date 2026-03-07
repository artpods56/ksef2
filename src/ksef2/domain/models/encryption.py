"""Domain models for public encryption certificates exposed by KSeF."""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from ksef2.domain.models.base import KSeFBaseModel

type CertUsageValue = Literal["ksef_token_encryption", "symmetric_key_encryption"]


class CertUsageEnum(StrEnum):
    KSEF_TOKEN_ENCRYPTION = "ksef_token_encryption"
    SYMMETRIC_KEY_ENCRYPTION = "symmetric_key_encryption"


CertUsage = CertUsageEnum


class PublicKeyCertificate(KSeFBaseModel):
    """Public certificate that can encrypt tokens or session keys for KSeF."""

    certificate: str
    valid_from: datetime
    valid_to: datetime
    usage: list[CertUsage]
