from typing import final

from ksef2.core import middleware
from ksef2.domain.models.limits import ApiRateLimits, ContextLimits, SubjectLimits
from ksef2.endpoints.limits import (
    GetApiRateLimitsEndpoint,
    GetContextLimitsEndpoint,
    GetSubjectLimitsEndpoint,
    ResetApiRateLimitsEndpoint,
    ResetSessionLimitsEndpoint,
    ResetSubjectLimitsEndpoint,
    SetApiRateLimitsEndpoint,
    SetSessionLimitsEndpoint,
    SetSubjectLimitsEndpoint,
)
from ksef2.infra.mappers.limits import (
    ApiRateLimitsMapper,
    ContextLimitsMapper,
    SubjectLimitsMapper,
)


@final
class LimitsService:
    def __init__(self, transport: middleware.KSeFProtocol) -> None:
        self._transport = transport
        self._get_context_limits_ep = GetContextLimitsEndpoint(transport)
        self._get_subject_limits_ep = GetSubjectLimitsEndpoint(transport)
        self._get_api_rate_limits_ep = GetApiRateLimitsEndpoint(transport)
        self._set_session_limits_ep = SetSessionLimitsEndpoint(transport)
        self._reset_session_limits_ep = ResetSessionLimitsEndpoint(transport)
        self._set_subject_limits_ep = SetSubjectLimitsEndpoint(transport)
        self._reset_subject_limits_ep = ResetSubjectLimitsEndpoint(transport)
        self._set_api_rate_limits_ep = SetApiRateLimitsEndpoint(transport)
        self._reset_api_rate_limits_ep = ResetApiRateLimitsEndpoint(transport)

    def get_context_limits(self, *, access_token: str) -> ContextLimits:
        return ContextLimitsMapper.map_response(
            self._get_context_limits_ep.send(bearer_token=access_token)
        )

    def get_subject_limits(self, *, access_token: str) -> SubjectLimits:
        return SubjectLimitsMapper.map_response(
            self._get_subject_limits_ep.send(bearer_token=access_token)
        )

    def get_api_rate_limits(self, *, access_token: str) -> ApiRateLimits:
        return ApiRateLimitsMapper.map_response(
            self._get_api_rate_limits_ep.send(bearer_token=access_token)
        )

    def set_session_limits(self, *, access_token: str, limits: ContextLimits) -> None:
        body = ContextLimitsMapper.map_request(limits)
        self._set_session_limits_ep.send(bearer_token=access_token, body=body)

    def reset_session_limits(self, *, access_token: str) -> None:
        self._reset_session_limits_ep.send(bearer_token=access_token)

    def set_subject_limits(self, *, access_token: str, limits: SubjectLimits) -> None:
        self._set_subject_limits_ep.send(
            bearer_token=access_token, body=SubjectLimitsMapper.map_request(limits)
        )

    def reset_subject_limits(self, *, access_token: str) -> None:
        self._reset_subject_limits_ep.send(bearer_token=access_token)

    def set_api_rate_limits(self, *, access_token: str, limits: ApiRateLimits) -> None:
        self._set_api_rate_limits_ep.send(
            bearer_token=access_token, body=ApiRateLimitsMapper.map_request(limits)
        )

    def reset_api_rate_limits(self, *, access_token: str) -> None:
        self._reset_api_rate_limits_ep.send(bearer_token=access_token)
