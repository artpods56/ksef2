"""Tests for testdata endpoint classes — URL correctness and HTTP method."""

from __future__ import annotations

from tests.unit.conftest import FakeTransport


class TestCreateSubjectEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import CreateSubjectEndpoint

        ep = CreateSubjectEndpoint(FakeTransport())
        assert ep.url == "/testdata/subject"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import CreateSubjectEndpoint

        fake_transport.enqueue(status_code=204)
        ep = CreateSubjectEndpoint(fake_transport)

        ep.send({"subjectNip": "1234567890"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/subject"
        assert call.json == {"subjectNip": "1234567890"}


class TestDeleteSubjectEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import DeleteSubjectEndpoint

        ep = DeleteSubjectEndpoint(FakeTransport())
        assert ep.url == "/testdata/subject/remove"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import DeleteSubjectEndpoint

        fake_transport.enqueue(status_code=204)
        ep = DeleteSubjectEndpoint(fake_transport)

        ep.send({"subjectNip": "1234567890"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/subject/remove"


class TestCreatePersonEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import CreatePersonEndpoint

        ep = CreatePersonEndpoint(FakeTransport())
        assert ep.url == "/testdata/person"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import CreatePersonEndpoint

        fake_transport.enqueue(status_code=204)
        ep = CreatePersonEndpoint(fake_transport)

        ep.send({"nip": "1234567890", "pesel": "00000000000"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/person"


class TestDeletePersonEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import DeletePersonEndpoint

        ep = DeletePersonEndpoint(FakeTransport())
        assert ep.url == "/testdata/person/remove"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import DeletePersonEndpoint

        fake_transport.enqueue(status_code=204)
        ep = DeletePersonEndpoint(fake_transport)

        ep.send({"nip": "1234567890"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/person/remove"


class TestGrantPermissionsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import GrantPermissionsEndpoint

        ep = GrantPermissionsEndpoint(FakeTransport())
        assert ep.url == "/testdata/permissions"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import GrantPermissionsEndpoint

        fake_transport.enqueue(status_code=204)
        ep = GrantPermissionsEndpoint(fake_transport)

        ep.send(
            {"contextIdentifier": {}, "authorizedIdentifier": {}, "permissions": []}
        )

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/permissions"


class TestRevokePermissionsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import RevokePermissionsEndpoint

        ep = RevokePermissionsEndpoint(FakeTransport())
        assert ep.url == "/testdata/permissions/revoke"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import RevokePermissionsEndpoint

        fake_transport.enqueue(status_code=204)
        ep = RevokePermissionsEndpoint(fake_transport)

        ep.send({"contextIdentifier": {}, "authorizedIdentifier": {}})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/permissions/revoke"


class TestEnableAttachmentsEndpoint:
    def test_url(self) -> None:
        from ksef2.endpoints.testdata import EnableAttachmentsEndpoint

        ep = EnableAttachmentsEndpoint(FakeTransport())
        assert ep.url == "/testdata/attachment"

    def test_send_posts(self, fake_transport: FakeTransport) -> None:
        from ksef2.endpoints.testdata import EnableAttachmentsEndpoint

        fake_transport.enqueue(status_code=204)
        ep = EnableAttachmentsEndpoint(fake_transport)

        ep.send({"nip": "1234567890"})

        call = fake_transport.calls[0]
        assert call.method == "POST"
        assert call.path == "/testdata/attachment"
