from pathlib import Path

from ksef2.services.renderers import InvoicePDFExporter, InvoiceXSLTRenderer


def main(source_dir: Path, output_dir: Path):
    print(f"Input directory: {source_dir}")
    print(f"Output directory: {output_dir}")

    exporter = InvoicePDFExporter()

    html_exporter = InvoiceXSLTRenderer()

    for path in source_dir.glob("*.xml"):
        print(f"Exporting {path.name} ...")
        
        
        print("Exporting to HTML ...")
        exported_html_path = html_exporter.render_to_file(
            path, output_dir / f"{path.stem}.html"
        )
        print(f"  Saved to: {exported_html_path}")
         
        print("Exporting to PDF ...")
        exported_file_path = exporter.export_to_file(
            path, output_dir / f"{path.stem}.pdf"
        )
        print(f"  Saved to: {exported_file_path}")


if __name__ == "__main__":
    ROOT = Path(__file__).parents[3]

    INPUT_DIR = ROOT / "docs" / "assets" / "sample_invoices" / "fa3"
    OUTPUT_DIR = ROOT / "output" / "pdf_exports"

    print(f"Input directory: {INPUT_DIR}dd")

    main(source_dir=INPUT_DIR, output_dir=OUTPUT_DIR)
