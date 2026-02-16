from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import AwareDatetime, AnyUrl, Field

from ksef2.domain.models.base import KSeFBaseModel, KSeFBaseParams


class SortOrder(StrEnum):
    ASC = "Asc"
    DESC = "Desc"


class InvoiceSubjectType(StrEnum):
    """
    Enumeration representing different types of invoice subjects.

    Values:
        Subject1 -> Seller
        Subject2 -> Buyer
        Subject3 -> Other / Third Subject
        SubjectAuthorized -> Authorized Subject
    """

    SUBJECT1 = "Subject1"
    SUBJECT2 = "Subject2"
    SUBJECT3 = "Subject3"
    SUBJECT_AUTHORIZED = "SubjectAuthorized"


class DateType(StrEnum):
    ISSUE = "Issue"
    INVOICING = "Invoicing"
    PERMANENT_STORAGE = "PermanentStorage"


class AmountType(StrEnum):
    BRUTTO = "Brutto"
    NETTO = "Netto"
    VAT = "Vat"


class BuyerIdentifierType(StrEnum):
    NIP = "Nip"
    VAT_UE = "VatUe"
    OTHER = "Other"
    NONE = "None"


class FormType(StrEnum):
    FA = "FA"
    PEF = "PEF"
    RR = "RR"


class InvoiceType(StrEnum):
    VAT = "Vat"
    ZAL = "Zal"
    KOR = "Kor"
    ROZ = "Roz"
    UPR = "Upr"
    KOR_ZAL = "KorZal"
    KOR_ROZ = "KorRoz"
    VAT_PEF = "VatPef"
    VAT_PEF_SP = "VatPefSp"
    KOR_PEF = "KorPef"
    VAT_RR = "VatRr"
    KOR_VAT_RR = "KorVatRr"


class InvoicingMode(StrEnum):
    ONLINE = "Online"
    OFFLINE = "Offline"


class ThirdSubjectIdentifierType(StrEnum):
    NIP = "Nip"
    INTERNAL_ID = "InternalId"
    VAT_UE = "VatUe"
    OTHER = "Other"
    NONE = "None"


# ---------------------------------------------------------------------------
# Existing response model
# ---------------------------------------------------------------------------


class SendInvoiceResponse(KSeFBaseModel):
    """Response from ``POST /sessions/online/{ref}/invoices``."""

    reference_number: str


# ---------------------------------------------------------------------------
# Query / Filter models
# ---------------------------------------------------------------------------


class InvoiceQueryDateRange(KSeFBaseModel):
    date_type: DateType
    from_: AwareDatetime
    to: AwareDatetime | None = None
    restrict_to_hwm_date: bool | None = None


class InvoiceQueryAmount(KSeFBaseModel):
    type: AmountType
    from_: float | None = None
    to: float | None = None


class InvoiceQueryBuyerIdentifier(KSeFBaseModel):
    type: BuyerIdentifierType
    value: str | None = None


class InvoiceQueryParams(KSeFBaseParams):
    sort_order: SortOrder = SortOrder.ASC
    page_offset: int = Field(default=0, ge=0)
    page_size: int = Field(default=10, ge=10, le=250)


class InvoiceQueryFilters(KSeFBaseModel):
    subject_type: InvoiceSubjectType
    date_range: InvoiceQueryDateRange
    ksef_number: str | None = None
    invoice_number: str | None = None
    amount: InvoiceQueryAmount | None = None
    seller_nip: str | None = None
    buyer_identifier: InvoiceQueryBuyerIdentifier | None = None
    currency_codes: list[str] | None = None
    invoicing_mode: InvoicingMode | None = None
    is_self_invoicing: bool | None = None
    form_type: FormType | None = None
    invoice_types: list[InvoiceType] | None = None
    has_attachment: bool | None = None


# ---------------------------------------------------------------------------
# Response models — Invoice Metadata
# ---------------------------------------------------------------------------


class InvoiceMetadataSeller(KSeFBaseModel):
    nip: str
    name: str | None = None


class InvoiceMetadataBuyerIdentifier(KSeFBaseModel):
    type: BuyerIdentifierType
    value: str | None = None


class InvoiceMetadataBuyer(KSeFBaseModel):
    identifier: InvoiceMetadataBuyerIdentifier
    name: str | None = None


class InvoiceMetadataThirdSubjectIdentifier(KSeFBaseModel):
    type: ThirdSubjectIdentifierType
    value: str | None = None


class InvoiceMetadataThirdSubject(KSeFBaseModel):
    identifier: InvoiceMetadataThirdSubjectIdentifier
    name: str | None = None
    role: int


class InvoiceMetadataAuthorizedSubject(KSeFBaseModel):
    nip: str
    name: str | None = None
    role: int


class InvoiceMetadata(KSeFBaseModel):
    ksef_number: str
    invoice_number: str
    issue_date: date
    invoicing_date: AwareDatetime
    acquisition_date: AwareDatetime
    permanent_storage_date: AwareDatetime
    seller: InvoiceMetadataSeller
    buyer: InvoiceMetadataBuyer
    net_amount: float
    gross_amount: float
    vat_amount: float
    currency: str
    invoicing_mode: InvoicingMode
    invoice_type: InvoiceType
    form_code_system: str
    form_code_version: str
    form_code_value: str
    is_self_invoicing: bool
    has_attachment: bool
    invoice_hash: str
    hash_of_corrected_invoice: str | None = None
    third_subjects: list[InvoiceMetadataThirdSubject] | None = None
    authorized_subject: InvoiceMetadataAuthorizedSubject | None = None


class QueryInvoicesMetadataResponse(KSeFBaseModel):
    has_more: bool
    is_truncated: bool
    permanent_storage_hwm_date: AwareDatetime | None = None
    invoices: list[InvoiceMetadata]


# ---------------------------------------------------------------------------
# Response models — Export
# ---------------------------------------------------------------------------


class ExportInvoicesResponse(KSeFBaseModel):
    reference_number: str


class ExportStatusInfo(KSeFBaseModel):
    code: int
    description: str
    details: list[str] | None = None


class PackagePart(KSeFBaseModel):
    ordinal_number: int
    part_name: str
    method: str
    url: AnyUrl
    part_size: int
    part_hash: str
    encrypted_part_size: int
    encrypted_part_hash: str
    expiration_date: AwareDatetime


class InvoicePackage(KSeFBaseModel):
    invoice_count: int
    size: int
    parts: list[PackagePart]
    is_truncated: bool
    last_issue_date: date | None = None
    last_invoicing_date: AwareDatetime | None = None
    last_permanent_storage_date: AwareDatetime | None = None
    permanent_storage_hwm_date: AwareDatetime | None = None


class InvoiceExportStatusResponse(KSeFBaseModel):
    status: ExportStatusInfo
    completed_date: AwareDatetime | None = None
    package_expiration_date: AwareDatetime | None = None
    package: InvoicePackage | None = None
