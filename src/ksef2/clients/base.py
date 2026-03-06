from functools import cached_property
from types import TracebackType
from typing import final, Self

import httpx

from ksef2.clients.auth import AuthClient
from ksef2.clients import encryption, peppol
from ksef2.clients.testdata import TestDataClient
from ksef2.config import (
    ConnectionPoolConfig,
    Environment,
    TimeoutConfig,
    TlsConfig,
    TransportConfig,
)
from ksef2.core import exceptions, middlewares, stores
from ksef2.core.http import HttpTransport


@final
class Client:
    def __init__(
        self,
        environment: Environment = Environment.PRODUCTION,
        *,
        transport_config: TransportConfig | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._environment = environment
        self._transport_config = transport_config or TransportConfig()
        self._http_client = http_client or self._build_http_client(
            environment=environment,
            config=self._transport_config,
        )
        self._owns_http_client = http_client is None
        self._lifecycle_state = middlewares.ClientLifecycleState()
        self._transport = middlewares.KSeFExceptionMiddleware(
            middlewares.RetryMiddleware(
                middlewares.ClientLifecycleMiddleware(
                    HttpTransport(client=self._http_client, headers={}),
                    self._lifecycle_state,
                ),
                self._transport_config.retry,
            )
        )
        self._certificate_store = stores.CertificateStore()

    @staticmethod
    def _build_http_client(
        *,
        environment: Environment,
        config: TransportConfig,
    ) -> httpx.Client:
        timeout_cfg: TimeoutConfig = config.timeouts
        pool_cfg: ConnectionPoolConfig = config.pool
        tls_cfg: TlsConfig = config.tls

        verify: bool | str = (
            tls_cfg.ca_bundle_path
            if tls_cfg.ca_bundle_path is not None
            else tls_cfg.verify
        )

        return httpx.Client(
            base_url=environment.base_url,
            timeout=httpx.Timeout(
                connect=timeout_cfg.connect,
                read=timeout_cfg.read,
                write=timeout_cfg.write,
                pool=timeout_cfg.pool,
            ),
            limits=httpx.Limits(
                max_connections=pool_cfg.max_connections,
                max_keepalive_connections=pool_cfg.max_keepalive_connections,
                keepalive_expiry=pool_cfg.keepalive_expiry,
            ),
            verify=verify,
            proxy=config.proxy_url,
            trust_env=config.trust_env,
            http2=config.http2,
        )

    def _ensure_open(self) -> None:
        if self._lifecycle_state.closed:
            raise exceptions.KSeFClientClosedError("Client is closed.")

    @cached_property
    def authentication(self) -> AuthClient:
        self._ensure_open()
        return AuthClient(
            transport=self._transport,
            certificate_store=self._certificate_store,
            environment=self._environment,
        )

    @cached_property
    def encryption(self) -> encryption.EncryptionClient:
        self._ensure_open()
        return encryption.EncryptionClient(self._transport)

    @cached_property
    def testdata(self) -> TestDataClient:
        self._ensure_open()
        if self._environment is not Environment.TEST:
            raise exceptions.KSeFUnsupportedEnvironmentError(
                "testdata is only available for Environment.TEST"
            )
        return TestDataClient(self._transport)

    @cached_property
    def peppol(self) -> peppol.PeppolClient:
        self._ensure_open()
        return peppol.PeppolClient(self._transport)

    def close(self) -> None:
        if self._lifecycle_state.closed:
            return

        self._lifecycle_state.closed = True

        for name in ("authentication", "encryption", "testdata", "peppol"):
            self.__dict__.pop(name, None)

        if self._owns_http_client:
            self._http_client.close()

    def __enter__(self) -> Self:
        self._ensure_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
