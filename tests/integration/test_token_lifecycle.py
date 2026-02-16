"""Integration tests for the full token lifecycle: generate → status → revoke.

Run with:
    uv run pytest tests/integration/test_token_lifecycle.py -v -m integration
"""

from __future__ import annotations

import pytest

from ksef2 import Client, Environment
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
    TokenPermission,
    TokenStatus,
    TokenStatusResponse,
)


@pytest.fixture(scope="module")
def token_context():
    """Create subject with CredentialsManage, authenticate, generate a token.

    Yields (client, access_token, generated_token).
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
        tokens = client.auth.authenticate_xades(
            nip=org_nip,
            cert=cert,
            private_key=private_key,
        )
        access_token = tokens.access_token.token

        generated = client.tokens.generate(
            access_token=access_token,
            permissions=[TokenPermission.INVOICE_READ],
            description="Integration test token",
        )

        yield client, access_token, generated


@pytest.mark.integration
def test_generate_token(token_context):
    """Generate returns a token with reference number."""
    _client, _access_token, generated = token_context

    assert isinstance(generated, GenerateTokenResponse)
    assert generated.reference_number
    assert generated.token


@pytest.mark.integration
def test_token_status(token_context):
    """Check status of a generated token."""
    client, access_token, generated = token_context

    status = client.tokens.status(
        access_token=access_token,
        reference_number=generated.reference_number,
    )

    assert isinstance(status, TokenStatusResponse)
    assert status.reference_number == generated.reference_number
    assert status.status == TokenStatus.ACTIVE


@pytest.mark.integration
def test_revoke_token(token_context):
    """Revoke a generated token and verify status changes."""
    client, access_token, generated = token_context

    client.tokens.revoke(
        access_token=access_token,
        reference_number=generated.reference_number,
    )

    status = client.tokens.status(
        access_token=access_token,
        reference_number=generated.reference_number,
    )

    assert status.status in (TokenStatus.REVOKING, TokenStatus.REVOKED)
