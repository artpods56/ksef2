from dataclasses import dataclass

from ksef2.endpoints import auth, encryption, invoices, session, tokens


@dataclass(frozen=True)
class EndpointRef:
    method: str
    url: str

__auth_endpoints__ = [
    EndpointRef("POST", auth.ChallengeEndpoint.url),
    EndpointRef("POST", auth.TokenAuthEndpoint.url),
    EndpointRef("POST", auth.XAdESAuthEndpoint.url),
    EndpointRef("GET", auth.AuthStatusEndpoint.url),
    EndpointRef("POST", auth.RedeemTokenEndpoint.url),
    EndpointRef("POST", auth.RefreshTokenEndpoint.url),
]

__encryption_endpoints__ = [
    EndpointRef("GET", encryption.CertificateEndpoint.url),
]

__invoices_endpoints__ = [
    EndpointRef("GET", invoices.DownloadInvoiceEndpoint.url),
    EndpointRef("POST", invoices.SendingInvoicesEndpoint.url),
]

__session_endpoints__ = [
    EndpointRef("POST", session.OpenSessionEndpoint.url),
    EndpointRef("POST", session.TerminateSessionEndpoint.url),
]

__tokens_endpoints__ = [
    EndpointRef("POST", tokens.GenerateTokenEndpoint.url),
    EndpointRef("GET", tokens.TokenStatusEndpoint.url),
    EndpointRef("DELETE", tokens.RevokeTokenEndpoint.url),
]

__all_endpoints__: list[EndpointRef] = [
    *__auth_endpoints__,
    *__encryption_endpoints__,
    *__invoices_endpoints__,
    *__session_endpoints__,
    *__tokens_endpoints__,
]