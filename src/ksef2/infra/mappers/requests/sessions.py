from collections import namedtuple

from ksef2.domain.models.session import OpenOnlineSessionRequest
from ksef2.infra.mappers.sessions import from_spec, to_spec

OpenSessionData = namedtuple("OpenSessionData", ["reference_number", "valid_until"])


class OpenOnlineSessionMapper:
    @staticmethod
    def map_request(
        encrypted_key: bytes,
        iv: bytes,
        form_code,
    ):
        return to_spec(
            OpenOnlineSessionRequest(
                encrypted_key=encrypted_key,
                iv=iv,
                form_code=form_code,
            )
        )

    @staticmethod
    def map_response(response):
        mapped = from_spec(response)
        return OpenSessionData(
            reference_number=mapped.reference_number,
            valid_until=mapped.valid_until,
        )


class QuerySessionsMapper:
    @staticmethod
    def map_response(response):
        return from_spec(response)
