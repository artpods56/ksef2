from ksef2 import Client, Environment
from ksef2.core import exceptions
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.domain.models.testdata import Identifier, Permission

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

client = Client(environment=Environment.TEST)


def with_automatic_cleanup() -> None:
    """Set up test data with automatic cleanup.

    The creation and deletion of entities is handled automatically by the context manager.
    As long they are used within the managed context, they will be deleted when the context exits.
    This is helpful for integration tests and scripts where you want guaranteed cleanup.
    """

    print("Creating test data with automatic cleanup:")

    with client.testdata.temporal() as temp:
        print("Creating test subject ...")
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="Example organization",
        )

        print("Creating test person ...")
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        # Duplicate creates still raise errors. The temporal() context only guarantees
        # cleanup for resources already registered in the managed scope.
        try:
            temp.create_person(
                nip=PERSON_NIP,
                pesel=PERSON_PESEL,
                description="Example person",
            )
        except exceptions.KSeFApiError:
            print("Person already exists: cleanup will still run on exit.")

        print("Granting permissions ...")
        temp.grant_permissions(
            permissions=[
                Permission(type="invoice_read", description="Read invoices"),
                Permission(type="invoice_write", description="Send invoices"),
            ],
            grant_to=Identifier(type="nip", value=PERSON_NIP),
            in_context_of=Identifier(type="nip", value=ORG_NIP),
        )

        print("Cleanup has been performed automatically.")


def manual_cleanup() -> None:
    """Manually set up and clean up test data.

    This method shows how to set up and clean up test data manually.
    User is responsible for creating and deleting entities.
    Errors have to be handled manually.

    WARNING: If any step fails before cleanup, the remaining cleanup steps
    will never execute, leaving orphaned entities in the API. This is why
    the temporal() context manager approach is preferred.
    """

    print("Creating test data with manual cleanup:")

    print("Creating test subject ...")
    client.testdata.create_subject(
        nip=ORG_NIP,
        subject_type="enforcement_authority",
        description="Example organization",
    )

    print("Creating test person ...")
    client.testdata.create_person(
        nip=PERSON_NIP,
        pesel=PERSON_PESEL,
        description="Example person",
    )

    print("Trying to create already existing person ...")
    try:
        client.testdata.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )
    except exceptions.KSeFApiError:
        print("Person already exists: ...")

    print("Granting permissions ...")
    client.testdata.grant_permissions(
        permissions=[
            Permission(type="invoice_read", description="Read invoices"),
            Permission(type="invoice_write", description="Send invoices"),
        ],
        grant_to=Identifier(type="nip", value=PERSON_NIP),
        in_context_of=Identifier(type="nip", value=ORG_NIP),
    )

    print("Cleaning up ...")

    print("Revoking permissions ...")
    client.testdata.revoke_permissions(
        revoke_from=Identifier(type="nip", value=PERSON_NIP),
        in_context_of=Identifier(type="nip", value=ORG_NIP),
    )

    print("Deleting test person ...")
    client.testdata.delete_person(nip=PERSON_NIP)

    print("Deleting test subject ...")
    client.testdata.delete_subject(nip=ORG_NIP)


if __name__ == "__main__":
    # This method uses automatic cleanup and is the preferred way to set up test data.
    with_automatic_cleanup()

    print("\n")

    # this method shows how to setup and clean up test data manually
    manual_cleanup()
