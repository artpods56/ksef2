from typing import final, Any
from urllib.parse import urlencode

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
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.GenerateTokenResponse,
        )


@final
class ListTokensEndpoint:
    url: str = "/tokens"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        *,
        status: list[str] | None = None,
        description: str | None = None,
        author_identifier: str | None = None,
        author_identifier_type: str | None = None,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> spec.QueryTokensResponse:
        # Build query parameters
        query_params: list[tuple[str, str]] = []

        if status:
            for s in status:
                query_params.append(("status", s))

        if description is not None:
            query_params.append(("description", description))

        if author_identifier is not None:
            query_params.append(("authorIdentifier", author_identifier))

        if author_identifier_type is not None:
            query_params.append(("authorIdentifierType", author_identifier_type))

        if page_size is not None:
            query_params.append(("pageSize", str(page_size)))

        query_string = urlencode(query_params) if query_params else ""
        path = f"{self.url}?{query_string}" if query_string else self.url

        # Build headers
        headers_dict = headers.KSeFHeaders.bearer(access_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path, headers=headers_dict),
            spec.QueryTokensResponse,
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
                headers=headers.KSeFHeaders.bearer(access_token),
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
            headers=headers.KSeFHeaders.bearer(access_token),
        )
