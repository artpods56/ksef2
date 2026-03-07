"""Shared Pydantic base classes for SDK models and query parameter models."""

from typing import cast

from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class KSeFBaseModel(BaseModel):
    """Base model that forbids undeclared fields."""

    model_config = ConfigDict(extra="forbid")


class KSeFBaseParams[ParamsT](KSeFBaseModel):
    """Base model for query-parameter objects serialized with camelCase aliases."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        use_enum_values=True,
        serialize_by_alias=True,
    )

    def to_query_params(self) -> ParamsT:
        """Serialize the model into a JSON-safe query-parameter mapping."""
        return cast(
            ParamsT, self.model_dump(by_alias=True, exclude_none=True, mode="json")
        )
