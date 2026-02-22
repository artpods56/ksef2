"""Tests for invoice query/export mapper classes."""

from __future__ import annotations

from datetime import date, datetime, timezone

from ksef2.domain.models.invoices import (
    AmountType,
    BuyerIdentifierType,
    DateType,
    FormType,
    InvoiceQueryAmount,
    InvoiceQueryBuyerIdentifier,
    InvoiceQueryDateRange,
    InvoiceQueryFilters,
    InvoiceType,
    InvoicingMode,
    InvoiceSubjectType,
)
from ksef2.infra.mappers.requests.invoices import (
    ExportInvoicesMapper,
    ExportStatusMapper,
    InvoiceQueryFiltersMapper,
    QueryInvoicesMetadataMapper,
)
from pydantic import AnyUrl

from ksef2.infra.schema.api import spec as spec


def _minimal_domain_filters() -> InvoiceQueryFilters:
    return InvoiceQueryFilters(
        subject_type=InvoiceSubjectType.SELLER,
        date_range=InvoiceQueryDateRange(
            date_type=DateType.ISSUE,
            from_=datetime(2026, 1, 1, tzinfo=timezone.utc),
        ),
    )


_HASH_44 = "WO86CC+1Lef11wEosItld/NPwxGN8tobOMLqk9PQjgs="


def _minimal_spec_invoice() -> spec.InvoiceMetadata:
    return spec.InvoiceMetadata(
        ksefNumber="9999999999-20250101-AABBCC-DDEEFF-01",
        invoiceNumber="FV/2026/001",
        issueDate=date(2026, 1, 15),
        invoicingDate=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
        acquisitionDate=datetime(2026, 1, 15, 10, 1, tzinfo=timezone.utc),
        permanentStorageDate=datetime(2026, 1, 15, 10, 2, tzinfo=timezone.utc),
        seller=spec.InvoiceMetadataSeller(nip="9999999999", name="Seller"),
        buyer=spec.InvoiceMetadataBuyer(
            identifier=spec.InvoiceMetadataBuyerIdentifier(
                type=spec.BuyerIdentifierType.Nip, value="1111111111"
            ),
            name="Buyer",
        ),
        netAmount=100.0,
        grossAmount=123.0,
        vatAmount=23.0,
        currency="PLN",
        invoicingMode=spec.InvoicingMode.Online,
        invoiceType=spec.InvoiceType.Vat,
        formCode=spec.FormCode(systemCode="FA (3)", schemaVersion="1-0E", value="FA"),
        isSelfInvoicing=False,
        hasAttachment=False,
        invoiceHash=_HASH_44,
    )


class TestInvoiceQueryFiltersMapper:
    def test_maps_minimal_filters(self) -> None:
        filters = _minimal_domain_filters()
        result = InvoiceQueryFiltersMapper.map_request(filters)

        assert isinstance(result, spec.InvoiceQueryFilters)
        assert result.subjectType == spec.InvoiceQuerySubjectType.Subject1
        assert result.dateRange.dateType == spec.InvoiceQueryDateType.Issue

    def test_maps_optional_fields(self) -> None:
        filters = InvoiceQueryFilters(
            subject_type=InvoiceSubjectType.BUYER,
            date_range=InvoiceQueryDateRange(
                date_type=DateType.INVOICING,
                from_=datetime(2026, 1, 1, tzinfo=timezone.utc),
                to=datetime(2026, 3, 1, tzinfo=timezone.utc),
            ),
            amount=InvoiceQueryAmount(type=AmountType.BRUTTO, from_=100.0, to=500.0),
            buyer_identifier=InvoiceQueryBuyerIdentifier(
                type=BuyerIdentifierType.NIP, value="1111111111"
            ),
            invoicing_mode=InvoicingMode.ONLINE,
            form_type=FormType.FA,
            invoice_types=[InvoiceType.VAT, InvoiceType.KOR],
            currency_codes=["PLN", "EUR"],
            is_self_invoicing=False,
            has_attachment=True,
            seller_nip="9999999999",
        )
        result = InvoiceQueryFiltersMapper.map_request(filters)

        assert result.amount is not None
        assert result.amount.type == spec.AmountType.Brutto
        assert result.buyerIdentifier is not None
        assert result.buyerIdentifier.type == spec.BuyerIdentifierType.Nip
        assert result.invoicingMode == spec.InvoicingMode.Online
        assert result.formType == spec.InvoiceQueryFormType.FA
        assert result.invoiceTypes is not None
        assert len(result.invoiceTypes) == 2
        assert result.currencyCodes is not None
        assert len(result.currencyCodes) == 2
        assert result.sellerNip == "9999999999"
        assert result.hasAttachment is True


class TestQueryInvoicesMetadataMapper:
    def test_maps_empty_response(self) -> None:
        spec_resp = spec.QueryInvoicesMetadataResponse(
            hasMore=False,
            isTruncated=False,
            permanentStorageHwmDate=None,
            invoices=[],
        )
        result = QueryInvoicesMetadataMapper.map_response(spec_resp)

        assert result.has_more is False
        assert result.is_truncated is False
        assert result.invoices == []

    def test_maps_invoice_metadata(self) -> None:
        spec_resp = spec.QueryInvoicesMetadataResponse(
            hasMore=True,
            isTruncated=False,
            permanentStorageHwmDate=None,
            invoices=[_minimal_spec_invoice()],
        )
        result = QueryInvoicesMetadataMapper.map_response(spec_resp)

        assert len(result.invoices) == 1
        inv = result.invoices[0]
        assert inv.ksef_number == "9999999999-20250101-AABBCC-DDEEFF-01"
        assert inv.invoice_number == "FV/2026/001"
        assert inv.seller.nip == "9999999999"
        assert inv.buyer.identifier.type == BuyerIdentifierType.NIP
        assert inv.net_amount == 100.0
        assert inv.form_code_system == "FA (3)"
        assert inv.form_code_value == "FA"


class TestExportInvoicesMapper:
    def test_map_request(self) -> None:
        filters = _minimal_domain_filters()
        result = ExportInvoicesMapper.map_request(filters, "enc_key_b64", "iv_b64")

        assert isinstance(result, spec.InvoiceExportRequest)
        assert result.encryption.encryptedSymmetricKey == "enc_key_b64"
        assert result.encryption.initializationVector == "iv_b64"
        assert result.filters.subjectType == spec.InvoiceQuerySubjectType.Subject1

    def test_map_response(self) -> None:
        spec_resp = spec.ExportInvoicesResponse(
            referenceNumber="12345678-1234-1234-1234-123456789012",
        )
        result = ExportInvoicesMapper.map_response(spec_resp)
        assert result.reference_number == "12345678-1234-1234-1234-123456789012"


class TestExportStatusMapper:
    def test_maps_in_progress(self) -> None:
        spec_resp = spec.InvoiceExportStatusResponse(
            status=spec.StatusInfo(code=100, description="In progress"),
            completedDate=None,
            packageExpirationDate=None,
            package=None,
        )
        result = ExportStatusMapper.map_response(spec_resp)

        assert result.status.code == 100
        assert result.package is None

    def test_maps_completed_with_package(self) -> None:
        completed = datetime(2026, 2, 1, 12, 0, tzinfo=timezone.utc)
        expiry = datetime(2026, 2, 8, 12, 0, tzinfo=timezone.utc)
        part_expiry = datetime(2026, 2, 8, 12, 0, tzinfo=timezone.utc)

        spec_resp = spec.InvoiceExportStatusResponse(
            status=spec.StatusInfo(code=200, description="Completed"),
            completedDate=completed,
            packageExpirationDate=expiry,
            package=spec.InvoicePackage(
                invoiceCount=5,
                size=1024,
                parts=[
                    spec.InvoicePackagePart(
                        ordinalNumber=1,
                        partName="part-001.zip",
                        method="GET",
                        url=AnyUrl("https://example.com/part1"),
                        partSize=512,
                        partHash=_HASH_44,
                        encryptedPartSize=600,
                        encryptedPartHash=_HASH_44,
                        expirationDate=part_expiry,
                    ),
                ],
                isTruncated=False,
            ),
        )
        result = ExportStatusMapper.map_response(spec_resp)

        assert result.status.code == 200
        assert result.completed_date == completed
        assert result.package is not None
        assert result.package.invoice_count == 5
        assert len(result.package.parts) == 1
        assert result.package.parts[0].part_name == "part-001.zip"
        assert result.package.parts[0].part_size == 512
