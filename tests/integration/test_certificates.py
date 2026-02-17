from __future__ import annotations

import pytest

from ksef2.domain.models.certificates import (
    CertificateEnrollmentData,
    CertificateLimitsResponse,
    CertificateStatus,
    CertificateType,
    QueryCertificatesResponse,
)


@pytest.mark.integration
def test_get_certificate_limits(xades_authenticated_context):
    """Fetch certificate limits for the authenticated subject."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.certificates.get_limits(access_token=token)

    assert isinstance(result, CertificateLimitsResponse)
    assert isinstance(result.can_request, bool)
    assert result.enrollment.limit >= 0
    assert result.enrollment.remaining >= 0
    assert result.certificate.limit >= 0
    assert result.certificate.remaining >= 0


@pytest.mark.integration
def test_get_enrollment_data(xades_authenticated_context):
    """Fetch certificate enrollment data for CSR preparation.

    Note: This endpoint may fail with self-signed certs because it requires
    a specific authentication method (qualified certificate).
    """
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    try:
        result = client.certificates.get_enrollment_data(access_token=token)

        assert isinstance(result, CertificateEnrollmentData)
        assert result.common_name
        assert result.country_name
    except Exception as e:
        # Expected to fail with self-signed certs (error 25001)
        if "25001" in str(e):
            pytest.skip("Enrollment data not available for self-signed cert auth")
        raise


@pytest.mark.integration
def test_query_certificates_no_filters(xades_authenticated_context):
    """Query all certificates without filters."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.certificates.query(access_token=token)

    assert isinstance(result, QueryCertificatesResponse)
    assert isinstance(result.certificates, list)
    assert isinstance(result.has_more, bool)


@pytest.mark.integration
def test_query_certificates_with_status_filter(xades_authenticated_context):
    """Query certificates filtering by status."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.certificates.query(
        access_token=token,
        status=CertificateStatus.ACTIVE,
    )

    assert isinstance(result, QueryCertificatesResponse)
    # All returned certificates should be active
    for cert in result.certificates:
        assert cert.status == CertificateStatus.ACTIVE


@pytest.mark.integration
def test_query_certificates_with_type_filter(xades_authenticated_context):
    """Query certificates filtering by type."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.certificates.query(
        access_token=token,
        certificate_type=CertificateType.AUTHENTICATION,
    )

    assert isinstance(result, QueryCertificatesResponse)
    # All returned certificates should be authentication type
    for cert in result.certificates:
        assert cert.type == CertificateType.AUTHENTICATION


@pytest.mark.integration
def test_query_certificates_with_pagination(xades_authenticated_context):
    """Query certificates with pagination parameters."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    # Query with small page size
    result = client.certificates.query(
        access_token=token,
        page_size=10,
        page_offset=0,
    )

    assert isinstance(result, QueryCertificatesResponse)
    assert len(result.certificates) <= 10


@pytest.mark.integration
def test_query_certificates_with_name_filter(xades_authenticated_context):
    """Query certificates with partial name match."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    # First get all certificates to find a name to search for
    all_certs = client.certificates.query(access_token=token)

    if not all_certs.certificates:
        pytest.skip("No certificates available to test name filtering")

    # Use part of the first certificate's name
    first_cert_name = all_certs.certificates[0].name
    if len(first_cert_name) < 3:
        pytest.skip("Certificate name too short for partial match test")

    search_term = first_cert_name[:3]

    result = client.certificates.query(
        access_token=token,
        name=search_term,
    )

    assert isinstance(result, QueryCertificatesResponse)
    # All returned certificates should contain the search term in their name
    for cert in result.certificates:
        assert search_term.lower() in cert.name.lower()
