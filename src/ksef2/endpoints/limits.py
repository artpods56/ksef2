from typing import final

from ksef2.core import headers, codecs, middleware
from ksef2.infra.schema.api import spec as spec


@final
class GetContextLimitsEndpoint:
    url: str = "/limits/context"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> spec.EffectiveContextLimits:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.url,
                headers=headers.KSeFHeaders.bearer(bearer_token),
            ),
            spec.EffectiveContextLimits,
        )


@final
class GetSubjectLimitsEndpoint:
    url: str = "/limits/subject"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> spec.EffectiveSubjectLimits:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.url,
                headers=headers.KSeFHeaders.bearer(bearer_token),
            ),
            spec.EffectiveSubjectLimits,
        )


@final
class GetApiRateLimitsEndpoint:
    url: str = "/rate-limits"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> spec.EffectiveApiRateLimits:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.url,
                headers=headers.KSeFHeaders.bearer(bearer_token),
            ),
            spec.EffectiveApiRateLimits,
        )


@final
class SetSessionLimitsEndpoint:
    url: str = "/testdata/limits/context/session"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(
        self,
        bearer_token: str,
        body: spec.SetSessionLimitsRequest,
    ) -> None:
        _ = self._transport.post(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )


@final
class ResetSessionLimitsEndpoint:
    url: str = "/testdata/limits/context/session"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> None:
        _ = self._transport.delete(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )


@final
class SetSubjectLimitsEndpoint:
    url: str = "/testdata/limits/subject/certificate"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(
        self,
        bearer_token: str,
        body: spec.SetSubjectLimitsRequest,
    ) -> None:
        _ = self._transport.post(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )


@final
class ResetSubjectLimitsEndpoint:
    url: str = "/testdata/limits/subject/certificate"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> None:
        _ = self._transport.delete(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )


@final
class SetApiRateLimitsEndpoint:
    url: str = "/testdata/rate-limits"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(
        self,
        bearer_token: str,
        body: spec.SetRateLimitsRequest,
    ) -> None:
        _ = self._transport.post(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )


@final
class ResetApiRateLimitsEndpoint:
    url: str = "/testdata/rate-limits"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, bearer_token: str) -> None:
        _ = self._transport.delete(
            self.url,
            headers=headers.KSeFHeaders.bearer(bearer_token),
        )
