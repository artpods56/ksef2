# Invoices

Send, download, and manage structured invoices in KSeF.

## Operations

### Send Invoice

Upload a structured invoice to KSeF.

**SDK Endpoint:** `POST /sessions/online/{referenceNumber}/invoices`

---

### Download Invoice

Download an invoice by its KSeF reference number.

**SDK Endpoint:** `GET /invoices/ksef/{ksefNumber}`

---

## Sessions

All invoice operations require an active session:

```python
with client.sessions.open_online(access_token=token) as session:
    session.send_invoice(...)
    invoice = session.download_invoice(...)
```

**Session SDK endpoints:**
- `POST /sessions/online` - Open session
- `POST /sessions/online/{referenceNumber}/close` - Terminate session

---

## Related

- [Authentication](guides/authentication.md) - Getting access tokens
- [Sessions](guides/sessions.md) - Session management
