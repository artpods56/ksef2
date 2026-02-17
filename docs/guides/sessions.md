# Sessions

Manage KSeF sessions for invoice operations.

## Session Types

KSeF has two types of sessions:

1. **Authentication Sessions** (`/auth/sessions/*`) - Manage authenticated sessions and refresh tokens
2. **Invoice Sessions** (`/sessions/online`, `/sessions/batch`) - Send and process invoices

For authentication session management, see [Authentication](guides/authentication.md).

## Invoice Sessions

### Open Session

Start a new online session for invoice operations. Sessions can be used as context managers for automatic cleanup, or managed manually.

**SDK Endpoint:** `POST /sessions/online`

```python
from ksef2 import Client, Environment, FormSchema

client = Client(Environment.TEST)

# Context manager (recommended) — session terminates automatically
with client.sessions.open_online(
    access_token=tokens.access_token.token,
    form_code=FormSchema.FA3,
) as session:
    with open("invoice.xml", "rb") as f:
        result = session.send_invoice(f.read())
    print(result.reference_number)

# Manual management
session = client.sessions.open_online(
    access_token=tokens.access_token.token,
    form_code=FormSchema.FA3,
)
try:
    with open("invoice.xml", "rb") as f:
        result = session.send_invoice(f.read())
finally:
    session.terminate()
```

---

### Get Session Status

Get the current status of an active session.

```python
status = session.get_status()
print(f"Status: {status}")

state = session.get_state()
print(f"Reference: {state.reference_number}")
print(f"Valid until: {state.valid_until}")
```

---

### List Sessions

List all active invoice sessions.

**SDK Endpoint:** `GET /sessions`

```python
from ksef2.domain.models.session import QuerySessionsList, SessionType

sessions = client.sessions.list(
    access_token=access_token,
    query=QuerySessionsList(session_type=SessionType.ONLINE),
)
print(sessions)
```

---

### Resume Session

Resume an existing session from saved state. The session state is a Pydantic model that can be serialized/deserialized for passing between processes.

**SDK Endpoint:** Uses stored session state

```python
from ksef2.domain.models.session import OnlineSessionState

# Save session state
state: OnlineSessionState = session.get_state()
state_json = state.model_dump_json()

# --- Pass state_json to another process (e.g. via database or message queue) ---

# Restore and resume
restored_state = OnlineSessionState.model_validate_json(state_json)
resumed_session = client.sessions.resume(state=restored_state)

# Use the resumed session as normal
# resumed_session.send_invoice(invoice_xml)

# Terminate manually when done
resumed_session.terminate()
```

> Full example: [`scripts/examples/session/session_resume.py`](../../scripts/examples/session/session_resume.py)

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

- [Invoices](invoices.md) - Invoice operations within sessions
- [Authentication](authentication.md) - Getting access tokens
