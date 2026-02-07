from __future__ import annotations

import json

import httpx
import pytest
import respx

from ksef_sdk._environments import Environment
from ksef_sdk._testdata import TestDataClient
from ksef_sdk.models.testdata import (
    GrantPermissionsRequest,
    IdentifierInfo,
    RegisterPersonRequest,
    TestPermission,
)


BASE = "https://api-test.ksef.mf.gov.pl"


class TestTestDataClientInit:
    def test_rejects_non_test_env(self):
        with pytest.raises(ValueError, match="Environment.TEST"):
            TestDataClient(Environment.PRODUCTION)

    def test_rejects_demo_env(self):
        with pytest.raises(ValueError, match="Environment.TEST"):
            TestDataClient(Environment.DEMO)

    def test_accepts_test_env(self):
        client = TestDataClient(Environment.TEST)
        client.close()

    def test_context_manager(self):
        with TestDataClient(Environment.TEST) as client:
            assert client is not None


class TestRegisterPerson:
    @respx.mock
    def test_sends_correct_payload(self):
        route = respx.post(f"{BASE}/v2/testdata/person").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )

        req = RegisterPersonRequest(
            nip="7980332920",
            pesel="30112206276",
            description="JDG",
            isBailiff=False,
        )

        with TestDataClient(Environment.TEST) as client:
            resp = client.register_person(req)

        assert resp.status_code == 200
        sent = json.loads(route.calls[0].request.content)
        assert sent == {
            "nip": "7980332920",
            "pesel": "30112206276",
            "description": "JDG",
            "isBailiff": False,
        }


class TestGrantPermissions:
    @respx.mock
    def test_sends_correct_payload(self):
        route = respx.post(f"{BASE}/v2/testdata/permissions").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )

        req = GrantPermissionsRequest(
            contextIdentifier=IdentifierInfo(value="7980332920", type="Nip"),
            authorizedIdentifier=IdentifierInfo(value="30112206276", type="Pesel"),
            permissions=[
                TestPermission(
                    permissionType="InvoiceWrite", description="Write invoices"
                ),
            ],
        )

        with TestDataClient(Environment.TEST) as client:
            resp = client.grant_permissions(req)

        assert resp.status_code == 200
        sent = json.loads(route.calls[0].request.content)
        assert sent == {
            "contextIdentifier": {"value": "7980332920", "type": "Nip"},
            "authorizedIdentifier": {"value": "30112206276", "type": "Pesel"},
            "permissions": [
                {"permissionType": "InvoiceWrite", "description": "Write invoices"},
            ],
        }
