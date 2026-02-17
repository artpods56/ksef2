"""Integration tests for batch session endpoints."""

import pytest

from ksef2 import Client
from ksef2.domain.models.auth import AuthTokens
from ksef2.domain.models.batch import (
    BatchFileInfo,
    BatchFilePart,
    PartUploadRequest,
)
from ksef2.domain.models import BatchSessionState
from ksef2.domain.models.session import FormSchema


@pytest.mark.integration
class TestBatchSession:
    """Tests for batch session endpoints.

    These tests verify the batch session lifecycle:
    - POST /sessions/batch (open batch session)
    - POST /sessions/batch/{referenceNumber}/close (close batch session)
    """

    @pytest.mark.skip(
        reason="Batch session requires valid batch file - complex setup needed"
    )
    def test_open_batch_session(
        self,
        xades_authenticated_context: tuple[Client, AuthTokens],
    ) -> None:
        """Test opening a batch session.

        Note: This test is skipped by default because it requires:
        1. A properly prepared and encrypted batch file
        2. Valid file hashes (SHA-256)
        3. The file to be uploaded to the returned URLs

        The test demonstrates the API structure but would fail without
        real batch file preparation.
        """
        client, tokens = xades_authenticated_context

        # Example batch file info - would fail validation without real data
        batch_file = BatchFileInfo(
            file_size=16037,
            file_hash="WO86CC+1Lef11wEosItld/NPwxGN8tobOMLqk9PQjgs=",
            parts=[
                BatchFilePart(
                    ordinal_number=1,
                    file_size=16048,
                    file_hash="23ZyDAN0H/+yhC/En2xbNfF0tajAWSfejDaXD7fc2AE=",
                )
            ],
        )

        # This would open a batch session
        batch_session = client.sessions.open_batch(
            access_token=tokens.access_token.token,
            batch_file=batch_file,
        )

        # Verify response structure
        assert batch_session.reference_number
        assert len(batch_session.reference_number) == 36
        assert batch_session.part_upload_requests
        assert len(batch_session.part_upload_requests) == 1

        # Verify upload request structure
        upload_req = batch_session.part_upload_requests[0]
        assert upload_req.ordinal_number == 1
        assert upload_req.method == "PUT"
        assert upload_req.url
        assert upload_req.headers

    def test_batch_file_info_model(self) -> None:
        """Test that BatchFileInfo model validates correctly."""
        batch_file = BatchFileInfo(
            file_size=1000,
            file_hash="WO86CC+1Lef11wEosItld/NPwxGN8tobOMLqk9PQjgs=",
            parts=[
                BatchFilePart(
                    ordinal_number=1,
                    file_size=1000,
                    file_hash="23ZyDAN0H/+yhC/En2xbNfF0tajAWSfejDaXD7fc2AE=",
                )
            ],
        )

        assert batch_file.file_size == 1000
        assert len(batch_file.parts) == 1
        assert batch_file.parts[0].ordinal_number == 1

    def test_batch_file_info_multiple_parts(self) -> None:
        """Test BatchFileInfo with multiple parts."""
        parts = [
            BatchFilePart(
                ordinal_number=i,
                file_size=1000 * i,
                file_hash=f"hash{i}",
            )
            for i in range(1, 6)
        ]

        batch_file = BatchFileInfo(
            file_size=15000,
            file_hash="totalhash",
            parts=parts,
        )

        assert len(batch_file.parts) == 5
        assert batch_file.parts[0].ordinal_number == 1
        assert batch_file.parts[4].ordinal_number == 5

    def test_batch_session_state_serialization(self) -> None:
        """Test that BatchSessionState can be serialized and restored."""
        upload_requests = [
            PartUploadRequest(
                ordinal_number=1,
                method="PUT",
                url="https://example.com/upload/1",
                headers={"x-ms-blob-type": "BlockBlob"},
            )
        ]

        state = BatchSessionState.from_encoded(
            reference_number="20250217-SB-TEST123456-ABCDEF1234-E9",
            aes_key=b"0123456789abcdef0123456789abcdef",
            iv=b"0123456789abcdef",
            access_token="test-access-token",
            form_code=FormSchema.FA3,
            part_upload_requests=upload_requests,
        )

        # Serialize to JSON
        state_json = state.model_dump_json()

        # Restore from JSON
        restored = BatchSessionState.model_validate_json(state_json)

        assert restored.reference_number == state.reference_number
        assert restored.access_token == state.access_token
        assert restored.form_code == FormSchema.FA3
        assert len(restored.part_upload_requests) == 1
        assert restored.part_upload_requests[0].url == "https://example.com/upload/1"

        # Verify bytes can be decoded
        assert restored.get_aes_key_bytes() == b"0123456789abcdef0123456789abcdef"
        assert restored.get_iv_bytes() == b"0123456789abcdef"
