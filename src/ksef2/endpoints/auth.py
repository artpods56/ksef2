from typing import Any, final

from urllib.parse import urlencode

from ksef2.core import headers, codecs, protocols
from ksef2.infra.schema.api import spec as spec


@final
class ChallengeEndpoint:
    url: str = "/auth/challenge"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(self) -> spec.AuthenticationChallengeResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(self.url),
            spec.AuthenticationChallengeResponse,
        )


@final
class TokenAuthEndpoint:
    url: str = "/auth/ksef-token"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> spec.AuthenticationInitResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(self.url, json=body),
            spec.AuthenticationInitResponse,
        )


@final
class XAdESAuthEndpoint:
    url: str = "/auth/xades-signature"

    def __init__(self, transport: protocols.Middleware):
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

    def __init__(self, transport: protocols.Middleware):
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

    def __init__(self, transport: protocols.Middleware):
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

    def __init__(self, transport: protocols.Middleware):
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


@final
class ListActiveSessionsEndpoint:
    url: str = "/auth/sessions"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        bearer_token: str,
        *,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> spec.AuthenticationListResponse:
        headers_dict = headers.KSeFHeaders.bearer(bearer_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        query_params: list[tuple[str, str]] = []
        if page_size is not None:
            query_params.append(("pageSize", str(page_size)))

        query_string = urlencode(query_params) if query_params else ""
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                path,
                headers=headers_dict,
            ),
            spec.AuthenticationListResponse,
        )


@final
class TerminateCurrentSessionEndpoint:
    url: str = "/auth/sessions/current"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(self, bearer_token: str) -> None:
        _ = self._transport.delete(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )


@final
class TerminateAuthSessionEndpoint:
    url: str = "/auth/sessions/{referenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(self, bearer_token: str, reference_number: str) -> None:
        _ = self._transport.delete(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )
