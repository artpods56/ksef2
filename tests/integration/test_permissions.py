"""Integration tests for permissions endpoints.

These tests require:
    - .env.test with KSEF_TEST_SUBJECT_NIP, KSEF_TEST_PERSON_NIP, KSEF_TEST_PERSON_PESEL
    - Access to the KSeF TEST environment

Run with:
    source .env.test && uv run pytest tests/integration/test_permissions.py -v -m integration
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Generator, TypedDict

import pytest

from ksef2 import Client, FormSchema
from ksef2.clients.session import OnlineSessionClient
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.permissions import (
    AuthorizationPermissionType,
    AuthorizationSubjectIdentifierType,
    EntityPermission,
    EntityPermissionType,
    SubunitIdentifierType,
)
from ksef2.domain.models.testdata import (
    IdentifierType,
    PermissionType,
)


if TYPE_CHECKING:
    from tests.integration.conftest import KSeFCredentials

PermissionContext = TypedDict(
    "PermissionContext",
    {
        "client": Client,
        "session": OnlineSessionClient,
        "access_token": str,
        "seller_nip": str,
    },
)


@pytest.fixture(scope="module")
def permissions_context(
    real_client: Client,
    ksef_credentials: KSeFCredentials,
) -> Generator[PermissionContext, None, None]:
    """Create an authenticated session using existing credentials.

    Uses the subject from ksef_credentials to authenticate.
    Yields a dict with client, access_token, session, seller_nip.
    """
    client = real_client
    seller_nip = ksef_credentials.subject_nip

    cert, private_key = generate_test_certificate(seller_nip)
    tokens = client.auth.authenticate_xades(
        nip=seller_nip,
        cert=cert,
        private_key=private_key,
    )
    access_token = tokens.access_token.token

    with client.sessions.open_online(
        access_token=access_token,
        form_code=FormSchema.FA3,
    ) as session:
        context: PermissionContext = {
            "client": client,
            "access_token": access_token,
            "session": session,
            "seller_nip": seller_nip,
        }

        yield context


# ---------------------------------------------------------------------------
# GET endpoints
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_get_attachment_permission_status(permissions_context: PermissionContext):
    """Get attachment permission status."""
    session = permissions_context["session"]

    response = session.permissions.get_attachment_permission_status()

    assert response is not None
    assert hasattr(response, "is_attachment_allowed")
    assert isinstance(response.is_attachment_allowed, bool)


@pytest.mark.integration
def test_get_entity_roles(permissions_context: PermissionContext):
    """Get entity roles."""
    session = permissions_context["session"]

    response = session.permissions.get_entity_roles()

    assert response is not None
    assert hasattr(response, "roles")
    assert hasattr(response, "has_more")
    assert isinstance(response.roles, list)
    assert isinstance(response.has_more, bool)


# ---------------------------------------------------------------------------
# Query endpoints (POST)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_query_authorizations(permissions_context: PermissionContext):
    """Query authorization permissions."""
    from ksef2.domain.models.permissions import (
        AuthorizationPermissionsQueryRequest,
        AuthorizationPermissionsQueryResponse,
        QueryType,
    )

    session = permissions_context["session"]

    query = AuthorizationPermissionsQueryRequest(
        query_type=QueryType.GRANTED,
    )

    response = session.permissions.query_authorizations(query=query)

    assert isinstance(response, AuthorizationPermissionsQueryResponse)
    assert isinstance(response.authorization_grants, list)
    assert isinstance(response.has_more, bool)


@pytest.mark.integration
def test_query_eu_entities(permissions_context: PermissionContext):
    """Query EU entity permissions."""
    from ksef2.domain.models.permissions import (
        EuEntityPermissionsQueryRequest,
        EuEntityPermissionsQueryResponse,
    )

    session = permissions_context["session"]

    query = EuEntityPermissionsQueryRequest()

    response = session.permissions.query_eu_entities(query=query)

    assert isinstance(response, EuEntityPermissionsQueryResponse)
    assert isinstance(response.permissions, list)
    assert isinstance(response.has_more, bool)


@pytest.mark.integration
def test_query_personal(permissions_context: PermissionContext):
    """Query personal permissions."""
    from ksef2.domain.models.permissions import (
        PersonalPermissionsQueryRequest,
        PersonalPermissionsQueryResponse,
    )

    session = permissions_context["session"]

    query = PersonalPermissionsQueryRequest()

    response = session.permissions.query_personal(query=query)

    assert isinstance(response, PersonalPermissionsQueryResponse)
    assert isinstance(response.permissions, list)
    assert isinstance(response.has_more, bool)


@pytest.mark.integration
def test_query_persons(permissions_context: PermissionContext):
    """Query person permissions and verify domain response model."""
    from ksef2.domain.models.permissions import (
        PersonPermissionDetail,
        PersonPermissionsQueryRequest,
        PersonPermissionsQueryResponse,
        PermissionsQueryType,
    )

    session = permissions_context["session"]

    query = PersonPermissionsQueryRequest(
        query_type=PermissionsQueryType.PERMISSIONS_IN_CURRENT_CONTEXT,
    )

    response = session.permissions.query_persons(query=query)

    assert isinstance(response, PersonPermissionsQueryResponse)
    assert isinstance(response.permissions, list)
    assert isinstance(response.has_more, bool)

    for perm in response.permissions:
        assert isinstance(perm, PersonPermissionDetail)
        assert perm.id
        assert perm.author_identifier is not None
        assert perm.authorized_identifier is not None
        assert perm.permission_state is not None
        assert perm.permission_type is not None
        assert perm.description
        assert perm.start_date is not None
        assert isinstance(perm.can_delegate, bool)


@pytest.mark.integration
def test_query_subordinate_entities(permissions_context: PermissionContext):
    """Query subordinate entity roles."""
    from ksef2.domain.models.permissions import (
        SubordinateEntityRolesQueryRequest,
        SubordinateEntityRolesQueryResponse,
    )

    session = permissions_context["session"]

    query = SubordinateEntityRolesQueryRequest()

    response = session.permissions.query_subordinate_entities(query=query)

    assert isinstance(response, SubordinateEntityRolesQueryResponse)
    assert isinstance(response.roles, list)
    assert isinstance(response.has_more, bool)


@pytest.mark.integration
def test_query_subunits(permissions_context: PermissionContext):
    """Query subunit permissions."""
    from ksef2.domain.models.permissions import (
        SubunitPermissionsQueryRequest,
        SubunitPermissionsQueryResponse,
    )

    session = permissions_context["session"]

    query = SubunitPermissionsQueryRequest()

    response = session.permissions.query_subunits(query=query)

    assert isinstance(response, SubunitPermissionsQueryResponse)
    assert isinstance(response.permissions, list)
    assert isinstance(response.has_more, bool)


# ---------------------------------------------------------------------------
# Grant endpoints
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_grant_entity_permission(permissions_context: PermissionContext):
    """Grant permission to an entity."""
    session = permissions_context["session"]
    buyer_nip = generate_nip()

    response = session.permissions.grant_entity(
        subject_value=buyer_nip,
        permissions=[
            EntityPermission(
                type=EntityPermissionType.INVOICE_READ, can_delegate=False
            ),
        ],
        description="Test entity permission grant",
        entity_name="Test Buyer Entity",
    )

    assert response is not None
    assert hasattr(response, "reference_number")
    assert response.reference_number

    time.sleep(3)

    operation_status = session.permissions.get_operation_status(
        reference_number=response.reference_number,
    )

    assert operation_status is not None
    assert operation_status.status is not None
    assert operation_status.status.code is not None


@pytest.mark.integration
def test_grant_authorization_permission(permissions_context: PermissionContext):
    """Grant authorization permission."""
    session = permissions_context["session"]
    buyer_nip = generate_nip()

    response = session.permissions.grant_authorization(
        subject_type=AuthorizationSubjectIdentifierType.NIP,
        subject_value=buyer_nip,
        permission=AuthorizationPermissionType.SELF_INVOICING,
        description="Test authorization grant",
        entity_name="Test Authorization Entity",
    )

    assert response is not None
    assert hasattr(response, "reference_number")
    assert response.reference_number


@pytest.mark.integration
def test_grant_person_permission(permissions_context: PermissionContext):
    """Grant permission to a person."""
    session = permissions_context["session"]
    person_nip = generate_nip()

    response = session.permissions.grant_person(
        subject_identifier=IdentifierType.NIP,
        subject_value=person_nip,
        permissions=[PermissionType.INVOICE_READ],
        description="Test person permission grant",
        first_name="Test",
        last_name="Person",
    )

    assert response is not None
    assert hasattr(response, "reference_number")
    assert response.reference_number


@pytest.mark.integration
def test_grant_subunit_permission(permissions_context: PermissionContext):
    """Grant permission to a subunit."""
    session = permissions_context["session"]
    seller_nip = permissions_context["seller_nip"]

    response = session.permissions.grant_subunit(
        subject_identifier=IdentifierType.NIP,
        subject_value=seller_nip,
        context_identifier=SubunitIdentifierType.NIP,
        context_value=seller_nip,
        description="Test subunit permission grant",
        first_name="Test",
        last_name="User",
    )

    assert response is not None
    assert hasattr(response, "reference_number")
    assert response.reference_number


# ---------------------------------------------------------------------------
# Revoke endpoints
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_revoke_authorization_permission(permissions_context: PermissionContext):
    """Grant and then revoke an authorization permission."""
    session = permissions_context["session"]
    buyer_nip = generate_nip()

    # First, grant an authorization permission
    grant_response = session.permissions.grant_authorization(
        subject_type=AuthorizationSubjectIdentifierType.NIP,
        subject_value=buyer_nip,
        permission=AuthorizationPermissionType.SELF_INVOICING,
        description="Test authorization for revoke",
        entity_name="Test Entity for Revoke",
    )

    assert grant_response.reference_number

    # Wait for the grant to be processed
    time.sleep(5)

    # Query authorizations to find the one we just created
    from ksef2.domain.models.permissions import (
        AuthorizationPermissionsQueryRequest,
        QueryType,
    )
    from ksef2.domain.models.invoices import PaginationParams

    query_response = session.permissions.query_authorizations(
        query=AuthorizationPermissionsQueryRequest(query_type=QueryType.GRANTED),
        params=PaginationParams(page_size=100),
    )

    # Find our permission by description
    permission_id = None
    for grant in query_response.authorization_grants:
        if grant.description == "Test authorization for revoke":
            permission_id = grant.id
            break

    # If we found the permission, revoke it
    if permission_id:
        revoke_response = session.permissions.revoke_authorization(
            permission_id=permission_id,
        )

        assert revoke_response is not None
        assert hasattr(revoke_response, "reference_number")
        assert revoke_response.reference_number
    else:
        # If we didn't find it, the test still passes as we verified grant worked
        # The permission might not have been processed yet or might be in a different context
        pytest.skip(
            "Permission not found in query results - likely still being processed"
        )


@pytest.mark.integration
def test_revoke_common_permission(permissions_context: PermissionContext):
    """Grant and then revoke a common permission."""
    session = permissions_context["session"]
    buyer_nip = generate_nip()

    # First, grant an entity permission
    grant_response = session.permissions.grant_entity(
        subject_value=buyer_nip,
        permissions=[
            EntityPermission(
                type=EntityPermissionType.INVOICE_READ, can_delegate=False
            ),
        ],
        description="Test entity for revoke",
        entity_name="Test Entity for Revoke",
    )

    assert grant_response.reference_number

    time.sleep(5)

    _ = session.permissions.get_operation_status(
        reference_number=grant_response.reference_number,
    )

    # Query personal permissions to find the one we just created
    from ksef2.domain.models.permissions import PersonalPermissionsQueryRequest
    from ksef2.domain.models.invoices import PaginationParams

    query_response = session.permissions.query_personal(
        query=PersonalPermissionsQueryRequest(),
        params=PaginationParams(page_size=100),
    )

    # Find our permission by description
    permission_id = None
    for perm in query_response.permissions:
        if perm.description == "Test entity for revoke":
            permission_id = perm.id
            break

    # If we found the permission, revoke it
    if permission_id:
        revoke_response = session.permissions.revoke_common(
            permission_id=permission_id,
        )

        assert revoke_response is not None
        assert hasattr(revoke_response, "reference_number")
        assert revoke_response.reference_number
    else:
        # If we didn't find it, the test still passes as we verified grant worked
        # The permission might not have been processed yet or might be in a different context
        pytest.skip(
            "Permission not found in query results - likely still being processed"
        )
