from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ksef2.domain.models import KSeFBaseModel


def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


class ChallengeResponse(KSeFBaseModel):
    """Response from ``POST /auth/challenge``."""

    challenge: str
    timestamp: datetime
    timestamp_ms: int


class AuthInitResponse(KSeFBaseModel):
    """Response from ``POST /auth/ksef-token`` or ``POST /auth/xades-signature``."""

    reference_number: str
    authentication_token: str
    authentication_token_valid_until: datetime


class AuthTokens(KSeFBaseModel):
    """Tokens returned after successful authentication (redeem)."""

    access_token: str
    access_token_valid_until: datetime
    refresh_token: str
    refresh_token_valid_until: datetime


class RefreshedToken(KSeFBaseModel):
    """Response from ``POST /auth/token/refresh``."""

    access_token: str
    access_token_valid_until: datetime


class AuthStatusResponse(KSeFBaseModel):
    """Response from ``GET /auth/{referenceNumber}``."""

    start_date: datetime
    authentication_method: str
    status_code: int
    status_description: str | None = None


class PublicKeyCertificateInfo(KSeFBaseModel):
    """Domain representation of a public key certificate."""

    certificate: str
    valid_from: datetime
    valid_to: datetime
    usage: list[str]


@dataclass(frozen=True)
class SessionContext:
    """Immutable DTO capturing the state of an open KSeF session.

    Supports encrypted serialization using Fernet + PBKDF2HMAC for
    password-based protection. This allows safe persistence of session
    state (e.g. in Redis) across process boundaries.
    """

    reference_number: str
    aes_key: bytes
    iv: bytes
    access_token: str
    environment: str

    def to_json(self, password: str) -> str:
        """Serialize to encrypted JSON.

        Uses PBKDF2HMAC (SHA256, 480_000 iterations) for key derivation
        and Fernet (AES-128-CBC + HMAC-SHA256) for encryption.
        """
        salt = os.urandom(16)
        key = _derive_key(password, salt)
        payload = json.dumps(
            {
                "reference_number": self.reference_number,
                "aes_key": base64.b64encode(self.aes_key).decode(),
                "iv": base64.b64encode(self.iv).decode(),
                "access_token": self.access_token,
                "environment": self.environment,
            }
        ).encode()
        encrypted = Fernet(key).encrypt(payload)
        return json.dumps(
            {
                "salt": base64.b64encode(salt).decode(),
                "data": encrypted.decode(),
            }
        )

    @classmethod
    def from_json(cls, json_str: str, password: str) -> SessionContext:
        """Deserialize from encrypted JSON."""
        envelope = json.loads(json_str)
        salt = base64.b64decode(envelope["salt"])
        key = _derive_key(password, salt)
        decrypted = Fernet(key).decrypt(envelope["data"].encode())
        fields = json.loads(decrypted)
        return cls(
            reference_number=fields["reference_number"],
            aes_key=base64.b64decode(fields["aes_key"]),
            iv=base64.b64decode(fields["iv"]),
            access_token=fields["access_token"],
            environment=fields["environment"],
        )
