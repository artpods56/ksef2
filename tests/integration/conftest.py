from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Generator

import pytest

from ksef2 import Client
from ksef2.config import Environment
from ksef2.core.exceptions import KSeFApiError
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.auth import AuthTokens
from ksef2.domain.models.testdata import (
    SubjectType,
)
from ksef2.services.testdata import TemporalTestData


from dotenv import load_dotenv

_ = load_dotenv(".env.test")

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class KSeFCredentials:
    subject_nip: str
    person_nip: str
    person_pesel: str
    ksef_token: str


@pytest.fixture(scope="session")
def ksef_credentials() -> KSeFCredentials:
    """Load KSeF TEST credentials from environment variables.

    Required env vars:
        KSEF_TEST_SUBJECT_NIP - NIP for test subject
        KSEF_TEST_PERSON_NIP  - NIP for test person
        KSEF_TEST_PERSON_PESEL - PESEL for test person
        KSEF_TEST_KSEF_TOKEN  - KSeF token for authentication (optional for XAdES tests)
    """
    subject_nip = os.environ.get("KSEF_TEST_SUBJECT_NIP")
    person_nip = os.environ.get("KSEF_TEST_PERSON_NIP")
    person_pesel = os.environ.get("KSEF_TEST_PERSON_PESEL")
    ksef_token = os.environ.get("KSEF_TEST_KSEF_TOKEN")

    missing = []
    if not subject_nip:
        missing.append("KSEF_TEST_SUBJECT_NIP")
    if not person_nip:
        missing.append("KSEF_TEST_PERSON_NIP")
    if not person_pesel:
        missing.append("KSEF_TEST_PERSON_PESEL")

    if missing:
        pytest.skip(f"Missing required env vars: {', '.join(missing)}")

    assert subject_nip and person_nip and person_pesel

    return KSeFCredentials(
        subject_nip=subject_nip,
        person_nip=person_nip,
        person_pesel=person_pesel,
        ksef_token=ksef_token or "",
    )


@pytest.fixture(scope="session")
def real_client() -> Client:
    """Create a client pointing to the KSeF TEST environment."""
    return Client(environment=Environment.TEST)


@pytest.fixture
def test_context(real_client: Client, ksef_credentials: KSeFCredentials):
    """Create a test context with TemporalTestData for setup/teardown.

    This fixture provides a TemporalTestData context manager that automatically
    cleans up created subjects, persons, and permissions when the test completes.
    """
    return real_client.testdata.temporal()


def _ensure_subject_exists(td: TemporalTestData, nip: str) -> None:
    """Try to create subject, handling case where it already exists."""
    try:
        td.create_subject(
            nip=nip,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="Integration test subject",
        )
    except KSeFApiError as e:
        if _is_already_exists_error(e):
            logger.warning(f"Subject {nip} may already exist, continuing...")
        else:
            raise


def _ensure_person_exists(td: TemporalTestData, nip: str, pesel: str) -> None:
    """Try to create person, handling case where it already exists."""
    try:
        td.create_person(
            nip=nip,
            pesel=pesel,
            description="Integration test person",
        )
    except KSeFApiError as e:
        if _is_already_exists_error(e):
            logger.warning(f"Person {nip}/{pesel} may already exist, continuing...")
        else:
            raise


def _is_already_exists_error(e: KSeFApiError) -> bool:
    """Check if the error is because the resource already exists."""
    error_str = str(e).lower()
    return (
        "30001" in error_str
        or "already exists" in error_str
        or "już istnieje" in error_str
    )


@pytest.fixture
def xades_authenticated_context(
    real_client: Client,
    ksef_credentials: KSeFCredentials,
    test_context: TemporalTestData,
) -> Generator[tuple[Client, AuthTokens], None, None]:
    """Create an authenticated context using XAdES with self-signed certificate.

    This is the entry point for tests that don't have a KSeF token yet.
    Uses self-signed certificate for authentication (allowed on TEST env only).

    Sets up:
        1. Test subject (VAT_GROUP) - or uses existing
        2. Generates self-signed certificate for the subject
        3. Authenticates using XAdES with that certificate
        4. Yields (client, tokens)

    Note: Token generation may not work with self-signed certs - it requires
    the authenticated entity to have CredentialsManage permission which needs
    to be granted via the testdata API.

    Cleanup (automatic via TemporalTestData):
        1. Delete subject
    """
    td = test_context

    _ensure_subject_exists(td, ksef_credentials.subject_nip)

    cert, private_key = generate_test_certificate(ksef_credentials.subject_nip)

    tokens = real_client.auth.authenticate_xades(
        nip=ksef_credentials.subject_nip,
        cert=cert,
        private_key=private_key,
    )

    yield real_client, tokens


@pytest.fixture
def authenticated_context(
    real_client: Client,
    ksef_credentials: KSeFCredentials,
    test_context: TemporalTestData,
) -> Generator[tuple[Client, AuthTokens], None, None]:
    """Create an authenticated context using XAdES authentication.

    Note: We use XAdES instead of KSeF token authentication because:
    1. Token authentication requires encrypting the token with RSA-OAEP
    2. The KSeF token must fit within ~190 bytes (2048-bit key limit)
    3. Pre-generated tokens from env are typically JWTs that are too long

    Sets up:
        1. Test subject (VAT_GROUP) - or uses existing
        2. Authenticates using XAdES with self-signed certificate
        3. Yields (client, tokens)

    Cleanup (automatic via TemporalTestData):
        1. Delete subject
    """
    td = test_context

    _ensure_subject_exists(td, ksef_credentials.subject_nip)

    cert, private_key = generate_test_certificate(ksef_credentials.subject_nip)

    tokens = real_client.auth.authenticate_xades(
        nip=ksef_credentials.subject_nip,
        cert=cert,
        private_key=private_key,
    )

    yield real_client, tokens
