from typing import final, Any

from ksef2.core import headers, codecs
from ksef2.core.http import HttpTransport
from ksef2.infra.schema import model as spec


@final
class ChallengeEndpoint:
    url: str = "/auth/challenge"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def send(self) -> spec.AuthenticationChallengeResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(self.url),
            spec.AuthenticationChallengeResponse,
        )


@final
class TokenAuthEndpoint:
    url: str = "/auth/ksef-token"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> spec.AuthenticationInitResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(self.url, json=body),
            spec.AuthenticationInitResponse,
        )


@final
class XAdESAuthEndpoint:
    url: str = "/auth/xades-signature"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

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
    url: str = "/auth/{referenceNumber}"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

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
    url: str = "/auth/token/redeem"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

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
    url: str = "/auth/token/refresh"

    def __init__(self, transport: HttpTransport):
        self._transport = transport

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
