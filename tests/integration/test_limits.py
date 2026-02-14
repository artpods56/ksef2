from __future__ import annotations

import pytest

from ksef2.domain.models.limits import ApiRateLimits, ContextLimits, SubjectLimits


@pytest.mark.integration
def test_get_context_limits(xades_authenticated_context):
    """Fetch effective context limits."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.limits.get_context_limits(access_token=token)

    assert isinstance(result, ContextLimits)
    assert result.online_session.max_invoices > 0
    assert result.batch_session.max_invoices > 0


@pytest.mark.integration
def test_get_subject_limits(xades_authenticated_context):
    """Fetch effective subject limits."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.limits.get_subject_limits(access_token=token)

    assert isinstance(result, SubjectLimits)


@pytest.mark.integration
def test_get_api_rate_limits(xades_authenticated_context):
    """Fetch effective API rate limits."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    result = client.limits.get_api_rate_limits(access_token=token)

    assert isinstance(result, ApiRateLimits)
    assert result.online_session.per_second > 0
    assert result.invoice_send.per_hour > 0


@pytest.mark.integration
def test_set_session_limits_roundtrip(xades_authenticated_context):
    """Fetch session limits, modify, post back, then reset."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    limits = client.limits.get_context_limits(access_token=token)
    original_max = limits.online_session.max_invoices

    limits.online_session.max_invoices = original_max + 1
    client.limits.set_session_limits(access_token=token, limits=limits)

    updated = client.limits.get_context_limits(access_token=token)
    assert updated.online_session.max_invoices == original_max + 1

    client.limits.reset_session_limits(access_token=token)


@pytest.mark.integration
def test_set_api_rate_limits_roundtrip(xades_authenticated_context):
    """Fetch rate limits, modify, post back, then reset."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    limits = client.limits.get_api_rate_limits(access_token=token)
    original_per_second = limits.invoice_send.per_second

    limits.invoice_send.per_second = (
        original_per_second - 50
    )  # has to be between 1 and 100
    client.limits.set_api_rate_limits(access_token=token, limits=limits)

    updated = client.limits.get_api_rate_limits(access_token=token)
    assert updated.invoice_send.per_second == original_per_second - 50

    client.limits.reset_api_rate_limits(access_token=token)


@pytest.mark.integration
def test_reset_session_limits(xades_authenticated_context):
    """Reset session limits back to defaults."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    client.limits.reset_session_limits(access_token=token)


@pytest.mark.integration
def test_reset_api_rate_limits(xades_authenticated_context):
    """Reset API rate limits back to defaults."""
    client, tokens = xades_authenticated_context
    token = tokens.access_token.token

    client.limits.reset_api_rate_limits(access_token=token)
