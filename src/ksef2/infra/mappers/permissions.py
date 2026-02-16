from ksef2.domain.models.permissions import (
    AuthorizationGrantDetail,
    AuthorizationPermissionsQueryRequest,
    AuthorizationPermissionsQueryResponse,
    AuthorizationPermissionType,
    AuthorizationSubjectIdentifierType,
    AttachmentPermissionStatus,
    EntityPermission,
    EntityRole,
    EntityRolesResponse,
    EuEntityAdminContextIdentifierType,
    EuEntityDetails,
    EuEntityPermissionDetail,
    EuEntityPermissionsQueryRequest,
    EuEntityPermissionsQueryResponse,
    EuEntityPermissionType,
    EuEntityQueryPermissionType,
    GrantPermissionsResponse,
    IndirectPermissionType,
    IndirectTargetIdentifierType,
    OperationStatus,
    PermissionOperationStatusResponse,
    PersonalPermissionDetail,
    PersonalPermissionsQueryRequest,
    PersonalPermissionsQueryResponse,
    PersonPermissionDetail,
    PersonPermissionsQueryRequest,
    PersonPermissionsQueryResponse,
    SubjectEntityDetails,
    SubjectPersonDetails,
    SubordinateEntityRoleDetail,
    SubordinateEntityRolesQueryRequest,
    SubordinateEntityRolesQueryResponse,
    SubordinateEntityRoleType,
    SubunitIdentifierType,
    SubunitPermissionDetail,
    SubunitPermissionsQueryRequest,
    SubunitPermissionsQueryResponse,
)
from ksef2.domain.models.testdata import Identifier, IdentifierType, PermissionType
from ksef2.infra.schema.api import spec


class PermissionsMapper:
    @staticmethod
    def map_person_grant_request(
        subject_identifier: IdentifierType,
        subject_value: str,
        permissions: list[PermissionType],
        description: str,
        first_name: str,
        last_name: str,
    ) -> spec.PersonPermissionsGrantRequest:
        return spec.PersonPermissionsGrantRequest(
            subjectIdentifier=spec.PersonPermissionsSubjectIdentifier(
                type=spec.CertificateSubjectIdentifierType(subject_identifier.value),
                value=subject_value,
            ),
            permissions=[spec.PersonPermissionScope(p.value) for p in permissions],
            description=description,
            subjectDetails=spec.PersonPermissionSubjectDetails(
                subjectDetailsType=spec.PersonPermissionSubjectDetailsType(
                    "PersonByIdentifier"
                ),
                personById=spec.PersonDetails(
                    firstName=first_name,
                    lastName=last_name,
                ),
            ),
        )

    @staticmethod
    def map_entity_grant_request(
        subject_value: str,
        permissions: list[EntityPermission],
        description: str,
        entity_name: str,
    ) -> spec.EntityPermissionsGrantRequest:
        return spec.EntityPermissionsGrantRequest(
            subjectIdentifier=spec.EntityPermissionsSubjectIdentifier(
                type=spec.EntityAuthorizationsAuthorizingEntityIdentifierType("Nip"),
                value=subject_value,
            ),
            permissions=[
                spec.EntityPermission(
                    type=spec.EntityPermissionType(p.type.value),
                    canDelegate=p.can_delegate,
                )
                for p in permissions
            ],
            description=description,
            subjectDetails=spec.EntityDetails(
                fullName=entity_name,
            ),
        )

    @staticmethod
    def map_authorization_grant_request(
        subject_type: AuthorizationSubjectIdentifierType,
        subject_value: str,
        permission: AuthorizationPermissionType,
        description: str,
        entity_name: str,
    ) -> spec.EntityAuthorizationPermissionsGrantRequest:
        return spec.EntityAuthorizationPermissionsGrantRequest(
            subjectIdentifier=spec.EntityAuthorizationPermissionsSubjectIdentifier(
                type=spec.EntityAuthorizationPermissionsSubjectIdentifierType(
                    subject_type.value
                ),
                value=subject_value,
            ),
            permission=spec.EntityAuthorizationPermissionType(permission.value),
            description=description,
            subjectDetails=spec.EntityDetails(
                fullName=entity_name,
            ),
        )

    @staticmethod
    def map_indirect_grant_request(
        subject_identifier: IdentifierType,
        subject_value: str,
        permissions: list[IndirectPermissionType],
        description: str,
        first_name: str,
        last_name: str,
        target_identifier: IndirectTargetIdentifierType | None = None,
        target_value: str | None = None,
    ) -> spec.IndirectPermissionsGrantRequest:
        target_id = None
        if target_identifier and target_value:
            target_id = spec.IndirectPermissionsTargetIdentifier(
                type=spec.IndirectPermissionsTargetIdentifierType(
                    target_identifier.value
                ),
                value=target_value,
            )

        return spec.IndirectPermissionsGrantRequest(
            subjectIdentifier=spec.IndirectPermissionsSubjectIdentifier(
                type=spec.CertificateSubjectIdentifierType(subject_identifier.value),
                value=subject_value,
            ),
            targetIdentifier=target_id,
            permissions=[spec.IndirectPermissionType(p.value) for p in permissions],
            description=description,
            subjectDetails=spec.PersonPermissionSubjectDetails(
                subjectDetailsType=spec.PersonPermissionSubjectDetailsType(
                    "PersonByIdentifier"
                ),
                personById=spec.PersonDetails(
                    firstName=first_name,
                    lastName=last_name,
                ),
            ),
        )

    @staticmethod
    def map_subunit_grant_request(
        subject_identifier: IdentifierType,
        subject_value: str,
        context_identifier: SubunitIdentifierType,
        context_value: str,
        description: str,
        first_name: str,
        last_name: str,
        subunit_name: str | None = None,
    ) -> spec.SubunitPermissionsGrantRequest:
        return spec.SubunitPermissionsGrantRequest(
            subjectIdentifier=spec.SubunitPermissionsSubjectIdentifier(
                type=spec.CertificateSubjectIdentifierType(subject_identifier.value),
                value=subject_value,
            ),
            contextIdentifier=spec.SubunitPermissionsContextIdentifier(
                type=spec.SubunitPermissionsContextIdentifierType(
                    context_identifier.value
                ),
                value=context_value,
            ),
            description=description,
            subunitName=subunit_name,
            subjectDetails=spec.PersonPermissionSubjectDetails(
                subjectDetailsType=spec.PersonPermissionSubjectDetailsType(
                    "PersonByIdentifier"
                ),
                personById=spec.PersonDetails(
                    firstName=first_name,
                    lastName=last_name,
                ),
            ),
        )

    @staticmethod
    def map_eu_entity_grant_request(
        subject_value: str,
        permissions: list[EuEntityPermissionType],
        description: str,
    ) -> spec.EuEntityPermissionsGrantRequest:
        return spec.EuEntityPermissionsGrantRequest(
            subjectIdentifier=spec.EuEntityPermissionsSubjectIdentifier(
                type=spec.EuEntityAdministrationPermissionsSubjectIdentifierType(
                    "Fingerprint"
                ),
                value=subject_value,
            ),
            permissions=[spec.EntityPermissionType(p.value) for p in permissions],
            description=description,
            subjectDetails=spec.EuEntityPermissionSubjectDetails(
                subjectDetailsType=spec.EuEntityPermissionSubjectDetailsType(
                    "EntityByFingerprint"
                ),
            ),
        )

    @staticmethod
    def map_eu_entity_admin_grant_request(
        subject_value: str,
        context_identifier: EuEntityAdminContextIdentifierType,
        context_value: str,
        description: str,
        eu_entity_name: str,
    ) -> spec.EuEntityAdministrationPermissionsGrantRequest:
        return spec.EuEntityAdministrationPermissionsGrantRequest(
            subjectIdentifier=spec.EuEntityAdministrationPermissionsSubjectIdentifier(
                type=spec.EuEntityAdministrationPermissionsSubjectIdentifierType(
                    "Fingerprint"
                ),
                value=subject_value,
            ),
            contextIdentifier=spec.EuEntityAdministrationPermissionsContextIdentifier(
                type=spec.EuEntityAdministrationPermissionsContextIdentifierType(
                    context_identifier.value
                ),
                value=context_value,
            ),
            description=description,
            euEntityName=eu_entity_name,
            subjectDetails=spec.EuEntityPermissionSubjectDetails(
                subjectDetailsType=spec.EuEntityPermissionSubjectDetailsType(
                    "EntityByFingerprint"
                ),
            ),
            euEntityDetails=spec.EuEntityDetails(
                fullName=eu_entity_name,
                address="",
            ),
        )

    @staticmethod
    def map_response(r: spec.PermissionsOperationResponse) -> GrantPermissionsResponse:
        return GrantPermissionsResponse(
            reference_number=r.referenceNumber,
        )

    @staticmethod
    def map_operation_status_response(
        r: spec.PermissionsOperationStatusResponse,
    ) -> PermissionOperationStatusResponse:
        from ksef2.domain.models.permissions import OperationStatusCode

        return PermissionOperationStatusResponse(
            status=OperationStatus(
                code=OperationStatusCode(str(r.status.code)),
                description=r.status.description,
            ),
        )

    @staticmethod
    def map_attachment_status_response(
        r: spec.CheckAttachmentPermissionStatusResponse,
    ) -> AttachmentPermissionStatus:
        return AttachmentPermissionStatus(
            is_attachment_allowed=r.isAttachmentAllowed or False,
            revoked_date=r.revokedDate,
        )

    @staticmethod
    def map_entity_roles_response(
        r: spec.QueryEntityRolesResponse,
    ) -> EntityRolesResponse:
        from ksef2.domain.models.permissions import EntityRoleType

        roles = []
        for role in r.roles:
            parent_type = None
            parent_value = None
            if role.parentEntityIdentifier:
                parent_type = role.parentEntityIdentifier.type
                parent_value = role.parentEntityIdentifier.value
            roles.append(
                EntityRole(
                    role=EntityRoleType(role.role.value),
                    description=role.description,
                    start_date=role.startDate,
                    parent_entity_identifier_type=parent_type,
                    parent_entity_identifier_value=parent_value,
                )
            )
        return EntityRolesResponse(
            roles=roles,
            has_more=r.hasMore,
        )

    @staticmethod
    def map_person_query_request(
        request: PersonPermissionsQueryRequest,
    ) -> spec.PersonPermissionsQueryRequest:

        identifier = None
        if author_identifier := request.author_identifier:
            identifier = spec.PersonPermissionsAuthorIdentifier(
                type=spec.PersonPermissionsAuthorIdentifierType(
                    author_identifier.type.value
                ),
                value=author_identifier.value,
            )

        return spec.PersonPermissionsQueryRequest(
            authorIdentifier=identifier,
            authorizedIdentifier=spec.PersonPermissionsAuthorizedIdentifier(
                type=spec.CertificateSubjectIdentifierType(
                    request.authorized_identifier.type.value
                ),
                value=request.authorized_identifier.value,
            )
            if request.authorized_identifier
            else None,
            contextIdentifier=spec.PersonPermissionsContextIdentifier(
                type=spec.PersonPermissionsContextIdentifierType(
                    request.context_identifier.type.value
                ),
                value=request.context_identifier.value,
            )
            if request.context_identifier
            else None,
            targetIdentifier=spec.PersonPermissionsTargetIdentifier(
                type=spec.IndirectPermissionsTargetIdentifierType(
                    request.target_identifier.type.value
                ),
                value=request.target_identifier.value,
            )
            if request.target_identifier
            else None,
            permissionTypes=[
                spec.PersonPermissionScope(p.value) for p in request.permission_types
            ]
            if request.permission_types
            else None,
            permissionState=spec.PermissionState(request.permission_state.value)
            if request.permission_state
            else None,
            queryType=spec.PersonPermissionsQueryType(request.query_type.value),
        )

    @staticmethod
    def map_person_permissions_query_response(
        r: spec.QueryPersonPermissionsResponse,
    ) -> PersonPermissionsQueryResponse:
        from ksef2.domain.models.permissions import (
            PermissionState as DomainPermissionState,
        )

        details = []
        for p in r.permissions:
            details.append(
                PersonPermissionDetail(
                    id=p.id,
                    author_identifier=Identifier(
                        type=IdentifierType(p.authorIdentifier.type.value),
                        value=p.authorIdentifier.value,
                    )
                    if p.authorIdentifier.value
                    else None,
                    authorized_identifier=Identifier(
                        type=IdentifierType(p.authorizedIdentifier.type.value),
                        value=p.authorizedIdentifier.value,
                    )
                    if p.authorizedIdentifier.value
                    else None,
                    context_identifier=Identifier(
                        type=IdentifierType(p.contextIdentifier.type.value),
                        value=p.contextIdentifier.value,
                    )
                    if p.contextIdentifier
                    else None,
                    target_identifier=Identifier(
                        type=IdentifierType(p.targetIdentifier.type.value),
                        value=p.targetIdentifier.value
                        if p.targetIdentifier.value
                        else "str",
                    )
                    if p.targetIdentifier
                    else None,
                    permission_state=DomainPermissionState(p.permissionState.value),
                    permission_type=PermissionType(p.permissionScope.value),
                    description=p.description,
                    start_date=p.startDate,
                    can_delegate=p.canDelegate,
                    subject_person_details=SubjectPersonDetails(
                        first_name=p.subjectPersonDetails.firstName,
                        last_name=p.subjectPersonDetails.lastName,
                    )
                    if p.subjectPersonDetails
                    else None,
                    subject_entity_details=SubjectEntityDetails(
                        full_name=p.subjectEntityDetails.fullName,
                    )
                    if p.subjectEntityDetails
                    else None,
                )
            )
        return PersonPermissionsQueryResponse(
            permissions=details,
            has_more=r.hasMore,
        )

    # ------------------------------------------------------------------
    # query_authorizations
    # ------------------------------------------------------------------

    @staticmethod
    def map_authorizations_query_request(
        request: AuthorizationPermissionsQueryRequest,
    ) -> spec.EntityAuthorizationPermissionsQueryRequest:
        return spec.EntityAuthorizationPermissionsQueryRequest(
            authorizingIdentifier=spec.EntityAuthorizationsAuthorizingEntityIdentifier(
                type=spec.EntityAuthorizationsAuthorizingEntityIdentifierType(
                    request.authorizing_identifier.type.value
                ),
                value=request.authorizing_identifier.value,
            )
            if request.authorizing_identifier
            else None,
            authorizedIdentifier=spec.EntityAuthorizationsAuthorizedEntityIdentifier(
                type=spec.EntityAuthorizationPermissionsSubjectIdentifierType(
                    request.authorized_identifier.type.value
                ),
                value=request.authorized_identifier.value,
            )
            if request.authorized_identifier
            else None,
            queryType=spec.QueryType(request.query_type.value),
            permissionTypes=[
                spec.InvoicePermissionType(p.value) for p in request.permission_types
            ]
            if request.permission_types
            else None,
        )

    @staticmethod
    def map_authorizations_query_response(
        r: spec.QueryEntityAuthorizationPermissionsResponse,
    ) -> AuthorizationPermissionsQueryResponse:
        from ksef2.domain.models.permissions import (
            AuthorizationPermissionType as DomainAuthPT,
        )

        grants = []
        for g in r.authorizationGrants:
            author_id = (
                Identifier(
                    type=IdentifierType(g.authorIdentifier.type.value),
                    value=g.authorIdentifier.value,
                )
                if g.authorIdentifier
                else None
            )
            authorized_id = Identifier(
                type=IdentifierType(g.authorizedEntityIdentifier.type.value),
                value=g.authorizedEntityIdentifier.value,
            )
            authorizing_id = Identifier(
                type=IdentifierType(g.authorizingEntityIdentifier.type.value),
                value=g.authorizingEntityIdentifier.value,
            )
            subject_entity = (
                SubjectEntityDetails(full_name=g.subjectEntityDetails.fullName)
                if g.subjectEntityDetails
                else None
            )
            grants.append(
                AuthorizationGrantDetail(
                    id=g.id,
                    author_identifier=author_id,
                    authorized_entity_identifier=authorized_id,
                    authorizing_entity_identifier=authorizing_id,
                    authorization_scope=DomainAuthPT(g.authorizationScope.value),
                    description=g.description,
                    subject_entity_details=subject_entity,
                    start_date=g.startDate,
                )
            )
        return AuthorizationPermissionsQueryResponse(
            authorization_grants=grants,
            has_more=r.hasMore,
        )

    # ------------------------------------------------------------------
    # query_personal
    # ------------------------------------------------------------------

    @staticmethod
    def map_personal_query_request(
        request: PersonalPermissionsQueryRequest,
    ) -> spec.PersonalPermissionsQueryRequest:
        return spec.PersonalPermissionsQueryRequest(
            contextIdentifier=spec.PersonalPermissionsContextIdentifier(
                type=spec.PersonPermissionsContextIdentifierType(
                    request.context_identifier.type.value
                ),
                value=request.context_identifier.value,
            )
            if request.context_identifier
            else None,
            targetIdentifier=spec.PersonalPermissionsTargetIdentifier(
                type=spec.IndirectPermissionsTargetIdentifierType(
                    request.target_identifier.type.value
                ),
                value=request.target_identifier.value,
            )
            if request.target_identifier
            else None,
            permissionTypes=[
                spec.PersonalPermissionScope(p.value) for p in request.permission_types
            ]
            if request.permission_types
            else None,
            permissionState=spec.PermissionState(request.permission_state.value)
            if request.permission_state
            else None,
        )

    @staticmethod
    def map_personal_query_response(
        r: spec.QueryPersonalPermissionsResponse,
    ) -> PersonalPermissionsQueryResponse:
        from ksef2.domain.models.permissions import (
            PermissionState as DomainPermissionState,
        )

        details = []
        for p in r.permissions:
            context_id = (
                Identifier(
                    type=IdentifierType(p.contextIdentifier.type.value),
                    value=p.contextIdentifier.value,
                )
                if p.contextIdentifier
                else None
            )
            authorized_id = (
                Identifier(
                    type=IdentifierType(p.authorizedIdentifier.type.value),
                    value=p.authorizedIdentifier.value,
                )
                if p.authorizedIdentifier
                else None
            )

            target_identifier = (
                Identifier(
                    type=IdentifierType(p.authorizedIdentifier.type.value),
                    value=p.authorizedIdentifier.value,
                )
                if p.authorizedIdentifier
                else None
            )

            subject_person = (
                SubjectPersonDetails(
                    first_name=p.subjectPersonDetails.firstName,
                    last_name=p.subjectPersonDetails.lastName,
                )
                if p.subjectPersonDetails
                else None
            )
            subject_entity = (
                SubjectEntityDetails(full_name=p.subjectEntityDetails.fullName)
                if p.subjectEntityDetails
                else None
            )
            details.append(
                PersonalPermissionDetail(
                    id=p.id,
                    context_identifier=context_id,
                    authorized_identifier=authorized_id,
                    target_identifier=target_identifier,
                    permission_type=PermissionType(p.permissionScope.value),
                    description=p.description,
                    subject_person_details=subject_person,
                    subject_entity_details=subject_entity,
                    permission_state=DomainPermissionState(p.permissionState.value),
                    start_date=p.startDate,
                    can_delegate=p.canDelegate,
                )
            )
        return PersonalPermissionsQueryResponse(
            permissions=details,
            has_more=r.hasMore,
        )

    # ------------------------------------------------------------------
    # query_eu_entities
    # ------------------------------------------------------------------

    @staticmethod
    def map_eu_entities_query_request(
        request: EuEntityPermissionsQueryRequest,
    ) -> spec.EuEntityPermissionsQueryRequest:
        return spec.EuEntityPermissionsQueryRequest(
            vatUeIdentifier=request.vat_ue_identifier,
            authorizedFingerprintIdentifier=request.authorized_fingerprint_identifier,
            permissionTypes=[
                spec.EuEntityPermissionsQueryPermissionType(p.value)
                for p in request.permission_types
            ]
            if request.permission_types
            else None,
        )

    @staticmethod
    def map_eu_entities_query_response(
        r: spec.QueryEuEntityPermissionsResponse,
    ) -> EuEntityPermissionsQueryResponse:
        details = []
        for p in r.permissions:
            author_id = Identifier(
                type=IdentifierType(p.authorIdentifier.type.value),
                value=p.authorIdentifier.value,
            )
            subject_person = (
                SubjectPersonDetails(
                    first_name=p.subjectPersonDetails.firstName,
                    last_name=p.subjectPersonDetails.lastName,
                )
                if p.subjectPersonDetails
                else None
            )
            subject_entity = (
                SubjectEntityDetails(full_name=p.subjectEntityDetails.fullName)
                if p.subjectEntityDetails
                else None
            )
            eu_entity = (
                EuEntityDetails(
                    full_name=p.euEntityDetails.fullName,
                    address=p.euEntityDetails.address,
                )
                if p.euEntityDetails
                else None
            )
            details.append(
                EuEntityPermissionDetail(
                    id=p.id,
                    author_identifier=author_id,
                    vat_ue_identifier=p.vatUeIdentifier,
                    eu_entity_name=p.euEntityName,
                    authorized_fingerprint_identifier=p.authorizedFingerprintIdentifier,
                    permission_type=EuEntityQueryPermissionType(
                        p.permissionScope.value
                    ),
                    description=p.description,
                    subject_person_details=subject_person,
                    subject_entity_details=subject_entity,
                    eu_entity_details=eu_entity,
                    start_date=p.startDate,
                )
            )
        return EuEntityPermissionsQueryResponse(
            permissions=details,
            has_more=r.hasMore,
        )

    # ------------------------------------------------------------------
    # query_subordinate_entities
    # ------------------------------------------------------------------

    @staticmethod
    def map_subordinate_entities_query_request(
        request: SubordinateEntityRolesQueryRequest,
    ) -> spec.SubordinateEntityRolesQueryRequest:
        return spec.SubordinateEntityRolesQueryRequest(
            subordinateEntityIdentifier=spec.EntityPermissionsSubordinateEntityIdentifier(
                type=spec.EntityAuthorizationsAuthorizingEntityIdentifierType(
                    request.subordinate_entity_identifier.type.value
                ),
                value=request.subordinate_entity_identifier.value,
            )
            if request.subordinate_entity_identifier
            else None,
        )

    @staticmethod
    def map_subordinate_entities_query_response(
        r: spec.QuerySubordinateEntityRolesResponse,
    ) -> SubordinateEntityRolesQueryResponse:
        roles = []
        for role in r.roles:
            sub_id = Identifier(
                type=IdentifierType(role.subordinateEntityIdentifier.type.value),
                value=role.subordinateEntityIdentifier.value,
            )
            roles.append(
                SubordinateEntityRoleDetail(
                    subordinate_entity_identifier=sub_id,
                    role=SubordinateEntityRoleType(role.role.value),
                    description=role.description,
                    start_date=role.startDate,
                )
            )
        return SubordinateEntityRolesQueryResponse(
            roles=roles,
            has_more=r.hasMore,
        )

    # ------------------------------------------------------------------
    # query_subunits
    # ------------------------------------------------------------------

    @staticmethod
    def map_subunits_query_request(
        request: SubunitPermissionsQueryRequest,
    ) -> spec.SubunitPermissionsQueryRequest:
        return spec.SubunitPermissionsQueryRequest(
            subunitIdentifier=spec.SubunitPermissionsSubunitIdentifier(
                type=spec.SubunitPermissionsContextIdentifierType(
                    request.subunit_identifier.type.value
                ),
                value=request.subunit_identifier.value,
            )
            if request.subunit_identifier
            else None,
        )

    @staticmethod
    def map_subunits_query_response(
        r: spec.QuerySubunitPermissionsResponse,
    ) -> SubunitPermissionsQueryResponse:
        details = []
        for p in r.permissions:
            authorized_id = Identifier(
                type=IdentifierType(p.authorizedIdentifier.type.value),
                value=p.authorizedIdentifier.value,
            )
            subunit_id = Identifier(
                type=IdentifierType(p.subunitIdentifier.type.value),
                value=p.subunitIdentifier.value,
            )
            author_id = Identifier(
                type=IdentifierType(p.authorIdentifier.type.value),
                value=p.authorIdentifier.value,
            )
            subject_person = (
                SubjectPersonDetails(
                    first_name=p.subjectPersonDetails.firstName,
                    last_name=p.subjectPersonDetails.lastName,
                )
                if p.subjectPersonDetails
                else None
            )
            details.append(
                SubunitPermissionDetail(
                    id=p.id,
                    authorized_identifier=authorized_id,
                    subunit_identifier=subunit_id,
                    author_identifier=author_id,
                    permission_type=PermissionType(p.permissionScope.value),
                    description=p.description,
                    subject_person_details=subject_person,
                    subunit_name=p.subunitName,
                    start_date=p.startDate,
                )
            )
        return SubunitPermissionsQueryResponse(
            permissions=details,
            has_more=r.hasMore,
        )
