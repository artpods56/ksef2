"""CSV exporter for attachment tables."""

import csv
from io import StringIO
from pathlib import Path

from ksef2.domain.models.fa3.attachment import Attachment, AttachmentTable


class AttachmentCSVExporter:
    """Exports Attachment tables to CSV format.

    Each table is exported as a separate CSV file or string.
    Uses Python's built-in csv module for compatibility.
    """

    def __init__(self, delimiter: str = ",", include_metadata: bool = True):
        """Initialize CSV exporter.

        Args:
            delimiter: CSV field delimiter (default comma).
            include_metadata: Whether to include table metadata as comment rows.
        """
        self.delimiter = delimiter
        self.include_metadata = include_metadata

    def export_table(self, table: AttachmentTable) -> str:
        """Export a single table to CSV string.

        Args:
            table: The AttachmentTable to export.

        Returns:
            CSV content as string.
        """
        output = StringIO()
        writer = csv.writer(output, delimiter=self.delimiter)

        # Metadata as comments
        if self.include_metadata:
            if table.description:
                writer.writerow([f"# Description: {table.description}"])
            if table.meta_data:
                for meta in table.meta_data:
                    writer.writerow([f"# {meta.key}: {meta.value}"])

        # Header row with column names
        header = [col.name for col in table.header.columns]
        writer.writerow(header)

        # Data rows
        for row in table.rows:
            writer.writerow(row.cells)

        # Summary row (if present)
        if table.summary:
            writer.writerow(table.summary.cells)

        return output.getvalue()

    def export_table_to_file(self, table: AttachmentTable, path: str | Path) -> Path:
        """Export a single table to CSV file.

        Args:
            table: The AttachmentTable to export.
            path: Output file path.

        Returns:
            Path to the created file.
        """
        path = Path(path)
        csv_content = self.export_table(table)
        path.write_text(csv_content, encoding="utf-8")
        return path

    def export_all_tables(
        self, attachment: Attachment, output_dir: str | Path, prefix: str = "table"
    ) -> list[Path]:
        """Export all tables from an attachment to separate CSV files.

        Args:
            attachment: The Attachment containing tables.
            output_dir: Directory to write CSV files.
            prefix: Filename prefix for exported files.

        Returns:
            List of paths to created files.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        created_files: list[Path] = []
        table_index = 0

        for block_index, block in enumerate(attachment.data_blocks, 1):
            if not block.tables:
                continue

            for table in block.tables:
                table_index += 1
                filename = f"{prefix}_{block_index}_{table_index}.csv"
                file_path = output_dir / filename
                self.export_table_to_file(table, file_path)
                created_files.append(file_path)

        return created_files

    def export_to_single_csv(self, attachment: Attachment, path: str | Path) -> Path:
        """Export all tables to a single CSV file with separators.

        Tables are separated by blank lines and block/table headers.

        Args:
            attachment: The Attachment containing tables.
            path: Output file path.

        Returns:
            Path to the created file.
        """
        path = Path(path)
        output = StringIO()
        writer = csv.writer(output, delimiter=self.delimiter)

        table_index = 0
        for block_index, block in enumerate(attachment.data_blocks, 1):
            if not block.tables:
                continue

            block_header = block.header or f"Data Block {block_index}"

            for table in block.tables:
                table_index += 1

                # Separator and header
                if table_index > 1:
                    writer.writerow([])  # Blank line separator

                writer.writerow([f"### {block_header} - Table {table_index} ###"])

                # Table content (reuse export_table logic but inline)
                if self.include_metadata:
                    if table.description:
                        writer.writerow([f"# Description: {table.description}"])
                    if table.meta_data:
                        for meta in table.meta_data:
                            writer.writerow([f"# {meta.key}: {meta.value}"])

                header = [col.name for col in table.header.columns]
                writer.writerow(header)

                for row in table.rows:
                    writer.writerow(row.cells)

                if table.summary:
                    writer.writerow(table.summary.cells)

        path.write_text(output.getvalue(), encoding="utf-8")
        return path
