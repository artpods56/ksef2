# Releasing

This project already publishes to PyPI from version tags matching `v*`. This
document defines how to use that flow consistently while the SDK is being
stabilized for `1.0.0`.

## Versioning Policy

### Before `1.0.0`

- Use `0.x.y` versions for all releases from the stabilization branch.
- Treat `0.x` minor releases as allowed to contain breaking API changes.
- Treat patch releases as bug fixes, documentation fixes, test fixes, and
  non-breaking polish.
- Document every public-facing change in [`CHANGELOG.md`](../CHANGELOG.md).
- Add migration notes to the changelog whenever a release changes public names,
  signatures, behavior, or documented workflows.

### Starting at `1.0.0`

- Follow SemVer for the documented public API.
- Breaking changes require a major version bump.
- New backward-compatible capabilities use a minor version bump.
- Backward-compatible bug fixes use a patch version bump.

## Public API Surface for `1.0.0`

The `1.0.0` compatibility promise should cover:

- Top-level exports from `ksef2`
- Public client entry points documented in [`README.md`](../README.md)
- Guide workflows in [`docs/guides`](guides)
- Runnable example scripts referenced from the README and guide docs

Internal implementation details under `infra`, codegen artifacts, and
undocumented helper modules can still evolve as needed, but they should not be
presented as stable extension points unless explicitly documented.

## Pre-Release Checklist

Run this checklist before cutting any pre-`1.0.0` release:

1. Update [`CHANGELOG.md`](../CHANGELOG.md) from `Unreleased`.
2. Bump the package version in [`pyproject.toml`](../pyproject.toml) and
   [`src/ksef2/__init__.py`](../src/ksef2/__init__.py).
3. Verify README and guide examples still match the current public API.
4. Run `just release-check`.
5. Build distributable artifacts with `uv build`.
6. If the release changes documented behavior, add migration notes to the
   changelog entry.
7. Commit the version bump and changelog update.
8. Create and push a version tag in the form `vX.Y.Z`.

## `1.0.0` Release Gate

Do not cut `1.0.0` until these are true:

1. The current public API shape is intentionally frozen.
2. Remaining docs and examples are current and link-checked.
3. Release notes include migration guidance from the last pre-`1.0.0` release.
4. CI covers lint, format, type checks, unit tests, and the package build.
5. The documented support policy is explicit:
   current Python floor is `3.12+`
6. Risky behavior is documented, especially retry semantics and invoice-send
   failure handling.
7. The changelog is complete enough to explain the final pre-`1.0.0` deltas.

## Suggested Release Flow

### Pre-`1.0.0` release from this branch

1. Finish the feature or stabilization batch.
2. Move `Unreleased` notes into a new `0.x.y` section in
   [`CHANGELOG.md`](../CHANGELOG.md).
3. Bump versions.
4. Run the release checks and build.
5. Push the branch.
6. Tag `v0.x.y` and push the tag.

### `1.0.0` release

1. Freeze the public API and docs.
2. Write explicit migration notes from the final `0.x.y` release.
3. Convert `Unreleased` into the `1.0.0` changelog entry.
4. Bump versions to `1.0.0`.
5. Run release checks and build.
6. Tag `v1.0.0` and push the tag.
