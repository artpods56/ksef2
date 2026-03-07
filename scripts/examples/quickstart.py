"""Send a minimal invoice in the TEST environment.

Prerequisites:
- none; the script uses a generated TEST certificate identity

What it demonstrates:
- authenticating in TEST
- opening an online session
- sending an invoice with both context-manager and manual session handling
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
        / "invoice-template_v3.xml"
    )


def run(config: ExampleConfig) -> None:
    client = Client(config.environment)
    valid_nip = generate_nip()
    template_xml = config.template_path.read_text(encoding="utf-8")

    auth = client.authentication.with_test_certificate(nip=valid_nip)
    invoice_xml = InvoiceTemplater.create(
        template_xml,
        {
            "#nip#": valid_nip,
            "#invoicing_date#": date.today().isoformat(),
            "#invoice_number#": f"DEMO-{date.today():%Y%m%d}-{valid_nip[-4:]}",
        },
    )

    with auth.online_session(form_code=FormSchema.FA3) as session:
        result = session.send_invoice(invoice_xml=invoice_xml)
        print(result.reference_number)

    session = auth.online_session(form_code=FormSchema.FA3)
    try:
        result = session.send_invoice(invoice_xml=invoice_xml)
        print(result.reference_number)
    finally:
        session.close()


def main() -> int:
    run(ExampleConfig())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
