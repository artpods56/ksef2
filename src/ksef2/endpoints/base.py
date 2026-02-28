import abc
from typing import Any, ClassVar, Mapping, NotRequired, TypedDict
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, TypeAdapter, ValidationError
from ksef2.core import codecs, exceptions
from ksef2.core.protocols import Middleware

OffsetPaginationQueryParams = TypedDict(
    "OffsetPaginationQueryParams",
    {
        "pageOffset": NotRequired[int | None],
        "pageSize": NotRequired[int | None],
    },
)


class BaseEndpoints(abc.ABC):
    _PARAMS_ADAPTER: ClassVar[TypeAdapter[OffsetPaginationQueryParams]] = TypeAdapter(
        OffsetPaginationQueryParams
    )

    def __init__(self, transport: Middleware):
        self._transport = transport

    @classmethod
    def _parse[T: BaseModel](
        cls, response: httpx.Response, response_type: type[T]
    ) -> T:
        try:
            return codecs.JsonResponseCodec.parse(response, response_type)
        except ValidationError as e:
            raise exceptions.KSeFValidationError("Invalid response payload") from e

    @classmethod
    def _parse_list[T: BaseModel](
        cls, response: httpx.Response, response_type: type[T]
    ) -> list[T]:
        try:
            return codecs.JsonResponseCodec.parse_list(response, response_type)
        except ValidationError as e:
            raise exceptions.KSeFValidationError("Invalid response payload") from e

    def build_params[T: Mapping[str, Any]](
        self,
        params: T,
        adapter: TypeAdapter[T] | None = None,
    ) -> httpx.QueryParams:
        validated = (adapter or self._PARAMS_ADAPTER).validate_python(params)
        filtered = {k: v for k, v in validated.items() if v is not None}
        return httpx.QueryParams(urlencode(filtered, doseq=True))
