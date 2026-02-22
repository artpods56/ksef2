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
    auth = client.authentication.with_xades(
        nip=NIP,
        cert=cert,
        private_key=private_key,
    )

    # List active sessions
    print("Listing active authentication sessions ...")
    sessions = auth.sessions.list_page()
    print(f"  Response: {sessions}")

    # Paginated listing (if many sessions exist)
    # sessions = auth.sessions.list(
    #     page_size=10,
    #     continuation_token=None,  # from previous page
    # )

    # Terminate the current session
    print("Terminating current session ...")
    auth.sessions.terminate_current()
    print("  Current session terminated.")

    # To terminate a specific session by reference number:
    # auth.sessions.terminate(reference_number="some-reference-number")
    print("Session management complete.")


if __name__ == "__main__":
    main()
