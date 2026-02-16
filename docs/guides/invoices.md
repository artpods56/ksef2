# Invoices

Send, download, and manage structured invoices in KSeF.

## Operations

### Send Invoice

Upload a structured invoice to KSeF.

**SDK Endpoint:** `POST /sessions/online/{referenceNumber}/invoices`

```python
from ksef2.core.invoices import InvoiceFactory

template_xml = "path/to/invoice-template.xml".read_text(encoding="utf-8")
invoice_xml = InvoiceFactory.create(
    template_xml,
    {
        "#nip#": ORG_NIP,
        "#invoicing_date#": date.today().isoformat(),
        "#invoice_number#": "123/2024",
    },
)
invoice_ref = session.send_invoice(invoice_xml=invoice_xml)
print(f"Invoice sent: {invoice_ref.reference_number}")
```

---

### List Invoices

List all invoices in the current session.

**SDK Endpoint:** `GET /sessions/online/{referenceNumber}/invoices`

```python
invoices = session.list_invoices()
for invoice in invoices.invoices:
    print(f"KSeF Number: {invoice.ksefNumber}, Status: {invoice.status}")
```

---

### List Failed Invoices

List invoices that failed processing.

**SDK Endpoint:** `GET /sessions/online/{referenceNumber}/invoices/failed`

```python
failed = session.list_failed_invoices()
print(f"Failed invoices: {failed}")
```

---

### Get UPO

Get the UPO (Urzędowe Poświadczenie Odbioru - Official Receipt Confirmation) for an invoice.

**SDK Endpoint:** `GET /invoices/ksef/{ksefNumber}/upo`

```python
upo = session.get_invoice_upo_by_ksef_number(ksef_number="KSEF-NUMBER")
print(f"UPO size: {len(upo)} bytes")
```

---

### Download Invoice

Download an invoice by its KSeF reference number.

**SDK Endpoint:** `GET /invoices/ksef/{ksefNumber}`

---

## Example

All invoice operations require an active session. The example below sets up test data, authenticates, opens a session, and sends an invoice:

```python
from ksef2 import Client, FormSchema, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import (
    Identifier, IdentifierType, Permission, PermissionType, SubjectType,
)

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

client = Client(environment=Environment.TEST)

with client.testdata.temporal() as temp:
    temp.create_subject(
        nip=ORG_NIP,
        subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
        description="SDK test seller",
    )
    temp.create_person(
        nip=PERSON_NIP, pesel=PERSON_PESEL, description="Example person",
    )
    temp.grant_permissions(
        context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
        authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
        permissions=[
            Permission(type=PermissionType.INVOICE_WRITE, description="Send invoices"),
        ],
    )

    cert, private_key = generate_test_certificate(PERSON_NIP)
    tokens = client.auth.authenticate_xades(
        nip=PERSON_NIP, cert=cert, private_key=private_key,
    )

    with client.sessions.open_online(
        access_token=tokens.access_token.token,
        form_code=FormSchema.FA3,
    ) as session:
        with open("invoice.xml", "rb") as f:
            result = session.send_invoice(f.read())
        print(f"Invoice sent, reference number: {result.reference_number}")

```

> Full example: [`scripts/examples/invoices/send_invoice.py`](../../scripts/examples/invoices/send_invoice.py)

**Session SDK endpoints:**
- `POST /sessions/online` - Open session
- `POST /sessions/online/{referenceNumber}/close` - Terminate session

---

## Related

- [Authentication](authentication.md) - Getting access tokens
- [Sessions](sessions.md) - Session management
