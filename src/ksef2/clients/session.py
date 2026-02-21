from __future__ import annotations

import base64
from pathlib import Path
from typing import TYPE_CHECKING, final

from tenacity import RetryError, retry, retry_if_result, stop_after_delay, wait_fixed


from ksef2.clients.encryption import EncryptionClient
from ksef2.core import exceptions
from ksef2.core.crypto import (
    encrypt_invoice,
    select_certificate,
    encrypt_symmetric_key,
    decrypt_aes_cbc,
)
from ksef2.core import protocols
from ksef2.domain.models import invoices, InvoiceQueryFilters
from ksef2.domain.models.encryption import CertUsage
from ksef2.domain.models.invoices import (
    QueryInvoicesMetadataResponse,
    ExportInvoicesResponse,
    InvoiceExportStatusResponse,
    InvoicePackage,
)
from ksef2.domain.models.pagination import InvoiceQueryParams
from ksef2.domain.models.session import OnlineSessionState
from ksef2.endpoints.invoices import (
    DownloadInvoiceEndpoint,
    GetInvoiceUpoByKsefNumberEndpoint,
    GetInvoiceUpoByReferenceEndpoint,
    GetSessionInvoiceStatusEndpoint,
    GetSessionStatusEndpoint,
    ListFailedSessionInvoicesEndpoint,
    ListSessionInvoicesEndpoint,
    SendingInvoicesEndpoint,
    QueryInvoicesMetadataEndpoint,
    ExportInvoicesEndpoint,
    GetExportStatusEndpoint,
)
from ksef2.endpoints.session import TerminateSessionEndpoint
from ksef2.infra.schema.api import spec as spec
from ksef2.infra.mappers.requests.invoices import (
    SendInvoiceMapper,
    InvoiceQueryFiltersMapper,
    QueryInvoicesMetadataMapper,
    ExportInvoicesMapper,
    ExportStatusMapper,
)

if TYPE_CHECKING:
    from types import TracebackType

from structlog import get_logger

logger = get_logger(__name__)


@final
class OnlineSessionClient:
    def __init__(self, transport: protocols.Middleware, state: OnlineSessionState):
        self._transport = transport
        self._state = state
        self._invoice_endpoint = SendingInvoicesEndpoint(transport)
        self._download_endpoint = DownloadInvoiceEndpoint(transport)
        self._terminate_endpoint = TerminateSessionEndpoint(transport)
        self._session_status_ep = GetSessionStatusEndpoint(transport)
        self._list_invoices_ep = ListSessionInvoicesEndpoint(transport)
        self._invoice_status_ep = GetSessionInvoiceStatusEndpoint(transport)
        self._failed_invoices_ep = ListFailedSessionInvoicesEndpoint(transport)
        self._upo_by_ksef_ep = GetInvoiceUpoByKsefNumberEndpoint(transport)
        self._upo_by_ref_ep = GetInvoiceUpoByReferenceEndpoint(transport)
        self._query_metadata_ep = QueryInvoicesMetadataEndpoint(transport)
        self._export_ep = ExportInvoicesEndpoint(transport)
        self._export_status_ep = GetExportStatusEndpoint(transport)
        self._cert_client = EncryptionClient(transport)

    def query_metadata(
        self,
        *,
        filters: InvoiceQueryFilters,
        params: InvoiceQueryParams | None = None,
    ) -> QueryInvoicesMetadataResponse:
        spec_filters = InvoiceQueryFiltersMapper.map_request(filters)
        spec_resp = self._query_metadata_ep.send(
            access_token=self._state.access_token,
            body=spec_filters.model_dump(by_alias=True, exclude_none=True, mode="json"),
            **params.to_api_params()
            if params
            else InvoiceQueryParams().to_api_params(),
        )
        return QueryInvoicesMetadataMapper.map_response(spec_resp)

    def fetch_package(
        self, package: InvoicePackage, target_directory: Path | str = Path(".")
    ) -> list[Path]:
        target_path = Path(target_directory)
        target_path.mkdir(parents=True, exist_ok=True)

        saved_files: list[Path] = []

        aes_key = base64.b64decode(self._state.aes_key)
        iv = base64.b64decode(self._state.iv)

        for part in package.parts:
            logger.info(f"Downloading part: {part.part_name}")

            resp = self._transport.get(str(part.url))
            resp.raise_for_status()

            zip_data = decrypt_aes_cbc(resp.content, key=aes_key, iv=iv)

            output_filename = part.part_name.replace(".aes", "")
            output_file = target_path / output_filename

            with open(output_file, "wb") as f:
                f.write(zip_data)

            logger.info(f"Saved decrypted package to: {output_file}")
            saved_files.append(output_file)

        return saved_files

    def fetch_package_bytes(self, package: InvoicePackage) -> list[bytes]:
        aes_key = base64.b64decode(self._state.aes_key)
        iv = base64.b64decode(self._state.iv)

        result: list[bytes] = []
        for part in package.parts:
            logger.info(f"Downloading part: {part.part_name}")
            resp = self._transport.get(str(part.url))
            resp.raise_for_status()
            result.append(decrypt_aes_cbc(resp.content, key=aes_key, iv=iv))
        return result

    def schedule_invoices_export(
        self,
        *,
        filters: InvoiceQueryFilters,
    ) -> ExportInvoicesResponse:
        certificate = select_certificate(
            # [TODO]: client should use shared cert store to fetch certs
            certificates=self._cert_client.get_certificates(),
            usage=CertUsage.SYMMETRIC_KEY_ENCRYPTION,
        )
        raw_aes_key = base64.b64decode(self._state.aes_key)

        aes_key = encrypt_symmetric_key(
            key=raw_aes_key, cert_b64=certificate.certificate
        )

        spec_request = ExportInvoicesMapper.map_request(
            filters,
            aes_key,
            self._state.iv,
        )
        spec_resp = self._export_ep.send(
            access_token=self._state.access_token,
            body=spec_request.model_dump(by_alias=True, exclude_none=True, mode="json"),
        )
        return ExportInvoicesMapper.map_response(spec_resp)

    def get_export_status(
        self,
        *,
        reference_number: str,
    ) -> InvoiceExportStatusResponse:
        spec_resp = self._export_status_ep.send(
            access_token=self._state.access_token,
            reference_number=reference_number,
        )
        return ExportStatusMapper.map_response(spec_resp)

    def send_invoice(self, *, invoice_xml: bytes) -> invoices.SendInvoiceResponse:
        encrypted = encrypt_invoice(
            xml_bytes=invoice_xml,
            key=base64.b64decode(self._state.aes_key),
            iv=base64.b64decode(self._state.iv),
        )
        request_body = SendInvoiceMapper.map_request(invoice_xml, encrypted)

        response_dto = self._invoice_endpoint.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            body=request_body.model_dump(),
        )

        return SendInvoiceMapper.map_response(response_dto)

    def download_invoice(self, *, ksef_number: str) -> bytes:
        return self._download_endpoint.send(
            access_token=self._state.access_token,
            ksef_number=ksef_number,
        )

    def get_status(self) -> spec.SessionStatusResponse:
        return self._session_status_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
        )

    def list_invoices(
        self,
        *,
        page_size: int = 10,
        continuation_token: str | None = None,
    ) -> spec.SessionInvoicesResponse:
        return self._list_invoices_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            page_size=page_size,
            continuation_token=continuation_token,
        )

    def get_invoice_status(
        self, invoice_reference_number: str
    ) -> spec.SessionInvoiceStatusResponse:
        return self._invoice_status_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            invoice_reference_number=invoice_reference_number,
        )

    def list_failed_invoices(
        self,
        *,
        page_size: int = 10,
        continuation_token: str | None = None,
    ) -> spec.SessionInvoicesResponse:
        return self._failed_invoices_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            page_size=page_size,
            continuation_token=continuation_token,
        )

    def get_invoice_upo_by_ksef_number(self, ksef_number: str) -> bytes:
        return self._upo_by_ksef_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            ksef_number=ksef_number,
        )

    def get_invoice_upo_by_reference(self, invoice_reference_number: str) -> bytes:
        return self._upo_by_ref_ep.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
            invoice_reference_number=invoice_reference_number,
        )

    def terminate(self) -> None:
        self._terminate_endpoint.send(
            access_token=self._state.access_token,
            reference_number=self._state.reference_number,
        )

    def wait_for_invoices(
        self,
        *,
        filters: InvoiceQueryFilters,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> QueryInvoicesMetadataResponse:
        @retry(
            stop=stop_after_delay(timeout),
            wait=wait_fixed(poll_interval),
            retry=retry_if_result(lambda r: not r.invoices),
            reraise=True,
        )
        def _poll() -> QueryInvoicesMetadataResponse:
            return self.query_metadata(filters=filters)

        try:
            return _poll()
        except RetryError:
            raise exceptions.KSeFInvoiceQueryTimeoutError(timeout=timeout)

    def wait_for_export_package(
        self,
        *,
        reference_number: str,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> InvoicePackage:
        @retry(
            stop=stop_after_delay(timeout),
            wait=wait_fixed(poll_interval),
            retry=retry_if_result(lambda s: not (s.package and s.package.parts)),
            reraise=True,
        )
        def _poll() -> InvoiceExportStatusResponse:
            return self.get_export_status(reference_number=reference_number)

        try:
            status = _poll()
        except RetryError:
            raise exceptions.KSeFExportTimeoutError(
                reference_number=reference_number,
                timeout=timeout,
            )
        assert status.package is not None  # guaranteed by retry condition
        return status.package

    def export_and_download(
        self,
        *,
        filters: InvoiceQueryFilters,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> list[bytes]:
        export = self.schedule_invoices_export(filters=filters)
        package = self.wait_for_export_package(
            reference_number=export.reference_number,
            timeout=timeout,
            poll_interval=poll_interval,
        )
        return self.fetch_package_bytes(package=package)

    def get_state(self) -> OnlineSessionState:
        return self._state

    def __enter__(self) -> OnlineSessionClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            self.terminate()
        except exceptions.KSeFException:
            logger.warning("Failed to terminate KSeF session, might be already closed.")
        except Exception:
            logger.exception("Unexpected error during session termination.")
