"""Enable and revoke attachment permissions on TEST.

Demonstrates how to enable and revoke attachment sending permissions for a subject.

Usage:
    uv run python scripts/examples/testdata/attachments.py
"""

from datetime import date, timedelta

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip

ORG_NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        # Create a test subject
        print(f"Creating test subject with NIP: {ORG_NIP}")
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="Attachments test",
        )

        # Enable attachments for the subject
        print(f"Enabling attachments for NIP: {ORG_NIP}")
        client.testdata.enable_attachments(nip=ORG_NIP)
        print("  Attachments enabled")

        # At this point, the subject can send invoices with attachments

        # Revoke attachments (immediate)
        print(f"Revoking attachments for NIP: {ORG_NIP}")
        client.testdata.revoke_attachments(nip=ORG_NIP)
        print("  Attachments revoked immediately")

        # Re-enable for the next example
        print("Re-enabling attachments ...")
        client.testdata.enable_attachments(nip=ORG_NIP)

        # Revoke attachments with expected end date
        future_date = date.today() + timedelta(days=30)
        print(f"Revoking attachments with end date: {future_date}")
        client.testdata.revoke_attachments(
            nip=ORG_NIP,
            expected_end_date=future_date,
        )
        print(f"  Attachments will be revoked on {future_date}")

    print("Test data cleaned up.")


if __name__ == "__main__":
    main()
