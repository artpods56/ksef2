from dataclasses import dataclass, field
from enum import Enum


class Environment(Enum):
    PRODUCTION = "https://api.ksef.mf.gov.pl/v2"
    TEST = "https://api-test.ksef.mf.gov.pl/v2"
    DEMO = "https://api-demo.ksef.mf.gov.pl/v2"

    @property
    def base_url(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class TimeoutConfig:
    connect: float = 5.0
    read: float = 30.0
    write: float = 30.0
    pool: float = 5.0


@dataclass(frozen=True, slots=True)
class ConnectionPoolConfig:
    max_connections: int = 100
    max_keepalive_connections: int = 20
    keepalive_expiry: float = 30.0


@dataclass(frozen=True, slots=True)
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 0.5
    max_delay: float = 4.0
    backoff_multiplier: float = 2.0
    retryable_status_codes: tuple[int, ...] = (429, 502, 503, 504)


@dataclass(frozen=True, slots=True)
class TlsConfig:
    verify: bool = True
    ca_bundle_path: str | None = None


@dataclass(frozen=True, slots=True)
class TransportConfig:
    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)
    pool: ConnectionPoolConfig = field(default_factory=ConnectionPoolConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    tls: TlsConfig = field(default_factory=TlsConfig)
    proxy_url: str | None = None
    trust_env: bool = True
    http2: bool = True
