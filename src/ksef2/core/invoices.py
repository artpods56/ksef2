from __future__ import annotations


class InvoiceFactory:
    """Replace placeholders in invoice XML templates.

    Takes raw XML (as ``str`` or ``bytes``) and a mapping of
    ``placeholder → value``, performs the replacements, and returns
    UTF-8-encoded ``bytes`` ready for ``session.send_invoice()``.
    """

    @staticmethod
    def create(template_xml: str | bytes, replacements: dict[str, str]) -> bytes:
        """Return invoice XML bytes with *replacements* applied.

        Args:
            template_xml: Invoice XML template content.
            replacements: Mapping of placeholder strings to their values,
                e.g. ``{"#nip#": "1234567890", "#invoicing_date#": "2026-02-16"}``.

        Returns:
            UTF-8-encoded XML bytes.
        """
        text = (
            template_xml.decode("utf-8")
            if isinstance(template_xml, bytes)
            else template_xml
        )

        for placeholder, value in replacements.items():
            text = text.replace(placeholder, value)

        return text.encode("utf-8")
