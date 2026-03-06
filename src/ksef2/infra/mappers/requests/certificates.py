from ksef2.domain.models.certificates import (
    Certificate,
    CertificateEnrollmentData,
    CertificateEnrollmentResponse,
    CertificateEnrollmentStatusResponse,
    CertificateInfo,
    CertificateLimitsResponse,
    CertificatesInfoList,
    CertificateStatus,
    CertificateType,
    EnrollCertificateRequest,
    IdentifierType,
    QueryCertificatesRequest,
    RetrieveCertificatesRequest,
    RetrievedCertificatesList,
    RevocationReason,
    RevokeCertificateRequest,
)
from ksef2.infra.mappers.helpers import lookup
from ksef2.infra.schema.api import spec
from ksef2.infra.mappers import helpers

_CERTIFICATE_TYPE_TO_DOMAIN: dict[spec.KsefCertificateType, CertificateType] = {
    spec.KsefCertificateType.Authentication: "authentication",
    spec.KsefCertificateType.Offline: "offline",
}
_CERTIFICATE_TYPE_FROM_DOMAIN: dict[CertificateType, spec.KsefCertificateType] = {
    v: k for k, v in _CERTIFICATE_TYPE_TO_DOMAIN.items()
}

_REVOCATION_REASON: dict[RevocationReason, spec.CertificateRevocationReason] = {
    "unspecified": spec.CertificateRevocationReason.Unspecified,
    "superseded": spec.CertificateRevocationReason.Superseded,
    "key_compromise": spec.CertificateRevocationReason.KeyCompromise,
}

_IDENTIFIER_TYPE: dict[spec.CertificateSubjectIdentifierType, IdentifierType] = {
    spec.CertificateSubjectIdentifierType.Nip: "nip",
    spec.CertificateSubjectIdentifierType.Fingerprint: "fingerprint",
    spec.CertificateSubjectIdentifierType.Pesel: "pesel",
}

_STATUS_TO_DOMAIN: dict[spec.CertificateListItemStatus, CertificateStatus] = {
    spec.CertificateListItemStatus.Active: "active",
    spec.CertificateListItemStatus.Revoked: "revoked",
    spec.CertificateListItemStatus.Expired: "expired",
    spec.CertificateListItemStatus.Blocked: "blocked",
}
_STATUS_FROM_DOMAIN: dict[CertificateStatus, spec.CertificateListItemStatus] = {
    v: k for k, v in _STATUS_TO_DOMAIN.items()
}

_IDENTIFIER_FIELD: dict[spec.CertificateSubjectIdentifierType, str] = {
    spec.CertificateSubjectIdentifierType.Nip: "nip",
    spec.CertificateSubjectIdentifierType.Pesel: "pesel",
    spec.CertificateSubjectIdentifierType.Fingerprint: "fingerprint",
}


def map_get_limits_response(
    response: spec.CertificateLimitsResponse,
) -> CertificateLimitsResponse:
    return CertificateLimitsResponse(
        can_request=response.canRequest,
        enrollment_limit=response.enrollment.limit,
        enrollment_remaining=response.enrollment.remaining,
        certificate_limit=response.certificate.limit,
        certificate_remaining=response.certificate.remaining,
    )


def map_get_enrollment_data_response(
    response: spec.CertificateEnrollmentDataResponse,
) -> CertificateEnrollmentData:
    return CertificateEnrollmentData(
        common_name=response.commonName,
        name=response.givenName,
        surname=response.surname,
        iso_country_code=response.countryName,
        serial_number=response.serialNumber,
        unique_identifier=response.uniqueIdentifier,
        organization_name=response.organizationName,
        organization_identifier=response.organizationIdentifier,
    )


def map_enrollment_request(
    request: EnrollCertificateRequest,
) -> spec.EnrollCertificateRequest:
    return spec.EnrollCertificateRequest(
        certificateName=request.certificate_name,
        certificateType=lookup(
            _CERTIFICATE_TYPE_FROM_DOMAIN, request.certificate_type, "certificate type"
        ),
        csr=request.csr,
        validFrom=helpers.to_aware_datetime(request.valid_from)
        if request.valid_from
        else None,
    )


def map_cert_enrollment_response(
    response: spec.EnrollCertificateResponse,
) -> CertificateEnrollmentResponse:
    return CertificateEnrollmentResponse(
        reference_number=response.referenceNumber,
        timestamp=response.timestamp,
    )


def map_get_enrollment_status_response(
    response: spec.CertificateEnrollmentStatusResponse,
) -> CertificateEnrollmentStatusResponse:
    return CertificateEnrollmentStatusResponse(
        request_date=response.requestDate,
        status_code=response.status.code,
        status_description=response.status.description,
        status_details=response.status.details,
        certificate_serial_number=response.certificateSerialNumber,
    )


def map_retrieve_certificates_request(
    request: RetrieveCertificatesRequest,
) -> spec.RetrieveCertificatesRequest:
    return spec.RetrieveCertificatesRequest(
        certificateSerialNumbers=request.certificate_serial_numbers,
    )


def map_retrieve_certificates_response(
    response: spec.RetrieveCertificatesResponse,
) -> RetrievedCertificatesList:
    return RetrievedCertificatesList(
        certificates=[
            Certificate(
                name=c.certificateName,
                certificate_type=lookup(
                    _CERTIFICATE_TYPE_TO_DOMAIN, c.certificateType, "certificate type"
                ),
                base64_encoded_certificate=c.certificate,
                serial_number=c.certificateSerialNumber,
            )
            for c in response.certificates
        ],
    )


def map_revoke_request(
    request: RevokeCertificateRequest,
) -> spec.RevokeCertificateRequest | None:
    return spec.RevokeCertificateRequest(
        revocationReason=lookup(
            _REVOCATION_REASON, request.revocation_reason, "revocation reason"
        )
        if request.revocation_reason
        else None,
    )


def map_query_request(
    request: QueryCertificatesRequest,
) -> spec.QueryCertificatesRequest:
    return spec.QueryCertificatesRequest(
        certificateSerialNumber=request.certificate_serial_number,
        name=request.name,
        type=lookup(
            _CERTIFICATE_TYPE_FROM_DOMAIN, request.certificate_type, "certificate type"
        )
        if request.certificate_type
        else None,
        status=lookup(_STATUS_FROM_DOMAIN, request.status, "certificate status")
        if request.status
        else None,
        expiresAfter=helpers.to_aware_datetime(request.expires_after)
        if request.expires_after
        else None,
    )


def map_query_response(
    response: spec.QueryCertificatesResponse,
) -> CertificatesInfoList:

    certificates_info: list[CertificateInfo] = []

    for c in response.certificates:
        field_name = lookup(
            _IDENTIFIER_FIELD, c.subjectIdentifier.type, "identifier type"
        )

        certificate_info = CertificateInfo(
            serial_number=c.certificateSerialNumber,
            name=c.name,
            common_name=c.commonName,
            type=lookup(_CERTIFICATE_TYPE_TO_DOMAIN, c.type, "certificate type"),
            status=lookup(_STATUS_TO_DOMAIN, c.status, "certificate status"),
            identifier_type=lookup(
                _IDENTIFIER_TYPE, c.subjectIdentifier.type, "identifier type"
            ),
            valid_from=c.validFrom,
            valid_to=c.validTo,
            request_date=c.requestDate,
            last_use_date=c.lastUseDate,
            **{field_name: c.subjectIdentifier.value},
        )

        certificates_info.append(certificate_info)
    return CertificatesInfoList(
        certificates=certificates_info,
        has_more=response.hasMore,
    )


# single dispatch implementatio
