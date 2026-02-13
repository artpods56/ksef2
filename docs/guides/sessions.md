# Sessions

Manage KSeF online sessions for invoice operations.

## Operations

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
