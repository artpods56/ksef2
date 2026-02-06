from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ksef_sdk._generated.model import ExceptionResponse


class KsefError(Exception):
    """Base exception for all KSeF SDK errors."""


class KsefApiError(KsefError):
    """Raised on 4xx/5xx responses from the KSeF API."""

    def __init__(
        self,
        status_code: int,
        message: str,
        response: ExceptionResponse | None = None,
    ) -> None:
        self.status_code = status_code
        self.response = response
        super().__init__(f"[{status_code}] {message}")


class KsefAuthError(KsefApiError):
    """Raised on 401/403 responses."""


class KsefRateLimitError(KsefApiError):
    """Raised on 429 responses. Check ``retry_after`` for seconds to wait."""

    def __init__(
        self,
        retry_after: int | None,
        message: str,
        response: ExceptionResponse | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(429, message, response)


class KsefEncryptionError(KsefError):
    """Raised when encryption or decryption operations fail."""


class KsefSessionError(KsefError):
    """Raised on session-state violations (e.g. sending invoice on closed session)."""
