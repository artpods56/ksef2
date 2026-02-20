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
        return spec.SendInvoiceRequest(
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


class InvoiceQueryFiltersMapper:
    @staticmethod
    def map_request(
        filters: invoices.InvoiceQueryFilters,
    ) -> spec.InvoiceQueryFilters:
        date_range = spec.InvoiceQueryDateRange(
            dateType=spec.InvoiceQueryDateType(filters.date_range.date_type.value),
            **{"from": filters.date_range.from_},
            to=filters.date_range.to,
            restrictToPermanentStorageHwmDate=filters.date_range.restrict_to_hwm_date,
        )

        amount: spec.InvoiceQueryAmount | None = None
        if filters.amount is not None:
            amount = spec.InvoiceQueryAmount(
                type=spec.AmountType(filters.amount.type.value),
                **{"from": filters.amount.from_},
                to=filters.amount.to,
            )

        buyer_id: spec.InvoiceQueryBuyerIdentifier | None = None
        if filters.buyer_identifier is not None:
            buyer_id = spec.InvoiceQueryBuyerIdentifier(
                type=spec.BuyerIdentifierType(filters.buyer_identifier.type.value),
                value=filters.buyer_identifier.value,
            )

        invoicing_mode: spec.InvoicingMode | None = None
        if filters.invoicing_mode is not None:
            invoicing_mode = spec.InvoicingMode(filters.invoicing_mode.value)

        form_type: spec.InvoiceQueryFormType | None = None
        if filters.form_type is not None:
            form_type = spec.InvoiceQueryFormType(filters.form_type.value)

        invoice_types: list[spec.InvoiceType] | None = None
        if filters.invoice_types is not None:
            invoice_types = [spec.InvoiceType(t.value) for t in filters.invoice_types]

        currency_codes: list[spec.CurrencyCode] | None = None
        if filters.currency_codes is not None:
            currency_codes = [spec.CurrencyCode(c) for c in filters.currency_codes]

        return spec.InvoiceQueryFilters(
            subjectType=spec.InvoiceQuerySubjectType(filters.subject_type.value),
            dateRange=date_range,
            ksefNumber=filters.ksef_number,
            invoiceNumber=filters.invoice_number,
            amount=amount,
            sellerNip=filters.seller_nip,
            buyerIdentifier=buyer_id,
            currencyCodes=currency_codes,
            invoicingMode=invoicing_mode,
            isSelfInvoicing=filters.is_self_invoicing,
            formType=form_type,
            invoiceTypes=invoice_types,
            hasAttachment=filters.has_attachment,
        )


class QueryInvoicesMetadataMapper:
    @staticmethod
    def map_response(
        response: spec.QueryInvoicesMetadataResponse,
    ) -> invoices.QueryInvoicesMetadataResponse:
        return invoices.QueryInvoicesMetadataResponse(
            has_more=response.hasMore,
            is_truncated=response.isTruncated,
            permanent_storage_hwm_date=response.permanentStorageHwmDate,
            invoices=[_map_invoice_metadata(inv) for inv in response.invoices],
        )


class ExportInvoicesMapper:
    @staticmethod
    def map_request(
        filters: invoices.InvoiceQueryFilters,
        encrypted_symmetric_key: str,
        initialization_vector: str,
    ) -> spec.InvoiceExportRequest:
        return spec.InvoiceExportRequest(
            encryption=spec.EncryptionInfo(
                encryptedSymmetricKey=encrypted_symmetric_key,
                initializationVector=initialization_vector,
            ),
            filters=InvoiceQueryFiltersMapper.map_request(filters),
        )

    @staticmethod
    def map_response(
        response: spec.ExportInvoicesResponse,
    ) -> invoices.ExportInvoicesResponse:
        return invoices.ExportInvoicesResponse(
            reference_number=response.referenceNumber,
        )


class ExportStatusMapper:
    @staticmethod
    def map_response(
        response: spec.InvoiceExportStatusResponse,
    ) -> invoices.InvoiceExportStatusResponse:
        package: invoices.InvoicePackage | None = None
        if response.package is not None:
            package = invoices.InvoicePackage(
                invoice_count=response.package.invoiceCount,
                size=response.package.size,
                parts=[
                    invoices.PackagePart(
                        ordinal_number=p.ordinalNumber,
                        part_name=p.partName,
                        method=p.method,
                        url=p.url,
                        part_size=p.partSize,
                        part_hash=p.partHash,
                        encrypted_part_size=p.encryptedPartSize,
                        encrypted_part_hash=p.encryptedPartHash,
                        expiration_date=p.expirationDate,
                    )
                    for p in response.package.parts
                ],
                is_truncated=response.package.isTruncated,
                last_issue_date=response.package.lastIssueDate,
                last_invoicing_date=response.package.lastInvoicingDate,
                last_permanent_storage_date=response.package.lastPermanentStorageDate,
                permanent_storage_hwm_date=response.package.permanentStorageHwmDate,
            )

        return invoices.InvoiceExportStatusResponse(
            status=invoices.ExportStatusInfo(
                code=response.status.code,
                description=response.status.description,
                details=response.status.details,
            ),
            completed_date=response.completedDate,
            package_expiration_date=response.packageExpirationDate,
            package=package,
        )


def _map_invoice_metadata(
    inv: spec.InvoiceMetadata,
) -> invoices.InvoiceMetadata:
    buyer_id = invoices.InvoiceMetadataBuyerIdentifier(
        type=invoices.BuyerIdentifierType(inv.buyer.identifier.type.value),
        value=inv.buyer.identifier.value,
    )

    third_subjects: list[invoices.InvoiceMetadataThirdSubject] | None = None
    if inv.thirdSubjects is not None:
        third_subjects = [
            invoices.InvoiceMetadataThirdSubject(
                identifier=invoices.InvoiceMetadataThirdSubjectIdentifier(
                    type=invoices.ThirdSubjectIdentifierType(ts.identifier.type.value),
                    value=ts.identifier.value,
                ),
                name=ts.name,
                role=ts.role,
            )
            for ts in inv.thirdSubjects
        ]

    authorized_subject: invoices.InvoiceMetadataAuthorizedSubject | None = None
    if inv.authorizedSubject is not None:
        authorized_subject = invoices.InvoiceMetadataAuthorizedSubject(
            nip=inv.authorizedSubject.nip,
            name=inv.authorizedSubject.name,
            role=inv.authorizedSubject.role,
        )

    return invoices.InvoiceMetadata(
        ksef_number=inv.ksefNumber,
        invoice_number=inv.invoiceNumber,
        issue_date=inv.issueDate,
        invoicing_date=inv.invoicingDate,
        acquisition_date=inv.acquisitionDate,
        permanent_storage_date=inv.permanentStorageDate,
        seller=invoices.InvoiceMetadataSeller(
            nip=inv.seller.nip,
            name=inv.seller.name,
        ),
        buyer=invoices.InvoiceMetadataBuyer(
            identifier=buyer_id,
            name=inv.buyer.name,
        ),
        net_amount=inv.netAmount,
        gross_amount=inv.grossAmount,
        vat_amount=inv.vatAmount,
        currency=inv.currency,
        invoicing_mode=invoices.InvoicingMode(inv.invoicingMode.value),
        invoice_type=invoices.InvoiceType(inv.invoiceType.value),
        form_code_system=inv.formCode.systemCode,
        form_code_version=inv.formCode.schemaVersion,
        form_code_value=inv.formCode.value,
        is_self_invoicing=inv.isSelfInvoicing,
        has_attachment=inv.hasAttachment,
        invoice_hash=inv.invoiceHash,
        hash_of_corrected_invoice=inv.hashOfCorrectedInvoice,
        third_subjects=third_subjects,
        authorized_subject=authorized_subject,
    )
