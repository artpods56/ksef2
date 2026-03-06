# Sessions

The SDK exposes two different session concepts:

1. Authentication sessions through `auth.sessions`
2. Invoice sessions through `auth.online_session()`, `auth.batch_session()`, and `auth.session_log`

This guide focuses on invoice sessions.

## Open an Online Session

```python
from pathlib import Path

from ksef2 import FormSchema

with auth.online_session(form_code=FormSchema.FA3) as session:
    result = session.send_invoice(invoice_xml=Path("invoice.xml").read_bytes())
    print(result.reference_number)
```

Manual lifecycle is also supported:

```python
session = auth.online_session(form_code=FormSchema.FA3)
try:
    result = session.send_invoice(invoice_xml=b"<Invoice />")
finally:
    session.close()
```

SDK endpoints:
- `POST /sessions/online`
- `POST /sessions/online/{referenceNumber}/close`

## Session Status and Contents

```python
status = session.get_status()
print(status.status.code, status.status.description)

state = session.get_state()
print(state.reference_number, state.valid_until)

invoices = session.list_invoices()
failed = session.list_failed_invoices()
print(len(invoices.invoices), len(failed.invoices))
```

## Resume an Online Session

```python
from ksef2.domain.models.session import OnlineSessionState

state = session.get_state()
payload = state.model_dump_json()

restored_state = OnlineSessionState.model_validate_json(payload)
resumed = auth.resume_online_session(state=restored_state)
resumed.close()
```

Example:
- [`scripts/examples/session/session_resume.py`](../../scripts/examples/session/session_resume.py)

## Query Historical Invoice Sessions

Use `auth.session_log` to inspect previously opened invoice sessions.

```python
sessions = auth.session_log.query(session_type="online")
for item in sessions.sessions:
    print(item.reference_number, item.status.description)
```

To iterate all pages:

```python
for page in auth.session_log.all(session_type="online"):
    print(len(page.sessions))
```

SDK endpoint: `GET /sessions`

## Examples

- [`scripts/examples/session/workflow.py`](../../scripts/examples/session/workflow.py)
- [`scripts/examples/session/session_resume.py`](../../scripts/examples/session/session_resume.py)
- [`scripts/examples/session/session_management.py`](../../scripts/examples/session/session_management.py)

## Related

- [Invoices](invoices.md)
- [Authentication](authentication.md)
