from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

import httpx
from pydantic import BaseModel, TypeAdapter, ValidationError

from ksef_sdk._generated.model import ExceptionResponse
from ksef_sdk.exceptions import (
    KsefApiError,
    KsefAuthError,
    KsefRateLimitError,
)

if TYPE_CHECKING:
    from ksef_sdk._environments import Environment

T = TypeVar("T", bound=BaseModel)


class HttpTransport:
    """Thin wrapper around :class:`httpx.Client` with KSeF-specific error mapping."""

    def __init__(self, env: Environment) -> None:
        self._client = httpx.Client(base_url=env.base_url)
        self._access_token: str | None = None

    # -- lifecycle --

    def close(self) -> None:
        self._client.close()

    # -- auth header management --

    def set_access_token(self, token: str) -> None:
        self._access_token = token

    def clear_access_token(self) -> None:
        self._access_token = None

    # -- request helpers --

    def _raw_request(
        self,
        method: str,
        path: str,
        *,
        body: BaseModel | None = None,
        raw_body: bytes | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        headers: dict[str, str] = {}
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        if extra_headers:
            headers.update(extra_headers)

        kwargs: dict[str, Any] = {"headers": headers}
        if body is not None:
            kwargs["json"] = body.model_dump(by_alias=True, exclude_none=True)
        elif raw_body is not None:
            kwargs["content"] = raw_body

        resp = self._client.request(method, path, **kwargs)
        self._raise_for_status(resp)
        return resp

    def request(
        self,
        method: str,
        path: str,
        *,
        body: BaseModel | None = None,
        response_model: type[T] | None = None,
        raw_body: bytes | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> T | None:
        resp = self._raw_request(method, path, body=body, raw_body=raw_body, extra_headers=extra_headers)

        if response_model is None:
            return None

        return response_model.model_validate(resp.json())

    def get(self, path: str, *, response_model: type[T]) -> T:
        result = self.request("GET", path, response_model=response_model)
        assert result is not None
        return result

    def get_list(self, path: str, *, item_model: type[T]) -> list[T]:
        """GET a path that returns a JSON array of *item_model*."""
        resp = self._raw_request("GET", path)
        adapter: TypeAdapter[list[T]] = TypeAdapter(list[item_model])
        return adapter.validate_python(resp.json())

    def post(
        self,
        path: str,
        *,
        body: BaseModel | None = None,
        response_model: type[T] | None = None,
    ) -> T | None:
        return self.request("POST", path, body=body, response_model=response_model)

    # -- error mapping --

    @staticmethod
    def _raise_for_status(resp: httpx.Response) -> None:
        if resp.is_success:
            return

        status = resp.status_code

        # Try to parse the structured error response
        exception_response: ExceptionResponse | None = None
        message = resp.text
        try:
            exception_response = ExceptionResponse.model_validate(resp.json())
            if exception_response.exception:
                info = exception_response.exception
                parts = [info.serviceName or "", info.serviceCtx or ""]
                if info.exceptionDetailList:
                    parts.extend(d.exceptionDescription for d in info.exceptionDetailList if d.exceptionDescription)
                message = " | ".join(p for p in parts if p)
        except (ValueError, ValidationError):
            pass

        if status == 429:
            retry_after: int | None = None
            raw = resp.headers.get("Retry-After")
            if raw is not None:
                try:
                    retry_after = int(raw)
                except ValueError:
                    pass
            raise KsefRateLimitError(retry_after=retry_after, message=message, response=exception_response)

        if status in (401, 403):
            raise KsefAuthError(status, message, exception_response)

        raise KsefApiError(status, message, exception_response)
