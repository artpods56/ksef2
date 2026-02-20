from enum import Enum

from ksef2.domain.models import KSeFBaseModel


class AttachmentMetaData(KSeFBaseModel):
    """Key-value metadata for attachment data block."""

    key: str
    value: str


class AttachmentText(KSeFBaseModel):
    """Text block with paragraphs."""

    paragraphs: list[str]


class TableColumnType(str, Enum):
    """Column data type for table headers."""

    DATE = "date"
    DATETIME = "datetime"
    DECIMAL = "dec"
    INTEGER = "int"
    TIME = "time"
    TEXT = "txt"


class TableMetaData(KSeFBaseModel):
    """Key-value metadata for table."""

    key: str
    value: str


class TableHeaderColumn(KSeFBaseModel):
    """Column definition in table header."""

    name: str
    type: TableColumnType


class TableHeader(KSeFBaseModel):
    """Table header with column definitions."""

    columns: list[TableHeaderColumn]


class TableRow(KSeFBaseModel):
    """Row in a table with cell values."""

    cells: list[str]


class TableSum(KSeFBaseModel):
    """Table footer/summary row with cell values."""

    cells: list[str]


class AttachmentTable(KSeFBaseModel):
    """Table structure for attachment data block.

    Maps to FakturaZalacznikBlokDanychTabela from schema.

    Attributes:
        meta_data: Optional metadata key-value pairs for the table
        description: Optional description of the table
        header: Table header with column definitions (required)
        rows: Table data rows (at least 1 required, max 1000)
        summary: Optional summary/footer row
    """

    meta_data: list[TableMetaData] | None = None
    description: str | None = None
    header: TableHeader
    rows: list[TableRow]
    summary: TableSum | None = None


class DataBlock(KSeFBaseModel):
    """Data block for invoice attachment.

    Attributes:
        header: Optional header/title for the data block
        meta_data: Optional metadata key-value pairs
        text: Optional text content with paragraphs
        tables: Optional list of tables
    """

    header: str | None = None
    meta_data: list[AttachmentMetaData] | None = None
    text: AttachmentText | None = None
    tables: list[AttachmentTable] | None = None


class Attachment(KSeFBaseModel):
    """Invoice attachment containing data blocks."""

    data_blocks: list[DataBlock]
