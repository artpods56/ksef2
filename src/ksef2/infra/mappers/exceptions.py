"""Helpers for converting API exception payloads into SDK exceptions."""

from ksef2.core.exceptions import ExceptionCode
from ksef2.infra.schema.api import spec
from ksef2.core import exceptions

MAX_RAW_BODY_LENGTH = 200


def _truncate(raw_body: str) -> str:
    """Shorten oversized raw response bodies for exception messages."""
    if len(raw_body) <= MAX_RAW_BODY_LENGTH:
        return raw_body
    return raw_body[:MAX_RAW_BODY_LENGTH] + "..."


def get_primary_exception_details(
    response: spec.ExceptionResponse,
) -> spec.ExceptionDetails | None:
    """Return the first exception detail entry when one is present."""
    if exception := response.exception:
        return (
            exception.exceptionDetailList[0] if exception.exceptionDetailList else None
        )
    return None


class ExceptionsMapper:
    """Factory for turning error payloads into concrete SDK exception types."""

    @staticmethod
    def _extract_message(
        status_code: int, model: spec.ExceptionResponse | None, raw_body: str
    ) -> str:
        """Build a readable error message from an exception payload or raw body."""
        if model is None or model.exception is None:
            return f"KSeF error {status_code}. Raw response: {_truncate(raw_body)}"

        primary = get_primary_exception_details(model)
        if not primary:
            return f"KSeF error {status_code}. No details provided."

        code = primary.exceptionCode
        description = primary.exceptionDescription or "<no description>"

        enum_val = ExceptionCode.from_code(code)
        msg = (
            f"KSeF API error: {status_code}\n[{enum_val.name}:{enum_val}] {description}"
        )

        if primary.details:
            msg += f"\nDetails: {', '.join(primary.details)}"
        return msg

    @staticmethod
    def from_auth_error(
        status_code: int, model: spec.ExceptionResponse | None, raw_body: str
    ) -> exceptions.KSeFAuthError:
        """Create an authentication error from a parsed exception payload."""
        message = ExceptionsMapper._extract_message(status_code, model, raw_body)
        return exceptions.KSeFAuthError(
            status_code=status_code, message=message, response=model
        )

    @staticmethod
    def from_bad_request(
        model: spec.ExceptionResponse | None, raw_body: str
    ) -> exceptions.KSeFApiError:
        """Create a ``400`` API error from a parsed exception payload."""
        return ExceptionsMapper.from_api_error(
            status_code=400, model=model, raw_body=raw_body
        )

    @staticmethod
    def from_too_many_requests(
        model: spec.TooManyRequestsResponse | None,
        retry_after: int | None,
        raw_body: str,
    ) -> exceptions.KSeFRateLimitError:
        """Create a rate-limit error with optional ``Retry-After`` metadata."""
        if model and model.status and model.status.description:
            message = f"KSeF rate limit exceeded: {model.status.description}"
        else:
            message = f"KSeF error 429. Raw response: {_truncate(raw_body)}"

        return exceptions.KSeFRateLimitError(
            retry_after=retry_after,
            message=message,
            response=model,
        )

    @staticmethod
    def from_api_error(
        status_code: int, model: spec.ExceptionResponse | None, raw_body: str
    ) -> exceptions.KSeFApiError:
        """Create a generic API error from a parsed exception payload."""
        message = ExceptionsMapper._extract_message(status_code, model, raw_body)
        primary = get_primary_exception_details(model) if model else None
        code = ExceptionCode.from_code(primary.exceptionCode if primary else None)

        return exceptions.KSeFApiError(
            status_code=status_code,
            exception_code=code,
            message=message,
            response=model,
        )
