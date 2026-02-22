from __future__ import annotations

import logging
from datetime import date, datetime
from types import TracebackType
from typing import Self, final

from ksef2.core import protocols, exceptions
from ksef2.core.exceptions import ExceptionCode
from ksef2.domain.models.testdata import (
    AuthContextIdentifier,
    Identifier,
    Permission,
    SubjectType,
    SubUnit,
    CreateSubjectRequest,
)
from ksef2.endpoints.testdata import (
    BlockContextEndpoint,
    CreatePersonEndpoint,
    CreateSubjectEndpoint,
    DeletePersonEndpoint,
    DeleteSubjectEndpoint,
    EnableAttachmentsEndpoint,
    GrantPermissionsEndpoint,
    RevokeAttachmentsEndpoint,
    RevokePermissionsEndpoint,
    UnblockContextEndpoint,
)
from ksef2.infra.mappers.requests.testdata import TestDataMapper, TestDataMapperv2

logger = logging.getLogger(__name__)


@final
class TestDataService:
    def __init__(self, transport: protocols.Middleware) -> None:
        self._create_subject_ep = CreateSubjectEndpoint(transport)
        self._delete_subject_ep = DeleteSubjectEndpoint(transport)
        self._create_person_ep = CreatePersonEndpoint(transport)
        self._delete_person_ep = DeletePersonEndpoint(transport)
        self._grant_permissions_ep = GrantPermissionsEndpoint(transport)
        self._revoke_permissions_ep = RevokePermissionsEndpoint(transport)
        self._enable_attachments_ep = EnableAttachmentsEndpoint(transport)
        self._revoke_attachments_ep = RevokeAttachmentsEndpoint(transport)
        self._block_context_ep = BlockContextEndpoint(transport)
        self._unblock_context_ep = UnblockContextEndpoint(transport)

    def create_subject(
        self,
        *,
        nip: str,
        subject_type: SubjectType,
        description: str,
        subunits: list[SubUnit] | None = None,
        created_date: datetime | None = None,
    ) -> None:
        self._create_subject_ep.send(
            TestDataMapperv2.map_request(
                CreateSubjectRequest(
                    subject_nip=nip,
                    subject_type=subject_type,
                    description=description,
                    subunits=subunits,
                    created_date=created_date,
                )
            ).model_dump(mode="json", exclude_none=True)
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
        permissions: list[Permission],
        grant_to: Identifier,
        in_context_of: Identifier,
    ) -> None:
        self._grant_permissions_ep.send(
            TestDataMapper.grant_permissions(
                context=in_context_of,
                authorized=grant_to,
                permissions=permissions,
            )
        )

    def revoke_permissions(
        self, *, revoke_from: Identifier, in_context_of: Identifier
    ) -> None:
        self._revoke_permissions_ep.send(
            TestDataMapper.revoke_permissions(
                context=in_context_of,
                authorized=revoke_from,
            )
        )

    def enable_attachments(self, *, nip: str) -> None:
        self._enable_attachments_ep.send(TestDataMapper.enable_attachments(nip=nip))

    def revoke_attachments(
        self, *, nip: str, expected_end_date: date | None = None
    ) -> None:
        self._revoke_attachments_ep.send(
            TestDataMapper.revoke_attachments(
                nip=nip, expected_end_date=expected_end_date
            )
        )

    def block_context(self, *, context: AuthContextIdentifier) -> None:
        self._block_context_ep.send(
            TestDataMapper.block_context(context_identifier=context)
        )

    def unblock_context(self, *, context: AuthContextIdentifier) -> None:
        self._unblock_context_ep.send(
            TestDataMapper.unblock_context(context_identifier=context)
        )

    def temporal(self) -> TemporalTestData:
        return TemporalTestData(self)


@final
class TemporalTestData:
    def __init__(self, service: TestDataService) -> None:
        self._service = service
        self._subjects: list[str] = []
        self._persons: list[str] = []
        self._permissions: list[tuple[Identifier, Identifier]] = []
        self._attachments: list[str] = []
        self._blocked_contexts: list[AuthContextIdentifier] = []

    def __enter__(self) -> Self:
        return self

    def _cleanup_blocked_context(self, context: AuthContextIdentifier) -> None:
        try:
            self._service.unblock_context(context=context)
        except Exception:
            logger.warning("Failed to unblock context %s", context, exc_info=True)

    def _cleanup_attachment(self, nip: str) -> None:
        try:
            self._service.revoke_attachments(nip=nip)
        except Exception:
            logger.warning("Failed to revoke attachments for %s", nip, exc_info=True)

    def _cleanup_permission(
        self, in_context_of: Identifier, grant_to: Identifier
    ) -> None:
        try:
            self._service.revoke_permissions(
                revoke_from=grant_to, in_context_of=in_context_of
            )
        except Exception:
            logger.warning(
                "Failed to revoke permissions for %s → %s",
                in_context_of,
                grant_to,
                exc_info=True,
            )

    def _cleanup_person(self, nip: str) -> None:
        try:
            self._service.delete_person(nip=nip)
        except Exception:
            logger.warning("Failed to delete person %s", nip, exc_info=True)

    def _cleanup_subject(self, nip: str) -> None:
        try:
            self._service.delete_subject(nip=nip)
        except Exception:
            logger.warning("Failed to delete subject %s", nip, exc_info=True)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        for context in reversed(self._blocked_contexts):
            self._cleanup_blocked_context(context)
        for nip in reversed(self._attachments):
            self._cleanup_attachment(nip)
        for in_context_of, grant_to in reversed(self._permissions):
            self._cleanup_permission(in_context_of, grant_to)
        for nip in reversed(self._persons):
            self._cleanup_person(nip)
        for nip in reversed(self._subjects):
            self._cleanup_subject(nip)

    def create_subject(
        self,
        *,
        nip: str,
        subject_type: SubjectType,
        description: str,
        subunits: list[SubUnit] | None = None,
        created_date: datetime | None = None,
    ) -> None:
        if nip not in self._subjects:
            self._subjects.append(nip)

        try:
            self._service.create_subject(
                nip=nip,
                subject_type=subject_type,
                description=description,
                subunits=subunits,
                created_date=created_date,
            )
        except exceptions.KSeFApiError as e:
            if e.exception_code == ExceptionCode.OBJECT_ALREADY_EXISTS:
                logger.warning(
                    f"Subject identified with NIP: `{nip}` already exists, continuing..."
                )
            else:
                raise

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
        if nip not in self._persons:
            self._persons.append(nip)
        try:
            self._service.create_person(
                nip=nip,
                pesel=pesel,
                description=description,
                is_bailiff=is_bailiff,
                is_deceased=is_deceased,
                created_date=created_date,
            )
        except exceptions.KSeFApiError as e:
            if e.exception_code == ExceptionCode.OBJECT_ALREADY_EXISTS:
                logger.warning(
                    f"Person identified with NIP: `{nip}` already exists, continuing..."
                )
            else:
                raise

    def grant_permissions(
        self,
        *,
        permissions: list[Permission],
        grant_to: Identifier,
        in_context_of: Identifier,
    ) -> None:
        self._permissions.append((in_context_of, grant_to))
        try:
            self._service.grant_permissions(
                permissions=permissions, grant_to=grant_to, in_context_of=in_context_of
            )
        except exceptions.KSeFApiError as e:
            if e.exception_code == ExceptionCode.OBJECT_ALREADY_EXISTS:
                logger.warning(
                    f"Permissions for {in_context_of} → {grant_to} already exist, continuing..."
                )
            else:
                raise

    def enable_attachments(self, *, nip: str) -> None:
        self._service.enable_attachments(nip=nip)
        self._attachments.append(nip)

    def revoke_attachments(
        self, *, nip: str, expected_end_date: date | None = None
    ) -> None:
        self._service.revoke_attachments(nip=nip, expected_end_date=expected_end_date)

    def block_context(self, *, context: AuthContextIdentifier) -> None:
        self._service.block_context(context=context)
        self._blocked_contexts.append(context)

    def unblock_context(self, *, context: AuthContextIdentifier) -> None:
        self._service.unblock_context(context=context)
