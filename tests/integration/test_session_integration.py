from __future__ import annotations

import pytest

from ksef_sdk import KsefClient

from .conftest import SAMPLE_INVOICE_XML

pytestmark = pytest.mark.integration


class TestSession:
    @pytest.mark.usefixtures("setup_person")
    def test_send_invoice(self, ksef_client: KsefClient) -> None:
        """Open an online session and send a sample invoice."""
        with ksef_client.online_session() as session:
            resp = session.send_invoice(SAMPLE_INVOICE_XML)
            assert resp.referenceNumber
