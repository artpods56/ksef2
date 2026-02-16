# Plan: Implement Remaining Invoice Endpoints

## Context
The KSeF SDK currently covers 40/77 (52%) of the API. Three invoice-related endpoints are missing:
- `POST /invoices/query/metadata` — Query invoice metadata with filters
- `POST /invoices/exports` — Start async invoice export
- `GET /invoices/exports/{referenceNumber}` — Get export status

All spec (OpenAPI) models already exist in `src/ksef2/infra/schema/api/spec/models.py`. The SDK pattern requires: spec models -> mapper -> domain models -> service -> client.

## Files to Create/Modify

### 1. Domain models: `src/ksef2/domain/models/invoices.py` (edit existing)

Add full-depth domain models (snake_case, `KSeFBaseModel`-based):

**Enums** (re-export from spec where values are identical):
- `SortOrder` (Asc, Desc)
- `SubjectType` (Subject1, Subject2, Subject3, SubjectAuthorized)
- `DateType` (Issue, Invoicing, PermanentStorage)
- `AmountType` (Brutto, Netto, Vat)
- `BuyerIdentifierType` (Nip, VatUe, Other, None_)
- `FormType` (FA, PEF, RR)
- `InvoiceType` (Vat, Zal, Kor, ...)
- `InvoicingMode` (Online, Offline)

**Query/Filter models:**
- `InvoiceQueryDateRange(date_type, from_, to, restrict_to_hwm_date)`
- `InvoiceQueryAmount(type, from_, to)`
- `InvoiceQueryBuyerIdentifier(type, value)`
- `InvoiceQueryFilters(subject_type, date_range, ksef_number, invoice_number, amount, seller_nip, buyer_identifier, currency_codes, invoicing_mode, is_self_invoicing, form_type, invoice_types, has_attachment)`

**Response models:**
- `InvoiceMetadataSeller(nip, name)`
- `InvoiceMetadataBuyerIdentifier(type, value)`
- `InvoiceMetadataBuyer(identifier, name)`
- `InvoiceMetadataThirdSubjectIdentifier(type, value)`
- `InvoiceMetadataThirdSubject(identifier, name, role)`
- `InvoiceMetadataAuthorizedSubject(nip, name, role)`
- Reuse `FormSchema` from `domain/models/session.py` for form code mapping (maps spec `FormCode` to existing `FormSchema` enum)
- `InvoiceMetadata(ksef_number, invoice_number, issue_date, invoicing_date, acquisition_date, permanent_storage_date, seller, buyer, net_amount, gross_amount, vat_amount, currency, invoicing_mode, invoice_type, form_schema, is_self_invoicing, has_attachment, invoice_hash, hash_of_corrected_invoice, third_subjects, authorized_subject)`
- `QueryInvoicesMetadataResponse(has_more, is_truncated, permanent_storage_hwm_date, invoices)`
- `ExportInvoicesResponse(reference_number)`
- `ExportStatusInfo(code, description, details)`
- `PackagePart(ordinal_number, part_name, method, url, part_size, part_hash, encrypted_part_size, encrypted_part_hash, expiration_date)`
- `InvoicePackage(invoice_count, size, parts, is_truncated, last_issue_date, last_invoicing_date, last_permanent_storage_date, permanent_storage_hwm_date)`
- `InvoiceExportStatusResponse(status, completed_date, package_expiration_date, package)`

### 2. Mapper: `src/ksef2/infra/mappers/invoices.py` (edit existing)

Add mapper classes following the existing pattern (static `map_request`/`map_response` methods):

- `InvoiceQueryFiltersMapper.map_request(domain_filters) -> spec.InvoiceQueryFilters` — maps domain filter model to spec model
- `QueryInvoicesMetadataMapper.map_response(spec_resp) -> domain.QueryInvoicesMetadataResponse` — maps full response including nested InvoiceMetadata list
- `ExportInvoicesMapper.map_request(domain_filters, encryption_info) -> spec.InvoiceExportRequest`
- `ExportInvoicesMapper.map_response(spec_resp) -> domain.ExportInvoicesResponse`
- `ExportStatusMapper.map_response(spec_resp) -> domain.InvoiceExportStatusResponse`

### 3. Endpoints: `src/ksef2/endpoints/invoices.py` (edit existing)

Add 3 endpoint classes:

**`QueryInvoicesMetadataEndpoint`** (`POST /invoices/query/metadata`)
- Query params via TypedDict: `sortOrder` (str|None), `pageOffset` (int|None), `pageSize` (int|None)
- POST with `json=body` (dict from `InvoiceQueryFilters.model_dump()`)
- Returns `spec.QueryInvoicesMetadataResponse`

**`ExportInvoicesEndpoint`** (`POST /invoices/exports`)
- No query params
- POST with `json=body` (dict from `InvoiceExportRequest.model_dump()`)
- Returns `spec.ExportInvoicesResponse`

**`GetExportStatusEndpoint`** (`GET /invoices/exports/{referenceNumber}`)
- Path param: `referenceNumber` via `get_url()`
- Returns `spec.InvoiceExportStatusResponse`

### 4. Registry: `src/ksef2/endpoints/__init__.py` (edit)

Add `__invoices_query_endpoints__` list with the 3 new `EndpointRef` entries, include in `__all_endpoints__`.

### 5. Service: `src/ksef2/services/invoices.py` (create new)

`InvoicesService` class with:
- `query_metadata(access_token, filters, sort_order, page_offset, page_size) -> domain.QueryInvoicesMetadataResponse`
- `export(access_token, filters, encryption_info) -> domain.ExportInvoicesResponse`
- `get_export_status(access_token, reference_number) -> domain.InvoiceExportStatusResponse`

Each method: creates spec request via mapper -> calls endpoint -> maps response via mapper -> returns domain model.

### 6. Client: `src/ksef2/clients/base.py` (edit)

Add `invoices` cached_property returning `InvoicesService(self._transport)`.

### 7. Domain models re-export: `src/ksef2/domain/models/__init__.py` (edit)

Add new domain model exports.

### 8. Unit tests: `tests/unit/test_invoices_query_endpoints.py` (create new)

Following existing test pattern:
- `TestQueryInvoicesMetadataEndpoint` — URL, POST method, bearer header, query params, body forwarding
- `TestExportInvoicesEndpoint` — URL, POST method, bearer header, body forwarding
- `TestGetExportStatusEndpoint` — URL with path param, GET method, bearer header

### 9. Mapper unit tests: `tests/unit/test_invoices_mappers.py` (create new)

Test mapper round-trips for query filters and response mapping.

## Verification
```bash
just coverage   # Should show 3 fewer missing endpoints (34 instead of 37)
just test       # All unit tests pass
just typecheck  # No type errors
just lint       # No lint errors
```
