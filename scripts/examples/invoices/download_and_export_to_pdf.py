from __future__ import annotations

import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from ksef2.domain.models import (
    DateType,
    InvoiceQueryDateRange,
    InvoiceQueryFilters,
    InvoiceSubjectType,
)
from ksef2.domain.models.testdata import SubjectType
from ksef2.services.renderers import InvoicePDFExporter
from ksef2.utils import PackageReader


def generate_test_subject() -> tuple[str, Certificate, RSAPrivateKey]:
    nip = generate_nip()
    cert, key = generate_test_certificate(nip)
    return nip, cert, key


def send_invoice(
    client: Client,
    template_path: Path,
    seller_nip: str,
    buyer_nip: str,
    seller_cert: Certificate,
    seller_key: RSAPrivateKey,
) -> None:
    seller_auth = client.authentication.with_xades(
        nip=seller_nip,
        cert=seller_cert,
        private_key=seller_key,
    )

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
    buyer_cert: Certificate,
    buyer_key: RSAPrivateKey,
) -> None:
    buyer_auth = client.authentication.with_xades(
        nip=buyer_nip,
        cert=buyer_cert,
        private_key=buyer_key,
    )

    query_filters = InvoiceQueryFilters(
        subject_type=InvoiceSubjectType.BUYER,
        date_range=InvoiceQueryDateRange(
            date_type=DateType.ISSUE,
            from_=datetime.now(tz=timezone.utc) - timedelta(days=1),
            to=datetime.now(tz=timezone.utc),
        ),
    )

    with buyer_auth.online_session(form_code=FormSchema.FA3) as session:
        print("Waiting for invoice to appear in KSeF...")
        metadata = session.wait_for_invoices(filters=query_filters)
        print(f"Found {len(metadata.invoices)} invoice(s). Exporting...")

        zip_parts = session.export_and_download(filters=query_filters)

        downloads_dir.mkdir(parents=True, exist_ok=True)
        exporter = InvoicePDFExporter()

        for invoice in PackageReader(zip_parts):
            pdf_bytes = exporter.export_from_string(invoice_xml=invoice.xml)
            pdf_path = downloads_dir / f"{Path(invoice.name).stem}.pdf"
            _ = pdf_path.write_bytes(pdf_bytes)
            print(f"Saved: {pdf_path}")


def main(template_path: Path, downloads_dir: Path) -> None:

    client = Client(environment=Environment.TEST)
    seller_nip, seller_cert, seller_key = generate_test_subject()
    buyer_nip, buyer_cert, buyer_key = generate_test_subject()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=seller_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Test seller",
        )
        temp.create_subject(
            nip=buyer_nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Test buyer",
        )

        send_invoice(
            client, template_path, seller_nip, buyer_nip, seller_cert, seller_key
        )
        download_and_export(client, downloads_dir, buyer_nip, buyer_cert, buyer_key)

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
        / "invoice-template-fa-3-with-custom-subject_2.xml"
    )

    main(
        template_path=INVOICE_TEMPLATE_PATH,
        downloads_dir=DOWNLOAD_DIR,
    )
