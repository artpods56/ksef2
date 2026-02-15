from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate

VALID_NIP = generate_nip()


TEMPLATES_DIR = (
    Path(__file__).resolve().parent.parent / "docs" / "assets" / "sample_invoices"
)
INVOICE_TEMPLATE_NAME = "invoice-template-fa-3-with-custom-subject_2.xml"
INVOICE_TEMPLATE_PATH = TEMPLATES_DIR / INVOICE_TEMPLATE_NAME


def main() -> None:

    client = Client(Environment.TEST)

    # XAdES Authentication (TEST environment) - generates self-signed certificate automatically
    cert, private_key = generate_test_certificate(VALID_NIP)
    tokens = client.auth.authenticate_xades(
        nip=VALID_NIP,
        cert=cert,
        private_key=private_key,
    )

    # sessions are context managers, and will automatically terminate on exit
    with client.sessions.open_online(
        access_token=tokens.access_token.token,
        form_code=FormSchema.FA3,
    ) as session:
        with open(INVOICE_TEMPLATE_PATH, "rb") as f:
            result = session.send_invoice(f.read())
        print(result.reference_number)

    # Sessions also support manual management:
    session = client.sessions.open_online(
        access_token=tokens.access_token.token,
        form_code=FormSchema.FA3,
    )
    try:
        with open(INVOICE_TEMPLATE_PATH, "rb") as f:
            result = session.send_invoice(f.read())
        print(result.reference_number)
    finally:
        session.terminate()


if __name__ == "__main__":
    main()
