from typing import final, Any
from ksef_sdk.core import http, headers, codecs
from ksef_sdk.infra.schema import model as spec


@final
class GenerateTokenEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/tokens"

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.GenerateTokenResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.session(access_token),
                json=body,
            ),
            spec.GenerateTokenResponse,
        )


@final
class TokenStatusEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/tokens/{referenceNumber}"

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> spec.TokenStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.get_url(reference_number=reference_number),
                headers=headers.KSeFHeaders.session(access_token),
            ),
            spec.TokenStatusResponse,
        )


@final
class RevokeTokenEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/tokens/{referenceNumber}"

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(self, access_token: str, reference_number: str) -> None:
        _ = self._transport.delete(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.session(access_token),
        )
