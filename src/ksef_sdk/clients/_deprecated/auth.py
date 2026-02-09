from __future__ import annotations

import time
from typing import TYPE_CHECKING

from httpx._status_codes import codes

from ksef_sdk.clients._deprecated._base import BaseSubClient
from ksef_sdk.core.crypto import encrypt_token, select_certificate
from ksef_sdk.core.exceptions import KSeFAuthError
from ksef_sdk.domain.models._deprecated.auth import AuthTokens, RefreshedToken
from ksef_sdk.infra.mappers._deprecated.auth import (
    AuthInitMapper,
    AuthTokensMapper,
    ChallengeMapper,
    RefreshedTokenMapper,
)
from ksef_sdk.infra.schema.model import (
    AuthenticationChallengeResponse,
    AuthenticationInitResponse,
    AuthenticationOperationStatusResponse,
    AuthenticationTokenRefreshResponse,
    AuthenticationTokensResponse,
)

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
    from cryptography.x509 import Certificate


class AuthClient(BaseSubClient):
    """Handles the full KSeF authentication lifecycle."""

    # -- token-based auth --

    def authenticate(
        self,
        *,
        token: str,
        nip: str,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 30,
    ) -> AuthTokens:
        """Run the full KSeF token-authentication flow.

        1. Request a challenge
        2. Encrypt ``token|timestamp`` with MF public key
        3. POST encrypted token -> get referenceNumber
        4. Poll until status=200
        5. Redeem -> AuthTokens (access_token + refresh_token)
        """
        challenge_resp = self._request_challenge()
        challenge = ChallengeMapper.map_response(challenge_resp)

        certs = self._certificate_store.get_certificates()
        cert = select_certificate(certs, "KsefTokenEncryption")
        encrypted = encrypt_token(token, str(challenge.timestamp_ms), cert.certificate)

        body = AuthInitMapper.map_request(challenge.challenge, nip, encrypted)
        init_resp = self._http.post(
            "/auth/ksef-token",
            body=body,
            response_model=AuthenticationInitResponse,
        )
        init_domain = AuthInitMapper.map_response(init_resp)

        self._poll_auth_status(
            init_resp.referenceNumber,
            bearer_token=init_domain.authentication_token,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        return self._redeem_token(init_domain.authentication_token)

    # -- XAdES-based auth --

    def authenticate_xades(
        self,
        *,
        nip: str,
        cert: Certificate | None = None,
        private_key: RSAPrivateKey | None = None,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 30,
    ) -> AuthTokens:
        """Authenticate via XAdES signature (no pre-existing KSeF token needed).

        If *cert* and *private_key* are not provided, a self-signed test
        certificate is auto-generated using the NIP.
        """
        from ksef_sdk.core.xades import (
            build_auth_token_request_xml,
            generate_test_certificate,
            sign_xades,
            submit_xades_auth,
        )

        if cert is None or private_key is None:
            cert, private_key = generate_test_certificate(nip)

        challenge_resp = self._request_challenge()
        challenge = ChallengeMapper.map_response(challenge_resp)

        xml_bytes = build_auth_token_request_xml(challenge.challenge, nip)
        signed_xml = sign_xades(xml_bytes, cert, private_key)
        init_resp = submit_xades_auth(self._http, signed_xml, verify_chain=False)
        init_domain = AuthInitMapper.map_response(init_resp)

        self._poll_auth_status(
            init_resp.referenceNumber,
            bearer_token=init_domain.authentication_token,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        return self._redeem_token(init_domain.authentication_token)

    # -- token management --

    def refresh(self, refresh_token: str) -> RefreshedToken:
        """``POST /auth/token/refresh`` — obtain a new access token."""
        resp = self._http.request(
            "POST",
            "/auth/token/refresh",
            response_model=AuthenticationTokenRefreshResponse,
            extra_headers={"Authorization": f"Bearer {refresh_token}"},
        )
        return RefreshedTokenMapper.map_response(resp)

    # -- internal helpers --

    def _request_challenge(self) -> AuthenticationChallengeResponse:
        return self._http.post(
            "/auth/challenge",
            response_model=AuthenticationChallengeResponse,
        )

    def _poll_auth_status(
        self,
        reference_number: str,
        *,
        bearer_token: str | None = None,
        poll_interval: float = 1.0,
        max_attempts: int = 30,
    ) -> None:
        for _ in range(max_attempts):
            extra = (
                {"Authorization": f"Bearer {bearer_token}"} if bearer_token else None
            )
            status = self._http.request(
                "GET",
                f"/auth/{reference_number}",
                response_model=AuthenticationOperationStatusResponse,
                extra_headers=extra,
            )
            code = status.status.code
            if code == 200:
                return
            if code >= 400:
                raise KSeFAuthError(
                    code=code,
                    message="Authentication failed.",
                    response=status,
                )
            time.sleep(poll_interval)

        raise KSeFAuthError(
            code=codes.REQUEST_TIMEOUT,
            message="Authentication polling timed out.",
            response=None,
        )

    def _redeem_token(self, auth_token: str) -> AuthTokens:
        resp = self._http.request(
            "POST",
            "/auth/token/redeem",
            response_model=AuthenticationTokensResponse,
            extra_headers={"Authorization": f"Bearer {auth_token}"},
        )
        return AuthTokensMapper.map_response(resp)
