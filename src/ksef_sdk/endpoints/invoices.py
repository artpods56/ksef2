from typing import final, Any
from ksef_sdk.core import http, headers, codecs
from ksef_sdk.infra.schema import model as spec


@final
class SendingInvoicesEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/sessions/online/{referenceNumber}/invoices"

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
                self.get_url(
                    reference_number=reference_number
                ),
                headers=headers.KSeFHeaders.session(access_token),
                json=body,
            ),
            spec.SendInvoiceResponse,
        )
