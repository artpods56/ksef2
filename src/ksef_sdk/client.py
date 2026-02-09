from __future__ import annotations

from typing import TYPE_CHECKING, final

from ksef_sdk.core._certificates import CertificateStore
from ksef_sdk.core.http import HttpTransport
from ksef_sdk.domain.models._deprecated._environments import Environment

if TYPE_CHECKING:
    from types import TracebackType

    from ksef_sdk.clients._deprecated.auth import AuthClient
    from ksef_sdk.clients._deprecated.exports import ExportsClient
    from ksef_sdk.clients._deprecated.invoices import InvoicesClient
    from ksef_sdk.clients._deprecated.limits import LimitsClient
    from ksef_sdk.clients._deprecated.sessions import SessionsClient
    from ksef_sdk.clients._deprecated.tokens import TokensClient


@final
class KsefClient:
    """High-level stateless facade for the KSeF API.

    ``KsefClient`` owns the HTTP transport and certificate store.
    All session state lives in the sub-clients or is passed explicitly
    by the caller (e.g. ``access_token``).

    Usage::

        with KsefClient(env=Environment.TEST) as client:
            tokens = client.auth.authenticate(token="abc...", nip="1234567890")

            with client.sessions.open_online(access_token=tokens.access_token) as session:
                result = session.send_invoice(invoice_xml_bytes)
    """

    def __init__(self, *, env: Environment = Environment.PRODUCTION) -> None:
        self._http = HttpTransport(env)
        self._certificate_store = CertificateStore(self._http)
        self._auth: AuthClient | None = None
        self._sessions: SessionsClient | None = None
        self._tokens: TokensClient | None = None
        self._invoices: InvoicesClient | None = None
        self._exports: ExportsClient | None = None
        self._limits: LimitsClient | None = None

    # -- lifecycle --

    def close(self) -> None:
        """Close the underlying HTTP transport."""
        self._http.close()

    def __enter__(self) -> KsefClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    # -- sub-clients (lazy) --

    @property
    def auth(self) -> AuthClient:
        if self._auth is None:
            from ksef_sdk.clients._deprecated.auth import AuthClient

            self._auth = AuthClient(self._http, self._certificate_store)
        return self._auth

    @property
    def sessions(self) -> SessionsClient:
        if self._sessions is None:
            from ksef_sdk.clients._deprecated.sessions import SessionsClient

            self._sessions = SessionsClient(self._http, self._certificate_store)
        return self._sessions

    @property
    def tokens(self) -> TokensClient:
        if self._tokens is None:
            from ksef_sdk.clients._deprecated.tokens import TokensClient

            self._tokens = TokensClient(self._http, self._certificate_store)
        return self._tokens

    @property
    def invoices(self) -> InvoicesClient:
        if self._invoices is None:
            from ksef_sdk.clients._deprecated.invoices import InvoicesClient

            self._invoices = InvoicesClient(self._http, self._certificate_store)
        return self._invoices

    @property
    def exports(self) -> ExportsClient:
        if self._exports is None:
            from ksef_sdk.clients._deprecated.exports import ExportsClient

            self._exports = ExportsClient(self._http, self._certificate_store)
        return self._exports

    @property
    def limits(self) -> LimitsClient:
        if self._limits is None:
            from ksef_sdk.clients._deprecated.limits import LimitsClient

            self._limits = LimitsClient(self._http, self._certificate_store)
        return self._limits
