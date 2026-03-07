"""Mappings from generated encryption schema models to domain models."""

from typing import assert_never, overload

from ksef2.domain.models.encryption import (
    CertUsage,
    PublicKeyCertificate,
)
from ksef2.infra.schema.api import spec


@overload
def from_spec(response: spec.PublicKeyCertificateUsage) -> CertUsage: ...


@overload
def from_spec(response: spec.PublicKeyCertificate) -> PublicKeyCertificate: ...


def from_spec(
    response: spec.PublicKeyCertificateUsage | spec.PublicKeyCertificate,
) -> object:
    """Convert a generated encryption schema object into its domain counterpart."""
    if isinstance(response, spec.PublicKeyCertificate):
        return PublicKeyCertificate(
            certificate=response.certificate,
            valid_from=response.validFrom,
            valid_to=response.validTo,
            usage=[from_spec(usage) for usage in response.usage],
        )

    match response:
        case spec.PublicKeyCertificateUsage.KsefTokenEncryption:
            return "ksef_token_encryption"
        case spec.PublicKeyCertificateUsage.SymmetricKeyEncryption:
            return "symmetric_key_encryption"
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)
