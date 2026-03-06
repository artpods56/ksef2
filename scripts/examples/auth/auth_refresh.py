from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate

NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    # First, authenticate to get initial tokens
    print("Authenticating via XAdES ...")
    cert, private_key = generate_test_certificate(NIP)
    auth = client.authentication.with_xades(
        nip=NIP,
        cert=cert,
        private_key=private_key,
    )
    print(f"  Access token valid until:  {auth.auth_tokens.access_token.valid_until}")
    print(f"  Refresh token valid until: {auth.auth_tokens.refresh_token.valid_until}")

    # Refresh the access token
    print("Refreshing access token ...")
    refreshed = client.authentication.refresh(refresh_token=auth.refresh_token)
    print(f"  New access token valid until: {refreshed.access_token.valid_until}")
    print(f"  New access token preview: {refreshed.access_token.token[:40]}…")


if __name__ == "__main__":
    main()
