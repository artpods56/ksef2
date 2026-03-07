from __future__ import annotations

import base64
from collections.abc import Callable
from typing import final

import httpx
from tenacity import RetryError, retry, retry_if_result, stop_after_delay, wait_fixed

from ksef2.core import exceptions
from ksef2.core.crypto import encrypt_invoice
from ksef2.logging import get_logger
from ksef2.core.protocols import Middleware
from ksef2.domain.models import invoices
from ksef2.domain.models.session import (
    OnlineSessionState,
    SessionInvoiceStatusResponse,
    SessionInvoicesResponse,
    SessionStatusResponse,
)
from ksef2.domain.models.invoices import SendInvoicePayload
from ksef2.endpoints.invoices import InvoicesEndpoints
from ksef2.endpoints.session import SessionEndpoints

from ksef2.infra.mappers.invoices import from_spec as invoice_from_spec
from ksef2.infra.mappers.invoices import to_spec as invoice_to_spec
from ksef2.infra.mappers.sessions import from_spec as session_from_spec

from types import TracebackType

logger = get_logger(__name__)


@final
class OnlineSessionClient:
    """Client bound to a single online invoice session."""

    def __init__(self, transport: Middleware, state: OnlineSessionState):
        self._transport = transport
        self._state = state
        self._invoice_eps = InvoicesEndpoints(transport)
        self._session_eps = SessionEndpoints(transport)
        self._closed = False

    def _ensure_open(self) -> None:
        """Reject operations after the session client has been closed."""
        if self._closed:
            raise exceptions.KSeFClientClosedError("Session client is closed.")

    def send_invoice(self, *, invoice_xml: bytes) -> invoices.SendInvoiceResponse:
        """Encrypt and submit one invoice into the open session."""
        self._ensure_open()
        encrypted = encrypt_invoice(
            xml_bytes=invoice_xml,
            key=base64.b64decode(self._state.aes_key),
            iv=base64.b64decode(self._state.iv),
        )
        request_body = invoice_to_spec(
            SendInvoicePayload(
                xml_bytes=invoice_xml,
                encrypted_bytes=encrypted,
            )
        )

        response_dto = self._invoice_eps.send(
            reference_number=self._state.reference_number,
            body=request_body,
        )

        return invoice_from_spec(response_dto)

    def send_invoice_and_wait(
        self,
        *,
        invoice_xml: bytes,
        timeout: float = 60.0,
        poll_interval: float = 2.0,
    ) -> SessionInvoiceStatusResponse:
        """Submit an invoice and poll until KSeF assigns a final processing result."""
        self._ensure_open()
        result = self.send_invoice(invoice_xml=invoice_xml)
        return self.wait_for_invoice_ready(
            invoice_reference_number=result.reference_number,
            timeout=timeout,
            poll_interval=poll_interval,
        )

    def get_status(self) -> SessionStatusResponse:
        """Fetch the current state of the online session."""
        self._ensure_open()
        return session_from_spec(
            self._invoice_eps.get_session_status(
                reference_number=self._state.reference_number,
            )
        )

    def list_invoices(
        self,
        *,
        page_size: int = 10,
        continuation_token: str | None = None,
    ) -> SessionInvoicesResponse:
        """Fetch one page of invoices submitted in this session."""
        self._ensure_open()
        return session_from_spec(
            self._invoice_eps.list_session_invoices(
                reference_number=self._state.reference_number,
                continuation_token=continuation_token,
                pageSize=page_size,
            )
        )

    def get_invoice_status(
        self, *, invoice_reference_number: str
    ) -> SessionInvoiceStatusResponse:
        """Fetch processing status for one invoice sent in this session."""
        self._ensure_open()
        return session_from_spec(
            self._invoice_eps.get_session_invoice_status(
                reference_number=self._state.reference_number,
                invoice_reference_number=invoice_reference_number,
            )
        )

    def wait_for_invoice_ready(
        self,
        *,
        invoice_reference_number: str,
        timeout: float = 60.0,
        poll_interval: float = 2.0,
    ) -> SessionInvoiceStatusResponse:
        """Poll invoice status until it succeeds, fails, or times out."""
        self._ensure_open()

        retry_predicate: Callable[[SessionInvoiceStatusResponse], bool] = lambda s: (
            not s.ksef_number and s.status.code < 400
        )

        @retry(
            stop=stop_after_delay(timeout),
            wait=wait_fixed(poll_interval),
            retry=retry_if_result(retry_predicate),
            reraise=True,
        )
        def _poll() -> SessionInvoiceStatusResponse:
            return self.get_invoice_status(
                invoice_reference_number=invoice_reference_number
            )

        try:
            status = _poll()
        except RetryError as exc:
            raise exceptions.KSeFInvoiceProcessingTimeoutError(
                invoice_reference_number=invoice_reference_number,
                timeout=timeout,
            ) from exc

        if status.ksef_number:
            return status

        raise exceptions.KSeFSessionError(
            "Invoice processing failed: "
            f"{invoice_reference_number} ({status.status.code}: {status.status.description})"
        )

    def list_failed_invoices(
        self,
        *,
        page_size: int = 10,
        continuation_token: str | None = None,
    ) -> SessionInvoicesResponse:
        """Fetch one page of invoices that failed within this session."""
        self._ensure_open()
        return session_from_spec(
            self._invoice_eps.list_failed_session_invoices(
                reference_number=self._state.reference_number,
                continuation_token=continuation_token,
                pageSize=page_size,
            )
        )

    def get_invoice_upo_by_ksef_number(self, *, ksef_number: str) -> bytes:
        """Download the invoice UPO by KSeF number."""
        self._ensure_open()
        return self._invoice_eps.get_invoice_upo_by_ksef(
            reference_number=self._state.reference_number,
            ksef_number=ksef_number,
        )

    def get_invoice_upo_by_reference(self, *, invoice_reference_number: str) -> bytes:
        """Download the invoice UPO by session invoice reference number."""
        self._ensure_open()
        return self._invoice_eps.get_invoice_upo_by_reference(
            reference_number=self._state.reference_number,
            invoice_reference_number=invoice_reference_number,
        )

    def close(self) -> None:
        if self._closed:
            return

        self._session_eps.terminate_online(
            reference_number=self._state.reference_number,
        )
        self._closed = True

    def get_state(self) -> OnlineSessionState:
        """Return the serializable session state needed to resume later."""
        return self._state

    def __enter__(self) -> OnlineSessionClient:
        self._ensure_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            self.close()
        except exceptions.KSeFException:
            logger.warning(
                "Failed to terminate KSeF session",
                reference_number=self._state.reference_number,
            )
        except httpx.HTTPError:
            logger.warning(
                "Transport error during session termination",
                reference_number=self._state.reference_number,
                exc_info=True,
            )
