import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.packages import PackageReader
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.domain.models import InvoicesFilter
from ksef2.services.renderers import InvoicePDFExporter


def generate_test_subject() -> str:
    return generate_nip()


def send_invoice(
    client: Client,
    template_path: Path,
    seller_nip: str,
    buyer_nip: str,
) -> None:
    seller_auth = client.authentication.with_test_certificate(nip=seller_nip)

    with seller_auth.online_session(form_code=FormSchema.FA3) as session:
        invoice_xml = InvoiceFactory.create(
            template_xml=template_path.read_text(encoding="utf-8"),
            replacements={
                "#nip#": seller_nip,
                "#subject2nip#": buyer_nip,
                "#invoicing_date#": date.today().isoformat(),
                "#invoice_number#": str(int(time.time() * 1000)),
            },
        )
        result = session.send_invoice(invoice_xml=invoice_xml)
        print(f"Invoice sent: {result.reference_number}")


def download_and_export(
    client: Client,
    downloads_dir: Path,
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

    downloads_dir.mkdir(parents=True, exist_ok=True)
    exporter = InvoicePDFExporter()

    for invoice in PackageReader(zip_parts):
        pdf_bytes = exporter.export_from_string(invoice_xml=invoice.xml)
        pdf_path = downloads_dir / f"{Path(invoice.name).stem}.pdf"
        _ = pdf_path.write_bytes(pdf_bytes)
        print(f"Saved: {pdf_path}")


def main(template_path: Path, downloads_dir: Path) -> None:

    client = Client(environment=Environment.TEST)
    seller_nip = generate_test_subject()
    buyer_nip = generate_test_subject()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=seller_nip,
            subject_type="enforcement_authority",
            description="Test seller",
        )
        temp.create_subject(
            nip=buyer_nip,
            subject_type="enforcement_authority",
            description="Test buyer",
        )

        send_invoice(client, template_path, seller_nip, buyer_nip)
        download_and_export(client, downloads_dir, buyer_nip)

    print("Done.")


if __name__ == "__main__":
    # this is meant to be run from the root of the project
    # modify the paths accordingly if you're running it from somewhere else

    ROOT = Path(__file__).parents[3]
    DOWNLOAD_DIR = ROOT / "downloads" / "pdf_export"

    INVOICE_TEMPLATE_PATH = (
        ROOT
        / "docs"
        / "assets"
        / "sample_invoices"
        / "fa3"
        / "invoice-template-fa-3-with-custom-subject_2.xml"
    )

    main(
        template_path=INVOICE_TEMPLATE_PATH,
        downloads_dir=DOWNLOAD_DIR,
    )
