import base64
from typing import final

from ksef2.core.crypto import encrypt_symmetric_key, generate_session_key
from ksef2.core.protocols import Middleware
from ksef2.domain.models.invoices import (
    ExportHandle,
    ExportInvoicesPayload,
    InvoiceExportStatusResponse,
    InvoicesFilter,
    QueryInvoicesMetadataResponse,
)
from ksef2.domain.models.pagination import InvoiceMetadataParams
from ksef2.endpoints.invoices import InvoicesEndpoints
from ksef2.infra.mappers.invoices import from_spec, to_spec


@final
class InvoicesClient:
    def __init__(self, transport: Middleware) -> None:
        self._endpoints = InvoicesEndpoints(transport)

    def query_metadata(
        self,
        *,
        filters: InvoicesFilter,
        params: InvoiceMetadataParams | None = None,
    ) -> QueryInvoicesMetadataResponse:
        request = to_spec(filters)
        parameters = params or InvoiceMetadataParams()
        spec_resp = self._endpoints.query_metadata(
            body=request,
            **parameters.to_query_params(),
        )
        return from_spec(spec_resp)

    def download_invoice(self, *, ksef_number: str) -> bytes:
        return self._endpoints.download(ksef_number=ksef_number)

    def schedule_export(
        self,
        *,
        filters: InvoicesFilter,
        encryption_certificate: str,
    ) -> ExportHandle:
        aes_key, iv = generate_session_key()
        encrypted_key = encrypt_symmetric_key(
            key=aes_key,
            cert_b64=encryption_certificate,
        )
        spec_request = to_spec(
            ExportInvoicesPayload(
                filter=filters,
                encrypted_symmetric_key=base64.b64encode(encrypted_key).decode(),
                initialization_vector=base64.b64encode(iv).decode(),
            )
        )
        spec_resp = self._endpoints.export(body=spec_request)
        resp = from_spec(spec_resp)
        return ExportHandle(
            reference_number=resp.reference_number,
            aes_key=aes_key,
            iv=iv,
        )

    def get_export_status(
        self,
        *,
        reference_number: str,
    ) -> InvoiceExportStatusResponse:
        spec_resp = self._endpoints.get_export_status(
            reference_number=reference_number,
        )
        return from_spec(spec_resp)
