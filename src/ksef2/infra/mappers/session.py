import base64
from datetime import datetime
from typing import NamedTuple

from ksef2.domain.models import FormSchema
from ksef2.infra.schema.api import spec as spec


class OpenSessionData(NamedTuple):
    reference_number: str
    valid_until: datetime


class OpenOnlineSessionMapper:
    @staticmethod
    def map_request(
        encrypted_key: str,
        iv: bytes,
        form_code: FormSchema = FormSchema.FA3,
    ) -> spec.OpenOnlineSessionRequest:
        # Use model_construct to bypass Base64Str validation — the encrypted
        # key and IV are raw Base64 that Pydantic would try to decode as UTF-8.
        return spec.OpenOnlineSessionRequest.model_construct(
            formCode=spec.FormCode(
                value=form_code.schema_value,
                systemCode=form_code.system_code,
                schemaVersion=form_code.schema_version,
            ),
            encryption=spec.EncryptionInfo.model_construct(
                encryptedSymmetricKey=encrypted_key,
                initializationVector=base64.b64encode(iv).decode(),
            ),
        )

    @staticmethod
    def map_response(
        request: spec.OpenOnlineSessionResponse,
    ) -> OpenSessionData:
        return OpenSessionData(
            reference_number=request.referenceNumber,
            valid_until=request.validUntil,
        )
