"""
Send, query, export, and download invoices — full invoice lifecycle.

This example demonstrates the complete invoice workflow in KSeF:

1. **Setup** — create test subjects and grant permissions
2. **Authenticate** — obtain an access token via XAdES
3. **Send** — upload an invoice from a template
4. **Query status** — check processing status by reference number
5. **Export** — schedule a bulk export filtered by date range and subject type
6. **Download** — poll export status and fetch the resulting ZIP package

Run:
    uv run scripts/examples/invoices/send_query_export_download.py
"""

from __future__ import annotations

import time
from datetime import date, datetime, timezone

from ksef2 import Client, FormSchema, Environment
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    InvoiceQueryFilters,
    InvoiceSubjectType,
    InvoiceQueryDateRange,
    DateType,
)
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
    repo_root()
    / "docs"
    / "assets"
    / "sample_invoices"
    / "invoice-template-fa-3-with-custom-subject_2.xml"
)

DOWNLOAD_DIR = repo_root() / "downloads"


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
                Permission(
                    type=PermissionType.INVOICE_READ,
                    description="Read invoices",
                ),
            ],
        )

        cert, private_key = generate_test_certificate(ORG_NIP)

        tokens = client.auth.authenticate_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )
        access_token = tokens.access_token.token

        with client.sessions.open_online(
            access_token=access_token,
            form_code=FormSchema.FA3,
        ) as session:
            template_xml = INVOICE_TEMPLATE_PATH.read_text(encoding="utf-8")

            # building and sending sample invoice
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

            # let them process the invoice
            time.sleep(5)

            print(
                session.get_invoice_status(result.reference_number).model_dump_json(
                    indent=2
                )
            )

            # lets get all invoiced that were issued in the last year
            export = session.schedule_invoices_export(
                filters=InvoiceQueryFilters(
                    subject_type=InvoiceSubjectType.SUBJECT1,  # Subject 1  is a seller
                    date_range=InvoiceQueryDateRange(
                        date_type=DateType.ISSUE,
                        from_=datetime(2026, 1, 1, tzinfo=timezone.utc),
                        to=datetime.now(tz=timezone.utc),
                    ),
                ),
            )

            print(export.model_dump_json(indent=2))

            exported_invoices = session.get_export_status(
                reference_number=export.reference_number
            )

            print(exported_invoices.model_dump_json(indent=2))

            if package := exported_invoices.package:
                for path in session.fetch_package(
                    package=package, target_directory=DOWNLOAD_DIR
                ):
                    print(
                        f"Downloaded invoice of size {len(path.read_bytes())} bytes into {path}"
                    )


if __name__ == "__main__":
    main()
