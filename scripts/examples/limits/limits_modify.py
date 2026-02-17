"""Modify and reset API limits (TEST environment only).

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

        # --- Modify session limits ---
        print("Modifying session limits ...")
        limits = client.limits.get_context_limits(access_token=access_token)
        original_max = limits.online_session.max_invoices
        limits.online_session.max_invoices = 5000
        client.limits.set_session_limits(access_token=access_token, limits=limits)
        print(f"  max_invoices: {original_max} → 5000")

        # Reset session limits back to defaults
        print("  Resetting session limits ...")
        client.limits.reset_session_limits(access_token=access_token)

        # --- Modify subject limits ---
        print("Modifying subject limits ...")
        subject_limits = client.limits.get_subject_limits(access_token=access_token)
        if subject_limits.certificate:
            subject_limits.certificate.max_certificates = 10
            client.limits.set_subject_limits(
                access_token=access_token, limits=subject_limits
            )
            print("  max_certificates → 10")

        # Reset subject limits back to defaults
        print("  Resetting subject limits ...")
        client.limits.reset_subject_limits(access_token=access_token)

        # --- Modify API rate limits ---
        print("Modifying API rate limits ...")
        rate_limits = client.limits.get_api_rate_limits(access_token=access_token)
        rate_limits.invoice_send.per_second = 50
        rate_limits.invoice_send.per_minute = 200
        client.limits.set_api_rate_limits(access_token=access_token, limits=rate_limits)
        print("  invoice_send: 100/s, 500/m")

        # Reset rate limits back to defaults
        print("  Resetting API rate limits ...")
        client.limits.reset_api_rate_limits(access_token=access_token)

        # --- Set production rate limits ---
        print("Setting production rate limits ...")
        client.limits.set_production_rate_limits(access_token=access_token)
        print("  Rate limits set to production values")

        # Check the new limits
        prod_limits = client.limits.get_api_rate_limits(access_token=access_token)
        print(
            f"  invoice_send: {prod_limits.invoice_send.per_second}/s, {prod_limits.invoice_send.per_minute}/m, {prod_limits.invoice_send.per_hour}/h"
        )

        # Reset back to test defaults
        print("  Resetting to test defaults ...")
        client.limits.reset_api_rate_limits(access_token=access_token)

        print("All limits reset to defaults.")

    print("Test data cleaned up.")


if __name__ == "__main__":
    main()
