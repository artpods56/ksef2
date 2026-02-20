"""HTML renderer for attachment data."""

from pathlib import Path

from ksef2.domain.models.fa3.attachment import (
    Attachment,
    AttachmentTable,
    AttachmentText,
    DataBlock,
    TableColumnType,
)


class AttachmentHTMLRenderer:
    """Renders Attachment domain models to HTML.

    The generated HTML is self-contained with embedded CSS,
    suitable for viewing in a browser or converting to PDF.
    """

    CSS = """
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .attachment { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .data-block { margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid #eee; }
        .data-block:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
        .block-header { font-size: 1.4em; font-weight: 600; color: #333; margin-bottom: 16px; }
        .metadata { background: #f8f9fa; padding: 12px 16px; border-radius: 4px; margin-bottom: 16px; }
        .metadata-item { display: inline-block; margin-right: 24px; }
        .metadata-key { font-weight: 600; color: #666; }
        .metadata-value { color: #333; }
        .text-block { margin-bottom: 16px; }
        .text-block p { margin: 0 0 8px 0; }
        .table-container { margin-bottom: 20px; overflow-x: auto; }
        .table-description { font-style: italic; color: #666; margin-bottom: 8px; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
        th, td { padding: 10px 12px; text-align: left; border: 1px solid #ddd; }
        th { background: #4a90d9; color: white; font-weight: 600; }
        th .col-type { font-weight: normal; font-size: 0.8em; opacity: 0.8; }
        tr:nth-child(even) { background: #f8f9fa; }
        tr:hover { background: #e8f4ff; }
        .summary-row { background: #fff3cd !important; font-weight: 600; }
        .col-int, .col-dec { text-align: right; }
        .col-date, .col-datetime, .col-time { text-align: center; }
        @media print {
            body { background: white; padding: 0; }
            .attachment { box-shadow: none; padding: 0; }
        }
    </style>
    """

    COLUMN_TYPE_LABELS = {
        TableColumnType.DATE: "date",
        TableColumnType.DATETIME: "datetime",
        TableColumnType.DECIMAL: "decimal",
        TableColumnType.INTEGER: "integer",
        TableColumnType.TIME: "time",
        TableColumnType.TEXT: "text",
    }

    def render(self, attachment: Attachment, title: str = "Invoice Attachment") -> str:
        """Render attachment to HTML string.

        Args:
            attachment: The Attachment domain model to render.
            title: HTML page title.

        Returns:
            Complete HTML document as string.
        """
        blocks_html = "\n".join(
            self._render_data_block(block, i)
            for i, block in enumerate(attachment.data_blocks, 1)
        )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._escape(title)}</title>
    {self.CSS}
</head>
<body>
    <div class="attachment">
        {blocks_html}
    </div>
</body>
</html>"""

    def render_to_file(
        self,
        attachment: Attachment,
        path: str | Path,
        title: str = "Invoice Attachment",
    ) -> Path:
        """Render attachment to HTML file.

        Args:
            attachment: The Attachment domain model to render.
            path: Output file path.
            title: HTML page title.

        Returns:
            Path to the created file.
        """
        path = Path(path)
        html = self.render(attachment, title)
        path.write_text(html, encoding="utf-8")
        return path

    def _render_data_block(self, block: DataBlock, index: int) -> str:
        """Render a single data block."""
        parts = ['<div class="data-block">']

        # Header
        header_text = block.header or f"Data Block {index}"
        parts.append(f'<div class="block-header">{self._escape(header_text)}</div>')

        # Metadata
        if block.meta_data:
            meta_items = "".join(
                f'<span class="metadata-item"><span class="metadata-key">{self._escape(m.key)}:</span> '
                f'<span class="metadata-value">{self._escape(m.value)}</span></span>'
                for m in block.meta_data
            )
            parts.append(f'<div class="metadata">{meta_items}</div>')

        # Text
        if block.text:
            parts.append(self._render_text(block.text))

        # Tables
        if block.tables:
            for table in block.tables:
                parts.append(self._render_table(table))

        parts.append("</div>")
        return "\n".join(parts)

    def _render_text(self, text: AttachmentText) -> str:
        """Render text block with paragraphs."""
        paragraphs = "".join(f"<p>{self._escape(p)}</p>" for p in text.paragraphs)
        return f'<div class="text-block">{paragraphs}</div>'

    def _render_table(self, table: AttachmentTable) -> str:
        """Render a table with header, rows, and optional summary."""
        parts = ['<div class="table-container">']

        # Table metadata
        if table.meta_data:
            meta_items = "".join(
                f'<span class="metadata-item"><span class="metadata-key">{self._escape(m.key)}:</span> '
                f'<span class="metadata-value">{self._escape(m.value)}</span></span>'
                for m in table.meta_data
            )
            parts.append(f'<div class="metadata">{meta_items}</div>')

        # Description
        if table.description:
            parts.append(
                f'<div class="table-description">{self._escape(table.description)}</div>'
            )

        parts.append("<table>")

        # Header
        col_types = []
        header_cells = []
        for col in table.header.columns:
            col_type = col.type
            col_types.append(col_type)
            type_label = self.COLUMN_TYPE_LABELS.get(col_type, "text")
            header_cells.append(
                f'<th>{self._escape(col.name)}<br><span class="col-type">({type_label})</span></th>'
            )
        parts.append(f"<thead><tr>{''.join(header_cells)}</tr></thead>")

        # Body
        parts.append("<tbody>")
        for row in table.rows:
            cells = []
            for i, cell in enumerate(row.cells):
                col_type = col_types[i] if i < len(col_types) else TableColumnType.TEXT
                css_class = self._get_column_css_class(col_type)
                cells.append(f'<td class="{css_class}">{self._escape(cell)}</td>')
            parts.append(f"<tr>{''.join(cells)}</tr>")

        # Summary row
        if table.summary:
            cells = []
            for i, cell in enumerate(table.summary.cells):
                col_type = col_types[i] if i < len(col_types) else TableColumnType.TEXT
                css_class = self._get_column_css_class(col_type)
                cells.append(f'<td class="{css_class}">{self._escape(cell)}</td>')
            parts.append(f'<tr class="summary-row">{"".join(cells)}</tr>')

        parts.append("</tbody></table></div>")
        return "\n".join(parts)

    def _get_column_css_class(self, col_type: TableColumnType) -> str:
        """Get CSS class for column type alignment."""
        return {
            TableColumnType.INTEGER: "col-int",
            TableColumnType.DECIMAL: "col-dec",
            TableColumnType.DATE: "col-date",
            TableColumnType.DATETIME: "col-datetime",
            TableColumnType.TIME: "col-time",
        }.get(col_type, "col-txt")

    def _escape(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )
