"""Tests for mapper classes."""

from __future__ import annotations

import base64
from datetime import datetime, timezone

from ksef2.core.crypto import sha256_b64
from ksef2.domain.models.session import FormSchema
from ksef2.infra.mappers.encryption import PublicKeyCertificateMapper
from ksef2.infra.mappers.invoices import SendInvoiceMapper
from ksef2.infra.mappers.session import OpenOnlineSessionMapper
from ksef2.infra.schema.api import spec as spec


class TestOpenOnlineSessionMapper:
    def test_map_request_form_code(self) -> None:
        result = OpenOnlineSessionMapper.map_request(
            encrypted_key=b"abc123==",
            iv=b"\x00" * 16,
            form_code=FormSchema.FA3,
        )

        assert isinstance(result, spec.OpenOnlineSessionRequest)
        assert result.formCode.systemCode == "FA (3)"
        assert result.formCode.schemaVersion == "1-0E"
        assert result.formCode.value == "FA"

    def test_map_request_encryption_info(self) -> None:
        iv = b"\x01\x02\x03\x04" * 4
        result = OpenOnlineSessionMapper.map_request(
            encrypted_key=b"key==",
            iv=iv,
        )

        assert (
            result.encryption.encryptedSymmetricKey
            == base64.b64encode(b"key==").decode()
        )
        assert result.encryption.initializationVector == base64.b64encode(iv).decode()

    def test_map_request_pef_schema(self) -> None:
        result = OpenOnlineSessionMapper.map_request(
            encrypted_key=b"k",
            iv=b"\x00" * 16,
            form_code=FormSchema.PEF3,
        )

        assert result.formCode.systemCode == "PEF (3)"
        assert result.formCode.schemaVersion == "2-1"
        assert result.formCode.value == "PEF"

    def test_map_response(self) -> None:
        valid = datetime(2025, 7, 11, 12, 0, 0, tzinfo=timezone.utc)
        dto = spec.OpenOnlineSessionResponse(
            referenceNumber="20250625-SO-2C3E6C8000-B675CF5D68-07",
            validUntil=valid,
        )

        result = OpenOnlineSessionMapper.map_response(dto)

        assert result.reference_number == "20250625-SO-2C3E6C8000-B675CF5D68-07"
        assert result.valid_until == valid


class TestSendInvoiceMapper:
    SAMPLE_XML = b"<Invoice><Total>100.00</Total></Invoice>"

    def test_map_request_sizes(self) -> None:
        encrypted = b"\x00" * 48  # fake encrypted content
        result = SendInvoiceMapper.map_request(self.SAMPLE_XML, encrypted)

        assert result.invoiceSize == len(self.SAMPLE_XML)
        assert result.encryptedInvoiceSize == len(encrypted)

    def test_map_request_hashes(self) -> None:
        encrypted = b"\xff" * 32
        result = SendInvoiceMapper.map_request(self.SAMPLE_XML, encrypted)

        assert result.invoiceHash == sha256_b64(self.SAMPLE_XML)
        assert result.encryptedInvoiceHash == sha256_b64(encrypted)

    def test_map_request_encrypted_content_is_base64(self) -> None:
        encrypted = b"encrypted_data_here"
        result = SendInvoiceMapper.map_request(self.SAMPLE_XML, encrypted)

        decoded = base64.b64decode(result.encryptedInvoiceContent)
        assert decoded == encrypted

    def test_map_response(self) -> None:
        dto = spec.SendInvoiceResponse(
            referenceNumber="20250625-EE-319D7EE000-B67F415CDC-2C",
        )

        result = SendInvoiceMapper.map_response(dto)

        assert result.reference_number == "20250625-EE-319D7EE000-B67F415CDC-2C"


class TestPublicKeyCertificateMapper:
    def test_maps_fields_correctly(self) -> None:
        now = datetime(2025, 6, 1, tzinfo=timezone.utc)
        later = datetime(2025, 12, 1, tzinfo=timezone.utc)
        dto = spec.PublicKeyCertificate.model_construct(
            certificate="AAAA",
            validFrom=now,
            validTo=later,
            usage=["SymmetricKeyEncryption"],
        )

        result = PublicKeyCertificateMapper.map_response([dto])

        assert len(result) == 1
        cert = result[0]
        assert cert.certificate == "AAAA"
        assert cert.valid_from == now
        assert cert.valid_to == later

    def test_maps_multiple_usages(self) -> None:
        from ksef2.domain.models.encryption import CertUsage

        dto = spec.PublicKeyCertificate.model_construct(
            certificate="BB",
            validFrom=datetime(2025, 1, 1, tzinfo=timezone.utc),
            validTo=datetime(2026, 1, 1, tzinfo=timezone.utc),
            usage=["SymmetricKeyEncryption", "KsefTokenEncryption"],
        )

        result = PublicKeyCertificateMapper.map_response([dto])

        assert CertUsage.SYMMETRIC_KEY_ENCRYPTION in result[0].usage
        assert CertUsage.KSEF_TOKEN_ENCRYPTION in result[0].usage

    def test_maps_empty_list(self) -> None:
        assert PublicKeyCertificateMapper.map_response([]) == []
