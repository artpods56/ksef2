from dataclasses import dataclass

from ksef2.endpoints import (
    auth,
    certificates,
    encryption,
    invoices,
    limits,
    peppol,
    permissions,
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

__invoices_query_endpoints__ = [
    EndpointRef("POST", invoices.QueryInvoicesMetadataEndpoint.url),
    EndpointRef("POST", invoices.ExportInvoicesEndpoint.url),
    EndpointRef("GET", invoices.GetExportStatusEndpoint.url),
]

__invoices_status_endpoints__ = [
    EndpointRef("GET", session.ListSessionsEndpoint.url),
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
    EndpointRef("GET", session.GetSessionUpoEndpoint.url),
    EndpointRef("POST", session.OpenBatchSessionEndpoint.url),
    EndpointRef("POST", session.CloseBatchSessionEndpoint.url),
]

__testdata_endpoints__ = [
    EndpointRef("POST", testdata.CreateSubjectEndpoint.url),
    EndpointRef("POST", testdata.DeleteSubjectEndpoint.url),
    EndpointRef("POST", testdata.CreatePersonEndpoint.url),
    EndpointRef("POST", testdata.DeletePersonEndpoint.url),
    EndpointRef("POST", testdata.GrantPermissionsEndpoint.url),
    EndpointRef("POST", testdata.RevokePermissionsEndpoint.url),
    EndpointRef("POST", testdata.EnableAttachmentsEndpoint.url),
    EndpointRef("POST", testdata.RevokeAttachmentsEndpoint.url),
    EndpointRef("POST", testdata.BlockContextEndpoint.url),
    EndpointRef("POST", testdata.UnblockContextEndpoint.url),
]

__tokens_endpoints__ = [
    EndpointRef("POST", tokens.GenerateTokenEndpoint.url),
    EndpointRef("GET", tokens.ListTokensEndpoint.url),
    EndpointRef("GET", tokens.TokenStatusEndpoint.url),
    EndpointRef("DELETE", tokens.RevokeTokenEndpoint.url),
]

__permissions_endpoints__ = [
    EndpointRef("POST", permissions.GrantPersonPermissionsEndpoint.url),
    EndpointRef("POST", permissions.GrantEntityPermissionsEndpoint.url),
    EndpointRef("POST", permissions.GrantAuthorizationPermissionsEndpoint.url),
    EndpointRef("POST", permissions.GrantIndirectPermissionsEndpoint.url),
    EndpointRef("POST", permissions.GrantSubunitPermissionsEndpoint.url),
    EndpointRef("POST", permissions.GrantEuEntityPermissionsEndpoint.url),
    EndpointRef("POST", permissions.GrantEuEntityAdministrationPermissionsEndpoint.url),
    EndpointRef(
        "DELETE",
        permissions.RevokeAuthorizationPermissionsEndpoint.url + "/{permissionId}",
    ),
    EndpointRef(
        "DELETE", permissions.RevokeCommonPermissionsEndpoint.url + "/{permissionId}"
    ),
    EndpointRef("GET", permissions.GetAttachmentPermissionStatusEndpoint.url),
    EndpointRef(
        "GET",
        permissions.GetPermissionOperationStatusEndpoint.url + "/{referenceNumber}",
    ),
    EndpointRef("GET", permissions.GetEntityRolesEndpoint.url),
    EndpointRef("POST", permissions.QueryAuthorizationsPermissionsEndpoint.url),
    EndpointRef("POST", permissions.QueryEuEntitiesPermissionsEndpoint.url),
    EndpointRef("POST", permissions.QueryPersonalPermissionsEndpoint.url),
    EndpointRef("POST", permissions.QueryPersonsPermissionsEndpoint.url),
    EndpointRef("POST", permissions.QuerySubordinateEntitiesRolesEndpoint.url),
    EndpointRef("POST", permissions.QuerySubunitsPermissionsEndpoint.url),
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
    EndpointRef("POST", limits.SetProductionRateLimitsEndpoint.url),
]

__certificates_endpoints__ = [
    EndpointRef("GET", certificates.CertificateLimitsEndpoint.url),
    EndpointRef("GET", certificates.CertificateEnrollmentDataEndpoint.url),
    EndpointRef("POST", certificates.EnrollCertificateEndpoint.url),
    EndpointRef("GET", certificates.CertificateEnrollmentStatusEndpoint.url),
    EndpointRef("POST", certificates.RetrieveCertificatesEndpoint.url),
    EndpointRef("POST", certificates.RevokeCertificateEndpoint.url),
    EndpointRef("POST", certificates.QueryCertificatesEndpoint.url),
]

__peppol_endpoints__ = [
    EndpointRef("GET", peppol.QueryPeppolProvidersEndpoint.url),
]

__all_endpoints__: list[EndpointRef] = [
    *__auth_endpoints__,
    *__certificates_endpoints__,
    *__encryption_endpoints__,
    *__invoices_endpoints__,
    *__invoices_query_endpoints__,
    *__invoices_status_endpoints__,
    *__peppol_endpoints__,
    *__session_endpoints__,
    *__testdata_endpoints__,
    *__tokens_endpoints__,
    *__permissions_endpoints__,
    *__limits_endpoints__,
]
