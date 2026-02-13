# Authentication

The SDK supports multiple authentication methods for accessing the KSeF API.

## Authentication Methods

### 1. XAdES Authentication

Uses a digital certificate to sign an authentication request. Works with self-signed certificates on the TEST environment.

**Endpoint:** `POST /auth/xades-signature`

**KSeF API:** [`/auth/xades-signature`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Uzyskiwanie-dostepu/paths/~1auth~1xades-signature/post)

**Requirements:**
- Self-signed certificate (TEST only) or qualified certificate (PRODUCTION)
- Certificate must include appropriate identifiers (NIP/PESEL)

---

### 2. Token Authentication

Uses a pre-generated KSeF token (not the access token) for authentication.

**Endpoint:** `POST /auth/ksef-token`

**KSeF API:** [`/auth/ksef-token`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Uzyskiwanie-dostepu/paths/~1auth~1ksef-token/post)

**Requirements:**
- Valid KSeF token obtained from:
  - KSeF portal directly
  - Token generation API (requires `CredentialsManage` permission)

---

### 3. Token Refresh

Refresh an expired access token without re-authenticating.

**Endpoint:** `POST /auth/token/refresh`

**KSeF API:** [`/auth/token/refresh`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Uzyskiwanie-dostepu/paths/~1auth~1token~1refresh/post)

**Requirements:**
- Valid refresh token from previous authentication

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

**Endpoints:**
- `POST /auth/challenge` - Get authentication challenge
- `POST /auth/xades-signature` - Submit XAdES signed request
- `POST /auth/ksef-token` - Submit token-based request
- `GET /auth/{referenceNumber}` - Check auth status
- `POST /auth/token/redeem` - Redeem auth token for access/refresh
- `POST /auth/token/refresh` - Refresh access token

---

## Environment Support

| Environment | Base URL | Self-Signed Cert | Notes |
|-------------|----------|------------------|-------|
| PRODUCTION | `api.ksef.mf.gov.pl/api/v2` | ❌ | Requires qualified cert |
| TEST | `api-test.ksef.mf.gov.pl/api/v2` | ✅ | Full test support |
| DEMO | `api-demo.ksef.mf.gov.pl/api/v2` | ✅ | Demo environment |

---

## Related

- [Test Data](guides/testdata.md) - Setting up test subjects
- [Tokens](guides/tokens.md) - Token generation and management
- KSeF API: [Authentication](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Uzyskiwanie-dostepu)
