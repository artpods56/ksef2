from typing import final

from ksef2.core.protocols import Middleware
from ksef2.domain.models.limits import ApiRateLimits, ContextLimits, SubjectLimits
from ksef2.endpoints.limits import LimitEndpoints
from ksef2.infra.mappers.limits import from_spec, to_spec


@final
class LimitsClient:
    def __init__(self, transport: Middleware) -> None:
        self._endpoints = LimitEndpoints(transport)

    def get_context_limits(self) -> ContextLimits:
        return from_spec(self._endpoints.get_context_limits())

    def get_subject_limits(self) -> SubjectLimits:
        return from_spec(self._endpoints.get_subject_limits())

    def get_api_rate_limits(self) -> ApiRateLimits:
        return from_spec(self._endpoints.get_api_rate_limits())

    def set_session_limits(self, *, limits: ContextLimits) -> None:
        self._endpoints.set_session_limits(body=to_spec(limits))

    def reset_session_limits(self) -> None:
        self._endpoints.reset_session_limits()

    def set_subject_limits(self, *, limits: SubjectLimits) -> None:
        self._endpoints.set_subject_limits(body=to_spec(limits))

    def reset_subject_limits(self) -> None:
        self._endpoints.reset_subject_limits()

    def set_api_rate_limits(self, *, limits: ApiRateLimits) -> None:
        self._endpoints.set_api_rate_limits(body=to_spec(limits))

    def reset_api_rate_limits(self) -> None:
        self._endpoints.reset_api_rate_limits()

    def set_production_rate_limits(self) -> None:
        self._endpoints.set_production_rate_limits()
