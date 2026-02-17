from __future__ import annotations

from typing import TypedDict, NotRequired

from pydantic import Field

from ksef2.domain.models import KSeFBaseParams, SortOrder


class PaginationParams(KSeFBaseParams):
    page_offset: int = Field(default=0, ge=0)
    page_size: int = Field(default=10, ge=10, le=250)

    def to_api_params(self) -> PaginationQueryParams:
        return {"pageOffset": self.page_offset, "pageSize": self.page_size}


class InvoiceQueryParams(PaginationParams):
    sort_order: SortOrder = SortOrder.ASC


PaginationQueryParams = TypedDict(
    "PaginationQueryParams",
    {
        "pageOffset": NotRequired[int | None],
        "pageSize": NotRequired[int | None],
    },
)
