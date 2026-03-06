from datetime import date
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip

VALID_NIP = generate_nip()
ROOT = next(
    path for path in Path(__file__).resolve().parents if (path / "pyproject.toml").exists()
)

INVOICE_TEMPLATE_PATH = (
    ROOT
    / "docs"
    / "assets"
    / "sample_invoices"
    / "fa3"
    / "invoice-template_v3.xml"
)


def main() -> None:
    client = Client(Environment.TEST)

    auth = client.authentication.with_test_certificate(nip=VALID_NIP)

    template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
    invoice_xml = InvoiceFactory.create(
        template_xml,
        {
            "#nip#": VALID_NIP,
            "#invoicing_date#": date.today().isoformat(),
            "#invoice_number#": f"DEMO-{date.today():%Y%m%d}-{VALID_NIP[-4:]}",
        },
    )

    # Sessions are context managers and will automatically terminate on exit
    with auth.online_session(form_code=FormSchema.FA3) as session:
        result = session.send_invoice(invoice_xml=invoice_xml)
        print(result.reference_number)

    # Sessions also support manual management:
    session = auth.online_session(form_code=FormSchema.FA3)
    try:
        result = session.send_invoice(invoice_xml=invoice_xml)
        print(result.reference_number)
    finally:
        session.close()


if __name__ == "__main__":
    main()
