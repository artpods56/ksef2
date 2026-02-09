# ksef-sdk

Python SDK for Poland's KSeF (Krajowy System e-Faktur) API.

## Installation

```bash
uv add ksef-sdk
```

Requires Python 3.12+.

## Quick Start

```python
from ksef_sdk import Client
from ksef_sdk.config import Environment

client = Client(Environment.TEST)

# Authenticate with a KSeF token
tokens = client.auth.authenticate_token(
    ksef_token="your-ksef-token",
    nip="1234567890",
)

# Open an online session and send an invoice
from ksef_sdk.domain.models.session import FormSchema

with client.sessions.open_online(
    access_token=tokens.access_token.token,
    form_code=FormSchema.FA3,
) as session:
    with open("invoice.xml", "rb") as f:
        result = session.send_invoice(f.read())
    print(result.reference_number)
```

### XAdES Authentication (TEST environment)

On the TEST environment you can authenticate with a self-signed certificate — no pre-existing KSeF token needed:

```python
from ksef_sdk import Client
from ksef_sdk.config import Environment
from ksef_sdk.core._xades import generate_test_certificate

client = Client(Environment.TEST)

cert, private_key = generate_test_certificate("1234567890")
tokens = client.auth.authenticate_xades(
    nip="1234567890",
    cert=cert,
    private_key=private_key,
)
print(tokens.access_token.token)
```

## API Reference

### `Client(environment)`

Top-level entry point. All functionality is accessed through service properties.

```python
from ksef_sdk import Client
from ksef_sdk.config import Environment

client = Client(Environment.TEST)
```

#### `client.auth` — `AuthService`

Full authentication lifecycle: challenge, encrypt/sign, submit, poll, redeem.

| Method | Description |
|---|---|
| `authenticate_token(*, ksef_token, nip, context_type?, poll_interval?, max_poll_attempts?)` | Token-based auth flow. Returns `AuthTokens` with `access_token` and `refresh_token`. |
| `authenticate_xades(*, nip, cert, private_key, verify_chain?, poll_interval?, max_poll_attempts?)` | XAdES certificate auth flow. Returns `AuthTokens`. |
| `refresh(*, refresh_token)` | Refresh an expired access token. Returns `RefreshedToken`. |

#### `client.sessions` — `OpenSessionService`

Online session management with AES encryption.

| Method | Description |
|---|---|
| `open_online(*, access_token, form_code)` | Opens an online session. Returns `OnlineSessionClient` (context manager). |
| `resume(state)` | Rehydrates a session from a `SessionState` object. |

#### `OnlineSessionClient`

Returned by `open_online()`. Supports `with` blocks for automatic termination.

| Method | Description |
|---|---|
| `send_invoice(invoice_xml)` | Encrypts and sends an invoice. Returns `SendInvoiceResponse`. |
| `download_invoice(ksef_number)` | Downloads an invoice by KSeF number. Returns raw XML bytes. |
| `terminate()` | Closes the session. Called automatically when using `with`. |

#### `client.tokens` — `TokenService`

KSeF token management (requires an active session token).

| Method | Description |
|---|---|
| `generate(*, access_token, permissions, description, poll_interval?, max_poll_attempts?)` | Generate a new KSeF token. Returns `GenerateTokenResponse`. |
| `status(*, access_token, reference_number)` | Check token status. Returns `TokenStatusResponse`. |
| `revoke(*, access_token, reference_number)` | Revoke a token. |

#### `client.encryption` — `EncryptionClient`

| Method | Description |
|---|---|
| `get_certificates()` | Fetch MF public-key certificates. Returns `list[PublicKeyCertificate]`. |

#### `client.testdata` — `TestDataService`

Test data management (TEST environment only).

| Method | Description |
|---|---|
| `create_subject(*, nip, subject_type, description, subunits?, created_date?)` | Register a test subject (company). |
| `delete_subject(*, nip)` | Remove a test subject. |
| `create_person(*, nip, pesel, description, is_bailiff?, is_deceased?, created_date?)` | Register a test person. |
| `delete_person(*, nip)` | Remove a test person. |
| `grant_permissions(*, context, authorized, permissions)` | Grant permissions to an identifier. |
| `revoke_permissions(*, context, authorized)` | Revoke permissions. |
| `enable_attachments(*, nip)` | Enable attachments for a subject. |

## Environments

| Environment | URL |
|---|---|
| `Environment.PRODUCTION` | `https://api.ksef.mf.gov.pl/api/v2` |
| `Environment.TEST` | `https://api-test.ksef.mf.gov.pl/api/v2` |
| `Environment.DEMO` | `https://api-demo.ksef.mf.gov.pl/api/v2` |

## Error Handling

All errors inherit from `KSeFException`:

| Exception | When |
|---|---|
| `KSeFApiError` | 4xx/5xx API responses |
| `KSeFAuthError` | Authentication failures (401/403, polling errors) |
| `KSeFRateLimitError` | 429 Too Many Requests (includes `retry_after`) |
| `KSeFEncryptionError` | Encryption/decryption failures |
| `KSeFSessionError` | Session-state violations |
| `NoCertificateAvailableError` | No valid certificate found for the requested usage |

## Development

```bash
uv sync --all-groups
uv run pytest tests/unit/ -v
```

### Regenerating models

```bash
uv run --group codegen datamodel-codegen --input openapi.json --output src/ksef_sdk/infra/schema/model.py
```
