from __future__ import annotations

from typing import TYPE_CHECKING

from ksef_sdk._auth import (
    init_token_auth,
    poll_auth_status,
    redeem_token,
    refresh_access_token as _refresh_access_token,
    request_challenge,
)
from ksef_sdk._environments import Environment
from ksef_sdk._generated.model import (
    FormCode,
    PublicKeyCertificate,
    SessionInvoicesResponse,
    SessionStatusResponse,
)
from ksef_sdk._http import HttpTransport
from ksef_sdk._sessions import OnlineSession

if TYPE_CHECKING:
    from types import TracebackType


class KsefClient:
    """High-level facade for the KSeF API.

    Usage::

        with KsefClient(nip="1234567890", token="abc...", env=Environment.TEST) as client:
            client.authenticate()

            with client.online_session() as session:
                result = session.send_invoice(invoice_xml_bytes)
                print(result.referenceNumber)
    """

    def __init__(
        self,
        *,
        nip: str,
        token: str,
        env: Environment = Environment.PRODUCTION,
    ) -> None:
        self._nip = nip
        self._token = token
        self._http = HttpTransport(env)
        self._certificates: list[PublicKeyCertificate] | None = None
        self._refresh_token: str | None = None

    # -- lifecycle (resource management) --

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

    # -- certificates --

    def get_public_key_certificates(self) -> list[PublicKeyCertificate]:
        """Fetch (and cache) MF public-key certificates."""
        if self._certificates is None:
            self._certificates = self._http.get_list(
                "/security/public-key-certificates",
                item_model=PublicKeyCertificate,
            )
        return self._certificates

    # -- authentication --

    def authenticate(
        self,
        *,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 30,
    ) -> None:
        """Run the full KSeF token-authentication flow.

        1. Request a challenge
        2. Encrypt ``token|timestamp`` with MF public key
        3. POST encrypted token → get referenceNumber
        4. Poll until status=200
        5. Redeem → access_token + refresh_token
        """
        certs = self.get_public_key_certificates()

        challenge = request_challenge(self._http)

        init_resp = init_token_auth(
            self._http,
            nip=self._nip,
            token=self._token,
            challenge=challenge,
            certificates=certs,
        )

        poll_auth_status(
            self._http,
            init_resp.referenceNumber,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        # Use the authenticationToken from init as Bearer to redeem
        tokens = redeem_token(self._http, init_resp.authenticationToken.token)
        self._http.set_access_token(tokens.accessToken.token)
        self._refresh_token = tokens.refreshToken.token

    def refresh_access_token(self) -> None:
        """Refresh the current access token using the stored refresh token."""
        if self._refresh_token is None:
            from ksef_sdk.exceptions import KsefAuthError
            raise KsefAuthError(0, "No refresh token available — authenticate first")

        resp = _refresh_access_token(self._http, self._refresh_token)
        self._http.set_access_token(resp.accessToken.token)

    # -- sessions --

    def online_session(self, *, form_code: FormCode | None = None) -> OnlineSession:
        """Create an :class:`OnlineSession` context manager."""
        certs = self.get_public_key_certificates()
        return OnlineSession(self._http, certs, form_code=form_code)

    # -- status queries --

    def get_session_status(self, reference_number: str) -> SessionStatusResponse:
        """``GET /sessions/{referenceNumber}``"""
        return self._http.get(
            f"/sessions/{reference_number}",
            response_model=SessionStatusResponse,
        )

    def get_session_invoices(
        self,
        reference_number: str,
        *,
        continuation_token: str | None = None,
    ) -> SessionInvoicesResponse:
        """``GET /sessions/{referenceNumber}/invoices``"""
        path = f"/sessions/{reference_number}/invoices"
        if continuation_token:
            path += f"?continuationToken={continuation_token}"
        return self._http.get(path, response_model=SessionInvoicesResponse)
