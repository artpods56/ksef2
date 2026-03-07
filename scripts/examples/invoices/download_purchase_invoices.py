"""Download purchase invoices (faktury zakupowe) for multiple entities.

Intended for accounting firms or shared-service centres managing several
companies.  For each NIP the script authenticates with the certificate
downloaded from MCU, schedules an export of all purchase invoices in the
requested date range, and saves the resulting ZIP packages to disk.

Directory layout expected for certificates (files downloaded from KSEF/MCU)::

    certs/
        1111111111.pem   # certificate — <NIP>.pem
        1111111111.key   # private key  — <NIP>.key
        2222222222.pem
        2222222222.key
        ...

Usage::

    python download_purchase_invoices.py

Edit the constants below to match your setup.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from ksef2 import Client, Environment
from ksef2.core import exceptions
from ksef2.core.xades import load_certificate_from_pem, load_private_key_from_pem
from ksef2.domain.models import InvoicesFilter

# ── configuration ────────────────────────────────────────────────────────────

ENVIRONMENT = Environment.PRODUCTION  # or Environment.DEMO

# List of NIPs to process.  Matching <NIP>.pem / <NIP>.key must exist in CERT_DIR.
NIPS = [
    "1111111111",
    "2222222222",
    # ... add all 25 here
]

CERT_DIR = Path("certs")  # directory with .pem / .key files from MCU/KSEF
DOWNLOAD_DIR = Path("downloads")  # invoices will be saved here, one sub-dir per NIP

# Date range for purchase invoices to download.
# KSeF enforces a maximum window of 3 months per export request.
# For longer periods run the script multiple times with adjusted dates.
DATE_TO = datetime.now(tz=timezone.utc)
DATE_FROM = DATE_TO - timedelta(days=90)

# Polling configuration for the SDK export wait helper
POLL_INTERVAL = 3.0
MAX_POLL_ATTEMPTS = 60

# ─────────────────────────────────────────────────────────────────────────────


def download_for_nip(client: Client, nip: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"[{nip}] Authenticating …")

    cert = load_certificate_from_pem(CERT_DIR / f"{nip}.pem")
    key = load_private_key_from_pem(CERT_DIR / f"{nip}.key")

    auth = client.authentication.with_xades(
        nip=nip,
        cert=cert,
        private_key=key,
        verify_chain=False,
    )

    target_dir = DOWNLOAD_DIR / nip
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{nip}] Scheduling export of purchase invoices …")
    export = auth.invoices.schedule_export(
        filters=InvoicesFilter(
            role="buyer",
            date_type="issue_date",
            date_from=DATE_FROM,
            date_to=DATE_TO,
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
        print(f"[{nip}] Export timed out — try increasing MAX_POLL_ATTEMPTS.")
        return

    paths = auth.invoices.fetch_package(
        package=package,
        export=export,
        target_directory=target_dir,
    )
    for path in paths:
        print(f"[{nip}] Downloaded: {path}  ({path.stat().st_size:,} bytes)")

    print(f"[{nip}] Done.")


def main() -> None:
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    client = Client(ENVIRONMENT)

    for nip in NIPS:
        try:
            download_for_nip(client, nip)
        except Exception as exc:  # noqa: BLE001
            print(f"[{nip}] ERROR: {exc}")

    print("\nAll done.")


if __name__ == "__main__":
    main()
