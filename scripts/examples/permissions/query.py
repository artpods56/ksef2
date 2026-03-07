from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip

ORG_NIP = generate_nip()


def main() -> None:
    client = Client(environment=Environment.TEST)

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="Permission query example",
        )

        auth = client.authentication.with_test_certificate(nip=ORG_NIP)

        print(
            auth.permissions.get_attachment_permission_status().model_dump_json(
                indent=2
            )
        )


if __name__ == "__main__":
    main()
