from functools import cached_property
from typing import final

import httpx

from ksef2.clients.auth import AuthClient
from ksef2.clients import encryption, peppol
from ksef2.config import Environment
from ksef2.core.http import HttpTransport
from ksef2.core.middlewares.exceptions import KSeFExceptionMiddleware

from ksef2.clients.testdata import TestDataClient
from ksef2.core import stores


@final
class Client:
    def __init__(self, environment: Environment = Environment.PRODUCTION) -> None:
        self._environment = environment
        self._transport = KSeFExceptionMiddleware(
            HttpTransport(
                client=httpx.Client(base_url=environment.base_url), headers={}
            ),
        )
        self._certificate_store = stores.CertificateStore()

    @cached_property
    def authentication(self) -> AuthClient:
        return AuthClient(
            transport=self._transport,
            certificate_store=self._certificate_store,
            environment=self._environment,
        )

    @cached_property
    def encryption(self) -> encryption.EncryptionClient:
        return encryption.EncryptionClient(self._transport)

    @cached_property
    def testdata(self) -> TestDataClient:
        base_url = self._environment.testdata_base_url
        if base_url is None:
            raise ValueError("Testdata is only available on TEST environment")
        transport = KSeFExceptionMiddleware(
            HttpTransport(client=httpx.Client(base_url=base_url), headers={}),
        )
        return TestDataClient(transport)

    @cached_property
    def peppol(self) -> peppol.PeppolClient:
        return peppol.PeppolClient(self._transport)
