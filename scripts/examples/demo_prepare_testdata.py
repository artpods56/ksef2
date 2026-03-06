"""Prepare test data for demonstrating the export_invoices CLI.

Sets up temporary subjects on the KSeF TEST environment, sends a sample
invoice, writes buyer credentials to disk, and prints the exact CLI command
to run.  The script stays alive until you press Enter — test data is cleaned
up on exit.

Run::

    uv run scripts/examples/demo_prepare_testdata.py

Then, in another terminal, copy-paste the printed CLI command.
"""

import time
from datetime import date
from pathlib import Path

from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import Identifier, Permission

ROOT = next(
    path
    for path in Path(__file__).resolve().parents
    if (path / "pyproject.toml").exists()
)
INVOICE_TEMPLATE_PATH = (
    ROOT
    / "docs"
    / "assets"
    / "sample_invoices"
    / "fa3"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)

CREDS_DIR = ROOT / ".demo_creds"


def main() -> None:
    seller_nip = generate_nip()
    buyer_nip = generate_nip()
    buyer_pesel = generate_pesel()

    buyer_cert, buyer_key = generate_test_certificate(buyer_nip)

    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        # --- Create subjects ---
        print("Setting up test data on KSeF TEST ...\n")

        temp.create_subject(
            nip=seller_nip,
            subject_type="enforcement_authority",
            description="Demo seller",
        )
        temp.create_subject(
            nip=buyer_nip,
            subject_type="enforcement_authority",
            description="Demo buyer",
        )
        temp.create_person(
            nip=buyer_nip,
            pesel=buyer_pesel,
            description="Demo buyer person",
        )

        # --- Grant permissions ---
        for nip in (seller_nip, buyer_nip):
            temp.grant_permissions(
                permissions=[
                    Permission(type="invoice_write", description="Write invoices"),
                    Permission(type="invoice_read", description="Read invoices"),
                ],
                grant_to=Identifier(type="nip", value=nip),
                in_context_of=Identifier(type="nip", value=nip),
            )

        # --- Send a sample invoice ---
        print("Sending a sample invoice as the seller ...")
        seller_auth = client.authentication.with_test_certificate(nip=seller_nip)

        template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
        invoice_xml = InvoiceFactory.create(
            template_xml,
            {
                "#nip#": seller_nip,
                "#subject2nip#": buyer_nip,
                "#invoicing_date#": date.today().isoformat(),
                "#invoice_number#": str(int(time.time() * 1000)),
            },
        )

        with seller_auth.online_session(form_code=FormSchema.FA3) as session:
            status = session.send_invoice_and_wait(
                invoice_xml=invoice_xml,
                timeout=60.0,
                poll_interval=2.0,
            )

        print(f"Invoice sent and processed (ref: {status.reference_number})")

        # --- Write buyer credentials to disk ---
        CREDS_DIR.mkdir(parents=True, exist_ok=True)

        cert_path = CREDS_DIR / "buyer_cert.pem"
        key_path = CREDS_DIR / "buyer_key.pem"

        cert_path.write_bytes(buyer_cert.public_bytes(Encoding.PEM))
        key_path.write_bytes(
            buyer_key.private_bytes(
                Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()
            )
        )

        # --- Print summary ---
        print("\n" + "=" * 60)
        print("  TEST DATA READY")
        print("=" * 60)
        print(f"  Seller NIP:    {seller_nip}")
        print(f"  Buyer NIP:     {buyer_nip}")
        print(f"  Buyer PESEL:   {buyer_pesel}")
        print(f"  Buyer cert:    {cert_path}")
        print(f"  Buyer key:     {key_path}")
        print(f"  Invoice ref:   {status.reference_number}")
        print("=" * 60)
        print("\nRun this in another terminal:\n")
        print(
            f"  uv run scripts/cli/export_invoices.py \\\n"
            f"    --nip {buyer_nip} \\\n"
            f"    --cert {cert_path} \\\n"
            f"    --key {key_path} \\\n"
            f"    --days 1 \\\n"
            f"    --env test"
        )
        print()

        input("Press Enter to clean up test data and exit ...")

    # Cleanup: remove credential files
    for f in (cert_path, key_path):
        f.unlink(missing_ok=True)
    if CREDS_DIR.exists() and not any(CREDS_DIR.iterdir()):
        CREDS_DIR.rmdir()

    print("Test data cleaned up. Done.")


if __name__ == "__main__":
    main()
