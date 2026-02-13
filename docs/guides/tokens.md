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

**SDK Endpoint:** `POST /tokens`

**Requirements:**
- Valid access token with `CREDENTIALS_MANAGE` permission

---

### Token Status

Check the status of a token generation request.

**SDK Endpoint:** `GET /tokens/{referenceNumber}`

---

### Revoke Token

Revoke an existing KSeF token.

**SDK Endpoint:** `DELETE /tokens/{referenceNumber}`

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
