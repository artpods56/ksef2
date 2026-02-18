"""End-to-end tests that execute the example scripts against Environment.TEST.

Each test imports and calls the main() function of a self-contained example.
No pre-configured credentials are required — examples provision their own test
subjects via the testdata API and clean up automatically via temporal().

Skipped examples (require external config not available in CI):
  - auth/auth_xades_demo.py    — needs MCU certificate files
  - invoices/download_purchase_invoices.py — needs MCU certificate files
  - auth/auth_token.py         — needs KSEF_TEST_KSEF_TOKEN env var (skipped if absent)
"""

from __future__ import annotations

import pytest

import scripts.examples.auth.auth_refresh as auth_refresh_example
import scripts.examples.auth.auth_token as auth_token_example
import scripts.examples.auth.auth_xades as auth_xades_example
import scripts.examples.auth.token_management as token_management_example
import scripts.examples.invoices.download_purchase_invoices_test as download_example
import scripts.examples.invoices.send_invoice as send_invoice_example
import scripts.examples.invoices.send_query_export_download as send_example
import scripts.examples.limits.limits_modify as limits_modify_example
import scripts.examples.limits.limits_query as limits_query_example
import scripts.examples.permissions.grant_permissions as grant_permissions_example
import scripts.examples.permissions.query_permissions as query_permissions_example
import scripts.examples.quickstart as quickstart_example
import scripts.examples.session.session_management as session_management_example
import scripts.examples.session.session_resume as session_resume_example
import scripts.examples.session.workflow as workflow_example
import scripts.examples.testdata.attachments as attachments_example
import scripts.examples.testdata.block_context as block_context_example
import scripts.examples.testdata.setup_test_data as setup_test_data_example

# ── auth ──────────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_example_auth_xades() -> None:
    """XAdES authentication with a self-signed certificate.

    Covers: challenge → sign → submit → poll → redeem tokens.
    """
    auth_xades_example.main()


@pytest.mark.integration
def test_example_auth_refresh() -> None:
    """Token refresh after initial XAdES authentication.

    Covers: XAdES auth → list sessions → refresh access token.
    """
    auth_refresh_example.main()


@pytest.mark.integration
@pytest.mark.skip(
    reason=(
        "Token auth requires a short KSeF token (<190 bytes for RSA-OAEP/2048). "
        "JWTs from the TEST environment exceed this limit. "
        "See auth/auth_token.py for manual usage with a short token."
    )
)
def test_example_auth_token() -> None:
    """Token-based authentication using a pre-generated KSeF token."""
    auth_token_example.main()


@pytest.mark.integration
def test_example_token_management() -> None:
    """KSeF token lifecycle: generate, check status, revoke.

    Covers: testdata setup → XAdES auth → generate token →
    check status → revoke → verify revocation → cleanup.
    """
    token_management_example.main()


# ── session ───────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_example_session_management() -> None:
    """Authentication session listing and termination.

    Covers: XAdES auth → list active sessions → terminate current session.
    """
    session_management_example.main()


@pytest.mark.integration
def test_example_session_resume() -> None:
    """Session state serialization and resume from saved state.

    Covers: testdata setup → open session (manual) → serialize state →
    restore state → resume session → terminate.
    """
    session_resume_example.main()


@pytest.mark.integration
def test_example_session_workflow() -> None:
    """Full online session workflow including invoice operations.

    Covers: testdata setup → XAdES auth → open session → list invoices →
    send invoice → list failed invoices → get UPO → download invoice →
    list sessions.
    """
    workflow_example.main()


# ── invoices ──────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_example_quickstart() -> None:
    """Quickstart: authenticate and send an invoice (context manager + manual).

    Covers: XAdES auth → open session via context manager → send invoice →
    open session manually → send invoice → terminate.
    """
    quickstart_example.main()


@pytest.mark.integration
def test_example_send_invoice() -> None:
    """Send a single invoice and immediately download it by KSeF number.

    Covers: testdata setup → XAdES auth → open session → send invoice →
    download invoice XML → cleanup.
    """
    send_invoice_example.main()


@pytest.mark.integration
def test_example_send_query_export_download() -> None:
    """Full invoice lifecycle: send, query status, schedule export, download.

    Covers: testdata setup → XAdES auth → open session → send invoice →
    poll status → schedule export → fetch package → cleanup.
    """
    send_example.main()


@pytest.mark.integration
def test_example_download_purchase_invoices() -> None:
    """Purchase invoice download across multiple buyer entities.

    Covers: create seller + N buyers → send invoices as Subject2 →
    authenticate as each buyer → export Subject2 invoices → fetch packages.
    """
    download_example.main()


# ── limits ────────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_example_limits_query() -> None:
    """Query all API limit types from an authenticated client.

    Covers: testdata setup → XAdES auth → get context limits →
    get subject limits → get API rate limits → cleanup.
    """
    limits_query_example.main()


@pytest.mark.integration
def test_example_limits_modify() -> None:
    """Modify and reset API limits (TEST environment only).

    Covers: testdata setup → XAdES auth → modify session/subject/rate limits →
    reset each to defaults → set production rate limits → cleanup.
    """
    limits_modify_example.main()


# ── permissions ───────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_example_grant_permissions() -> None:
    """Grant permissions to a person and an entity.

    Covers: testdata setup → XAdES auth → grant person permissions →
    grant entity permissions → cleanup.
    """
    grant_permissions_example.main()


@pytest.mark.integration
def test_example_query_permissions() -> None:
    """Query all permission types after granting them.

    Covers: testdata setup → XAdES auth → grant permissions → query persons /
    authorizations / personal / EU entities / subordinate entities /
    subunits → cleanup.
    """
    query_permissions_example.main()


# ── testdata ──────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_example_testdata_setup_automatic() -> None:
    """Testdata setup with automatic cleanup via temporal() context manager."""
    setup_test_data_example.with_automatic_cleanup()


@pytest.mark.integration
def test_example_testdata_setup_manual() -> None:
    """Testdata setup with manual create/revoke/delete lifecycle."""
    setup_test_data_example.manual_cleanup()


@pytest.mark.integration
def test_example_block_context() -> None:
    """Block and unblock an authentication context.

    Covers: create subject → block context → unblock context → cleanup.
    """
    block_context_example.main()


@pytest.mark.integration
def test_example_attachments() -> None:
    """Enable and revoke invoice attachment permissions.

    Covers: create subject → enable attachments → revoke immediately →
    re-enable → revoke with future end date → cleanup.
    """
    attachments_example.main()
