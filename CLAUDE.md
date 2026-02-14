# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Python SDK for Poland's KSeF (Krajowy System e-Faktur) v2.0 API — the national e-invoicing system. Package name: `ksef2`. Requires Python 3.12+. Uses `uv` as package manager.

## Commands

```bash
# Install all deps (including dev)
uv sync --all-groups

# Run unit tests
uv run pytest tests/unit/ -v

# Run a single test
uv run pytest tests/unit/test_auth_service.py -v
uv run pytest tests/unit/test_auth_service.py::test_name -v

# Type checking
uv run basedpyright

# Linting
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Regenerate OpenAPI models (requires codegen group)
uv run --group codegen datamodel-codegen --input openapi.json --output src/ksef2/infra/schema/spec.py

# API coverage report (updates coverage.json badge)
uv run python scripts/api_coverage.py
```

## Architecture

The SDK follows a layered architecture with clear separation between API transport, domain models, and public-facing services.

### Layer Overview (bottom-up)

1. **`infra/schema/model.py`** — Auto-generated Pydantic models from `openapi.json`. Do not edit manually; regenerate with `datamodel-codegen`.

2. **`endpoints/`** — Thin typed wrappers around HTTP calls. Each endpoint class owns a URL path and calls `HttpTransport`, returning a parsed `infra/schema` model. No business logic here.

3. **`infra/mappers/`** — Translate between `infra/schema` (OpenAPI camelCase) models and `domain/models` (snake_case Pydantic). Each mapper is a class with static `map_response`/`map_request` methods.

4. **`domain/models/`** — Clean Pydantic models that form the SDK's public API types. All inherit from `KSeFBaseModel`.

5. **`services/`** — Orchestrate multi-step API flows (e.g., challenge → auth → poll → redeem). Services compose endpoints + mappers and are the main business logic layer.

6. **`clients/base.py` → `Client`** — Top-level facade exposed as `ksef2.Client`. Lazily creates services via `@cached_property`. This is the public entry point.

### Core Utilities (`core/`)

- **`http.py`** — `HttpTransport` wraps `httpx.Client` (HTTP/2 enabled). All API calls go through this.
- **`crypto.py`** — RSA encryption of KSeF tokens.
- **`xades.py`** — XAdES XML signature generation for certificate-based auth.
- **`stores.py`** — `CertificateStore` caches KSeF encryption certificates.
- **`codecs.py`** — JSON response parsing into Pydantic schema models.
- **`headers.py`** — KSeF-specific HTTP header builders (bearer tokens, etc.).
- **`exceptions.py`** — SDK exception hierarchy (`KSeFRateLimitError`, `KSeFAuthError`, etc.).

### Deprecated Code

`clients/_deprecated/` and `domain/models/_deprecated/` contain the old client architecture (`KsefClient` in `client.py`). The new architecture uses `clients/base.py` → `Client` with the services layer. The deprecated `KsefClient` lazily instantiates old-style sub-clients directly, bypassing the services layer.

### Data Flow for a Typical API Call

`Client` → `Service` → `Endpoint` (HTTP call) → `infra/schema` model → `Mapper` → `domain/models` model → returned to caller

### Environments

Three KSeF environments defined in `config.py`: `PRODUCTION`, `TEST`, `DEMO`. The `TEST` environment additionally exposes testdata endpoints at a different base URL.

### Adding a New Endpoint

1. Add endpoint class in `endpoints/` with URL and typed `send()` method
2. Register it in `endpoints/__init__.py` (`__all_endpoints__`) for API coverage tracking
3. Add domain models in `domain/models/`
4. Add mapper in `infra/mappers/`
5. Add or extend a service in `services/`
6. Wire into `Client` in `clients/base.py`

### Testing

Tests use `respx` to mock HTTP responses (no real API calls in unit tests). Integration tests (marked `@pytest.mark.integration`) hit the real KSeF TEST environment.
