# Test Data

The TEST environment provides test data APIs for setting up integration tests.

**Note:** These endpoints are only available on the TEST environment, not PRODUCTION or DEMO.

**Base URL:** `https://api-test.ksef.mf.gov.pl/v2`

---

## Operations

### Create Subject

Create a test subject (organization/entity).

**Endpoint:** `POST /testdata/subject`

**KSeF API:** [`/testdata/subject`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Dane-testyowe/paths/~1testdata~1subject/post)

---

### Create Person

Create a test person associated with a subject.

**Endpoint:** `POST /testdata/person`

**KSeF API:** [`/testdata/person`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Dane-testyowe/paths/~1testdata~1person/post)

---

### Grant Permissions

Grant permissions to a person for a subject context.

**Endpoint:** `POST /testdata/permissions`

**KSeF API:** [`/testdata/permissions`](https://api-test.ksef.mf.gov.pl/docs/v2/index.html#tag/Dane-testyowe/paths/~1testdata~1permissions/post)

---

### Revoke Permissions

Revoke previously granted permissions.

**Endpoint:** `POST /testdata/permissions/revoke`

---

### Delete Subject

Delete a test subject.

**Endpoint:** `POST /testdata/subject/remove`

---

### Delete Person

Delete a test person.

**Endpoint:** `POST /testdata/person/remove`

---

## Automatic Cleanup

Use `temporal()` for automatic cleanup:

```python
with client.testdata.temporal() as td:
    td.create_subject(...)
    td.create_person(...)
    td.grant_permissions(...)
    
    # Tests run here
    
# Automatic cleanup:
# 1. Revoke permissions
# 2. Delete person
# 3. Delete subject
```

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

- [Authentication](guides/authentication.md) - Using XAdES auth
- [Tokens](guides/tokens.md) - Token generation
- KSeF API: [Test Data](https://api-test.ksef.mf.gov.pl/docs/v2)
