"""Block and unblock authentication contexts (TEST environment only).

Demonstrates how to block and unblock authentication for a context.
When blocked, the context cannot authenticate until unblocked.

Usage:
    uv run python scripts/examples/testdata/block_context.py
"""

from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.domain.models.testdata import (
    AuthContextIdentifier,
    AuthContextIdentifierType,
    SubjectType,
)

ORG_NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        # Create a test subject
        print(f"Creating test subject with NIP: {ORG_NIP}")
        temp.create_subject(
            nip=ORG_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Block context test",
        )

        # Create identifier for the context
        context_id = AuthContextIdentifier(
            type=AuthContextIdentifierType.NIP,
            value=ORG_NIP,
        )

        # Block the context
        print(f"Blocking context for NIP: {ORG_NIP}")
        client.testdata.block_context(context_identifier=context_id)
        print("  Context blocked - authentication is now disabled")

        # At this point, any authentication attempt for this NIP would fail

        # Unblock the context
        print(f"Unblocking context for NIP: {ORG_NIP}")
        client.testdata.unblock_context(context_identifier=context_id)
        print("  Context unblocked - authentication is now enabled")

    print("Test data cleaned up.")


if __name__ == "__main__":
    main()
