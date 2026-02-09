from typing import final, Any

from ksef_sdk.core import http


@final
class CreateSubjectEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/subject"

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class DeleteSubjectEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/subject/remove"

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class CreatePersonEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/person"

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class DeletePersonEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/person/remove"

    def send(self, body: dict[str, Any]) -> None:
        _ = self._transport.post(self.url, json=body)


@final
class GrantPermissionsEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/permissions"

    def send(self, body: dict[str, Any]) -> None:
        self._transport.post(self.url, json=body)


@final
class RevokePermissionsEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/permissions/revoke"

    def send(self, body: dict[str, Any]) -> None:
        self._transport.post(self.url, json=body)


@final
class EnableAttachmentsEndpoint:
    def __init__(self, transport: http.HttpTransport):
        self._transport = transport

    @property
    def url(self) -> str:
        return "/testdata/attachment-permission"

    def send(self, body: dict[str, Any]) -> None:
        self._transport.post(self.url, json=body)
