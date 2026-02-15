from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core import exceptions
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()

client = Client(environment=Environment.TEST)


def with_automatic_cleanup():
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
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Example organization",
        )

        print("Creating test person ...")
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        # trying to create the same person again will result in an exception that gets suppressed by the context manager
        # calling create_person() method outside of the context manager will result in an exception that has to be handled manually
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        print("Granting permissions ...")
        temp.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
            authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
            permissions=[
                Permission(
                    type=PermissionType.INVOICE_READ, description="Read invoices"
                ),
                Permission(
                    type=PermissionType.INVOICE_WRITE, description="Send invoices"
                ),
            ],
        )

        print("Cleanup has been performed automatically.")


def manual_cleanup():
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
        subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
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
        context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
        authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
        permissions=[
            Permission(type=PermissionType.INVOICE_READ, description="Read invoices"),
            Permission(type=PermissionType.INVOICE_WRITE, description="Send invoices"),
        ],
    )

    print("Cleaning up ...")

    print("Revoking permissions ...")
    client.testdata.revoke_permissions(
        context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
        authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
    )

    print("Deleting test person ...")
    client.testdata.delete_person(nip=PERSON_NIP)

    print("Deleting test subject ...")
    client.testdata.delete_subject(nip=ORG_NIP)


if __name__ == "__main__":
    # this method uses automatic cleanup and it's the preferred way to set up test data'
    with_automatic_cleanup()

    print("\n")

    # this method shows how to setup and clean up test data manually
    manual_cleanup()
