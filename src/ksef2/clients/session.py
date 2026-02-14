from __future__ import annotations

from typing import TYPE_CHECKING, final

from ksef2.core import exceptions
from ksef2.core.crypto import encrypt_invoice
from ksef2.core import protocols
from ksef2.domain.models import invoices
from ksef2.domain.models.session import SessionState
from ksef2.endpoints.invoices import DownloadInvoiceEndpoint, SendingInvoicesEndpoint
from ksef2.endpoints.session import TerminateSessionEndpoint
from ksef2.infra.mappers.invoices import SendInvoiceMapper

if TYPE_CHECKING:
    from types import TracebackType

from structlog import get_logger

logger = get_logger(__name__)


@final
class OnlineSessionClient:
    def __init__(self, transport: protocols.Middleware, state: SessionState):
        self._transport = transport
        self._state = state
        self._invoice_endpoint = SendingInvoicesEndpoint(transport)
        self._download_endpoint = DownloadInvoiceEndpoint(transport)
        self._terminate_endpoint = TerminateSessionEndpoint(transport)

    def send_invoice(self, invoice_xml: bytes) -> invoices.SendInvoiceResponse:
        encrypted = encrypt_invoice(invoice_xml, self._state.aes_key, self._state.iv)
        request_body = SendInvoiceMapper.map_request(invoice_xml, encrypted)

        response_dto = self._invoice_endpoint.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            body=request_body.model_dump(),
        )

        return SendInvoiceMapper.map_response(response_dto)

    def download_invoice(self, ksef_number: str) -> bytes:
        return self._download_endpoint.send(
            access_token=self._state.access_token,
            ksef_number=ksef_number,
        )

    def terminate(self) -> None:
        self._terminate_endpoint.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
        )

    def __enter__(self) -> OnlineSessionClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            self.terminate()
        except exceptions.KSeFException:
            logger.warning("Failed to terminate KSeF session, might be already closed.")
        except Exception:
            logger.exception("Unexpected error during session termination.")
