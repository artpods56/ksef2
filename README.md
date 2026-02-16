<div align="center">
<a href="https://github.com/artpods56/KUL_Notarius" title="TrendRadar">
  <img src="https://raw.githubusercontent.com/artpods56/ksef2/master/docs/assets/logo.png" alt="KSeF Toolkit" width="50%">
</a>

**Python SDK and Tools for Poland's KSeF (Krajowy System e-Faktur) v2.0 API.**

![API Coverage](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/artpods56/ksef2/master/coverage.json&query=$.message&label=KSeF%20API%20coverage&color=$.color)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) \
[![beartype](https://raw.githubusercontent.com/beartype/beartype-assets/main/badge/bear-ified.svg)](https://github.com/beartype/beartype)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Installation

```bash
uv add ksef2
```

Requires Python 3.12+.

## Quick Start

```python
from datetime import datetime, timezone
from ksef2 import Client, Environment, FormSchema
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    InvoiceQueryFilters, InvoiceSubjectType, InvoiceQueryDateRange, DateType,
)

NIP = "5261040828"
client = Client(Environment.TEST)

# Authenticate (XAdES — TEST environment)
cert, key = generate_test_certificate(NIP)
tokens = client.auth.authenticate_xades(nip=NIP, cert=cert, private_key=key)

with client.sessions.open_online(
    access_token=tokens.access_token.token,
    form_code=FormSchema.FA3,
) as session:

    # Send an invoice
    result = session.send_invoice(open("invoice.xml", "rb").read())
    print(result.reference_number)

    # Check processing status
    status = session.get_invoice_status(result.reference_number)

    # Export invoices matching a query
    export = session.schedule_invoices_export(
        filters=InvoiceQueryFilters(
            subject_type=InvoiceSubjectType.SUBJECT1,
            date_range=InvoiceQueryDateRange(
                date_type=DateType.ISSUE,
                from_=datetime(2026, 1, 1, tzinfo=timezone.utc),
                to=datetime.now(tz=timezone.utc),
            ),
        ),
    )

    # Download the exported package
    export_result = session.get_export_status(export.reference_number)
    if package := export_result.package:
        for path in session.fetch_package(package=package, target_directory="downloads"):
            print(f"Downloaded: {path}")
```
> Full runnable version: [`send_query_export_download.py`](scripts/examples/invoices/send_query_export_download.py) — more examples in [`scripts/examples`](scripts/examples).

### Token Authentication

For production, or when you have a pre-generated KSeF token:

```python
from ksef2 import Client, Environment

# uses production environment by default
client = Client()

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

The SDK currently covers **33 of 77** KSeF API endpoints (43%). Calculated via `scripts/api_coverage.py`. See individual feature docs for endpoint details:

- [Authentication](docs/guides/authentication.md)
- [Invoices](docs/guides/invoices.md)
- [Sessions](docs/guides/sessions.md)
- [Tokens](docs/guides/tokens.md)
- [Test Data](docs/guides/testdata.md)
- [Limits](docs/guides/limits.md)

## License

[MIT](LICENSE.md)
