import time

from ksef2 import Client, Environment
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import EntityPermission, Identifier, Permission
from ksef2.domain.models.pagination import OffsetPaginationParams
from ksef2.domain.models.permissions import (
    AuthorizationPermissionsQuery,
    EuEntityPermissionsQuery,
    PersonalPermissionsQuery,
    PersonPermissionsQuery,
    SubordinateEntityRolesQuery,
    SubunitPermissionsQuery,
)

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()
PARTNER_NIP = generate_nip()

client = Client(environment=Environment.TEST)


def main() -> None:
    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type="enforcement_authority",
            description="SDK test org",
        )
        temp.create_subject(
            nip=PARTNER_NIP,
            subject_type="enforcement_authority",
            description="SDK test partner",
        )
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )
        temp.grant_permissions(
            permissions=[
                Permission(
                    type="credentials_manage",
                    description="Manage credentials",
                ),
                Permission(
                    type="invoice_read",
                    description="Read invoices",
                ),
            ],
            grant_to=Identifier(type="nip", value=PERSON_NIP),
            in_context_of=Identifier(type="nip", value=ORG_NIP),
        )

        cert, private_key = generate_test_certificate(ORG_NIP)

        # Authenticate - no session needed for permission operations
        auth = client.authentication.with_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )

        # Grant some permissions so there is data to query.
        _ = auth.permissions.grant_entity(
            subject_value=PARTNER_NIP,
            permissions=[
                EntityPermission(type="invoice_read", can_delegate=False),
            ],
            description="Partner invoice read access",
            entity_name="Test Partner Entity",
        )
        _ = auth.permissions.grant_authorization(
            subject_type="nip",
            subject_value=PARTNER_NIP,
            permission="self_invoicing",
            description="Self-invoicing authorization",
            entity_name="Test Partner Entity",
        )
        _ = auth.permissions.grant_person(
            subject_type="pesel",
            subject_value=PERSON_PESEL,
            permissions=["invoice_read", "invoice_write"],
            description="Person invoice access",
            first_name="John",
            last_name="Doe",
        )

        time.sleep(5)

        print("Get all persons permissions ...")
        resp = auth.permissions.query_persons(
            query=PersonPermissionsQuery(
                query_type="in_context",
            ),
        )
        print(resp.model_dump_json(indent=2))

        print("Get persons permissions with credentials manage permission ...")
        resp = auth.permissions.query_persons(
            query=PersonPermissionsQuery(
                query_type="in_context",
                permission_types=["credentials_manage"],
            ),
        )
        print(resp.model_dump_json(indent=2))

        print("Query granted authorizations ...")
        resp = auth.permissions.query_authorizations(
            query=AuthorizationPermissionsQuery(
                query_type="granted",
            ),
        )
        print(resp.model_dump_json(indent=2))

        print("Query received authorizations ...")
        resp = auth.permissions.query_personal(
            query=PersonalPermissionsQuery(),
        )
        print(resp.model_dump_json(indent=2))

        print("Query active personal permissions ...")
        resp = auth.permissions.query_personal(
            query=PersonalPermissionsQuery(
                permission_state="active",
            ),
        )
        print(resp.model_dump_json(indent=2))

        print("Query EU entities ...")
        resp = auth.permissions.query_eu_entities(
            query=EuEntityPermissionsQuery(),
        )
        print(resp.model_dump_json(indent=2))

        print("Query subordinate entities ...")
        resp = auth.permissions.query_subordinate_entities(
            query=SubordinateEntityRolesQuery(),
        )
        print(resp.model_dump_json(indent=2))

        print("Query subunits ...")
        resp = auth.permissions.query_subunits(
            query=SubunitPermissionsQuery(),
        )
        print(resp.model_dump_json(indent=2))

        print("Query authorizations (received, page_size=20) ...")
        resp = auth.permissions.query_authorizations(
            query=AuthorizationPermissionsQuery(
                query_type="received",
            ),
            params=OffsetPaginationParams(page_offset=0, page_size=20),
        )
        print(resp.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
