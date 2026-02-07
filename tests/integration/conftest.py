from __future__ import annotations

import os
import random
import textwrap

import pytest

from ksef_sdk import Environment, KsefClient, TestDataClient
from ksef_sdk.models.testdata import (
    GrantPermissionsRequest,
    IdentifierInfo,
    RegisterPersonRequest,
    TestPermission,
)


def _generate_random_nip() -> str:
    """Generate a random 10-digit NIP valid for the KSeF TEST environment.

    The XSD pattern is ``[1-9]((\\d[1-9])|([1-9]\\d))\\d{7}`` — the first
    digit is 1-9 and at least one of digits 2-3 must be non-zero.
    """
    first = random.randint(1, 9)
    # Digits 2-3: ensure at least one is non-zero (range 01-99)
    second_third = random.randint(1, 99)
    rest = random.randint(0, 9_999_999)
    return f"{first}{second_third:02d}{rest:07d}"


# ---------------------------------------------------------------------------
# Env-var fixtures — skip if credentials are not provided
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ksef_nip() -> str:
    """NIP for integration tests.

    Falls back to a random NIP when ``KSEF_TEST_NIP`` is not set
    (the TEST environment accepts any valid-format NIP).
    """
    return os.environ.get("KSEF_TEST_NIP") or _generate_random_nip()


@pytest.fixture(scope="session")
def ksef_token() -> str | None:
    """KSeF token for token-based auth tests.

    Returns ``None`` when ``KSEF_TEST_TOKEN`` is not set — tests that
    need it should skip explicitly.
    """
    return os.environ.get("KSEF_TEST_TOKEN") or None


@pytest.fixture(scope="session")
def ksef_pesel() -> str:
    pesel = os.environ.get("KSEF_TEST_PESEL")
    if not pesel:
        pytest.skip("KSEF_TEST_PESEL not set")
    return pesel


# ---------------------------------------------------------------------------
# TestDataClient — session-scoped, shared by all integration tests
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def testdata_client() -> TestDataClient:
    client = TestDataClient(Environment.TEST)
    yield client  # type: ignore[misc]
    client.close()


# ---------------------------------------------------------------------------
# setup_person — idempotent person + permission bootstrap
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def setup_person(
    testdata_client: TestDataClient,
    ksef_nip: str,
    ksef_pesel: str,
) -> None:
    """Register a person and grant InvoiceWrite permission (idempotent)."""
    testdata_client.register_person(
        RegisterPersonRequest(
            nip=ksef_nip,
            pesel=ksef_pesel,
            description="Integration-test person",
        )
    )
    testdata_client.grant_permissions(
        GrantPermissionsRequest(
            contextIdentifier=IdentifierInfo(value=ksef_nip, type="Nip"),
            authorizedIdentifier=IdentifierInfo(value=ksef_pesel, type="Pesel"),
            permissions=[
                TestPermission(
                    permissionType="InvoiceWrite",
                    description="Allow sending invoices",
                ),
            ],
        )
    )


# ---------------------------------------------------------------------------
# KsefClient — function-scoped, authenticated per test
# ---------------------------------------------------------------------------


@pytest.fixture()
def ksef_client(ksef_nip: str, ksef_token: str | None) -> KsefClient:
    """Authenticated KsefClient.

    Uses token-based auth when ``KSEF_TEST_TOKEN`` is set, otherwise
    falls back to XAdES auth with an auto-generated self-signed certificate.
    """
    client = KsefClient(nip=ksef_nip, token=ksef_token, env=Environment.TEST)
    if ksef_token:
        client.authenticate()
    else:
        client.authenticate_xades()
    yield client  # type: ignore[misc]
    client.close()


# ---------------------------------------------------------------------------
# Sample invoice XML used by session tests
# ---------------------------------------------------------------------------

SAMPLE_INVOICE_XML = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <Faktura xmlns="http://crd.gov.pl/wzor/2021/11/29/11089/">
        <Naglowek><KodFormularza>FA</KodFormularza></Naglowek>
    </Faktura>
""").encode()
