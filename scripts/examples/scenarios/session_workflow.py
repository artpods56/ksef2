"""Exercise a full online-session workflow, from setup through invoice history queries.

Prerequisites:
- none; the script provisions and cleans up its own TEST-environment data

What it demonstrates:
- temporary test subjects and permissions
- online session state and status inspection
- sending and downloading an invoice
- querying historical session logs
"""

import random
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceTemplater
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.domain.models import Identifier, Permission
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
    client = Client(environment=config.environment)
    organization_nip = generate_nip()
    person_nip = generate_nip()
    person_pesel = generate_pesel()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=organization_nip,
            subject_type="enforcement_authority",
            description="Scenario seller",
        )
        temp.create_person(
            nip=person_nip,
            pesel=person_pesel,
            description="Scenario person",
        )
        temp.grant_permissions(
            permissions=[
                Permission(type="invoice_write", description="Send invoices"),
                Permission(type="introspection", description="Inspect sessions"),
                Permission(
                    type="enforcement_operations",
                    description="Manage enforcement operations",
                ),
            ],
            grant_to=Identifier(type="nip", value=person_nip),
            in_context_of=Identifier(type="nip", value=organization_nip),
        )

        auth = client.authentication.with_test_certificate(nip=organization_nip)
        template_xml = config.template_path.read_text(encoding="utf-8")

        with auth.online_session(form_code=FormSchema.FA3) as session:
            print("Session state:")
            print(session.get_state().model_dump_json(indent=2))

            print("Session status:")
            print(session.get_status())

            print("Invoices before sending:")
            print(session.list_invoices().model_dump_json(indent=2))

            invoice_xml = InvoiceTemplater.create(
                template_xml,
                {
                    "#nip#": organization_nip,
                    "#invoicing_date#": date.today().isoformat(),
                    "#invoice_number#": str(random.randint(1, 1000)),
                },
            )

            invoice_ref = session.send_invoice(invoice_xml=invoice_xml)
            print(f"Invoice sent: {invoice_ref.model_dump_json(indent=2)}")

            status = session.wait_for_invoice_ready(
                invoice_reference_number=invoice_ref.reference_number
            )
            print(f"Invoice processed as KSeF number: {status.ksef_number}")

            print("Failed invoices:")
            print(session.list_failed_invoices())

            print("Invoices after sending:")
            print(session.list_invoices().model_dump_json(indent=2))

            if status.ksef_number:
                print(f"Fetching UPO for {status.ksef_number}...")
                upo = session.get_invoice_upo_by_ksef_number(
                    ksef_number=status.ksef_number
                )
                print(f"UPO size: {len(upo)} bytes")

                print(f"Downloading invoice {status.ksef_number}...")
                xml_bytes = auth.invoices.download_invoice(
                    ksef_number=status.ksef_number
                )
                print(f"Invoice size: {len(xml_bytes)} bytes")

        print("Listing online sessions:")
        print(auth.session_log.query(session_type="online"))


def main() -> int:
    run(ExampleConfig())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
