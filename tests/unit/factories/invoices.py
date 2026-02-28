from ksef2.infra.schema.api import spec
from ksef2.infra.schema.api.supp.invoices import (
    InvoiceExportRequest,
    QueryInvoicesMetadataRequest,
    SendInvoiceRequest,
)
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="inv_query_metadata_req")
class QueryInvoicesMetadataRequestFactory(
    ModelFactory[QueryInvoicesMetadataRequest]
): ...


@register_fixture(name="inv_query_metadata_resp")
class QueryInvoicesMetadataResponseFactory(
    ModelFactory[spec.QueryInvoicesMetadataResponse]
): ...


@register_fixture(name="inv_export_req")
class InvoiceExportRequestFactory(ModelFactory[InvoiceExportRequest]): ...


@register_fixture(name="inv_export_resp")
class ExportInvoicesResponseFactory(ModelFactory[spec.ExportInvoicesResponse]): ...


@register_fixture(name="inv_export_status_resp")
class InvoiceExportStatusResponseFactory(
    ModelFactory[spec.InvoiceExportStatusResponse]
): ...


@register_fixture(name="inv_send_req")
class SendInvoiceRequestFactory(ModelFactory[SendInvoiceRequest]): ...


@register_fixture(name="inv_send_resp")
class SendInvoiceResponseFactory(ModelFactory[spec.SendInvoiceResponse]): ...


@register_fixture(name="inv_session_status_resp")
class SessionStatusResponseFactory(ModelFactory[spec.SessionStatusResponse]): ...


@register_fixture(name="inv_session_invoices_resp")
class SessionInvoicesResponseFactory(ModelFactory[spec.SessionInvoicesResponse]): ...


@register_fixture(name="inv_session_invoice_status_resp")
class SessionInvoiceStatusResponseFactory(
    ModelFactory[spec.SessionInvoiceStatusResponse]
): ...
