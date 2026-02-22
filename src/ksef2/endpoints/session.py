from typing import final, Any, TypedDict, Literal, NotRequired, Unpack
from urllib.parse import urlencode

from pydantic import TypeAdapter

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
                headers=headers.KSeFHeaders.bearer(access_token),
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
            headers=headers.KSeFHeaders.bearer(access_token),
        )


@final
class OpenBatchSessionEndpoint:
    """Open a batch session for sending invoices in bulk.

    Requires InvoiceWrite or EnforcementOperations permission.
    """

    url: str = "/sessions/batch"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.OpenBatchSessionResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.OpenBatchSessionResponse,
        )


@final
class CloseBatchSessionEndpoint:
    """Close a batch session and start processing the invoice batch.

    This triggers processing of the invoice batch and generation of UPO
    for valid invoices and a collective UPO for the session.

    Requires InvoiceWrite or EnforcementOperations permission.
    """

    url: str = "/sessions/batch/{referenceNumber}/close"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> None:
        """Close the batch session.

        Args:
            access_token: Bearer token for authentication.
            reference_number: Batch session reference number.

        Returns:
            None - returns 204 No Content on success.
        """
        _ = self._transport.post(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.bearer(access_token),
        )


@final
class GetSessionUpoEndpoint:
    """Get UPO (Official Proof of Receipt) for a session by UPO reference number.

    Returns XML document containing the collective UPO for the session.
    """

    url: str = "/sessions/{referenceNumber}/upo/{upoReferenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str, upo_reference_number: str) -> str:
        return self.url.format(
            referenceNumber=reference_number,
            upoReferenceNumber=upo_reference_number,
        )

    def send(
        self,
        access_token: str,
        reference_number: str,
        upo_reference_number: str,
    ) -> bytes:
        """Send the request and return the UPO XML content.

        Args:
            access_token: Bearer token for authentication.
            reference_number: Session reference number.
            upo_reference_number: UPO reference number.

        Returns:
            Raw XML bytes containing the UPO document.
        """
        resp = self._transport.get(
            self.get_url(
                reference_number=reference_number,
                upo_reference_number=upo_reference_number,
            ),
            headers=headers.KSeFHeaders.bearer(access_token),
        )
        return resp.content


ListSessionEndpointQueryParams = TypedDict(
    "ListSessionEndpointQueryParams",
    {
        "sessionType": Literal["Online", "Batch"],
        "referenceNumber": NotRequired[str | None],
        "dateCreatedFrom": NotRequired[str | None],
        "dateCreatedTo": NotRequired[str | None],
        "dateClosedFrom": NotRequired[str | None],
        "dateClosedTo": NotRequired[str | None],
        "dateModifiedFrom": NotRequired[str | None],
        "dateModifiedTo": NotRequired[str | None],
        "statuses": NotRequired[
            list[Literal["InProgress", "Succeeded", "Failed", "Cancelled"]]
        ],
    },
)


@final
class ListSessionsEndpoint:
    url: str = "/sessions"

    _adapter = TypeAdapter(ListSessionEndpointQueryParams)

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, params: ListSessionEndpointQueryParams) -> str:
        return f"{self.url}?{urlencode(params, doseq=True)}"

    def send(
        self,
        access_token: str,
        continuation_token: str | None = None,
        **query_params: Unpack[ListSessionEndpointQueryParams],
    ) -> spec.SessionsQueryResponse:
        valid_params = self._adapter.validate_python(query_params)

        path = self.get_url(valid_params)

        headers_dict = headers.KSeFHeaders.bearer(access_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path, headers=headers_dict),
            spec.SessionsQueryResponse,
        )
