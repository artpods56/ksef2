from enum import Enum

from pydantic import AwareDatetime

from ksef2.domain.models import KSeFBaseModel


class CertUsage(Enum):
    KSEF_TOKEN_ENCRYPTION = "KsefTokenEncryption"
    SYMMETRIC_KEY_ENCRYPTION = "SymmetricKeyEncryption"


class PublicKeyCertificate(KSeFBaseModel):
    certificate: str
    valid_from: AwareDatetime
    valid_to: AwareDatetime
    usage: list[CertUsage]
