from functools import cached_property
from typing import final

from ksef_sdk.clients import encryption
from ksef_sdk.config import Environment
from ksef_sdk.core.http import HttpTransport

from ksef_sdk.services import auth, session, testdata, tokens
from ksef_sdk.core import stores


@final
class Client:
    def __init__(self, environment: Environment = Environment.PRODUCTION) -> None:
        self._environment = environment
        self._transport = HttpTransport(environment)

    @cached_property
    def auth(self) -> auth.AuthService:
        return auth.AuthService(
            transport=self._transport,
            certificate_store=stores.CertificateStore(),
        )

    @cached_property
    def encryption(self) -> encryption.EncryptionClient:
        return encryption.EncryptionClient(self._transport)

    @cached_property
    def sessions(self) -> session.OpenSessionService:
        return session.OpenSessionService(
            transport=self._transport,
            certificate_store=stores.CertificateStore(),
        )

    @cached_property
    def tokens(self) -> tokens.TokenService:
        return tokens.TokenService(self._transport)

    @cached_property
    def testdata(self) -> testdata.TestDataService:
        base_url = self._environment.testdata_base_url
        if base_url is None:
            raise ValueError("Testdata is only available on TEST environment")
        transport = HttpTransport(self._environment, base_url=base_url)
        return testdata.TestDataService(transport)
