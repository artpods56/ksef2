"""Modify and reset API limits on TEST.

The TEST environment allows modifying limits for testing purposes.
The recommended workflow: fetch current limits, modify, push back.

Demonstrates:
  - Modifying session limits
  - Modifying subject limits
  - Modifying API rate limits
  - Setting production rate limits
  - Resetting limits to defaults

Usage:
    uv run python scripts/examples/limits/limits_modify.py
"""

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.domain.models.testdata import Identifier, Permission

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
            subject_type="enforcement_authority",
            description="Limits modify test",
        )

        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        temp.grant_permissions(
            permissions=[
                Permission(type="invoice_write", description="Sending invoices"),
            ],
            grant_to=Identifier(type="nip", value=PERSON_NIP),
            in_context_of=Identifier(type="nip", value=ORG_NIP),
        )

        # Authenticate and get an AuthenticatedClient
        print("Authenticating ...")
        auth = client.authentication.with_test_certificate(nip=ORG_NIP)

        # --- Modify session limits ---
        print("\nModifying session limits ...")
        limits = auth.limits.get_context_limits()
        original_max = limits.online_session.max_invoices
        limits.online_session.max_invoices = 5000
        auth.limits.set_session_limits(limits=limits)
        print(f"  max_invoices: {original_max} -> 5000")

        # Reset session limits back to defaults
        print("  Resetting session limits ...")
        auth.limits.reset_session_limits()

        # --- Modify subject limits ---
        print("\nModifying subject limits ...")
        subject_limits = auth.limits.get_subject_limits()
        if subject_limits.certificate:
            subject_limits.certificate.max_certificates = 10
            auth.limits.set_subject_limits(limits=subject_limits)
            print("  max_certificates -> 10")

        # Reset subject limits back to defaults
        print("  Resetting subject limits ...")
        auth.limits.reset_subject_limits()

        # --- Modify API rate limits ---
        print("\nModifying API rate limits ...")
        rate_limits = auth.limits.get_api_rate_limits()
        rate_limits.invoice_send.per_second = 50
        rate_limits.invoice_send.per_minute = 200
        auth.limits.set_api_rate_limits(limits=rate_limits)
        print("  invoice_send: 50/request, 200/m")

        # Reset rate limits back to defaults
        print("  Resetting API rate limits ...")
        auth.limits.reset_api_rate_limits()

        # --- Set production rate limits ---
        print("\nSetting production rate limits ...")
        auth.limits.set_production_rate_limits()
        print("  Rate limits set to production values")

        # Check the new limits
        prod_limits = auth.limits.get_api_rate_limits()
        inv = prod_limits.invoice_send
        print(
            f"  invoice_send: {inv.per_second}/request, {inv.per_minute}/m, {inv.per_hour}/h"
        )

        # Reset back to test defaults
        print("  Resetting to test defaults ...")
        auth.limits.reset_api_rate_limits()

        print("\nAll limits reset to defaults.")

    print("Test data cleaned up.")


if __name__ == "__main__":
    main()
