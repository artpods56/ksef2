"""Query API limits using authenticated client.

Demonstrates querying:
  - Context limits (session type limits)
  - Subject limits (certificate/enrollment limits)
  - API rate limits

Usage:
    uv run python scripts/examples/limits/limits_query.py
"""

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

    # Set up test data
    print("Setting up test data ...")
    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Limits query test",
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

        cert, private_key = generate_test_certificate(ORG_NIP)

        # Authenticate and get an AuthenticatedClient
        print("Authenticating ...")
        auth = client.auth.authenticate_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )

        # Query limits directly from authenticated client (no session needed!)
        print("\nContext limits (session type):")
        context_limits = auth.limits.get_context_limits()
        print("  Online session:")
        print(f"    Max invoices: {context_limits.online_session.max_invoices}")
        print(
            f"    Max invoice size (MB): "
            f"{context_limits.online_session.max_invoice_size_mb}"
        )
        print(
            f"    Max with attachment (MB): "
            f"{context_limits.online_session.max_invoice_with_attachment_size_mb}"
        )
        print("  Batch session:")
        print(f"    Max invoices: {context_limits.batch_session.max_invoices}")
        print(
            f"    Max invoice size (MB): "
            f"{context_limits.batch_session.max_invoice_size_mb}"
        )

        # Query subject limits (certificate/enrollment limits)
        print("\nSubject limits (certificate/enrollment):")
        subject_limits = auth.limits.get_subject_limits()
        if subject_limits.certificate:
            print(f"  Max certificates: {subject_limits.certificate.max_certificates}")
        if subject_limits.enrollment:
            print(f"  Max enrollments:  {subject_limits.enrollment.max_enrollments}")

        # Query API rate limits
        print("\nAPI rate limits:")
        rate_limits = auth.limits.get_api_rate_limits()
        inv = rate_limits.invoice_send
        print(
            f"  Invoice send: {inv.per_second}/s  {inv.per_minute}/m  {inv.per_hour}/h"
        )
        sess = rate_limits.online_session
        print(
            f"  Online session: {sess.per_second}/s  {sess.per_minute}/m  {sess.per_hour}/h"
        )
        dl = rate_limits.invoice_download
        print(
            f"  Invoice download: {dl.per_second}/s  {dl.per_minute}/m  {dl.per_hour}/h"
        )

        print("\nAll limits queried successfully.")

    print("Test data cleaned up.")


if __name__ == "__main__":
    main()
