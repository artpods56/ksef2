from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)
from ksef2.domain.models.tokens import TokenPermission

NIP = generate_nip()


def main() -> None:

    client = Client(environment=Environment.TEST)

    # Set up: create subject with CREDENTIALS_MANAGE permission
    print("Setting up test data ...")
    with client.testdata.temporal() as td:
        td.create_subject(
            nip=NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Token management test",
        )
        td.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value=NIP),
            authorized=Identifier(type=IdentifierType.NIP, value=NIP),
            permissions=[
                Permission(
                    type=PermissionType.INVOICE_WRITE, description="Sending invoices"
                ),
                Permission(
                    type=PermissionType.CREDENTIALS_MANAGE, description="Manage creds"
                ),
            ],
        )

        # Authenticate
        print("Authenticating ...")
        cert, private_key = generate_test_certificate(NIP)
        tokens = client.auth.authenticate_xades(
            nip=NIP,
            cert=cert,
            private_key=private_key,
        )
        access_token = tokens.access_token.token

        # Generate a new KSeF token
        print("Generating KSeF token ...")
        result = client.tokens.generate(
            access_token=access_token,
            permissions=[
                TokenPermission.INVOICE_READ,
                TokenPermission.INVOICE_WRITE,
            ],
            description="Example API token",
        )
        print(f"  Token:     {result.token[:40]}...")
        print(f"  Reference: {result.reference_number}")

        # Check token status
        print("Checking token status ...")
        status = client.tokens.status(
            access_token=access_token,
            reference_number=result.reference_number,
        )
        print(f"  Status: {status.status.value}")

        # Revoke the token
        print("Revoking token ...")
        client.tokens.revoke(
            access_token=access_token,
            reference_number=result.reference_number,
        )

        # Verify it's revoked
        print("Verifying revocation ...")
        status = client.tokens.status(
            access_token=access_token,
            reference_number=result.reference_number,
        )
        print(f"  Status: {status.status.value}")

    print("Done, test data cleaned up.")


if __name__ == "__main__":
    main()
