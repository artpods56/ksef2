"""End-to-end test harness for download_purchase_invoices.py (TEST environment).

Runs the complete purchase-invoice download workflow against Environment.TEST
without needing MCU certificates or pre-existing KSEF data:

  1. Setup  — create a seller and N buyer entities via the testdata API
  2. Send   — authenticate as the seller and send one invoice per buyer
              (each buyer is Subject2, so each invoice appears as a
               purchase invoice from the buyer'request perspective)
  3. Wait   — poll until KSeF finishes processing
  4. Download — for each buyer: authenticate with their generated cert,
               open a session, schedule an export of Subject2 invoices,
               and fetch the resulting ZIP package

All test subjects are cleaned up automatically when the script exits
(via the temporal() context manager).

Run::

    uv run scripts/examples/invoices/download_purchase_invoices_test.py
"""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core import exceptions
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.domain.models import InvoicesFilter

# ── configuration ────────────────────────────────────────────────────────────

N_BUYERS = 3  # number of buyer entities to create
INVOICES_PER_BUYER = 2  # invoices the seller sends to each buyer

ROOT = next(
    path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
)

DOWNLOAD_DIR = ROOT / "downloads" / "test"

INVOICE_TEMPLATE_PATH = (
    ROOT
    / "docs"
    / "assets"
    / "sample_invoices"
    / "fa3"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)

# Seconds between export-status polls
POLL_INTERVAL = 3.0
MAX_POLL_ATTEMPTS = 60

# ─────────────────────────────────────────────────────────────────────────────


def send_invoices(
    client: Client,
    seller_nip: str,
    buyers: list[str],
) -> None:
    """Authenticate as seller and send INVOICES_PER_BUYER invoices to each buyer."""
    print(f"\n[seller {seller_nip}] Authenticating …")
    auth = client.authentication.with_test_certificate(nip=seller_nip)

    template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")

    with auth.online_session(form_code=FormSchema.FA3) as session:
        for buyer_nip in buyers:
            for i in range(INVOICES_PER_BUYER):
                status = session.send_invoice_and_wait(
                    invoice_xml=InvoiceFactory.create(
                        template_xml,
                        {
                            "#nip#": seller_nip,
                            "#subject2nip#": buyer_nip,
                            "#invoicing_date#": date.today().isoformat(),
                            "#invoice_number#": (
                                f"DEMO-{date.today():%Y%m%d}-{buyer_nip[-4:]}-{i + 1}"
                            ),
                        },
                    ),
                    timeout=60.0,
                    poll_interval=2.0,
                )
                print(
                    f"[seller] Sent invoice #{i + 1} to buyer {buyer_nip} → {status.reference_number}"
                )
    print("[seller] All invoices sent and processed.")


def download_for_buyer(
    client: Client,
    buyer_nip: str,
    target_dir: Path,
) -> None:
    """Authenticate as buyer and download all purchase invoices (Subject2)."""
    print(f"\n[buyer {buyer_nip}] Authenticating …")
    auth = client.authentication.with_test_certificate(nip=buyer_nip)

    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"[buyer {buyer_nip}] Scheduling export of purchase invoices …")
    export = auth.invoices.schedule_export(
        filters=InvoicesFilter(
            role="buyer",
            date_type="issue_date",
            date_from=datetime.now(tz=timezone.utc) - timedelta(days=90),
            date_to=datetime.now(tz=timezone.utc),
            amount_type="brutto",
        )
    )

    try:
        package = auth.invoices.wait_for_export_package(
            reference_number=export.reference_number,
            timeout=POLL_INTERVAL * MAX_POLL_ATTEMPTS,
            poll_interval=POLL_INTERVAL,
        )
    except exceptions.KSeFExportTimeoutError:
        print(f"[buyer {buyer_nip}] Export timed out.")
        return

    paths = auth.invoices.fetch_package(
        package=package,
        export=export,
        target_directory=target_dir,
    )
    for path in paths:
        print(
            f"[buyer {buyer_nip}] Downloaded: {path.name}  ({path.stat().st_size:,} bytes)"
        )


def main() -> None:
    client = Client(Environment.TEST)

    seller_nip = generate_nip()
    buyer_nips = [generate_nip() for _ in range(N_BUYERS)]

    print("=" * 60)
    print(f"Seller NIP : {seller_nip}")
    print(f"Buyer NIPs : {', '.join(buyer_nips)}")
    print("=" * 60)

    with client.testdata.temporal() as temp:
        # Register all entities in the TEST environment
        temp.create_subject(
            nip=seller_nip,
            subject_type="enforcement_authority",
            description="Test seller",
        )
        for buyer_nip in buyer_nips:
            temp.create_subject(
                nip=buyer_nip,
                subject_type="enforcement_authority",
                description=f"Test buyer {buyer_nip}",
            )

        # Seller sends invoices to all buyers
        send_invoices(
            client=client,
            seller_nip=seller_nip,
            buyers=buyer_nips,
        )

        # Each buyer downloads their purchase invoices
        for buyer_nip in buyer_nips:
            try:
                download_for_buyer(
                    client=client,
                    buyer_nip=buyer_nip,
                    target_dir=DOWNLOAD_DIR / buyer_nip,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"[buyer {buyer_nip}] ERROR: {exc}")

    print("\nDone. Test subjects cleaned up.")


if __name__ == "__main__":
    main()
