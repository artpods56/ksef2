# Tokens

Manage KSeF tokens for authentication and authorization.

## Token Types

### KSeF Token

A separate credential used for token-based authentication (`authenticate_token`).

**Note:** KSeF tokens are different from access/refresh tokens. They must be generated after authentication with appropriate permissions.

---

## Operations

### Generate Token

Create a new KSeF token for future authentication.

**Endpoint:** `POST /token/manage`

**KSeF API:** [`/token/manage`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Zarzadzanie-tokenami/paths/~1token~1manage/post)

**Requirements:**
- Valid access token with `CREDENTIALS_MANAGE` permission

---

### Token Status

Check the status of a token generation request.

**Endpoint:** `GET /token/manage/{referenceNumber}`

**KSeF API:** [`/token/manage/{referenceNumber}`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Zarzadzanie-tokenami/paths/~1token~1manage~1%7BreferenceNumber%7D/get)

---

### Revoke Token

Revoke an existing KSeF token.

**Endpoint:** `DELETE /token/manage/{referenceNumber}`

**KSeF API:** [`/token/manage/{referenceNumber}`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Zarzadzanie-tokenami/paths/~1token~1manage~1%7BreferenceNumber%7D/delete)

---

## Token Permissions

| Permission | Description |
|------------|-------------|
| `INVOICE_READ` | Read/download invoices |
| `INVOICE_WRITE` | Send invoices |
| `INTROSPECTION` | Search invoices |
| `CREDENTIALS_READ` | Read token info |
| `CREDENTIALS_MANAGE` | Generate/revoke tokens |
| `ENFORCEMENT_OPERATIONS` | Enforcement operations |
| `SUBUNIT_MANAGE` | Manage subunits |

---

## Related

- [Authentication](guides/authentication.md) - Using tokens for authentication
- KSeF API: [Tokeny](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Zarzadzanie-tokenami)
