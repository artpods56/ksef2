"""End-to-end tests that execute the example scripts against Environment.TEST.

Each test imports and calls the main() function of a self-contained example.
No pre-configured credentials are required — examples provision their own test
subjects via the testdata API and clean up automatically via temporal().
"""

from __future__ import annotations

import pytest

import scripts.examples.auth.auth_xades as auth_xades_example
import scripts.examples.invoices.download_purchase_invoices_test as download_example
import scripts.examples.invoices.send_query_export_download as send_example


@pytest.mark.integration
def test_example_auth_xades() -> None:
    """XAdES authentication with a self-signed certificate.

    Covers: challenge → sign → submit → poll → redeem tokens.
    """
    auth_xades_example.main()


@pytest.mark.integration
def test_example_send_query_export_download() -> None:
    """Full invoice lifecycle: create subject, send invoice, export, download.

    Covers: testdata setup → XAdES auth → open session → send invoice →
    poll status → schedule export → fetch package → cleanup.
    """
    send_example.main()


@pytest.mark.integration
def test_example_download_purchase_invoices() -> None:
    """Purchase invoice download across multiple buyer entities.

    Covers: create seller + N buyers → send invoices (Subject2) →
    authenticate as each buyer → export Subject2 invoices → fetch packages.
    """
    download_example.main()
