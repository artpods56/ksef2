from typing import final, Any

from ksef2.core import middleware


@final
class CreateSubjectEndpoint:
    url: str = "/testdata/subject"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class DeleteSubjectEndpoint:
    url: str = "/testdata/subject/remove"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class CreatePersonEndpoint:
    url: str = "/testdata/person"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class DeletePersonEndpoint:
    url: str = "/testdata/person/remove"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class GrantPermissionsEndpoint:
    url: str = "/testdata/permissions"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class RevokePermissionsEndpoint:
    url: str = "/testdata/permissions/revoke"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class EnableAttachmentsEndpoint:
    url: str = "/testdata/attachment"

    def __init__(self, transport: middleware.KSeFProtocol):
        self._transport = transport

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)
