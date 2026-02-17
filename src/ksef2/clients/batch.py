"""Batch session client for managing batch upload sessions."""

from typing import final

from ksef2.core import protocols
from ksef2.domain.models.batch import PartUploadRequest
from ksef2.domain.models import BatchSessionState
from ksef2.endpoints.session import CloseBatchSessionEndpoint


@final
class BatchSessionClient:
    """Client for managing an active batch session.

    This client is returned when opening a batch session and provides
    methods for managing the session lifecycle.
    """

    def __init__(
        self,
        transport: protocols.Middleware,
        state: BatchSessionState,
    ):
        self._transport = transport
        self._state = state
        self._close_ep = CloseBatchSessionEndpoint(transport)

    @property
    def reference_number(self) -> str:
        """Get the batch session reference number."""
        return self._state.reference_number

    @property
    def access_token(self) -> str:
        """Get the access token for this session."""
        return self._state.access_token

    @property
    def aes_key(self) -> bytes:
        """Get the AES key for encrypting batch files."""
        return self._state.get_aes_key_bytes()

    @property
    def iv(self) -> bytes:
        """Get the initialization vector for AES encryption."""
        return self._state.get_iv_bytes()

    @property
    def part_upload_requests(self) -> list[PartUploadRequest]:
        """Get the upload instructions for each file part."""
        return self._state.part_upload_requests

    def get_state(self) -> BatchSessionState:
        """Get the serializable state of this batch session.

        The returned state can be serialized to JSON and used later
        to resume the session or access upload URLs.

        Returns:
            BatchSessionState containing all session information.
        """
        return self._state

    def close(self) -> None:
        """Close the batch session and start processing.

        This triggers processing of the invoice batch and generation of UPO
        for valid invoices and a collective UPO for the session.
        """
        self._close_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
        )
