# KSeF SDK Documentation

This directory contains detailed documentation for the KSeF SDK features.

## Overview

The SDK provides a Python interface to Poland's KSeF (Krajowy System e-Faktur) v2.0 API - the national e-invoicing system.

## Feature Areas

| Area | Description | Guide |
|------|-------------|-------|
| [Authentication](guides/authentication.md) | XAdES, Token-based, Refresh | `/auth/*` |
| [Invoices](guides/invoices.md) | Send, Download, Search | `/online/*` |
| [Sessions](guides/sessions.md) | Session management | `/online/session` |
| [Tokens](guides/tokens.md) | Token generation, refresh, revocation | `/token/manage` |
| [Test Data](guides/testdata.md) | Test environment setup | `/testdata/*` |
| [Limits](guides/limits.md) | API limits and restrictions | `/limits/*`, `/rate-limits` |

## Requirements

### Runtime Requirements
- Python 3.12+
- `cryptography` - for XAdES signing
- `httpx` - for HTTP client
- `signxml` - for XAdES signatures

## API Reference

- [KSeF API Documentation](https://api-test.ksef.mf.gov.pl/docs/v2)
- [OpenAPI Specification](../../openapi.json)
