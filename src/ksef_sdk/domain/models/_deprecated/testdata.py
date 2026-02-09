from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class RegisterPersonRequest(BaseModel):
    """Register a person (JDG or bailiff) on the KSeF TEST environment."""

    nip: Annotated[str, Field(description="NIP number of the business entity")]
    pesel: Annotated[str, Field(description="PESEL number of the person")]
    description: Annotated[str, Field(description="Label for the person, e.g. 'JDG'")]
    isBailiff: Annotated[bool, Field(description="Whether the person is a bailiff")] = (
        False
    )


class SubunitInfo(BaseModel):
    """A subunit within a VAT-group subject structure."""

    subjectNip: Annotated[str, Field(description="NIP of the subunit")]
    description: Annotated[str, Field(description="Label for the subunit")]


class RegisterSubjectRequest(BaseModel):
    """Create a subject structure (e.g. VAT group with subunits) on the KSeF TEST environment."""

    subjectNip: Annotated[str, Field(description="NIP of the main subject")]
    subjectType: Annotated[
        Literal["EnforcementAuthority", "VatGroup", "JST"],
        Field(description="Subject type"),
    ]
    description: Annotated[str, Field(description="Label for the subject")]
    subunits: Annotated[
        list[SubunitInfo], Field(description="Optional list of subunits")
    ] = []


class TestPermission(BaseModel):
    """A single permission entry to grant."""

    permissionType: Annotated[
        Literal[
            "InvoiceRead",
            "InvoiceWrite",
            "Introspection",
            "CredentialsRead",
            "CredentialsManage",
            "EnforcementOperations",
            "SubunitManage",
        ],
        Field(description="Permission type"),
    ]
    description: Annotated[
        str, Field(description="Human-readable description of the permission")
    ]


class IdentifierInfo(BaseModel):
    """An identifier (NIP, PESEL, or Fingerprint) used in permission grants."""

    value: Annotated[str, Field(description="The identifier value")]
    type: Annotated[
        Literal["Nip", "Pesel", "Fingerprint"],
        Field(description="Identifier type. contextIdentifier only accepts 'Nip'."),
    ]


class GrantPermissionsRequest(BaseModel):
    """Grant permissions to a person in a given context on the KSeF TEST environment."""

    contextIdentifier: Annotated[
        IdentifierInfo,
        Field(description="The context (business entity) to grant access to"),
    ]
    authorizedIdentifier: Annotated[
        IdentifierInfo, Field(description="The person being granted permissions")
    ]
    permissions: Annotated[
        list[TestPermission], Field(description="List of permissions to grant")
    ]
