import abc
from collections.abc import Mapping
from typing import Any

import httpx


class BaseMiddleware(abc.ABC):
    @abc.abstractmethod
    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response: ...

    def get(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        return self.request("GET", path, headers=headers, params=params)

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response:
        return self.request(
            "POST", path, headers=headers, json=json, params=params, content=content
        )

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        return self.request("DELETE", path, headers=headers, params=params)
