from functools import singledispatch
from typing import overload

from pydantic import BaseModel

from ksef2.domain.models.limits import (
    ApiRateLimits,
    ContextLimits,
    RateLimitValues,
    SessionLimits,
    SubjectCertificateLimits,
    SubjectEnrollmentLimits,
    SubjectLimits,
)
from ksef2.infra.schema.api import spec


@overload
def from_spec(response: spec.EffectiveContextLimits) -> ContextLimits: ...


@overload
def from_spec(response: spec.EffectiveSubjectLimits) -> SubjectLimits: ...


@overload
def from_spec(response: spec.EffectiveApiRateLimits) -> ApiRateLimits: ...


def from_spec(response: BaseModel) -> object:
    return _from_spec(response)


@singledispatch
def _from_spec(response: BaseModel) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(response).__name__}. "
        f"Register one with @_from_spec.register"
    )


@_from_spec.register
def _(response: spec.EffectiveContextLimits) -> ContextLimits:
    return ContextLimits(
        online_session=SessionLimits(
            max_invoice_size_mb=response.onlineSession.maxInvoiceSizeInMB,
            max_invoice_with_attachment_size_mb=response.onlineSession.maxInvoiceWithAttachmentSizeInMB,
            max_invoices=response.onlineSession.maxInvoices,
        ),
        batch_session=SessionLimits(
            max_invoice_size_mb=response.batchSession.maxInvoiceSizeInMB,
            max_invoice_with_attachment_size_mb=response.batchSession.maxInvoiceWithAttachmentSizeInMB,
            max_invoices=response.batchSession.maxInvoices,
        ),
    )


@_from_spec.register
def _(response: spec.EffectiveSubjectLimits) -> SubjectLimits:
    return SubjectLimits(
        certificate=(
            SubjectCertificateLimits(
                max_certificates=response.certificate.maxCertificates,
            )
            if response.certificate
            else None
        ),
        enrollment=(
            SubjectEnrollmentLimits(
                max_enrollments=response.enrollment.maxEnrollments,
            )
            if response.enrollment
            else None
        ),
    )


def _map_rate_limit_values(values: spec.EffectiveApiRateLimitValues) -> RateLimitValues:
    return RateLimitValues(
        per_second=values.perSecond,
        per_minute=values.perMinute,
        per_hour=values.perHour,
    )


@_from_spec.register
def _(response: spec.EffectiveApiRateLimits) -> ApiRateLimits:
    return ApiRateLimits(
        online_session=_map_rate_limit_values(response.onlineSession),
        batch_session=_map_rate_limit_values(response.batchSession),
        invoice_send=_map_rate_limit_values(response.invoiceSend),
        invoice_status=_map_rate_limit_values(response.invoiceStatus),
        session_list=_map_rate_limit_values(response.sessionList),
        session_invoice_list=_map_rate_limit_values(response.sessionInvoiceList),
        session_misc=_map_rate_limit_values(response.sessionMisc),
        invoice_metadata=_map_rate_limit_values(response.invoiceMetadata),
        invoice_export=_map_rate_limit_values(response.invoiceExport),
        invoice_export_status=_map_rate_limit_values(response.invoiceExportStatus),
        invoice_download=_map_rate_limit_values(response.invoiceDownload),
        other=_map_rate_limit_values(response.other),
    )
