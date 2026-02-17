import random
import time
from datetime import date

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    IdentifierType,
    SubjectType,
    PermissionType,
    Identifier,
    Permission,
)
from ksef2.domain.models.session import QuerySessionsList, SessionType
from scripts.examples._common import repo_root

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

INVOICE_TEMPLATE_PATH = (
    repo_root() / "docs" / "assets" / "sample_invoices" / "invoice-template_v3.xml"
)

client = Client(environment=Environment.TEST)


def main():
    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="SDK test seller",
        )
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        temp.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
            authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
            permissions=[
                Permission(
                    type=PermissionType.INVOICE_WRITE,
                    description="Send invoices",
                ),
                Permission(
                    type=PermissionType.INTROSPECTION,
                    description="Introspect sessions",
                ),
                Permission(
                    type=PermissionType.ENFORCEMENT_OPERATIONS,
                    description="Manage enforcement operations",
                ),
            ],
        )

        cert, private_key = generate_test_certificate(ORG_NIP)

        auth = client.auth.authenticate_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )
        access_token = auth.access_token

        with client.sessions.open_online(
            access_token=access_token, form_code=FormSchema.FA3
        ) as session:
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

            if ksef_number := invoices_list.invoices[0].ksefNumber:
                print(f"Fetching UPO for {ksef_number} ...")
                upo = session.get_invoice_upo_by_ksef_number(ksef_number=ksef_number)
                print(f"UPO size: {len(upo)} bytes")

                print(f"Downloading invoice {ksef_number} ...")
                xml_bytes = session.download_invoice(ksef_number=ksef_number)
                print(f"Invoice size: {len(xml_bytes)} bytes")

            print("Listing online sessions:")
            print(
                client.sessions.list(
                    access_token=access_token,
                    query=QuerySessionsList(session_type=SessionType.ONLINE),
                )
            )


if __name__ == "__main__":
    main()
