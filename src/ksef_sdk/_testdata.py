from __future__ import annotations

from typing import Any

import httpx

from ksef_sdk._environments import Environment
from ksef_sdk.models.testdata import (
    GrantPermissionsRequest,
    RegisterPersonRequest,
    RegisterSubjectRequest,
)


class TestDataClient:
    """Unauthenticated client for KSeF TEST-environment testdata endpoints.

    These endpoints (``/v2/testdata/…``) are only available on the TEST
    environment and allow bootstrapping persons, subjects, and permissions
    for integration testing.
    """

    def __init__(self, env: Environment) -> None:
        if env is not Environment.TEST:
            raise ValueError(
                f"TestDataClient only works with Environment.TEST, got {env!r}"
            )
        # testdata endpoints live under /v2, not /api/v2
        base = env.value.split("/api/")[0]
        self._client = httpx.Client(base_url=base)

    # -- lifecycle --

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> TestDataClient:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # -- endpoints --

    def register_person(self, request: RegisterPersonRequest) -> httpx.Response:
        return self._client.post(
            "/v2/testdata/person",
            json=request.model_dump(by_alias=True),
        )

    def register_subject(self, request: RegisterSubjectRequest) -> httpx.Response:
        return self._client.post(
            "/v2/testdata/subject",
            json=request.model_dump(by_alias=True),
        )

    def grant_permissions(self, request: GrantPermissionsRequest) -> httpx.Response:
        return self._client.post(
            "/v2/testdata/permissions",
            json=request.model_dump(by_alias=True),
        )
