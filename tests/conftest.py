from __future__ import annotations

import base64
import textwrap

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime


@pytest.fixture()
def rsa_key_pair():
    """Generate a 2048-bit RSA key pair for testing."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key


@pytest.fixture()
def self_signed_cert_b64(rsa_key_pair):
    """Return a Base64-encoded DER self-signed certificate."""
    private_key = rsa_key_pair
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "KSeF Test"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))
        .sign(private_key, hashes.SHA256())
    )
    return base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode()


@pytest.fixture()
def sample_certificates(self_signed_cert_b64):
    """Return a list of PublicKeyCertificate models usable in tests."""
    from ksef_sdk._generated.model import PublicKeyCertificate
    import datetime as dt

    now = dt.datetime.now(dt.timezone.utc)
    # Use model_construct to bypass Base64Str validation — DER bytes aren't valid UTF-8
    return [
        PublicKeyCertificate.model_construct(
            certificate=self_signed_cert_b64,
            validFrom=now,
            validTo=now + dt.timedelta(days=365),
            usage=["KsefTokenEncryption", "SymmetricKeyEncryption"],
        ),
    ]


SAMPLE_INVOICE_XML = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <Faktura xmlns="http://crd.gov.pl/wzor/2021/11/29/11089/">
        <Naglowek><KodFormularza>FA</KodFormularza></Naglowek>
    </Faktura>
""").encode()
