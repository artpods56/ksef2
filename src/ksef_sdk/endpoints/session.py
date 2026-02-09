from typing import final, Any
from ksef_sdk.core import http, headers, codecs
from ksef_sdk.infra.schema import model as spec


@final
class OpenSessionEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/sessions/online"

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
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/sessions/online/{referenceNumber}"

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> None:
        self._transport.delete(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.session(access_token),
        )
