# Test Data

The TEST environment provides test data APIs for setting up integration tests.

**Note:** These endpoints are only available on the TEST environment, not PRODUCTION or DEMO.

---

## Operations

### Create Subject

Create a test subject (organization/entity).

**SDK Endpoint:** `POST /testdata/subject`

---

### Create Person

Create a test person associated with a subject.

**SDK Endpoint:** `POST /testdata/person`

---

### Grant Permissions

Grant permissions to a person for a subject context.

**SDK Endpoint:** `POST /testdata/permissions`

---

### Revoke Permissions

Revoke previously granted permissions.

**SDK Endpoint:** `POST /testdata/permissions/revoke`

---

### Delete Subject

Delete a test subject.

**SDK Endpoint:** `POST /testdata/subject/remove`

---

### Delete Person

Delete a test person.

**SDK Endpoint:** `POST /testdata/person/remove`

---

## Automatic Cleanup

Use `temporal()` for automatic cleanup. The context manager tracks created entities and cleans them up on exit, even if errors occur. Duplicate creation errors are suppressed within the context manager.

```python
from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
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
        description="Example organization",
    )
    temp.create_person(
        nip=PERSON_NIP, pesel=PERSON_PESEL, description="Example person",
    )
    temp.grant_permissions(
        context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
        authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
        permissions=[
            Permission(type=PermissionType.INVOICE_READ, description="Read invoices"),
            Permission(type=PermissionType.INVOICE_WRITE, description="Send invoices"),
        ],
    )

    # Tests run here

# Automatic cleanup on exit:
# 1. Revoke permissions
# 2. Delete person
# 3. Delete subject
```

## Manual Cleanup

You can also manage test data manually, but this requires explicit cleanup and error handling:

```python
from ksef2.core import exceptions

# Create
client.testdata.create_subject(
    nip=ORG_NIP,
    subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
    description="Example organization",
)
client.testdata.create_person(
    nip=PERSON_NIP, pesel=PERSON_PESEL, description="Example person",
)
client.testdata.grant_permissions(
    context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
    authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
    permissions=[
        Permission(type=PermissionType.INVOICE_READ, description="Read invoices"),
        Permission(type=PermissionType.INVOICE_WRITE, description="Send invoices"),
    ],
)

# Clean up (must be done manually)
client.testdata.revoke_permissions(
    context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
    authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
)
client.testdata.delete_person(nip=PERSON_NIP)
client.testdata.delete_subject(nip=ORG_NIP)
```

> Full example: [`scripts/examples/testdata/setup_test_data.py`](../../scripts/examples/testdata/setup_test_data.py)

---

## Subject Types

| Type | Description |
|------|-------------|
| `VAT_GROUP` | VAT group |
| `ENFORCEMENT_AUTHORITY` | Enforcement authority |
| `JST` | Local government |

---

## Permission Types

| Permission | Description |
|------------|-------------|
| `INVOICE_READ` | Read invoices |
| `INVOICE_WRITE` | Send invoices |
| `INTROSPECTION` | Search invoices |
| `CREDENTIALS_READ` | Read credentials |
| `CREDENTIALS_MANAGE` | Manage credentials |
| `ENFORCEMENT_OPERATIONS` | Enforcement operations |
| `SUBUNIT_MANAGE` | Manage subunits |

---

## Related

- [Authentication](authentication.md) - Using XAdES auth
- [Tokens](tokens.md) - Token generation
