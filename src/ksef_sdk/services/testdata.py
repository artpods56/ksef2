from __future__ import annotations

from datetime import datetime
from typing import final

from ksef_sdk.core.http import HttpTransport
from ksef_sdk.domain.models.testdata import (
    Identifier,
    Permission,
    SubjectType,
    Subunit,
)
from ksef_sdk.endpoints.testdata import (
    CreatePersonEndpoint,
    CreateSubjectEndpoint,
    DeletePersonEndpoint,
    DeleteSubjectEndpoint,
    EnableAttachmentsEndpoint,
    GrantPermissionsEndpoint,
    RevokePermissionsEndpoint,
)
from ksef_sdk.infra.mappers.testdata import TestDataMapper


@final
class TestDataService:
    def __init__(self, transport: HttpTransport) -> None:
        self._create_subject_ep = CreateSubjectEndpoint(transport)
        self._delete_subject_ep = DeleteSubjectEndpoint(transport)
        self._create_person_ep = CreatePersonEndpoint(transport)
        self._delete_person_ep = DeletePersonEndpoint(transport)
        self._grant_permissions_ep = GrantPermissionsEndpoint(transport)
        self._revoke_permissions_ep = RevokePermissionsEndpoint(transport)
        self._enable_attachments_ep = EnableAttachmentsEndpoint(transport)

    def create_subject(
        self,
        *,
        nip: str,
        subject_type: SubjectType,
        description: str,
        subunits: list[Subunit] | None = None,
        created_date: datetime | None = None,
    ) -> None:
        self._create_subject_ep.send(
            TestDataMapper.create_subject(
                nip=nip,
                subject_type=subject_type,
                description=description,
                subunits=subunits,
                created_date=created_date,
            )
        )

    def delete_subject(self, *, nip: str) -> None:
        self._delete_subject_ep.send(TestDataMapper.delete_subject(nip=nip))

    def create_person(
        self,
        *,
        nip: str,
        pesel: str,
        description: str,
        is_bailiff: bool = False,
        is_deceased: bool = False,
        created_date: datetime | None = None,
    ) -> None:
        self._create_person_ep.send(
            TestDataMapper.create_person(
                nip=nip,
                pesel=pesel,
                description=description,
                is_bailiff=is_bailiff,
                is_deceased=is_deceased,
                created_date=created_date,
            )
        )

    def delete_person(self, *, nip: str) -> None:
        self._delete_person_ep.send(TestDataMapper.delete_person(nip=nip))

    def grant_permissions(
        self,
        *,
        context: Identifier,
        authorized: Identifier,
        permissions: list[Permission],
    ) -> None:
        self._grant_permissions_ep.send(
            TestDataMapper.grant_permissions(
                context=context,
                authorized=authorized,
                permissions=permissions,
            )
        )

    def revoke_permissions(
        self,
        *,
        context: Identifier,
        authorized: Identifier,
    ) -> None:
        self._revoke_permissions_ep.send(
            TestDataMapper.revoke_permissions(
                context=context,
                authorized=authorized,
            )
        )

    def enable_attachments(self, *, nip: str) -> None:
        self._enable_attachments_ep.send(TestDataMapper.enable_attachments(nip=nip))
