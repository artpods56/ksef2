import base64
from typing import NamedTuple

from pydantic import AwareDatetime

from ksef2.domain.models import FormSchema
from ksef2.infra.schema.api import spec as spec


class OpenSessionData(NamedTuple):
    reference_number: str
    valid_until: AwareDatetime


class OpenOnlineSessionMapper:
    @staticmethod
    def map_request(
        encrypted_key: str,
        iv: bytes,
        form_code: FormSchema = FormSchema.FA3,
    ) -> spec.OpenOnlineSessionRequest:
        encryption = spec.EncryptionInfo(
            encryptedSymmetricKey=encrypted_key,
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
