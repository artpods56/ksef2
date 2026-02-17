from __future__ import annotations

from typing import Any, final
from urllib.parse import urlencode

from ksef2.core import codecs, headers, protocols
from ksef2.infra.schema.api import spec


@final
class CertificateLimitsEndpoint:
    """GET /certificates/limits - Get certificate limits for authenticated subject."""

    url: str = "/certificates/limits"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(self, access_token: str) -> spec.CertificateLimitsResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.CertificateLimitsResponse,
        )


@final
class CertificateEnrollmentDataEndpoint:
    """GET /certificates/enrollments/data - Get data for CSR preparation."""

    url: str = "/certificates/enrollments/data"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(self, access_token: str) -> spec.CertificateEnrollmentDataResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.CertificateEnrollmentDataResponse,
        )


@final
class EnrollCertificateEndpoint:
    """POST /certificates/enrollments - Submit certificate enrollment request."""

    url: str = "/certificates/enrollments"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.EnrollCertificateResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.EnrollCertificateResponse,
        )


@final
class CertificateEnrollmentStatusEndpoint:
    """GET /certificates/enrollments/{referenceNumber} - Get enrollment status."""

    url: str = "/certificates/enrollments/{referenceNumber}"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, reference_number: str) -> str:
        return self.url.format(referenceNumber=reference_number)

    def send(
        self,
        access_token: str,
        reference_number: str,
    ) -> spec.CertificateEnrollmentStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.get_url(reference_number=reference_number),
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.CertificateEnrollmentStatusResponse,
        )


@final
class RetrieveCertificatesEndpoint:
    """POST /certificates/retrieve - Retrieve certificates by serial numbers."""

    url: str = "/certificates/retrieve"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.RetrieveCertificatesResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.RetrieveCertificatesResponse,
        )


@final
class RevokeCertificateEndpoint:
    """POST /certificates/{certificateSerialNumber}/revoke - Revoke a certificate."""

    url: str = "/certificates/{certificateSerialNumber}/revoke"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def get_url(self, *, certificate_serial_number: str) -> str:
        return self.url.format(certificateSerialNumber=certificate_serial_number)

    def send(
        self,
        access_token: str,
        certificate_serial_number: str,
        body: dict[str, Any] | None = None,
    ) -> None:
        _ = self._transport.post(
            self.get_url(certificate_serial_number=certificate_serial_number),
            headers=headers.KSeFHeaders.bearer(access_token),
            json=body or {},
        )


@final
class QueryCertificatesEndpoint:
    """POST /certificates/query - Query certificates list."""

    url: str = "/certificates/query"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
        *,
        page_size: int | None = None,
        page_offset: int | None = None,
    ) -> spec.QueryCertificatesResponse:
        query_params: list[tuple[str, str]] = []

        if page_size is not None:
            query_params.append(("pageSize", str(page_size)))

        if page_offset is not None:
            query_params.append(("pageOffset", str(page_offset)))

        query_string = urlencode(query_params) if query_params else ""
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QueryCertificatesResponse,
        )
