import pytest

from ksef2.domain.models.pagination import (
    OffsetPaginationParams,
    PermissionsQueryParams,
    CertificateQueryParams,
    InvoiceQueryParams,
)


@pytest.fixture
def bearer_headers() -> dict[str, str]:
    return {"Authorization": "Bearer <token>"}


@pytest.fixture
def pagination_params() -> OffsetPaginationParams:
    return OffsetPaginationParams()


@pytest.fixture
def permissions_params() -> PermissionsQueryParams:
    return PermissionsQueryParams()


@pytest.fixture
def certificate_params() -> CertificateQueryParams:
    return CertificateQueryParams()


@pytest.fixture
def invoice_params() -> InvoiceQueryParams:
    return InvoiceQueryParams()
