from __future__ import annotations

from ksef2 import Client, FormSchema, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)

from scripts.examples._common import repo_root

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

INVOICE_TEMPLATE_PATH = (
    repo_root() / "docs" / "assets" / "sample_invoices" / "invoice-template-fa-3-with-custom-subject_2.xml"
)


def main() -> None:
    
    client = Client(environment=Environment.TEST)

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
            ],
        )

        cert, private_key = generate_test_certificate(PERSON_NIP)

        tokens = client.auth.authenticate_xades(
            nip=PERSON_NIP,
            cert=cert,
            private_key=private_key,
        )
        access_token = tokens.access_token.token

        with client.sessions.open_online(
            access_token=access_token,
            form_code=FormSchema.FA3,
        ) as session:
            with open(INVOICE_TEMPLATE_PATH, "rb") as f:
                result = session.send_invoice(f.read())

                print(
                    f"Invoice has been sent, reference number: {result.reference_number}"
                )

            downloaded_invoice = session.download_invoice(
                ksef_number=result.reference_number
            )
            print(f"Downloaded invoice of size {len(downloaded_invoice)} bytes")


if __name__ == "__main__":
    main()
