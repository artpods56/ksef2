from typing import Annotated

from pydantic import Field

from ksef2.infra.schema.api.spec.models import (
    AuthenticationContextIdentifier,
    AuthorizationPolicy,
)
from ksef2.infra.schema.api.supp.base import BaseSupp


class InitTokenAuthenticationRequest(BaseSupp):
    """Supplementary model with str field annotation instead of Base64Str"""

    challenge: Annotated[str, Field(max_length=36, min_length=36)]
    """
    Wygenerowany wcześniej challenge.
    """
    contextIdentifier: AuthenticationContextIdentifier
    """
    Identyfikator kontekstu do którego następuje uwierzytelnienie.
    """
    encryptedToken: str
    """
    Zaszyfrowany token wraz z timestampem z challenge'a, w postaci `token|timestamp`, zakodowany w formacie Base64.
    """
    authorizationPolicy: AuthorizationPolicy | None = None
    """
    Polityka autoryzacji żądań przy każdym użyciu tokena dostępu.
    """
