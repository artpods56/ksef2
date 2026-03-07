"""Prepare a batch ZIP, upload it, and inspect the processed session in TEST.

Prerequisites:
- none; the script provisions and cleans up its own TEST-environment data

What it demonstrates:
- preparing multiple XML invoices for a batch session
- opening a batch session and uploading encrypted parts
- closing the session and polling until processing completes
- listing processed invoices and downloading the collective UPO
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from ksef2 import Client, Environment, FormSchema
from ksef2.core.invoices import InvoiceTemplater
from ksef2.core.tools import generate_nip
from ksef2.domain.models import BatchInvoice
from scripts.examples._common import repo_root


@dataclass
class ExampleConfig:
    environment: Environment = Environment.TEST
    invoice_count: int = 2
    poll_interval: float = 2.0
    status_timeout: float = 120.0
    template_path: Path = field(
        default_factory=lambda: (
            repo_root()
            / "docs"
            / "assets"
            / "sample_invoices"
            / "fa3"
            / "invoice-template_v3.xml"
        )
    )


def build_invoices(
    *, seller_nip: str, template_xml: str, count: int
) -> list[BatchInvoice]:
    now = datetime.now(tz=timezone.utc)
    today = now.date().isoformat()
    invoices: list[BatchInvoice] = []

    for ordinal in range(1, count + 1):
        invoice_number = f"BATCH-{now:%Y%m%d%H%M%S}-{ordinal:02d}"
        invoices.append(
            BatchInvoice(
                file_name=f"invoice-{ordinal:02d}.xml",
                content=InvoiceTemplater.create(
                    template_xml,
                    {
                        "#nip#": seller_nip,
                        "#invoicing_date#": today,
                        "#invoice_number#": invoice_number,
                    },
                ),
            )
        )

    return invoices


def run(config: ExampleConfig) -> None:
    client = Client(environment=config.environment)
    seller_nip = generate_nip()

    with client.testdata.temporal() as temp:
        temp.create_subject(
            nip=seller_nip,
            subject_type="enforcement_authority",
            description="SDK batch example seller",
        )

        auth = client.authentication.with_test_certificate(nip=seller_nip)
        template_xml = config.template_path.read_text(encoding="utf-8")
        invoices = build_invoices(
            seller_nip=seller_nip,
            template_xml=template_xml,
            count=config.invoice_count,
        )

        prepared_batch = auth.batch.prepare_batch(
            invoices=invoices,
            form_code=FormSchema.FA3,
        )
        print(
            "Prepared batch with "
            f"{len(prepared_batch.invoices)} invoice(s) and "
            f"{len(prepared_batch.parts)} encrypted part(s)"
        )

        with auth.batch_session(prepared_batch=prepared_batch) as session:
            print(f"Opened batch session: {session.reference_number}")
            session.upload_parts()
            print("Uploaded all batch parts")

        print("Closed batch session and started processing")

        status = auth.batch.wait_for_completion(
            session=session,
            timeout=config.status_timeout,
            poll_interval=config.poll_interval,
        )
        print(
            "Batch session completed: "
            f"{status.status.code} {status.status.description} "
            f"(total={status.invoice_count}, ok={status.successful_invoice_count}, "
            f"failed={status.failed_invoice_count})"
        )

        if status.failed_invoice_count:
            print("Batch completed with failed invoices; inspect the status output.")

        invoices_page = auth.batch.list_invoices(session=session)
        for invoice in invoices_page.invoices:
            print(
                "Invoice result: "
                f"ref={invoice.reference_number} "
                f"ksef={invoice.ksef_number} "
                f"status={invoice.status.code} {invoice.status.description}"
            )

        if status.upo and status.upo.pages:
            for upo_page in status.upo.pages:
                upo_xml = auth.batch.get_upo(
                    session=session,
                    upo_reference_number=upo_page.reference_number,
                )
                print(
                    "Downloaded collective UPO page "
                    f"{upo_page.reference_number} of size {len(upo_xml)} bytes"
                )


def main() -> int:
    run(ExampleConfig())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
