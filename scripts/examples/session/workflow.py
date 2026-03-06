import random
import time
from datetime import date

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import Identifier, Permission
from scripts.examples._common import repo_root

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

INVOICE_TEMPLATE_PATH = (
    repo_root()
    / "docs"
    / "assets"
    / "sample_invoices"
    / "fa3"
    / "invoice-template_v3.xml"
)

client = Client(environment=Environment.TEST)


def main() -> None:
    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="SDK test seller",
        )
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        temp.grant_permissions(
            permissions=[
                Permission(
                    type="invoice_write",
                    description="Send invoices",
                ),
                Permission(
                    type="introspection",
                    description="Introspect sessions",
                ),
                Permission(
                    type="enforcement_operations",
                    description="Manage enforcement operations",
                ),
            ],
            grant_to=Identifier(type="nip", value=PERSON_NIP),
            in_context_of=Identifier(type="nip", value=ORG_NIP),
        )

        cert, private_key = generate_test_certificate(ORG_NIP)

        auth = client.authentication.with_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )
        with auth.online_session(form_code=FormSchema.FA3) as session:
            print(session.get_state().model_dump_json(indent=2))

            print("Session status:")
            print(session.get_status())

            print("Invoices before sending:")
            print(session.list_invoices().model_dump_json(indent=2))

            template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
            invoice_xml = InvoiceFactory.create(
                template_xml,
                {
                    "#nip#": ORG_NIP,
                    "#invoicing_date#": date.today().isoformat(),
                    "#invoice_number#": str(random.randint(1, 1000)),
                },
            )
            invoice_ref = session.send_invoice(invoice_xml=invoice_xml)
            print(f"Invoice sent: {invoice_ref.model_dump_json(indent=2)}")

            # give them some time to process the invoice
            time.sleep(5)

            print("Failed invoices:")
            print(session.list_failed_invoices())

            print("Invoices after sending:")
            invoices_list = session.list_invoices()
            print(invoices_list.model_dump_json(indent=2))

            if ksef_number := invoices_list.invoices[0].ksef_number:
                print(f"Fetching UPO for {ksef_number} ...")
                upo = session.get_invoice_upo_by_ksef_number(ksef_number=ksef_number)
                print(f"UPO size: {len(upo)} bytes")

                print(f"Downloading invoice {ksef_number} ...")
                xml_bytes = auth.invoices.download_invoice(ksef_number=ksef_number)
                print(f"Invoice size: {len(xml_bytes)} bytes")

            print("Listing online sessions:")
            print(
                auth.session_log.query(
                    session_type="online",
                )
            )


if __name__ == "__main__":
    main()
