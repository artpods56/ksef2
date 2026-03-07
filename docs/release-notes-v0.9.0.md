# ksef2 v0.9.0

`v0.9.0` is a pre-`1.0.0` release focused primarily on developer-experience improvements, API tightening, and release hardening rather than broad new surface area.

This release continues the cleanup of the public SDK facade before `1.0.0`: stricter and more consistent public types, better mapper behavior against real KSeF responses, clearer session and authentication semantics, and a more stable release pipeline.

## Highlights

- Public API typing is more consistent and easier to use, with literal-first public models across sessions, encryption, invoices, permissions, and tokens.
- Authentication response mapping now handles the real KSeF wire-format method codes correctly, which fixes runtime issues that only appeared in integration flows.
- Session history filters preserve compatibility at the client boundary while still normalizing to the public literal-first model internally.
- Documentation and release preparation were tightened up, including an explicit pre-`1.0.0` checklist and refreshed guides/examples.
- Validation is stronger across the board: static type checking is clean, unit coverage remains green, and integration coverage passes end to end.

## Why this is a pre-1.0.0 release

The SDK is very close to a stable `1.0.0` surface, but this release still intentionally sits in the `0.x` range because the project is finishing API-shape cleanup and final contract hardening. Users should expect the interface to be much more stable than earlier releases, but not yet frozen to a `1.0.0` compatibility promise.

## Changelog

See the full change list in [CHANGELOG.md](../CHANGELOG.md).
