from __future__ import annotations

from typing import Any

from ksef_sdk.core.http import HttpTransport
from ksef_sdk.domain.models._deprecated._environments import Environment
from ksef_sdk.domain.models._deprecated.testdata import (
    GrantPermissionsRequest,
    RegisterPersonRequest,
    RegisterSubjectRequest,
)


class TestDataClient:
    """Unauthenticated client for KSeF TEST-environment testdata endpoints.

    These endpoints (``/v2/testdata/...``) are only available on the TEST
    environment and allow bootstrapping persons, subjects, and permissions
    for integration testing.
    """

    def __init__(self, env: Environment) -> None:
        if env.testdata_url is None:
            raise ValueError(
                f"TestDataClient only works with environments that have a testdata_url, got {env!r}"
            )
        self._http = HttpTransport(env, base_url=env.testdata_url)

    # -- lifecycle --

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> TestDataClient:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # -- endpoints --

    def register_person(self, request: RegisterPersonRequest) -> None:
        self._http.post("/v2/testdata/person", body=request)

    def register_subject(self, request: RegisterSubjectRequest) -> None:
        self._http.post("/v2/testdata/subject", body=request)

    def grant_permissions(self, request: GrantPermissionsRequest) -> None:
        self._http.post("/v2/testdata/permissions", body=request)
