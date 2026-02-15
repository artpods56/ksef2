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
        encrypted_key: bytes,
        iv: bytes,
        form_code: FormSchema = FormSchema.FA3,
    ) -> spec.OpenOnlineSessionRequest:
        encryption = spec.EncryptionInfo(
            encryptedSymmetricKey=base64.b64encode(encrypted_key).decode(),
            initializationVector=base64.b64encode(iv).decode(),
        )
        return spec.OpenOnlineSessionRequest(
            formCode=spec.FormCode(
                value=form_code.schema_value,
                systemCode=form_code.system_code,
                schemaVersion=form_code.schema_version,
            ),
            encryption=encryption,
        )

    @staticmethod
    def map_response(
        request: spec.OpenOnlineSessionResponse,
    ) -> OpenSessionData:
        return OpenSessionData(
            reference_number=request.referenceNumber,
            valid_until=request.validUntil,
        )
