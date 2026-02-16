from typing import Annotated

from pydantic import AnyUrl, AwareDatetime, Field

from ksef2.infra.schema.api.spec.models import InvoiceStatusInfo, InvoicingMode
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


class SessionInvoiceStatusResponse(BaseSupp):
    ordinalNumber: Annotated[int, Field(ge=1)]
    """
    Numer sekwencyjny faktury w ramach sesji.
    """
    invoiceNumber: Annotated[str | None, Field(max_length=256)] = None
    """
    Numer faktury.
    """
    ksefNumber: Annotated[
        str | None,
        Field(
            max_length=36,
            min_length=35,
            pattern="^([1-9](\\d[1-9]|[1-9]\\d)\\d{7})-(20[2-9][0-9]|2[1-9]\\d{2}|[3-9]\\d{3})(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])-([0-9A-F]{6})-?([0-9A-F]{6})-([0-9A-F]{2})$",
        ),
    ] = None
    """
    Numer KSeF.
    """
    referenceNumber: Annotated[str, Field(max_length=36, min_length=36)]
    """
    Numer referencyjny faktury.
    """
    invoiceHash: Annotated[str, Field(max_length=44, min_length=44)]
    """
    Skrót SHA256 faktury, zakodowany w formacie Base64.
    """
    invoiceFileName: Annotated[str | None, Field(max_length=128)] = None
    """
    Nazwa pliku faktury (zwracana dla faktur wysyłanych wsadowo).
    """
    acquisitionDate: AwareDatetime | None = None
    """
    Data nadania numeru KSeF.
    """
    invoicingDate: AwareDatetime
    """
    Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
    """
    permanentStorageDate: AwareDatetime | None = None
    """
    Data trwałego zapisu faktury w repozytorium KSeF.
    """
    upoDownloadUrl: AnyUrl | None = None
    """
    Adres do pobrania UPO.
    """
    upoDownloadUrlExpirationDate: AwareDatetime | None = None
    """
    Data i godzina wygaśnięcia adresu.
    """
    invoicingMode: InvoicingMode | None = None
    """
    Tryb fakturowania (online/offline).
    """
    status: InvoiceStatusInfo
    """
    Status faktury.
    """


class SessionInvoicesResponse(BaseSupp):
    continuationToken: str | None = None
    """
    Token służący do pobrania kolejnej strony wyników. Jeśli jest pusty, to nie ma kolejnych stron.
    """
    invoices: list[SessionInvoiceStatusResponse] = []
    """
    Lista pobranych faktur.
    """
