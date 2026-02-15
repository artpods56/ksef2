from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
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


def main() -> None:
    client = Client(environment=Environment.TEST)

    # Set up and authenticate
    print("Setting up and authenticating ...")
    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Limits modify test",
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
                    type=PermissionType.INVOICE_WRITE, description="Sending invoices"
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

        # Query context limits (session type limits)
        print("Querying context limits ...")
        context_limits = client.limits.get_context_limits(access_token=access_token)
        print("Online session:")
        print(f"Max invoices: {context_limits.online_session.max_invoices}")
        print(
            f"Max invoice size (MB): {context_limits.online_session.max_invoice_size_mb}"
        )
        print(
            f"Max with attachment (MB): {context_limits.online_session.max_invoice_with_attachment_size_mb}"
        )
        print("Batch session:")
        print(f"Max invoices: {context_limits.batch_session.max_invoices}")
        print(
            f"Max invoice size (MB): {context_limits.batch_session.max_invoice_size_mb}"
        )

        # Query subject limits (certificate/enrollment limits)
        print("Querying subject limits ...")
        subject_limits = client.limits.get_subject_limits(access_token=access_token)
        if subject_limits.certificate:
            print(f"Max certificates: {subject_limits.certificate.max_certificates}")
        if subject_limits.enrollment:
            print(f"Max enrollments:  {subject_limits.enrollment.max_enrollments}")

        # Query API rate limits
        print("Querying API rate limits ...")
        rate_limits = client.limits.get_api_rate_limits(access_token=access_token)
        print(
            f" Invoice send: {rate_limits.invoice_send.per_second}/s  {rate_limits.invoice_send.per_minute}/m  {rate_limits.invoice_send.per_hour}/h"
        )
        print(
            f"Online session: {rate_limits.online_session.per_second}/s  {rate_limits.online_session.per_minute}/m  {rate_limits.online_session.per_hour}/h"
        )
        print(
            f"Invoice download: {rate_limits.invoice_download.per_second}/s  {rate_limits.invoice_download.per_minute}/m  {rate_limits.invoice_download.per_hour}/h"
        )

        print("All limits queried successfully.")

    print("Test data cleaned up.")


if __name__ == "__main__":
    main()
