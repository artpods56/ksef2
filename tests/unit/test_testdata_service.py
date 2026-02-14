"""Tests for TestDataService — request body mapping and HTTP calls."""

from __future__ import annotations

from datetime import datetime, timezone

from ksef2.domain.models.testdata import (
    Identifier,
    IdentifierType,
    Permission,
    PermissionType,
    SubjectType,
    SubUnit,
)
from ksef2.services.testdata import TestDataService

from tests.unit.conftest import FakeTransport


def _build_service(transport: FakeTransport) -> TestDataService:
    return TestDataService(transport)  # type: ignore[arg-type]


class TestCreateSubject:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.create_subject(
            nip="1234567890",
            subject_type=SubjectType.VAT_GROUP,
            description="Test VAT group",
        )

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/subject"
        assert call.json == {
            "subjectNip": "1234567890",
            "subjectType": "VatGroup",
            "description": "Test VAT group",
        }

    def test_with_subunits(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.create_subject(
            nip="1234567890",
            subject_type=SubjectType.VAT_GROUP,
            description="Test subject",
            subunits=[
                SubUnit(subject_nip="1111111111", description="Sub 1"),
                SubUnit(subject_nip="2222222222", description="Sub 2"),
            ],
        )

        body = fake_transport.calls[0].json
        assert body["subunits"] == [
            {"subjectNip": "1111111111", "description": "Sub 1"},
            {"subjectNip": "2222222222", "description": "Sub 2"},
        ]

    def test_with_created_date(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)
        dt = datetime(2025, 1, 15, 12, 0, 0, tzinfo=timezone.utc)

        svc.create_subject(
            nip="1234567890",
            subject_type=SubjectType.JST,
            description="Test subject",
            created_date=dt,
        )

        body = fake_transport.calls[0].json
        assert body["createdDate"] == "2025-01-15T12:00:00Z"

    def test_all_subject_types(self, fake_transport: FakeTransport) -> None:
        for st in SubjectType:
            fake_transport.enqueue(status_code=204)
            svc = _build_service(fake_transport)
            svc.create_subject(nip="1234567890", subject_type=st, description="Test subject")

            body = fake_transport.calls[-1].json
            assert body["subjectType"] == st.value


class TestDeleteSubject:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.delete_subject(nip="1234567890")

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/subject/remove"
        assert call.json == {"subjectNip": "1234567890"}


class TestCreatePerson:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.create_person(
            nip="1234567890",
            pesel="00000000000",
            description="Test JDG",
            is_bailiff=True,
        )

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/person"
        assert call.json == {
            "nip": "1234567890",
            "pesel": "00000000000",
            "description": "Test JDG",
            "isBailiff": True,
        }

    def test_with_deceased_and_date(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)
        dt = datetime(2025, 6, 1, tzinfo=timezone.utc)

        svc.create_person(
            nip="1234567890",
            pesel="00000000000",
            description="Test",
            is_deceased=True,
            created_date=dt,
        )

        body = fake_transport.calls[0].json
        assert body["isDeceased"] is True
        assert body["createdDate"] == dt.isoformat()

    def test_defaults(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.create_person(
            nip="1234567890",
            pesel="00000000000",
            description="Test",
        )

        body = fake_transport.calls[0].json
        assert body["isBailiff"] is False
        assert "isDeceased" not in body
        assert "createdDate" not in body


class TestDeletePerson:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.delete_person(nip="1234567890")

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/person/remove"
        assert call.json == {"nip": "1234567890"}


class TestGrantPermissions:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value="1234567890"),
            authorized=Identifier(type=IdentifierType.PESEL, value="00000000000"),
            permissions=[
                Permission(
                    type=PermissionType.INVOICE_READ, description="Read invoices"
                ),
                Permission(
                    type=PermissionType.INVOICE_WRITE, description="Write invoices"
                ),
            ],
        )

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/permissions"
        assert call.json == {
            "contextIdentifier": {"type": "Nip", "value": "1234567890"},
            "authorizedIdentifier": {"type": "Pesel", "value": "00000000000"},
            "permissions": [
                {"permissionType": "InvoiceRead", "description": "Read invoices"},
                {"permissionType": "InvoiceWrite", "description": "Write invoices"},
            ],
        }

    def test_fingerprint_identifier(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.grant_permissions(
            context=Identifier(type=IdentifierType.NIP, value="1234567890"),
            authorized=Identifier(type=IdentifierType.FINGERPRINT, value="ABC123"),
            permissions=[
                Permission(type=PermissionType.INTROSPECTION, description="Introspect"),
            ],
        )

        body = fake_transport.calls[0].json
        assert body["authorizedIdentifier"]["type"] == "Fingerprint"


class TestRevokePermissions:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.revoke_permissions(
            context=Identifier(type=IdentifierType.NIP, value="1234567890"),
            authorized=Identifier(type=IdentifierType.PESEL, value="00000000000"),
        )

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/permissions/revoke"
        assert call.json == {
            "contextIdentifier": {"type": "Nip", "value": "1234567890"},
            "authorizedIdentifier": {"type": "Pesel", "value": "00000000000"},
        }


class TestEnableAttachments:
    def test_sends_correct_body(self, fake_transport: FakeTransport) -> None:
        fake_transport.enqueue(status_code=204)
        svc = _build_service(fake_transport)

        svc.enable_attachments(nip="1234567890")

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/attachment"
        assert call.json == {"nip": "1234567890"}
