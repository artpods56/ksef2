from __future__ import annotations

import pytest

from ksef_sdk import TestDataClient
from ksef_sdk.models.testdata import (
    GrantPermissionsRequest,
    IdentifierInfo,
    RegisterPersonRequest,
    TestPermission,
)

pytestmark = pytest.mark.integration


class TestTestData:
    def test_register_person(
        self,
        testdata_client: TestDataClient,
        ksef_nip: str,
        ksef_pesel: str,
    ) -> None:
        resp = testdata_client.register_person(
            RegisterPersonRequest(
                nip=ksef_nip,
                pesel=ksef_pesel,
                description="integration-test person",
            )
        )
        assert resp.status_code == 200

    def test_grant_permissions(
        self,
        testdata_client: TestDataClient,
        ksef_nip: str,
        ksef_pesel: str,
    ) -> None:
        resp = testdata_client.grant_permissions(
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
        assert resp.status_code == 200
