from typing import final, Any

from ksef_sdk.core import headers, codecs
from ksef_sdk.core.http import HttpTransport
from ksef_sdk.infra.schema import model as spec


@final
class ChallengeEndpoint:
    def __init__(self, transport: HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/auth/challenge"

    def send(self) -> spec.AuthenticationChallengeResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(self.url),
            spec.AuthenticationChallengeResponse,
        )


@final
class TokenAuthEndpoint:
    def __init__(self, transport: HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/auth/ksef-token"

    def send(self, body: dict[str, Any]) -> spec.AuthenticationInitResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(self.url, json=body),
            spec.AuthenticationInitResponse,
        )


@final
class XAdESAuthEndpoint:
    def __init__(self, transport: HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/auth/xades-signature"

    def get_url(self, *, verify_chain: bool = False) -> str:
        return f"{self.url}?verifyCertificateChain={str(verify_chain).lower()}"

    def send(
        self,
        signed_xml: bytes,
        *,
        verify_chain: bool = False,
    ) -> spec.AuthenticationInitResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.request(
                "POST",
                self.get_url(verify_chain=verify_chain),
                content=signed_xml,
                headers={"Content-Type": "application/xml"},
            ),
            spec.AuthenticationInitResponse,
        )


@final
class AuthStatusEndpoint:
    def __init__(self, transport: HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/auth/{referenceNumber}"

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        bearer_token: str,
        reference_number: str,
    ) -> spec.AuthenticationOperationStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.get_url(reference_number=reference_number),
                headers=headers.KSeFHeaders.bearer(bearer_token),
            ),
            spec.AuthenticationOperationStatusResponse,
        )


@final
class RedeemTokenEndpoint:
    def __init__(self, transport: HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/auth/token/redeem"

    def send(
        self,
        bearer_token: str,
    ) -> spec.AuthenticationTokensResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(bearer_token),
            ),
            spec.AuthenticationTokensResponse,
        )


@final
class RefreshTokenEndpoint:
    def __init__(self, transport: HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/auth/token/refresh"

    def send(
        self,
        bearer_token: str,
    ) -> spec.AuthenticationTokenRefreshResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(bearer_token),
            ),
            spec.AuthenticationTokenRefreshResponse,
        )
