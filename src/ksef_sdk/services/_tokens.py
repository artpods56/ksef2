from __future__ import annotations

import time
from typing import TYPE_CHECKING, Sequence

from ksef_sdk.infra.schema.model import (
    GenerateTokenRequest,
    GenerateTokenResponse,
    TokenStatusResponse,
)
from ksef_sdk.core.exceptions import KSeFApiError

if TYPE_CHECKING:
    from ksef_sdk.core._http import HttpTransport


def generate_token(
    http: HttpTransport,
    *,
    permissions: Sequence[str],
    description: str,
) -> GenerateTokenResponse:
    """``POST /tokens`` — request generation of a new KSeF token."""
    body = GenerateTokenRequest(permissions=list(permissions), description=description)
    return http.post("/tokens", body=body, response_model=GenerateTokenResponse)


def get_token_status(
    http: HttpTransport,
    reference_number: str,
) -> TokenStatusResponse:
    """``GET /tokens/{referenceNumber}`` — get the current status of a token."""
    return http.get(
        f"/tokens/{reference_number}",
        response_model=TokenStatusResponse,
    )


def poll_token_status(
    http: HttpTransport,
    reference_number: str,
    *,
    poll_interval: float = 1.0,
    max_attempts: int = 60,
) -> TokenStatusResponse:
    """Poll ``GET /tokens/{referenceNumber}`` until the token becomes ``Active``.

    Raises :class:`KsefApiError` if the token transitions to ``Failed``.
    """
    for _ in range(max_attempts):
        status = get_token_status(http, reference_number)
        if status.status == "Active":
            return status
        if status.status in ("Failed", "Revoked"):
            raise KSeFApiError(
                0,
                f"Token activation failed: status={status.status}",
            )
        time.sleep(poll_interval)

    raise KSeFApiError(
        0, f"Token activation polling timed out after {max_attempts} attempts"
    )


def revoke_token(
    http: HttpTransport,
    reference_number: str,
) -> None:
    """``DELETE /tokens/{referenceNumber}`` — revoke a KSeF token."""
    http.request("DELETE", f"/tokens/{reference_number}")
