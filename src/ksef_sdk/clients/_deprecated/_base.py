from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ksef_sdk.core._certificates import CertificateStore
    from ksef_sdk.core.http import HttpTransport


class BaseSubClient:
    """Common base for all sub-clients."""

    def __init__(
        self,
        http: HttpTransport,
        certificate_store: CertificateStore,
    ) -> None:
        self._http = http
        self._certificate_store = certificate_store
