"""End-to-end test harness for download_purchase_invoices.py (TEST environment).

Runs the complete purchase-invoice download workflow against Environment.TEST
without needing MCU certificates or pre-existing KSEF data:

  1. Setup  — create a seller and N buyer entities via the testdata API
  2. Send   — authenticate as the seller and send one invoice per buyer
              (each buyer is Subject2, so each invoice appears as a
               purchase invoice from the buyer's perspective)
  3. Wait   — poll until KSeF finishes processing
  4. Download — for each buyer: authenticate with their generated cert,
               open a session, schedule an export of Subject2 invoices,
               and fetch the resulting ZIP package

All test subjects are cleaned up automatically when the script exits
(via the temporal() context manager).

Run::

    uv run scripts/examples/invoices/download_purchase_invoices_test.py
"""

from __future__ import annotations

import time
from datetime import date, datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509 import Certificate

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    DateType,
    InvoiceQueryDateRange,
    InvoiceQueryFilters,
    InvoiceSubjectType,
)
from ksef2.domain.models.testdata import Identifier, IdentifierType, SubjectType
from scripts.examples._common import repo_root

# ── configuration ────────────────────────────────────────────────────────────

N_BUYERS = 3            # number of buyer entities to create
INVOICES_PER_BUYER = 2  # invoices the seller sends to each buyer

DOWNLOAD_DIR = repo_root() / "downloads" / "test"

INVOICE_TEMPLATE_PATH = (
    repo_root()
    / "docs"
    / "assets"
    / "sample_invoices"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)

# Seconds between export-status polls
POLL_INTERVAL = 3.0
MAX_POLL_ATTEMPTS = 60

# ─────────────────────────────────────────────────────────────────────────────


def send_invoices(
    client: Client,
    seller_nip: str,
    seller_cert: Certificate,
    seller_key: RSAPrivateKey,
    buyers: list[str],
) -> None:
    """Authenticate as seller and send INVOICES_PER_BUYER invoices to each buyer."""
    print(f"\n[seller {seller_nip}] Authenticating …")
    auth = client.auth.authenticate_xades(
        nip=seller_nip,
        cert=seller_cert,
        private_key=seller_key,
    )

    template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")

    with client.sessions.open_online(
        access_token=auth.access_token,
        form_code=FormSchema.FA3,
    ) as session:
        for buyer_nip in buyers:
            for i in range(INVOICES_PER_BUYER):
                invoice_xml = InvoiceFactory.create(
                    template_xml,
                    {
                        "#nip#": seller_nip,
                        "#subject2nip#": buyer_nip,
                        "#invoicing_date#": date.today().isoformat(),
                        "#invoice_number#": str(int(time.time() * 1000) + i),
                    },
                )
                result = session.send_invoice(invoice_xml=invoice_xml)
                print(
                    f"[seller] Sent invoice #{i + 1} to buyer {buyer_nip}"
                    f" → {result.reference_number}"
                )

    print("[seller] All invoices sent, waiting for KSeF to process …")
    time.sleep(8)


def download_for_buyer(
    client: Client,
    buyer_nip: str,
    buyer_cert: Certificate,
    buyer_key: RSAPrivateKey,
    target_dir: Path,
) -> None:
    """Authenticate as buyer and download all purchase invoices (Subject2)."""
    print(f"\n[buyer {buyer_nip}] Authenticating …")
    auth = client.auth.authenticate_xades(
        nip=buyer_nip,
        cert=buyer_cert,
        private_key=buyer_key,
    )

    target_dir.mkdir(parents=True, exist_ok=True)

    with client.sessions.open_online(
        access_token=auth.access_token,
        form_code=FormSchema.FA3,
    ) as session:
        print(f"[buyer {buyer_nip}] Scheduling export of purchase invoices …")
        export = session.schedule_invoices_export(
            filters=InvoiceQueryFilters(
                subject_type=InvoiceSubjectType.SUBJECT2,  # buyer perspective
                date_range=InvoiceQueryDateRange(
                    date_type=DateType.ISSUE,
                    from_=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    to=datetime.now(tz=timezone.utc),
                ),
            ),
        )

        package = None
        for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
            status = session.get_export_status(export.reference_number)
            if status.package:
                package = status.package
                break
            print(
                f"[buyer {buyer_nip}] Waiting for package …"
                f" ({attempt}/{MAX_POLL_ATTEMPTS})"
            )
            time.sleep(POLL_INTERVAL)

        if package is None:
            print(f"[buyer {buyer_nip}] Export timed out.")
            return

        paths = session.fetch_package(package=package, target_directory=target_dir)
        for path in paths:
            print(
                f"[buyer {buyer_nip}] Downloaded: {path.name}"
                f"  ({path.stat().st_size:,} bytes)"
            )


def main() -> None:
    client = Client(Environment.TEST)

    seller_nip = generate_nip()
    buyer_nips = [generate_nip() for _ in range(N_BUYERS)]

    print("=" * 60)
    print(f"Seller NIP : {seller_nip}")
    print(f"Buyer NIPs : {', '.join(buyer_nips)}")
    print("=" * 60)

    # Generate certs for all entities up front (before the temporal context
    # so we have them available throughout)
    seller_cert, seller_key = generate_test_certificate(seller_nip)
    buyer_certs: dict[str, tuple[Certificate, RSAPrivateKey]] = {
        nip: generate_test_certificate(nip) for nip in buyer_nips
    }

    with client.testdata.temporal() as temp:
        # Register all entities in the TEST environment
        temp.create_subject(
            nip=seller_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Test seller",
        )
        for buyer_nip in buyer_nips:
            temp.create_subject(
                nip=buyer_nip,
                subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
                description=f"Test buyer {buyer_nip}",
            )

        # Seller sends invoices to all buyers
        send_invoices(
            client=client,
            seller_nip=seller_nip,
            seller_cert=seller_cert,
            seller_key=seller_key,
            buyers=buyer_nips,
        )

        # Each buyer downloads their purchase invoices
        for buyer_nip in buyer_nips:
            buyer_cert, buyer_key = buyer_certs[buyer_nip]
            try:
                download_for_buyer(
                    client=client,
                    buyer_nip=buyer_nip,
                    buyer_cert=buyer_cert,
                    buyer_key=buyer_key,
                    target_dir=DOWNLOAD_DIR / buyer_nip,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"[buyer {buyer_nip}] ERROR: {exc}")

    print("\nDone. Test subjects cleaned up.")


if __name__ == "__main__":
    main()
