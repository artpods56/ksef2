# Certificates Module — Architecture Reference

This document describes the architecture patterns used in the certificates module of the KSEF SDK. Use it as a blueprint when refactoring other modules (invoices, permissions, tokens, etc.) to follow the same conventions.

## Project Conventions

- Do not add `from __future__ import annotations` or other `__future__` imports. This project does not use future imports.

## Refactor Lessons

- **Keep online and batch session flows symmetrical.**
  Opening a session should follow one pattern:
  `domain request -> infra.mappers.sessions.to_spec -> endpoint -> infra.mappers.sessions.from_spec -> domain response`
  Avoid introducing a separate one-off mapper class for batch session opening if the same session mapper module can own the conversion.

- **Mapper helpers should return the narrowest domain literal type.**
  If the destination field is `CertificateSubjectIdentifierType`, `AuthorizationSubjectIdentifierType`, `SubunitIdentifierType`, or `EntityIdentifierType`, annotate and return that exact type rather than the broader `IdentifierType`.

- **Do not duplicate supplementary schema models across modules.**
  If a request model is batch-specific, define it once in `infra/schema/api/supp/batch.py`. Do not keep a second model with the same name in `supp/session.py` or another sibling module.

- **When refactoring boundaries, update polyfactory coverage with the code.**
  Add or update fixtures for both domain and spec models, then cover the mapper path in both directions. This is especially important when replacing legacy mapper classes with split `to_spec` / `from_spec` modules.

## Layer Overview

```
Client (orchestration)
  → Mapper/requests (domain → spec)
  → Endpoints (HTTP calls, spec models only)
  → Mapper/responses (spec → domain)
  → returns domain model
```

Each layer has a single responsibility:
- **Domain models** — flat data structures, no logic, no infra dependencies
- **Mappers** — pure structural transformation between domain and spec models
- **Endpoints** — HTTP operations, accept and return spec models
- **Clients** — thin orchestration gluing mappers + endpoints, expose only domain models

---

## 1. Domain Models

**Location**: `src/ksef2/domain/models/certificates.py`

### Rules

- All models extend `KSeFBaseModel` (pydantic `BaseModel` with `extra="forbid"`)
- **Flat structure** — no nested classes, no inner models
- **Pure data** — no methods, no logic
- **snake_case** field names throughout
- Optional fields: `field: Type | None = None`

### String-Constrained Types

Use `type` aliases with `Literal` for the public API:

```python
type CertificateType = Literal["authentication", "offline"]
type CertificateStatus = Literal["active", "blocked", "revoked", "expired"]
type RevocationReason = Literal["unspecified", "superseded", "key_compromise"]
```

These keep the external API string-friendly — users pass `"authentication"` not `CertificateTypeEnum.AUTHENTICATION`.

### StrEnum Mirrors

Each `Literal` type has a corresponding `StrEnum` class used internally by the mapper layer for `singledispatch` registration (Literal type aliases are not classes, so `singledispatch` cannot register on them):

```python
class CertificateTypeEnum(StrEnum):
    AUTHENTICATION = "authentication"
    OFFLINE = "offline"

class CertificateStatusEnum(StrEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    REVOKED = "revoked"
    EXPIRED = "expired"
```

Since `StrEnum` inherits from `str`, enum values are accepted by pydantic where `Literal` strings are expected. The enums are **not** part of the public API.

### List Wrappers

Lists are always wrapped in their own model:

```python
class RetrievedCertificatesList(KSeFBaseModel):
    certificates: list[Certificate]

class CertificatesInfoList(KSeFBaseModel):
    certificates: list[CertificateInfo]
    has_more: bool  # paginated lists include this
```

### Request Models

Request models live in the same file as response models. They use the same `Literal` type aliases:

```python
class EnrollCertificateRequest(KSeFBaseModel):
    certificate_name: str
    certificate_type: CertificateType
    csr: str
    valid_from: datetime | str | None = None
```

Datetime fields in requests accept both `datetime` and `str` for flexibility. Response models use concrete `datetime`.

---

## 2. Mapper Layer

**Location**: `src/ksef2/infra/mappers/certificates/`

```
certificates/
  __init__.py      # re-exports to_spec and from_spec
  requests.py      # domain → spec (singledispatch-based)
  responses.py     # spec → domain (singledispatch-based)
```

### `__init__.py`

```python
from ksef2.infra.mappers.certificates.requests import to_spec
from ksef2.infra.mappers.certificates.responses import from_spec

__all__ = ["to_spec", "from_spec"]
```

### Public API: `to_spec` and `from_spec`

Each module exposes a single polymorphic function with `@overload` signatures for type safety:

```python
@overload
def to_spec(request: EnrollCertificateRequest) -> spec.EnrollCertificateRequest: ...

@overload
def to_spec(request: CertificateType) -> spec.KsefCertificateType: ...

# ... more overloads ...

def to_spec(request: BaseModel | Enum | str) -> object:
    ...
```

### Singledispatch Pattern

Internal dispatch uses `functools.singledispatch`. The public `to_spec`/`from_spec` wraps it:

```python
@singledispatch
def _to_spec(request: BaseModel | Enum | str) -> object:
    raise NotImplementedError(
        f"No mapper registered for {type(request).__name__}. "
        f"Register one with @_to_spec.register"
    )
```

**BaseModel subclasses** register directly:

```python
@_to_spec.register
def _(request: EnrollCertificateRequest) -> spec.EnrollCertificateRequest:
    return spec.EnrollCertificateRequest(
        certificateName=request.certificate_name,
        certificateType=to_spec(request.certificate_type),
        csr=request.csr,
        validFrom=helpers.to_aware_datetime(request.valid_from)
        if request.valid_from
        else None,
    )
```

**StrEnum classes** register for enum-to-enum mapping:

```python
@_to_spec.register
def _(request: CertificateTypeEnum) -> spec.KsefCertificateType:
    match request:
        case CertificateTypeEnum.AUTHENTICATION:
            return spec.KsefCertificateType.Authentication
        case CertificateTypeEnum.OFFLINE:
            return spec.KsefCertificateType.Offline
        case _ as unreachable:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(unreachable)
```

### String → StrEnum Bridging

Since domain models use `Literal` types (which are `str` at runtime), the public `to_spec` function converts strings to the appropriate `StrEnum` before dispatching. This uses the `get_matching_enum` helper:

```python
from ksef2.infra.mappers.helpers import get_matching_enum

# Define which enums are valid for this mapper module
class ValidCertificatesEnums(Enum):
    CertificateType = CertificateTypeEnum
    CertificateStatus = CertificateStatusEnum
    RevocationReason = RevocationReasonEnum
    IdentifierType = IdentifierTypeEnum

VALID_CERT_ENUMS = [v.value for v in ValidCertificatesEnums.__members__.values()]

def to_spec(request: BaseModel | Enum | str) -> object:
    if isinstance(request, str):
        enum_cls = get_matching_enum(request, VALID_CERT_ENUMS)
        if enum_cls is None:
            raise NotImplementedError(f"No mapper for string value: {request!r}")
        return _to_spec(enum_cls(request))
    return _to_spec(request)
```

### Response Mappers (`from_spec`)

Same pattern but mapping spec → domain. Spec enums are real classes, so they register on `singledispatch` directly (no string bridging needed):

```python
@_from_spec.register
def _(response: spec.KsefCertificateType) -> CertificateType:
    match response:
        case spec.KsefCertificateType.Authentication:
            return "authentication"
        case spec.KsefCertificateType.Offline:
            return "offline"
        case _ as unreachable:
            assert_never(unreachable)
```

### Note: Encryption Module Request Mapper

The encryption module defines a `to_spec` mapper even though the endpoint is
response-only. It is used by the client for local filtering logic (e.g., mapping
domain `CertUsage` values to spec `PublicKeyCertificateUsage`). This follows the
same `singledispatch` + string-bridging pattern used in other modules.

### Helpers

**Location**: `src/ksef2/infra/mappers/helpers.py`

```python
def to_aware_datetime(dt: str | datetime) -> datetime:
    """Convert to UTC-aware datetime. Naive datetimes assumed Europe/Warsaw."""

def lookup[_K, _V](mapping: dict[_K, _V], key: _K, label: str) -> _V:
    """Safe dict lookup with descriptive ValueError on missing key."""

def get_matching_enum(value: str, enums: Sequence[type[StrEnum]]) -> type[StrEnum] | None:
    """Find which StrEnum class contains the given string value."""
```

### Conditional Mapping Pattern

Optional datetime fields use this pattern:

```python
validFrom=helpers.to_aware_datetime(request.valid_from)
if request.valid_from
else None,
```

---

## 3. Endpoints Layer

**Location**: `src/ksef2/endpoints/certificates.py`

### Rules

- Decorated with `@final`
- Extends `BaseEndpoints`
- Methods map 1:1 to HTTP operations
- Accept and return **spec models only** (never domain models)
- Use `self._parse(response, TargetModel)` for response deserialization
- Use `body.model_dump(mode="json")` for request serialization
- Route paths come from `ksef2.core.routes`

```python
@final
class CertificatesEndpoints(BaseEndpoints):
    def enroll(
        self, body: spec.EnrollCertificateRequest
    ) -> spec.EnrollCertificateResponse:
        return self._parse(
            self._transport.post(
                path=routes.CertificateRoutes.ENROLLMENT,
                json=body.model_dump(mode="json"),
            ),
            spec.EnrollCertificateResponse,
        )

    def query(
        self,
        body: spec.QueryCertificatesRequest,
        **params: Unpack[OffsetPaginationQueryParams],
    ) -> spec.QueryCertificatesResponse:
        return self._parse(
            self._transport.post(
                path=routes.CertificateRoutes.QUERY,
                params=self.build_params(params),
                json=body.model_dump(mode="json"),
            ),
            spec.QueryCertificatesResponse,
        )
```

Void operations discard the response:

```python
def revoke(self, certificate_serial_number: str, body: spec.RevokeCertificateRequest | None = None) -> None:
    _ = self._transport.post(
        path=routes.CertificateRoutes.REVOKE.format(
            certificateSerialNumber=certificate_serial_number
        ),
        json=body.model_dump(mode="json") if body else None,
    )
```

---

## 4. Client Layer

**Location**: `src/ksef2/clients/certificates.py`

### Rules

- Decorated with `@final`
- Constructor takes `Middleware`, creates endpoints internally
- All public method parameters are **keyword-only** (`*,`)
- Never exposes spec models — accepts and returns domain models only
- Thin orchestration — no business logic

### Pattern

Every method follows the same flow:

```python
def enroll(
    self,
    *,
    certificate_name: str,
    certificate_type: CertificateType,
    csr: str,
    valid_from: datetime | str | None = None,
) -> CertificateEnrollmentResponse:
    # 1. Build domain request model
    request = EnrollCertificateRequest(
        certificate_name=certificate_name,
        certificate_type=certificate_type,
        csr=csr,
        valid_from=valid_from,
    )
    # 2. Map domain → spec
    body = to_spec(request)
    # 3. Call endpoint, map spec → domain
    return from_spec(self._endpoints.enroll(body=body))
```

Simple read operations skip the request model:

```python
def get_limits(self) -> CertificateLimitsResponse:
    return from_spec(self._endpoints.get_limits())
```

Pagination is handled inline:

```python
def query(self, *, ..., params: OffsetPaginationParams | None = None) -> CertificatesInfoList:
    parameters = params or OffsetPaginationParams()
    request = QueryCertificatesRequest(...)
    body = to_spec(request)
    spec_resp = self._endpoints.query(body=body, **parameters.to_query_params())
    return from_spec(spec_resp)
```

### Note: Encryption Client Filtering

`EncryptionClient.get_certificates()` accepts an optional `usage` filter using
domain `CertUsage` values and filters results in-memory using the encryption
request mapper. This keeps the public API string-friendly while reusing mapper
logic.

---

## 5. Test Infrastructure

### Factories

**Location**: `tests/unit/factories/certificates.py`

Two tiers of factories using `polyfactory`:

**Spec model factories** — for testing mappers and endpoints in isolation:

```python
@register_fixture(name="cert_limits_resp")
class CertificateLimitsResponseFactory(
    ModelFactory[spec.CertificateLimitsResponse]
): ...

@register_fixture(name="cert_enroll_resp")
class EnrollCertificateResponseFactory(
    ModelFactory[spec.EnrollCertificateResponse]
): ...
```

**Domain model factories** — for testing request mappers:

```python
@register_fixture(name="domain_enroll_cert_req")
class DomainEnrollCertificateRequestFactory(
    ModelFactory[certificates.EnrollCertificateRequest]
):
    certificate_type: str = "authentication"
    csr: str = VALID_BASE64
```

Important: fields with `Literal` types or constrained values need explicit defaults in the factory, because polyfactory may generate invalid random values.

**Non-fixture factories** — for inline use in tests (not registered as pytest fixtures):

```python
class CertificateListItemFactory(ModelFactory[spec.CertificateListItem]):
    certificateSerialNumber: str = "SN123"
    name: str = "Test Cert"
    commonName: str = "CN=Test"
    type: spec.KsefCertificateType = spec.KsefCertificateType.Authentication
    status: spec.CertificateListItemStatus = spec.CertificateListItemStatus.Active
```

### Conftest

The `tests/unit/conftest.py` wildcard-imports all factory modules to register fixtures:

```python
from tests.unit.factories.certificates import *  # noqa
from tests.unit.factories.encryption import *  # noqa
```

### Test Structure

**Location**: `tests/unit/mappers/certificates.py`

Tests are organized into two classes:

```python
class TestCertificatesMapper:
    """Tests for from_spec (response mappers)"""

    def test_map_limits_response(self, cert_limits_resp: BaseFactory[spec.CertificateLimitsResponse]):
        mapped_input = cert_limits_resp.build()
        output = from_spec(mapped_input)

        assert isinstance(output, certificates.CertificateLimitsResponse)
        assert output.can_request == mapped_input.canRequest
        # ... field-by-field assertions ...

class TestCertificatesRequestMapper:
    """Tests for to_spec (request mappers)"""

    def test_to_spec_enroll_certificate_request(self):
        request = DomainEnrollCertificateRequestFactory.build(valid_from=None)
        output = to_spec(request)

        assert isinstance(output, spec.EnrollCertificateRequest)
        assert output.certificateName == request.certificate_name
        assert output.certificateType == to_spec(request.certificate_type)
        # ...
```

### Coverage Checklist

For each mapper module, ensure every dispatch handler is tested:

**Response mappers (`from_spec`):**
- One test per `@_from_spec.register` handler
- Enum mappers: one test per enum variant
- Composite models: verify nested `from_spec` calls produce correct types
- List models: verify length preservation

**Request mappers (`to_spec`):**
- One test per `@_to_spec.register` handler
- Enum mappers: one test per enum variant
- Models with optional fields: test with `None` and with values
- Conditional datetime fields: test both branches

---

## 6. File Checklist for a Complete Module

When refactoring a module (e.g., `invoices`), create/update these files:

| File | Purpose |
|------|---------|
| `src/ksef2/domain/models/<module>.py` | Domain models, Literal types, StrEnums |
| `src/ksef2/infra/mappers/<module>/__init__.py` | Re-exports `to_spec`, `from_spec` |
| `src/ksef2/infra/mappers/<module>/requests.py` | Domain → spec mappers (singledispatch) |
| `src/ksef2/infra/mappers/<module>/responses.py` | Spec → domain mappers (singledispatch) |
| `src/ksef2/endpoints/<module>.py` | HTTP operations, spec models only |
| `src/ksef2/clients/<module>.py` | Orchestration, domain models only |
| `tests/unit/factories/<module>.py` | Polyfactory factories (spec + domain) |
| `tests/unit/mappers/<module>.py` | Mapper tests (from_spec + to_spec) |
| `tests/unit/clients/test_<module>.py` | Client tests |

---

## 7. Simplified Modules (Responses Only)

Some modules like `peppol` only have response mappers (no request body mapping). In these cases:

**Mapper structure** — only `responses.py` needed:

```
peppol/
  __init__.py      # re-exports only from_spec
  responses.py     # spec → domain (singledispatch-based)
```

**`__init__.py`** — only re-export `from_spec`:

```python
from ksef2.infra.mappers.peppol.responses import from_spec

__all__ = ["from_spec"]
```

**`responses.py`** — same pattern, but only handles response mapping:

```python
from enum import Enum
from functools import singledispatch
from typing import overload

from ksef2.domain.models.peppol import (
    ListPeppolProvidersResponse,
    PeppolProvider,
)
from ksef2.infra.schema.api import spec

from pydantic import BaseModel


@overload
def from_spec(response: spec.PeppolProvider) -> PeppolProvider: ...


@overload
def from_spec(
    response: spec.QueryPeppolProvidersResponse,
) -> ListPeppolProvidersResponse: ...


def from_spec(response: BaseModel | Enum) -> object:
    return _from_spec(response)


@singledispatch
def _from_spec(response: BaseModel | Enum) -> object:
    raise NotImplementedError(...)


@_from_spec.register
def _(response: spec.PeppolProvider) -> PeppolProvider:
    return PeppolProvider(
        id=response.id,
        name=response.name,
        date_created=response.dateCreated,
    )


@_from_spec.register
def _(
    response: spec.QueryPeppolProvidersResponse,
) -> ListPeppolProvidersResponse:
    return ListPeppolProvidersResponse(
        providers=[from_spec(p) for p in response.peppolProviders],
        has_more=response.hasMore,
    )
```

---

## 8. Client Tests

**Location**: `tests/unit/clients/test_<module>.py`

### FakeTransport Setup

The `FakeTransport` class implements the `Middleware` protocol for testing:

```python
# tests/unit/fakes/transport.py
@final
@dataclass()
class FakeTransport(protocols.Middleware):
    calls: list[RecordedCall] = field(default_factory=list)
    responses: list[httpx.Response] = field(default_factory=list)
    # ... methods ...
```

### Conftest Fixture

```python
# tests/unit/clients/conftest.py
import pytest
from ksef2.clients.peppol import PeppolClient
from tests.unit.fakes.transport import FakeTransport


@pytest.fixture
def peppol_client(fake_transport: FakeTransport):
    return PeppolClient(fake_transport)
```

### Test Examples

**Basic query test:**

```python
from ksef2.clients.peppol import PeppolClient
from ksef2.core.routes import PeppolRoutes
from tests.unit.factories.peppol import QueryPeppolProvidersResponseFactory
from tests.unit.fakes.transport import FakeTransport


class TestPeppolClient:
    def test_query(
        self,
        peppol_client: PeppolClient,
        fake_transport: FakeTransport,
        peppol_providers_resp: QueryPeppolProvidersResponseFactory,
    ):
        expected = peppol_providers_resp.build()
        fake_transport.enqueue(expected.model_dump(mode="json"))
        
        response = peppol_client.query()
        
        assert len(response.providers) == len(expected.peppolProviders)
        assert response.has_more == expected.hasMore
```

**Pagination with `all()` method:**

```python
    def test_all_multiple_pages(
        self,
        peppol_client: PeppolClient,
        fake_transport: FakeTransport,
        peppol_providers_resp: QueryPeppolProvidersResponseFactory,
    ):
        page1 = peppol_providers_resp.build(
            peppolProviders=[PeppolProviderFactory.build(id="PPL000001")],
            hasMore=True,
        )
        page2 = peppol_providers_resp.build(
            peppolProviders=[PeppolProviderFactory.build(id="PPL000002")],
            hasMore=False,
        )

        fake_transport.enqueue(page1.model_dump(mode="json"))
        fake_transport.enqueue(page2.model_dump(mode="json"))

        providers = list(peppol_client.all())

        assert len(providers) == 2
        assert len(fake_transport.calls) == 2
```

---

## 9. Common Patterns

### Handling Optional Fields from API

Some API fields may be `null`/empty. Domain models should use `| None`:

```python
# Domain model
class PeppolProvider(KSeFBaseModel):
    name: str | None  # API can return null
```

### String-Validated Fields in Spec

Spec models may have strict validation (e.g., regex patterns). Use explicit values in tests:

```python
# ID must be 9 chars: P + 2 letters + 6 digits
PeppolProviderFactory.build(id="PPL123456")  # OK
# PeppolProviderFactory.build(id="PPL001")  # Fails validation
```

### Keyword-Only Client Parameters

All public client methods should use keyword-only arguments:

```python
def query(
    self,
    *,  # Forces keyword arguments
    params: OffsetPaginationParams | None = None,
) -> ListPeppolProvidersResponse:
    ...
```

---

## 10. Pagination Pattern

The SDK uses a consistent pagination pattern across modules with TypedDict, mixins, and typed query parameters.

### TypedDict in Endpoints

Endpoints define query parameters using `TypedDict` with `NotRequired` for optional fields:

```python
# src/ksef2/endpoints/tokens.py
from typing import NotRequired, TypedDict, Unpack, final

ListTokensQueryParams = TypedDict(
    "ListTokensQueryParams",
    {
        "status": NotRequired[list[str] | None],
        "description": NotRequired[str | None],
        "authorIdentifier": NotRequired[str | None],
        "authorIdentifierType": NotRequired[str | None],
        "pageSize": NotRequired[int | None],
    },
)
_LIST_TOKENS_PARAMS = TypeAdapter(ListTokensQueryParams)


@final
class TokenEndpoints(BaseEndpoints):
    def list_tokens(
        self,
        continuation_token: str | None = None,
        **params: Unpack[ListTokensQueryParams],
    ) -> spec.QueryTokensResponse:
        return self._parse(
            self._transport.get(
                path=routes.TokenRoutes.LIST_TOKENS,
                params=self.build_params(params, _LIST_TOKENS_PARAMS),
                headers=headers,
            ),
            spec.QueryTokensResponse,
        )
```

### Base Params with `to_query_params()`

All pagination params inherit from `KSeFBaseParams`, which provides `to_query_params()`:

```python
# src/ksef2/domain/models/base.py
class KSeFBaseParams[ParamsT](KSeFBaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        use_enum_values=True,
        serialize_by_alias=True,
    )

    def to_query_params(self) -> ParamsT:
        return cast(
            ParamsT, self.model_dump(by_alias=True, exclude_none=True, mode="json")
        )
```

Key features:
- `alias_generator=to_camel` - converts `page_size` to `pageSize` for API
- `use_enum_values=True` - serializes enums as their values
- `to_query_params()` returns a TypedDict typed result

### Mixins

Mixins provide reusable pagination fields:

```python
# src/ksef2/domain/models/pagination.py
class PageSizeMixin(BaseModel):
    page_size: int = Field(default=10, ge=10, le=100)


class PageOffsetMixin(BaseModel):
    page_offset: int = Field(default=0, ge=0)


class SortOrderMixin(BaseModel):
    sort_order: SortOrder = SortOrder.ASC
```

### Token-Based Pagination (Continuation Token)

For endpoints using continuation tokens:

```python
class TokenListParams(KSeFBaseParams[ListTokensQueryParams], PageSizeMixin):
    """GET /tokens"""

    status: list[TokenStatus] | None = None
    description: str | None = None
    author_identifier: str | None = None
    author_identifier_type: TokenAuthorIdentifierType | None = None
```

### Offset-Based Pagination

For endpoints using offset + page size:

```python
class OffsetPaginationParams(
    KSeFBaseParams[OffsetPaginationQueryParams], PageSizeMixin, PageOffsetMixin
):
    def next_page(self) -> Self:
        return self.model_copy(update={"page_offset": self.page_offset + 1})
```

### Client Usage

Clients accept the params model and convert to query params:

```python
# src/ksef2/clients/tokens.py
def list_page(
    self,
    *,
    continuation_token: str | None = None,
    params: TokenListParams | None = None
) -> QueryTokensResponse:
    parameters = params or TokenListParams()
    spec_resp = self._endpoints.list_tokens(
        continuation_token=continuation_token,
        **parameters.to_query_params()
    )
    return from_spec(spec_resp)
```

### Checklist for Adding Pagination

1. **Endpoints layer**: Define `TypedDict` for query params
2. **Domain layer**: Create params model inheriting from `KSeFBaseParams[...]` + mixins
3. **Client layer**: Accept params model, call `to_query_params()`
