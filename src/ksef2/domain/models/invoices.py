from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, AnyUrl

from ksef2.domain.models.base import KSeFBaseModel
from ksef2.domain.types import CurrencyCodes, KsefInvoiceTypes
from ksef2.domain.models.session import FormSchema


class SortOrder(StrEnum):
    ASC = "Asc"
    DESC = "Desc"


class BuyerIdentifierType(StrEnum):
    NIP = "Nip"
    VAT_UE = "VatUe"
    OTHER = "Other"
    NONE = "None"


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
# Existing response request
# ---------------------------------------------------------------------------


class SendInvoiceResponse(KSeFBaseModel):
    """Response from ``POST /sessions/online/{ref}/invoices``."""

    reference_number: str


class InvoicesMetadataFilter(KSeFBaseModel):
    role: Literal["seller", "buyer", "third_subject", "authorized_subject"]
    date_from: datetime | str
    date_to: datetime | str
    invoice_number: str | None = None
    ksef_number: str | None = None
    amount_min: float | None = None
    amount_max: float | None = None


class Identity(KSeFBaseModel):
    type: Literal["nip"]
    value: str


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


@dataclass(frozen=True)
class ExportHandle:
    """Holds export reference + crypto keys needed to later fetch/decrypt the package."""

    reference_number: str
    aes_key: bytes
    iv: bytes


### Public API ###


class AmountMixin(KSeFBaseModel):
    amount_type: Literal["brutto", "netto", "vat"]
    amount_min: float | None = None
    amount_max: float | None = None


class InvoicesFilter(KSeFBaseModel):
    # role
    role: Literal["buyer", "seller", "third_subject", "authorized_subject"]

    # dates
    date_type: Literal["issue_date", "invoicing_date", "permanent_storage"]
    date_from: datetime | str
    date_to: datetime | str = field(default_factory=datetime.now)
    restrict_to_permanent_storage_hwm_date: bool | None = None

    # currency and amounts
    currency_codes: list[CurrencyCodes] | None = None
    amount_type: Literal["brutto", "netto", "vat"]
    amount_min: float | None = None
    amount_max: float | None = None

    # identification
    seller_nip: str | None = None
    buyer_nip: str | None = None
    buyer_vat_ue: str | None = None
    buyer_other_id: str | None = None
    invoice_number: str | None = None
    ksef_number: str | None = None

    # data
    invoice_schema: FormSchema | None = None
    invoice_types: list[KsefInvoiceTypes] | None = None
    has_attachment: bool | None = None

    # others
    invoicing_mode: Literal["Online", "Offline"] | None = None
    is_self_invoicing: bool | None = None


class ExportInvoicesPayload(KSeFBaseModel):
    filter: InvoicesFilter
    encrypted_symmetric_key: str
    initialization_vector: str


class SendInvoicePayload(KSeFBaseModel):
    xml_bytes: bytes
    encrypted_bytes: bytes
