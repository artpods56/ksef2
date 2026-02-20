"""Reader for KSeF export package ZIP archives.

KSeF export packages are encrypted ZIP archives containing XML invoice files
and potentially non-invoice files (manifests, signatures, metadata). This
reader encapsulates knowledge of the package structure so callers don't need
to understand the KSeF specification to extract invoices.
"""

from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterator, final

_KNOWN_NON_INVOICE_FILES = frozenset(
    {
        "manifest.xml",
        "metadata.xml",
        "signature.xml",
    }
)


@dataclass(frozen=True, slots=True)
class PackageInvoice:
    name: str
    xml: bytes


@final
class PackageReader:
    def __init__(self, zip_parts: list[bytes] | bytes) -> None:
        if isinstance(zip_parts, bytes):
            zip_parts = [zip_parts]
        self._parts = zip_parts

    def __iter__(self) -> Iterator[PackageInvoice]:
        return self.invoices()

    def invoices(self) -> Iterator[PackageInvoice]:
        for part in self._parts:
            with zipfile.ZipFile(io.BytesIO(part), "r") as zf:
                for entry in zf.namelist():
                    if not entry.lower().endswith(".xml"):
                        continue
                    if PurePosixPath(entry).name.lower() in _KNOWN_NON_INVOICE_FILES:
                        continue
                    yield PackageInvoice(name=entry, xml=zf.read(entry))
