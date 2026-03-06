"""Limits endpoints for managing KSeF limits."""

from typing import final

from ksef2.core import routes
from ksef2.endpoints.base import BaseEndpoints
from ksef2.infra.schema.api import spec


@final
class LimitEndpoints(BaseEndpoints):
    def get_context_limits(self) -> spec.EffectiveContextLimits:
        return self._parse(
            self._transport.get(
                path=routes.LimitRoutes.GET_CONTEXT_LIMITS,
            ),
            spec.EffectiveContextLimits,
        )

    def get_subject_limits(self) -> spec.EffectiveSubjectLimits:
        return self._parse(
            self._transport.get(
                path=routes.LimitRoutes.GET_SUBJECT_LIMITS,
            ),
            spec.EffectiveSubjectLimits,
        )

    def get_api_rate_limits(self) -> spec.EffectiveApiRateLimits:
        return self._parse(
            self._transport.get(
                path=routes.LimitRoutes.GET_API_RATE_LIMITS,
            ),
            spec.EffectiveApiRateLimits,
        )

    def set_session_limits(self, body: spec.SetSessionLimitsRequest) -> None:
        _ = self._transport.post(
            path=routes.LimitRoutes.SET_SESSION_LIMITS,
            json=body.model_dump(mode="json", by_alias=True),
        )

    def reset_session_limits(self) -> None:
        _ = self._transport.delete(
            path=routes.LimitRoutes.RESET_SESSION_LIMITS,
        )

    def set_subject_limits(self, body: spec.SetSubjectLimitsRequest) -> None:
        _ = self._transport.post(
            path=routes.LimitRoutes.SET_SUBJECT_LIMITS,
            json=body.model_dump(mode="json", by_alias=True),
        )

    def reset_subject_limits(self) -> None:
        _ = self._transport.delete(
            path=routes.LimitRoutes.RESET_SUBJECT_LIMITS,
        )

    def set_api_rate_limits(self, body: spec.SetRateLimitsRequest) -> None:
        _ = self._transport.post(
            path=routes.LimitRoutes.SET_API_RATE_LIMITS,
            json=body.model_dump(mode="json", by_alias=True),
        )

    def reset_api_rate_limits(self) -> None:
        _ = self._transport.delete(
            path=routes.LimitRoutes.RESET_API_RATE_LIMITS,
        )

    def set_production_rate_limits(self) -> None:
        _ = self._transport.post(
            path=routes.LimitRoutes.SET_PRODUCTION_RATE_LIMITS,
        )
