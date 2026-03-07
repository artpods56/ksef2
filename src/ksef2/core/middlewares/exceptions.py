from typing import final, Any, override

import httpx
from pydantic import BaseModel, ValidationError

from ksef2.core import middlewares, protocols
from ksef2.infra.mappers.exceptions import ExceptionsMapper
from ksef2.infra.schema.api import spec


@final
class KSeFExceptionMiddleware(middlewares.BaseMiddleware):
    def __init__(self, transport: protocols.Middleware) -> None:
        self._next = transport

    @staticmethod
    def _try_parse[T: BaseModel](content: str, model: type[T]) -> T | None:
        try:
            return model.model_validate_json(content)
        except (ValidationError, ValueError):
            return None

    @staticmethod
    def _parse_retry_after(headers: httpx.Headers) -> int | None:
        value = headers.get("Retry-After")
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @classmethod
    def _raise_for_status(cls, response: httpx.Response) -> None:
        if response.is_success:
            return

        status = response.status_code
        raw_body = response.text

        if status == 429:
            model = cls._try_parse(raw_body, spec.TooManyRequestsResponse)
            retry_after = cls._parse_retry_after(response.headers)
            raise ExceptionsMapper.from_too_many_requests(model, retry_after, raw_body)

        model = cls._try_parse(raw_body, spec.ExceptionResponse)

        if status in (401, 403):
            raise ExceptionsMapper.from_auth_error(status, model, raw_body)

        if status == 400:
            raise ExceptionsMapper.from_bad_request(model, raw_body)

        raise ExceptionsMapper.from_api_error(status, model, raw_body)

    def _handle(self, response: httpx.Response) -> httpx.Response:
        self._raise_for_status(response)
        return response

    @override
    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: httpx.QueryParams | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response:
        return self._handle(
            self._next.request(
                method,
                path,
                headers=headers,
                params=params,
                json=json,
                content=content,
            )
        )
