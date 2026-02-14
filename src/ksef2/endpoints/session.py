from typing import final, Any
from ksef2.core import headers, codecs, protocols
from ksef2.infra.schema.api import spec as spec


@final
class OpenSessionEndpoint:
    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    url: str = "/sessions/online"

    def get_url(self) -> str:
        return self.url

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.OpenOnlineSessionResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.get_url(),
                headers=headers.KSeFHeaders.session(access_token),
                json=body,
            ),
            spec.OpenOnlineSessionResponse,
        )


@final
class TerminateSessionEndpoint:
    url: str = "/sessions/online/{referenceNumber}/close"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> None:
        _ = self._transport.post(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.session(access_token),
        )
