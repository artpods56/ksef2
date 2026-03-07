"""Prepare TEST data for demo purposes.

Prerequisites:
- run from the repository checkout so the sample invoice path resolves
"""

import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceTemplater
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from scripts.examples._common import repo_root


@dataclass
class ExampleConfig:
    environment: Environment = Environment.TEST
    creds_dir: Path = repo_root() / ".demo_creds"
    template_path: Path = (
        repo_root()
        / "docs"
        / "assets"
        / "sample_invoices"
        / "fa3"
        / "invoice-template-fa-3-with-custom-subject_2.xml"
    )


def run(config: ExampleConfig) -> None:
    seller_nip = generate_nip()
    buyer_nip = generate_nip()
    buyer_cert, buyer_key = generate_test_certificate(buyer_nip)
    client = Client(environment=config.environment)

    with client.testdata.temporal() as temp:
        print("Setting up test data on KSeF TEST...\n")

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

        print("Sending a sample invoice as the seller...")
        seller_auth = client.authentication.with_test_certificate(nip=seller_nip)

        template_xml = config.template_path.read_text(encoding="utf-8")
        invoice_xml = InvoiceTemplater.create(
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

        config.creds_dir.mkdir(parents=True, exist_ok=True)
        cert_path = config.creds_dir / "buyer_cert.pem"
        key_path = config.creds_dir / "buyer_key.pem"

        _ = cert_path.write_bytes(buyer_cert.public_bytes(Encoding.PEM))
        _ = key_path.write_bytes(
            buyer_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.TraditionalOpenSSL,
                NoEncryption(),
            )
        )

        print("  TEST DATA READY")
        print(f"  Seller NIP:    {seller_nip}")
        print(f"  Buyer NIP:     {buyer_nip}")
        print(f"  Buyer cert:    {cert_path}")
        print(f"  Buyer key:     {key_path}")
        print(f"  Invoice ref:   {status.reference_number}")

        _ = input("Press Enter to clean up test data and exit...")

    for path in (cert_path, key_path):
        path.unlink(missing_ok=True)
    if config.creds_dir.exists() and not any(config.creds_dir.iterdir()):
        config.creds_dir.rmdir()

    print("Test data cleaned up. Done.")


def main() -> int:
    run(ExampleConfig())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
