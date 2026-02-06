from __future__ import annotations

from enum import Enum


class Environment(Enum):
    PRODUCTION = "https://ksef.mf.gov.pl/api"
    TEST = "https://ksef-test.mf.gov.pl/api"
    DEMO = "https://ksef-demo.mf.gov.pl/api"

    @property
    def base_url(self) -> str:
        return self.value
