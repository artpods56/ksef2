# Limits and Restrictions

Manage API limits and restrictions for the KSeF system.

## Context Limits

Get the effective limits for the current context (session type limits).

**SDK Endpoint:** `GET /limits/context`

```python
response = client.limits.get_context_limits(access_token=token)
print(response.online_session.max_invoices)
print(response.batch_session.max_invoices)
```

## Subject Limits

Get the effective limits for the current subject (certificate/enrollment limits).

**SDK Endpoint:** `GET /limits/subject`

```python
response = client.limits.get_subject_limits(access_token=token)
print(response.certificate.max_certificates)
print(response.enrollment.max_enrollments)
```

## API Rate Limits

Get the current API rate limits.

**SDK Endpoint:** `GET /rate-limits`

```python
response = client.limits.get_api_rate_limits(access_token=token)
print(response.online_session.per_second)
print(response.batch_session.per_minute)
```

## Test Environment Only

The following endpoints are only available on the TEST environment and allow modifying limits for testing purposes.

The recommended workflow is to **fetch** the current limits, **modify** the values you need, and **post** them back:

### Set Session Limits

**SDK Endpoint:** `POST /testdata/limits/context/session`

```python
# Fetch current limits
limits = client.limits.get_context_limits(access_token=token)

# Modify what you need
limits.online_session.max_invoices = 5000
limits.batch_session.max_invoice_size_mb = 5

# Push back
client.limits.set_session_limits(access_token=token, limits=limits)
```

### Reset Session Limits

**SDK Endpoint:** `DELETE /testdata/limits/context/session`

```python
client.limits.reset_session_limits(access_token=token)
```

### Set Subject Limits

**SDK Endpoint:** `POST /testdata/limits/subject/certificate`

```python
# Fetch current limits
limits = client.limits.get_subject_limits(access_token=token)

# Modify what you need
limits.certificate.max_certificates = 5

# Push back
client.limits.set_subject_limits(access_token=token, limits=limits)
```

### Reset Subject Limits

**SDK Endpoint:** `DELETE /testdata/limits/subject/certificate`

```python
client.limits.reset_subject_limits(access_token=token)
```

### Set API Rate Limits

**SDK Endpoint:** `POST /testdata/rate-limits`

```python
# Fetch current rate limits
limits = client.limits.get_api_rate_limits(access_token=token)

# Modify what you need
limits.invoice_send.per_second = 100
limits.invoice_send.per_minute = 500
limits.online_session.per_hour = 1200

# Push back
client.limits.set_api_rate_limits(access_token=token, limits=limits)
```

### Reset API Rate Limits

**SDK Endpoint:** `DELETE /testdata/rate-limits`

```python
client.limits.reset_api_rate_limits(access_token=token)
```
