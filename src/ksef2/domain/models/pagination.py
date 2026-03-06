from datetime import datetime
from typing import Self

from pydantic import Field, BaseModel

from ksef2.domain.models.base import KSeFBaseParams
from ksef2.domain.models.invoices import SortOrder
from ksef2.domain.models.session import (
    SessionStatusEnum,
    SessionTypeEnum,
    SessionStatus,
)
from ksef2.domain.models.tokens import TokenAuthorIdentifierType, TokenStatus
from ksef2.endpoints.base import OffsetPaginationQueryParams
from ksef2.endpoints.invoices import InvoiceMetadataQueryParams
from ksef2.endpoints.session import ListSessionsQueryParams
from ksef2.endpoints.tokens import ListTokensQueryParams


class PageSizeMixin(BaseModel):
    page_size: int = Field(default=10, ge=10, le=100)


class PageOffsetMixin(BaseModel):
    page_offset: int = Field(default=0, ge=0)


class SortOrderMixin(BaseModel):
    sort_order: SortOrder = SortOrder.ASC


class OffsetPaginationParams(
    KSeFBaseParams[OffsetPaginationQueryParams], PageSizeMixin, PageOffsetMixin
):
    def next_page(self) -> Self:
        return self.model_copy(update={"page_offset": self.page_offset + 1})


class InvoiceMetadataParams(
    KSeFBaseParams[InvoiceMetadataQueryParams],
    PageSizeMixin,
    PageOffsetMixin,
    SortOrderMixin,
): ...


class PermissionsQueryParams(OffsetPaginationParams): ...


class TokenPaginationParams(KSeFBaseParams):
    """Base for endpoints using pageSize + x-continuation-token header."""

    page_size: int = Field(default=10, ge=10, le=100)


class SessionListParams(TokenPaginationParams):
    """GET /sessions"""

    page_size: int = Field(default=10, ge=10, le=1000)
    session_type: SessionTypeEnum
    reference_number: str | None = None
    date_created_from: datetime | None = None
    date_created_to: datetime | None = None
    date_closed_from: datetime | None = None
    date_closed_to: datetime | None = None
    date_modified_from: datetime | None = None
    date_modified_to: datetime | None = None
    statuses: list[SessionStatusEnum] | None = None


class SessionInvoiceListParams(TokenPaginationParams):
    page_size: int = Field(default=10, ge=10, le=1000)


class TokenListParams(KSeFBaseParams[ListTokensQueryParams], PageSizeMixin):
    status: list[TokenStatus] | None = None
    description: str | None = None
    author_identifier: str | None = None
    author_identifier_type: TokenAuthorIdentifierType | None = None


class AuthSessionListParams(TokenPaginationParams): ...


class ListSessionsQuery(KSeFBaseParams[ListSessionsQueryParams], PageSizeMixin):
    session_type: SessionTypeEnum
    reference_number: str | None = None
    date_created_from: datetime | None = None
    date_created_to: datetime | None = None
    date_closed_from: datetime | None = None
    date_closed_to: datetime | None = None
    date_modified_from: datetime | None = None
    date_modified_to: datetime | None = None
    statuses: list[SessionStatus] | None = None
