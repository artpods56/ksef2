from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class KSeFEnv:
    api_url: str
    testdata_url: str | None = None


class Environment(Enum):
    TEST = KSeFEnv(
        api_url="https://api-test.ksef.mf.gov.pl/api/v2",
        testdata_url="https://api-test.ksef.mf.gov.pl",
    )
    PROD = KSeFEnv(api_url="https://api.ksef.mf.gov.pl/api/v2")
    DEMO = KSeFEnv(api_url="https://api-demo.ksef.mf.gov.pl/api/v2")
    PRODUCTION = PROD

    @property
    def api_url(self) -> str:
        return self.value.api_url

    @property
    def testdata_url(self) -> str | None:
        return self.value.testdata_url
