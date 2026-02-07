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
    GenerateTokenResponse,
    PublicKeyCertificate,
    SessionInvoicesResponse,
    SessionStatusResponse,
    TokenStatusResponse,
)
from ksef_sdk._http import HttpTransport
from ksef_sdk._sessions import OnlineSession
from ksef_sdk._tokens import (
    generate_token,
    get_token_status,
    poll_token_status,
    revoke_token,
)
from ksef_sdk._xades import (
    authenticate_xades as _authenticate_xades,
    generate_test_certificate,
)

if TYPE_CHECKING:
    from types import TracebackType

    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
    from cryptography.x509 import Certificate


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
        token: str | None = None,
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

        Requires a ``token`` to have been passed to the constructor.
        For token-less auth see :meth:`authenticate_xades`.
        """
        if self._token is None:
            from ksef_sdk.exceptions import KsefAuthError

            raise KsefAuthError(
                0, "No KSeF token provided — pass token= to KsefClient or use authenticate_xades()"
            )

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

    def authenticate_xades(
        self,
        *,
        cert: Certificate | None = None,
        private_key: RSAPrivateKey | None = None,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 30,
    ) -> None:
        """Authenticate via XAdES signature (no pre-existing KSeF token needed).

        If *cert* and *private_key* are not provided, a self-signed test
        certificate is auto-generated using the client's NIP.
        """
        if cert is None or private_key is None:
            cert, private_key = generate_test_certificate(self._nip)

        self._refresh_token = _authenticate_xades(
            self._http,
            self._nip,
            cert,
            private_key,
            poll_interval=poll_interval,
            max_poll_attempts=max_poll_attempts,
        )

    # -- token management --

    def generate_ksef_token(
        self,
        permissions: list[str],
        description: str,
        *,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> GenerateTokenResponse:
        """Generate a new KSeF token and wait for it to become active.

        Returns the :class:`GenerateTokenResponse` whose ``.token`` field
        contains the token string usable for future :meth:`authenticate` calls.
        """
        resp = generate_token(
            self._http, permissions=permissions, description=description
        )
        poll_token_status(
            self._http,
            resp.referenceNumber,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )
        return resp

    def get_ksef_token_status(self, reference_number: str) -> TokenStatusResponse:
        """Get the current status of a KSeF token."""
        return get_token_status(self._http, reference_number)

    def revoke_ksef_token(self, reference_number: str) -> None:
        """Revoke a KSeF token."""
        revoke_token(self._http, reference_number)

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
