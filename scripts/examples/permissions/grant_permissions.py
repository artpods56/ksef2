from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    IdentifierType,
    SubjectType,
    PermissionType,
    Identifier,
    Permission,
    EntityPermission,
    EntityPermissionType,
)

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

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
            permissions=[
                Permission(
                    type=PermissionType.CREDENTIALS_MANAGE,
                    description="Manage credentials",
                ),
            ],
            grant_to=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
            in_context_of=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
        )

        cert, private_key = generate_test_certificate(ORG_NIP)

        # Authenticate - no session needed for permission operations
        auth = client.authentication.with_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )

        print("Granting person permissions...")
        result = auth.permissions.grant_person(
            subject_identifier=IdentifierType.PESEL,
            subject_value=PERSON_PESEL,
            permissions=[PermissionType.INVOICE_READ, PermissionType.INVOICE_WRITE],
            description="Test person permissions",
            first_name="John",
            last_name="Doe",
        )
        print(f"Person permissions granted: {result.reference_number}")

        print("Granting entity permissions...")
        result = auth.permissions.grant_entity(
            subject_value=ORG_NIP,
            permissions=[
                EntityPermission(
                    type=EntityPermissionType.INVOICE_READ,
                    can_delegate=True,
                ),
            ],
            description="Test entity permissions",
            entity_name="Test Entity",
        )
        print(f"Entity permissions granted: {result.reference_number}")


if __name__ == "__main__":
    main()
