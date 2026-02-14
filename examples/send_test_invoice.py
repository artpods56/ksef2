"""Send a minimal FA3 invoice to the KSeF TEST environment.

This script demonstrates the full flow:
  1. Register a test subject and grant permissions
  2. Authenticate with a self-signed certificate (XAdES)
  3. Build a typed FA3 invoice using xsdata-generated dataclasses
  4. Validate the invoice XML against the FA3 XSD
  5. Open an online session and send the invoice
  6. Clean up (terminate session, delete test subject)

Usage:
    uv run python examples/send_test_invoice.py
"""

from __future__ import annotations

import datetime
from pathlib import Path

from lxml import etree
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate, XmlDateTime

from ksef2 import Client, FormSchema
from ksef2.config import Environment
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)
from ksef2.infra.schema.fa3 import (
    Faktura,
    Podmiot2Gv,
    Podmiot2Jst,
    TkodFormularza,
    TkodKraju,
    TkodWaluty,
    Tnaglowek,
    TnaglowekWariantFormularza,
    Tpodmiot1,
    Tpodmiot2,
    TrodzajFaktury,
    TstawkaPodatku,
    Tadres3,
    Twybor1,
    Twybor12,
)

SELLER_NIP = "1111111111"
BUYER_NIP = "2222222222"

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas" / "FA3"


# ---------------------------------------------------------------------------
# XSD validation helpers
# ---------------------------------------------------------------------------


class _LocalSchemaResolver(etree.Resolver):
    """Resolve imported XSD URLs to local copies in schemas/FA3/."""

    def resolve(self, system_url, public_id, context):  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        if system_url and "/" in system_url:
            filename = system_url.rsplit("/", 1)[-1]
            local = SCHEMAS_DIR / filename
            if local.exists():
                return self.resolve_filename(str(local), context)  # pyright: ignore[reportAttributeAccessIssue]
        return None


def _load_xsd_schema() -> etree.XMLSchema:
    parser = etree.XMLParser()
    parser.resolvers.add(_LocalSchemaResolver())
    doc = etree.parse(str(SCHEMAS_DIR / "schemat.xsd"), parser)
    return etree.XMLSchema(doc)


def validate_invoice_xml(xml_bytes: bytes) -> None:
    schema = _load_xsd_schema()
    doc = etree.fromstring(xml_bytes)
    if not schema.validate(doc):
        errors = "\n".join(str(e) for e in schema.error_log)  # pyright: ignore[reportGeneralTypeIssues]
        raise ValueError(f"Invoice XML is not valid:\n{errors}")


# ---------------------------------------------------------------------------
# Invoice builder
# ---------------------------------------------------------------------------


def build_invoice() -> bytes:
    """Build a minimal valid FA3 invoice and return serialized XML bytes."""
    now = datetime.datetime.now(datetime.timezone.utc)
    today = XmlDate(now.year, now.month, now.day)

    faktura = Faktura(
        naglowek=Tnaglowek(
            kod_formularza=Tnaglowek.KodFormularza(value=TkodFormularza.FA),
            wariant_formularza=TnaglowekWariantFormularza.VALUE_3,
            data_wytworzenia_fa=XmlDateTime(
                now.year,
                now.month,
                now.day,
                now.hour,
                now.minute,
                now.second,
                0,
                0,
            ),
        ),
        podmiot1=Faktura.Podmiot1(
            dane_identyfikacyjne=Tpodmiot1(
                nip=SELLER_NIP,
                nazwa="Test Seller Sp. z o.o.",
            ),
            adres=Tadres3(
                kod_kraju=TkodKraju.PL,
                adres_l1="ul. Testowa 1, 00-001 Warszawa",
            ),
        ),
        podmiot2=Faktura.Podmiot2(
            dane_identyfikacyjne=Tpodmiot2(nip=BUYER_NIP),
            jst=Podmiot2Jst.VALUE_2,
            gv=Podmiot2Gv.VALUE_2,
        ),
        fa=Faktura.Fa(
            kod_waluty=TkodWaluty.PLN,
            p_1=str(today),
            p_2=f"FV/{now.year}/TEST/001",
            p_13_1="1000.00",
            p_14_1="230.00",
            p_15="1230.00",
            adnotacje=Faktura.Fa.Adnotacje(
                p_16=Twybor12.VALUE_2,
                p_17=Twybor12.VALUE_2,
                p_18=Twybor12.VALUE_2,
                p_18_a=Twybor12.VALUE_2,
                zwolnienie=Faktura.Fa.Adnotacje.Zwolnienie(
                    p_19_n=Twybor1.VALUE_1,
                ),
                nowe_srodki_transportu=Faktura.Fa.Adnotacje.NoweSrodkiTransportu(
                    p_22_n=Twybor1.VALUE_1,
                ),
                p_23=Twybor12.VALUE_2,
                pmarzy=Faktura.Fa.Adnotacje.Pmarzy(
                    p_pmarzy_n=Twybor1.VALUE_1,
                ),
            ),
            rodzaj_faktury=TrodzajFaktury.VAT,
            fa_wiersz=[
                Faktura.Fa.FaWiersz(
                    nr_wiersza_fa=1,
                    p_7="Usluga testowa",
                    p_8_b="1",
                    p_9_a="1000.00",
                    p_11="1000.00",
                    p_12=TstawkaPodatku.VALUE_23,
                ),
            ],
        ),
    )

    config = SerializerConfig(xml_declaration=True, pretty_print=True)
    serializer = XmlSerializer(config=config)
    return serializer.render(faktura).encode("utf-8")


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------


def main() -> None:
    client = Client(environment=Environment.TEST)

    # 1. Register test subjects
    print("[1/7] Creating test subjects …")
    client.testdata.create_subject(
        nip=SELLER_NIP,
        subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
        description="SDK test seller",
    )
    client.testdata.create_subject(
        nip=BUYER_NIP,
        subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
        description="SDK test buyer",
    )

    # 2. Grant invoice-write permission for the seller
    print("[2/7] Granting permissions …")
    client.testdata.grant_permissions(
        context=Identifier(type=IdentifierType.NIP, value=SELLER_NIP),
        authorized=Identifier(type=IdentifierType.NIP, value=SELLER_NIP),
        permissions=[
            Permission(
                type=PermissionType.INVOICE_WRITE,
                description="Send invoices",
            ),
        ],
    )

    # 3. Generate a self-signed certificate
    print("[3/7] Generating test certificate …")
    cert, private_key = generate_test_certificate(SELLER_NIP)

    # 4. Authenticate via XAdES
    print("[4/7] Authenticating (XAdES) …")
    tokens = client.auth.authenticate_xades(
        nip=SELLER_NIP,
        cert=cert,
        private_key=private_key,
    )
    access_token = tokens.access_token.token
    print(f"       Token valid until {tokens.access_token.valid_until}")

    # 5. Build and validate the invoice
    print("[5/7] Building invoice …")
    invoice_xml = build_invoice()
    validate_invoice_xml(invoice_xml)
    print("       XSD validation passed")

    # 6. Open session and send
    print("[6/7] Sending invoice …")
    with client.sessions.open_online(
        access_token=access_token,
        form_code=FormSchema.FA3,
    ) as session:
        result = session.send_invoice(invoice_xml)
        print(f"[7/7] Invoice sent! Reference: {result.reference_number}")

    print("Done.")


if __name__ == "__main__":
    main()
