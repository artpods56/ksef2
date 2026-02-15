from pydantic import BaseModel, ConfigDict


class BaseSupp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
