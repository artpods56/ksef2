from typing import Any, Protocol

import httpx

from ksef_sdk.domain.models.session import SessionState


class Endpoint(Protocol):
    """Protocol for an API endpoint."""

    url: str

    def get_url(self, **kwargs: dict[str, str]) -> str: ...

    def send(
        self,
        state: SessionState,
        body: dict[str, Any],
    ) -> httpx.Response: ...
