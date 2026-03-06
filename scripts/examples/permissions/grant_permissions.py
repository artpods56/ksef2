from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.domain.models import EntityPermission, Identifier, Permission

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

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
                    type="credentials_manage",
                    description="Manage credentials",
                ),
            ],
            grant_to=Identifier(type="nip", value=PERSON_NIP),
            in_context_of=Identifier(type="nip", value=ORG_NIP),
        )

        # Authenticate - no session needed for permission operations
        auth = client.authentication.with_test_certificate(nip=ORG_NIP)

        print("Granting person permissions...")
        result = auth.permissions.grant_person(
            subject_type="pesel",
            subject_value=PERSON_PESEL,
            permissions=["invoice_read", "invoice_write"],
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
                    type="invoice_read",
                    can_delegate=True,
                ),
            ],
            description="Test entity permissions",
            entity_name="Test Entity",
        )
        print(f"Entity permissions granted: {result.reference_number}")


if __name__ == "__main__":
    main()
