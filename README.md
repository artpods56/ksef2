# ksef-sdk

Python SDK for Poland's KSeF (Krajowy System e-Faktur) API.

## Installation

```bash
uv add ksef-sdk
```

Requires Python 3.12+.

## Quick Start

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

## Features

- Full token-based authentication flow (challenge, encrypt, poll, redeem)
- Online session management with automatic open/close via context managers
- Invoice encryption (AES-256-CBC) and submission
- Typed request/response models (170 auto-generated Pydantic v2 models)
- Structured error handling with `KsefApiError`, `KsefAuthError`, `KsefRateLimitError`

## Environments

| Environment | URL |
|---|---|
| `Environment.PRODUCTION` | `https://ksef.mf.gov.pl/api` |
| `Environment.TEST` | `https://ksef-test.mf.gov.pl/api` |
| `Environment.DEMO` | `https://ksef-demo.mf.gov.pl/api` |

## Development

```bash
uv sync --all-groups
uv run pytest
uv run ruff check src/
```

### Regenerating models

```bash
uv run --group codegen datamodel-codegen --input openapi.json --output src/ksef_sdk/_generated/model.py
```
