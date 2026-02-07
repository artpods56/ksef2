# ksef-sdk

Python SDK for Poland's KSeF (Krajowy System e-Faktur) API.

## Installation

```bash
uv add ksef-sdk
```

Requires Python 3.12+.

## Quick Start

### With a KSeF token

```python
from ksef_sdk import KsefClient, Environment

with KsefClient(nip="1234567890", token="your-ksef-token", env=Environment.TEST) as client:
    client.authenticate()

    with client.online_session() as session:
        with open("invoice.xml", "rb") as f:
            result = session.send_invoice(f.read())
        print(result.referenceNumber)

    status = client.get_session_status(session.reference_number)
    print(status.status.code, status.status.description)
```

### Without a token (XAdES auth)

On the TEST environment you can authenticate with a self-signed certificate — no pre-existing token needed:

```python
from ksef_sdk import KsefClient, Environment

with KsefClient(nip="1234567890", env=Environment.TEST) as client:
    client.authenticate_xades()  # auto-generates a self-signed cert

    # Generate a reusable KSeF token
    resp = client.generate_ksef_token(
        permissions=["InvoiceRead", "InvoiceWrite"],
        description="My token",
    )
    print(resp.token)
```

## Features

- **Token-based authentication** — challenge, encrypt, poll, redeem
- **XAdES certificate authentication** — sign with a qualified or self-signed certificate (no token required)
- **KSeF token management** — generate, query status, and revoke tokens
- Online session management with automatic open/close via context managers
- Invoice encryption (AES-256-CBC) and submission
- Typed request/response models (170+ auto-generated Pydantic v2 models)
- Structured error handling with `KsefApiError`, `KsefAuthError`, `KsefRateLimitError`

## Environments

| Environment | URL |
|---|---|
| `Environment.PRODUCTION` | `https://api.ksef.mf.gov.pl/api/v2` |
| `Environment.TEST` | `https://api-test.ksef.mf.gov.pl/api/v2` |
| `Environment.DEMO` | `https://api-demo.ksef.mf.gov.pl/api/v2` |

## Development

```bash
uv sync --all-groups
uv run pytest                            # unit tests
uv run pytest tests/integration/ -v      # integration tests (hits TEST env)
uv run ruff check src/
```

### Regenerating models

```bash
uv run --group codegen datamodel-codegen --input openapi.json --output src/ksef_sdk/_generated/model.py
```
