# Permissions

Permissions are managed through `auth.permissions`.

## Grant Person Permissions

```python
result = auth.permissions.grant_person(
    subject_type="pesel",
    subject_value="12345678901",
    permissions=["invoice_read", "invoice_write"],
    description="Person invoice access",
    first_name="Jan",
    last_name="Kowalski",
)
print(result.reference_number)
```

SDK endpoint: `POST /permissions/persons/grants`

## Grant Entity Permissions

```python
from ksef2.domain.models import EntityPermission

result = auth.permissions.grant_entity(
    subject_value="5261040828",
    permissions=[
        EntityPermission(type="invoice_read", can_delegate=True),
    ],
    description="Entity invoice read access",
    entity_name="Example Entity",
)
print(result.reference_number)
```

SDK endpoint: `POST /permissions/entities/grants`

## Grant Authorizations

```python
result = auth.permissions.grant_authorization(
    subject_type="nip",
    subject_value="5261040828",
    permission="self_invoicing",
    description="Self-invoicing authorization",
    entity_name="Example Entity",
)
print(result.reference_number)
```

SDK endpoint: `POST /permissions/authorizations/grants`

## Query Permissions

```python
from ksef2.domain.models.pagination import OffsetPaginationParams
from ksef2.domain.models.permissions import (
    AuthorizationPermissionsQuery,
    PersonalPermissionsQuery,
    PersonPermissionsQuery,
    SubordinateEntityRolesQuery,
    SubunitPermissionsQuery,
)

persons = auth.permissions.query_persons(
    query=PersonPermissionsQuery(
        query_type="in_context",
        permission_types=["invoice_read"],
    )
)
print(len(persons.permissions))

authorizations = auth.permissions.query_authorizations(
    query=AuthorizationPermissionsQuery(query_type="granted"),
    params=OffsetPaginationParams(page_offset=0, page_size=20),
)
print(len(authorizations.authorization_grants))

personal = auth.permissions.query_personal(
    query=PersonalPermissionsQuery(permission_state="active")
)
print(len(personal.permissions))

subordinate = auth.permissions.query_subordinate_entities(
    query=SubordinateEntityRolesQuery()
)
print(len(subordinate.roles))

subunits = auth.permissions.query_subunits(
    query=SubunitPermissionsQuery()
)
print(len(subunits.permissions))
```

SDK endpoints:
- `POST /permissions/query/persons/grants`
- `POST /permissions/query/authorizations/grants`
- `POST /permissions/query/personal/grants`
- `POST /permissions/query/subordinate-entities/roles`
- `POST /permissions/query/subunits/grants`

## Attachment Permission Status

```python
status = auth.permissions.get_attachment_permission_status()
print(status.is_attachment_allowed)
```

SDK endpoint: `GET /permissions/attachments/status`

## Operation Status

Permission grants and revocations return a reference number. Use it to inspect async status:

```python
operation = auth.permissions.get_operation_status(reference_number=result.reference_number)
print(operation.status.code, operation.status.description)
```

SDK endpoint: `GET /permissions/operations/{referenceNumber}`

## Revoke Granted Permissions

```python
auth.permissions.revoke_common(permission_id="permission-id")
auth.permissions.revoke_authorization(permission_id="permission-id")
```

SDK endpoints:
- `DELETE /permissions/common/grants/{permissionId}`
- `DELETE /permissions/authorizations/grants/{permissionId}`

## Examples

- [`scripts/examples/permissions/grant_permissions.py`](../../scripts/examples/permissions/grant_permissions.py)
- [`scripts/examples/permissions/query_permissions.py`](../../scripts/examples/permissions/query_permissions.py)
- [`scripts/examples/permissions/query.py`](../../scripts/examples/permissions/query.py)

## Related

- [Authentication](authentication.md)
- [Test Data](testdata.md)
