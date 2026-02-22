from __future__ import annotations

from typing import final

from ksef2.core import protocols
from ksef2.domain.models.limits import ApiRateLimits, ContextLimits, SubjectLimits
from ksef2.endpoints.limits import (
    GetApiRateLimitsEndpoint,
    GetContextLimitsEndpoint,
    GetSubjectLimitsEndpoint,
    ResetApiRateLimitsEndpoint,
    ResetSessionLimitsEndpoint,
    ResetSubjectLimitsEndpoint,
    SetApiRateLimitsEndpoint,
    SetProductionRateLimitsEndpoint,
    SetSessionLimitsEndpoint,
    SetSubjectLimitsEndpoint,
)
from ksef2.infra.mappers.requests.limits import (
    ApiRateLimitsMapper,
    ContextLimitsMapper,
    SubjectLimitsMapper,
)


@final
class LimitsService:
    """Limits service for querying and modifying API limits.

    This service can be instantiated with either:
    - An access token string (for use with AuthenticatedClient)
    - Will automatically use the token for all operations.
    """

    def __init__(self, transport: protocols.Middleware, access_token: str) -> None:
        self._access_token = access_token
        self._get_context_limits_ep = GetContextLimitsEndpoint(transport)
        self._get_subject_limits_ep = GetSubjectLimitsEndpoint(transport)
        self._get_api_rate_limits_ep = GetApiRateLimitsEndpoint(transport)
        self._set_session_limits_ep = SetSessionLimitsEndpoint(transport)
        self._reset_session_limits_ep = ResetSessionLimitsEndpoint(transport)
        self._set_subject_limits_ep = SetSubjectLimitsEndpoint(transport)
        self._reset_subject_limits_ep = ResetSubjectLimitsEndpoint(transport)
        self._set_api_rate_limits_ep = SetApiRateLimitsEndpoint(transport)
        self._reset_api_rate_limits_ep = ResetApiRateLimitsEndpoint(transport)
        self._set_production_rate_limits_ep = SetProductionRateLimitsEndpoint(transport)

    def get_context_limits(self) -> ContextLimits:
        """Get the effective limits for the current context (session type limits)."""
        return ContextLimitsMapper.map_response(
            self._get_context_limits_ep.send(bearer_token=self._access_token)
        )

    def get_subject_limits(self) -> SubjectLimits:
        """Get the effective limits for the current subject (certificate/enrollment)."""
        return SubjectLimitsMapper.map_response(
            self._get_subject_limits_ep.send(bearer_token=self._access_token)
        )

    def get_api_rate_limits(self) -> ApiRateLimits:
        """Get the current API rate limits."""
        return ApiRateLimitsMapper.map_response(
            self._get_api_rate_limits_ep.send(bearer_token=self._access_token)
        )

    def set_session_limits(self, *, limits: ContextLimits) -> None:
        """Set session limits (test environment only)."""
        body = ContextLimitsMapper.map_request(limits)
        self._set_session_limits_ep.send(bearer_token=self._access_token, body=body)

    def reset_session_limits(self) -> None:
        """Reset session limits to defaults (test environment only)."""
        self._reset_session_limits_ep.send(bearer_token=self._access_token)

    def set_subject_limits(self, *, limits: SubjectLimits) -> None:
        """Set subject limits (test environment only)."""
        self._set_subject_limits_ep.send(
            bearer_token=self._access_token,
            body=SubjectLimitsMapper.map_request(limits),
        )

    def reset_subject_limits(self) -> None:
        """Reset subject limits to defaults (test environment only)."""
        self._reset_subject_limits_ep.send(bearer_token=self._access_token)

    def set_api_rate_limits(self, *, limits: ApiRateLimits) -> None:
        """Set API rate limits (test environment only)."""
        self._set_api_rate_limits_ep.send(
            bearer_token=self._access_token,
            body=ApiRateLimitsMapper.map_request(limits),
        )

    def reset_api_rate_limits(self) -> None:
        """Reset API rate limits to defaults (test environment only)."""
        self._reset_api_rate_limits_ep.send(bearer_token=self._access_token)

    def set_production_rate_limits(self) -> None:
        """Set API rate limits to production values (test environment only)."""
        self._set_production_rate_limits_ep.send(bearer_token=self._access_token)
