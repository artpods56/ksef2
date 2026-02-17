"""Domain models for batch session operations."""

from __future__ import annotations

import base64

from ksef2.domain.models.base import KSeFBaseModel
from ksef2.domain.models.session import BaseSessionState, FormSchema


class BatchFilePart(KSeFBaseModel):
    """Information about a part of the batch file."""

    ordinal_number: int
    """Sequential number of the file part (1-indexed)."""

    file_size: int
    """Size of the encrypted file part in bytes."""

    file_hash: str
    """SHA-256 hash of the encrypted file part, Base64 encoded."""


class BatchFileInfo(KSeFBaseModel):
    """Information about the batch file being uploaded."""

    file_size: int
    """Total size of the batch file in bytes. Max 5GB."""

    file_hash: str
    """SHA-256 hash of the batch file, Base64 encoded."""

    parts: list[BatchFilePart]
    """List of file parts. Max 50 parts, each max 100MB before encryption."""


class PartUploadRequest(KSeFBaseModel):
    """Upload endpoint information for a batch session part."""

    ordinal_number: int
    """Sequential number of the file part (1-indexed)."""

    method: str
    """HTTP method to use for uploading (typically PUT)."""

    url: str
    """URL to upload the file part to."""

    headers: dict[str, str | None]
    """Headers to include in the upload request."""


class OpenBatchSessionResponse(KSeFBaseModel):
    """Response from opening a batch session."""

    reference_number: str
    """Reference number of the batch session."""

    part_upload_requests: list[PartUploadRequest]
    """Upload instructions for each file part."""


class BatchSessionState(BaseSessionState):
    """Serializable state of a batch session.

    This class holds all information needed to resume a batch session
    or to upload file parts. Can be serialized to JSON for persistence.

    Inherits common session fields from BaseSessionState:
    - reference_number, aes_key, iv, access_token, form_code
    - get_aes_key_bytes(), get_iv_bytes() helper methods
    """

    part_upload_requests: list[PartUploadRequest]
    """Upload instructions for each file part."""

    @classmethod
    def from_encoded(
        cls,
        reference_number: str,
        aes_key: bytes,
        iv: bytes,
        access_token: str,
        form_code: FormSchema,
        part_upload_requests: list[PartUploadRequest],
    ) -> BatchSessionState:
        """Create state from raw bytes (aes_key, iv).

        Args:
            reference_number: Batch session reference number.
            aes_key: Raw AES key bytes.
            iv: Raw initialization vector bytes.
            access_token: Bearer token for authentication.
            form_code: Invoice schema for this session.
            part_upload_requests: Upload instructions for file parts.

        Returns:
            BatchSessionState with Base64-encoded key and IV.
        """
        return cls(
            reference_number=reference_number,
            aes_key=base64.b64encode(aes_key).decode(),
            iv=base64.b64encode(iv).decode(),
            access_token=access_token,
            form_code=form_code,
            part_upload_requests=part_upload_requests,
        )
