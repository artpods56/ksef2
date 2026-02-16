from typing import Any, TypedDict, NotRequired, final, Unpack
from urllib.parse import urlencode

from pydantic import TypeAdapter

from ksef2.core import headers, codecs, protocols
from ksef2.infra.schema.api import spec as spec


PaginationQueryParams = TypedDict(
    "PaginationQueryParams",
    {
        "pageOffset": NotRequired[int | None],
        "pageSize": NotRequired[int | None],
    },
)


PAGINATION_PARAMS_ADAPTER = TypeAdapter(PaginationQueryParams)


@final
class GrantPersonPermissionsEndpoint:
    url: str = "/permissions/persons/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GrantEntityPermissionsEndpoint:
    url: str = "/permissions/entities/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GrantAuthorizationPermissionsEndpoint:
    url: str = "/permissions/authorizations/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GrantIndirectPermissionsEndpoint:
    url: str = "/permissions/indirect/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GrantSubunitPermissionsEndpoint:
    url: str = "/permissions/subunits/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GrantEuEntityPermissionsEndpoint:
    url: str = "/permissions/eu-entities/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GrantEuEntityAdministrationPermissionsEndpoint:
    url: str = "/permissions/eu-entities/administration/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.PermissionsOperationResponse,
        )


@final
class RevokeAuthorizationPermissionsEndpoint:
    url: str = "/permissions/authorizations/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        permission_id: str,
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.delete(
                f"{self.url}/{permission_id}",
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.PermissionsOperationResponse,
        )


@final
class RevokeCommonPermissionsEndpoint:
    url: str = "/permissions/common/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        permission_id: str,
    ) -> spec.PermissionsOperationResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.delete(
                f"{self.url}/{permission_id}",
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.PermissionsOperationResponse,
        )


@final
class GetAttachmentPermissionStatusEndpoint:
    url: str = "/permissions/attachments/status"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(self, access_token: str) -> spec.CheckAttachmentPermissionStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                self.url,
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.CheckAttachmentPermissionStatusResponse,
        )


@final
class GetPermissionOperationStatusEndpoint:
    url: str = "/permissions/operations"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self, access_token: str, reference_number: str
    ) -> spec.PermissionsOperationStatusResponse:
        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                f"{self.url}/{reference_number}",
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.PermissionsOperationStatusResponse,
        )


@final
class GetEntityRolesEndpoint:
    url: str = "/permissions/query/entities/roles"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QueryEntityRolesResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        query_string = urlencode(query_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.get(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
            ),
            spec.QueryEntityRolesResponse,
        )


@final
class QueryAuthorizationsPermissionsEndpoint:
    url: str = "/permissions/query/authorizations/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        *,
        access_token: str,
        body: dict[str, Any],
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QueryEntityAuthorizationPermissionsResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        path = f"{self.url}?{urlencode(query_params)}"

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QueryEntityAuthorizationPermissionsResponse,
        )


@final
class QueryEuEntitiesPermissionsEndpoint:
    url: str = "/permissions/query/eu-entities/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QueryEuEntityPermissionsResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        query_string = urlencode(query_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QueryEuEntityPermissionsResponse,
        )


@final
class QueryPersonalPermissionsEndpoint:
    url: str = "/permissions/query/personal/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QueryPersonalPermissionsResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        query_string = urlencode(query_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QueryPersonalPermissionsResponse,
        )


@final
class QueryPersonsPermissionsEndpoint:
    url: str = "/permissions/query/persons/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        *,
        access_token: str,
        body: dict[str, Any],
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QueryPersonPermissionsResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        path = f"{self.url}?{urlencode(query_params, doseq=True)}"

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QueryPersonPermissionsResponse,
        )


@final
class QuerySubordinateEntitiesRolesEndpoint:
    url: str = "/permissions/query/subordinate-entities/roles"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QuerySubordinateEntityRolesResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        query_string = urlencode(query_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QuerySubordinateEntityRolesResponse,
        )


@final
class QuerySubunitsPermissionsEndpoint:
    url: str = "/permissions/query/subunits/grants"

    def __init__(self, transport: protocols.Middleware):
        self._transport = transport

    def send(
        self,
        access_token: str,
        body: dict[str, Any],
        **params: Unpack[PaginationQueryParams],
    ) -> spec.QuerySubunitPermissionsResponse:
        query_params = PAGINATION_PARAMS_ADAPTER.validate_python(params)
        query_string = urlencode(query_params)
        path = f"{self.url}?{query_string}" if query_string else self.url

        return codecs.JsonResponseCodec.parse(
            self._transport.post(
                path,
                headers=headers.KSeFHeaders.bearer(access_token),
                json=body,
            ),
            spec.QuerySubunitPermissionsResponse,
        )
