# Certificates

Manage KSeF certificates for authentication and offline invoice signing.

## Certificate Types

| Type | Description |
|------|-------------|
| `AUTHENTICATION` | Certificate used for authentication in the KSeF system |
| `OFFLINE` | Certificate used for confirming authenticity and integrity of offline invoices |

---

## Operations

All certificate operations are accessed through the authenticated client via `auth.certificates`.

### Get Certificate Limits

Get information about certificate limits and whether you can request a new certificate.

**SDK Endpoint:** `GET /certificates/limits`

```python
# After authenticating:
auth = client.auth.authenticate_xades(nip=NIP, cert=cert, private_key=private_key)

limits = auth.certificates.get_limits()

print(f"Can request new certificate: {limits.can_request}")
print(f"Enrollment limit: {limits.enrollment.remaining}/{limits.enrollment.limit}")
print(f"Certificate limit: {limits.certificate.remaining}/{limits.certificate.limit}")
```

---

### Get Enrollment Data

Get data required for preparing a PKCS#10 Certificate Signing Request (CSR).

**SDK Endpoint:** `GET /certificates/enrollments/data`

**Note:** This endpoint requires authentication with a qualified certificate (not self-signed).

```python
enrollment_data = auth.certificates.get_enrollment_data()

print(f"Common Name: {enrollment_data.common_name}")
print(f"Country: {enrollment_data.country_name}")
print(f"Organization: {enrollment_data.organization_name}")
print(f"Unique ID: {enrollment_data.unique_identifier}")
```

---

### Enroll Certificate

Submit a certificate enrollment request.

**SDK Endpoint:** `POST /certificates/enrollments`

**Requirements:**
- Authentication with a qualified certificate
- Available enrollment quota

```python
from ksef2.domain.models.certificates import CertificateType

# Submit enrollment with your CSR (Base64-encoded DER format)
result = auth.certificates.enroll(
    certificate_name="My Authentication Certificate",
    certificate_type=CertificateType.AUTHENTICATION,
    csr=base64_encoded_csr,
    valid_from=None,  # Optional: defaults to immediate validity
)

print(f"Reference number: {result.reference_number}")
print(f"Submitted at: {result.timestamp}")
```

---

### Get Enrollment Status

Check the status of a certificate enrollment request.

**SDK Endpoint:** `GET /certificates/enrollments/{referenceNumber}`

**Status Codes:**
| Code | Description |
|------|-------------|
| 100 | Request accepted for processing |
| 200 | Request processed (certificate generated) |
| 400 | Request rejected |
| 500 | Unknown error |
| 550 | Operation cancelled by system |

```python
status = auth.certificates.get_enrollment_status(
    reference_number=result.reference_number,
)

print(f"Request date: {status.request_date}")
print(f"Status: {status.status.code} - {status.status.description}")
if status.certificate_serial_number:
    print(f"Certificate serial: {status.certificate_serial_number}")
```

---

### Query Certificates

Query certificates matching specified criteria.

**SDK Endpoint:** `POST /certificates/query`

```python
from ksef2.domain.models.certificates import CertificateStatus, CertificateType

# Query all certificates
response = auth.certificates.query()

for cert in response.certificates:
    print(f"{cert.certificate_serial_number}: {cert.name} ({cert.status.value})")

# Filter by status
response = auth.certificates.query(status=CertificateStatus.ACTIVE)

# Filter by type
response = auth.certificates.query(certificate_type=CertificateType.AUTHENTICATION)

# Filter by name (partial match)
response = auth.certificates.query(name="My Cert")

# With pagination
response = auth.certificates.query(page_size=20, page_offset=0)
```

---

### Retrieve Certificates

Download certificates by their serial numbers.

**SDK Endpoint:** `POST /certificates/retrieve`

```python
# Retrieve up to 10 certificates
response = auth.certificates.retrieve(
    certificate_serial_numbers=["0321C82DA41B4362", "0321F21DA462A362"],
)

for cert in response.certificates:
    print(f"{cert.certificate_serial_number}: {cert.certificate_name}")
    print(f"Type: {cert.certificate_type.value}")
    # cert.certificate contains Base64-encoded DER data
```

---

### Revoke Certificate

Revoke a certificate by its serial number.

**SDK Endpoint:** `POST /certificates/{certificateSerialNumber}/revoke`

```python
from ksef2.domain.models.certificates import CertificateRevocationReason

# Revoke without reason
auth.certificates.revoke(certificate_serial_number="0321C82DA41B4362")

# Revoke with reason
auth.certificates.revoke(
    certificate_serial_number="0321C82DA41B4362",
    revocation_reason=CertificateRevocationReason.KEY_COMPROMISE,
)
```

---

## Certificate Statuses

| Status | Description |
|--------|-------------|
| `ACTIVE` | Certificate is active and can be used |
| `BLOCKED` | Certificate is blocked (transitional state during revocation) |
| `REVOKED` | Certificate has been revoked |
| `EXPIRED` | Certificate has expired |

---

## Revocation Reasons

| Reason | Description |
|--------|-------------|
| `UNSPECIFIED` | No specific reason |
| `SUPERSEDED` | Certificate replaced by another |
| `KEY_COMPROMISE` | Private key has been compromised |

---

## Subject Identifier Types

| Type | Description |
|------|-------------|
| `NIP` | Polish tax identification number (10 digits) |
| `PESEL` | Polish personal identification number (11 digits) |
| `FINGERPRINT` | Certificate fingerprint |

---

## Full Example

Complete certificate lifecycle — query, check limits, and manage certificates:

```python
from ksef2 import Client, Environment
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.certificates import (
    CertificateStatus,
    CertificateType,
)

NIP = "1234567890"
client = Client(environment=Environment.TEST)

cert, private_key = generate_test_certificate(NIP)
auth = client.auth.authenticate_xades(nip=NIP, cert=cert, private_key=private_key)

# Check certificate limits
limits = auth.certificates.get_limits()
print(f"Can request: {limits.can_request}")
print(f"Certificates remaining: {limits.certificate.remaining}/{limits.certificate.limit}")

# Query active authentication certificates
response = auth.certificates.query(
    status=CertificateStatus.ACTIVE,
    certificate_type=CertificateType.AUTHENTICATION,
)
print(f"Found {len(response.certificates)} active auth certificates")

for cert in response.certificates:
    print(f"  {cert.name}")
    print(f"    Serial: {cert.certificate_serial_number}")
    print(f"    Valid: {cert.valid_from} to {cert.valid_to}")
    print(f"    Last used: {cert.last_use_date}")

# Download certificate data if needed
if response.certificates:
    serial = response.certificates[0].certificate_serial_number
    certs = auth.certificates.retrieve(certificate_serial_numbers=[serial])
    print(f"Downloaded {len(certs.certificates)} certificate(s)")
```

---

## Related

- [Authentication](authentication.md) - Using certificates for authentication
- [Limits](limits.md) - Managing certificate and enrollment limits
