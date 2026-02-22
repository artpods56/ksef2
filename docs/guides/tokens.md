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

```python
from ksef2.domain.models.tokens import TokenPermission

result = auth.tokens.generate(
    permissions=[
        TokenPermission.INVOICE_READ,
        TokenPermission.INVOICE_WRITE,
    ],
    description="Example API token",
)
print(f"Token:     {result.token[:40]}...")
print(f"Reference: {result.reference_number}")
```

---

### List Tokens

List all generated tokens with optional filtering.

**SDK Endpoint:** `GET /tokens`

```python
from ksef2.domain.models.tokens import TokenStatus

# List all tokens
response = auth.tokens.list_sessions()
for token in response.tokens:
    print(f"{token.reference_number}: {token.status.value} - {token.description}")

# Filter by status
response = auth.tokens.list_sessions(
    status=[TokenStatus.ACTIVE],
)

# Filter by description (min 3 chars, case-insensitive)
response = auth.tokens.list_sessions(
    description="API token",
)

# Filter by author
from ksef2.domain.models.tokens import TokenAuthorIdentifier, TokenAuthorIdentifierType

response = auth.tokens.list_sessions(
    author_filter=TokenAuthorIdentifier(
        type=TokenAuthorIdentifierType.NIP,
        value="1234567890",
    ),
)

# Pagination
response = auth.tokens.list_sessions(
    page_size=20,
)
if response.continuation_token:
    next_page = auth.tokens.list_sessions(
        continuation_token=response.continuation_token,
    )
```

---

### Token Status

Check the status of a token generation request.

**SDK Endpoint:** `GET /tokens/{referenceNumber}`

```python
status = auth.tokens.status(
    reference_number=result.reference_number,
)
print(f"Status: {status.status.value}")
```

---

### Revoke Token

Revoke an existing KSeF token.

**SDK Endpoint:** `DELETE /tokens/{referenceNumber}`

```python
auth.tokens.revoke(
    reference_number=result.reference_number,
)
```

---

## Full Example

Full token lifecycle — generate, list, check status, and revoke:

```python
from ksef2.domain.models.tokens import TokenPermission, TokenStatus

# Generate a new KSeF token (requires CREDENTIALS_MANAGE permission)
result = auth.tokens.generate(
    permissions=[
        TokenPermission.INVOICE_READ,
        TokenPermission.INVOICE_WRITE,
    ],
    description="Example API token",
)
print(f"Token:     {result.token[:40]}...")
print(f"Reference: {result.reference_number}")

# List all active tokens
response = auth.tokens.list_sessions(
    status=[TokenStatus.ACTIVE],
)
print(f"Active tokens: {len(response.tokens)}")

# Check token status
status = auth.tokens.status(
    reference_number=result.reference_number,
)
print(f"Status: {status.status.value}")

# Revoke the token
auth.tokens.revoke(
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

## Token Statuses

| Status | Description |
|--------|-------------|
| `PENDING` | Token created but still activating |
| `ACTIVE` | Token is active and can be used |
| `REVOKING` | Token is being revoked |
| `REVOKED` | Token has been revoked |
| `FAILED` | Token activation failed |

---

## Author Identifier Types

Used for filtering tokens by author:

| Type | Description |
|------|-------------|
| `NIP` | Polish tax identification number |
| `PESEL` | Polish personal identification number |
| `FINGERPRINT` | Certificate fingerprint |

---

## Related

- [Authentication](authentication.md) - Using tokens for authentication
