from __future__ import annotations

from typing import Any
from pydantic import BaseModel
from enum import IntEnum


class ExceptionCode(IntEnum):
    """Enumeration of all possible exception codes."""

    UNKNOWN_ERROR = 10000
    OBJECT_ALREADY_EXISTS = 30001
    VALIDATION_ERROR = 21405
    UPO_NOT_FOUND = 21178
    NOT_PROCESSED_YET = 21165

    @staticmethod
    def from_code(code: int | None) -> ExceptionCode:
        try:
            return ExceptionCode(code)
        except ValueError:
            return ExceptionCode.UNKNOWN_ERROR


class KSeFException(Exception):
    """Base exception for all KSeF SDK errors."""

    code: str = "SDK_ERROR"

    def __init__(self, message: str, **context: Any):
        super().__init__(message)
        self.context: dict[str, Any] = context
        self.context["code"] = self.code


class KSeFInvoiceRenderingError(KSeFException):
    """Raised when invoice rendering fails."""

    code: str = "INVOICE_RENDERING_ERROR"


class KSeFApiError(KSeFException):
    """Raised on 4xx/5xx responses from the KSeF API."""

    code: str = "API_ERROR"

    def __init__(
        self,
        status_code: int,
        exception_code: ExceptionCode,
        message: str,
        response: BaseModel | None = None,
    ) -> None:
        self.status_code = status_code
        self.response = response
        self.exception_code = exception_code

        msg = (
            f"{self.code}/{status_code}: {message}\n"
            f"Response: {response.model_dump_json(indent=2) if response else '<none>'}"
        )

        super().__init__(msg)


class KSeFAuthError(KSeFApiError):
    """Raised on 401/403 responses."""

    code: str = "AUTH_ERROR"

    def __init__(
        self,
        status_code: int,
        message: str,
        response: BaseModel | None = None,
    ) -> None:
        super().__init__(status_code, ExceptionCode.UNKNOWN_ERROR, message, response)


class KSeFRateLimitError(KSeFApiError):
    """Raised on 429 responses. Check ``retry_after`` for seconds to wait."""

    code: str = "RATE_LIMIT_ERROR"

    def __init__(
        self,
        retry_after: int | None,
        message: str,
        response: BaseModel | None = None,
    ) -> None:
        self.retry_after = retry_after
        self.response = response
        super().__init__(429, ExceptionCode.UNKNOWN_ERROR, message, response)


class KSeFEncryptionError(KSeFException):
    """Raised when encryption or decryption operations fail."""

    code: str = "ENCRYPTION_ERROR"

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(f"{self.code}: {message}")


class KSeFSessionError(KSeFException):
    """Raised on session-state violations (e.g. sending invoice on closed session)."""

    code: str = "SESSION_ERROR"

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(f"{self.code}: {message}")


class NoCertificateAvailableError(KSeFException):
    """Raised when no certificate is available for signing."""

    code: str = "NO_CERTIFICATE_AVAILABLE"

    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(f"{self.code}: {message}")


class KSeFExportTimeoutError(KSeFException):
    """Raised when polling for an export package exceeds the timeout."""

    code: str = "EXPORT_TIMEOUT"

    def __init__(
        self,
        reference_number: str,
        timeout: float,
    ) -> None:
        self.reference_number = reference_number
        self.timeout = timeout
        super().__init__(
            f"Export package {reference_number} not ready after {timeout}s",
            reference_number=reference_number,
            timeout=timeout,
        )


class KSeFInvoiceQueryTimeoutError(KSeFException):
    """Raised when polling for invoices to appear exceeds the timeout."""

    code: str = "INVOICE_QUERY_TIMEOUT"

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout
        super().__init__(
            f"No invoices found after polling for {timeout}s",
            timeout=timeout,
        )
