import base64

from ksef2.core.crypto import sha256_b64
from ksef2.infra.schema.api import spec as spec
from ksef2.domain.models import invoices


class SendInvoiceMapper:
    @staticmethod
    def map_request(
        xml_bytes: bytes,
        encrypted_bytes: bytes,
    ) -> spec.SendInvoiceRequest:
        return spec.SendInvoiceRequest.model_construct(
            invoiceHash=sha256_b64(xml_bytes),
            invoiceSize=len(xml_bytes),
            encryptedInvoiceHash=sha256_b64(encrypted_bytes),
            encryptedInvoiceSize=len(encrypted_bytes),
            encryptedInvoiceContent=base64.b64encode(encrypted_bytes).decode(),
        )

    @staticmethod
    def map_response(
        response: spec.SendInvoiceResponse,
    ) -> invoices.SendInvoiceResponse:
        return invoices.SendInvoiceResponse(reference_number=response.referenceNumber)
