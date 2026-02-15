# Implementing New KSeF API Endpoints

This guide documents the process for implementing new endpoints in the KSeF SDK.

## Overview

The SDK follows a layered architecture:
```
Client → Service → Endpoint → HTTP Transport → infra/schema (OpenAPI models)
```

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

The SDK auto-generates Pydantic models from OpenAPI in `src/ksef2/infra/schema/api/spec.py`.

**Search for existing models:**
```bash
grep -n "ModelName" src/ksef2/infra/schema/api/models.py
```

If the model doesn't exist, regenerate the schema:
```bash
just regenerate-models
```

### Step 3: Implement the Endpoint Class

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

### Step 4: Register the Endpoint

Add the endpoint to `src/ksef2/endpoints/__init__.py`:

```python
__auth_endpoints__ = [
    # ... existing endpoints ...
    EndpointRef("GET", auth.ListActiveSessionsEndpoint.url),
    EndpointRef("DELETE", auth.TerminateCurrentSessionEndpoint.url),
    EndpointRef("DELETE", auth.TerminateAuthSessionEndpoint.url),
]
```

### Step 5: Add Service Methods (Optional)

If you want the endpoint accessible via the client, add methods to the appropriate Service class:

**Example** (from `services/auth.py`):
```python
from ksef2.endpoints.auth import (
    ListActiveSessionsEndpoint,
    TerminateCurrentSessionEndpoint,
    TerminateAuthSessionEndpoint,
)

class AuthService:
    def __init__(self, ...):
        # ... existing endpoints ...
        self._list_sessions_ep = ListActiveSessionsEndpoint(transport)
        self._terminate_current_ep = TerminateCurrentSessionEndpoint(transport)
        self._terminate_session_ep = TerminateAuthSessionEndpoint(transport)

    def list_active_sessions(
        self,
        *,
        access_token: str,
        page_size: int | None = None,
        continuation_token: str | None = None,
    ):
        """List active authentication sessions."""
        return self._list_sessions_ep.send(
            bearer_token=access_token,
            page_size=page_size,
            continuation_token=continuation_token,
        )

    def terminate_current_session(self, *, access_token: str) -> None:
        """Terminate the current authentication session."""
        self._terminate_current_ep.send(bearer_token=access_token)

    def terminate_session(
        self,
        *,
        access_token: str,
        reference_number: str,
    ) -> None:
        """Terminate a specific authentication session by reference number."""
        self._terminate_session_ep.send(
            bearer_token=access_token,
            reference_number=reference_number,
        )
```

### Step 6: Write Tests

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
    client, tokens = xades_authenticated_context

    response = client.auth.list_active_sessions(
        access_token=tokens.access_token.token,
    )

    assert response is not None
    assert hasattr(response, "items")
```

**Note:** Integration tests use fixtures from `tests/integration/conftest.py`:
- `xades_authenticated_context` - for XAdES authentication
- `authenticated_context` - for token authentication (requires `KSEF_TEST_KSEF_TOKEN`)

### Step 7: Run Lint and Typecheck

```bash
# Lint
uv run ruff check src/ksef2/endpoints/auth.py src/ksef2/services/auth.py

# Typecheck
uv run basedpyright src/ksef2/endpoints/auth.py src/ksef2/services/auth.py
```

### Step 8: Update Documentation

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
| Endpoints | `src/ksef2/endpoints/` |
| Services | `src/ksef2/services/` |
| Schema (models) | `src/ksef2/infra/schema/api/spec.py` |
| Unit tests | `tests/unit/` |
| Integration tests | `tests/integration/` |
| Documentation | `docs/guides/` |
| OpenAPI spec | `openapi.json` |

## Running Tests

```bash
# Unit tests
uv run pytest tests/unit/ -v

# Integration tests (requires .env.test with credentials)
source .env.test && uv run pytest tests/integration/ -v -m integration

# Single test
uv run pytest tests/unit/test_auth_endpoints.py::test_name -v
```
