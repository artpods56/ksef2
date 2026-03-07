"""Send a TEST invoice, download it as the buyer, and render the results to PDF.

Prerequisites:
- none; the script provisions and cleans up its own TEST-environment data

What it demonstrates:
- sending an invoice between TEST subjects
- buyer-side export and download
- rendering exported invoices to PDF
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceTemplater
from ksef2.core.packages import PackageReader
from ksef2.core.tools import generate_nip
from ksef2.domain.models import InvoicesFilter
from ksef2.services.renderers import InvoicePDFExporter
from scripts.examples._common import repo_root


@dataclass
class ExampleConfig:
    environment: Environment = Environment.TEST
    template_path: Path = field(
        default_factory=lambda: (
            repo_root()
            / "docs"
            / "assets"
            / "sample_invoices"
            / "fa3"
            / "invoice-template-fa-3-with-custom-subject_2.xml"
        )
    )
    downloads_dir: Path = field(
        default_factory=lambda: repo_root() / "downloads" / "pdf_export"
    )


def send_invoice(
    client: Client,
    template_path: Path,
    seller_nip: str,
    buyer_nip: str,
) -> None:
    seller_auth = client.authentication.with_test_certificate(nip=seller_nip)
    template_xml = template_path.read_text(encoding="utf-8")

    with seller_auth.online_session(form_code=FormSchema.FA3) as session:
        # we generate valid invoice from the template because we need the nips to match
        invoice_xml = InvoiceTemplater.create(
            template_xml=template_xml,
            replacements={
                "#nip#": seller_nip,
                "#subject2nip#": buyer_nip,
                "#invoicing_date#": datetime.now(tz=timezone.utc).date().isoformat(),
                "#invoice_number#": str(int(time.time() * 1000)),
            },
        )
        result = session.send_invoice(invoice_xml=invoice_xml)
        print(f"Invoice sent: {result.reference_number}")


def download_and_export(
    client: Client,
    downloads_directory: Path,
    buyer_nip: str,
) -> None:
    buyer_auth = client.authentication.with_test_certificate(nip=buyer_nip)
    query_filters = InvoicesFilter(
        role="buyer",
        date_type="issue_date",
        date_from=datetime.now(tz=timezone.utc) - timedelta(days=1),
        date_to=datetime.now(tz=timezone.utc),
        amount_type="brutto",
    )

    print("Waiting for invoice to appear in KSeF...")
    metadata = buyer_auth.invoices.wait_for_invoices(filters=query_filters)
    print(f"Found {len(metadata.invoices)} invoice(s). Exporting...")

    zip_parts = buyer_auth.invoices.export_and_download(filters=query_filters)

    downloads_directory.mkdir(parents=True, exist_ok=True)
    exporter = InvoicePDFExporter()

    for invoice in PackageReader(zip_parts):
        pdf_bytes = exporter.export_from_string(invoice_xml=invoice.xml)
        pdf_path = downloads_directory / f"{Path(invoice.name).stem}.pdf"
        _ = pdf_path.write_bytes(pdf_bytes)
        print(f"Saved: {pdf_path}")


def run(config: ExampleConfig) -> None:
    client = Client(environment=config.environment)
    seller_nip = generate_nip()
    buyer_nip = generate_nip()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=seller_nip,
            subject_type="enforcement_authority",
            description="Scenario seller",
        )
        temp.create_subject(
            nip=buyer_nip,
            subject_type="enforcement_authority",
            description="Scenario buyer",
        )

        send_invoice(client, config.template_path, seller_nip, buyer_nip)
        download_and_export(client, config.downloads_dir, buyer_nip)

    print("Done.")


def main() -> int:
    run(ExampleConfig())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
