from __future__ import annotations

from ksef_sdk.clients._deprecated._base import BaseSubClient
from ksef_sdk.core.http import HttpTransport
from ksef_sdk.core.endpoints import OnlineSessionInvoicesEndpoint
from ksef_sdk.domain.models import invoices


class InvoicesClient:
    def __init__(self, transport: HttpTransport):
        self._send_online = OnlineSessionInvoicesEndpoint(transport)

    def send_interactive(
        self,
        request: SendInvoiceRequest,
        state: SessionState,
    ) -> SendInvoiceResponse:
        spec_request = InteractiveInvoiceMapper.map_request(request)

        resp = self._send_online.send(
            state,
            spec_request.model_dump(by_alias=True, exclude_none=True),
        )

        return InteractiveInvoiceMapper.map_response(
            JsonResponseCodec.parse(resp, invoices.SendInvoiceResponse)
        )


class InvoicesClient(BaseSubClient):
    """Sub-client for invoice download and metadata queries."""

    def download(self, access_token: str, ksef_number: str) -> bytes:
        """``GET /invoices/{ksefNumber}`` — download raw invoice XML."""
        return self._http.get_raw(
            f"/invoices/{ksef_number}",
            token=access_token,
        )
