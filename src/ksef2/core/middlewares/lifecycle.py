from dataclasses import dataclass
from typing import Any, final, override

import httpx

from ksef2.core import exceptions, protocols
from ksef2.core.middlewares.base import BaseMiddleware


@dataclass(slots=True)
class ClientLifecycleState:
    closed: bool = False


@final
class ClientLifecycleMiddleware(BaseMiddleware):
    def __init__(
        self,
        transport: protocols.Middleware,
        state: ClientLifecycleState,
    ) -> None:
        self._next = transport
        self._state = state

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
        if self._state.closed:
            raise exceptions.KSeFClientClosedError("Client is closed.")

        return self._next.request(
            method,
            path,
            headers=headers,
            params=params,
            json=json,
            content=content,
        )
