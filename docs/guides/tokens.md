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

## Example

Full token lifecycle — generate, check status, and revoke:

```python
from ksef2.domain.models.tokens import TokenPermission

# Generate a new KSeF token (requires CREDENTIALS_MANAGE permission)
result = client.tokens.generate(
    access_token=access_token,
    permissions=[
        TokenPermission.INVOICE_READ,
        TokenPermission.INVOICE_WRITE,
    ],
    description="Example API token",
)
print(f"Token:     {result.token[:40]}...")
print(f"Reference: {result.reference_number}")

# Check token status
status = client.tokens.status(
    access_token=access_token,
    reference_number=result.reference_number,
)
print(f"Status: {status.status.value}")

# Revoke the token
client.tokens.revoke(
    access_token=access_token,
    reference_number=result.reference_number,
)
```

> Full example: [`scripts/examples/auth/token_management.py`](../../scripts/examples/auth/token_management.py)

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

- [Authentication](authentication.md) - Using tokens for authentication
