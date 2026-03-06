from enum import Enum
from functools import singledispatch
from typing import assert_never, overload

from pydantic import BaseModel

from ksef2.domain.models.encryption import CertUsage, CertUsageEnum
from ksef2.infra.mappers.helpers import get_matching_enum
from ksef2.infra.schema.api import spec


class ValidEncryptionEnums(Enum):
    CertUsage = CertUsageEnum


VALID_ENCRYPTION_ENUMS = [v.value for v in ValidEncryptionEnums.__members__.values()]


@overload
def to_spec(request: CertUsage) -> spec.PublicKeyCertificateUsage: ...


def to_spec(request: BaseModel | Enum | str) -> object:
    if isinstance(request, str):
        enum_cls = get_matching_enum(request, VALID_ENCRYPTION_ENUMS)
        if enum_cls is None:
            raise NotImplementedError(f"No mapper for string value: {request!r}")
        return _to_spec(enum_cls(request))
    return _to_spec(request)


@singledispatch
def _to_spec(request: BaseModel | Enum | str) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(request).__name__}. "
        f"Register one with @_to_spec.register"
    )


@_to_spec.register
def _(request: CertUsageEnum) -> spec.PublicKeyCertificateUsage:
    match request:
        case CertUsageEnum.KSEF_TOKEN_ENCRYPTION:
            return spec.PublicKeyCertificateUsage.KsefTokenEncryption
        case CertUsageEnum.SYMMETRIC_KEY_ENCRYPTION:
            return spec.PublicKeyCertificateUsage.SymmetricKeyEncryption
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)
