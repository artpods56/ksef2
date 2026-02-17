from enum import StrEnum
from typing import final, Any, TypedDict, Unpack, Literal, NotRequired
from urllib.parse import urlencode

from pydantic import TypeAdapter

from ksef2.core import headers, codecs, protocols
from ksef2.infra.schema.api import spec as spec


# ---------------------------------------------------------------------------
# Query / Export endpoints
# ---------------------------------------------------------------------------


class SortOrder(StrEnum):
    ASC = "Asc"
    DESC = "Desc"


QueryInvoicesMetadataQueryParams = TypedDict(
    "QueryInvoicesMetadataQueryParams",
    {
        "sortOrder": NotRequired[SortOrder | None],
        "pageOffset": NotRequired[int | None],
        "pageSize": NotRequired[int | None],
    },
)


@final
class QueryInvoicesMetadataEndpoint:
    url: str = "/invoices/query/metadata"

    _adapter = TypeAdapter(QueryInvoicesMetadataQueryParams)

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
        **query_params: Unpack[QueryInvoicesMetadataQueryParams],
    ) -> spec.QueryInvoicesMetadataResponse:
        valid_params = self._adapter.validate_python(query_params)
        query_string = urlencode(valid_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QueryInvoicesMetadataResponse,
        )


@final
class ExportInvoicesEndpoint:
    url: str = "/invoices/exports"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.ExportInvoicesResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.ExportInvoicesResponse,
        )


@final
class GetExportStatusEndpoint:
    url: str = "/invoices/exports/{referenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> spec.InvoiceExportStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.get_url(reference_number=reference_number),
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.InvoiceExportStatusResponse,
        )


@final
class DownloadInvoiceEndpoint:
    url: str = "/invoices/ksef/{ksefNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, ksef_number: str) -> str:
        return self.url.format(ksefNumber=ksef_number)

    def send(self, access_token: str, ksef_number: str) -> bytes:
        resp = self._transport.get(
            self.get_url(ksef_number=ksef_number),
            headers=headers.KSeFHeaders.bearer(access_token),
        )
        return resp.content


@final
class SendingInvoicesEndpoint:
    url: str = "/sessions/online/{referenceNumber}/invoices"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
        body: dict[str, Any],
    ) -> spec.SendInvoiceResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.get_url(reference_number=reference_number),
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.SendInvoiceResponse,
        )


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
        "statuses": list[Literal["InProgress", "Succeeded", "Failed", "Cancelled"]],
    },
)


@final
class ListSessionsEndpoint:
    url: str = "/sessions"

    _adapter = TypeAdapter(ListSessionEndpointQueryParams)

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        continuation_token: str | None = None,
        **query_params: Unpack[ListSessionEndpointQueryParams],
    ) -> spec.SessionsQueryResponse:
        valid_params = self._adapter.validate_python(query_params)

        path = f"{self.url}?{urlencode(valid_params, doseq=True)}"

        print(path)

        headers_dict = headers.KSeFHeaders.bearer(access_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path, headers=headers_dict),
            spec.SessionsQueryResponse,
        )


@final
class GetSessionStatusEndpoint:
    url: str = "/sessions/{referenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> spec.SessionStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.get_url(reference_number=reference_number),
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.SessionStatusResponse,
        )


ListSessionInvoicesQueryParams = TypedDict(
    "ListSessionInvoicesQueryParams",
    {
        "pageSize": NotRequired[int | None],
    },
)


@final
class ListSessionInvoicesEndpoint:
    url: str = "/sessions/{referenceNumber}/invoices"

    _adapter = TypeAdapter(ListSessionInvoicesQueryParams)

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
        *,
        page_size: int,
        continuation_token: str | None = None,
    ) -> spec.SessionInvoicesResponse:
        valid_params = self._adapter.validate_python({"pageSize": page_size})

        query_string = urlencode(valid_params)
        base = self.get_url(reference_number=reference_number)
        path = f"{base}?{query_string}" if query_string else base

        headers_dict = headers.KSeFHeaders.bearer(access_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path, headers=headers_dict),
            spec.SessionInvoicesResponse,
        )


@final
class GetSessionInvoiceStatusEndpoint:
    url: str = "/sessions/{referenceNumber}/invoices/{invoiceReferenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str, invoice_reference_number: str) -> str:
        return self.url.format(
            referenceNumber=reference_number,
            invoiceReferenceNumber=invoice_reference_number,
        )

    def send(
        self,
        access_token: str,
        reference_number: str,
        invoice_reference_number: str,
    ) -> spec.SessionInvoiceStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.get_url(
                    reference_number=reference_number,
                    invoice_reference_number=invoice_reference_number,
                ),
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.SessionInvoiceStatusResponse,
        )


ListFailedSessionInvoicesQueryParams = TypedDict(
    "ListFailedSessionInvoicesQueryParams",
    {
        "pageSize": NotRequired[int | None],
    },
)


@final
class ListFailedSessionInvoicesEndpoint:
    url: str = "/sessions/{referenceNumber}/invoices/failed"

    _adapter = TypeAdapter(ListFailedSessionInvoicesQueryParams)

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
        *,
        page_size: int,
        continuation_token: str | None = None,
    ) -> spec.SessionInvoicesResponse:
        valid_params = self._adapter.validate_python({"pageSize": page_size})
        query_string = urlencode(valid_params)
        base = self.get_url(reference_number=reference_number)
        path = f"{base}?{query_string}" if query_string else base

        headers_dict = headers.KSeFHeaders.bearer(access_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        return codecs.JsonResponseCodec.parse(
            self._transport.get(path, headers=headers_dict),
            spec.SessionInvoicesResponse,
        )


@final
class GetInvoiceUpoByKsefNumberEndpoint:
    url: str = "/sessions/{referenceNumber}/invoices/ksef/{ksefNumber}/upo"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str, ksef_number: str) -> str:
        return self.url.format(
            referenceNumber=reference_number,
            ksefNumber=ksef_number,
        )

    def send(
        self,
        access_token: str,
        reference_number: str,
        ksef_number: str,
    ) -> bytes:
        resp = self._transport.get(
            self.get_url(
                reference_number=reference_number,
                ksef_number=ksef_number,
            ),
            headers=headers.KSeFHeaders.bearer(access_token),
        )
        return resp.content


@final
class GetInvoiceUpoByReferenceEndpoint:
    url: str = "/sessions/{referenceNumber}/invoices/{invoiceReferenceNumber}/upo"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str, invoice_reference_number: str) -> str:
        return self.url.format(
            referenceNumber=reference_number,
            invoiceReferenceNumber=invoice_reference_number,
        )

    def send(
        self,
        access_token: str,
        reference_number: str,
        invoice_reference_number: str,
    ) -> bytes:
        resp = self._transport.get(
            self.get_url(
                reference_number=reference_number,
                invoice_reference_number=invoice_reference_number,
            ),
            headers=headers.KSeFHeaders.bearer(access_token),
        )
        return resp.content
