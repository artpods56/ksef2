import time
from datetime import datetime, timezone, timedelta, date

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceFactory
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    InvoiceQueryFilters,
    InvoiceSubjectType,
    SubjectType,
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    InvoiceQueryDateRange,
    DateType,
)
from ksef2.domain.models.session import SessionType

BUYER_NIP = generate_nip()
BUYER_PESEL = generate_pesel()
ORG_NIP = generate_nip()

org_cert, org_key = generate_test_certificate(ORG_NIP)
client = Client(environment=Environment.TEST)

auth = client.authentication.with_xades(nip=ORG_NIP, cert=org_cert, private_key=org_key)

invoice_url = "/Users/user/PycharmProjects/KSEF_SDK/docs/assets/sample_invoices/fa3/invoice-template_v3.xml"

with client.testdata.temporal() as temp:
    temp.create_subject(
        nip=ORG_NIP,
        subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
        description="SDK test seller",
    )
    temp.create_person(
        nip=BUYER_NIP,
        pesel=BUYER_PESEL,
        description="SDK test buyer",
    )

    temp.grant_permissions(
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
        grant_to=Identifier(type=IdentifierType.NIP, value=BUYER_NIP),
        in_context_of=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
    )

    with auth.online_session(form_code=FormSchema.FA3) as session:
        with open(invoice_url, "rb") as f:
            response = session.send_invoice(
                invoice_xml=InvoiceFactory.create(
                    template_xml=f.read(),
                    replacements={
                        "#nip#": ORG_NIP,
                        "#subject2nip#": BUYER_NIP,
                        "#invoicing_date#": date.today().isoformat(),
                        "#invoice_number#": str(int(time.time())),
                    },
                )
            )

        time.sleep(5)

        print(
            session.get_invoice_status(
                invoice_reference_number=response.reference_number
            ).model_dump_json(indent=2)
        )

        datetime_now = datetime.now(timezone.utc)

        datetime_delta = datetime_now - timedelta(days=1)

        query_result = session.wait_for_invoices(
            filters=InvoiceQueryFilters(
                date_range=InvoiceQueryDateRange(
                    date_type=DateType.ISSUE, from_=datetime_delta, to=datetime_now
                ),
                subject_type=InvoiceSubjectType.SELLER,
            )
        )

        print(query_result.model_dump_json(indent=2))

        print(session.get_status().model_dump_json(indent=2))

        for session in auth.session_log.list(
            session_type=SessionType.ONLINE,
        ):
            print(session.model_dump_json(indent=2))

        auth.sessions.list_page()
