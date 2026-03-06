from datetime import date
from pathlib import Path

from ksef2 import Client, FormSchema, Environment
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip

ORG_NIP = generate_nip()
ROOT = next(
    path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
)

INVOICE_TEMPLATE_PATH = (
    ROOT
    / "docs"
    / "assets"
    / "sample_invoices"
    / "fa3"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="SDK test seller",
        )
        auth = client.authentication.with_test_certificate(nip=ORG_NIP)
        with auth.online_session(form_code=FormSchema.FA3) as session:
            template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
            result = session.send_invoice(
                invoice_xml=InvoiceFactory.create(
                    template_xml,
                    {
                        "#nip#": ORG_NIP,
                        "#subject2nip#": generate_nip(),
                        "#invoicing_date#": date.today().isoformat(),
                        "#invoice_number#": f"DEMO-{date.today():%Y%m%d}-{generate_nip()[-4:]}",
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


if __name__ == "__main__":
    main()
