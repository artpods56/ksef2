from datetime import datetime
from enum import StrEnum
from typing import Literal

from ksef2.domain.models.base import KSeFBaseModel

type ContextIdentifierType = Literal["nip", "internal_id", "nip_vat_ue", "peppol_id"]

type AuthenticationMethod = Literal[
    "token",
    "trusted_profile",
    "internal_certificate",
    "qualified_signature",
    "qualified_seal",
    "personal_signature",
    "peppol_signature",
]

type AuthenticationMethodCategory = Literal[
    "xades_signature",
    "national_node",
    "token",
    "other",
]


class ContextIdentifierTypeEnum(StrEnum):
    NIP = "nip"
    INTERNAL_ID = "internal_id"
    NIP_VAT_UE = "nip_vat_ue"
    PEPPOL_ID = "peppol_id"


class AuthenticationMethodEnum(StrEnum):
    TOKEN = "token"
    TRUSTED_PROFILE = "trusted_profile"
    INTERNAL_CERTIFICATE = "internal_certificate"
    QUALIFIED_SIGNATURE = "qualified_signature"
    QUALIFIED_SEAL = "qualified_seal"
    PERSONAL_SIGNATURE = "personal_signature"
    PEPPOL_SIGNATURE = "peppol_signature"


class AuthenticationMethodCategoryEnum(StrEnum):
    XADES_SIGNATURE = "xades_signature"
    NATIONAL_NODE = "national_node"
    TOKEN = "token"
    OTHER = "other"


class InitTokenAuthenticationRequest(KSeFBaseModel):
    challenge: str
    context_type: ContextIdentifierType
    context_value: str
    encrypted_token: str


class ChallengeResponse(KSeFBaseModel):
    challenge: str
    timestamp: datetime
    timestamp_ms: int


class TokenCredentials(KSeFBaseModel):
    token: str
    valid_until: datetime


class AuthInitResponse(KSeFBaseModel):
    reference_number: str
    authentication_token: TokenCredentials


class AuthOperationStatus(KSeFBaseModel):
    start_date: datetime
    authentication_method: AuthenticationMethod
    authentication_method_category: AuthenticationMethodCategory
    authentication_method_code: str
    authentication_method_display_name: str
    status_code: int
    status_description: str
    status_details: list[str] | None = None
    is_token_redeemed: bool | None = None
    last_token_refresh_date: datetime | None = None
    refresh_token_valid_until: datetime | None = None


class AuthenticationSession(KSeFBaseModel):
    reference_number: str
    start_date: datetime
    authentication_method: AuthenticationMethod
    authentication_method_category: AuthenticationMethodCategory
    authentication_method_code: str
    authentication_method_display_name: str
    status_code: int
    status_description: str
    status_details: list[str] | None = None
    is_token_redeemed: bool | None = None
    last_token_refresh_date: datetime | None = None
    refresh_token_valid_until: datetime | None = None
    is_current: bool | None = None


class AuthenticationSessionsResponse(KSeFBaseModel):
    continuation_token: str | None = None
    items: list[AuthenticationSession]


class AuthTokens(KSeFBaseModel):
    access_token: TokenCredentials
    refresh_token: TokenCredentials


class RefreshedToken(KSeFBaseModel):
    access_token: TokenCredentials
