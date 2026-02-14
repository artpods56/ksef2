from enum import Enum


class Environment(Enum):
    PRODUCTION = "https://api.ksef.mf.gov.pl/v2"
    TEST = "https://api-test.ksef.mf.gov.pl/v2"
    DEMO = "https://api-demo.ksef.mf.gov.pl/v2"

    @property
    def base_url(self) -> str:
        return self.value

    @property
    def testdata_base_url(self) -> str | None:
        """Only TEST has testdata endpoints."""
        if self == Environment.TEST:
            return "https://api-test.ksef.mf.gov.pl/v2"
        return None
