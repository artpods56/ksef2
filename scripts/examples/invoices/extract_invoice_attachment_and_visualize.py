from xsdata.formats.dataclass.parsers.config import ParserConfig
from ksef2.infra.schema.fa3.models import Faktura
from xsdata_pydantic.bindings import XmlParser

from ksef2.infra.mappers.invoices.fa3 import AttachmentMapper
from ksef2.services.renderers import AttachmentHTMLRenderer, AttachmentCSVExporter
from scripts.examples._common import repo_root

INVOICE_TEMPLATE_PATH = (
    repo_root()
    / "docs"
    / "assets"
    / "sample_invoices"
    / "sample_fa3_invoice_with_attachment.xml"
)

OUTPUT_DIR = repo_root() / "output"


def main():

    config = ParserConfig()
    parser = XmlParser(config=config)

    with open(INVOICE_TEMPLATE_PATH, "rb") as f:
        invoice: Faktura = parser.parse(f, Faktura)

    print("Raw invoice XML:")
    print(invoice.model_dump_json(indent=2, exclude_none=True))

    if invoice.zalacznik:
        print("Exporting invoice attachment ...")

        # maps parsed xml data to our domain classes
        attachment = AttachmentMapper.map_attachment(invoice.zalacznik)
        print("Invoice attachment after mapping:")
        print(attachment.model_dump_json(indent=2, exclude_none=True))

        # create output directory
        OUTPUT_DIR.mkdir(exist_ok=True)

        # Render to HTML
        html_renderer = AttachmentHTMLRenderer()
        html_path = html_renderer.render_to_file(
            attachment, OUTPUT_DIR / "attachment.html", title="Invoice Attachment"
        )
        print(f"HTML attachment saved to: {html_path}")

        csv_exporter = AttachmentCSVExporter()
        csv_files = csv_exporter.export_all_tables(
            attachment, OUTPUT_DIR / "csv", prefix="attachment_table"
        )
        print(f"CSV files saved to: {csv_files}")

    else:
        print("No attachment found.")


if __name__ == "__main__":
    main()
