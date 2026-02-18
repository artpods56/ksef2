from __future__ import annotations

import time
from datetime import date

from ksef2 import Client, FormSchema, Environment
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import SubjectType
from scripts.examples._common import repo_root

ORG_NIP = generate_nip()

INVOICE_TEMPLATE_PATH = (
    repo_root()
    / "docs"
    / "assets"
    / "sample_invoices"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="SDK test seller",
        )
        cert, private_key = generate_test_certificate(ORG_NIP)

        auth = client.auth.authenticate_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )
        access_token = auth.access_token

        with client.sessions.open_online(
            access_token=access_token,
            form_code=FormSchema.FA3,
        ) as session:
            template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")
            result = session.send_invoice(
                invoice_xml=InvoiceFactory.create(
                    template_xml,
                    {
                        "#nip#": ORG_NIP,
                        "#subject2nip#": generate_nip(),
                        "#invoicing_date#": date.today().isoformat(),
                        "#invoice_number#": str(int(time.time())),
                    },
                )
            )

            print(f"Invoice has been sent, reference number: {result.reference_number}")

            # KSeF assigns a ksefNumber after processing — wait briefly then fetch it
            time.sleep(5)
            status = session.get_invoice_status(result.reference_number)

            if status.ksefNumber:
                downloaded_invoice = session.download_invoice(
                    ksef_number=status.ksefNumber
                )
                print(f"Downloaded invoice of size {len(downloaded_invoice)} bytes")


if __name__ == "__main__":
    main()
