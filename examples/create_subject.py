from ksef2 import Client
from ksef2.config import Environment
from ksef2.domain.models import (
    SubjectType,
)

client = Client(environment=Environment.TEST)

PERSON_NIP = "7760257837"
PERSON_PESEL = "97091558747"
ORG_NIP = "3779539749"

with client.testdata.temporal() as td:
    # print("creating subject")
    td.create_subject(
        nip=ORG_NIP,
        subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
        description="Test subject",
    )
    print("creating person")
    td.create_person(nip=PERSON_NIP, pesel=PERSON_PESEL, description="Test person")
    # print("granting permissions")
    # td.grant_permissions(context=Identifier(type=IdentifierType.NIP, value=ORG_NIP), authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP), permissions=[Permission(type=PermissionType.INVOICE_READ, description="Read invoices")])
    # print("done")
