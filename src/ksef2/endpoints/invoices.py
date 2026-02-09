from typing import final, Any
from ksef2.core import http, headers, codecs
from ksef2.infra.schema import model as spec


@final
class DownloadInvoiceEndpoint:
    url: str = "/invoices/ksef/{ksefNumber}"

    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    def get_url(self, *, ksef_number: str) -> str:
        return self.url.format(ksefNumber=ksef_number)

    def send(self, access_token: str, ksef_number: str) -> bytes:
        resp = self._transport.get(
            self.get_url(ksef_number=ksef_number),
            headers=headers.KSeFHeaders.session(access_token),
        )
        return resp.content


@final
class SendingInvoicesEndpoint:
    url: str = "/sessions/online/{referenceNumber}/invoices"

    def __init__(self, transport: http.HttpTransport):
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
                headers=headers.KSeFHeaders.session(access_token),
                json=body,
            ),
            spec.SendInvoiceResponse,
        )
