from __future__ import annotations

import base64

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import pytest

from ksef_sdk._crypto import (
    encrypt_invoice,
    encrypt_symmetric_key,
    encrypt_token,
    generate_session_key,
    select_certificate,
    sha256_b64,
)
from ksef_sdk.exceptions import KsefEncryptionError


class TestEncryptToken:
    def test_roundtrip(self, rsa_key_pair, self_signed_cert_b64):
        token = "my-ksef-token"
        timestamp_ms = "1735689600000"

        encrypted_b64 = encrypt_token(token, timestamp_ms, self_signed_cert_b64)
        ciphertext = base64.b64decode(encrypted_b64)

        # Decrypt with the private key to verify
        plaintext = rsa_key_pair.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        assert plaintext == b"my-ksef-token|1735689600000"

    def test_bad_cert_raises(self):
        with pytest.raises(KsefEncryptionError, match="Failed to load public key"):
            encrypt_token("token", "ts", "not-valid-base64-cert")


class TestEncryptSymmetricKey:
    def test_roundtrip(self, rsa_key_pair, self_signed_cert_b64):
        key = b"0" * 32
        encrypted_b64 = encrypt_symmetric_key(key, self_signed_cert_b64)
        ciphertext = base64.b64decode(encrypted_b64)

        plaintext = rsa_key_pair.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        assert plaintext == key


class TestGenerateSessionKey:
    def test_lengths(self):
        key, iv = generate_session_key()
        assert len(key) == 32
        assert len(iv) == 16

    def test_randomness(self):
        k1, iv1 = generate_session_key()
        k2, iv2 = generate_session_key()
        assert k1 != k2
        assert iv1 != iv2


class TestEncryptInvoice:
    def test_output_is_block_aligned(self):
        key, iv = generate_session_key()
        data = b"<invoice>test</invoice>"
        ciphertext = encrypt_invoice(data, key, iv)
        assert len(ciphertext) % 16 == 0

    def test_roundtrip(self):
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

        key, iv = generate_session_key()
        plaintext = b"<invoice>test data here</invoice>"
        ciphertext = encrypt_invoice(plaintext, key, iv)

        # Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove PKCS#7 padding
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        assert decrypted == plaintext


class TestSha256B64:
    def test_known_value(self):
        # SHA-256 of empty string is well-known
        result = sha256_b64(b"")
        expected = base64.b64encode(
            bytes.fromhex(
                "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            )
        ).decode()
        assert result == expected


class TestSelectCertificate:
    def test_finds_matching(self, sample_certificates):
        cert = select_certificate(sample_certificates, "KsefTokenEncryption")
        assert "KsefTokenEncryption" in cert.usage

    def test_raises_on_missing(self, sample_certificates):
        with pytest.raises(KsefEncryptionError, match="No certificate found"):
            select_certificate(sample_certificates, "NonExistent")
