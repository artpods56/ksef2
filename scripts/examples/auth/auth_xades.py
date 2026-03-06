from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip

NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    # Authenticate with XAdES signature
    print("Authenticating via XAdES ...")
    auth = client.authentication.with_test_certificate(nip=NIP)

    print(f"Access token:  {auth.access_token[:40]}…")
    print(f"  Valid until: {auth.auth_tokens.access_token.valid_until}")
    print(f"Refresh token: {auth.refresh_token[:40]}…")
    print(f"  Valid until: {auth.auth_tokens.refresh_token.valid_until}")


if __name__ == "__main__":
    main()
