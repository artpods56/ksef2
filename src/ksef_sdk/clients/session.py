from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ksef_sdk.clients._deprecated._base import BaseSubClient
from ksef_sdk.core._crypto import (
    encrypt_invoice,
    encrypt_symmetric_key,
    generate_session_key,
    select_certificate,
)
from ksef_sdk.core.exceptions import KSeFSessionError
from ksef_sdk.domain.models.auth import SessionContext
from ksef_sdk.domain.models.common import FormSchema
from ksef_sdk.domain.models.invoices import SendInvoiceResponse
from ksef_sdk.domain.models.sessions import (
    OpenOnlineSessionResponse,
    SessionInvoicesResponse,
    SessionStatus,
)
from ksef_sdk.infra.mappers.sessions import (
    OpenOnlineSessionMapper,
    SendInvoiceMapper,
    SessionInvoicesMapper,
    SessionStatusMapper,
)
from ksef_sdk.infra.schema.model import (
    SendInvoiceResponse as SpecSendInvoiceResponse,
    SessionInvoicesResponse as SpecSessionInvoicesResponse,
    SessionStatusResponse as SpecSessionStatusResponse,
)

if TYPE_CHECKING:
    from ksef_sdk.core._certificates import CertificateStore
    from ksef_sdk.core._http import HttpTransport


@dataclass(frozen=True)
class SessionState:
    reference_number: str
    aes_key: bytes
    iv: bytes
    access_token: str


class OnlineSession:
    """Manages the lifecycle of a KSeF online (interactive) session.

    Use as a context manager::

        with client.sessions.open_online(access_token=tokens.access_token) as session:
            session.send_invoice(xml_bytes)
    """

    def __init__(
        self,
        http: HttpTransport,
        certificate_store: CertificateStore,
        access_token: str,
        *,
        form_code: FormSchema = FormSchema.FA3,
    ) -> None:
        self._http = http
        self._certificate_store = certificate_store
        self._access_token = access_token
        self._form_code = form_code
        self._reference_number: str | None = None
        self._aes_key: bytes | None = None
        self._iv: bytes | None = None

    @classmethod
    def _from_context(
        cls,
        http: HttpTransport,
        ctx: SessionContext,
    ) -> OnlineSession:
        """Restore an already-open session from a :class:`SessionContext`."""
        session = cls.__new__(cls)
        session._http = http
        session._certificate_store = None  # type: ignore[assignment]
        session._access_token = ctx.access_token
        session._form_code = FormSchema.FA3
        session._reference_number = ctx.reference_number
        session._aes_key = ctx.aes_key
        session._iv = ctx.iv
        return session

    @property
    def reference_number(self) -> str:
        if self._reference_number is None:
            raise KSeFSessionError("Session has not been opened")
        return self._reference_number

    @property
    def is_open(self) -> bool:
        return self._reference_number is not None

    # -- lifecycle --

    def open(self) -> OpenOnlineSessionResponse:
        """Open the online session on the KSeF side."""
        from ksef_sdk.infra.schema.model import (
            OpenOnlineSessionResponse as SpecOpenResp,
        )

        if self._reference_number is not None:
            raise KSeFSessionError("Session is already open")

        certs = self._certificate_store.get_certificates()
        cert = select_certificate(certs, "SymmetricKeyEncryption")
        self._aes_key, self._iv = generate_session_key()
        encrypted_key = encrypt_symmetric_key(self._aes_key, cert.certificate)

        body = OpenOnlineSessionMapper.map_request(
            encrypted_key, self._iv, self._form_code
        )
        spec_resp = self._http.post_json(
            "/sessions/online",
            json_body=body.model_dump(by_alias=True, exclude_none=True),
            response_model=SpecOpenResp,
            token=self._access_token,
        )
        self._reference_number = spec_resp.referenceNumber
        return OpenOnlineSessionMapper.map_response(spec_resp)

    def send_invoice(self, xml_bytes: bytes) -> SendInvoiceResponse:
        """Encrypt and send an invoice XML within this session."""
        if self._aes_key is None or self._iv is None:
            raise KSeFSessionError("Session has not been opened")

        encrypted = encrypt_invoice(xml_bytes, self._aes_key, self._iv)
        json_body = SendInvoiceMapper.map_request(xml_bytes, encrypted)

        spec_resp = self._http.post_json(
            f"/sessions/online/{self.reference_number}/invoices",
            json_body=json_body,
            response_model=SpecSendInvoiceResponse,
            token=self._access_token,
        )
        return SendInvoiceResponse(reference_number=spec_resp.referenceNumber)

    def close(self) -> None:
        """Close the online session."""
        if self._reference_number is None:
            return
        self._http.post(
            f"/sessions/online/{self._reference_number}/close",
            token=self._access_token,
        )
        self._reference_number = None
        self._aes_key = None
        self._iv = None

    def status(self) -> SessionStatus:
        """Get the current status of the session."""
        spec_resp = self._http.get(
            f"/sessions/{self.reference_number}",
            response_model=SpecSessionStatusResponse,
            token=self._access_token,
        )
        return SessionStatusMapper.map_response(spec_resp)

    # -- serialization / rehydration --

    def to_context(self, environment: str = "TEST") -> SessionContext:
        """Export the current session state for persistence."""
        if self._reference_number is None or self._aes_key is None or self._iv is None:
            raise KSeFSessionError("Session has not been opened")
        return SessionContext(
            reference_number=self._reference_number,
            aes_key=self._aes_key,
            iv=self._iv,
            access_token=self._access_token,
            environment=environment,
        )

    # -- context manager --

    def __enter__(self) -> OnlineSession:
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()


class SessionsClient(BaseSubClient):
    """Sub-client for session management."""

    def open_online(
        self,
        *,
        access_token: str,
        form_code: FormSchema = FormSchema.FA3,
    ) -> OnlineSession:
        """Create an :class:`OnlineSession` context manager."""
        return OnlineSession(
            self._http,
            self._certificate_store,
            access_token,
            form_code=form_code,
        )

    def resume(self, ctx: SessionContext) -> OnlineSession:
        """Restore an already-open session from a :class:`SessionContext`."""
        return OnlineSession._from_context(self._http, ctx)

    def status(self, access_token: str, reference_number: str) -> SessionStatus:
        """``GET /sessions/{referenceNumber}``"""
        spec_resp = self._http.get(
            f"/sessions/{reference_number}",
            response_model=SpecSessionStatusResponse,
            token=access_token,
        )
        return SessionStatusMapper.map_response(spec_resp)

    def invoices(
        self,
        access_token: str,
        reference_number: str,
        *,
        continuation_token: str | None = None,
    ) -> SessionInvoicesResponse:
        """``GET /sessions/{referenceNumber}/invoices``"""
        path = f"/sessions/{reference_number}/invoices"
        if continuation_token:
            path += f"?continuationToken={continuation_token}"
        spec_resp = self._http.get(
            path,
            response_model=SpecSessionInvoicesResponse,
            token=access_token,
        )
        return SessionInvoicesMapper.map_response(spec_resp)
