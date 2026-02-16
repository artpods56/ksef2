from typing import Annotated

from pydantic import Field, field_validator

from ksef2.infra.schema.api.spec.models import (
    PersonPermissionsAuthorIdentifierType,
    CertificateSubjectIdentifierType,
    PersonPermissionsContextIdentifier,
    PersonPermissionsTargetIdentifier,
    PersonPermissionScope,
    PermissionState,
    PersonPermissionsQueryType,
)
from ksef2.infra.schema.api.supp.base import BaseSupp


class PersonPermissionsAuthorIdentifier(BaseSupp):
    """
    Identyfikator osoby lub podmiotu nadającego uprawnienie.
    | Type | Value |
    | --- | --- |
    | Nip | 10 cyfrowy numer NIP |
    | Pesel | 11 cyfrowy numer PESEL |
    | Fingerprint | Odcisk palca certyfikatu |
    | System | Identyfikator systemowy KSeF |
    """

    type: PersonPermissionsAuthorIdentifierType
    """
    Typ identyfikatora.
    """
    value: Annotated[str | None, Field(max_length=64, min_length=6)] = None
    """
    Wartość identyfikatora. W przypadku typu System należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
    """

    @classmethod
    @field_validator("value", mode="before")
    def filter_out_system(cls, value: str):
        if value == "System":
            return None
        return value


class PersonPermissionsAuthorizedIdentifier(BaseSupp):
    """
    Identyfikator osoby lub podmiotu uprawnionego.
    | Type | Value |
    | --- | --- |
    | Nip | 10 cyfrowy numer NIP |
    | Pesel | 11 cyfrowy numer PESEL |
    | Fingerprint | Odcisk palca certyfikatu |
    """

    type: CertificateSubjectIdentifierType
    """
    Typ identyfikatora.
    """
    value: Annotated[str, Field(max_length=64, min_length=10)]
    """
    Wartość identyfikatora.
    """

    @classmethod
    @field_validator("value", mode="before")
    def filter_out_system(cls, value: str):
        if value == "System":
            return None
        return value


class PersonPermissionsQueryRequest(BaseSupp):
    """Supplementary model for person permissions query request."""

    authorIdentifier: PersonPermissionsAuthorIdentifier | None = None
    """
    Identyfikator osoby lub podmiotu nadającego uprawnienie.
    | Type | Value |
    | --- | --- |
    | Nip | 10 cyfrowy numer NIP |
    | Pesel | 11 cyfrowy numer PESEL |
    | Fingerprint | Odcisk palca certyfikatu |
    | System | Identyfikator systemowy KSeF |
    """
    authorizedIdentifier: PersonPermissionsAuthorizedIdentifier | None = None
    """
    Identyfikator osoby lub podmiotu uprawnionego.
    | Type | Value |
    | --- | --- |
    | Nip | 10 cyfrowy numer NIP |
    | Pesel | 11 cyfrowy numer PESEL |
    | Fingerprint | Odcisk palca certyfikatu |
    """
    contextIdentifier: PersonPermissionsContextIdentifier | None = None
    """
    Identyfikator kontekstu uprawnienia (dla uprawnień nadanych administratorom jednostek podrzędnych).
    | Type | Value |
    | --- | --- |
    | Nip | 10 cyfrowy numer NIP |
    | InternalId | Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: `{nip}-{5_cyfr}` |
    """
    targetIdentifier: PersonPermissionsTargetIdentifier | None = None
    """
    Identyfikator podmiotu docelowego dla uprawnień nadanych pośrednio.
    | Type | Value |
    | --- | --- |
    | Nip | 10 cyfrowy numer NIP |
    | AllPartners | Identyfikator oznaczający, że uprawnienie nadane w sposób pośredni jest typu generalnego |
    | InternalId | Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: `{nip}-{5_cyfr}` |
    """
    permissionTypes: list[PersonPermissionScope] | None = None
    """
    Lista rodzajów wyszukiwanych uprawnień.
    """
    permissionState: PermissionState | None = None
    """
    Stan uprawnienia. 
    | Type | Value |
    | --- | --- |
    | Active | Uprawnienia aktywne |
    | Inactive | Uprawnienia nieaktywne, nadane w sposób pośredni |
    """
    queryType: PersonPermissionsQueryType
    """
    Typ zapytania.
    | Type | Value |
    | --- | --- |
    | PermissionsInCurrentContext | Lista uprawnień obowiązujących w bieżącym kontekście |
    | PermissionsGrantedInCurrentContext | Lista uprawnień nadanych w bieżącym kontekście |
    """
