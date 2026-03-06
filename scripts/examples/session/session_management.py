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
    print(f"  Found {len(sessions.items)} session(s)")
    for item in sessions.items:
        print(f"  {item.reference_number} current={item.is_current}")

    # Paginated listing (if many sessions exist)
    # for page in auth.sessions.list(page_size=10):
    #     print(len(page.items))

    # Terminate the current session
    print("Terminating current session ...")
    auth.sessions.terminate_current()
    print("  Current session terminated.")

    # To terminate a specific session by reference number:
    # auth.sessions.close(reference_number="some-reference-number")
    print("Session management complete.")


if __name__ == "__main__":
    main()
