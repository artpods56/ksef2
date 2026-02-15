from __future__ import annotations

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip
from ksef2.core.xades import generate_test_certificate

NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    # Authenticate
    print("Authenticating ...")
    cert, private_key = generate_test_certificate(NIP)
    tokens = client.auth.authenticate_xades(
        nip=NIP,
        cert=cert,
        private_key=private_key,
    )
    access_token = tokens.access_token.token

    # List active sessions
    print("Listing active authentication sessions ...")
    sessions = client.auth.list_active_sessions(access_token=access_token)
    print(f"  Response: {sessions}")

    # Paginated listing (if many sessions exist)
    # sessions = client.auth.list_active_sessions(
    #     access_token=access_token,
    #     page_size=10,
    #     continuation_token=None,  # from previous page
    # )

    # Terminate the current session
    print("Terminating current session ...")
    client.auth.terminate_current_session(access_token=access_token)
    print("  Current session terminated.")

    # To terminate a specific session by reference number:
    # client.auth.terminate_session(
    #     access_token=access_token,
    #     reference_number="some-reference-number",
    # )
    print("Session management complete.")


if __name__ == "__main__":
    main()
