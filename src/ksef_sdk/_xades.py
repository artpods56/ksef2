from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509 import Certificate
from cryptography.x509.oid import NameOID, ObjectIdentifier
from lxml import etree
from signxml.algorithms import DigestAlgorithm, SignatureConstructionMethod, SignatureMethod
from signxml.xades.xades import XAdESSigner

from ksef_sdk._auth import poll_auth_status, redeem_token, request_challenge
from ksef_sdk._generated.model import AuthenticationInitResponse

if TYPE_CHECKING:
    from ksef_sdk._http import HttpTransport

# OID 2.5.4.97 = organizationIdentifier (used in company-seal certificates)
_OID_ORGANIZATION_IDENTIFIER = ObjectIdentifier("2.5.4.97")

_AUTH_TOKEN_NS = "http://ksef.mf.gov.pl/auth/token/2.0"


def generate_test_certificate(nip: str) -> tuple[Certificate, RSAPrivateKey]:
    """Generate a self-signed RSA-2048 certificate for XAdES auth on the TEST environment.

    The DN uses the company-seal format matching the Java/C# reference implementations:
    ``2.5.4.97=VATPL-{NIP}, CN=KSeF SDK Test, C=PL``
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "KSeF SDK Test"),
        x509.NameAttribute(_OID_ORGANIZATION_IDENTIFIER, f"VATPL-{nip}"),
        x509.NameAttribute(NameOID.COMMON_NAME, "KSeF SDK Test"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
    ])

    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(hours=1))
        .not_valid_after(now + datetime.timedelta(days=365))
        .sign(private_key, hashes.SHA256())
    )
    return cert, private_key


def build_auth_token_request_xml(
    challenge: str,
    nip: str,
    subject_identifier_type: str = "certificateSubject",
) -> bytes:
    """Build the AuthTokenRequest XML per the XSD ``http://ksef.mf.gov.pl/auth/token/2.0``."""
    nsmap: dict[str | None, str] = {None: _AUTH_TOKEN_NS}
    root = etree.Element(f"{{{_AUTH_TOKEN_NS}}}AuthTokenRequest", nsmap=nsmap)

    etree.SubElement(root, f"{{{_AUTH_TOKEN_NS}}}Challenge").text = challenge

    ctx = etree.SubElement(root, f"{{{_AUTH_TOKEN_NS}}}ContextIdentifier")
    etree.SubElement(ctx, f"{{{_AUTH_TOKEN_NS}}}Nip").text = nip

    etree.SubElement(
        root, f"{{{_AUTH_TOKEN_NS}}}SubjectIdentifierType"
    ).text = subject_identifier_type

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8")


def sign_xades(
    xml_bytes: bytes,
    cert: Certificate,
    private_key: RSAPrivateKey,
) -> bytes:
    """Sign XML with an enveloped XAdES-B signature (RSA-SHA256)."""
    signer = XAdESSigner(
        method=SignatureConstructionMethod.enveloped,
        signature_algorithm=SignatureMethod.RSA_SHA256,
        digest_algorithm=DigestAlgorithm.SHA256,
    )
    root = etree.fromstring(xml_bytes)  # noqa: S320

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )

    signed_root = signer.sign(data=root, key=key_pem, cert=cert_pem)
    return etree.tostring(signed_root, xml_declaration=True, encoding="UTF-8")


def submit_xades_auth(
    http: HttpTransport,
    signed_xml: bytes,
    *,
    verify_chain: bool = False,
) -> AuthenticationInitResponse:
    """``POST /auth/xades-signature`` — submit the signed AuthTokenRequest XML."""
    path = f"/auth/xades-signature?verifyCertificateChain={str(verify_chain).lower()}"
    resp = http.request(
        "POST",
        path,
        raw_body=signed_xml,
        extra_headers={"Content-Type": "application/xml"},
        response_model=AuthenticationInitResponse,
    )
    return resp


def authenticate_xades(
    http: HttpTransport,
    nip: str,
    cert: Certificate,
    private_key: RSAPrivateKey,
    *,
    poll_interval: float = 1.0,
    max_poll_attempts: int = 30,
) -> str:
    """Full XAdES authentication flow: challenge -> build XML -> sign -> submit -> poll -> redeem.

    On success, sets the access token on *http* and returns the refresh token string.
    """
    challenge = request_challenge(http)

    xml_bytes = build_auth_token_request_xml(challenge.challenge, nip)
    signed_xml = sign_xades(xml_bytes, cert, private_key)

    init_resp = submit_xades_auth(http, signed_xml, verify_chain=False)

    # The authenticationToken must be set as Bearer for polling and redeeming.
    http.set_access_token(init_resp.authenticationToken.token)

    _ = poll_auth_status(
        http,
        init_resp.referenceNumber,
        poll_interval=poll_interval,
        max_attempts=max_poll_attempts,
    )

    tokens = redeem_token(http, init_resp.authenticationToken.token)
    http.set_access_token(tokens.accessToken.token)
    return tokens.refreshToken.token
