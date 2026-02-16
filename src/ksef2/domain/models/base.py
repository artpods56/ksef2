from typing import Any

from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class KSeFBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class KSeFBaseParams(KSeFBaseModel):
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

    def to_api_params(self) -> dict[str, Any]:
        return self.model_dump(
            exclude_none=True,
            mode="json",
        )
