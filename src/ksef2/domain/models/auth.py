from enum import Enum

from pydantic import AwareDatetime

from ksef2.domain.models.base import KSeFBaseModel


class ContextIdentifierType(Enum):
    NIP = "Nip"
    INTERNAL_ID = "InternalId"
    NIP_VAT_UE = "NipVatUe"
    PEPPOL_ID = "PeppolId"


class AuthenticationMethod(Enum):
    TOKEN = "Token"
    TRUSTED_PROFILE = "TrustedProfile"
    INTERNAL_CERTIFICATE = "InternalCertificate"
    QUALIFIED_SIGNATURE = "QualifiedSignature"
    QUALIFIED_SEAL = "QualifiedSeal"
    PERSONAL_SIGNATURE = "PersonalSignature"
    PEPPOL_SIGNATURE = "PeppolSignature"


class ChallengeResponse(KSeFBaseModel):
    challenge: str
    timestamp: AwareDatetime
    timestamp_ms: int


class TokenCredentials(KSeFBaseModel):
    token: str
    valid_until: AwareDatetime


class AuthInitResponse(KSeFBaseModel):
    reference_number: str
    authentication_token: TokenCredentials


class AuthOperationStatus(KSeFBaseModel):
    start_date: AwareDatetime
    authentication_method: AuthenticationMethod
    status_code: int
    status_description: str
    status_details: list[str] | None = None
    is_token_redeemed: bool | None = None


class AuthTokens(KSeFBaseModel):
    access_token: TokenCredentials
    refresh_token: TokenCredentials


class RefreshedToken(KSeFBaseModel):
    access_token: TokenCredentials
