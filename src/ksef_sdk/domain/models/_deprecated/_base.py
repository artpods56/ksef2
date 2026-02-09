from pydantic import BaseModel, ConfigDict


class KSeFBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
