"""Integration tests for 'Status wysylki i UPO' endpoints.

These tests require:
    - .env.test with KSEF_TEST_SUBJECT_NIP, KSEF_TEST_PERSON_NIP, KSEF_TEST_PERSON_PESEL
    - Access to the KSeF TEST environment

Run with:
    source .env.test && uv run pytest tests/integration/test_invoices_status.py -v -m integration
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from ksef2 import Client, FormSchema, Environment
from ksef2.clients.authenticated import AuthenticatedClient
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.session import QuerySessionsList, SessionType, SessionStatus
from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)
from ksef2.infra.schema.api import spec

INVOICE_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "assets"
    / "sample_invoices"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)


@pytest.fixture(scope="module")
def session_with_invoice():
    """Open an online session, send one invoice, close the session, return context.

    Yields (client, access_token, session_ref, invoice_ref, session).
    """
    client = Client(environment=Environment.TEST)

    seller_nip = generate_nip()
    buyer_nip = generate_nip()
    person_nip = generate_nip()
    person_pesel = generate_pesel()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=seller_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Integration test seller",
        )
        temp.create_subject(
            nip=buyer_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Integration test buyer",
        )
        temp.create_person(
            nip=person_nip,
            pesel=person_pesel,
            description="Integration test person",
        )
        temp.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value=seller_nip),
            authorized=Identifier(type=IdentifierType.NIP, value=person_nip),
            permissions=[
                Permission(
                    type=PermissionType.INVOICE_WRITE,
                    description="Send invoices",
                ),
                Permission(
                    type=PermissionType.INTROSPECTION,
                    description="Introspect sessions",
                ),
            ],
        )

        cert, private_key = generate_test_certificate(seller_nip)
        auth = client.auth.authenticate_xades(
            nip=seller_nip,
            cert=cert,
            private_key=private_key,
        )
        access_token = auth.access_token

        with client.sessions.open_online(
            access_token=access_token,
            form_code=FormSchema.FA3,
        ) as session:
            template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
            invoice_xml = InvoiceFactory.create(
                template_xml,
                {
                    "#nip#": seller_nip,
                    "#subject2nip#": buyer_nip,
                    "#invoicing_date#": "2026-02-15",
                    "#invoice_number#": str(int(time.time())),
                },
            )
            result = session.send_invoice(invoice_xml=invoice_xml)
            invoice_ref = result.reference_number
            session_ref = session.get_state().reference_number

            yield client, access_token, session_ref, invoice_ref, session


# ---------------------------------------------------------------------------
# List sessions (via client.sessions.list — uses QuerySessionsList model)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_list_sessions(xades_authenticated_context: tuple[Client, AuthenticatedClient]):
    """List sessions filtered by type."""
    client, auth = xades_authenticated_context
    token = auth.access_token

    response = client.sessions.list(
        access_token=token,
        query=QuerySessionsList(session_type=SessionType.ONLINE),
    )

    assert isinstance(response, spec.SessionsQueryResponse)
    assert hasattr(response, "sessions")
    assert hasattr(response, "continuationToken")


@pytest.mark.integration
def test_list_sessions_batch(
    xades_authenticated_context: tuple[Client, AuthenticatedClient],
):
    """List batch sessions."""
    client, auth = xades_authenticated_context
    token = auth.access_token

    response = client.sessions.list(
        access_token=token,
        query=QuerySessionsList(session_type=SessionType.BATCH),
    )

    assert isinstance(response, spec.SessionsQueryResponse)


@pytest.mark.integration
def test_list_sessions_with_status_filter(
    xades_authenticated_context: tuple[Client, AuthenticatedClient],
):
    """List sessions filtered by statuses."""
    client, auth = xades_authenticated_context
    token = auth.access_token

    response = client.sessions.list(
        access_token=token,
        query=QuerySessionsList(
            session_type=SessionType.ONLINE,
            statuses=[SessionStatus.SUCCEEDED, SessionStatus.IN_PROGRESS],
        ),
    )

    assert isinstance(response, spec.SessionsQueryResponse)


# ---------------------------------------------------------------------------
# Session status & invoice status (requires an active/closed session)
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_get_session_status(session_with_invoice):
    """Get status of a session with at least one invoice."""
    _client, _token, _session_ref, _invoice_ref, session = session_with_invoice

    response = session.get_status()

    assert isinstance(response, spec.SessionStatusResponse)
    assert response.status is not None
    assert response.status.code is not None
    assert response.dateCreated is not None


@pytest.mark.integration
def test_list_session_invoices(session_with_invoice):
    """List invoices within a session."""
    _client, _token, _session_ref, _invoice_ref, session = session_with_invoice

    response = session.list_invoices(page_size=10)

    assert isinstance(response, spec.SessionInvoicesResponse)
    assert len(response.invoices) >= 1


@pytest.mark.integration
def test_get_session_invoice_status(session_with_invoice):
    """Get status of a specific invoice in a session."""
    _client, _token, _session_ref, invoice_ref, session = session_with_invoice

    response = session.get_invoice_status(invoice_ref)

    assert isinstance(response, spec.SessionInvoiceStatusResponse)
    assert response.referenceNumber == invoice_ref
    assert response.status is not None


@pytest.mark.integration
def test_list_failed_session_invoices(session_with_invoice):
    """List failed invoices within a session (may be empty)."""
    _client, _token, _session_ref, _invoice_ref, session = session_with_invoice

    response = session.list_failed_invoices(page_size=10)

    assert isinstance(response, spec.SessionInvoicesResponse)
    assert hasattr(response, "invoices")
