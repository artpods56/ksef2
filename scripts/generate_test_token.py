#!/usr/bin/env python
"""Generate a KSeF token for integration testing.

Usage:
    python scripts/generate_test_token.py

Requires environment variables in .env.test:
    KSEF_TEST_SUBJECT_NIP
    KSEF_TEST_PERSON_NIP
    KSEF_TEST_PERSON_PESEL

The generated token can be added to .env.test as KSEF_TEST_KSEF_TOKEN
"""

from __future__ import annotations

import os
import sys

from ksef2 import Client
from ksef2.config import Environment
from ksef2.core.exceptions import KSeFApiError
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import SubjectType

from dotenv import load_dotenv
from structlog import get_logger

logger = get_logger(__name__)

_ = load_dotenv()


def main() -> int:
    """Generate KSeF credentials for integration testing.

    This script:
    1. Creates a test subject via testdata API
    2. Authenticates using XAdES with self-signed certificate
    3. Returns access token that can be used for API calls

    Note: Token generation (creating KSeF tokens) requires additional setup
    that may not work in all test environments. For full token generation,
    you may need to use the KSeF portal directly or the Java/C# reference
    implementations.
    """

    try:
        subject_nip = os.environ["KSEF_TEST_SUBJECT_NIP"]
        _ = os.environ["KSEF_TEST_PERSON_NIP"]
        _ = os.environ["KSEF_TEST_PERSON_PESEL"]
    except KeyError as e:
        raise ValueError(f"Missing required environment variable: {e}") from e

    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as td:
        logger.info("Creating test subject...")
        try:
            td.create_subject(
                nip=subject_nip,
                subject_type=SubjectType.VAT_GROUP,
                description="Integration test subject",
            )
        except KSeFApiError as e:
            if e.status_code == 500:
                logger.warning("Subject may already exist, continuing...")
            else:
                raise

        logger.info("Authenticating with XAdES (self-signed cert)...")
        cert, private_key = generate_test_certificate(subject_nip)
        tokens = client.auth.authenticate_xades(
            nip=subject_nip,
            cert=cert,
            private_key=private_key,
        )

        logger.info(f"Generated token: {tokens.model_dump_json(indent=2)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
