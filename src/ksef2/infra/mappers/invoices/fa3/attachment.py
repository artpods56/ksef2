"""Mappers for FA3 invoice attachment schema to domain models."""

from ksef2.domain.models.fa3.attachment import (
    Attachment,
    AttachmentMetaData,
    AttachmentTable,
    AttachmentText,
    DataBlock,
    TableColumnType,
    TableHeader,
    TableHeaderColumn,
    TableMetaData,
    TableRow,
    TableSum,
)
from ksef2.infra.schema.fa3.models.schemat import (
    FakturaZalacznik,
    FakturaZalacznikBlokDanych,
    FakturaZalacznikBlokDanychMetaDane,
    FakturaZalacznikBlokDanychTabela,
    FakturaZalacznikBlokDanychTabelaSuma,
    FakturaZalacznikBlokDanychTabelaTmetaDane,
    FakturaZalacznikBlokDanychTabelaTnaglowek,
    FakturaZalacznikBlokDanychTabelaTnaglowekKol,
    FakturaZalacznikBlokDanychTabelaWiersz,
    FakturaZalacznikBlokDanychTekst,
)


class AttachmentMapper:
    """Maps FA3 schema attachment models to domain models."""

    @staticmethod
    def map_attachment(schema: FakturaZalacznik) -> Attachment:
        """Map FakturaZalacznik schema to Attachment domain model.

        Args:
            schema: The FakturaZalacznik schema model from FA3 invoice.

        Returns:
            Attachment domain model.
        """
        return Attachment(
            data_blocks=[
                AttachmentMapper.map_data_block(block) for block in schema.blok_danych
            ]
        )

    @staticmethod
    def map_data_block(schema: FakturaZalacznikBlokDanych) -> DataBlock:
        """Map FakturaZalacznikBlokDanych schema to DataBlock domain model.

        Args:
            schema: The FakturaZalacznikBlokDanych schema model.

        Returns:
            DataBlock domain model.
        """
        return DataBlock(
            header=schema.znaglowek,
            meta_data=[AttachmentMapper.map_meta_data(md) for md in schema.meta_dane]
            if schema.meta_dane
            else None,
            text=AttachmentMapper.map_text(schema.tekst) if schema.tekst else None,
            tables=[AttachmentMapper.map_table(table) for table in schema.tabela]
            if schema.tabela
            else None,
        )

    @staticmethod
    def map_meta_data(schema: FakturaZalacznikBlokDanychMetaDane) -> AttachmentMetaData:
        """Map FakturaZalacznikBlokDanychMetaDane to AttachmentMetaData.

        Args:
            schema: The metadata schema model.

        Returns:
            AttachmentMetaData domain model.
        """
        return AttachmentMetaData(
            key=schema.zklucz,
            value=schema.zwartosc,
        )

    @staticmethod
    def map_text(schema: FakturaZalacznikBlokDanychTekst) -> AttachmentText:
        """Map FakturaZalacznikBlokDanychTekst to AttachmentText.

        Args:
            schema: The text schema model.

        Returns:
            AttachmentText domain model.
        """
        return AttachmentText(
            paragraphs=list(schema.akapit),
        )

    @staticmethod
    def map_table(schema: FakturaZalacznikBlokDanychTabela) -> AttachmentTable:
        """Map FakturaZalacznikBlokDanychTabela to AttachmentTable.

        Args:
            schema: The table schema model.

        Returns:
            AttachmentTable domain model.
        """
        return AttachmentTable(
            meta_data=[
                AttachmentMapper.map_table_meta_data(md) for md in schema.tmeta_dane
            ]
            if schema.tmeta_dane
            else None,
            description=schema.opis,
            header=AttachmentMapper.map_table_header(schema.tnaglowek),
            rows=[AttachmentMapper.map_table_row(row) for row in schema.wiersz],
            summary=AttachmentMapper.map_table_sum(schema.suma)
            if schema.suma
            else None,
        )

    @staticmethod
    def map_table_meta_data(
        schema: FakturaZalacznikBlokDanychTabelaTmetaDane,
    ) -> TableMetaData:
        """Map FakturaZalacznikBlokDanychTabelaTmetaDane to TableMetaData.

        Args:
            schema: The table metadata schema model.

        Returns:
            TableMetaData domain model.
        """
        return TableMetaData(
            key=schema.tklucz,
            value=schema.twartosc,
        )

    @staticmethod
    def map_table_header(
        schema: FakturaZalacznikBlokDanychTabelaTnaglowek,
    ) -> TableHeader:
        """Map FakturaZalacznikBlokDanychTabelaTnaglowek to TableHeader.

        Args:
            schema: The table header schema model.

        Returns:
            TableHeader domain model.
        """
        return TableHeader(
            columns=[
                AttachmentMapper.map_table_header_column(col) for col in schema.kol
            ],
        )

    @staticmethod
    def map_table_header_column(
        schema: FakturaZalacznikBlokDanychTabelaTnaglowekKol,
    ) -> TableHeaderColumn:
        """Map FakturaZalacznikBlokDanychTabelaTnaglowekKol to TableHeaderColumn.

        Args:
            schema: The table header column schema model.

        Returns:
            TableHeaderColumn domain model.
        """
        return TableHeaderColumn(
            name=schema.nkom.value,
            type=TableColumnType(schema.typ.value),
        )

    @staticmethod
    def map_table_row(schema: FakturaZalacznikBlokDanychTabelaWiersz) -> TableRow:
        """Map FakturaZalacznikBlokDanychTabelaWiersz to TableRow.

        Args:
            schema: The table row schema model.

        Returns:
            TableRow domain model.
        """
        return TableRow(
            cells=list(schema.wkom),
        )

    @staticmethod
    def map_table_sum(schema: FakturaZalacznikBlokDanychTabelaSuma) -> TableSum:
        """Map FakturaZalacznikBlokDanychTabelaSuma to TableSum.

        Args:
            schema: The table sum/footer schema model.

        Returns:
            TableSum domain model.
        """
        return TableSum(
            cells=list(schema.skom),
        )
