# Sessions

Manage KSeF sessions for invoice operations.

## Session Types

KSeF has two types of sessions:

1. **Authentication Sessions** (`/auth/sessions/*`) - Manage authenticated sessions and refresh tokens
2. **Invoice Sessions** (`/sessions/online`, `/sessions/batch`) - Send and process invoices

For authentication session management, see [Authentication](guides/authentication.md).

## Invoice Sessions

### Open Session

Start a new online session for invoice operations.

**SDK Endpoint:** `POST /sessions/online`

---

### Resume Session

Resume an existing session from saved state.

**SDK Endpoint:** Uses stored session state

---

### Terminate Session

End an active session.

**SDK Endpoint:** `POST /sessions/online/{referenceNumber}/close`

---

## Session Lifecycle

```
1. Open Session
   POST /sessions/online → {referenceNumber, ...}

2. Perform Operations
   - send_invoice()
   - download_invoice()

3. Terminate Session
   POST /sessions/online/{referenceNumber}/close
```

---

## Related

- [Invoices](guides/invoices.md) - Invoice operations within sessions
- [Authentication](guides/authentication.md) - Getting access tokens
