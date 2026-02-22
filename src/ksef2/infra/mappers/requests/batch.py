"""Mapper for batch session API requests and responses."""

import base64

from ksef2.domain.models import FormSchema
from ksef2.domain.models.batch import (
    BatchFileInfo,
    OpenBatchSessionResponse,
    PartUploadRequest,
)
from ksef2.infra.schema.api import spec as spec


class BatchSessionMapper:
    """Maps batch session API requests and responses to domain models."""

    @staticmethod
    def map_request(
        encrypted_key: bytes,
        iv: bytes,
        batch_file: BatchFileInfo,
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
    ) -> spec.OpenBatchSessionRequest:
        """Map domain models to API request.

        Args:
            encrypted_key: RSA-encrypted AES key, Base64 encoded.
            iv: Initialization vector for AES encryption.
            batch_file: Information about the batch file.
            form_code: Invoice schema to use. Defaults to FA3.
            offline_mode: Whether offline invoicing mode is declared.

        Returns:
            OpenBatchSessionRequest for the API.
        """
        encryption = spec.EncryptionInfo(
            encryptedSymmetricKey=base64.b64encode(encrypted_key).decode(),
            initializationVector=base64.b64encode(iv).decode(),
        )

        file_parts = [
            spec.BatchFilePartInfo(
                ordinalNumber=part.ordinal_number,
                fileSize=part.file_size,
                fileHash=part.file_hash,
            )
            for part in batch_file.parts
        ]

        batch_file_info = spec.BatchFileInfo(
            fileSize=batch_file.file_size,
            fileHash=batch_file.file_hash,
            fileParts=file_parts,
        )

        return spec.OpenBatchSessionRequest(
            formCode=spec.FormCode(
                value=form_code.schema_value,
                systemCode=form_code.system_code,
                schemaVersion=form_code.schema_version,
            ),
            batchFile=batch_file_info,
            encryption=encryption,
            offlineMode=offline_mode,
        )

    @staticmethod
    def map_part_upload_request(
        part: spec.PartUploadRequest,
    ) -> PartUploadRequest:
        """Map a single part upload request from spec to domain model."""
        return PartUploadRequest(
            ordinal_number=part.ordinalNumber,
            method=part.method,
            url=str(part.url),
            headers=part.headers,
        )

    @staticmethod
    def map_response(
        response: spec.OpenBatchSessionResponse,
    ) -> OpenBatchSessionResponse:
        """Map API response to domain model.

        Args:
            response: API response from opening batch session.

        Returns:
            OpenBatchSessionResponse domain model.
        """
        return OpenBatchSessionResponse(
            reference_number=response.referenceNumber,
            part_upload_requests=[
                BatchSessionMapper.map_part_upload_request(part)
                for part in response.partUploadRequests
            ],
        )
