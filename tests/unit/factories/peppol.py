from ksef2.infra.schema.api import spec
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture(name="peppol_providers_resp")
class QueryPeppolProvidersResponseFactory(
    ModelFactory[spec.QueryPeppolProvidersResponse]
): ...
