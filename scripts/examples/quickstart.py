import time
from datetime import date

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from scripts.examples._common import repo_root

VALID_NIP = generate_nip()

INVOICE_TEMPLATE_PATH = (
    repo_root()
    / "docs"
    / "assets"
    / "sample_invoices"
    / "fa3"
    / "invoice-template_v3.xml"
)


def main() -> None:
    client = Client(Environment.TEST)

    cert, private_key = generate_test_certificate(VALID_NIP)
    auth = client.authentication.with_xades(
        nip=VALID_NIP,
        cert=cert,
        private_key=private_key,
    )

    template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
    invoice_xml = InvoiceFactory.create(
        template_xml,
        {
            "#nip#": VALID_NIP,
            "#invoicing_date#": date.today().isoformat(),
            "#invoice_number#": str(int(time.time())),
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
