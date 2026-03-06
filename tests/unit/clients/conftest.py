import pytest

from ksef2.clients.auth import AuthClient
from ksef2.clients.certificates import CertificatesClient
from ksef2.clients.invoices import InvoicesClient
from ksef2.clients.limits import LimitsClient
from ksef2.clients.peppol import PeppolClient
from ksef2.clients.permissions import PermissionsClient
from ksef2.clients.session_log import InvoiceSessionLogClient
from ksef2.clients.testdata import TestDataClient
from ksef2.clients.tokens import TokensClient
from ksef2.core.stores import CertificateStore
from tests.unit.fakes.transport import FakeTransport


@pytest.fixture
def auth_client(fake_transport: FakeTransport) -> AuthClient:
    return AuthClient(fake_transport, CertificateStore())


@pytest.fixture
def permissions_client(fake_transport: FakeTransport) -> PermissionsClient:
    return PermissionsClient(fake_transport)


@pytest.fixture
def certificates_client(fake_transport: FakeTransport) -> CertificatesClient:
    return CertificatesClient(fake_transport)


@pytest.fixture
def peppol_client(fake_transport: FakeTransport) -> PeppolClient:
    return PeppolClient(fake_transport)


@pytest.fixture
def tokens_client(fake_transport: FakeTransport) -> TokensClient:
    return TokensClient(fake_transport)


@pytest.fixture
def invoices_client(fake_transport: FakeTransport) -> InvoicesClient:
    return InvoicesClient(fake_transport)


@pytest.fixture
def limits_client(fake_transport: FakeTransport) -> LimitsClient:
    return LimitsClient(fake_transport)


@pytest.fixture
def session_log_client(fake_transport: FakeTransport) -> InvoiceSessionLogClient:
    return InvoiceSessionLogClient(fake_transport)


@pytest.fixture
def testdata_client(fake_transport: FakeTransport) -> TestDataClient:
    return TestDataClient(fake_transport)
