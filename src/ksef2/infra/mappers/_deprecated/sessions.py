from __future__ import annotations

from ksef2.domain.models._deprecated.sessions import (
    SessionInvoiceStatus,
    SessionInvoicesResponse,
    SessionStatus,
)
from ksef2.infra.schema import model as spec


class SessionStatusMapper:
    @staticmethod
    def map_response(r: spec.SessionStatusResponse) -> SessionStatus:
        return SessionStatus(
            status_code=r.status.code,
            status_description=r.status.description,
            date_created=r.dateCreated,
            date_updated=r.dateUpdated,
            valid_until=r.validUntil,
        )


class SessionInvoicesMapper:
    @staticmethod
    def map_response(r: spec.SessionInvoicesResponse) -> SessionInvoicesResponse:
        return SessionInvoicesResponse(
            invoices=[
                SessionInvoiceStatus(
                    reference_number=inv.referenceNumber,
                    ksef_number=inv.ksefNumber,
                    status_code=inv.status.code,
                    status_description=inv.status.description,
                )
                for inv in r.invoices
            ],
            continuation_token=r.continuationToken,
        )
