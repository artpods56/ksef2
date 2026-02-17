"""Integration tests for the full token lifecycle: generate → status → revoke.

Run with:
    uv run pytest tests/integration/test_token_lifecycle.py -v -m integration
"""

from __future__ import annotations

import pytest

from ksef2 import Client, Environment
from ksef2.clients.authenticated import AuthenticatedClient
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)
from ksef2.domain.models.tokens import (
    GenerateTokenResponse,
    QueryTokensResponse,
    TokenAuthorIdentifier,
    TokenAuthorIdentifierType,
    TokenPermission,
    TokenStatus,
    TokenStatusResponse,
)


@pytest.fixture(scope="module")
def token_context():
    """Create subject with CredentialsManage, authenticate, generate a token.

    Yields (client, auth, generated_token).
    """
    client = Client(environment=Environment.TEST)

    org_nip = generate_nip()
    person_nip = generate_nip()
    person_pesel = generate_pesel()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=org_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Token lifecycle test",
        )
        temp.create_person(
            nip=person_nip,
            pesel=person_pesel,
            description="Token lifecycle person",
        )
        temp.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value=org_nip),
            authorized=Identifier(type=IdentifierType.NIP, value=person_nip),
            permissions=[
                Permission(
                    type=PermissionType.INVOICE_WRITE,
                    description="Send invoices",
                ),
                Permission(
                    type=PermissionType.INVOICE_READ,
                    description="Read invoices",
                ),
                Permission(
                    type=PermissionType.CREDENTIALS_MANAGE,
                    description="Manage credentials",
                ),
            ],
        )

        cert, private_key = generate_test_certificate(org_nip)
        auth = client.auth.authenticate_xades(
            nip=org_nip,
            cert=cert,
            private_key=private_key,
        )

        generated = auth.tokens.generate(
            permissions=[TokenPermission.INVOICE_READ],
            description="Integration test token",
        )

        yield client, auth, generated


@pytest.mark.integration
def test_generate_token(token_context):
    """Generate returns a token with reference number."""
    _client, _auth, generated = token_context

    assert isinstance(generated, GenerateTokenResponse)
    assert generated.reference_number
    assert generated.token


@pytest.mark.integration
def test_token_status(token_context):
    """Check status of a generated token."""
    _client, auth, generated = token_context

    assert isinstance(auth, AuthenticatedClient)

    status = auth.tokens.status(
        reference_number=generated.reference_number,
    )

    assert isinstance(status, TokenStatusResponse)
    assert status.reference_number == generated.reference_number
    assert status.status == TokenStatus.ACTIVE


@pytest.mark.integration
def test_revoke_token(token_context):
    """Revoke a generated token and verify status changes."""
    _client, auth, generated = token_context

    auth.tokens.revoke(
        reference_number=generated.reference_number,
    )

    status = auth.tokens.status(
        reference_number=generated.reference_number,
    )

    assert status.status in (TokenStatus.REVOKING, TokenStatus.REVOKED)


@pytest.mark.integration
def test_list_tokens(token_context):
    """List tokens and verify the generated token appears."""
    _client, auth, generated = token_context

    response = auth.tokens.list()

    assert isinstance(response, QueryTokensResponse)
    assert isinstance(response.tokens, list)

    # Find the generated token in the list
    ref_numbers = [t.reference_number for t in response.tokens]
    assert generated.reference_number in ref_numbers


@pytest.mark.integration
def test_list_tokens_with_status_filter(token_context):
    """List tokens filtered by status."""
    _client, auth, _generated = token_context

    # Filter by ACTIVE and REVOKED statuses
    response = auth.tokens.list(
        status=[TokenStatus.ACTIVE, TokenStatus.REVOKED],
    )

    assert isinstance(response, QueryTokensResponse)
    # All returned tokens should have ACTIVE or REVOKED status
    for token in response.tokens:
        assert token.status in (TokenStatus.ACTIVE, TokenStatus.REVOKED)


@pytest.mark.integration
def test_list_tokens_with_description_filter(token_context):
    """List tokens filtered by description."""
    _client, auth, _generated = token_context

    response = auth.tokens.list(
        description="Integration test",
    )

    assert isinstance(response, QueryTokensResponse)
    # All returned tokens should contain "integration test" in description (case-insensitive)
    for token in response.tokens:
        assert "integration test" in token.description.lower()


@pytest.mark.integration
def test_list_tokens_with_author_filter(token_context):
    """List tokens filtered by author identifier."""
    _client, auth, _generated = token_context

    # First, get all tokens to find an author NIP
    all_tokens = auth.tokens.list()
    if not all_tokens.tokens:
        pytest.skip("No tokens available to test author filter")

    # Use the first token's author for filtering
    first_author = all_tokens.tokens[0].author_identifier

    author_filter = TokenAuthorIdentifier(
        type=TokenAuthorIdentifierType(first_author.type.value),
        value=first_author.value,
    )

    response = auth.tokens.list(
        author_filter=author_filter,
    )

    assert isinstance(response, QueryTokensResponse)
    # All returned tokens should have the same author
    for token in response.tokens:
        assert token.author_identifier.value == first_author.value
