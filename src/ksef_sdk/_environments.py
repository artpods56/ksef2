from __future__ import annotations

from enum import Enum


class Environment(Enum):
    PRODUCTION = "https://api.ksef.mf.gov.pl/api/v2"
    TEST = "https://api-test.ksef.mf.gov.pl/api/v2"
    DEMO = "https://api-demo.ksef.mf.gov.pl/api/v2"

    @property
    def base_url(self) -> str:
        return self.value
