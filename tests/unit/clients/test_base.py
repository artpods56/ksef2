import pytest

from ksef2.clients.base import Client
from ksef2.clients.testdata import TestDataClient as KSeFTestDataClient
from ksef2.config import Environment


class TestClient:
    def test_testdata_accessor_uses_client(
        self,
    ) -> None:
        client = Client(environment=Environment.TEST)

        assert isinstance(client.testdata, KSeFTestDataClient)

    def test_testdata_accessor_rejects_production_environment(self) -> None:
        client = Client(environment=Environment.PRODUCTION)

        with pytest.raises(ValueError, match="Testdata is only available"):
            _ = client.testdata
