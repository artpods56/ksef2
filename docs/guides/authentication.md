# Authentication

The SDK supports multiple authentication methods for accessing the KSeF API.

## Authentication Methods

### 1. XAdES Authentication

Uses a digital certificate to sign an authentication request.

**SDK Endpoint:** `POST /auth/xades-signature`

#### TEST environment — self-signed certificate

The SDK can generate a self-signed certificate on the fly. This is the fastest
way to get started and works exclusively on the TEST environment.

```python
from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate

NIP = generate_nip()
client = Client(environment=Environment.TEST)

# Generate a self-signed certificate (TEST environment only)
cert, private_key = generate_test_certificate(NIP)

auth = client.authentication.with_xades(
    nip=NIP,
    cert=cert,
    private_key=private_key,
)

print(f"Access token:  {auth.access_token[:40]}…")
print(f"  Valid until: {auth.auth_tokens.access_token.valid_until}")
print(f"Refresh token: {auth.refresh_token[:40]}…")
print(f"  Valid until: {auth.auth_tokens.refresh_token.valid_until}")
```

> Full example: [`scripts/examples/auth/auth_xades.py`](../../scripts/examples/auth/auth_xades.py)

#### DEMO / PRODUCTION — MCU-issued certificate

The DEMO and PRODUCTION environments reject self-signed certificates
(`exceptionCode 21115 — Nieprawidłowy certyfikat`).  You must use a certificate
issued by MCU (Ministerstwo Finansów):

1. Log into MCU at <https://ap-demo.ksef.mf.gov.pl/web/> (DEMO) or the
   production portal with your Profil Zaufany or electronic seal.
2. Generate a **signing certificate** (separate from the login certificate).
3. Download the two files provided by KSEF:
   - **`<NIP>.pem`** — the certificate (`.pem` extension)
   - **`<NIP>.key`** — the private key (`.key` extension)

```python
from ksef2 import Client, Environment
from ksef2.core.xades import load_certificate_from_pem, load_private_key_from_pem

cert = load_certificate_from_pem("1234567890.pem")  # .pem — certificate from KSEF
key = load_private_key_from_pem("1234567890.key")  # .key — private key from KSEF

auth = Client(Environment.DEMO).authentication.with_xades(
    nip="1234567890",
    cert=cert,
    private_key=key,
    verify_chain=False,
)
```

If your certificate was packaged as a `.p12` / `.pfx` archive:

```python
from ksef2.core.xades import load_certificate_and_key_from_p12

cert, key = load_certificate_and_key_from_p12("cert.p12", password=b"secret")
```

> Full example: [`scripts/examples/auth/auth_xades_demo.py`](../../scripts/examples/auth/auth_xades_demo.py)

---

### 2. Token Authentication

Uses a pre-generated KSeF token (not the access token) for authentication.

**SDK Endpoint:** `POST /auth/ksef-token`

**Requirements:**
- Valid KSeF token obtained from:
  - KSeF portal directly
  - Token generation API (requires `CredentialsManage` permission)

```python
from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip

NIP = generate_nip()
KSEF_TOKEN = "<your-token-here>"

client = Client(environment=Environment.TEST)

auth = client.authentication.with_token(
    ksef_token=KSEF_TOKEN,
    nip=NIP,
)

print(f"Access token:  {auth.access_token[:40]}…")
print(f"Refresh token: {auth.refresh_token[:40]}…")
```

> Full example: [`scripts/examples/auth/auth_token.py`](../../scripts/examples/auth/auth_token.py)

---

### 3. Token Refresh

Refresh an expired access token without re-authenticating.

**SDK Endpoint:** `POST /auth/token/refresh`

**Requirements:**
- Valid refresh token from previous authentication

```python
# After initial authentication...
refreshed = client.authentication.refresh(refresh_token=auth.refresh_token)
print(f"New access token valid until: {refreshed.auth_tokens.access_token.valid_until}")

# The AuthenticatedClient can now be used for API calls
sessions = refreshed.sessions.list_page()
```

> Full example: [`scripts/examples/auth/auth_refresh.py`](../../scripts/examples/auth/auth_refresh.py)

---

### 4. Active Sessions Management

Manage active authentication sessions. Each successful authentication creates a session tied to a refresh token.

**List Active Sessions** - Get all active authentication sessions for your account.

**SDK Endpoint:** `GET /auth/sessions`

Returns a paginated list with:
- `referenceNumber` - Session identifier
- `startDate` - When the session was created
- `authenticationMethod` - Method used (XAdES, Token, etc.)
- `status` - Session status (200 = success)
- `isCurrent` - Whether this is the current session
- `refreshTokenValidUntil` - When the refresh token expires

**Terminate Current Session** - Invalidate the session used for the current request.

**SDK Endpoint:** `DELETE /auth/sessions/current`

**Terminate Specific Session** - Invalidate a specific session by reference number.

**SDK Endpoint:** `DELETE /auth/sessions/{referenceNumber}`

Note: Terminating a session invalidates its refresh token. Active access tokens remain valid until expiration.

```python
# List active sessions
sessions = auth.sessions.list_page()

# Paginated listing
# sessions = auth.sessions.list(
#     page_size=10,
#     continuation_token=None,  # from previous page
# )

# Terminate the current session
auth.sessions.terminate_current()

# Terminate a specific session by reference number
# auth.sessions.terminate(reference_number="some-reference-number")
```

> Full example: [`scripts/examples/session/session_management.py`](../../scripts/examples/session/session_management.py)

---

## Authentication Flow

```
1. Get Challenge
   POST /auth/challenge → {challenge, timestamp}

2. Authenticate (choose method)
   
   XAdES:
   a. Build AuthTokenRequest XML
   b. Sign with XAdES
   c. POST /auth/xades-signature → {authenticationToken, referenceNumber}
   
   Token:
   a. Encrypt (ksef_token|timestamp) with RSA-OAEP
   b. POST /auth/ksef-token → {authenticationToken, referenceNumber}

3. Poll Status
   GET /auth/{referenceNumber} (with bearer token)
   → Wait for status 200

4. Redeem Tokens
   POST /auth/token/redeem (with authenticationToken)
   → {accessToken, refreshToken}
```

**SDK Endpoints:**
- `POST /auth/challenge` - Get authentication challenge
- `POST /auth/xades-signature` - Submit XAdES signed request
- `POST /auth/ksef-token` - Submit token-based request
- `GET /auth/{referenceNumber}` - Check auth status
- `POST /auth/token/redeem` - Redeem auth token for access/refresh
- `POST /auth/token/refresh` - Refresh access token
- `GET /auth/sessions` - List active authentication sessions
- `DELETE /auth/sessions/current` - Terminate current session
- `DELETE /auth/sessions/{referenceNumber}` - Terminate specific session

---

## Environment Support

| Environment | Base URL | Self-Signed Cert | Notes |
|-------------|----------|------------------|-------|
| PRODUCTION | `api.ksef.mf.gov.pl/v2` | ❌ | MCU-issued cert required |
| TEST | `api-test.ksef.mf.gov.pl/v2` | ✅ | `generate_test_certificate()` works here |
| DEMO | `api-demo.ksef.mf.gov.pl/v2` | ❌ | MCU-issued cert required |

---

## Related

- [Test Data](testdata.md) - Setting up test subjects
- [Tokens](tokens.md) - Token generation and management
