from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate

NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    # First, authenticate to get initial tokens
    print("Authenticating via XAdES ...")
    cert, private_key = generate_test_certificate(NIP)
    tokens = client.auth.authenticate_xades(
        nip=NIP,
        cert=cert,
        private_key=private_key,
    )
    print(f"  Access token valid until:  {tokens.access_token.valid_until}")
    print(f"  Refresh token valid until: {tokens.refresh_token.valid_until}")

    # Refresh the access token
    print("Refreshing access token ...")
    refreshed = client.auth.refresh(refresh_token=tokens.refresh_token.token)
    print(f"  New access token valid until: {refreshed.access_token.valid_until}")

    # The new access token can now be used for API calls
    print("Using refreshed token to list active sessions ...")
    sessions = client.auth.list_active_sessions(
        access_token=refreshed.access_token.token,
    )
    print(f"  Active sessions response: {sessions}")


if __name__ == "__main__":
    main()
