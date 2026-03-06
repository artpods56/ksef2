from ksef2 import Client, Environment, FormSchema
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models.session import OnlineSessionState
from ksef2.domain.models.testdata import Identifier, Permission

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        print("Creating test subject ...")
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="Session resume test",
        )

        print("Creating test person ...")
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )

        temp.grant_permissions(
            permissions=[
                Permission(type="invoice_write", description="Send invoices"),
            ],
            grant_to=Identifier(type="nip", value=PERSON_NIP),
            in_context_of=Identifier(type="nip", value=ORG_NIP),
        )

        # we are using self-signed certificate here, this will only work in test environment
        cert, private_key = generate_test_certificate(PERSON_NIP)
        auth = client.authentication.with_xades(
            nip=PERSON_NIP, cert=cert, private_key=private_key
        )
        # Open a session WITHOUT context manager (manual lifecycle)
        print("Opening session (manual mode) ...")
        session = auth.online_session(form_code=FormSchema.FA3)

        # Save the session state so it can be serialized and passed elsewhere.
        state: OnlineSessionState = (
            session.get_state()
        )  # [TODO] state should probably be secured somehow
        state_json = state.model_dump_json()

        print(f"Session state saved ({len(state_json)} bytes)")
        print(f"  Reference: {state.reference_number}")
        print(f"  Valid until: {state.valid_until}")

        # --- Simulate passing state to another process ---
        # In a real app you would store state_json in a database or message queue

        # Resume the session from saved state
        print("Resuming session from saved state ...")
        restored_state = OnlineSessionState.model_validate_json(state_json)
        resumed_session = auth.resume_online_session(state=restored_state)

        # The resumed session can send invoices, download, etc. as long as it is valid
        # Values stored in state should be properly secured
        # resumed_session.send_invoice(invoice_xml)

        # Terminate manually when done
        print("Terminating session ...")
        resumed_session.close()

        print("Session terminated.")


if __name__ == "__main__":
    main()
