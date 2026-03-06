from collections.abc import Callable
from typing import final

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509 import Certificate
from httpx import Response
from tenacity import (
    RetryError,
    retry,
    retry_if_result,
    stop_after_attempt,
    wait_fixed,
)

from ksef2.core.xades import generate_test_certificate
from ksef2.clients.authenticated import AuthenticatedClient
from ksef2.clients.encryption import EncryptionClient
from ksef2.config import Environment
from ksef2.core import exceptions
from ksef2.core.crypto import encrypt_token
from ksef2.core.exceptions import KSeFAuthError
from ksef2.core.protocols import Middleware
from ksef2.core.stores import CertificateStore
from ksef2.domain.models.auth import (
    AuthOperationStatus,
    AuthTokens,
    ContextIdentifierType,
    InitTokenAuthenticationRequest,
    RefreshedToken,
)
from ksef2.endpoints.auth import AuthEndpoints
from ksef2.infra.mappers.auth import from_spec, to_spec


@final
class AuthClient:
    def __init__(
        self,
        transport: Middleware,
        certificate_store: CertificateStore,
        environment: Environment = Environment.PRODUCTION,
    ) -> None:
        self._transport = transport
        self._certificate_store = certificate_store
        self._environment = environment
        self._certificates = EncryptionClient(transport)
        self._auth_ep = AuthEndpoints(transport)

    def with_token(
        self,
        *,
        ksef_token: str,
        nip: str,
        context_type: ContextIdentifierType = "nip",
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> AuthenticatedClient:
        self._ensure_certificates()

        challenge = from_spec(self._auth_ep.challenge())
        try:
            cert = self._certificate_store.get_valid("ksef_token_encryption")
        except exceptions.NoCertificateAvailableError as exc:
            raise exceptions.NoCertificateAvailableError(
                "No valid certificate for KsefTokenEncryption found."
            ) from exc

        encrypted = encrypt_token(
            ksef_token, str(challenge.timestamp_ms), cert.certificate
        )
        request = InitTokenAuthenticationRequest(
            challenge=challenge.challenge,
            context_type=context_type,
            context_value=nip,
            encrypted_token=encrypted,
        )
        init_resp = from_spec(self._auth_ep.token_auth(body=to_spec(request)))

        self._poll_until_authenticated(
            auth_token=init_resp.authentication_token.token,
            reference_number=init_resp.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        return self._build_authenticated_client(
            auth_tokens=self._redeem(init_resp.authentication_token.token)
        )

    def with_xades(
        self,
        *,
        nip: str,
        cert: Certificate,
        private_key: RSAPrivateKey,
        verify_chain: bool = False,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> AuthenticatedClient:
        from ksef2.core.xades import build_auth_token_request_xml, sign_xades

        challenge = from_spec(self._auth_ep.challenge())
        xml_bytes = build_auth_token_request_xml(challenge.challenge, nip)
        signed_xml = sign_xades(xml_bytes, cert, private_key)

        init_resp = from_spec(
            self._auth_ep.xades_auth(signed_xml, verify_chain=verify_chain)
        )

        self._poll_until_authenticated(
            auth_token=init_resp.authentication_token.token,
            reference_number=init_resp.reference_number,
            poll_interval=poll_interval,
            max_attempts=max_poll_attempts,
        )

        return self._build_authenticated_client(
            auth_tokens=self._redeem(init_resp.authentication_token.token)
        )

    def with_test_certificate(
        self,
        *,
        nip: str,
        verify_chain: bool = False,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 60,
    ) -> AuthenticatedClient:
        if self._environment is not Environment.TEST:
            raise exceptions.KSeFUnsupportedEnvironmentError(
                "with_test_certificate() is only available for Environment.TEST"
            )

        cert, private_key = generate_test_certificate(nip)
        return self.with_xades(
            nip=nip,
            cert=cert,
            private_key=private_key,
            verify_chain=verify_chain,
            poll_interval=poll_interval,
            max_poll_attempts=max_poll_attempts,
        )

    def refresh(self, *, refresh_token: str) -> RefreshedToken:
        return from_spec(self._auth_ep.refresh_token(bearer_token=refresh_token))

    def _build_authenticated_client(
        self, *, auth_tokens: AuthTokens
    ) -> AuthenticatedClient:
        return AuthenticatedClient(
            transport=self._transport,
            auth_tokens=auth_tokens,
            certificate_store=self._certificate_store,
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

        retry_predicate: Callable[[Response], bool] = lambda resp: resp.status_code < 200
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_fixed(poll_interval),
            retry=retry_if_result(retry_predicate),
            reraise=True,
        )
        def _poll() -> AuthOperationStatus:
            status = from_spec(
                self._auth_ep.auth_status(
                    bearer_token=auth_token,
                    reference_number=reference_number,
                )
            )
            if status.status_code >= 400:
                raise KSeFAuthError(
                    status_code=status.status_code,
                    message=f"Authentication failed: {status.status_description}",
                )
            return status

        try:
            _ = _poll()
        except RetryError as exc:
            raise KSeFAuthError(
                status_code=408,
                message="Authentication polling timed out.",
            ) from exc

    def _redeem(self, auth_token: str) -> AuthTokens:
        return from_spec(self._auth_ep.redeem_token(bearer_token=auth_token))
