"""
Send an invoice, wait for processing, export matching invoices, and download the package.

Run:
    uv run scripts/examples/invoices/send_query_export_download.py
"""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.domain.models import InvoicesFilter

NIP = generate_nip()
ROOT = next(
    path
    for path in Path(__file__).resolve().parents
    if (path / "pyproject.toml").exists()
)

INVOICE_TEMPLATE_PATH = (
    ROOT / "docs" / "assets" / "sample_invoices" / "fa3" / "invoice-template_v3.xml"
)

DOWNLOAD_DIR = ROOT / "downloads" / "invoice_export"


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=NIP,
            subject_type="enforcement_authority",
            description="README lifecycle example",
        )

        auth = client.authentication.with_test_certificate(nip=NIP)

        template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
        invoice_xml = InvoiceFactory.create(
            template_xml,
            {
                "#nip#": NIP,
                "#invoicing_date#": date.today().isoformat(),
                # Demo-only identifier. Use your own business numbering in production.
                "#invoice_number#": f"DEMO-{datetime.now(tz=timezone.utc):%Y%m%d%H%M%S}",
            },
        )

        with auth.online_session(form_code=FormSchema.FA3) as session:
            result = session.send_invoice(invoice_xml=invoice_xml)
            print(f"Invoice sent: {result.reference_number}")

            status = session.wait_for_invoice_ready(
                invoice_reference_number=result.reference_number,
                timeout=60.0,
                poll_interval=2.0,
            )
            print(f"Invoice processed as KSeF number: {status.ksef_number}")

        export = auth.invoices.schedule_export(
            filters=InvoicesFilter(
                role="seller",
                date_type="issue_date",
                date_from=datetime.now(tz=timezone.utc) - timedelta(days=1),
                date_to=datetime.now(tz=timezone.utc),
                amount_type="brutto",
            )
        )
        print(f"Export scheduled: {export.reference_number}")

        package = auth.invoices.wait_for_export_package(
            reference_number=export.reference_number,
            timeout=120.0,
            poll_interval=2.0,
        )
        print(f"Export package ready with {len(package.parts)} part(s)")

        for path in auth.invoices.fetch_package(
            package=package,
            export=export,
            target_directory=DOWNLOAD_DIR,
        ):
            print(f"Downloaded: {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
