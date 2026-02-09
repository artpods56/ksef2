from __future__ import annotations

from datetime import datetime
from typing import Any

from ksef_sdk.domain.models.testdata import (
    Identifier,
    Permission,
    SubjectType,
    Subunit,
)


class TestDataMapper:
    @staticmethod
    def create_subject(
        *,
        nip: str,
        subject_type: SubjectType,
        description: str,
        subunits: list[Subunit] | None = None,
        created_date: datetime | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "subjectNip": nip,
            "subjectType": subject_type.value,
            "description": description,
        }
        if subunits:
            body["subunits"] = [
                {"subjectNip": s.nip, "description": s.description} for s in subunits
            ]
        if created_date is not None:
            body["createdDate"] = created_date.isoformat()
        return body

    @staticmethod
    def delete_subject(*, nip: str) -> dict[str, Any]:
        return {"subjectNip": nip}

    @staticmethod
    def create_person(
        *,
        nip: str,
        pesel: str,
        description: str,
        is_bailiff: bool = False,
        is_deceased: bool = False,
        created_date: datetime | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "nip": nip,
            "pesel": pesel,
            "description": description,
            "isBailiff": is_bailiff,
        }
        if is_deceased:
            body["isDeceased"] = is_deceased
        if created_date is not None:
            body["createdDate"] = created_date.isoformat()
        return body

    @staticmethod
    def delete_person(*, nip: str) -> dict[str, Any]:
        return {"nip": nip}

    @staticmethod
    def grant_permissions(
        *,
        context: Identifier,
        authorized: Identifier,
        permissions: list[Permission],
    ) -> dict[str, Any]:
        return {
            "contextIdentifier": {
                "type": context.type.value,
                "value": context.value,
            },
            "authorizedIdentifier": {
                "type": authorized.type.value,
                "value": authorized.value,
            },
            "permissions": [
                {"permissionType": p.type.value, "description": p.description}
                for p in permissions
            ],
        }

    @staticmethod
    def revoke_permissions(
        *,
        context: Identifier,
        authorized: Identifier,
    ) -> dict[str, Any]:
        return {
            "contextIdentifier": {
                "type": context.type.value,
                "value": context.value,
            },
            "authorizedIdentifier": {
                "type": authorized.type.value,
                "value": authorized.value,
            },
        }

    @staticmethod
    def enable_attachments(*, nip: str) -> dict[str, Any]:
        return {"nip": nip}
