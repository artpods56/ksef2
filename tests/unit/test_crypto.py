"""Tests for crypto utility functions."""

from __future__ import annotations

import base64
import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from ksef2.core.crypto import (
    encrypt_invoice,
    generate_session_key,
    sha256_b64,
)


class TestGenerateSessionKey:
    def test_aes_key_is_32_bytes(self) -> None:
        aes_key, _ = generate_session_key()
        assert len(aes_key) == 32

    def test_iv_is_16_bytes(self) -> None:
        _, iv = generate_session_key()
        assert len(iv) == 16

    def test_keys_are_random(self) -> None:
        a = generate_session_key()
        b = generate_session_key()
        assert a != b


class TestEncryptInvoice:
    def test_roundtrip_decrypt(self) -> None:
        aes_key, iv = generate_session_key()
        plaintext = b"<Invoice>test</Invoice>"

        ciphertext = encrypt_invoice(plaintext, aes_key, iv)

        # Decrypt manually to verify
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        # Remove PKCS#7 padding
        pad_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-pad_len]

        assert decrypted == plaintext

    def test_output_is_block_aligned(self) -> None:
        aes_key, iv = generate_session_key()
        plaintext = b"x" * 13  # not block-aligned

        ciphertext = encrypt_invoice(plaintext, aes_key, iv)

        assert len(ciphertext) % 16 == 0

    def test_output_length_for_exact_block(self) -> None:
        aes_key, iv = generate_session_key()
        plaintext = b"x" * 16  # exactly one block

        ciphertext = encrypt_invoice(plaintext, aes_key, iv)

        # PKCS#7 adds a full block of padding when input is block-aligned
        assert len(ciphertext) == 32

    def test_different_iv_produces_different_ciphertext(self) -> None:
        aes_key = b"\x00" * 32
        iv_a = b"\x01" * 16
        iv_b = b"\x02" * 16
        plaintext = b"<Invoice/>"

        ct_a = encrypt_invoice(plaintext, aes_key, iv_a)
        ct_b = encrypt_invoice(plaintext, aes_key, iv_b)

        assert ct_a != ct_b


class TestSha256B64:
    def test_known_hash(self) -> None:
        data = b"hello"
        expected = base64.b64encode(hashlib.sha256(data).digest()).decode()

        assert sha256_b64(data) == expected

    def test_empty_input(self) -> None:
        expected = base64.b64encode(hashlib.sha256(b"").digest()).decode()

        assert sha256_b64(b"") == expected

    def test_output_is_44_chars(self) -> None:
        # SHA-256 = 32 bytes -> Base64 = 44 characters (with padding)
        result = sha256_b64(b"anything")
        assert len(result) == 44
