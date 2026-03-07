"""Submit a batch with one high-level call and inspect the processed session in TEST.

Prerequisites:
- none; the script provisions and cleans up its own TEST-environment data

What it demonstrates:
- preparing multiple XML invoices in memory
- submitting a batch with `auth.batch.submit_batch()`
- polling until the batch session completes
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
        invoice_number = f"BATCH-FAST-{now:%Y%m%d%H%M%S}-{ordinal:02d}"
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
            description="SDK batch submit example seller",
        )

        auth = client.authentication.with_test_certificate(nip=seller_nip)
        template_xml = config.template_path.read_text(encoding="utf-8")
        invoices = build_invoices(
            seller_nip=seller_nip,
            template_xml=template_xml,
            count=config.invoice_count,
        )

        state = auth.batch.submit_batch(
            invoices=invoices,
            form_code=FormSchema.FA3,
        )
        print(f"Submitted batch session: {state.reference_number}")

        status = auth.batch.wait_for_completion(
            session=state,
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

        invoices_page = auth.batch.list_invoices(session=state)
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
                    session=state,
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
