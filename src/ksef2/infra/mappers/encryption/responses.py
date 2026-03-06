from enum import Enum
from functools import singledispatch
from typing import assert_never, overload

from pydantic import BaseModel

from ksef2.domain.models.encryption import CertUsage, PublicKeyCertificate
from ksef2.infra.schema.api import spec


@overload
def from_spec(response: spec.PublicKeyCertificateUsage) -> CertUsage: ...


@overload
def from_spec(response: spec.PublicKeyCertificate) -> PublicKeyCertificate: ...


def from_spec(response: BaseModel | Enum) -> object:
    return _from_spec(response)


@singledispatch
def _from_spec(response: BaseModel | Enum) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(response).__name__}. "
        f"Register one with @_from_spec.register"
    )


@_from_spec.register
def _(response: spec.PublicKeyCertificateUsage) -> CertUsage:
    match response:
        case spec.PublicKeyCertificateUsage.KsefTokenEncryption:
            return "ksef_token_encryption"
        case spec.PublicKeyCertificateUsage.SymmetricKeyEncryption:
            return "symmetric_key_encryption"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)


@_from_spec.register
def _(response: spec.PublicKeyCertificate) -> PublicKeyCertificate:
    return PublicKeyCertificate(
        certificate=response.certificate,
        valid_from=response.validFrom,
        valid_to=response.validTo,
        usage=[from_spec(u) for u in response.usage],
    )
