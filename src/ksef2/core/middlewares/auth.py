from collections.abc import Mapping
from typing import final, Any

import httpx

from ksef2.core.middlewares.base import BaseMiddleware
from ksef2.core.protocols import Middleware


@final
class BearerTokenMiddleware(BaseMiddleware):
    def __init__(self, transport: Middleware, token: str) -> None:
        self._next = transport
        self._token = token

    def _merge(self, extra: dict[str, str] | None) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self._token}"}
        return headers | (extra or {})

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
        **kwargs,
    ) -> httpx.Response:
        return self._next.request(
            method,
            path,
            headers=self._merge(headers),
            params=params,
            json=json,
            content=content,
            **kwargs,
        )
