from typing import final, Any
from ksef2.core import headers, codecs, protocols
from ksef2.infra.schema.api import spec as spec


@final
class GenerateTokenEndpoint:
    url: str = "/tokens"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

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
    url: str = "/tokens/{referenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

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
    url: str = "/tokens/{referenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(self, access_token: str, reference_number: str) -> None:
        _ = self._transport.delete(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.session(access_token),
        )
