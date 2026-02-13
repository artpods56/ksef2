# Sessions

Manage KSeF online sessions for invoice operations.

## Operations

### Open Session

Start a new online session for invoice operations.

**Endpoint:** `POST /online/session`

**KSeF API:** [`/online/session`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Sesje/paths/~1online~1session/post)

---

### Resume Session

Resume an existing session.

**Endpoint:** `POST /online/session/resume`

---

### Terminate Session

End an active session.

**Endpoint:** `DELETE /online/session`

**KSeF API:** [`/online/session`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Sesje/paths/~1online~1session/delete)

---

## Session Lifecycle

```
1. Open Session
   POST /online/session → {sessionId, ...}

2. Perform Operations
   - send_invoice()
   - download_invoice()
   - search_invoices()

3. Terminate Session
   DELETE /online/session
```

---

## Related

- [Invoices](guides/invoices.md) - Invoice operations within sessions
- [Authentication](guides/authentication.md) - Getting access tokens
- KSeF API: [Sesje](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Sesje)
