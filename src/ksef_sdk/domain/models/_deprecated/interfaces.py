from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Signer(Protocol):
    """Protocol for pluggable XML signing strategies."""

    def sign(self, xml_bytes: bytes) -> bytes: ...
