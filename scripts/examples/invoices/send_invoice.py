"""Send one invoice in TEST, wait for processing, and download it back.

Prerequisites:
- none; the script provisions and cleans up its own TEST-environment data

What it demonstrates:
- test subject provisioning
- invoice submission in an online session
- waiting for processing and downloading by KSeF number
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceTemplater
from ksef2.core.tools import generate_nip
from scripts.examples._common import repo_root


@dataclass
class ExampleConfig:
    environment: Environment = Environment.TEST
    template_path: Path = (
        repo_root()
        / "docs"
        / "assets"
        / "sample_invoices"
        / "fa3"
        / "invoice-template-fa-3-with-custom-subject_2.xml"
    )


def run(config: ExampleConfig) -> None:
    client = Client(environment=config.environment)
    seller_nip = generate_nip()
    buyer_nip = generate_nip()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=seller_nip,
            subject_type="enforcement_authority",
            description="SDK test seller",
        )

        auth = client.authentication.with_test_certificate(nip=seller_nip)
        template_xml = config.template_path.read_text(encoding="utf-8")

        with auth.online_session(form_code=FormSchema.FA3) as session:
            result = session.send_invoice(
                invoice_xml=InvoiceTemplater.create(
                    template_xml,
                    {
                        "#nip#": seller_nip,
                        "#subject2nip#": buyer_nip,
                        "#invoicing_date#": date.today().isoformat(),
                        "#invoice_number#": f"DEMO-{date.today():%Y%m%d}-{buyer_nip[-4:]}",
                    },
                )
            )

            print(f"Invoice has been sent, reference number: {result.reference_number}")

            status = session.wait_for_invoice_ready(
                invoice_reference_number=result.reference_number
            )

            if status.ksef_number:
                downloaded_invoice = auth.invoices.download_invoice(
                    ksef_number=status.ksef_number
                )
                print(f"Downloaded invoice of size {len(downloaded_invoice)} bytes")


def main() -> int:
    run(ExampleConfig())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
