# Invoices

Send, download, and manage structured invoices in KSeF.

## Operations

### Send Invoice

Upload a structured invoice to KSeF.

**Endpoint:** `POST /online/sendInvoice`

**KSeF API:** [`/online/sendInvoice`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Faktury/paths/~1online~1sendInvoice/post)

---

### Download Invoice

Download an invoice by its KSeF reference number.

**Endpoint:** `POST /online/getInvoice`

**KSeF API:** [`/online/getInvoice`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Faktury/paths/~1online~1getInvoice/post)

---

### Search Invoices

Search for invoices by various criteria.

**Endpoint:** `POST /online/searchInvoices`

**KSeF API:** [`/online/searchInvoices`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Faktury/paths/~1online~1searchInvoices/post)

---

## Sessions

All invoice operations require an active session:

```python
with client.sessions.open_online(access_token=token) as session:
    session.send_invoice(...)
    invoice = session.download_invoice(...)
```

**Session endpoints:**
- `POST /online/session` - Open session
- `DELETE /online/session` - Terminate session

---

## Related

- [Authentication](guides/authentication.md) - Getting access tokens
- [Sessions](guides/sessions.md) - Session management
- KSeF API: [Invoices](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Faktury)
