from typing import Any, final

import httpx


@final
class HttpTransport:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response:
        return self._client.request(
            method,
            path,
            headers=headers,
            json=json,
            content=content,
        )

    def get(
        self, path: str, *, headers: dict[str, str] | None = None
    ) -> httpx.Response:
        return self.request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return self.request("POST", path, headers=headers, json=json)

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        return self.request("DELETE", path, headers=headers)
