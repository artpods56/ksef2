from ksef2.infra.schema.api import spec
from ksef2.core import exceptions

MAX_RAW_BODY_LENGTH = 200


def _truncate(raw_body: str) -> str:
    if len(raw_body) <= MAX_RAW_BODY_LENGTH:
        return raw_body
    return raw_body[:MAX_RAW_BODY_LENGTH] + "..."


class ExceptionsMapper:
    @staticmethod
    def from_too_many_requests(
        model: spec.TooManyRequestsResponse | None,
        retry_after: int | None,
        raw_body: str,
    ) -> exceptions.KSeFRateLimitError:
        if model is not None:
            message = f"{model.status.description}: " + ", ".join(model.status.details)
        else:
            message = f"Too Many Requests. Raw response: {_truncate(raw_body)}"

        return exceptions.KSeFRateLimitError(
            retry_after=retry_after, message=message, response=model
        )

    @staticmethod
    def from_auth_error(
        status_code: int,
        model: spec.ExceptionResponse | None,
        raw_body: str,
    ) -> exceptions.KSeFAuthError:
        if model is not None:
            message = f"Authentication error: {status_code}"
        else:
            message = f"Authentication error: {status_code}. Raw response: {_truncate(raw_body)}"

        return exceptions.KSeFAuthError(
            status_code=status_code,
            message=message,
            response=model,
        )

    @staticmethod
    def from_bad_request(
        model: spec.ExceptionResponse | None,
        raw_body: str,
    ) -> exceptions.KSeFApiError:
        if model is not None and model.exception is not None:
            message = ""
            for detail in model.exception.exceptionDetailList or []:
                patch = [
                    f"{detail.exceptionDescription or ''}\n",
                    *[
                        f"{detail_description}\n"
                        for detail_description in detail.details or []
                    ],
                ]
                message += "".join(patch)
        else:
            message = f"Bad Request. Raw response: {_truncate(raw_body)}"

        return exceptions.KSeFApiError(status_code=400, message=message, response=model)

    @staticmethod
    def from_api_error(
        status_code: int,
        model: spec.ExceptionResponse | None,
        raw_body: str,
    ) -> exceptions.KSeFApiError:
        if model is not None:
            message = f"KSeF API error: {status_code}"
        else:
            message = (
                f"KSeF API error: {status_code}. Raw response: {_truncate(raw_body)}"
            )

        return exceptions.KSeFApiError(
            status_code=status_code,
            message=message,
            response=model,
        )
