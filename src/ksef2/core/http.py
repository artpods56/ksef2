from typing import Any, final, Literal, override

import httpx

from ksef2.core.middlewares.base import BaseMiddleware

HttpMethod = Literal["POST", "GET", "DELETE"]


@final
class HttpTransport(BaseMiddleware):
    def __init__(self, client: httpx.Client, headers: dict[str, Any]) -> None:
        self._client = client
        self._headers = headers

    def _merge(self, extra: dict[str, str] | None) -> dict[str, Any]:
        if not extra:
            return self._headers
        return {**self._headers, **extra}

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
        return self._client.request(
            method,
            path,
            headers=self._merge(headers),
            json=json,
            content=content,
            params=params,
        )

    def with_headers(self, headers: dict[str, str]):
        merged_headers = self._headers | headers
        return HttpTransport(self._client, headers=merged_headers)
