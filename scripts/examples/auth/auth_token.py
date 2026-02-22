from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip


from dotenv import load_dotenv

_ = load_dotenv()

NIP = generate_nip()


KSEF_TOKEN = "<your-token-here>"


def main() -> None:
    # you should be able to use any environment here
    client = Client(environment=Environment.TEST)

    print("Authenticating via KSeF token ...")
    auth = client.authentication.with_token(
        ksef_token=KSEF_TOKEN,
        nip=NIP,
    )

    print(f"Access token:  {auth.access_token[:40]}…")
    print(f"  Valid until: {auth.auth_tokens.access_token.valid_until}")
    print(f"Refresh token: {auth.refresh_token[:40]}…")
    print(f"  Valid until: {auth.auth_tokens.refresh_token.valid_until}")


if __name__ == "__main__":
    main()
