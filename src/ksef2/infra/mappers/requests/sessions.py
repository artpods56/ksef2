import base64
from typing import NamedTuple

from pydantic import AwareDatetime

from ksef2.domain.models import FormSchema
from ksef2.domain.models.session import (
    ListSessionsResponse,
    SessionSummary,
    StatusInfo,
)
from ksef2.infra.schema.api import spec as spec


class OpenSessionData(NamedTuple):
    reference_number: str
    valid_until: AwareDatetime


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


class QuerySessionsMapper:
    """Handles mapping of query sessions response to domain model.

    Note:
        The endpoint doesnt require request body so we are not mapping it.
    """

    @staticmethod
    def _map_session_items(item: spec.SessionsQueryResponseItem) -> SessionSummary:
        return SessionSummary(
            reference_number=item.referenceNumber,
            status=StatusInfo(
                code=item.status.code,
                description=item.status.description,
                details=list(item.status.details or []),
            ),
            date_created=item.dateCreated,
            date_updated=item.dateUpdated,
            total_invoice_count=item.totalInvoiceCount,
            successful_invoice_count=item.successfulInvoiceCount,
            failed_invoice_count=item.failedInvoiceCount,
        )

    @classmethod
    def map_response(cls, response: spec.SessionsQueryResponse) -> ListSessionsResponse:
        return ListSessionsResponse(
            continuation_token=response.continuationToken,
            sessions=[cls._map_session_items(item=item) for item in response.sessions],
        )
