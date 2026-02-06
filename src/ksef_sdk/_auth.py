from __future__ import annotations

import time
from typing import TYPE_CHECKING

from ksef_sdk._crypto import encrypt_token, select_certificate
from ksef_sdk._generated.model import (
    AuthenticationChallengeResponse,
    AuthenticationContextIdentifier,
    AuthenticationInitResponse,
    AuthenticationOperationStatusResponse,
    AuthenticationTokenRefreshResponse,
    AuthenticationTokensResponse,
    InitTokenAuthenticationRequest,
    PublicKeyCertificate,
)
from ksef_sdk.exceptions import KsefAuthError

if TYPE_CHECKING:
    from ksef_sdk._http import HttpTransport


def request_challenge(http: HttpTransport) -> AuthenticationChallengeResponse:
    """``POST /auth/challenge`` — obtain a challenge UUID + timestamp."""
    return http.post(
        "/auth/challenge",
        response_model=AuthenticationChallengeResponse,
    )  # type: ignore[return-value]


def init_token_auth(
    http: HttpTransport,
    *,
    nip: str,
    token: str,
    challenge: AuthenticationChallengeResponse,
    certificates: list[PublicKeyCertificate],
) -> AuthenticationInitResponse:
    """``POST /auth/ksef-token`` — start token-based authentication."""
    cert = select_certificate(certificates, "KsefTokenEncryption")
    encrypted = encrypt_token(
        token,
        challenge.timestamp.isoformat(),
        cert.certificate,
    )

    # Use model_construct — encryptedToken is Base64Str containing encrypted binary data.
    body = InitTokenAuthenticationRequest.model_construct(
        challenge=challenge.challenge,
        contextIdentifier=AuthenticationContextIdentifier(type="Nip", value=nip),
        encryptedToken=encrypted,
    )
    return http.post(
        "/auth/ksef-token",
        body=body,
        response_model=AuthenticationInitResponse,
    )  # type: ignore[return-value]


def poll_auth_status(
    http: HttpTransport,
    reference_number: str,
    *,
    poll_interval: float = 1.0,
    max_attempts: int = 30,
) -> AuthenticationOperationStatusResponse:
    """``GET /auth/{referenceNumber}`` — poll until authentication completes.

    Raises :class:`KsefAuthError` if the operation fails or times out.
    """
    for _ in range(max_attempts):
        status = http.get(
            f"/auth/{reference_number}",
            response_model=AuthenticationOperationStatusResponse,
        )
        code = status.status.code
        if code == 200:
            return status
        if code >= 400:
            raise KsefAuthError(
                code,
                f"Authentication failed: {status.status.description}",
            )
        time.sleep(poll_interval)

    raise KsefAuthError(0, f"Authentication polling timed out after {max_attempts} attempts")


def redeem_token(http: HttpTransport, auth_token: str) -> AuthenticationTokensResponse:
    """``POST /auth/token/redeem`` — exchange authenticationToken for access + refresh tokens.

    The *auth_token* (JWT from :func:`init_token_auth`) is sent as Bearer.
    """
    http.set_access_token(auth_token)
    try:
        return http.post(
            "/auth/token/redeem",
            response_model=AuthenticationTokensResponse,
        )  # type: ignore[return-value]
    finally:
        http.clear_access_token()


def refresh_access_token(http: HttpTransport, refresh_token: str) -> AuthenticationTokenRefreshResponse:
    """``POST /auth/token/refresh`` — obtain a new access token using a refresh token."""
    # The refresh token is sent as Bearer
    http.set_access_token(refresh_token)
    try:
        return http.post(
            "/auth/token/refresh",
            response_model=AuthenticationTokenRefreshResponse,
        )  # type: ignore[return-value]
    finally:
        # Restore after refresh attempt — caller sets the new access token
        http.clear_access_token()
