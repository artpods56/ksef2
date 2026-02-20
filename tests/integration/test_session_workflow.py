"""Integration tests for the online session workflow.

Covers: sessions.open_online (context manager), send_invoice, download_invoice,
get_status, list_invoices, list_failed_invoices, get_invoice_upo_by_ksef_number,
get_invoice_upo_by_reference, get_state, sessions.resume.

Run with:
    uv run pytest tests/integration/test_session_workflow.py -v -m integration
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from ksef2 import Client, FormSchema, Environment
from ksef2.clients.session import OnlineSessionClient
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.session import OnlineSessionState
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
    / "fa3"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)


@pytest.fixture(scope="module")
def workflow_context():
    """Full workflow: testdata → auth → open session → send invoice.

    Yields a dict with all context needed by individual tests.
    The session stays open for the duration of the module.
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
            description="Workflow test seller",
        )
        temp.create_subject(
            nip=buyer_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Workflow test buyer",
        )
        temp.create_person(
            nip=person_nip,
            pesel=person_pesel,
            description="Workflow test person",
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
                    "#invoicing_date#": "2026-02-16",
                    "#invoice_number#": str(int(time.time())),
                },
            )
            result = session.send_invoice(invoice_xml=invoice_xml)

            # Give KSeF time to process the invoice
            time.sleep(5)

            invoices_list = session.list_invoices()

            yield {
                "client": client,
                "access_token": access_token,
                "session": session,
                "invoice_ref": result.reference_number,
                "invoices_list": invoices_list,
            }


# ---------------------------------------------------------------------------
# get_state
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_get_state_returns_session_state(workflow_context):
    """get_state returns a SessionState with all required fields."""
    session: OnlineSessionClient = workflow_context["session"]

    state = session.get_state()

    assert isinstance(state, OnlineSessionState)
    assert state.reference_number
    assert state.access_token
    assert state.aes_key
    assert state.iv
    assert state.valid_until is not None
    assert state.form_code == FormSchema.FA3


# ---------------------------------------------------------------------------
# download_invoice
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_download_invoice_returns_xml_bytes(workflow_context):
    """download_invoice returns non-empty XML bytes."""
    session: OnlineSessionClient = workflow_context["session"]
    invoices_list = workflow_context["invoices_list"]

    if not invoices_list.invoices or not invoices_list.invoices[0].ksefNumber:
        pytest.skip("No processed invoice with ksefNumber available")

    ksef_number = invoices_list.invoices[0].ksefNumber
    xml_bytes = session.download_invoice(ksef_number=ksef_number)

    assert isinstance(xml_bytes, bytes)
    assert len(xml_bytes) > 0


# ---------------------------------------------------------------------------
# get_invoice_upo_by_ksef_number
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_get_invoice_upo_by_ksef_number(workflow_context):
    """UPO by KSeF number returns non-empty bytes."""
    session: OnlineSessionClient = workflow_context["session"]
    invoices_list = workflow_context["invoices_list"]

    if not invoices_list.invoices or not invoices_list.invoices[0].ksefNumber:
        pytest.skip("No processed invoice with ksefNumber available")

    ksef_number = invoices_list.invoices[0].ksefNumber
    upo = session.get_invoice_upo_by_ksef_number(ksef_number=ksef_number)

    assert isinstance(upo, bytes)
    assert len(upo) > 0


# ---------------------------------------------------------------------------
# get_invoice_upo_by_reference
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_get_invoice_upo_by_reference(workflow_context):
    """UPO by invoice reference number returns non-empty bytes."""
    session: OnlineSessionClient = workflow_context["session"]
    invoice_ref = workflow_context["invoice_ref"]

    upo = session.get_invoice_upo_by_reference(invoice_reference_number=invoice_ref)

    assert isinstance(upo, bytes)
    assert len(upo) > 0


# ---------------------------------------------------------------------------
# sessions.resume
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_resume_session_from_state(workflow_context):
    """Resume a session from serialized state and use it."""
    client: Client = workflow_context["client"]
    session: OnlineSessionClient = workflow_context["session"]

    state = session.get_state()

    # Round-trip through JSON serialization
    state_json = state.model_dump_json()
    restored_state = OnlineSessionState.model_validate_json(state_json)

    resumed = client.sessions.resume(state=restored_state)

    assert isinstance(resumed, OnlineSessionClient)

    # The resumed session should be able to query status
    status = resumed.get_status()
    assert isinstance(status, spec.SessionStatusResponse)
    assert status.status is not None


# ---------------------------------------------------------------------------
# GetSessionUpoEndpoint - collective UPO for session
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.skip(
    reason="Session UPO requires completed session with UPO reference number"
)
def test_get_session_upo_by_reference(workflow_context):
    """Test getting collective UPO for a session by UPO reference number.

    Note: This test is skipped because:
    1. The session UPO is only available after the session is closed
    2. We need a valid upoReferenceNumber from the session status
    3. The workflow_context keeps the session open for other tests

    The endpoint (GET /sessions/{referenceNumber}/upo/{upoReferenceNumber})
    returns the collective UPO XML for the entire session, which is different
    from the per-invoice UPO endpoints.
    """
    _ = workflow_context  # noqa: F841 - context used in real implementation

    # In a real scenario, you would:
    # 1. Close the session
    # 2. Get the session status which includes upoReferenceNumber
    # 3. Call GetSessionUpoEndpoint with both reference numbers

    # This is the endpoint structure (not actually callable in this test):
    # endpoint = GetSessionUpoEndpoint(client._transport)
    # upo_xml = endpoint.send(
    #     access_token=workflow_context["access_token"],
    #     reference_number=session.reference_number,
    #     upo_reference_number="<upo-ref-from-session-status>",
    # )
    pass
