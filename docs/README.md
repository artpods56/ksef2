# KSeF SDK Documentation

This directory contains the maintained human-facing documentation for the current `ksef2` public API.

## Guides

| Area | What it covers |
|------|----------------|
| [Authentication](guides/authentication.md) | XAdES auth, KSeF token auth, refresh, auth-session management |
| [Invoices](guides/invoices.md) | Sending invoices, session invoice status, metadata queries, exports, downloads |
| [Sessions](guides/sessions.md) | Online session lifecycle, session resume, invoice session history |
| [Tokens](guides/tokens.md) | Generating, listing, checking, and revoking KSeF tokens |
| [Permissions](guides/permissions.md) | Grant, revoke, query, and operation-status flows |
| [Certificates](guides/certificates.md) | Limits, enrollment, query, retrieval, and revocation |
| [Limits](guides/limits.md) | Querying and modifying TEST-environment limits |
| [Test Data](guides/testdata.md) | TEST-environment subjects, people, permissions, attachments, and blocked contexts |

## Example Scripts

Runnable examples live in [`scripts/examples`](../scripts/examples).
The guide pages above link to the most relevant scripts for each area.

Good starting points:

- [`scripts/examples/quickstart.py`](../scripts/examples/quickstart.py)
- [`scripts/examples/invoices/send_query_export_download.py`](../scripts/examples/invoices/send_query_export_download.py)
- [`scripts/examples/session/session_resume.py`](../scripts/examples/session/session_resume.py)

## Reference Material

- [KSeF API docs](https://api-test.ksef.mf.gov.pl/docs/v2)
- [Generated API reference](API_DOCS.md)
- [Release process and versioning policy](releasing.md)
- [Project changelog](../CHANGELOG.md)
