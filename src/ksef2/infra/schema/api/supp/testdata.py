from typing import Annotated, Literal
from pydantic import BaseModel, Field, AwareDatetime


class SubUnit(BaseModel):
    subjectNip: Annotated[
        str,
        Field(
            min_length=10,
            max_length=10,
            pattern=r"^[1-9]((\d[1-9])|([1-9]\d))\d{7}$",
            description="10 cyfrowy numer NIP.",
        ),
    ]
    description: Annotated[
        str, Field(min_length=5, max_length=256, description="Opis podmiotu")
    ]


class CreateSubjectRequest(BaseModel):
    subjectNip: Annotated[
        str,
        Field(
            min_length=10,
            max_length=10,
            pattern=r"^[1-9]((\d[1-9])|([1-9]\d))\d{7}$",
            description="10 cyfrowy numer NIP.",
        ),
    ]
    subjectType: Annotated[
        Literal["EnforcementAuthority", "VatGroup", "JST"],
        Field(description="Typ podmiotu."),
    ]
    subunits: Annotated[
        list[SubUnit] | None,
        Field(default=None, description="Lista podrzędnych podmiotów"),
    ]
    description: Annotated[
        str, Field(min_length=5, max_length=256, description="Opis podmiotu")
    ]
    createdDate: Annotated[
        AwareDatetime | None,
        Field(default=None, description="Data utworzenia podmiotu"),
    ]
