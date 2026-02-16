import time

from ksef2 import Client, Environment, FormSchema
from ksef2.core.tools import generate_nip, generate_pesel
from ksef2.core.xades import generate_test_certificate
from ksef2.domain.models import (
    AuthorizationPermissionType,
    AuthorizationSubjectIdentifierType,
    EntityPermission,
    EntityPermissionType,
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
)
from ksef2.domain.models.invoices import PaginationParams
from ksef2.domain.models.permissions import (
    AuthorizationPermissionsQueryRequest,
    EuEntityPermissionsQueryRequest,
    PersonalPermissionsQueryRequest,
    PersonPermissionsQueryRequest,
    PermissionsQueryType,
    PermissionState,
    QueryType,
    SubordinateEntityRolesQueryRequest,
    SubunitPermissionsQueryRequest,
)

ORG_NIP = generate_nip()
PERSON_NIP = generate_nip()
PERSON_PESEL = generate_pesel()
PARTNER_NIP = generate_nip()

client = Client(environment=Environment.TEST)


def main():
    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=ORG_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="SDK test org",
        )
        temp.create_subject(
            nip=PARTNER_NIP,
            subject_type=SubjectType.ENFORCEMENT_AUTHORITY,
            description="SDK test partner",
        )
        temp.create_person(
            nip=PERSON_NIP,
            pesel=PERSON_PESEL,
            description="Example person",
        )
        temp.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value=ORG_NIP),
            authorized=Identifier(type=IdentifierType.NIP, value=PERSON_NIP),
            permissions=[
                Permission(
                    type=PermissionType.CREDENTIALS_MANAGE,
                    description="Manage credentials",
                ),
                Permission(
                    type=PermissionType.INVOICE_READ,
                    description="Read invoices",
                ),
            ],
        )

        cert, private_key = generate_test_certificate(ORG_NIP)

        tokens = client.auth.authenticate_xades(
            nip=ORG_NIP,
            cert=cert,
            private_key=private_key,
        )
        access_token = tokens.access_token.token

        with client.sessions.open_online(
            access_token=access_token, form_code=FormSchema.FA3
        ) as session:
            # Grant some permissions so there's data to query
            _ = session.permissions.grant_entity(
                subject_value=PARTNER_NIP,
                permissions=[
                    EntityPermission(
                        type=EntityPermissionType.INVOICE_READ, can_delegate=False
                    ),
                ],
                description="Partner invoice read access",
                entity_name="Test Partner Entity",
            )
            _ = session.permissions.grant_authorization(
                subject_type=AuthorizationSubjectIdentifierType.NIP,
                subject_value=PARTNER_NIP,
                permission=AuthorizationPermissionType.SELF_INVOICING,
                description="Self-invoicing authorization",
                entity_name="Test Partner Entity",
            )
            _ = session.permissions.grant_person(
                subject_identifier=IdentifierType.PESEL,
                subject_value=PERSON_PESEL,
                permissions=[PermissionType.INVOICE_READ, PermissionType.INVOICE_WRITE],
                description="Person invoice access",
                first_name="John",
                last_name="Doe",
            )

            time.sleep(5)

            print("Get all persons permissions ...")
            resp = session.permissions.query_persons(
                query=PersonPermissionsQueryRequest(
                    query_type=PermissionsQueryType.PERMISSIONS_IN_CURRENT_CONTEXT,
                ),
            )
            print(resp.model_dump_json(indent=2))

            print("Get persons permissions with credentials manage permission ...")
            resp = session.permissions.query_persons(
                query=PersonPermissionsQueryRequest(
                    query_type=PermissionsQueryType.PERMISSIONS_IN_CURRENT_CONTEXT,
                    permission_types=[PermissionType.CREDENTIALS_MANAGE],
                ),
            )
            print(resp.model_dump_json(indent=2))

            print("Query granted authorizations ...")
            resp = session.permissions.query_authorizations(
                query=AuthorizationPermissionsQueryRequest(
                    query_type=QueryType.GRANTED,
                ),
            )
            print(resp.model_dump_json(indent=2))

            print("Query received authorizations ...")
            resp = session.permissions.query_personal(
                query=PersonalPermissionsQueryRequest(),
            )
            print(resp.model_dump_json(indent=2))

            print("Query active personal permissions ...")
            resp = session.permissions.query_personal(
                query=PersonalPermissionsQueryRequest(
                    permission_state=PermissionState.ACTIVE,
                ),
            )
            print(resp.model_dump_json(indent=2))

            print("Query EU entities ...")
            resp = session.permissions.query_eu_entities(
                query=EuEntityPermissionsQueryRequest(),
            )
            print(resp.model_dump_json(indent=2))

            print("Query subordinate entities ...")
            resp = session.permissions.query_subordinate_entities(
                query=SubordinateEntityRolesQueryRequest(),
            )
            print(resp.model_dump_json(indent=2))

            print("Query subunits ...")
            resp = session.permissions.query_subunits(
                query=SubunitPermissionsQueryRequest(),
            )
            print(resp.model_dump_json(indent=2))

            print("Query authorizations (received, page_size=20) ...")
            resp = session.permissions.query_authorizations(
                query=AuthorizationPermissionsQueryRequest(
                    query_type=QueryType.RECEIVED,
                ),
                params=PaginationParams(page_offset=0, page_size=20),
            )
            print(resp.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
