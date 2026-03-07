from unittest.mock import MagicMock, patch

import httpx
import pytest

from ksef2.clients.base import Client
from ksef2.clients.testdata import TestDataClient as KSeFTestDataClient
from ksef2.config import Environment, TimeoutConfig, TransportConfig
from ksef2.core.exceptions import (
    KSeFClientClosedError,
    KSeFUnsupportedEnvironmentError,
)

HTTPX_CLIENT_CLASS = httpx.Client


class TestClient:
    def test_testdata_accessor_uses_client(
        self,
    ) -> None:
        client = Client(environment=Environment.TEST)

        assert isinstance(client.testdata, KSeFTestDataClient)

    def test_testdata_accessor_rejects_production_environment(self) -> None:
        client = Client(environment=Environment.PRODUCTION)

        with pytest.raises(
            KSeFUnsupportedEnvironmentError,
            match="testdata is only available",
        ):
            _ = client.testdata

    @patch("ksef2.clients.base.httpx.Client")
    def test_close_closes_owned_http_client(
        self,
        client_cls: MagicMock,
    ) -> None:
        http_client = MagicMock(spec=HTTPX_CLIENT_CLASS)
        client_cls.return_value = http_client

        client = Client(environment=Environment.TEST)
        client.close()

        http_client.close.assert_called_once()

    def test_close_does_not_close_user_supplied_http_client(self) -> None:
        http_client = MagicMock(spec=HTTPX_CLIENT_CLASS)

        client = Client(environment=Environment.TEST, http_client=http_client)
        client.close()

        http_client.close.assert_not_called()

    @patch("ksef2.clients.base.httpx.Client")
    def test_context_manager_closes_owned_client(
        self,
        client_cls: MagicMock,
    ) -> None:
        http_client = MagicMock(spec=HTTPX_CLIENT_CLASS)
        client_cls.return_value = http_client

        with Client(environment=Environment.TEST):
            pass

        http_client.close.assert_called_once()

    @patch("ksef2.clients.base.httpx.Client")
    def test_transport_config_is_translated_to_httpx_client(
        self,
        client_cls: MagicMock,
    ) -> None:
        http_client = MagicMock(spec=HTTPX_CLIENT_CLASS)
        client_cls.return_value = http_client

        config = TransportConfig(
            timeouts=TimeoutConfig(connect=1.0, read=2.0, write=3.0, pool=4.0),
            proxy_url="http://proxy.local:8080",
        )

        _ = Client(environment=Environment.TEST, transport_config=config)

        _, kwargs = client_cls.call_args
        timeout = kwargs["timeout"]
        assert isinstance(timeout, httpx.Timeout)
        assert timeout.connect == 1.0
        assert timeout.read == 2.0
        assert timeout.write == 3.0
        assert timeout.pool == 4.0
        assert kwargs["proxy"] == "http://proxy.local:8080"
        assert kwargs["http2"] is True

    @patch("ksef2.clients.base.httpx.Client")
    def test_accessors_raise_after_close(
        self,
        client_cls: MagicMock,
    ) -> None:
        client_cls.return_value = MagicMock(spec=HTTPX_CLIENT_CLASS)
        client = Client(environment=Environment.TEST)
        client.close()

        with pytest.raises(KSeFClientClosedError, match="Client is closed"):
            _ = client.authentication
