from ksef2.domain.models._deprecated._base import KSeFBaseModel


class SessionLimits(KSeFBaseModel):
    max_invoice_size_mb: int
    max_invoice_with_attachment_size_mb: int
    max_invoices: int


class ContextLimits(KSeFBaseModel):
    online_session: SessionLimits
    batch_session: SessionLimits


class SubjectCertificateLimits(KSeFBaseModel):
    max_certificates: int | None = None


class SubjectEnrollmentLimits(KSeFBaseModel):
    max_enrollments: int | None = None


class SubjectLimits(KSeFBaseModel):
    certificate: SubjectCertificateLimits | None = None
    enrollment: SubjectEnrollmentLimits | None = None


class RateLimitValues(KSeFBaseModel):
    per_second: int
    per_minute: int
    per_hour: int


class ApiRateLimits(KSeFBaseModel):
    online_session: RateLimitValues
    batch_session: RateLimitValues
    invoice_send: RateLimitValues
    invoice_status: RateLimitValues
    session_list: RateLimitValues
    session_invoice_list: RateLimitValues
    session_misc: RateLimitValues
    invoice_metadata: RateLimitValues
    invoice_export: RateLimitValues
    invoice_export_status: RateLimitValues
    invoice_download: RateLimitValues
    other: RateLimitValues
