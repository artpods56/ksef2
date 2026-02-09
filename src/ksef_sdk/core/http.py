from typing import Any, final
import httpx

from ksef_sdk.config import Environment
from ksef_sdk.core import exceptions


@final
class HttpTransport:
    def __init__(
        self, environment: Environment, *, base_url: str | None = None
    ) -> None:
        self._environment = environment
        self._base_url = base_url or environment.base_url
        self._client = httpx.Client(http2=True)

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        if response.is_success:
            return

        status = response.status_code

        if status == 429:
            retry_after: int | None = None
            raw = response.headers.get("Retry-After")
            if raw is not None:
                try:
                    retry_after = int(raw)
                except ValueError:
                    pass
            raise exceptions.KSeFRateLimitError(
                retry_after=retry_after,
                message="Server responded with 429 Too Many Requests.",
            )

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response:

        full_path = self._base_url + path

        resp = self._client.request(
            method,
            full_path,
            headers=headers,
            json=json,
            content=content,
        )
        self._raise_for_status(resp)
        return resp

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
