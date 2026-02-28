from ksef2.infra.schema.api import spec
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="limit_context_resp")
class EffectiveContextLimitsFactory(ModelFactory[spec.EffectiveContextLimits]): ...


@register_fixture(name="limit_subject_resp")
class EffectiveSubjectLimitsFactory(ModelFactory[spec.EffectiveSubjectLimits]): ...


@register_fixture(name="limit_rate_resp")
class EffectiveApiRateLimitsFactory(ModelFactory[spec.EffectiveApiRateLimits]): ...


@register_fixture(name="limit_set_session_req")
class SetSessionLimitsRequestFactory(ModelFactory[spec.SetSessionLimitsRequest]): ...


@register_fixture(name="limit_set_subject_req")
class SetSubjectLimitsRequestFactory(ModelFactory[spec.SetSubjectLimitsRequest]): ...


@register_fixture(name="limit_set_rate_req")
class SetRateLimitsRequestFactory(ModelFactory[spec.SetRateLimitsRequest]): ...
