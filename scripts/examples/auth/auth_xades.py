from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate

NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    # Generate a self-signed certificate (TEST environment only)
    print("Generating self-signed certificate ...")
    cert, private_key = generate_test_certificate(NIP)

    # Authenticate with XAdES signature
    print("Authenticating via XAdES ...")
    tokens = client.auth.authenticate_xades(
        nip=NIP,
        cert=cert,
        private_key=private_key,
        # verify_chain=False is the default — required for self-signed certs
    )

    print(f"Access token:  {tokens.access_token.token[:40]}…")
    print(f"  Valid until: {tokens.access_token.valid_until}")
    print(f"Refresh token: {tokens.refresh_token.token[:40]}…")
    print(f"  Valid until: {tokens.refresh_token.valid_until}")


if __name__ == "__main__":
    main()
