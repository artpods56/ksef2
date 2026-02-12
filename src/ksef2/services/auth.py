from __future__ import annotations

import time
from typing import TYPE_CHECKING, final

from ksef2.clients.encryption import EncryptionClient
from ksef2.core import exceptions
from ksef2.core.crypto import encrypt_token
from ksef2.core.exceptions import KSeFAuthError
from ksef2.core import middleware
from ksef2.core.stores import CertificateStore
from ksef2.domain.models.auth import (
    AuthTokens,
    ContextIdentifierType,
    RefreshedToken,
)
from ksef2.domain.models.encryption import CertUsage
from ksef2.endpoints.auth import (
    AuthStatusEndpoint,
    ChallengeEndpoint,
    RedeemTokenEndpoint,
    RefreshTokenEndpoint,
    TokenAuthEndpoint,
    XAdESAuthEndpoint,
)
from ksef2.infra.mappers.auth import (
    AuthInitMapper,
    AuthStatusMapper,
    AuthTokensMapper,
    ChallengeMapper,
    RefreshTokenMapper,
)

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
    from cryptography.x509 import Certificate


@final
class AuthService:
    def __init__(
        self,
        transport: middleware.KSeFProtocol,
        certificate_store: CertificateStore,
    ) -> None:
        self._transport = transport
        self._certificate_store = certificate_store
        self._certificates = EncryptionClient(transport)
        self._challenge_ep = ChallengeEndpoint(transport)
        self._token_auth_ep = TokenAuthEndpoint(transport)
        self._xades_auth_ep = XAdESAuthEndpoint(transport)
        self._status_ep = AuthStatusEndpoint(transport)
        self._redeem_ep = RedeemTokenEndpoint(transport)
        self._refresh_ep = RefreshTokenEndpoint(transport)

    def authenticate_token(
        self,
        *,
        ksef_token: str,
        nip: str,
        context_type: ContextIdentifierType = ContextIdentifierType.NIP,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> AuthTokens:
        self._ensure_certificates()

        challenge = ChallengeMapper.map_response(self._challenge_ep.send())

        cert = self._certificate_store.get_valid(CertUsage.KSEF_TOKEN_ENCRYPTION)

        if not cert:
            raise exceptions.NoCertificateAvailableError(
                "No valid certificate for KsefTokenEncryption found."
            )

        encrypted = encrypt_token(
            ksef_token, str(challenge.timestamp_ms), cert.certificate
        )

        body = AuthInitMapper.map_token_request(
            challenge.challenge, context_type, nip, encrypted
        )
        init_resp = AuthInitMapper.map_response(
            self._token_auth_ep.send(body.model_dump())
        )

        self._poll_until_authenticated(
            auth_token=init_resp.authentication_token.token,
            reference_number=init_resp.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        return self._redeem(init_resp.authentication_token.token)

    def authenticate_xades(
        self,
        *,
        nip: str,
        cert: Certificate,
        private_key: RSAPrivateKey,
        verify_chain: bool = False,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> AuthTokens:
        from ksef2.core.xades import build_auth_token_request_xml, sign_xades

        challenge = ChallengeMapper.map_response(self._challenge_ep.send())

        xml_bytes = build_auth_token_request_xml(challenge.challenge, nip)
        signed_xml = sign_xades(xml_bytes, cert, private_key)

        init_resp = AuthInitMapper.map_response(
            self._xades_auth_ep.send(signed_xml, verify_chain=verify_chain)
        )

        self._poll_until_authenticated(
            auth_token=init_resp.authentication_token.token,
            reference_number=init_resp.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        return self._redeem(init_resp.authentication_token.token)

    def refresh(self, *, refresh_token: str) -> RefreshedToken:
        return RefreshTokenMapper.map_response(
            self._refresh_ep.send(bearer_token=refresh_token)
        )

    def _ensure_certificates(self) -> None:
        if not self._certificate_store.all():
            self._certificate_store.load(self._certificates.get_certificates())

    def _poll_until_authenticated(
        self,
        *,
        auth_token: str,
        reference_number: str,
        poll_interval: float,
        max_attempts: int,
    ) -> None:
        for _ in range(max_attempts):
            status = AuthStatusMapper.map_response(
                self._status_ep.send(
                    bearer_token=auth_token,
                    reference_number=reference_number,
                )
            )
            if status.status_code == 200:
                return
            if status.status_code >= 400:
                raise KSeFAuthError(
                    status_code=status.status_code,
                    message=f"Authentication failed: {status.status_description}",
                )
            time.sleep(poll_interval)

        raise KSeFAuthError(
            status_code=408,
            message="Authentication polling timed out.",
        )

    def _redeem(self, auth_token: str) -> AuthTokens:
        return AuthTokensMapper.map_response(
            self._redeem_ep.send(bearer_token=auth_token)
        )
