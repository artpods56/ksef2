from typing import Annotated

from pydantic import Field

from ksef2.infra.schema.api.supp.base import BaseSupp


class SendInvoiceRequest(BaseSupp):
    invoiceHash: Annotated[str, Field(max_length=44, min_length=44)]
    """
    Skrót SHA256 oryginalnej faktury, zakodowany w formacie Base64.
    """
    invoiceSize: Annotated[int, Field(ge=1)]
    """
    Rozmiar oryginalnej faktury w bajtach. Maksymalny rozmiar zależy od limitów ustawionych dla uwierzytelnionego kontekstu.
    """
    encryptedInvoiceHash: Annotated[str, Field(max_length=44, min_length=44)]
    """
    Skrót SHA256 zaszyfrowanej faktury, zakodowany w formacie Base64.
    """
    encryptedInvoiceSize: Annotated[int, Field(ge=1)]
    """
    Rozmiar zaszyfrowanej faktury w bajtach.
    """
    encryptedInvoiceContent: str
    """
    Faktura zaszyfrowana algorytmem AES-256-CBC z dopełnianiem PKCS#7 (kluczem przekazanym przy otwarciu sesji), zakodowana w formacie Base64.
    """
    offlineMode: bool = False
