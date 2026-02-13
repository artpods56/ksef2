<div align="center">

**Python SDK and Tools for Poland's KSeF (Krajowy System e-Faktur) v2.0 API.**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) 
[![beartype](https://raw.githubusercontent.com/beartype/beartype-assets/main/badge/bear-ified.svg)](https://github.com/beartype/beartype)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Installation

```bash
uv add ksef2
```

Requires Python 3.12+.

## Quick Start

```python
from ksef2 import Client, Environment, FormSchema
from ksef2.core.xades import generate_test_certificate

VALID_NIP = "5261040828"

client = Client(Environment.TEST)

# XAdES Authentication (TEST environment) - generates self-signed certificate automatically
cert, private_key = generate_test_certificate(VALID_NIP)
tokens = client.auth.authenticate_xades(
    nip=VALID_NIP,
    cert=cert,
    private_key=private_key,
)

# Send invoice
with client.sessions.open_online(
    access_token=tokens.access_token.token,
    form_code=FormSchema.FA3,
) as session:
    with open("invoice.xml", "rb") as f:
        result = session.send_invoice(f.read())
    print(result.reference_number)

# Sessions also support manual management:
session = client.sessions.open_online(
    access_token=tokens.access_token.token,
    form_code=FormSchema.FA3,
)
try:
    with open("invoice.xml", "rb") as f:
        result = session.send_invoice(f.read())
    print(result.reference_number)
finally:
    session.terminate()
```

### Token Authentication

For production, or when you have a pre-generated KSeF token:

```python
from ksef2 import Client, Environment

client = Client(Environment.TEST)

tokens = client.auth.authenticate_token(
    ksef_token="your-ksef-token",
    nip=VALID_NIP,
)
print(tokens.access_token.token)
```

## Development

```bash
just sync          # Install all dependencies (including dev)
just test          # Run unit tests
just regenerate-models  # Regenerate OpenAPI models
```

### Other commands

```bash
just integration   # Run integration tests (requires KSEF credentials in .env)
just coverage       # Calculate API coverage (updates coverage.json)
just fetch-spec     # Fetch latest OpenAPI spec from KSeF
```

## API Coverage

The SDK currently covers **14 of 77** KSeF API endpoints (18%). Calculated via `scripts/api_coverage.py`. See individual feature docs for endpoint details:

- [Authentication](docs/guides/authentication.md)
- [Invoices](docs/guides/invoices.md)
- [Sessions](docs/guides/sessions.md)
- [Tokens](docs/guides/tokens.md)
- [Test Data](docs/guides/testdata.md)

## License

[MIT](LICENSE.md)
