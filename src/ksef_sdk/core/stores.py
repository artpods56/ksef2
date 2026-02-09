from __future__ import annotations
from collections.abc import Iterable

from datetime import datetime, timezone

from ksef_sdk.core import exceptions
from ksef_sdk.domain.models import encryption


class CertificateStore:
    def __init__(self) -> None:
        self._certificates: list[encryption.PublicKeyCertificate] = []

    def load(self, certs: Iterable[encryption.PublicKeyCertificate]) -> None:
        """Replace stored certificates."""
        self._certificates = list(certs)

    def add(self, cert: encryption.PublicKeyCertificate) -> None:
        self._certificates.append(cert)

    def all(self) -> list[encryption.PublicKeyCertificate]:
        return list(self._certificates)

    def get_valid(
        self, usage: encryption.CertUsage
    ) -> encryption.PublicKeyCertificate | None:
        """Get a valid certificate for given usage.

        Raises:
            NoCertificateAvailableError: If no valid certificate found for usage.
        """
        cert = next(iter(self.by_usage(usage=usage)), None)
        if cert is None:
            raise exceptions.NoCertificateAvailableError(
                f"No valid certificate for usage: {usage}"
            )
        return cert

    def list_valid(
        self,
        *,
        at: datetime | None = None,
    ) -> list[encryption.PublicKeyCertificate]:
        def make_aware(dt: datetime, tz=timezone.utc) -> datetime:
            """Convert naive datetime to aware, or return if already aware"""
            if dt.tzinfo is None:
                return dt.replace(tzinfo=tz)
            return dt

        now = make_aware(at) if at else datetime.now(tz=timezone.utc)

        return [
            cert
            for cert in self._certificates
            if cert.valid_from <= now <= cert.valid_to
        ]

    def by_usage(
        self,
        usage: encryption.CertUsage,
        *,
        at: datetime | None = None,
    ) -> list[encryption.PublicKeyCertificate]:
        return [cert for cert in self.list_valid(at=at) if usage in cert.usage]
