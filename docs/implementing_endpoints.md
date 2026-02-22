# Implementing New KSeF API Endpoints

This guide documents the process for implementing new endpoints in the KSeF SDK.

## Overview

The SDK follows a layered architecture:
```
Client → Service → Mapper → Endpoint → HTTP Transport
                     ↕          ↕
              Domain Models   infra/schema (OpenAPI spec models)
```

- **Spec models** (`src/ksef2/infra/schema/api/spec/models.py`): Auto-generated Pydantic models from OpenAPI. Use camelCase field names. Never modify manually.
- **Domain models** (`src/ksef2/domain/models/`): Python-idiomatic models with snake_case fields, extending `KSeFBaseModel`. These are the public API.
- **Mappers** (`src/ksef2/infra/mappers/`): Static classes that translate between spec ↔ domain models. Each mapper has `map_request()` and/or `map_response()` methods.
- **Endpoints** (`src/ksef2/endpoints/`): Thin HTTP wrappers that accept spec models (as dicts) and return spec models.
- **Services** (`src/ksef2/services/`): Orchestrate mapper + endpoint calls. Accept and return domain models.
- **Client** (`src/ksef2/clients/base.py`): Entry point that exposes services as cached properties.

## Process

### Step 1: Find the API Specification

1. Check the OpenAPI spec at `openapi.json` for the endpoint definition
2. Note the:
   - HTTP method (GET, POST, DELETE, etc.)
   - URL path (e.g., `/auth/sessions`)
   - Request/response schemas
   - Query parameters, headers, authentication requirements

**Example** (from `openapi.json`):
```json
"/auth/sessions": {
  "get": {
    "tags": ["Aktywne sesje"],
    "summary": "Pobranie listy aktywnych sesji",
    "parameters": [
      {"name": "pageSize", "in": "query", ...},
      {"name": "x-continuation-token", "in": "header", ...}
    ],
    "responses": {
      "200": {
        "content": {
          "application/json": {
            "schema": {"$ref": "#/components/schemas/AuthenticationListResponse"}
          }
        }
      }
    }
  }
}
```

### Step 2: Check Existing Schema Models

The SDK auto-generates Pydantic models from OpenAPI in `src/ksef2/infra/schema/api/spec/models.py`.

**Search for existing models:**
```bash
grep -n "class ModelName" src/ksef2/infra/schema/api/spec/models.py
```

If the model doesn't exist, regenerate the schema:
```bash
just regenerate-models
```

### Step 3: Create Domain Models

Create or extend domain models in `src/ksef2/domain/models/`. These use snake_case and extend `KSeFBaseModel`:

```python
from __future__ import annotations
from enum import StrEnum
from ksef2.domain.models.base import KSeFBaseModel


class TokenStatus(StrEnum):
    PENDING = "Pending"
    ACTIVE = "Active"
    REVOKED = "Revoked"


class GenerateTokenResponse(KSeFBaseModel):
    reference_number: str
    token: str
```

**Key rules:**
- All models extend `KSeFBaseModel` (which sets `extra="forbid"`)
- Use snake_case field names (unlike spec models which use camelCase)
- Use Python `StrEnum` for enums
- Re-export new models from `src/ksef2/domain/models/__init__.py`
- Reuse existing domain types where possible (e.g., `FormSchema` from `session.py`)

### Step 4: Create Mappers

Add mapper classes in `src/ksef2/infra/mappers/`. Each mapper translates between spec and domain models:

**Example** (from `mappers/tokens.py`):
```python
from ksef2.domain.models.tokens import GenerateTokenResponse, TokenPermission
from ksef2.infra.schema.api import spec as spec


class GenerateTokenMapper:
    @staticmethod
    def map_request(
        permissions: list[TokenPermission],
        description: str,
    ) -> spec.GenerateTokenRequest:
        return spec.GenerateTokenRequest(
            permissions=[spec.TokenPermissionType(p.value) for p in permissions],
            description=description,
        )

    @staticmethod
    def map_response(r: spec.GenerateTokenResponse) -> GenerateTokenResponse:
        return GenerateTokenResponse(
            reference_number=r.referenceNumber,
            token=r.token,
        )
```

**Key patterns:**
- `map_request()`: domain model → spec model (for request bodies)
- `map_response()`: spec model → domain model (for API responses)
- All methods are `@staticmethod`
- Map camelCase (spec) ↔ snake_case (domain)
- For nested objects, map each level explicitly

### Step 5: Implement the Endpoint Class

Create the endpoint in the appropriate file under `src/ksef2/endpoints/`.

**Example** (from `endpoints/auth.py`):
```python
from typing import final
from urllib.parse import urlencode

from ksef2.core import headers, codecs, middleware
from ksef2.infra.schema.api import spec as spec


@final
class ListActiveSessionsEndpoint:
    url: str = "/auth/sessions"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(
        self,
        bearer_token: str,
        *,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ) -> spec.AuthenticationListResponse:
        # Build headers
        headers_dict = headers.KSeFHeaders.bearer(bearer_token)
        if continuation_token:
            headers_dict["x-continuation-token"] = continuation_token

        # Build query string (if needed)
        query_params: list[tuple[str, str]] = []
        if page_size is not None:
            query_params.append(("pageSize", str(page_size)))

        query_string = urlencode(query_params) if query_params else ""
        path = f"{self.url}?{query_string}" if query_string else self.url

        # Make request and parse response
        return codecs.JsonResponseCodec.parse(
            self._transport.get(path, headers=headers_dict),
            spec.AuthenticationListResponse,
        )


@final
class TerminateCurrentSessionEndpoint:
    url: str = "/auth/sessions/current"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> None:
        _ = self._transport.delete(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )


@final
class TerminateAuthSessionEndpoint:
    url: str = "/auth/sessions/{referenceNumber}"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(self, bearer_token: str, reference_number: str) -> None:
        _ = self._transport.delete(
            self.get_url(reference_number=reference_number),
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )
```

**Key patterns:**
- Use `@final` decorator for type safety
- Use `spec.ModelName` for request/response types from OpenAPI
- Use `headers.KSeFHeaders.bearer(token)` for authenticated requests
- Use `codecs.JsonResponseCodec.parse()` to parse responses
- Return `None` for 204 No Content responses

### Step 6: Register the Endpoint

Add the endpoint to `src/ksef2/endpoints/__init__.py`:

```python
__auth_endpoints__ = [
    # ... existing endpoints ...
    EndpointRef("GET", auth.ListActiveSessionsEndpoint.url),
    EndpointRef("DELETE", auth.TerminateCurrentSessionEndpoint.url),
    EndpointRef("DELETE", auth.TerminateAuthSessionEndpoint.url),
]
```

### Step 7: Add Service Methods

Services orchestrate mappers and endpoints. They accept domain models, use mappers to convert, call endpoints, and return domain models.

**Example** (from `services/tokens.py`):

```python
from typing import final
from ksef2.core import protocols
from ksef2.domain.models.tokens import GenerateTokenResponse, TokenPermission
from ksef2.endpoints.tokens import GenerateTokenEndpoint
from ksef2.infra.mappers.requests.tokens import GenerateTokenMapper


@final
class TokenService:
   def __init__(self, transport: protocols.Middleware) -> None:
      self._generate_ep = GenerateTokenEndpoint(transport)

   def generate(
           self,
           *,
           access_token: str,
           permissions: list[TokenPermission],
           description: str,
   ) -> GenerateTokenResponse:
      # 1. Map domain → spec (request)
      body = GenerateTokenMapper.map_request(permissions, description)
      # 2. Call endpoint with spec model
      spec_resp = self._generate_ep.send(
         access_token=access_token,
         body=body.model_dump(),
      )
      # 3. Map spec → domain (response)
      return GenerateTokenMapper.map_response(spec_resp)
```

**Key pattern:** mapper.map_request() → endpoint.send() → mapper.map_response()

### Step 8: Register on Client

Add the service as a cached property on `src/ksef2/clients/base.py`:

```python
from ksef2.services import tokens

@cached_property
def tokens(self) -> tokens.TokenService:
    return tokens.TokenService(self._transport)
```

### Step 9: Write Tests

#### Unit Tests
Add to `tests/unit/test_[feature]_endpoints.py`:

```python
def test_list_sessions_returns_active_sessions(fake_transport):
    """Test listing active sessions."""
    ep = ListActiveSessionsEndpoint(fake_transport)
    
    response = ep.send(
        bearer_token="test_token",
        page_size=10,
    )
    
    assert isinstance(response, spec.AuthenticationListResponse)
```

#### Integration Tests
Add to `tests/integration/test_[feature].py`:

```python
@pytest.mark.integration
def test_list_active_sessions(xades_authenticated_context):
    """List active authentication sessions."""
    client, auth = xades_authenticated_context

    response = auth.sessions.list_page()

    assert response is not None
    assert hasattr(response, "items")
```

**Note:** Integration tests use fixtures from `tests/integration/conftest.py`:
- `xades_authenticated_context` - for XAdES authentication with self-signed certificate
- `authenticated_context` - same as above (both use self-signed XAdES certificates)

Both fixtures use `generate_test_certificate()` to create self-signed certificates on-the-fly.
No real credentials are needed - only test NIP/PESEL identifiers from `.env.test`.

### Step 10: Run Lint and Typecheck

```bash
# Lint
uv run ruff check src/ksef2/endpoints/auth.py src/ksef2/services/auth.py

# Typecheck
uv run basedpyright src/ksef2/endpoints/auth.py src/ksef2/services/auth.py
```

### Step 11: Update Documentation

Update the relevant guide in `docs/guides/`:

```markdown
### 4. Active Sessions Management

**List Active Sessions** - Get all active authentication sessions.

**SDK Endpoint:** `GET /auth/sessions`

**Terminate Current Session** - Invalidate the current session.

**SDK Endpoint:** `DELETE /auth/sessions/current`
```

## Common Patterns

### HTTP Methods
```python
# GET
self._transport.get(url, headers=headers_dict)

# POST with JSON body
self._transport.post(url, headers=headers_dict, json=body)

# POST with raw content (XML, etc.)
self._transport.request("POST", url, content=bytes, headers={"Content-Type": "application/xml"})

# DELETE
self._transport.delete(url, headers=headers_dict)
```

### Headers
```python
from ksef2.core import headers

# Bearer token (for authenticated endpoints)
headers.KSeFHeaders.bearer(access_token)

# Session token (for session-based endpoints)  
headers.KSeFHeaders.session(access_token)
```

### Query Parameters
```python
from urllib.parse import urlencode

query_params: list[tuple[str, str]] = []
if page_size is not None:
    query_params.append(("pageSize", str(page_size)))

query_string = urlencode(query_params) if query_params else ""
path = f"{self.url}?{query_string}" if query_string else self.url
```

## File Locations

| Component | Location |
|-----------|----------|
| Client | `src/ksef2/clients/base.py` |
| Services | `src/ksef2/services/` |
| Mappers | `src/ksef2/infra/mappers/` |
| Endpoints | `src/ksef2/endpoints/` |
| Endpoint registry | `src/ksef2/endpoints/__init__.py` |
| Domain models | `src/ksef2/domain/models/` |
| Domain models re-exports | `src/ksef2/domain/models/__init__.py` |
| Spec models (auto-generated) | `src/ksef2/infra/schema/api/spec/models.py` |
| Unit tests | `tests/unit/` |
| Integration tests | `tests/integration/` |
| Documentation | `docs/guides/` |
| OpenAPI spec | `openapi.json` |

## Running Tests

```bash
# Unit tests
uv run pytest tests/unit/ -v

# Integration tests (requires .env.test with test NIP/PESEL identifiers)
uv run pytest tests/integration/ -v -m integration

# Single test
uv run pytest tests/unit/test_auth_endpoints.py::test_name -v
```

## Endpoints Without Response Bodies

Some endpoints return `200 OK` with no response body (e.g., testdata endpoints like `block_context`, `unblock_context`, `revoke_attachments`). For these:

1. **No response model needed** - Don't create domain models for the response
2. **No response mapper needed** - Skip the `map_response()` method
3. **Endpoint returns `None`** or ignores the response:

```python
@final
class BlockContextEndpoint:
    url: str = "/testdata/context/block"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)
```

4. **Service method returns `None`**:

```python
def block_context(self, *, context_identifier: AuthContextIdentifier) -> None:
   self._block_context_ep.send(
      TestDataMapper.block_context(context=context_identifier)
   )
```
