from __future__ import annotations

import base64
from typing import TYPE_CHECKING

from ksef_sdk.core._crypto import (
    encrypt_invoice,
    encrypt_symmetric_key,
    generate_session_key,
    select_certificate,
    sha256_b64,
)
from ksef_sdk.infra.schema.model import (
    FormCode,
    OpenOnlineSessionResponse,
    PublicKeyCertificate,
    SendInvoiceResponse,
    SessionStatusResponse,
)
from ksef_sdk.core.exceptions import KSeFSessionError

if TYPE_CHECKING:
    from ksef_sdk.core._http import HttpTransport


class OnlineSession:
    """Manages the lifecycle of a KSeF online (interactive) session.

    Use as a context manager::

        with OnlineSession(http, certificates) as session:
            session.send_invoice(xml_bytes)
    """

    def __init__(
        self,
        http: HttpTransport,
        certificates: list[PublicKeyCertificate],
        *,
        form_code: FormCode | None = None,
    ) -> None:
        self._http = http
        self._certificates = certificates
        self._form_code = form_code or FormCode(
            systemCode="FA (3)",
            schemaVersion="1-0E",
            value="FA",
        )
        self._reference_number: str | None = None
        self._aes_key: bytes | None = None
        self._iv: bytes | None = None

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
        if self._reference_number is not None:
            raise KSeFSessionError("Session is already open")

        cert = select_certificate(self._certificates, "SymmetricKeyEncryption")
        self._aes_key, self._iv = generate_session_key()
        encrypted_key = encrypt_symmetric_key(self._aes_key, cert.certificate)

        # Build the JSON body directly — Pydantic's Base64Str serializer
        # cannot handle binary data via model_construct (double-encodes strings,
        # errors on raw bytes).
        body_json = {
            "formCode": self._form_code.model_dump(by_alias=True),
            "encryption": {
                "encryptedSymmetricKey": encrypted_key,
                "initializationVector": base64.b64encode(self._iv).decode(),
            },
        }
        resp = self._http.post_json(
            "/sessions/online",
            json_body=body_json,
            response_model=OpenOnlineSessionResponse,
        )
        self._reference_number = resp.referenceNumber
        return resp

    def send_invoice(self, xml_bytes: bytes) -> SendInvoiceResponse:
        """Encrypt and send an invoice XML within this session."""
        if self._aes_key is None or self._iv is None:
            raise KSeFSessionError("Session has not been opened")

        encrypted = encrypt_invoice(xml_bytes, self._aes_key, self._iv)

        body_json = {
            "invoiceHash": sha256_b64(xml_bytes),
            "invoiceSize": len(xml_bytes),
            "encryptedInvoiceHash": sha256_b64(encrypted),
            "encryptedInvoiceSize": len(encrypted),
            "encryptedInvoiceContent": base64.b64encode(encrypted).decode(),
        }
        return self._http.post_json(
            f"/sessions/online/{self.reference_number}/invoices",
            json_body=body_json,
            response_model=SendInvoiceResponse,
        )

    def close(self) -> None:
        """Close the online session."""
        if self._reference_number is None:
            return  # already closed / never opened
        self._http.post(f"/sessions/online/{self._reference_number}/close")
        self._reference_number = None
        self._aes_key = None
        self._iv = None

    def status(self) -> SessionStatusResponse:
        """Get the current status of the session."""
        return self._http.get(
            f"/sessions/{self.reference_number}",
            response_model=SessionStatusResponse,
        )

    # -- context manager --

    def __enter__(self) -> OnlineSession:
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()
