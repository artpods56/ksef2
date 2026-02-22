# Permissions

Grant and query permissions for persons, entities, and authorizations in KSeF.

## Operations

### Grant Person Permissions

Grant permissions to a person identified by PESEL or NIP.

```python
from ksef2.domain.models import IdentifierType, PermissionType

result = auth.permissions.grant_person(
    subject_identifier=IdentifierType.PESEL,
    subject_value="12345678901",
    permissions=[PermissionType.INVOICE_READ, PermissionType.INVOICE_WRITE],
    description="Person invoice access",
    first_name="John",
    last_name="Doe",
)
print(f"Person permissions granted: {result.reference_number}")
```

---

### Grant Entity Permissions

Grant permissions to an entity (organization) identified by NIP. Entity permissions support delegation via `can_delegate`.

```python
from ksef2.domain.models import EntityPermission, EntityPermissionType

result = auth.permissions.grant_entity(
    subject_value=PARTNER_NIP,
    permissions=[
        EntityPermission(
            type=EntityPermissionType.INVOICE_READ,
            can_delegate=True,
        ),
    ],
    description="Entity invoice read access",
    entity_name="Test Entity",
)
print(f"Entity permissions granted: {result.reference_number}")
```

---

### Grant Authorization

Grant a self-invoicing or other authorization to a subject.

```python
from ksef2.domain.models import (
    AuthorizationPermissionType,
    AuthorizationSubjectIdentifierType,
)

result = auth.permissions.grant_authorization(
    subject_type=AuthorizationSubjectIdentifierType.NIP,
    subject_value=PARTNER_NIP,
    permissions=AuthorizationPermissionType.SELF_INVOICING,
    description="Self-invoicing authorization",
    entity_name="Test Partner Entity",
)
```

---

### Query Person Permissions

Query permissions granted to persons in the current context. Optionally filter by permission type.

```python
from ksef2.domain.models.permissions import (
    PersonPermissionsQueryRequest,
    PermissionsQueryType,
)
from ksef2.domain.models import PermissionType

# All person permissions in current context
resp = auth.permissions.query_persons(
    query=PersonPermissionsQueryRequest(
        query_type=PermissionsQueryType.PERMISSIONS_IN_CURRENT_CONTEXT,
    ),
)

# Filtered by permission type
resp = auth.permissions.query_persons(
    query=PersonPermissionsQueryRequest(
        query_type=PermissionsQueryType.PERMISSIONS_IN_CURRENT_CONTEXT,
        permission_types=[PermissionType.CREDENTIALS_MANAGE],
    ),
)
```

---

### Query Authorization Permissions

Query granted or received authorizations.

```python
from ksef2.domain.models.permissions import (
    AuthorizationPermissionsQueryRequest,
    QueryType,
)
from ksef2.domain.models.pagination import PaginationParams

# Granted authorizations
resp = auth.permissions.query_authorizations(
    query=AuthorizationPermissionsQueryRequest(
        query_type=QueryType.GRANTED,
    ),
)

# Received authorizations with pagination
resp = auth.permissions.query_authorizations(
    query=AuthorizationPermissionsQueryRequest(
        query_type=QueryType.RECEIVED,
    ),
    params=PaginationParams(page_offset=0, page_size=20),
)
```

---

### Query Personal Permissions

Query permissions assigned to the currently authenticated user. Optionally filter by state.

```python
from ksef2.domain.models.permissions import (
    PersonalPermissionsQueryRequest,
    PermissionState,
)

# All personal permissions
resp = auth.permissions.query_personal(
    query=PersonalPermissionsQueryRequest(),
)

# Only active permissions
resp = auth.permissions.query_personal(
    query=PersonalPermissionsQueryRequest(
        permission_state=PermissionState.ACTIVE,
    ),
)
```

---

### Query EU Entity Permissions

Query permissions for EU entities.

```python
from ksef2.domain.models.permissions import EuEntityPermissionsQueryRequest

resp = auth.permissions.query_eu_entities(
    query=EuEntityPermissionsQueryRequest(),
)
```

---

### Query Subordinate Entity Roles

Query roles assigned to subordinate entities.

```python
from ksef2.domain.models.permissions import SubordinateEntityRolesQueryRequest

resp = auth.permissions.query_subordinate_entities(
    query=SubordinateEntityRolesQueryRequest(),
)
```

---

### Query Subunit Permissions

Query permissions assigned to subunits.

```python
from ksef2.domain.models.permissions import SubunitPermissionsQueryRequest

resp = auth.permissions.query_subunits(
    query=SubunitPermissionsQueryRequest(),
)
```

---

## Example

All permissions operations require an authenticated client. The example below sets up test data, authenticates, and grants permissions to a person and an entity:

```python
from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    IdentifierType,
    SubjectType,
    PermissionType,
    Identifier,
    Permission,
    EntityPermission,
    EntityPermissionType,
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
        nip=PERSON_NIP,
        pesel=PERSON_PESEL,
        description="Example person",
    )
    temp.grant_permissions(permissions=[
        Permission(
            type=PermissionType.CREDENTIALS_MANAGE,
            description="Manage credentials",
        ),
    ], grant_to=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
        in_context_of=Identifier(type=IdentifierType.NIP, value=ORG_NIP))

    cert, private_key = generate_test_certificate(ORG_NIP)

    # Authenticate and get an AuthenticatedClient
    auth = client.authentication.with_xades(
        nip=ORG_NIP, cert=cert, private_key=private_key,
    )

    # Grant permissions directly from authenticated client (no session needed!)
    result = auth.permissions.grant_person(
        subject_identifier=IdentifierType.PESEL,
        subject_value=PERSON_PESEL,
        permissions=[PermissionType.INVOICE_READ, PermissionType.INVOICE_WRITE],
        description="Test person permissions",
        first_name="John",
        last_name="Doe",
    )
    print(f"Person permissions granted: {result.reference_number}")

    result = auth.permissions.grant_entity(
        subject_value=ORG_NIP,
        permissions=[
            EntityPermission(
                type=EntityPermissionType.INVOICE_READ,
                can_delegate=True,
            ),
        ],
        description="Test entity permissions",
        entity_name="Test Entity",
    )
    print(f"Entity permissions granted: {result.reference_number}")
```

> Full examples: [`scripts/examples/permissions/grant_permissions.py`](../../scripts/examples/permissions/grant_permissions.py), [`scripts/examples/permissions/query_permissions.py`](../../scripts/examples/permissions/query_permissions.py)

---

## Related

- [Authentication](authentication.md) - Getting access tokens
- [Sessions](sessions.md) - Session management
- [Test Data](testdata.md) - Setting up test environment
