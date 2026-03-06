# Changelog

All notable changes to this project should be documented in this file.

The project is currently in the pre-`1.0.0` phase. This changelog starts
tracking the stabilization work leading into `1.0.0`.

## [Unreleased]

### Added

- Explicit `Client.close()` support and sync context-manager lifecycle handling.
- SDK-owned transport configuration via `TransportConfig`, `TimeoutConfig`,
  `ConnectionPoolConfig`, `RetryConfig`, and `TlsConfig`.
- Retry middleware for safe and idempotent requests.
- Dedicated SDK exceptions for closed clients and environment-gated features.
- A documented release workflow and versioning policy in
  [`docs/releasing.md`](docs/releasing.md).

### Changed

- TEST-data operations now reuse the main client transport instead of creating a
  separate internal HTTP client.
- `client.testdata` and `authentication.with_test_certificate()` now raise
  typed SDK exceptions instead of `ValueError`.
- README and guide docs now point to the refactored public API and current
  example scripts.

## [0.8.0]

- Baseline refactored public API before the `1.0.0` stabilization pass.
