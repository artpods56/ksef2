from ksef2.domain.models.limits import (
    ApiRateLimits,
    ContextLimits,
    RateLimitValues,
    SessionLimits,
    SubjectCertificateLimits,
    SubjectEnrollmentLimits,
    SubjectLimits,
)
from ksef2.infra.schema.api import spec as spec


class ContextLimitsMapper:
    @staticmethod
    def map_response(r: spec.EffectiveContextLimits) -> ContextLimits:
        return ContextLimits(
            online_session=SessionLimits(
                max_invoice_size_mb=r.onlineSession.maxInvoiceSizeInMB,
                max_invoice_with_attachment_size_mb=r.onlineSession.maxInvoiceWithAttachmentSizeInMB,
                max_invoices=r.onlineSession.maxInvoices,
            ),
            batch_session=SessionLimits(
                max_invoice_size_mb=r.batchSession.maxInvoiceSizeInMB,
                max_invoice_with_attachment_size_mb=r.batchSession.maxInvoiceWithAttachmentSizeInMB,
                max_invoices=r.batchSession.maxInvoices,
            ),
        )

    @staticmethod
    def map_request(limits: ContextLimits) -> spec.SetSessionLimitsRequest:
        return spec.SetSessionLimitsRequest(
            onlineSession=spec.OnlineSessionContextLimitsOverride(
                maxInvoices=limits.online_session.max_invoices,
                maxInvoiceSizeInMB=limits.online_session.max_invoice_size_mb,
                maxInvoiceWithAttachmentSizeInMB=limits.online_session.max_invoice_with_attachment_size_mb,
            ),
            batchSession=spec.BatchSessionContextLimitsOverride(
                maxInvoices=limits.batch_session.max_invoices,
                maxInvoiceSizeInMB=limits.batch_session.max_invoice_size_mb,
                maxInvoiceWithAttachmentSizeInMB=limits.batch_session.max_invoice_with_attachment_size_mb,
            ),
        )


class SubjectLimitsMapper:
    @staticmethod
    def map_response(r: spec.EffectiveSubjectLimits) -> SubjectLimits:
        return SubjectLimits(
            certificate=(
                SubjectCertificateLimits(max_certificates=r.certificate.maxCertificates)
                if r.certificate
                else None
            ),
            enrollment=(
                SubjectEnrollmentLimits(max_enrollments=r.enrollment.maxEnrollments)
                if r.enrollment
                else None
            ),
        )

    @staticmethod
    def map_request(limits: SubjectLimits) -> spec.SetSubjectLimitsRequest:
        return spec.SetSubjectLimitsRequest(
            certificate=(
                spec.CertificateSubjectLimitsOverride(
                    maxCertificates=limits.certificate.max_certificates,
                )
                if limits.certificate is not None
                else None
            ),
            enrollment=(
                spec.EnrollmentSubjectLimitsOverride(
                    maxEnrollments=limits.enrollment.max_enrollments,
                )
                if limits.enrollment is not None
                else None
            ),
        )


class ApiRateLimitsMapper:
    @staticmethod
    def map_response(r: spec.EffectiveApiRateLimits) -> ApiRateLimits:
        def map_values(v: spec.EffectiveApiRateLimitValues) -> RateLimitValues:
            return RateLimitValues(
                per_second=v.perSecond,
                per_minute=v.perMinute,
                per_hour=v.perHour,
            )

        return ApiRateLimits(
            online_session=map_values(r.onlineSession),
            batch_session=map_values(r.batchSession),
            invoice_send=map_values(r.invoiceSend),
            invoice_status=map_values(r.invoiceStatus),
            session_list=map_values(r.sessionList),
            session_invoice_list=map_values(r.sessionInvoiceList),
            session_misc=map_values(r.sessionMisc),
            invoice_metadata=map_values(r.invoiceMetadata),
            invoice_export=map_values(r.invoiceExport),
            invoice_export_status=map_values(r.invoiceExportStatus),
            invoice_download=map_values(r.invoiceDownload),
            other=map_values(r.other),
        )

    @staticmethod
    def map_request(limits: ApiRateLimits) -> spec.SetRateLimitsRequest:
        def map_values(v: RateLimitValues) -> spec.ApiRateLimitValuesOverride:
            return spec.ApiRateLimitValuesOverride(
                perSecond=v.per_second,
                perMinute=v.per_minute,
                perHour=v.per_hour,
            )

        return spec.SetRateLimitsRequest(
            rateLimits=spec.ApiRateLimitsOverride(
                onlineSession=map_values(limits.online_session),
                batchSession=map_values(limits.batch_session),
                invoiceSend=map_values(limits.invoice_send),
                invoiceStatus=map_values(limits.invoice_status),
                sessionList=map_values(limits.session_list),
                sessionInvoiceList=map_values(limits.session_invoice_list),
                sessionMisc=map_values(limits.session_misc),
                invoiceMetadata=map_values(limits.invoice_metadata),
                invoiceExport=map_values(limits.invoice_export),
                invoiceExportStatus=map_values(limits.invoice_export_status),
                invoiceDownload=map_values(limits.invoice_download),
                other=map_values(limits.other),
            )
        )
