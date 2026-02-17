from typing import Any, Protocol

import httpx

from ksef2.domain.models.session import OnlineSessionState


class Endpoint(Protocol):
    """Protocol for an API endpoint."""

    url: str

    def get_url(self, **kwargs: dict[str, str]) -> str: ...

    def send(
        self,
        state: OnlineSessionState,
        body: dict[str, Any],
    ) -> httpx.Response: ...


class Middleware(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response: ...

    def get(
        self, path: str, *, headers: dict[str, str] | None = None
    ) -> httpx.Response: ...

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response: ...

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response: ...
