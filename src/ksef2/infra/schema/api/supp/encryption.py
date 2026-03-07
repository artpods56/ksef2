from pydantic import AwareDatetime

from ksef2.infra.schema.api.spec.models import PublicKeyCertificateUsage
from ksef2.infra.schema.api.supp.base import BaseSupp


class PublicKeyCertificate(BaseSupp):
    """Supplementary response with raw Base64 string instead of Base64Str decoding."""

    certificate: str
    validFrom: AwareDatetime
    validTo: AwareDatetime
    usage: list[PublicKeyCertificateUsage]
