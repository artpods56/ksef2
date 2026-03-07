from collections.abc import Callable, Iterable
from io import BytesIO
from pathlib import Path
from typing import final
from zipfile import ZIP_DEFLATED, ZipFile

from tenacity import RetryError, retry, retry_if_result, stop_after_delay, wait_fixed

from ksef2.clients.batch import BatchSessionClient
from ksef2.core import exceptions
from ksef2.core.crypto import encrypt_invoice, sha256_b64
from ksef2.core.protocols import Middleware
from ksef2.domain.models.batch import (
    BatchEncryptionData,
    BatchFileInfo,
    BatchFilePart,
    BatchInvoice,
    BatchInvoiceHash,
    BatchPreparedPart,
    BatchSessionState,
    PreparedBatch,
)
from ksef2.domain.models.session import (
    FormSchema,
    SessionInvoicesResponse,
    SessionStatusResponse,
)
from ksef2.endpoints.invoices import InvoicesEndpoints
from ksef2.endpoints.session import SessionEndpoints
from ksef2.infra.mappers.sessions import from_spec as session_from_spec

MAX_BATCH_PART_SIZE = 100_000_000


@final
class BatchService:
    """High-level workflow for preparing and sending invoice batches."""

    def __init__(
        self,
        *,
        authed_transport: Middleware,
        upload_transport: Middleware,
        get_encryption_key: Callable[[], tuple[bytes, bytes, bytes]],
        open_batch_session: Callable[..., BatchSessionClient],
    ) -> None:
        self._invoice_eps = InvoicesEndpoints(authed_transport)
        self._session_eps = SessionEndpoints(authed_transport)
        self._upload_transport = upload_transport
        self._get_encryption_key = get_encryption_key
        self._open_batch_session = open_batch_session

    def prepare_batch(
        self,
        *,
        invoices: Iterable[BatchInvoice],
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
        max_part_size: int = MAX_BATCH_PART_SIZE,
    ) -> PreparedBatch:
        """Build a ZIP package, split it, and encrypt each upload part.

        Args:
            invoices: Invoice XML payloads to include in the batch package.
            form_code: Invoice schema declared for the batch session.
            offline_mode: Whether to declare offline invoicing mode for the batch.
            max_part_size: Maximum size of each ZIP part before encryption.

        Returns:
            A prepared batch with encrypted part payloads and the metadata required
            to open a batch session.
        """
        normalized = list(invoices)
        self._validate_invoices(normalized)
        self._validate_max_part_size(max_part_size)

        aes_key, iv, encrypted_key = self._get_encryption_key()
        zip_bytes = self._build_zip(normalized)
        raw_parts = self._split_bytes(zip_bytes, max_part_size=max_part_size)

        prepared_parts: list[BatchPreparedPart] = []
        declared_parts: list[BatchFilePart] = []

        for ordinal_number, raw_part in enumerate(raw_parts, start=1):
            encrypted_part = self._encrypt_batch_part(
                payload=raw_part,
                aes_key=aes_key,
                iv=iv,
            )
            part_hash = sha256_b64(encrypted_part)
            prepared_parts.append(
                BatchPreparedPart(
                    ordinal_number=ordinal_number,
                    content=encrypted_part,
                    file_size=len(encrypted_part),
                    file_hash=part_hash,
                )
            )
            declared_parts.append(
                BatchFilePart(
                    ordinal_number=ordinal_number,
                    file_size=len(encrypted_part),
                    file_hash=part_hash,
                )
            )

        return PreparedBatch(
            form_code=form_code,
            offline_mode=offline_mode,
            batch_file=BatchFileInfo(
                file_size=len(zip_bytes),
                file_hash=sha256_b64(zip_bytes),
                parts=declared_parts,
            ),
            parts=prepared_parts,
            encryption=BatchEncryptionData.from_bytes(
                aes_key=aes_key,
                iv=iv,
                encrypted_key=encrypted_key,
            ),
            invoices=[
                BatchInvoiceHash(
                    file_name=invoice.file_name,
                    invoice_hash=sha256_b64(invoice.content),
                )
                for invoice in normalized
            ],
        )

    def prepare_batch_from_paths(
        self,
        *,
        invoice_paths: Iterable[Path | str],
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
        max_part_size: int = MAX_BATCH_PART_SIZE,
    ) -> PreparedBatch:
        """Load invoice XML files from disk and prepare a batch package.

        Args:
            invoice_paths: Paths to XML files that should be added to the batch.
            form_code: Invoice schema declared for the batch session.
            offline_mode: Whether to declare offline invoicing mode for the batch.
            max_part_size: Maximum size of each ZIP part before encryption.

        Returns:
            A prepared batch with encrypted parts ready to be uploaded.
        """
        invoices = [
            BatchInvoice(file_name=Path(path).name, content=Path(path).read_bytes())
            for path in invoice_paths
        ]
        return self.prepare_batch(
            invoices=invoices,
            form_code=form_code,
            offline_mode=offline_mode,
            max_part_size=max_part_size,
        )

    def open_session(self, *, prepared_batch: PreparedBatch) -> BatchSessionClient:
        """Open a batch session for an already prepared package.

        Args:
            prepared_batch: Prepared batch payload returned by ``prepare_batch()``.

        Returns:
            A session client exposing the upload instructions returned by KSeF.
        """
        encryption = prepared_batch.encryption
        return self._open_batch_session(
            batch_file=prepared_batch.batch_file,
            aes_key=encryption.get_aes_key_bytes(),
            iv=encryption.get_iv_bytes(),
            encrypted_key=encryption.get_encrypted_key_bytes(),
            form_code=prepared_batch.form_code,
            offline_mode=prepared_batch.offline_mode,
            prepared_batch=prepared_batch,
        )

    def upload_parts(
        self,
        *,
        session: BatchSessionClient,
        prepared_batch: PreparedBatch,
    ) -> None:
        """Upload all prepared batch parts using the session's presigned URLs.

        Args:
            session: Open batch session that already contains upload instructions.
            prepared_batch: Prepared batch whose part ordinals match the session.
        """
        upload_requests = {
            request.ordinal_number: request for request in session.part_upload_requests
        }
        parts = {part.ordinal_number: part for part in prepared_batch.parts}

        if set(upload_requests) != set(parts):
            raise exceptions.KSeFValidationError(
                "Prepared parts do not match the batch session upload instructions.",
                upload_ordinals=sorted(upload_requests),
                prepared_ordinals=sorted(parts),
            )

        for ordinal_number in sorted(upload_requests):
            upload_request = upload_requests[ordinal_number]
            part = parts[ordinal_number]
            _ = self._upload_transport.request(
                upload_request.method,
                upload_request.url,
                headers={
                    "Content-Type": "application/octet-stream",
                    **{
                        key: value
                        for key, value in upload_request.headers.items()
                        if value is not None
                    },
                },
                content=part.content,
            )

    def submit_prepared_batch(
        self, *, prepared_batch: PreparedBatch
    ) -> BatchSessionState:
        """Open, upload, and close a batch session for a prepared package.

        Args:
            prepared_batch: Prepared batch payload returned by ``prepare_batch()``.

        Returns:
            Serializable state of the submitted batch session.
        """
        with self.open_session(prepared_batch=prepared_batch) as session:
            state = session.get_state()
            session.upload_parts()
        return state

    def submit_batch(
        self,
        *,
        invoices: Iterable[BatchInvoice],
        form_code: FormSchema = FormSchema.FA3,
        offline_mode: bool = False,
        max_part_size: int = MAX_BATCH_PART_SIZE,
    ) -> BatchSessionState:
        """Prepare and submit a batch in one call.

        Args:
            invoices: Invoice XML payloads to include in the batch package.
            form_code: Invoice schema declared for the batch session.
            offline_mode: Whether to declare offline invoicing mode for the batch.
            max_part_size: Maximum size of each ZIP part before encryption.

        Returns:
            Serializable state of the submitted batch session.
        """
        prepared_batch = self.prepare_batch(
            invoices=invoices,
            form_code=form_code,
            offline_mode=offline_mode,
            max_part_size=max_part_size,
        )
        return self.submit_prepared_batch(prepared_batch=prepared_batch)

    def get_status(
        self,
        *,
        session: str | BatchSessionState | BatchSessionClient,
    ) -> SessionStatusResponse:
        """Fetch the current status of a batch session.

        Args:
            session: Session reference number, persisted state, or open session client.

        Returns:
            Current batch session status as reported by KSeF.
        """
        return session_from_spec(
            self._invoice_eps.get_session_status(
                reference_number=self._resolve_reference_number(session),
            )
        )

    def list_invoices(
        self,
        *,
        session: str | BatchSessionState | BatchSessionClient,
        page_size: int = 10,
        continuation_token: str | None = None,
    ) -> SessionInvoicesResponse:
        return session_from_spec(
            self._invoice_eps.list_session_invoices(
                reference_number=self._resolve_reference_number(session),
                continuation_token=continuation_token,
                pageSize=page_size,
            )
        )

    def list_failed_invoices(
        self,
        *,
        session: str | BatchSessionState | BatchSessionClient,
        page_size: int = 10,
        continuation_token: str | None = None,
    ) -> SessionInvoicesResponse:
        return session_from_spec(
            self._invoice_eps.list_failed_session_invoices(
                reference_number=self._resolve_reference_number(session),
                continuation_token=continuation_token,
                pageSize=page_size,
            )
        )

    def get_upo(
        self,
        *,
        session: str | BatchSessionState | BatchSessionClient,
        upo_reference_number: str,
    ) -> bytes:
        """Download the collective UPO for a batch session.

        Args:
            session: Session reference number, persisted state, or open session client.
            upo_reference_number: UPO page reference returned in the session status.

        Returns:
            Raw XML bytes of the requested UPO page.
        """
        return self._session_eps.get_session_upo(
            reference_number=self._resolve_reference_number(session),
            upo_reference_number=upo_reference_number,
        )

    def wait_for_completion(
        self,
        *,
        session: str | BatchSessionState | BatchSessionClient,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> SessionStatusResponse:
        """Poll a batch session until KSeF reports a terminal status.

        Args:
            session: Session reference number, persisted state, or open session client.
            timeout: Maximum number of seconds to wait for completion.
            poll_interval: Delay between status checks.

        Returns:
            Final successful batch session status.
        """
        reference_number = self._resolve_reference_number(session)

        retry_predicate: Callable[[SessionStatusResponse], bool] = lambda status: (
            status.status.code < 200
        )

        @retry(
            stop=stop_after_delay(timeout),
            wait=wait_fixed(poll_interval),
            retry=retry_if_result(retry_predicate),
            reraise=True,
        )
        def _poll() -> SessionStatusResponse:
            return self.get_status(session=reference_number)

        try:
            status = _poll()
        except RetryError as exc:
            raise exceptions.KSeFBatchSessionTimeoutError(
                reference_number=reference_number,
                timeout=timeout,
            ) from exc

        if status.status.code >= 400:
            raise exceptions.KSeFSessionError(
                "Batch session processing failed: "
                f"{reference_number} ({status.status.code}: {status.status.description})"
            )

        return status

    @staticmethod
    def _validate_invoices(invoices: list[BatchInvoice]) -> None:
        if not invoices:
            raise exceptions.KSeFValidationError(
                "At least one invoice is required to build a batch package."
            )

        file_names = [invoice.file_name for invoice in invoices]
        if any(not name for name in file_names):
            raise exceptions.KSeFValidationError(
                "Every batch invoice must define a non-empty file name."
            )

        if len(file_names) != len(set(file_names)):
            raise exceptions.KSeFValidationError(
                "Batch invoice file names must be unique.",
                duplicate_file_names=sorted(
                    {name for name in file_names if file_names.count(name) > 1}
                ),
            )

    @staticmethod
    def _validate_max_part_size(max_part_size: int) -> None:
        if max_part_size < 1 or max_part_size > MAX_BATCH_PART_SIZE:
            raise exceptions.KSeFValidationError(
                "max_part_size must be between 1 and 100000000 bytes.",
                max_part_size=max_part_size,
            )

    @staticmethod
    def _build_zip(invoices: list[BatchInvoice]) -> bytes:
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, mode="w", compression=ZIP_DEFLATED) as archive:
            for invoice in invoices:
                archive.writestr(invoice.file_name, invoice.content)
        return zip_buffer.getvalue()

    @staticmethod
    def _split_bytes(payload: bytes, *, max_part_size: int) -> list[bytes]:
        return [
            payload[offset : offset + max_part_size]
            for offset in range(0, len(payload), max_part_size)
        ]

    @staticmethod
    def _encrypt_batch_part(
        *,
        payload: bytes,
        aes_key: bytes,
        iv: bytes,
    ) -> bytes:
        return encrypt_invoice(payload, key=aes_key, iv=iv)

    @staticmethod
    def _resolve_reference_number(
        session: str | BatchSessionState | BatchSessionClient,
    ) -> str:
        if isinstance(session, str):
            return session
        if isinstance(session, BatchSessionClient):
            return session.get_state().reference_number
        return session.reference_number
