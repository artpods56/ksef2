from functools import cached_property
from typing import final

import httpx

from ksef2.clients import encryption
from ksef2.config import Environment
from ksef2.core.http import HttpTransport
from ksef2.core.middleware import KSeFProtocol

from ksef2.services import (
    auth,
    certificates,
    limits,
    peppol,
    session,
    testdata,
    tokens,
)
from ksef2.core import stores


@final
class Client:
    def __init__(self, environment: Environment = Environment.PRODUCTION) -> None:
        self._environment = environment
        self._transport = KSeFProtocol(
            HttpTransport(client=httpx.Client(base_url=environment.base_url)),
        )

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
        transport = KSeFProtocol(
            HttpTransport(client=httpx.Client(base_url=base_url)),
        )
        return testdata.TestDataService(transport)

    @cached_property
    def limits(self) -> limits.LimitsService:
        return limits.LimitsService(self._transport)

    @cached_property
    def certificates(self) -> certificates.CertificateService:
        return certificates.CertificateService(self._transport)

    @cached_property
    def peppol(self) -> peppol.PeppolService:
        return peppol.PeppolService(self._transport)
