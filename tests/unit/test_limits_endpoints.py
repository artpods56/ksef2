"""Tests for limits endpoint classes — URL correctness, HTTP method, headers."""

from __future__ import annotations

from tests.unit.conftest import FakeTransport, _TOKEN


# ---------------------------------------------------------------------------
# GetContextLimitsEndpoint
# ---------------------------------------------------------------------------


class TestGetContextLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import GetContextLimitsEndpoint

        ep = GetContextLimitsEndpoint(FakeTransport())
        assert ep.url == "/limits/context"

    def test_send_gets(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import GetContextLimitsEndpoint

        fake_transport.enqueue(
            {
                "onlineSession": {
                    "maxInvoiceSizeInMB": 1,
                    "maxInvoiceWithAttachmentSizeInMB": 3,
                    "maxInvoices": 10000,
                },
                "batchSession": {
                    "maxInvoiceSizeInMB": 1,
                    "maxInvoiceWithAttachmentSizeInMB": 3,
                    "maxInvoices": 10000,
                },
            }
        )
        ep = GetContextLimitsEndpoint(fake_transport)
        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.path == "/limits/context"
        assert call.headers is not None
        assert "Authorization" in call.headers
        assert call.headers["Authorization"] == f"Bearer {_TOKEN}"


# ---------------------------------------------------------------------------
# GetSubjectLimitsEndpoint
# ---------------------------------------------------------------------------


class TestGetSubjectLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import GetSubjectLimitsEndpoint

        ep = GetSubjectLimitsEndpoint(FakeTransport())
        assert ep.url == "/limits/subject"

    def test_send_gets(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import GetSubjectLimitsEndpoint

        fake_transport.enqueue(
            {
                "enrollment": {"maxEnrollments": 6},
                "certificate": {"maxCertificates": 2},
            }
        )
        ep = GetSubjectLimitsEndpoint(fake_transport)
        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.path == "/limits/subject"


# ---------------------------------------------------------------------------
# GetApiRateLimitsEndpoint
# ---------------------------------------------------------------------------


class TestGetApiRateLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import GetApiRateLimitsEndpoint

        ep = GetApiRateLimitsEndpoint(FakeTransport())
        assert ep.url == "/rate-limits"

    def test_send_gets(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import GetApiRateLimitsEndpoint

        fake_transport.enqueue(
            {
                "onlineSession": {"perSecond": 100, "perMinute": 300, "perHour": 1200},
                "batchSession": {"perSecond": 100, "perMinute": 200, "perHour": 600},
                "invoiceSend": {"perSecond": 100, "perMinute": 300, "perHour": 1800},
                "invoiceStatus": {
                    "perSecond": 300,
                    "perMinute": 1200,
                    "perHour": 12000,
                },
                "sessionList": {"perSecond": 50, "perMinute": 100, "perHour": 600},
                "sessionInvoiceList": {
                    "perSecond": 100,
                    "perMinute": 200,
                    "perHour": 2000,
                },
                "sessionMisc": {"perSecond": 100, "perMinute": 1200, "perHour": 12000},
                "invoiceMetadata": {"perSecond": 80, "perMinute": 160, "perHour": 200},
                "invoiceExport": {"perSecond": 40, "perMinute": 80, "perHour": 200},
                "invoiceExportStatus": {
                    "perSecond": 100,
                    "perMinute": 600,
                    "perHour": 6000,
                },
                "invoiceDownload": {"perSecond": 80, "perMinute": 160, "perHour": 640},
                "other": {"perSecond": 100, "perMinute": 300, "perHour": 1200},
            }
        )
        ep = GetApiRateLimitsEndpoint(fake_transport)
        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "GET"
        assert call.path == "/rate-limits"


# ---------------------------------------------------------------------------
# SetSessionLimitsEndpoint
# ---------------------------------------------------------------------------


class TestSetSessionLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import SetSessionLimitsEndpoint

        ep = SetSessionLimitsEndpoint(FakeTransport())
        assert ep.url == "/testdata/limits/context/session"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import SetSessionLimitsEndpoint
        from ksef2.infra.schema.api import spec as spec

        fake_transport.enqueue(status_code=200)
        ep = SetSessionLimitsEndpoint(fake_transport)

        body = spec.SetSessionLimitsRequest(
            onlineSession=spec.OnlineSessionContextLimitsOverride(
                maxInvoices=5000,
                maxInvoiceSizeInMB=2,
                maxInvoiceWithAttachmentSizeInMB=5,
            ),
            batchSession=spec.BatchSessionContextLimitsOverride(
                maxInvoices=5000,
                maxInvoiceSizeInMB=2,
                maxInvoiceWithAttachmentSizeInMB=5,
            ),
        )
        ep.send(bearer_token=_TOKEN, body=body)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/limits/context/session"
        assert call.json is not None


# ---------------------------------------------------------------------------
# ResetSessionLimitsEndpoint
# ---------------------------------------------------------------------------


class TestResetSessionLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import ResetSessionLimitsEndpoint

        ep = ResetSessionLimitsEndpoint(FakeTransport())
        assert ep.url == "/testdata/limits/context/session"

    def test_send_deletes(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import ResetSessionLimitsEndpoint

        fake_transport.enqueue(status_code=200)
        ep = ResetSessionLimitsEndpoint(fake_transport)
        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "DELETE"
        assert call.path == "/testdata/limits/context/session"


# ---------------------------------------------------------------------------
# SetSubjectLimitsEndpoint
# ---------------------------------------------------------------------------


class TestSetSubjectLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import SetSubjectLimitsEndpoint

        ep = SetSubjectLimitsEndpoint(FakeTransport())
        assert ep.url == "/testdata/limits/subject/certificate"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import SetSubjectLimitsEndpoint
        from ksef2.infra.schema.api import spec as spec

        fake_transport.enqueue(status_code=200)
        ep = SetSubjectLimitsEndpoint(fake_transport)

        body = spec.SetSubjectLimitsRequest(
            certificate=spec.CertificateSubjectLimitsOverride(maxCertificates=5)
        )
        ep.send(bearer_token=_TOKEN, body=body)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/limits/subject/certificate"


# ---------------------------------------------------------------------------
# ResetSubjectLimitsEndpoint
# ---------------------------------------------------------------------------


class TestResetSubjectLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import ResetSubjectLimitsEndpoint

        ep = ResetSubjectLimitsEndpoint(FakeTransport())
        assert ep.url == "/testdata/limits/subject/certificate"

    def test_send_deletes(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import ResetSubjectLimitsEndpoint

        fake_transport.enqueue(status_code=200)
        ep = ResetSubjectLimitsEndpoint(fake_transport)
        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "DELETE"
        assert call.path == "/testdata/limits/subject/certificate"


# ---------------------------------------------------------------------------
# SetApiRateLimitsEndpoint
# ---------------------------------------------------------------------------


class TestSetApiRateLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import SetApiRateLimitsEndpoint

        ep = SetApiRateLimitsEndpoint(FakeTransport())
        assert ep.url == "/testdata/rate-limits"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import SetApiRateLimitsEndpoint
        from ksef2.infra.schema.api import spec as spec

        fake_transport.enqueue(status_code=200)
        ep = SetApiRateLimitsEndpoint(fake_transport)

        body = spec.SetRateLimitsRequest(
            rateLimits=spec.ApiRateLimitsOverride(
                onlineSession=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=150, perHour=600
                ),
                batchSession=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=150, perHour=600
                ),
                invoiceSend=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=150, perHour=900
                ),
                invoiceStatus=spec.ApiRateLimitValuesOverride(
                    perSecond=150, perMinute=600, perHour=6000
                ),
                sessionList=spec.ApiRateLimitValuesOverride(
                    perSecond=25, perMinute=50, perHour=300
                ),
                sessionInvoiceList=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=100, perHour=1000
                ),
                sessionMisc=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=600, perHour=6000
                ),
                invoiceMetadata=spec.ApiRateLimitValuesOverride(
                    perSecond=40, perMinute=80, perHour=100
                ),
                invoiceExport=spec.ApiRateLimitValuesOverride(
                    perSecond=20, perMinute=40, perHour=100
                ),
                invoiceExportStatus=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=300, perHour=3000
                ),
                invoiceDownload=spec.ApiRateLimitValuesOverride(
                    perSecond=40, perMinute=80, perHour=320
                ),
                other=spec.ApiRateLimitValuesOverride(
                    perSecond=50, perMinute=150, perHour=600
                ),
            )
        )
        ep.send(bearer_token=_TOKEN, body=body)

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/rate-limits"


# ---------------------------------------------------------------------------
# ResetApiRateLimitsEndpoint
# ---------------------------------------------------------------------------


class TestResetApiRateLimitsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.limits import ResetApiRateLimitsEndpoint

        ep = ResetApiRateLimitsEndpoint(FakeTransport())
        assert ep.url == "/testdata/rate-limits"

    def test_send_deletes(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.limits import ResetApiRateLimitsEndpoint

        fake_transport.enqueue(status_code=200)
        ep = ResetApiRateLimitsEndpoint(fake_transport)
        ep.send(bearer_token=_TOKEN)

        call = fake_transport.calls[0]
        assert call.method == "DELETE"
        assert call.path == "/testdata/rate-limits"
