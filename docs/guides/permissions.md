# Permissions

Grant and query permissions for persons, entities, and authorizations in KSeF.

## Operations

### Grant Person Permissions

Grant permissions to a person identified by PESEL or NIP.

```python
from ksef2.domain.models import IdentifierType, PermissionType

result = session.permissions.grant_person(
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

result = session.permissions.grant_entity(
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

result = session.permissions.grant_authorization(
    subject_type=AuthorizationSubjectIdentifierType.NIP,
    subject_value=PARTNER_NIP,
    permission=AuthorizationPermissionType.SELF_INVOICING,
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
resp = session.permissions.query_persons(
    query=PersonPermissionsQueryRequest(
        query_type=PermissionsQueryType.PERMISSIONS_IN_CURRENT_CONTEXT,
    ),
)

# Filtered by permission type
resp = session.permissions.query_persons(
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
from ksef2.domain.models.invoices import PaginationParams

# Granted authorizations
resp = session.permissions.query_authorizations(
    query=AuthorizationPermissionsQueryRequest(
        query_type=QueryType.GRANTED,
    ),
)

# Received authorizations with pagination
resp = session.permissions.query_authorizations(
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
resp = session.permissions.query_personal(
    query=PersonalPermissionsQueryRequest(),
)

# Only active permissions
resp = session.permissions.query_personal(
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

resp = session.permissions.query_eu_entities(
    query=EuEntityPermissionsQueryRequest(),
)
```

---

### Query Subordinate Entity Roles

Query roles assigned to subordinate entities.

```python
from ksef2.domain.models.permissions import SubordinateEntityRolesQueryRequest

resp = session.permissions.query_subordinate_entities(
    query=SubordinateEntityRolesQueryRequest(),
)
```

---

### Query Subunit Permissions

Query permissions assigned to subunits.

```python
from ksef2.domain.models.permissions import SubunitPermissionsQueryRequest

resp = session.permissions.query_subunits(
    query=SubunitPermissionsQueryRequest(),
)
```

---

## Example

All permissions operations require an active session. The example below sets up test data, authenticates, opens a session, and grants permissions to a person and an entity:

```python
from ksef2 import Client, Environment, FormSchema
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
    temp.grant_permissions(
        context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
        authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
        permissions=[
            Permission(
                type=PermissionType.CREDENTIALS_MANAGE,
                description="Manage credentials",
            ),
        ],
    )

    cert, private_key = generate_test_certificate(ORG_NIP)
    tokens = client.auth.authenticate_xades(
        nip=ORG_NIP, cert=cert, private_key=private_key,
    )

    with client.sessions.open_online(
        access_token=tokens.access_token.token,
        form_code=FormSchema.FA3,
    ) as session:
        result = session.permissions.grant_person(
            subject_identifier=IdentifierType.PESEL,
            subject_value=PERSON_PESEL,
            permissions=[PermissionType.INVOICE_READ, PermissionType.INVOICE_WRITE],
            description="Test person permissions",
            first_name="John",
            last_name="Doe",
        )
        print(f"Person permissions granted: {result.reference_number}")

        result = session.permissions.grant_entity(
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
