from dataclasses import dataclass

from ksef2.endpoints import (
    auth,
    encryption,
    invoices,
    limits,
    session,
    testdata,
    tokens,
)


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
    EndpointRef("GET", auth.ListActiveSessionsEndpoint.url),
    EndpointRef("DELETE", auth.TerminateCurrentSessionEndpoint.url),
    EndpointRef("DELETE", auth.TerminateAuthSessionEndpoint.url),
]

__encryption_endpoints__ = [
    EndpointRef("GET", encryption.CertificateEndpoint.url),
]

__invoices_endpoints__ = [
    EndpointRef("GET", invoices.DownloadInvoiceEndpoint.url),
    EndpointRef("POST", invoices.SendingInvoicesEndpoint.url),
]

__invoices_status_endpoints__ = [
    EndpointRef("GET", invoices.ListSessionsEndpoint.url),
    EndpointRef("GET", invoices.GetSessionStatusEndpoint.url),
    EndpointRef("GET", invoices.ListSessionInvoicesEndpoint.url),
    EndpointRef("GET", invoices.GetSessionInvoiceStatusEndpoint.url),
    EndpointRef("GET", invoices.ListFailedSessionInvoicesEndpoint.url),
    EndpointRef("GET", invoices.GetInvoiceUpoByKsefNumberEndpoint.url),
    EndpointRef("GET", invoices.GetInvoiceUpoByReferenceEndpoint.url),
]

__session_endpoints__ = [
    EndpointRef("POST", session.OpenSessionEndpoint.url),
    EndpointRef("POST", session.TerminateSessionEndpoint.url),
]

__testdata_endpoints__ = [
    EndpointRef("POST", testdata.CreateSubjectEndpoint.url),
    EndpointRef("POST", testdata.DeleteSubjectEndpoint.url),
    EndpointRef("POST", testdata.CreatePersonEndpoint.url),
    EndpointRef("POST", testdata.DeletePersonEndpoint.url),
    EndpointRef("POST", testdata.GrantPermissionsEndpoint.url),
    EndpointRef("POST", testdata.RevokePermissionsEndpoint.url),
    EndpointRef("POST", testdata.EnableAttachmentsEndpoint.url),
]

__tokens_endpoints__ = [
    EndpointRef("POST", tokens.GenerateTokenEndpoint.url),
    EndpointRef("GET", tokens.TokenStatusEndpoint.url),
    EndpointRef("DELETE", tokens.RevokeTokenEndpoint.url),
]

__limits_endpoints__ = [
    EndpointRef("GET", limits.GetContextLimitsEndpoint.url),
    EndpointRef("GET", limits.GetSubjectLimitsEndpoint.url),
    EndpointRef("GET", limits.GetApiRateLimitsEndpoint.url),
    EndpointRef("POST", limits.SetSessionLimitsEndpoint.url),
    EndpointRef("DELETE", limits.ResetSessionLimitsEndpoint.url),
    EndpointRef("POST", limits.SetSubjectLimitsEndpoint.url),
    EndpointRef("DELETE", limits.ResetSubjectLimitsEndpoint.url),
    EndpointRef("POST", limits.SetApiRateLimitsEndpoint.url),
    EndpointRef("DELETE", limits.ResetApiRateLimitsEndpoint.url),
]

__all_endpoints__: list[EndpointRef] = [
    *__auth_endpoints__,
    *__encryption_endpoints__,
    *__invoices_endpoints__,
    *__invoices_status_endpoints__,
    *__session_endpoints__,
    *__testdata_endpoints__,
    *__tokens_endpoints__,
    *__limits_endpoints__,
]
