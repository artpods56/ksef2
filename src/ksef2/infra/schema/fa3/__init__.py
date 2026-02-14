from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from xsdata.models.datatype import XmlDate, XmlDateTime  # noqa: F401


class KolTyp(Enum):
    DATE = "date"
    DATETIME = "datetime"
    DEC = "dec"
    INT = "int"
    TIME = "time"
    TXT = "txt"


class Podmiot2Gv(Enum):
    """
    :cvar VALUE_1: Tak
    :cvar VALUE_2: Nie
    """

    VALUE_1 = 1
    VALUE_2 = 2


class Podmiot2Jst(Enum):
    """
    :cvar VALUE_1: Tak
    :cvar VALUE_2: Nie
    """

    VALUE_1 = 1
    VALUE_2 = 2


class TformaPlatnosci(Enum):
    """
    Typy form płatności.

    :cvar VALUE_1: Gotówka
    :cvar VALUE_2: Karta
    :cvar VALUE_3: Bon
    :cvar VALUE_4: Czek
    :cvar VALUE_5: Kredyt
    :cvar VALUE_6: Przelew
    :cvar VALUE_7: Mobilna
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7


class Tgtu(Enum):
    """
    Oznaczenie dotyczące dostawy towarów i świadczenia usług.

    :cvar GTU_01: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. a rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_02: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. b rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_03: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. c rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_04: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. d rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_05: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. e rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_06: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. f rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_07: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. g rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_08: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. h rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_09: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. i rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_10: Dostawa towarów, o których mowa w § 10 ust. 3 pkt 1
        lit. j rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_11: Świadczenie usług, o których mowa w § 10 ust. 3 pkt 2
        lit. a rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_12: Świadczenie usług, o których mowa w § 10 ust. 3 pkt 2
        lit. b rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar GTU_13: Świadczenie usług, o których mowa w § 10 ust. 3 pkt 2
        lit. c rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    """

    GTU_01 = "GTU_01"
    GTU_02 = "GTU_02"
    GTU_03 = "GTU_03"
    GTU_04 = "GTU_04"
    GTU_05 = "GTU_05"
    GTU_06 = "GTU_06"
    GTU_07 = "GTU_07"
    GTU_08 = "GTU_08"
    GTU_09 = "GTU_09"
    GTU_10 = "GTU_10"
    GTU_11 = "GTU_11"
    GTU_12 = "GTU_12"
    GTU_13 = "GTU_13"


@dataclass(kw_only=True)
class TkluczWartosc:
    """
    Typ złożony, klucz-wartość.

    :ivar nr_wiersza: Numer wiersza podany w polu NrWierszaFa lub
        NrWierszaZam, jeśli informacja odnosi się wyłącznie do danej
        pozycji faktury
    :ivar klucz: Klucz
    :ivar wartosc: Wartość
    """

    class Meta:
        name = "TKluczWartosc"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    nr_wiersza: None | int = field(
        default=None,
        metadata={
            "name": "NrWiersza",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_exclusive": 0,
            "total_digits": 14,
            "white_space": "collapse",
        },
    )
    klucz: str = field(
        metadata={
            "name": "Klucz",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "min_length": 1,
            "max_length": 256,
        }
    )
    wartosc: str = field(
        metadata={
            "name": "Wartosc",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "min_length": 1,
            "max_length": 256,
        }
    )


class TkodFormularza(Enum):
    """
    Symbol wzoru formularza.
    """

    FA = "FA"


class TkodWaluty(Enum):
    """
    Słownik kodów walut.

    :cvar AED: DIRHAM ZEA
    :cvar AFN: AFGANI
    :cvar ALL: LEK
    :cvar AMD: DRAM
    :cvar ANG: GULDEN ANTYLI HOLENDERSKICH
    :cvar AOA: KWANZA
    :cvar ARS: PESO ARGENTYŃSKIE
    :cvar AUD: DOLAR AUSTRALIJSKI
    :cvar AWG: GULDEN ARUBAŃSKI
    :cvar AZN: MANAT AZERBEJDŻAŃSKI
    :cvar BAM: MARKA ZAMIENNA
    :cvar BBD: DOLAR BARBADOSKI
    :cvar BDT: TAKA
    :cvar BGN: LEW
    :cvar BHD: DINAR BAHRAJSKI
    :cvar BIF: FRANK BURUNDYJSKI
    :cvar BMD: DOLAR BERMUDZKI
    :cvar BND: DOLAR BRUNEJSKI
    :cvar BOB: BOLIWIANO
    :cvar BOV: BOLIWIANO MVDOL
    :cvar BRL: REAL
    :cvar BSD: DOLAR BAHAMSKI
    :cvar BTN: NGULTRUM
    :cvar BWP: PULA
    :cvar BYN: RUBEL BIAŁORUSKI
    :cvar BZD: DOLAR BELIZEŃSKI
    :cvar CAD: DOLAR KANADYJSKI
    :cvar CDF: FRANK KONGIJSKI
    :cvar CHE: FRANK SZWAJCARSKI VIR EURO
    :cvar CHF: FRANK SZWAJCARSKI
    :cvar CHW: FRANK SZWAJCARSKI VIR FRANK
    :cvar CLF: JEDNOSTKA ROZLICZENIOWA CHILIJSKA
    :cvar CLP: PESO CHILIJSKIE
    :cvar CNY: YUAN RENMINBI
    :cvar COP: PESO KOLUMBIJSKIE
    :cvar COU: UNIDAD DE VALOR REAL KOLUMBILSKIE
    :cvar CRC: COLON KOSTARYKAŃSKI
    :cvar CUC: PESO WYMIENIALNE
    :cvar CUP: PESO KUBAŃSKIE
    :cvar CVE: ESCUDO REPUBLIKI ZIELONEGO PRZYLĄDKA
    :cvar CZK: KORONA CZESKA
    :cvar DJF: FRANK DŻIBUTI
    :cvar DKK: KORONA DUŃSKA
    :cvar DOP: PESO DOMINIKAŃSKIE
    :cvar DZD: DINAR ALGIERSKI
    :cvar EGP: FUNT EGIPSKI
    :cvar ERN: NAKFA
    :cvar ETB: BIRR
    :cvar EUR: EURO
    :cvar FJD: DOLAR FIDŻI
    :cvar FKP: FUNT FALKLANDZKI
    :cvar GBP: FUNT SZTERLING
    :cvar GEL: LARI
    :cvar GGP: FUNT GUERNSEY
    :cvar GHS: GHANA CEDI
    :cvar GIP: FUNT GIBRALTARSKI
    :cvar GMD: DALASI
    :cvar GNF: FRANK GWINEJSKI
    :cvar GTQ: QUETZAL
    :cvar GYD: DOLAR GUJAŃSKI
    :cvar HKD: DOLAR HONGKONGU
    :cvar HNL: LEMPIRA
    :cvar HRK: KUNA
    :cvar HTG: GOURDE
    :cvar HUF: FORINT
    :cvar IDR: RUPIA INDONEZYJSKA
    :cvar ILS: SZEKEL
    :cvar IMP: FUNT MANX
    :cvar INR: RUPIA INDYJSKA
    :cvar IQD: DINAR IRACKI
    :cvar IRR: RIAL IRAŃSKI
    :cvar ISK: KORONA ISLANDZKA
    :cvar JEP: FUNT JERSEY
    :cvar JMD: DOLAR JAMAJSKI
    :cvar JOD: DINAR JORDAŃSKI
    :cvar JPY: JEN
    :cvar KES: SZYLING KENIJSKI
    :cvar KGS: SOM
    :cvar KHR: RIEL
    :cvar KMF: FRANK KOMORÓW
    :cvar KPW: WON PÓŁNOCNO­KOREAŃSKI
    :cvar KRW: WON POŁUDNIOWO­KOREAŃSKI
    :cvar KWD: DINAR KUWEJCKI
    :cvar KYD: DOLAR KAJMAŃSKI
    :cvar KZT: TENGE
    :cvar LAK: KIP
    :cvar LBP: FUNT LIBAŃSKI
    :cvar LKR: RUPIA LANKIJSKA
    :cvar LRD: DOLAR LIBERYJSKI
    :cvar LSL: LOTI
    :cvar LYD: DINAR LIBIJSKI
    :cvar MAD: DIRHAM MAROKAŃSKI
    :cvar MDL: LEJ MOŁDAWII
    :cvar MGA: ARIARY
    :cvar MKD: DENAR
    :cvar MMK: KYAT
    :cvar MNT: TUGRIK
    :cvar MOP: PATACA
    :cvar MRU: OUGUIYA
    :cvar MUR: RUPIA MAURITIUSU
    :cvar MVR: RUPIA MALEDIWSKA
    :cvar MWK: KWACHA MALAWIJSKA
    :cvar MXN: PESO MEKSYKAŃSKIE
    :cvar MXV: UNIDAD DE INVERSION (UDI) MEKSYKAŃSKIE
    :cvar MYR: RINGGIT
    :cvar MZN: METICAL
    :cvar NAD: DOLAR NAMIBIJSKI
    :cvar NGN: NAIRA
    :cvar NIO: CORDOBA ORO
    :cvar NOK: KORONA NORWESKA
    :cvar NPR: RUPIA NEPALSKA
    :cvar NZD: DOLAR NOWOZELANDZKI
    :cvar OMR: RIAL OMAŃSKI
    :cvar PAB: BALBOA
    :cvar PEN: SOL
    :cvar PGK: KINA
    :cvar PHP: PESO FILIPIŃSKIE
    :cvar PKR: RUPIA PAKISTAŃSKA
    :cvar PLN: ZŁOTY
    :cvar PYG: GUARANI
    :cvar QAR: RIAL KATARSKI
    :cvar RON: LEJ RUMUŃSKI
    :cvar RSD: DINAR SERBSKI
    :cvar RUB: RUBEL ROSYJSKI
    :cvar RWF: FRANK RWANDYJSKI
    :cvar SAR: RIAL SAUDYJSKI
    :cvar SBD: DOLAR WYSP SALOMONA
    :cvar SCR: RUPIA SESZELSKA
    :cvar SDG: FUNT SUDAŃSKI
    :cvar SEK: KORONA SZWEDZKA
    :cvar SGD: DOLAR SINGAPURSKI
    :cvar SHP: FUNT ŚWIĘTEJ HELENY (ŚWIĘTA HELENA I WYSPA
        WNIEBOWSTĄPIENIA)
    :cvar SLL: LEONE
    :cvar SOS: SZYLING SOMALIJSKI
    :cvar SRD: DOLAR SURINAMSKI
    :cvar SSP: FUNT POŁUDNIOWOSUDAŃSKI
    :cvar STN: DOBRA
    :cvar SVC: COLON SALWADORSKI (SV1)
    :cvar SYP: FUNT SYRYJSKI
    :cvar SZL: LILANGENI
    :cvar THB: BAT
    :cvar TJS: SOMONI
    :cvar TMT: MANAT TURKMEŃSKI
    :cvar TND: DINAR TUNEZYJSKI
    :cvar TOP: PAANGA
    :cvar TRY: LIRA TURECKA
    :cvar TTD: DOLAR TRYNIDADU I TOBAGO
    :cvar TWD: NOWY DOLAR TAJWAŃSKI
    :cvar TZS: SZYLING TANZAŃSKI
    :cvar UAH: HRYWNA
    :cvar UGX: SZYLING UGANDYJSKI
    :cvar USD: DOLAR AMERYKAŃSKI
    :cvar USN: DOLAR AMERYKAŃSKI (NEXT DAY)
    :cvar UYI: PESO EN UNIDADES INDEXADAS URUGWAJSKIE
    :cvar UYU: PESO URUGWAJSKIE
    :cvar UYW: PESO EN UNIDADES INDEXADAS URUGWAJSKIE
    :cvar UZS: SUM
    :cvar VES: BOLIWAR SOBERANO
    :cvar VND: DONG
    :cvar VUV: VATU
    :cvar WST: TALA
    :cvar XAF: FRANK CFA (BEAC)
    :cvar XAG: SREBRO
    :cvar XAU: ZŁOTO
    :cvar XBA: BOND MARKETS UNIT EUROPEAN COMPOSITE UNIT (EURCO)
    :cvar XBB: BOND MARKETS UNIT EUROPEAN MONETARY UNIT (E.M.U.-6)
    :cvar XBC: BOND MARKETS UNIT EUROPEAN UNIT OF ACCOUNT 9 (E.U.A.-9)
    :cvar XBD: BOND MARKETS UNIT EUROPEAN UNIT OF ACCOUNT 17 (E.U.A.-17)
    :cvar XCD: DOLAR WSCHODNIO­KARAIBSKI
    :cvar XCG: GULDEN KARAIBSKI
    :cvar XDR: SDR MIĘDZYNARODOWY FUNDUSZ WALUTOWY
    :cvar XOF: FRANK CFA (BCEAO)
    :cvar XPD: PALLAD
    :cvar XPF: FRANK CFP
    :cvar XPT: PLATYNA
    :cvar XSU: SUCRE SISTEMA UNITARIO DE COMPENSACION REGIONAL DE PAGOS
        SUCRE
    :cvar XUA: ADB UNIT OF ACCOUNT MEMBER COUNTRIES OF THE AFRICAN
        DEVELOPMENT BANK GROUP
    :cvar XXX: BRAK WALUTY
    :cvar YER: RIAL JEMEŃSKI
    :cvar ZAR: RAND
    :cvar ZMW: KWACHA ZAMBIJSKA
    :cvar ZWL: DOLAR ZIMBABWE
    """

    AED = "AED"
    AFN = "AFN"
    ALL = "ALL"
    AMD = "AMD"
    ANG = "ANG"
    AOA = "AOA"
    ARS = "ARS"
    AUD = "AUD"
    AWG = "AWG"
    AZN = "AZN"
    BAM = "BAM"
    BBD = "BBD"
    BDT = "BDT"
    BGN = "BGN"
    BHD = "BHD"
    BIF = "BIF"
    BMD = "BMD"
    BND = "BND"
    BOB = "BOB"
    BOV = "BOV"
    BRL = "BRL"
    BSD = "BSD"
    BTN = "BTN"
    BWP = "BWP"
    BYN = "BYN"
    BZD = "BZD"
    CAD = "CAD"
    CDF = "CDF"
    CHE = "CHE"
    CHF = "CHF"
    CHW = "CHW"
    CLF = "CLF"
    CLP = "CLP"
    CNY = "CNY"
    COP = "COP"
    COU = "COU"
    CRC = "CRC"
    CUC = "CUC"
    CUP = "CUP"
    CVE = "CVE"
    CZK = "CZK"
    DJF = "DJF"
    DKK = "DKK"
    DOP = "DOP"
    DZD = "DZD"
    EGP = "EGP"
    ERN = "ERN"
    ETB = "ETB"
    EUR = "EUR"
    FJD = "FJD"
    FKP = "FKP"
    GBP = "GBP"
    GEL = "GEL"
    GGP = "GGP"
    GHS = "GHS"
    GIP = "GIP"
    GMD = "GMD"
    GNF = "GNF"
    GTQ = "GTQ"
    GYD = "GYD"
    HKD = "HKD"
    HNL = "HNL"
    HRK = "HRK"
    HTG = "HTG"
    HUF = "HUF"
    IDR = "IDR"
    ILS = "ILS"
    IMP = "IMP"
    INR = "INR"
    IQD = "IQD"
    IRR = "IRR"
    ISK = "ISK"
    JEP = "JEP"
    JMD = "JMD"
    JOD = "JOD"
    JPY = "JPY"
    KES = "KES"
    KGS = "KGS"
    KHR = "KHR"
    KMF = "KMF"
    KPW = "KPW"
    KRW = "KRW"
    KWD = "KWD"
    KYD = "KYD"
    KZT = "KZT"
    LAK = "LAK"
    LBP = "LBP"
    LKR = "LKR"
    LRD = "LRD"
    LSL = "LSL"
    LYD = "LYD"
    MAD = "MAD"
    MDL = "MDL"
    MGA = "MGA"
    MKD = "MKD"
    MMK = "MMK"
    MNT = "MNT"
    MOP = "MOP"
    MRU = "MRU"
    MUR = "MUR"
    MVR = "MVR"
    MWK = "MWK"
    MXN = "MXN"
    MXV = "MXV"
    MYR = "MYR"
    MZN = "MZN"
    NAD = "NAD"
    NGN = "NGN"
    NIO = "NIO"
    NOK = "NOK"
    NPR = "NPR"
    NZD = "NZD"
    OMR = "OMR"
    PAB = "PAB"
    PEN = "PEN"
    PGK = "PGK"
    PHP = "PHP"
    PKR = "PKR"
    PLN = "PLN"
    PYG = "PYG"
    QAR = "QAR"
    RON = "RON"
    RSD = "RSD"
    RUB = "RUB"
    RWF = "RWF"
    SAR = "SAR"
    SBD = "SBD"
    SCR = "SCR"
    SDG = "SDG"
    SEK = "SEK"
    SGD = "SGD"
    SHP = "SHP"
    SLL = "SLL"
    SOS = "SOS"
    SRD = "SRD"
    SSP = "SSP"
    STN = "STN"
    SVC = "SVC"
    SYP = "SYP"
    SZL = "SZL"
    THB = "THB"
    TJS = "TJS"
    TMT = "TMT"
    TND = "TND"
    TOP = "TOP"
    TRY = "TRY"
    TTD = "TTD"
    TWD = "TWD"
    TZS = "TZS"
    UAH = "UAH"
    UGX = "UGX"
    USD = "USD"
    USN = "USN"
    UYI = "UYI"
    UYU = "UYU"
    UYW = "UYW"
    UZS = "UZS"
    VES = "VES"
    VND = "VND"
    VUV = "VUV"
    WST = "WST"
    XAF = "XAF"
    XAG = "XAG"
    XAU = "XAU"
    XBA = "XBA"
    XBB = "XBB"
    XBC = "XBC"
    XBD = "XBD"
    XCD = "XCD"
    XCG = "XCG"
    XDR = "XDR"
    XOF = "XOF"
    XPD = "XPD"
    XPF = "XPF"
    XPT = "XPT"
    XSU = "XSU"
    XUA = "XUA"
    XXX = "XXX"
    YER = "YER"
    ZAR = "ZAR"
    ZMW = "ZMW"
    ZWL = "ZWL"


class TkodyKrajowUe(Enum):
    """
    Kody krajów członkowskich Unii Europejskiej, w tym kod dla obszaru
    Irlandii Północnej.

    :cvar AT: AUSTRIA
    :cvar BE: BELGIA
    :cvar BG: BUŁGARIA
    :cvar CY: CYPR
    :cvar CZ: CZECHY
    :cvar DK: DANIA
    :cvar EE: ESTONIA
    :cvar FI: FINLANDIA
    :cvar FR: FRANCJA
    :cvar DE: NIEMCY
    :cvar EL: GRECJA
    :cvar HR: CHORWACJA
    :cvar HU: WĘGRY
    :cvar IE: IRLANDIA
    :cvar IT: WŁOCHY
    :cvar LV: ŁOTWA
    :cvar LT: LITWA
    :cvar LU: LUKSEMBURG
    :cvar MT: MALTA
    :cvar NL: HOLANDIA
    :cvar PL: POLSKA
    :cvar PT: PORTUGALIA
    :cvar RO: RUMUNIA
    :cvar SK: SŁOWACJA
    :cvar SI: SŁOWENIA
    :cvar ES: HISZPANIA
    :cvar SE: SZWECJA
    :cvar XI: IRLANDIA PÓŁNOCNA
    """

    AT = "AT"
    BE = "BE"
    BG = "BG"
    CY = "CY"
    CZ = "CZ"
    DK = "DK"
    EE = "EE"
    FI = "FI"
    FR = "FR"
    DE = "DE"
    EL = "EL"
    HR = "HR"
    HU = "HU"
    IE = "IE"
    IT = "IT"
    LV = "LV"
    LT = "LT"
    LU = "LU"
    MT = "MT"
    NL = "NL"
    PL = "PL"
    PT = "PT"
    RO = "RO"
    SK = "SK"
    SI = "SI"
    ES = "ES"
    SE = "SE"
    XI = "XI"


class Tladunek(Enum):
    """
    Typy ładunków.

    :cvar VALUE_1: Bańka
    :cvar VALUE_2: Beczka
    :cvar VALUE_3: Butla
    :cvar VALUE_4: Karton
    :cvar VALUE_5: Kanister
    :cvar VALUE_6: Klatka
    :cvar VALUE_7: Kontener
    :cvar VALUE_8: Kosz/koszyk
    :cvar VALUE_9: Łubianka
    :cvar VALUE_10: Opakowanie zbiorcze
    :cvar VALUE_11: Paczka
    :cvar VALUE_12: Pakiet
    :cvar VALUE_13: Paleta
    :cvar VALUE_14: Pojemnik
    :cvar VALUE_15: Pojemnik do ładunków masowych stałych
    :cvar VALUE_16: Pojemnik do ładunków masowych w postaci płynnej
    :cvar VALUE_17: Pudełko
    :cvar VALUE_18: Puszka
    :cvar VALUE_19: Skrzynia
    :cvar VALUE_20: Worek
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7
    VALUE_8 = 8
    VALUE_9 = 9
    VALUE_10 = 10
    VALUE_11 = 11
    VALUE_12 = 12
    VALUE_13 = 13
    VALUE_14 = 14
    VALUE_15 = 15
    VALUE_16 = 16
    VALUE_17 = 17
    VALUE_18 = 18
    VALUE_19 = 19
    VALUE_20 = 20


class TnaglowekWariantFormularza(Enum):
    VALUE_3 = 3


class ToznaczenieProcedury(Enum):
    """
    Oznaczenia dotyczące procedur dla faktur.

    :cvar WSTO_EE: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 2a rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar IED: Oznaczenie dotyczące procedury, o której mowa w § 10 ust.
        4 pkt 2b rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar TT_D: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 5 rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar I_42: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 8 rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar I_63: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 9 rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar B_SPV: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 10 rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar B_SPV_DOSTAWA: Oznaczenie dotyczące procedury, o której mowa w
        § 10 ust. 4 pkt 11 rozporządzenia w sprawie szczegółowego
        zakresu danych zawartych w deklaracjach podatkowych i w
        ewidencji w zakresie podatku od towarów i usług
    :cvar B_MPV_PROWIZJA: Oznaczenie dotyczące procedury, o której mowa
        w § 10 ust. 4 pkt 12 rozporządzenia w sprawie szczegółowego
        zakresu danych zawartych w deklaracjach podatkowych i w
        ewidencji w zakresie podatku od towarów i usług
    """

    WSTO_EE = "WSTO_EE"
    IED = "IED"
    TT_D = "TT_D"
    I_42 = "I_42"
    I_63 = "I_63"
    B_SPV = "B_SPV"
    B_SPV_DOSTAWA = "B_SPV_DOSTAWA"
    B_MPV_PROWIZJA = "B_MPV_PROWIZJA"


class ToznaczenieProceduryZ(Enum):
    """
    Oznaczenia dotyczące procedur dla zamówień.

    :cvar WSTO_EE: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 2a rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar IED: Oznaczenie dotyczące procedury, o której mowa w § 10 ust.
        4 pkt 2b rozporządzenia w sprawie szczegółowego zakresu danych
        zawartych w deklaracjach podatkowych i w ewidencji w zakresie
        podatku od towarów i usług
    :cvar TT_D: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 5 rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar B_SPV: Oznaczenie dotyczące procedury, o której mowa w § 10
        ust. 4 pkt 10 rozporządzenia w sprawie szczegółowego zakresu
        danych zawartych w deklaracjach podatkowych i w ewidencji w
        zakresie podatku od towarów i usług
    :cvar B_SPV_DOSTAWA: Oznaczenie dotyczące procedury, o której mowa w
        § 10 ust. 4 pkt 11 rozporządzenia w sprawie szczegółowego
        zakresu danych zawartych w deklaracjach podatkowych i w
        ewidencji w zakresie podatku od towarów i usług
    :cvar B_MPV_PROWIZJA: Oznaczenie dotyczące procedury, o której mowa
        w § 10 ust. 4 pkt 12 rozporządzenia w sprawie szczegółowego
        zakresu danych zawartych w deklaracjach podatkowych i w
        ewidencji w zakresie podatku od towarów i usług
    """

    WSTO_EE = "WSTO_EE"
    IED = "IED"
    TT_D = "TT_D"
    B_SPV = "B_SPV"
    B_SPV_DOSTAWA = "B_SPV_DOSTAWA"
    B_MPV_PROWIZJA = "B_MPV_PROWIZJA"


@dataclass(kw_only=True)
class Tpodmiot1:
    """
    Zestaw danych identyfikacyjnych oraz danych adresowych podatnika.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar nazwa: Imię i nazwisko lub nazwa
    """

    class Meta:
        name = "TPodmiot1"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    nip: str = field(
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        }
    )
    nazwa: str = field(
        metadata={
            "name": "Nazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "min_length": 1,
            "max_length": 512,
        }
    )


class TrachunekWlasnyBanku(Enum):
    """
    Typy rachunków własnych.

    :cvar VALUE_1: Rachunek banku lub rachunek spółdzielczej kasy
        oszczędnościowo-kredytowej służący do dokonywania rozliczeń z
        tytułu nabywanych przez ten bank lub tę kasę wierzytelności
        pieniężnych
    :cvar VALUE_2: Rachunek banku lub rachunek spółdzielczej kasy
        oszczędnościowo-kredytowej wykorzystywany przez ten bank lub tę
        kasę do pobrania należności od nabywcy towarów lub usług za
        dostawę towarów lub świadczenie usług, potwierdzone fakturą, i
        przekazania jej w całości albo części dostawcy towarów lub
        usługodawcy
    :cvar VALUE_3: Rachunek banku lub rachunek spółdzielczej kasy
        oszczędnościowo-kredytowej prowadzony przez ten bank lub tę kasę
        w ramach gospodarki własnej, niebędący rachunkiem rozliczeniowym
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


class TrodzajFaktury(Enum):
    """
    Rodzaj faktury.

    :cvar VAT: Faktura podstawowa
    :cvar KOR: Faktura korygująca
    :cvar ZAL: Faktura dokumentująca otrzymanie zapłaty lub jej części
        przed dokonaniem czynności oraz faktura wystawiona w związku z
        art. 106f ust. 4 ustawy (faktura zaliczkowa)
    :cvar ROZ: Faktura wystawiona w związku z art. 106f ust. 3 ustawy
    :cvar UPR: Faktura, o której mowa w art. 106e ust. 5 pkt 3 ustawy
    :cvar KOR_ZAL: Faktura korygująca fakturę dokumentującą otrzymanie
        zapłaty lub jej części przed dokonaniem czynności oraz fakturę
        wystawioną w związku z art. 106f ust. 4 ustawy (faktura
        korygująca fakturę zaliczkową)
    :cvar KOR_ROZ: Faktura korygująca fakturę wystawioną w związku z
        art. 106f ust. 3 ustawy
    """

    VAT = "VAT"
    KOR = "KOR"
    ZAL = "ZAL"
    ROZ = "ROZ"
    UPR = "UPR"
    KOR_ZAL = "KOR_ZAL"
    KOR_ROZ = "KOR_ROZ"


class TrodzajTransportu(Enum):
    """
    Rodzaj transportu.

    :cvar VALUE_1: Transport morski
    :cvar VALUE_2: Transport kolejowy
    :cvar VALUE_3: Transport drogowy
    :cvar VALUE_4: Transport lotniczy
    :cvar VALUE_5: Przesyłka pocztowa
    :cvar VALUE_7: Stałe instalacje przesyłowe
    :cvar VALUE_8: Żegluga śródlądowa
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_7 = 7
    VALUE_8 = 8


class TrolaPodmiotu3(Enum):
    """
    Rola podmiotu trzeciego.

    :cvar VALUE_1: Faktor - w przypadku gdy na fakturze występują dane
        faktora
    :cvar VALUE_2: Odbiorca - w przypadku gdy na fakturze występują dane
        jednostek wewnętrznych, oddziałów, wyodrębnionych w ramach
        nabywcy, które same nie stanowią nabywcy w rozumieniu ustawy
    :cvar VALUE_3: Podmiot pierwotny - w przypadku gdy na fakturze
        występują dane podmiotu będącego w stosunku do podatnika
        podmiotem przejętym lub przekształconym, który dokonywał dostawy
        lub świadczył usługę. Z wyłączeniem przypadków, o których mowa w
        art. 106j ust.2 pkt 3 ustawy, gdy dane te wykazywane są w części
        Podmiot1K
    :cvar VALUE_4: Dodatkowy nabywca - w przypadku gdy na fakturze
        występują dane kolejnych (innych niż wymieniony w części
        Podmiot2) nabywców
    :cvar VALUE_5: Wystawca faktury - w przypadku gdy na fakturze
        występują dane podmiotu wystawiającego fakturę w imieniu
        podatnika. Nie dotyczy przypadku, gdy wystawcą faktury jest
        nabywca
    :cvar VALUE_6: Dokonujący płatności - w przypadku gdy na fakturze
        występują dane podmiotu regulującego zobowiązanie w miejsce
        nabywcy
    :cvar VALUE_7: Jednostka samorządu terytorialnego - wystawca
    :cvar VALUE_8: Jednostka samorządu terytorialnego - odbiorca
    :cvar VALUE_9: Członek grupy VAT - wystawca
    :cvar VALUE_10: Członek grupy VAT - odbiorca
    :cvar VALUE_11: Pracownik
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7
    VALUE_8 = 8
    VALUE_9 = 9
    VALUE_10 = 10
    VALUE_11 = 11


class TrolaPodmiotuUpowaznionego(Enum):
    """
    Rola podmiotu upoważnionego.

    :cvar VALUE_1: Organ egzekucyjny - w przypadku, o którym mowa w art.
        106c pkt 1 ustawy
    :cvar VALUE_2: Komornik sądowy - w przypadku, o którym mowa w art.
        106c pkt 2 ustawy
    :cvar VALUE_3: Przedstawiciel podatkowy - w przypadku gdy na
        fakturze występują dane przedstawiciela podatkowego, o którym
        mowa w art. 18a - 18d ustawy
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


class TstatusInfoPodatnika(Enum):
    """
    Status podatnika.

    :cvar VALUE_1: Podatnik znajdujący się w stanie likwidacji
    :cvar VALUE_2: Podatnik, który jest w trakcie postępowania
        restrukturyzacyjnego
    :cvar VALUE_3: Podatnik znajdujący się w stanie upadłości
    :cvar VALUE_4: Przedsiębiorstwo w spadku
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4


class TstawkaPodatku(Enum):
    """
    Stawka podatku.

    :cvar VALUE_23:
    :cvar VALUE_22:
    :cvar VALUE_8:
    :cvar VALUE_7:
    :cvar VALUE_5:
    :cvar VALUE_4:
    :cvar VALUE_3:
    :cvar VALUE_0_KR: Stawka 0% w przypadku sprzedaży towarów i
        świadczenia usług na terytorium kraju (z wyłączeniem WDT i
        eksportu)
    :cvar VALUE_0_WDT: Stawka 0% w przypadku wewnątrzwspólnotowej
        dostawy towarów (WDT)
    :cvar VALUE_0_EX: Stawka 0% w przypadku eksportu towarów
    :cvar ZW: zwolnione od podatku
    :cvar OO: odwrotne obciążenie
    :cvar NP_I: niepodlegające opodatkowaniu- dostawy towarów oraz
        świadczenia usług poza terytorium kraju, z wyłączeniem
        transakcji, o których mowa w art. 100 ust. 1 pkt 4 ustawy oraz
        OSS
    :cvar NP_II: niepodlegajace opodatkowaniu na terytorium kraju,
        świadczenie usług o których mowa w art. 100 ust. 1 pkt 4 ustawy
    """

    VALUE_23 = "23"
    VALUE_22 = "22"
    VALUE_8 = "8"
    VALUE_7 = "7"
    VALUE_5 = "5"
    VALUE_4 = "4"
    VALUE_3 = "3"
    VALUE_0_KR = "0 KR"
    VALUE_0_WDT = "0 WDT"
    VALUE_0_EX = "0 EX"
    ZW = "zw"
    OO = "oo"
    NP_I = "np I"
    NP_II = "np II"


class TtypKorekty(Enum):
    """
    Typ skutku korekty w ewidencji dla podatku od towarów i usług.

    :cvar VALUE_1: Korekta skutkująca w dacie ujęcia faktury pierwotnej
    :cvar VALUE_2: Korekta skutkująca w dacie wystawienia faktury
        korygującej
    :cvar VALUE_3: Korekta skutkująca w dacie innej, w tym gdy dla
        różnych pozycji faktury korygującej daty te są różne
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


@dataclass(kw_only=True)
class TidentyfikatorOsobyFizycznej:
    """
    Podstawowy zestaw danych identyfikacyjnych o osobie fizycznej.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar imie_pierwsze: Pierwsze imię
    :ivar nazwisko: Nazwisko
    :ivar data_urodzenia: Data urodzenia
    :ivar pesel: Identyfikator podatkowy numer PESEL
    """

    class Meta:
        name = "TIdentyfikatorOsobyFizycznej"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: str = field(
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        }
    )
    imie_pierwsze: str = field(
        metadata={
            "name": "ImiePierwsze",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    nazwisko: str = field(
        metadata={
            "name": "Nazwisko",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 81,
        }
    )
    data_urodzenia: str = field(
        metadata={
            "name": "DataUrodzenia",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_inclusive": "1900-01-01",
            "max_inclusive": "2050-12-31",
            "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
        }
    )
    pesel: None | str = field(
        default=None,
        metadata={
            "name": "PESEL",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"\d{11}",
        },
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyFizycznej1:
    """
    Podstawowy zestaw danych identyfikacyjnych o osobie fizycznej z
    identyfikatorem NIP albo PESEL.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar pesel: Identyfikator podatkowy numer PESEL
    :ivar imie_pierwsze: Pierwsze imię
    :ivar nazwisko: Nazwisko
    :ivar data_urodzenia: Data urodzenia
    """

    class Meta:
        name = "TIdentyfikatorOsobyFizycznej1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )
    pesel: None | str = field(
        default=None,
        metadata={
            "name": "PESEL",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"\d{11}",
        },
    )
    imie_pierwsze: str = field(
        metadata={
            "name": "ImiePierwsze",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    nazwisko: str = field(
        metadata={
            "name": "Nazwisko",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 81,
        }
    )
    data_urodzenia: str = field(
        metadata={
            "name": "DataUrodzenia",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_inclusive": "1900-01-01",
            "max_inclusive": "2050-12-31",
            "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
        }
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyFizycznej2:
    """
    Podstawowy zestaw danych identyfikacyjnych o osobie fizycznej z
    identyfikatorem NIP.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar imie_pierwsze: Pierwsze imię
    :ivar nazwisko: Nazwisko
    :ivar data_urodzenia: Data urodzenia
    """

    class Meta:
        name = "TIdentyfikatorOsobyFizycznej2"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: str = field(
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        }
    )
    imie_pierwsze: str = field(
        metadata={
            "name": "ImiePierwsze",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    nazwisko: str = field(
        metadata={
            "name": "Nazwisko",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 81,
        }
    )
    data_urodzenia: str = field(
        metadata={
            "name": "DataUrodzenia",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_inclusive": "1900-01-01",
            "max_inclusive": "2050-12-31",
            "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
        }
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyFizycznejPelny:
    """
    Pełny zestaw danych identyfikacyjnych o osobie fizycznej.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar imie_pierwsze: Pierwsze imię
    :ivar nazwisko: Nazwisko
    :ivar data_urodzenia: Data urodzenia
    :ivar imie_ojca: Imię ojca
    :ivar imie_matki: Imię matki
    :ivar pesel: Identyfikator podatkowy numer PESEL
    """

    class Meta:
        name = "TIdentyfikatorOsobyFizycznejPelny"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )
    imie_pierwsze: str = field(
        metadata={
            "name": "ImiePierwsze",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    nazwisko: str = field(
        metadata={
            "name": "Nazwisko",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 81,
        }
    )
    data_urodzenia: str = field(
        metadata={
            "name": "DataUrodzenia",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_inclusive": "1900-01-01",
            "max_inclusive": "2050-12-31",
            "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
        }
    )
    imie_ojca: str = field(
        metadata={
            "name": "ImieOjca",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    imie_matki: str = field(
        metadata={
            "name": "ImieMatki",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    pesel: str = field(
        metadata={
            "name": "PESEL",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"\d{11}",
        }
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyFizycznejZagranicznej:
    """
    Zestaw danych identyfikacyjnych dla osoby fizycznej zagranicznej.

    :ivar imie_pierwsze: Imię pierwsze [First name]
    :ivar nazwisko: Nazwisko [Family name]
    :ivar data_urodzenia: Data urodzenia [Date of Birth]
    :ivar miejsce_urodzenia: Miejsce urodzenia [Place of Birth]
    :ivar imie_ojca: Imię ojca [Father’s name]
    :ivar imie_matki: Imię matki [Mother’s name]
    :ivar nip: Identyfikator podatkowy NIP [Tax Identification Number
        (NIP)]
    """

    class Meta:
        name = "TIdentyfikatorOsobyFizycznejZagranicznej"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    imie_pierwsze: str = field(
        metadata={
            "name": "ImiePierwsze",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 30,
        }
    )
    nazwisko: str = field(
        metadata={
            "name": "Nazwisko",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 81,
        }
    )
    data_urodzenia: str = field(
        metadata={
            "name": "DataUrodzenia",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_inclusive": "1900-01-01",
            "max_inclusive": "2050-12-31",
            "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
        }
    )
    miejsce_urodzenia: str = field(
        metadata={
            "name": "MiejsceUrodzenia",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 56,
        }
    )
    imie_ojca: None | str = field(
        default=None,
        metadata={
            "name": "ImieOjca",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 30,
        },
    )
    imie_matki: None | str = field(
        default=None,
        metadata={
            "name": "ImieMatki",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 30,
        },
    )
    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyNiefizycznej:
    """
    Podstawowy zestaw danych identyfikacyjnych o osobie niefizycznej.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar pelna_nazwa: Pełna nazwa
    :ivar regon: Numer REGON
    """

    class Meta:
        name = "TIdentyfikatorOsobyNiefizycznej"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: str = field(
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        }
    )
    pelna_nazwa: str = field(
        metadata={
            "name": "PelnaNazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 240,
        }
    )
    regon: None | str = field(
        default=None,
        metadata={
            "name": "REGON",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"\d{14}",
        },
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyNiefizycznej1:
    """
    Podstawowy zestaw danych identyfikacyjnych o osobie niefizycznej - bez
    elementu Numer REGON.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar pelna_nazwa: Pełna nazwa
    """

    class Meta:
        name = "TIdentyfikatorOsobyNiefizycznej1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: str = field(
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        }
    )
    pelna_nazwa: str = field(
        metadata={
            "name": "PelnaNazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 240,
        }
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyNiefizycznejPelny:
    """
    Pełny zestaw danych identyfikacyjnych o osobie niefizycznej.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar pelna_nazwa: Pełna nazwa
    :ivar skrocona_nazwa: Skrócona nazwa
    :ivar regon: Numer REGON
    """

    class Meta:
        name = "TIdentyfikatorOsobyNiefizycznejPelny"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )
    pelna_nazwa: str = field(
        metadata={
            "name": "PelnaNazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 240,
        }
    )
    skrocona_nazwa: str = field(
        metadata={
            "name": "SkroconaNazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 70,
        }
    )
    regon: str = field(
        metadata={
            "name": "REGON",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"\d{14}",
        }
    )


@dataclass(kw_only=True)
class TidentyfikatorOsobyNiefizycznejZagranicznej:
    """
    Zestaw danych identyfikacyjnych dla osoby niefizycznej zagranicznej.

    :ivar pelna_nazwa: Pełna nazwa [Name]
    :ivar skrocona_nazwa: Nazwa skrócona [Short Name]
    :ivar nip: Identyfikator podatkowy NIP [Tax Identification Number
        (NIP)]
    """

    class Meta:
        name = "TIdentyfikatorOsobyNiefizycznejZagranicznej"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    pelna_nazwa: str = field(
        metadata={
            "name": "PelnaNazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 240,
        }
    )
    skrocona_nazwa: None | str = field(
        default=None,
        metadata={
            "name": "SkroconaNazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 70,
        },
    )
    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )


class TkodKraju(Enum):
    """
    Słownik kodów krajów.

    :cvar AF: AFGANISTAN
    :cvar AX: ALAND ISLANDS
    :cvar AL: ALBANIA
    :cvar DZ: ALGIERIA
    :cvar AD: ANDORA
    :cvar AO: ANGOLA
    :cvar AI: ANGUILLA
    :cvar AQ: ANTARKTYDA
    :cvar AG: ANTIGUA I BARBUDA
    :cvar AN: ANTYLE HOLENDERSKIE
    :cvar SA: ARABIA SAUDYJSKA
    :cvar AR: ARGENTYNA
    :cvar AM: ARMENIA
    :cvar AW: ARUBA
    :cvar AU: AUSTRALIA
    :cvar AT: AUSTRIA
    :cvar AZ: AZERBEJDŻAN
    :cvar BS: BAHAMY
    :cvar BH: BAHRAJN
    :cvar BD: BANGLADESZ
    :cvar BB: BARBADOS
    :cvar BE: BELGIA
    :cvar BZ: BELIZE
    :cvar BJ: BENIN
    :cvar BM: BERMUDY
    :cvar BT: BHUTAN
    :cvar BY: BIAŁORUŚ
    :cvar BO: BOLIWIA
    :cvar BQ: BONAIRE, SINT EUSTATIUS I SABA
    :cvar BA: BOŚNIA I HERCEGOWINA
    :cvar BW: BOTSWANA
    :cvar BR: BRAZYLIA
    :cvar BN: BRUNEI DARUSSALAM
    :cvar IO: BRYTYJSKIE TERYTORIUM OCEANU INDYJSKIEGO
    :cvar BG: BUŁGARIA
    :cvar BF: BURKINA FASO
    :cvar BI: BURUNDI
    :cvar XC: CEUTA
    :cvar CL: CHILE
    :cvar CN: CHINY
    :cvar HR: CHORWACJA
    :cvar CW: CURAÇAO
    :cvar CY: CYPR
    :cvar TD: CZAD
    :cvar ME: CZARNOGÓRA
    :cvar DK: DANIA
    :cvar DM: DOMINIKA
    :cvar DO: DOMINIKANA
    :cvar DJ: DŻIBUTI
    :cvar EG: EGIPT
    :cvar EC: EKWADOR
    :cvar ER: ERYTREA
    :cvar EE: ESTONIA
    :cvar ET: ETIOPIA
    :cvar FK: FALKLANDY
    :cvar FJ: FIDŻI REPUBLIKA
    :cvar PH: FILIPINY
    :cvar FI: FINLANDIA
    :cvar FR: FRANCJA
    :cvar TF: FRANCUSKIE TERYTORIUM POŁUDNIOWE
    :cvar GA: GABON
    :cvar GM: GAMBIA
    :cvar GH: GHANA
    :cvar GI: GIBRALTAR
    :cvar GR: GRECJA
    :cvar GD: GRENADA
    :cvar GL: GRENLANDIA
    :cvar GE: GRUZJA
    :cvar GU: GUAM
    :cvar GG: GUERNSEY
    :cvar GY: GUJANA
    :cvar GF: GUJANA FRANCUSKA
    :cvar GP: GWADELUPA
    :cvar GT: GWATEMALA
    :cvar GN: GWINEA
    :cvar GQ: GWINEA RÓWNIKOWA
    :cvar GW: GWINEA-BISSAU
    :cvar HT: HAITI
    :cvar ES: HISZPANIA
    :cvar HN: HONDURAS
    :cvar HK: HONGKONG
    :cvar IN: INDIE
    :cvar ID: INDONEZJA
    :cvar IQ: IRAK
    :cvar IR: IRAN
    :cvar IE: IRLANDIA
    :cvar IS: ISLANDIA
    :cvar IL: IZRAEL
    :cvar JM: JAMAJKA
    :cvar JP: JAPONIA
    :cvar YE: JEMEN
    :cvar JE: JERSEY
    :cvar JO: JORDANIA
    :cvar KY: KAJMANY
    :cvar KH: KAMBODŻA
    :cvar CM: KAMERUN
    :cvar CA: KANADA
    :cvar QA: KATAR
    :cvar KZ: KAZACHSTAN
    :cvar KE: KENIA
    :cvar KG: KIRGISTAN
    :cvar KI: KIRIBATI
    :cvar CO: KOLUMBIA
    :cvar KM: KOMORY
    :cvar CG: KONGO
    :cvar CD: KONGO, REPUBLIKA DEMOKRATYCZNA
    :cvar KP: KOREAŃSKA REPUBLIKA LUDOWO-DEMOKRATYCZNA
    :cvar XK: KOSOWO
    :cvar CR: KOSTARYKA
    :cvar CU: KUBA
    :cvar KW: KUWEJT
    :cvar LA: LAOS
    :cvar LS: LESOTHO
    :cvar LB: LIBAN
    :cvar LR: LIBERIA
    :cvar LY: LIBIA
    :cvar LI: LIECHTENSTEIN
    :cvar LT: LITWA
    :cvar LV: ŁOTWA
    :cvar LU: LUKSEMBURG
    :cvar MK: MACEDONIA
    :cvar MG: MADAGASKAR
    :cvar YT: MAJOTTA
    :cvar MO: MAKAU
    :cvar MW: MALAWI
    :cvar MV: MALEDIWY
    :cvar MY: MALEZJA
    :cvar ML: MALI
    :cvar MT: MALTA
    :cvar MP: MARIANY PÓŁNOCNE
    :cvar MA: MAROKO
    :cvar MQ: MARTYNIKA
    :cvar MR: MAURETANIA
    :cvar MU: MAURITIUS
    :cvar MX: MEKSYK
    :cvar XL: MELILLA
    :cvar FM: MIKRONEZJA
    :cvar UM: MINOR
    :cvar MD: MOŁDOWA
    :cvar MC: MONAKO
    :cvar MN: MONGOLIA
    :cvar MS: MONTSERRAT
    :cvar MZ: MOZAMBIK
    :cvar MM: MYANMAR (BURMA)
    :cvar NA: NAMIBIA
    :cvar NR: NAURU
    :cvar NP: NEPAL
    :cvar NL: NIDERLANDY (HOLANDIA)
    :cvar DE: NIEMCY
    :cvar NE: NIGER
    :cvar NG: NIGERIA
    :cvar NI: NIKARAGUA
    :cvar NU: NIUE
    :cvar NF: NORFOLK
    :cvar NO: NORWEGIA
    :cvar NC: NOWA KALEDONIA
    :cvar NZ: NOWA ZELANDIA
    :cvar PS: OKUPOWANE TERYTORIUM PALESTYNY
    :cvar OM: OMAN
    :cvar PK: PAKISTAN
    :cvar PW: PALAU
    :cvar PA: PANAMA
    :cvar PG: PAPUA NOWA GWINEA
    :cvar PY: PARAGWAJ
    :cvar PE: PERU
    :cvar PN: PITCAIRN
    :cvar PF: POLINEZJA FRANCUSKA
    :cvar PL: POLSKA
    :cvar GS: POŁUDNIOWA GEORGIA I POŁUD.WYSPY SANDWICH
    :cvar PT: PORTUGALIA
    :cvar PR: PORTORYKO
    :cvar CF: REP.ŚRODKOWOAFRYKAŃSKA
    :cvar CZ: REPUBLIKA CZESKA
    :cvar KR: REPUBLIKA KOREI
    :cvar ZA: REPUBLIKA POŁUDNIOWEJ AFRYKI
    :cvar RE: REUNION
    :cvar RU: ROSJA
    :cvar RO: RUMUNIA
    :cvar RW: RWANDA
    :cvar EH: SAHARA ZACHODNIA
    :cvar BL: SAINT BARTHELEMY
    :cvar KN: SAINT KITTS I NEVIS
    :cvar LC: SAINT LUCIA
    :cvar MF: SAINT MARTIN
    :cvar VC: SAINT VINCENT I GRENADYNY
    :cvar SV: SALWADOR
    :cvar WS: SAMOA
    :cvar AS: SAMOA AMERYKAŃSKIE
    :cvar SM: SAN MARINO
    :cvar SN: SENEGAL
    :cvar RS: SERBIA
    :cvar SC: SESZELE
    :cvar SL: SIERRA LEONE
    :cvar SG: SINGAPUR
    :cvar SK: SŁOWACJA
    :cvar SI: SŁOWENIA
    :cvar SO: SOMALIA
    :cvar LK: SRI LANKA
    :cvar PM: SAINT PIERRE I MIQUELON
    :cvar US: STANY ZJEDNOCZONE AMERYKI
    :cvar SZ: SUAZI
    :cvar SD: SUDAN
    :cvar SS: SUDAN POŁUDNIOWY
    :cvar SR: SURINAM
    :cvar SJ: SVALBARD I JAN MAYEN
    :cvar SH: ŚWIĘTA HELENA
    :cvar SY: SYRIA
    :cvar CH: SZWAJCARIA
    :cvar SE: SZWECJA
    :cvar TJ: TADŻYKISTAN
    :cvar TH: TAJLANDIA
    :cvar TW: TAJWAN
    :cvar TZ: TANZANIA
    :cvar TG: TOGO
    :cvar TK: TOKELAU
    :cvar TO: TONGA
    :cvar TT: TRYNIDAD I TOBAGO
    :cvar TN: TUNEZJA
    :cvar TR: TURCJA
    :cvar TM: TURKMENISTAN
    :cvar TV: TUVALU
    :cvar UG: UGANDA
    :cvar UA: UKRAINA
    :cvar UY: URUGWAJ
    :cvar UZ: UZBEKISTAN
    :cvar VU: VANUATU
    :cvar WF: WALLIS I FUTUNA
    :cvar VA: WATYKAN
    :cvar HU: WĘGRY
    :cvar VE: WENEZUELA
    :cvar GB: WIELKA BRYTANIA
    :cvar VN: WIETNAM
    :cvar IT: WŁOCHY
    :cvar TL: WSCHODNI TIMOR
    :cvar CI: WYBRZEŻE KOŚCI SŁONIOWEJ
    :cvar BV: WYSPA BOUVETA
    :cvar CX: WYSPA BOŻEGO NARODZENIA
    :cvar IM: WYSPA MAN
    :cvar SX: WYSPA SINT MAARTEN (CZĘŚĆ HOLENDERSKA WYSPY)
    :cvar CK: WYSPY COOKA
    :cvar VI: WYSPY DZIEWICZE-USA
    :cvar VG: WYSPY DZIEWICZE-W.B.
    :cvar HM: WYSPY HEARD I MCDONALD
    :cvar CC: WYSPY KOKOSOWE (KEELINGA)
    :cvar MH: WYSPY MARSHALLA
    :cvar FO: WYSPY OWCZE
    :cvar SB: WYSPY SALOMONA
    :cvar ST: WYSPY ŚWIĘTEGO TOMASZA I KSIĄŻĘCA
    :cvar TC: WYSPY TURKS I CAICOS
    :cvar ZM: ZAMBIA
    :cvar CV: ZIELONY PRZYLĄDEK
    :cvar ZW: ZIMBABWE
    :cvar AE: ZJEDNOCZONE EMIRATY ARABSKIE
    :cvar XI: ZJEDNOCZONE KRÓLESTWO (IRLANDIA PÓŁNOCNA)
    """

    AF = "AF"
    AX = "AX"
    AL = "AL"
    DZ = "DZ"
    AD = "AD"
    AO = "AO"
    AI = "AI"
    AQ = "AQ"
    AG = "AG"
    AN = "AN"
    SA = "SA"
    AR = "AR"
    AM = "AM"
    AW = "AW"
    AU = "AU"
    AT = "AT"
    AZ = "AZ"
    BS = "BS"
    BH = "BH"
    BD = "BD"
    BB = "BB"
    BE = "BE"
    BZ = "BZ"
    BJ = "BJ"
    BM = "BM"
    BT = "BT"
    BY = "BY"
    BO = "BO"
    BQ = "BQ"
    BA = "BA"
    BW = "BW"
    BR = "BR"
    BN = "BN"
    IO = "IO"
    BG = "BG"
    BF = "BF"
    BI = "BI"
    XC = "XC"
    CL = "CL"
    CN = "CN"
    HR = "HR"
    CW = "CW"
    CY = "CY"
    TD = "TD"
    ME = "ME"
    DK = "DK"
    DM = "DM"
    DO = "DO"
    DJ = "DJ"
    EG = "EG"
    EC = "EC"
    ER = "ER"
    EE = "EE"
    ET = "ET"
    FK = "FK"
    FJ = "FJ"
    PH = "PH"
    FI = "FI"
    FR = "FR"
    TF = "TF"
    GA = "GA"
    GM = "GM"
    GH = "GH"
    GI = "GI"
    GR = "GR"
    GD = "GD"
    GL = "GL"
    GE = "GE"
    GU = "GU"
    GG = "GG"
    GY = "GY"
    GF = "GF"
    GP = "GP"
    GT = "GT"
    GN = "GN"
    GQ = "GQ"
    GW = "GW"
    HT = "HT"
    ES = "ES"
    HN = "HN"
    HK = "HK"
    IN = "IN"
    ID = "ID"
    IQ = "IQ"
    IR = "IR"
    IE = "IE"
    IS = "IS"
    IL = "IL"
    JM = "JM"
    JP = "JP"
    YE = "YE"
    JE = "JE"
    JO = "JO"
    KY = "KY"
    KH = "KH"
    CM = "CM"
    CA = "CA"
    QA = "QA"
    KZ = "KZ"
    KE = "KE"
    KG = "KG"
    KI = "KI"
    CO = "CO"
    KM = "KM"
    CG = "CG"
    CD = "CD"
    KP = "KP"
    XK = "XK"
    CR = "CR"
    CU = "CU"
    KW = "KW"
    LA = "LA"
    LS = "LS"
    LB = "LB"
    LR = "LR"
    LY = "LY"
    LI = "LI"
    LT = "LT"
    LV = "LV"
    LU = "LU"
    MK = "MK"
    MG = "MG"
    YT = "YT"
    MO = "MO"
    MW = "MW"
    MV = "MV"
    MY = "MY"
    ML = "ML"
    MT = "MT"
    MP = "MP"
    MA = "MA"
    MQ = "MQ"
    MR = "MR"
    MU = "MU"
    MX = "MX"
    XL = "XL"
    FM = "FM"
    UM = "UM"
    MD = "MD"
    MC = "MC"
    MN = "MN"
    MS = "MS"
    MZ = "MZ"
    MM = "MM"
    NA = "NA"
    NR = "NR"
    NP = "NP"
    NL = "NL"
    DE = "DE"
    NE = "NE"
    NG = "NG"
    NI = "NI"
    NU = "NU"
    NF = "NF"
    NO = "NO"
    NC = "NC"
    NZ = "NZ"
    PS = "PS"
    OM = "OM"
    PK = "PK"
    PW = "PW"
    PA = "PA"
    PG = "PG"
    PY = "PY"
    PE = "PE"
    PN = "PN"
    PF = "PF"
    PL = "PL"
    GS = "GS"
    PT = "PT"
    PR = "PR"
    CF = "CF"
    CZ = "CZ"
    KR = "KR"
    ZA = "ZA"
    RE = "RE"
    RU = "RU"
    RO = "RO"
    RW = "RW"
    EH = "EH"
    BL = "BL"
    KN = "KN"
    LC = "LC"
    MF = "MF"
    VC = "VC"
    SV = "SV"
    WS = "WS"
    AS = "AS"
    SM = "SM"
    SN = "SN"
    RS = "RS"
    SC = "SC"
    SL = "SL"
    SG = "SG"
    SK = "SK"
    SI = "SI"
    SO = "SO"
    LK = "LK"
    PM = "PM"
    US = "US"
    SZ = "SZ"
    SD = "SD"
    SS = "SS"
    SR = "SR"
    SJ = "SJ"
    SH = "SH"
    SY = "SY"
    CH = "CH"
    SE = "SE"
    TJ = "TJ"
    TH = "TH"
    TW = "TW"
    TZ = "TZ"
    TG = "TG"
    TK = "TK"
    TO = "TO"
    TT = "TT"
    TN = "TN"
    TR = "TR"
    TM = "TM"
    TV = "TV"
    UG = "UG"
    UA = "UA"
    UY = "UY"
    UZ = "UZ"
    VU = "VU"
    WF = "WF"
    VA = "VA"
    HU = "HU"
    VE = "VE"
    GB = "GB"
    VN = "VN"
    IT = "IT"
    TL = "TL"
    CI = "CI"
    BV = "BV"
    CX = "CX"
    IM = "IM"
    SX = "SX"
    CK = "CK"
    VI = "VI"
    VG = "VG"
    HM = "HM"
    CC = "CC"
    MH = "MH"
    FO = "FO"
    SB = "SB"
    ST = "ST"
    TC = "TC"
    ZM = "ZM"
    CV = "CV"
    ZW = "ZW"
    AE = "AE"
    XI = "XI"


class Twybor1(Enum):
    """
    Pojedyncze pole wyboru.
    """

    VALUE_1 = 1


class Twybor12(Enum):
    """
    Podwójne pole wyboru.
    """

    VALUE_1 = 1
    VALUE_2 = 2


@dataclass(kw_only=True)
class Tadres3:
    """
    Informacje opisujące adres.

    :ivar kod_kraju: Kod Kraju [Country Code]
    :ivar adres_l1: Adres [Address]
    :ivar adres_l2: Adres [Address]
    :ivar gln: Globalny Numer Lokalizacyjny [Global Location Number]
    """

    class Meta:
        name = "TAdres"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    kod_kraju: TkodKraju = field(
        metadata={
            "name": "KodKraju",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
        }
    )
    adres_l1: str = field(
        metadata={
            "name": "AdresL1",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "min_length": 1,
            "max_length": 512,
        }
    )
    adres_l2: None | str = field(
        default=None,
        metadata={
            "name": "AdresL2",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 512,
        },
    )
    gln: None | str = field(
        default=None,
        metadata={
            "name": "GLN",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 13,
        },
    )


@dataclass(kw_only=True)
class Tnaglowek:
    """
    Nagłówek.

    :ivar kod_formularza:
    :ivar wariant_formularza:
    :ivar data_wytworzenia_fa: Data i czas wytworzenia faktury
    :ivar system_info: Nazwa systemu teleinformatycznego, z którego
        korzysta podatnik
    """

    class Meta:
        name = "TNaglowek"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    kod_formularza: Tnaglowek.KodFormularza = field(
        metadata={
            "name": "KodFormularza",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
        }
    )
    wariant_formularza: TnaglowekWariantFormularza = field(
        metadata={
            "name": "WariantFormularza",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
        }
    )
    data_wytworzenia_fa: XmlDateTime = field(
        metadata={
            "name": "DataWytworzeniaFa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "min_inclusive": XmlDateTime(2025, 9, 1, 0, 0, 0, 0, 0),
            "max_inclusive": XmlDateTime(2050, 1, 1, 23, 59, 59, 0, 0),
            "white_space": "collapse",
        }
    )
    system_info: None | str = field(
        default=None,
        metadata={
            "name": "SystemInfo",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 256,
        },
    )

    @dataclass(kw_only=True)
    class KodFormularza:
        value: TkodFormularza = field(
            metadata={
                "required": True,
            }
        )
        kod_systemowy: str = field(
            init=False,
            default="FA (3)",
            metadata={
                "name": "kodSystemowy",
                "type": "Attribute",
                "required": True,
            },
        )
        wersja_schemy: str = field(
            init=False,
            default="1-0E",
            metadata={
                "name": "wersjaSchemy",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class Tpodmiot2:
    """
    Zestaw danych identyfikacyjnych oraz danych adresowych nabywcy.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar kod_ue: Kod (prefiks) nabywcy VAT UE, o którym mowa w art.
        106e ust. 1 pkt 24 ustawy oraz w przypadku, o którym mowa w art.
        136 ust. 1 pkt 4 ustawy
    :ivar nr_vat_ue: Numer Identyfikacyjny VAT kontrahenta UE
    :ivar kod_kraju: Kod kraju nadania identyfikatora podatkowego
    :ivar nr_id: Identyfikator podatkowy inny
    :ivar brak_id: Podmiot nie posiada identyfikatora podatkowego lub
        identyfikator nie występuje na fakturze: 1- tak
    :ivar nazwa: Imię i nazwisko lub nazwa
    """

    class Meta:
        name = "TPodmiot2"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )
    kod_ue: None | TkodyKrajowUe = field(
        default=None,
        metadata={
            "name": "KodUE",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nr_vat_ue: None | str = field(
        default=None,
        metadata={
            "name": "NrVatUE",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "pattern": r"(\d|[A-Z]|\+|\*){1,12}",
        },
    )
    kod_kraju: None | TkodKraju = field(
        default=None,
        metadata={
            "name": "KodKraju",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nr_id: None | str = field(
        default=None,
        metadata={
            "name": "NrID",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 50,
            "white_space": "replace",
        },
    )
    brak_id: None | Twybor1 = field(
        default=None,
        metadata={
            "name": "BrakID",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nazwa: None | str = field(
        default=None,
        metadata={
            "name": "Nazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 512,
        },
    )


@dataclass(kw_only=True)
class Tpodmiot3:
    """
    Zestaw danych identyfikacyjnych oraz danych adresowych podmiotów
    trzecich.

    :ivar nip: Identyfikator podatkowy NIP
    :ivar idwew: Identyfikator wewnętrzny z NIP
    :ivar kod_ue: Kod (prefiks) nabywcy VAT UE, o którym mowa w art.
        106e ust. 1 pkt 24 ustawy oraz w przypadku, o którym mowa w art.
        136 ust. 1 pkt 4 ustawy
    :ivar nr_vat_ue: Numer Identyfikacyjny VAT kontrahenta UE
    :ivar kod_kraju: Kod kraju nadania identyfikatora podatkowego
    :ivar nr_id: Identyfikator podatkowy inny
    :ivar brak_id: Podmiot nie posiada identyfikatora podatkowego lub
        identyfikator nie występuje na fakturze: 1- tak
    :ivar nazwa: Imię i nazwisko lub nazwa
    """

    class Meta:
        name = "TPodmiot3"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    nip: None | str = field(
        default=None,
        metadata={
            "name": "NIP",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}",
        },
    )
    idwew: None | str = field(
        default=None,
        metadata={
            "name": "IDWew",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 20,
            "pattern": r"[1-9]((\d[1-9])|([1-9]\d))\d{7}-\d{5}",
        },
    )
    kod_ue: None | TkodyKrajowUe = field(
        default=None,
        metadata={
            "name": "KodUE",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nr_vat_ue: None | str = field(
        default=None,
        metadata={
            "name": "NrVatUE",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "pattern": r"(\d|[A-Z]|\+|\*){1,12}",
        },
    )
    kod_kraju: None | TkodKraju = field(
        default=None,
        metadata={
            "name": "KodKraju",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nr_id: None | str = field(
        default=None,
        metadata={
            "name": "NrID",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 50,
            "white_space": "replace",
        },
    )
    brak_id: None | Twybor1 = field(
        default=None,
        metadata={
            "name": "BrakID",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nazwa: None | str = field(
        default=None,
        metadata={
            "name": "Nazwa",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 512,
        },
    )


@dataclass(kw_only=True)
class TrachunekBankowy:
    """
    Informacje o rachunku.

    :ivar nr_rb: Pełny numer rachunku
    :ivar swift: Kod SWIFT
    :ivar rachunek_wlasny_banku: Rachunek własny
    :ivar nazwa_banku: Nazwa
    :ivar opis_rachunku: Opis rachunku
    """

    class Meta:
        name = "TRachunekBankowy"
        target_namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    nr_rb: str = field(
        metadata={
            "name": "NrRB",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "required": True,
            "min_length": 10,
            "max_length": 34,
        }
    )
    swift: None | str = field(
        default=None,
        metadata={
            "name": "SWIFT",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "pattern": r"[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3}){0,1}",
        },
    )
    rachunek_wlasny_banku: None | TrachunekWlasnyBanku = field(
        default=None,
        metadata={
            "name": "RachunekWlasnyBanku",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
        },
    )
    nazwa_banku: None | str = field(
        default=None,
        metadata={
            "name": "NazwaBanku",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 256,
        },
    )
    opis_rachunku: None | str = field(
        default=None,
        metadata={
            "name": "OpisRachunku",
            "type": "Element",
            "namespace": "http://crd.gov.pl/wzor/2025/06/25/13775/",
            "min_length": 1,
            "max_length": 256,
        },
    )


@dataclass(kw_only=True)
class TadresPolski:
    """
    Informacje opisujące adres polski.

    :ivar kod_kraju: Kraj
    :ivar wojewodztwo: Województwo
    :ivar powiat: Powiat
    :ivar gmina: Gmina
    :ivar ulica: Nazwa ulicy
    :ivar nr_domu: Numer budynku
    :ivar nr_lokalu: Numer lokalu
    :ivar miejscowosc: Nazwa miejscowości
    :ivar kod_pocztowy: Kod pocztowy
    :ivar poczta: Nazwa urzędu pocztowego
    """

    class Meta:
        name = "TAdresPolski"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    kod_kraju: TkodKraju = field(
        init=False,
        default=TkodKraju.PL,
        metadata={
            "name": "KodKraju",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        },
    )
    wojewodztwo: str = field(
        metadata={
            "name": "Wojewodztwo",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    powiat: str = field(
        metadata={
            "name": "Powiat",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    gmina: str = field(
        metadata={
            "name": "Gmina",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    ulica: None | str = field(
        default=None,
        metadata={
            "name": "Ulica",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 65,
        },
    )
    nr_domu: str = field(
        metadata={
            "name": "NrDomu",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 9,
        }
    )
    nr_lokalu: None | str = field(
        default=None,
        metadata={
            "name": "NrLokalu",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 10,
        },
    )
    miejscowosc: str = field(
        metadata={
            "name": "Miejscowosc",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 56,
        }
    )
    kod_pocztowy: str = field(
        metadata={
            "name": "KodPocztowy",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 8,
        }
    )
    poczta: str = field(
        metadata={
            "name": "Poczta",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 56,
        }
    )


@dataclass(kw_only=True)
class TadresPolski1:
    """
    Informacje opisujące adres polski - bez elementu Poczta.

    :ivar kod_kraju: Kraj
    :ivar wojewodztwo: Województwo
    :ivar powiat: Powiat
    :ivar gmina: Gmina
    :ivar ulica: Nazwa ulicy
    :ivar nr_domu: Numer budynku
    :ivar nr_lokalu: Numer lokalu
    :ivar miejscowosc: Nazwa miejscowości
    :ivar kod_pocztowy: Kod pocztowy
    """

    class Meta:
        name = "TAdresPolski1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    kod_kraju: TkodKraju = field(
        init=False,
        default=TkodKraju.PL,
        metadata={
            "name": "KodKraju",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        },
    )
    wojewodztwo: str = field(
        metadata={
            "name": "Wojewodztwo",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    powiat: str = field(
        metadata={
            "name": "Powiat",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    gmina: str = field(
        metadata={
            "name": "Gmina",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 36,
        }
    )
    ulica: None | str = field(
        default=None,
        metadata={
            "name": "Ulica",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 65,
        },
    )
    nr_domu: str = field(
        metadata={
            "name": "NrDomu",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 9,
        }
    )
    nr_lokalu: None | str = field(
        default=None,
        metadata={
            "name": "NrLokalu",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 10,
        },
    )
    miejscowosc: str = field(
        metadata={
            "name": "Miejscowosc",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 56,
        }
    )
    kod_pocztowy: str = field(
        metadata={
            "name": "KodPocztowy",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 8,
        }
    )


@dataclass(kw_only=True)
class TadresZagraniczny:
    """
    Informacje opisujące adres zagraniczny.

    :ivar kod_kraju: Kod Kraju [Country Code]
    :ivar kod_pocztowy: Kod pocztowy [Postal code]
    :ivar miejscowosc: Nazwa miejscowości [City]
    :ivar ulica: Nazwa ulicy [Street]
    :ivar nr_domu: Numer budynku [Building number]
    :ivar nr_lokalu: Numer lokalu [Flat number]
    """

    class Meta:
        name = "TAdresZagraniczny"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    kod_kraju: TkodKraju = field(
        metadata={
            "name": "KodKraju",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "pattern": r"P[A-KM-Z]|[A-OQ-Z][A-Z]",
        }
    )
    kod_pocztowy: None | str = field(
        default=None,
        metadata={
            "name": "KodPocztowy",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 8,
        },
    )
    miejscowosc: str = field(
        metadata={
            "name": "Miejscowosc",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
            "min_length": 1,
            "max_length": 56,
        }
    )
    ulica: None | str = field(
        default=None,
        metadata={
            "name": "Ulica",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 65,
        },
    )
    nr_domu: None | str = field(
        default=None,
        metadata={
            "name": "NrDomu",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 9,
        },
    )
    nr_lokalu: None | str = field(
        default=None,
        metadata={
            "name": "NrLokalu",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "min_length": 1,
            "max_length": 10,
        },
    )


@dataclass(kw_only=True)
class TpodmiotDowolnyBezAdresu:
    """
    Skrócony zestaw danych o osobie fizycznej lub niefizycznej.
    """

    class Meta:
        name = "TPodmiotDowolnyBezAdresu"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: None | TidentyfikatorOsobyFizycznej = field(
        default=None,
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    osoba_niefizyczna: None | TidentyfikatorOsobyNiefizycznej = field(
        default=None,
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )


@dataclass(kw_only=True)
class TpodmiotDowolnyBezAdresu1:
    """
    Skrócony zestaw danych o osobie fizycznej lub niefizycznej z
    identyfikatorem NIP albo PESEL.
    """

    class Meta:
        name = "TPodmiotDowolnyBezAdresu1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: None | TidentyfikatorOsobyFizycznej1 = field(
        default=None,
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    osoba_niefizyczna: None | TidentyfikatorOsobyNiefizycznej = field(
        default=None,
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )


@dataclass(kw_only=True)
class TpodmiotDowolnyBezAdresu2:
    """
    Skrócony zestaw danych o osobie fizycznej lub niefizycznej z
    identyfikatorem NIP.
    """

    class Meta:
        name = "TPodmiotDowolnyBezAdresu2"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: None | TidentyfikatorOsobyFizycznej2 = field(
        default=None,
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    osoba_niefizyczna: None | TidentyfikatorOsobyNiefizycznej = field(
        default=None,
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )


@dataclass(kw_only=True)
class TpodmiotDowolnyBezAdresu3:
    """
    Skrócony zestaw danych o osobie fizycznej lub niefizycznej z
    identyfikatorem NIP - bez elementu numer REGON dla osoby niefizycznej.
    """

    class Meta:
        name = "TPodmiotDowolnyBezAdresu3"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: None | TidentyfikatorOsobyFizycznej2 = field(
        default=None,
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    osoba_niefizyczna: None | TidentyfikatorOsobyNiefizycznej1 = field(
        default=None,
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )


@dataclass(kw_only=True)
class Faktura:
    """
    Faktura VAT.

    :ivar naglowek: Nagłówek
    :ivar podmiot1: Dane podatnika. Imię i nazwisko lub nazwa sprzedawcy
        towarów lub usług
    :ivar podmiot2: Dane nabywcy
    :ivar podmiot3: Dane podmiotu/-ów trzeciego/-ich (innego/-ych niż
        sprzedawca i nabywca wymieniony w części Podmiot2),
        związanego/-ych z fakturą
    :ivar podmiot_upowazniony: Dane podmiotu upoważnionego, związanego z
        fakturą
    :ivar fa: Na podstawie art. 106a - 106q ustawy. Pola dotyczące
        wartości sprzedaży i podatku wypełnia się w walucie, w której
        wystawiono fakturę, z wyjątkiem pól dotyczących podatku
        przeliczonego zgodnie z przepisami działu VI w związku z art.
        106e ust. 11 ustawy. W przypadku wystawienia faktury korygującej
        wypełnia się wszystkie pola wg stanu po korekcie, a pola
        dotyczące podstaw opodatkowania, podatku oraz należności ogółem
        wypełnia się poprzez różnicę
    :ivar stopka: Pozostałe dane na fakturze
    :ivar zalacznik: Załącznik do faktury VAT
    """

    class Meta:
        namespace = "http://crd.gov.pl/wzor/2025/06/25/13775/"

    naglowek: Tnaglowek = field(
        metadata={
            "name": "Naglowek",
            "type": "Element",
            "required": True,
        }
    )
    podmiot1: Faktura.Podmiot1 = field(
        metadata={
            "name": "Podmiot1",
            "type": "Element",
            "required": True,
        }
    )
    podmiot2: Faktura.Podmiot2 = field(
        metadata={
            "name": "Podmiot2",
            "type": "Element",
            "required": True,
        }
    )
    podmiot3: list[Faktura.Podmiot3] = field(
        default_factory=list,
        metadata={
            "name": "Podmiot3",
            "type": "Element",
            "max_occurs": 100,
        },
    )
    podmiot_upowazniony: None | Faktura.PodmiotUpowazniony = field(
        default=None,
        metadata={
            "name": "PodmiotUpowazniony",
            "type": "Element",
        },
    )
    fa: Faktura.Fa = field(
        metadata={
            "name": "Fa",
            "type": "Element",
            "required": True,
        }
    )
    stopka: None | Faktura.Stopka = field(
        default=None,
        metadata={
            "name": "Stopka",
            "type": "Element",
        },
    )
    zalacznik: None | Faktura.Zalacznik = field(
        default=None,
        metadata={
            "name": "Zalacznik",
            "type": "Element",
        },
    )

    @dataclass(kw_only=True)
    class Podmiot1:
        """
        :ivar prefiks_podatnika: Kod (prefiks) podatnika VAT UE dla
            przypadków określonych w art. 97 ust. 10 pkt 2 i 3 ustawy
            oraz w przypadku, o którym mowa w art. 136 ust. 1 pkt 3
            ustawy
        :ivar nr_eori: Numer EORI podatnika (sprzedawcy)
        :ivar dane_identyfikacyjne: Dane identyfikujące podatnika
        :ivar adres: Adres podatnika
        :ivar adres_koresp: Adres korespondencyjny podatnika
        :ivar dane_kontaktowe: Dane kontaktowe podatnika
        :ivar status_info_podatnika: Status podatnika
        """

        prefiks_podatnika: None | TkodyKrajowUe = field(
            default=None,
            metadata={
                "name": "PrefiksPodatnika",
                "type": "Element",
            },
        )
        nr_eori: None | str = field(
            default=None,
            metadata={
                "name": "NrEORI",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        dane_identyfikacyjne: Tpodmiot1 = field(
            metadata={
                "name": "DaneIdentyfikacyjne",
                "type": "Element",
                "required": True,
            }
        )
        adres: Tadres3 = field(
            metadata={
                "name": "Adres",
                "type": "Element",
                "required": True,
            }
        )
        adres_koresp: None | Tadres3 = field(
            default=None,
            metadata={
                "name": "AdresKoresp",
                "type": "Element",
            },
        )
        dane_kontaktowe: list[Faktura.Podmiot1.DaneKontaktowe] = field(
            default_factory=list,
            metadata={
                "name": "DaneKontaktowe",
                "type": "Element",
                "max_occurs": 3,
            },
        )
        status_info_podatnika: None | TstatusInfoPodatnika = field(
            default=None,
            metadata={
                "name": "StatusInfoPodatnika",
                "type": "Element",
            },
        )

        @dataclass(kw_only=True)
        class DaneKontaktowe:
            """
            :ivar email: Adres e-mail podatnika
            :ivar telefon: Numer telefonu podatnika
            """

            email: None | str = field(
                default=None,
                metadata={
                    "name": "Email",
                    "type": "Element",
                    "min_length": 3,
                    "max_length": 255,
                    "pattern": r"(.)+@(.)+",
                },
            )
            telefon: None | str = field(
                default=None,
                metadata={
                    "name": "Telefon",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 16,
                },
            )

    @dataclass(kw_only=True)
    class Podmiot2:
        """
        :ivar nr_eori: Numer EORI nabywcy towarów
        :ivar dane_identyfikacyjne: Dane identyfikujące nabywcę
        :ivar adres: Adres nabywcy. Pola opcjonalne dla przypadków
            określonych w art. 106e ust. 5 pkt 3 ustawy
        :ivar adres_koresp: Adres korespondencyjny nabywcy
        :ivar dane_kontaktowe: Dane kontaktowe nabywcy
        :ivar nr_klienta: Numer klienta dla przypadków, w których
            nabywca posługuje się nim w umowie lub zamówieniu
        :ivar idnabywcy: Unikalny klucz powiązania danych nabywcy na
            fakturach korygujących, w przypadku gdy dane nabywcy na
            fakturze korygującej zmieniły się w stosunku do danych na
            fakturze korygowanej
        :ivar jst: Znacznik jednostki podrzędnej JST. Wartość "1"
            oznacza, że faktura dotyczy jednostki podrzędnej JST. W
            takim przypadku, aby udostępnić fakturę jednostce podrzędnej
            JST, należy wypełnić sekcję Podmiot3, w szczególności podać
            NIP lub ID-Wew i określić rolę jako 8. Wartość "2" oznacza,
            że faktura nie dotyczy jednostki podrzędnej JST
        :ivar gv: Znacznik członka grupy VAT.
            Wartość "1" oznacza, że faktura dotyczy członka grupy VAT. W
            takim przypadku, aby udostępnić fakturę członkowi grupy VAT,
            należy wypełnić sekcję Podmiot3, w szczególności podać NIP
            lub ID-Wew i określić rolę jako 10. Wartość "2" oznacza, że
            faktura nie dotyczy członka grupy VAT
        """

        nr_eori: None | str = field(
            default=None,
            metadata={
                "name": "NrEORI",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        dane_identyfikacyjne: Tpodmiot2 = field(
            metadata={
                "name": "DaneIdentyfikacyjne",
                "type": "Element",
                "required": True,
            }
        )
        adres: None | Tadres3 = field(
            default=None,
            metadata={
                "name": "Adres",
                "type": "Element",
            },
        )
        adres_koresp: None | Tadres3 = field(
            default=None,
            metadata={
                "name": "AdresKoresp",
                "type": "Element",
            },
        )
        dane_kontaktowe: list[Faktura.Podmiot2.DaneKontaktowe] = field(
            default_factory=list,
            metadata={
                "name": "DaneKontaktowe",
                "type": "Element",
                "max_occurs": 3,
            },
        )
        nr_klienta: None | str = field(
            default=None,
            metadata={
                "name": "NrKlienta",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        idnabywcy: None | str = field(
            default=None,
            metadata={
                "name": "IDNabywcy",
                "type": "Element",
                "min_length": 1,
                "max_length": 32,
            },
        )
        jst: Podmiot2Jst = field(
            metadata={
                "name": "JST",
                "type": "Element",
                "required": True,
            }
        )
        gv: Podmiot2Gv = field(
            metadata={
                "name": "GV",
                "type": "Element",
                "required": True,
            }
        )

        @dataclass(kw_only=True)
        class DaneKontaktowe:
            """
            :ivar email: Adres e-mail nabywcy
            :ivar telefon: Numer telefonu nabywcy
            """

            email: None | str = field(
                default=None,
                metadata={
                    "name": "Email",
                    "type": "Element",
                    "min_length": 3,
                    "max_length": 255,
                    "pattern": r"(.)+@(.)+",
                },
            )
            telefon: None | str = field(
                default=None,
                metadata={
                    "name": "Telefon",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 16,
                },
            )

    @dataclass(kw_only=True)
    class Podmiot3:
        """
        :ivar idnabywcy: Unikalny klucz powiązania danych nabywcy na
            fakturach korygujących, w przypadku gdy dane nabywcy na
            fakturze korygującej zmieniły się w stosunku do danych na
            fakturze korygowanej
        :ivar nr_eori: Numer EORI podmiotu trzeciego
        :ivar dane_identyfikacyjne: Dane identyfikujące podmiot trzeci
        :ivar adres: Adres podmiotu trzeciego
        :ivar adres_koresp: Adres korespondencyjny podmiotu trzeciego
        :ivar dane_kontaktowe: Dane kontaktowe podmiotu trzeciego
        :ivar rola: Rola podmiotu
        :ivar rola_inna: Znacznik innego podmiotu: 1 - Inny podmiot
        :ivar opis_roli: Opis roli podmiotu - w przypadku wyboru roli
            jako Inny podmiot
        :ivar udzial: Udział - procentowy udział dodatkowego nabywcy.
            Różnica pomiędzy wartością 100% a sumą udziałów dodatkowych
            nabywców jest udziałem nabywcy wymienionego w części
            Podmiot2. W przypadku niewypełnienia pola przyjmuje się, że
            udziały występujących na fakturze nabywców są równe
        :ivar nr_klienta: Numer klienta dla przypadków, w których
            podmiot wymieniony jako podmiot trzeci posługuje się nim w
            umowie lub zamówieniu
        """

        idnabywcy: None | str = field(
            default=None,
            metadata={
                "name": "IDNabywcy",
                "type": "Element",
                "min_length": 1,
                "max_length": 32,
            },
        )
        nr_eori: None | str = field(
            default=None,
            metadata={
                "name": "NrEORI",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        dane_identyfikacyjne: Tpodmiot3 = field(
            metadata={
                "name": "DaneIdentyfikacyjne",
                "type": "Element",
                "required": True,
            }
        )
        adres: None | Tadres3 = field(
            default=None,
            metadata={
                "name": "Adres",
                "type": "Element",
            },
        )
        adres_koresp: None | Tadres3 = field(
            default=None,
            metadata={
                "name": "AdresKoresp",
                "type": "Element",
            },
        )
        dane_kontaktowe: list[Faktura.Podmiot3.DaneKontaktowe] = field(
            default_factory=list,
            metadata={
                "name": "DaneKontaktowe",
                "type": "Element",
                "max_occurs": 3,
            },
        )
        rola: None | TrolaPodmiotu3 = field(
            default=None,
            metadata={
                "name": "Rola",
                "type": "Element",
            },
        )
        rola_inna: None | Twybor1 = field(
            default=None,
            metadata={
                "name": "RolaInna",
                "type": "Element",
            },
        )
        opis_roli: None | str = field(
            default=None,
            metadata={
                "name": "OpisRoli",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        udzial: None | Decimal = field(
            default=None,
            metadata={
                "name": "Udzial",
                "type": "Element",
                "min_inclusive": Decimal("0"),
                "max_inclusive": Decimal("100"),
                "total_digits": 9,
                "fraction_digits": 6,
                "white_space": "collapse",
            },
        )
        nr_klienta: None | str = field(
            default=None,
            metadata={
                "name": "NrKlienta",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )

        @dataclass(kw_only=True)
        class DaneKontaktowe:
            """
            :ivar email: Adres e-mail podmiotu trzeciego
            :ivar telefon: Numer telefonu podmiotu trzeciego
            """

            email: None | str = field(
                default=None,
                metadata={
                    "name": "Email",
                    "type": "Element",
                    "min_length": 3,
                    "max_length": 255,
                    "pattern": r"(.)+@(.)+",
                },
            )
            telefon: None | str = field(
                default=None,
                metadata={
                    "name": "Telefon",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 16,
                },
            )

    @dataclass(kw_only=True)
    class PodmiotUpowazniony:
        """
        :ivar nr_eori: Numer EORI podmiotu upoważnionego
        :ivar dane_identyfikacyjne: Dane identyfikujące podmiotu
            upoważnionego
        :ivar adres: Adres podmiotu upoważnionego
        :ivar adres_koresp: Adres korespondencyjny podmiotu
            upoważnionego
        :ivar dane_kontaktowe: Dane kontaktowe podmiotu upoważnionego
        :ivar rola_pu: Rola podmiotu upoważnionego
        """

        nr_eori: None | str = field(
            default=None,
            metadata={
                "name": "NrEORI",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        dane_identyfikacyjne: Tpodmiot1 = field(
            metadata={
                "name": "DaneIdentyfikacyjne",
                "type": "Element",
                "required": True,
            }
        )
        adres: Tadres3 = field(
            metadata={
                "name": "Adres",
                "type": "Element",
                "required": True,
            }
        )
        adres_koresp: None | Tadres3 = field(
            default=None,
            metadata={
                "name": "AdresKoresp",
                "type": "Element",
            },
        )
        dane_kontaktowe: list[Faktura.PodmiotUpowazniony.DaneKontaktowe] = field(
            default_factory=list,
            metadata={
                "name": "DaneKontaktowe",
                "type": "Element",
                "max_occurs": 3,
            },
        )
        rola_pu: TrolaPodmiotuUpowaznionego = field(
            metadata={
                "name": "RolaPU",
                "type": "Element",
                "required": True,
            }
        )

        @dataclass(kw_only=True)
        class DaneKontaktowe:
            """
            :ivar email_pu: Adres e-mail podmiotu upoważnionego
            :ivar telefon_pu: Numer telefonu podmiotu upoważnionego
            """

            email_pu: None | str = field(
                default=None,
                metadata={
                    "name": "EmailPU",
                    "type": "Element",
                    "min_length": 3,
                    "max_length": 255,
                    "pattern": r"(.)+@(.)+",
                },
            )
            telefon_pu: None | str = field(
                default=None,
                metadata={
                    "name": "TelefonPU",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 16,
                },
            )

    @dataclass(kw_only=True)
    class Fa:
        """
        :ivar kod_waluty: Kod waluty (ISO 4217)
        :ivar p_1: Data wystawienia, z zastrzeżeniem art. 106na ust. 1
            ustawy
        :ivar p_1_m: Miejsce wystawienia faktury
        :ivar p_2: Kolejny numer faktury, nadany w ramach jednej lub
            więcej serii, który w sposób jednoznaczny identyfikuje
            fakturę
        :ivar wz: Numery dokumentów magazynowych WZ (wydanie na
            zewnątrz) związane z fakturą
        :ivar p_6: Data dokonania lub zakończenia dostawy towarów lub
            wykonania usługi lub data otrzymania zapłaty, o której mowa
            w art. 106b ust. 1 pkt 4 ustawy, o ile taka data jest
            określona i różni się od daty wystawienia faktury. Pole
            wypełnia się w przypadku, gdy dla wszystkich pozycji faktury
            data jest wspólna
        :ivar okres_fa: Okres, którego dotyczy faktura - w przypadkach,
            o których mowa w art. 19a ust. 3 zdanie pierwsze i ust. 4
            oraz ust. 5 pkt 4 ustawy
        :ivar p_13_1: Suma wartości sprzedaży netto objętej stawką
            podstawową - aktualnie 23% albo 22%. W przypadku faktur
            zaliczkowych - wartość zaliczki netto. W przypadku faktur
            korygujących - kwota różnicy, o której mowa w art. 106j ust.
            2 pkt 5 ustawy
        :ivar p_14_1: Kwota podatku od sumy wartości sprzedaży netto
            objętej stawką podstawową - aktualnie 23% albo 22%. W
            przypadku faktur zaliczkowych - kwota podatku wyliczona
            według wzoru, o którym mowa w art. 106f ust. 1 pkt 3 ustawy.
            W przypadku faktur korygujących - kwota różnicy, o której
            mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_14_1_w: W przypadku gdy faktura jest wystawiona w
            walucie obcej - kwota podatku od sumy wartości sprzedaży
            netto objętej stawką podstawową, przeliczona zgodnie z
            przepisami działu VI w związku z art. 106e ust. 11 ustawy -
            aktualnie 23% albo 22%. W przypadku faktur zaliczkowych -
            kwota podatku wyliczona według wzoru, o którym mowa w art.
            106f ust. 1 pkt 3 ustawy. W przypadku faktur korygujących -
            kwota różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_2: Suma wartości sprzedaży netto objętej stawką
            obniżoną pierwszą - aktualnie 8 % albo 7%. W przypadku
            faktur zaliczkowych - wartość zaliczki netto. W przypadku
            faktur korygujących - kwota różnicy, o której mowa w art.
            106j ust. 2 pkt 5 ustawy
        :ivar p_14_2: Kwota podatku od sumy wartości sprzedaży netto
            objętej stawką obniżoną pierwszą - aktualnie 8% albo 7%. W
            przypadku faktur zaliczkowych - kwota podatku wyliczona
            według wzoru, o którym mowa w art. 106f ust. 1 pkt 3 ustawy.
            W przypadku faktur korygujących - kwota różnicy, o której
            mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_14_2_w: W przypadku gdy faktura jest wystawiona w
            walucie obcej - kwota podatku od sumy wartości sprzedaży
            netto objętej stawką obniżoną pierwszą, przeliczona zgodnie
            z przepisami działu VI w związku z art. 106e ust. 11 ustawy
            - aktualnie 8% albo 7%. W przypadku faktur zaliczkowych -
            kwota podatku wyliczona według wzoru, o którym mowa w art.
            106f ust. 1 pkt 3 ustawy. W przypadku faktur korygujących -
            kwota różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_3: Suma wartości sprzedaży netto objętej stawką
            obniżoną drugą - aktualnie 5%. W przypadku faktur
            zaliczkowych - wartość zaliczki netto. W przypadku faktur
            korygujących - kwota różnicy, o której mowa w art. 106j ust.
            2 pkt 5 ustawy
        :ivar p_14_3: Kwota podatku od sumy wartości sprzedaży netto
            objętej stawką obniżoną drugą - aktualnie 5%. W przypadku
            faktur zaliczkowych - kwota podatku wyliczona według wzoru,
            o którym mowa w art. 106f ust. 1 pkt 3 ustawy. W przypadku
            faktur korygujących - kwota różnicy, o której mowa w art.
            106j ust. 2 pkt 5 ustawy
        :ivar p_14_3_w: W przypadku gdy faktura jest wystawiona w
            walucie obcej - kwota podatku od sumy wartości sprzedaży
            netto objętej stawką obniżoną drugą, przeliczona zgodnie z
            przepisami działu VI w związku z art. 106e ust. 11 ustawy -
            aktualnie 5%. W przypadku faktur zaliczkowych - kwota
            podatku wyliczona według wzoru, o którym mowa w art. 106f
            ust. 1 pkt 3 ustawy. W przypadku faktur korygujących - kwota
            różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_4: Suma wartości sprzedaży netto objętej ryczałtem
            dla taksówek osobowych. W przypadku faktur zaliczkowych -
            wartość zaliczki netto. W przypadku faktur korygujących -
            kwota różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_14_4: Kwota podatku od sumy wartości sprzedaży netto w
            przypadku ryczałtu dla taksówek osobowych. W przypadku
            faktur zaliczkowych - kwota podatku wyliczona według wzoru,
            o którym mowa w art. 106f ust. 1 pkt 3 ustawy. W przypadku
            faktur korygujących - kwota różnicy, o której mowa w art.
            106j ust. 2 pkt 5 ustawy
        :ivar p_14_4_w: W przypadku gdy faktura jest wystawiona w
            walucie obcej - wysokość ryczałtu dla taksówek osobowych,
            przeliczona zgodnie z przepisami działu VI w związku z art.
            106e ust. 11 ustawy. W przypadku faktur zaliczkowych - kwota
            podatku wyliczona według wzoru, o którym mowa w art. 106f
            ust. 1 pkt 3 ustawy. W przypadku faktur korygujących - kwota
            różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_5: Suma wartości sprzedaży netto w przypadku
            procedury szczególnej, o której mowa w dziale XII w
            rozdziale 6a ustawy. W przypadku faktur zaliczkowych -
            wartość zaliczki netto. W przypadku faktur korygujących -
            kwota różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_14_5: Kwota podatku od wartości dodanej w przypadku
            procedury szczególnej, o której mowa w dziale XII w
            rozdziale 6a ustawy. W przypadku faktur zaliczkowych - kwota
            podatku wyliczona według wzoru, o którym mowa w art. 106f
            ust. 1 pkt 3 ustawy. W przypadku faktur korygujących - kwota
            różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_6_1: Suma wartości sprzedaży objętej stawką 0% z
            wyłączeniem wewnątrzwspólnotowej dostawy towarów i eksportu.
            W przypadku faktur zaliczkowych - wartość zaliczki. W
            przypadku faktur korygujących - kwota różnicy, o której mowa
            w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_6_2: Suma wartości sprzedaży objętej stawką 0% w
            przypadku wewnątrzwspólnotowej dostawy towarów. W przypadku
            faktur korygujących - kwota różnicy, o której mowa w art.
            106j ust. 2 pkt 5 ustawy
        :ivar p_13_6_3: Suma wartości sprzedaży objętej stawką 0% w
            przypadku eksportu. W przypadku faktur zaliczkowych -
            wartość zaliczki. W przypadku faktur korygujących - kwota
            różnicy, o której mowa w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_7: Suma wartości sprzedaży zwolnionej od podatku. W
            przypadku faktur zaliczkowych - wartość zaliczki. W
            przypadku faktur korygujących - kwota różnicy wartości
            sprzedaży
        :ivar p_13_8: Suma wartości sprzedaży w przypadku dostawy
            towarów oraz świadczenia usług poza terytorium kraju, z
            wyłączeniem kwot wykazanych w polach P_13_5 i P_13_9. W
            przypadku faktur zaliczkowych - wartość zaliczki. W
            przypadku faktur korygujących - kwota różnicy wartości
            sprzedaży
        :ivar p_13_9: Suma wartości świadczenia usług, o których mowa w
            art. 100 ust. 1 pkt 4 ustawy. W przypadku faktur
            zaliczkowych - wartość zaliczki. W przypadku faktur
            korygujących - kwota różnicy wartości sprzedaży
        :ivar p_13_10: Suma wartości sprzedaży w procedurze odwrotnego
            obciążenia, dla której podatnikiem jest nabywca zgodnie z
            art. 17 ust. 1 pkt 7 i 8 ustawy oraz innych przypadków
            odwrotnego obciążenia występujących w obrocie krajowym. W
            przypadku faktur zaliczkowych - wartość zaliczki. W
            przypadku faktur korygujących - kwota różnicy, o której mowa
            w art. 106j ust. 2 pkt 5 ustawy
        :ivar p_13_11: Suma wartości sprzedaży w procedurze marży, o
            której mowa w art. 119 i art. 120 ustawy. W przypadku faktur
            zaliczkowych - wartość zaliczki. W przypadku faktur
            korygujących - kwota różnicy wartości sprzedaży
        :ivar p_15: Kwota należności ogółem. W przypadku faktur
            zaliczkowych - kwota zapłaty dokumentowana fakturą. W
            przypadku faktur, o których mowa w art. 106f ust. 3 ustawy -
            kwota pozostała do zapłaty. W przypadku faktur korygujących
            - korekta kwoty wynikającej z faktury korygowanej. W
            przypadku, o którym mowa w art. 106j ust. 3 ustawy - korekta
            kwot wynikających z faktur korygowanych
        :ivar kurs_waluty_z: Kurs waluty stosowany do wyliczenia kwoty
            podatku w przypadkach, o których mowa w dziale VI ustawy na
            fakturach, o których mowa w art. 106b ust. 1 pkt 4 ustawy
        :ivar adnotacje: Inne adnotacje na fakturze
        :ivar rodzaj_faktury: Rodzaj faktury
        :ivar przyczyna_korekty: Przyczyna korekty dla faktur
            korygujących
        :ivar typ_korekty: Typ skutku korekty w ewidencji dla podatku od
            towarów i usług
        :ivar dane_fa_korygowanej: Dane faktury korygowanej
        :ivar okres_fa_korygowanej: Dla faktury korygującej, o której
            mowa w art. 106j ust. 3 ustawy - okres, do którego odnosi
            się udzielany opust lub udzielana obniżka, w przypadku gdy
            podatnik udziela opustu lub obniżki ceny w odniesieniu do
            dostaw towarów lub usług dokonanych lub świadczonych na
            rzecz jednego odbiorcy w danym okresie
        :ivar nr_fa_korygowany: Poprawny numer faktury korygowanej w
            przypadku, gdy przyczyną korekty jest błędny numer faktury
            korygowanej. W takim przypadku błędny numer faktury należy
            wskazać w polu NrFaKorygowanej
        :ivar podmiot1_k: W przypadku korekty danych sprzedawcy należy
            podać pełne dane sprzedawcy występujące na fakturze
            korygowanej. Pole nie dotyczy przypadku korekty błędnego NIP
            występującego na fakturze pierwotnej - wówczas wymagana jest
            korekta faktury do wartości zerowych
        :ivar podmiot2_k: W przypadku korekty danych nabywcy
            występującego jako Podmiot2 lub dodatkowego nabywcy
            występującego jako Podmiot3 należy podać pełne dane tego
            podmiotu występujące na fakturze korygowanej. Korekcie nie
            podlegają błędne numery NIP identyfikujące nabywcę oraz
            dodatkowego nabywcę - wówczas wymagana jest korekta faktury
            do wartości zerowych. W przypadku korygowania pozostałych
            danych nabywcy lub dodatkowego nabywcy wskazany numer
            identyfikacyjny ma być tożsamy z numerem w części Podmiot2
            względnie Podmiot3 faktury korygującej
        :ivar p_15_zk: W przypadku korekt faktur zaliczkowych - kwota
            zapłaty przed korektą. W przypadku korekt faktur, o których
            mowa w art. 106f ust. 3 ustawy - kwota pozostała do zapłaty
            przed korektą
        :ivar kurs_waluty_zk: Kurs waluty stosowany do wyliczenia kwoty
            podatku w przypadkach, o których mowa w dziale VI ustawy
            przed korektą
        :ivar zaliczka_czesciowa: Dane dla przypadków faktur
            dokumentujących otrzymanie więcej niż jednej płatności, o
            której mowa w art. 106b ust. 1 pkt 4 ustawy. W przypadku,
            gdy faktura, o której mowa w art. 106f ust. 3 ustawy
            dokumentuje jednocześnie otrzymanie części zapłaty przed
            dokonaniem czynności, różnica kwoty w polu P_15 i sumy
            poszczególnych pól P_15Z stanowi kwotę pozostałą ponad
            płatności otrzymane przed wykonaniem czynności
            udokumentowanej fakturą
        :ivar fp: Faktura, o której mowa w art. 109 ust. 3d ustawy
        :ivar tp: Istniejące powiązania między nabywcą a dokonującym
            dostawy towarów lub usługodawcą, zgodnie z § 10 ust. 4 pkt
            3, z zastrzeżeniem ust. 4b rozporządzenia w sprawie
            szczegółowego zakresu danych zawartych w deklaracjach
            podatkowych i w ewidencji w zakresie podatku od towarów i
            usług
        :ivar dodatkowy_opis: Pola przeznaczone dla wykazywania
            dodatkowych danych na fakturze, w tym wymaganych przepisami
            prawa, dla których nie przewidziano innych pól/elementów
        :ivar faktura_zaliczkowa: Numery faktur zaliczkowych lub ich
            numery KSeF, jeśli zostały wystawione z użyciem KSeF
        :ivar zwrot_akcyzy: Informacja dodatkowa niezbędna dla rolników
            ubiegających się o zwrot podatku akcyzowego zawartego w
            cenie oleju napędowego
        :ivar fa_wiersz: Szczegółowe pozycje faktury w walucie, w której
            wystawiono fakturę - węzeł opcjonalny dla faktury
            zaliczkowej, faktury korygującej fakturę zaliczkową oraz
            faktur korygujących dotyczących wszystkich dostaw towarów
            lub usług dokonanych lub świadczonych w danym okresie, o
            których mowa w art. 106j ust. 3 ustawy, dla których należy
            podać dane dotyczące opustu lub obniżki w podziale na stawki
            podatku i procedury w części Fa. W przypadku faktur
            korygujących, o których mowa w art. 106j ust. 3 ustawy, gdy
            opust lub obniżka ceny odnosi się do części dostaw towarów
            lub usług dokonanych lub świadczonych w danym okresie w
            części FaWiersz należy podać nazwy (rodzaje) towarów lub
            usług objętych korektą. W przypadku faktur, o których mowa w
            art. 106f ust. 3 ustawy, należy wykazać pełne wartości
            zamówienia lub umowy. W przypadku faktur korygujących
            pozycje faktury (w tym faktur korygujących faktury, o
            których mowa w art. 106f ust. 3 ustawy, jeśli korekta
            dotyczy wartości zamówienia) należy wykazać różnice
            wynikające z korekty poszczególnych pozycji lub dane pozycji
            korygowanych wg stanu przed korektą i po korekcie jako
            osobne wiersze. W przypadku faktur korygujących faktury, o
            których mowa w art. 106f ust. 3 ustawy, jeśli korekta nie
            dotyczy wartości zamówienia i jednocześnie zmienia wysokość
            podstawy opodatkowania lub podatku, należy wprowadzić zapis
            wg stanu przed korektą i zapis wg stanu po korekcie w celu
            potwierdzenia braku zmiany wartości danej pozycji faktury
        :ivar rozliczenie: Dodatkowe rozliczenia na fakturze
        :ivar platnosc: Warunki płatności
        :ivar warunki_transakcji: Warunki transakcji, o ile występują
        :ivar zamowienie: Zamówienie lub umowa, o których mowa w art.
            106f ust. 1 pkt 4 ustawy (dla faktur zaliczkowych), w
            walucie, w której wystawiono fakturę zaliczkową. W przypadku
            faktury korygującej fakturę zaliczkową należy wykazać
            różnice wynikające z korekty poszczególnych pozycji
            zamówienia lub umowy lub dane pozycji korygowanych wg stanu
            przed korektą i po korekcie jako osobne wiersze, jeśli
            korekta dotyczy wartości zamówienia lub umowy. W przypadku
            faktur korygujących faktury zaliczkowe, jeśli korekta nie
            dotyczy wartości zamówienia lub umowy i jednocześnie zmienia
            wysokość podstawy opodatkowania lub podatku, należy
            wprowadzić zapis wg stanu przed korektą i zapis wg stanu po
            korekcie w celu potwierdzenia braku zmiany wartości danej
            pozycji
        """

        kod_waluty: TkodWaluty = field(
            metadata={
                "name": "KodWaluty",
                "type": "Element",
                "required": True,
            }
        )
        p_1: str = field(
            metadata={
                "name": "P_1",
                "type": "Element",
                "required": True,
                "min_inclusive": "2006-01-01",
                "max_inclusive": "2050-01-01",
                "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
            }
        )
        p_1_m: None | str = field(
            default=None,
            metadata={
                "name": "P_1M",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        p_2: str = field(
            metadata={
                "name": "P_2",
                "type": "Element",
                "required": True,
                "min_length": 1,
                "max_length": 256,
            }
        )
        wz: list[str] = field(
            default_factory=list,
            metadata={
                "name": "WZ",
                "type": "Element",
                "max_occurs": 1000,
                "min_length": 1,
                "max_length": 256,
            },
        )
        p_6: None | str = field(
            default=None,
            metadata={
                "name": "P_6",
                "type": "Element",
                "min_inclusive": "2006-01-01",
                "max_inclusive": "2050-01-01",
                "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
            },
        )
        okres_fa: None | Faktura.Fa.OkresFa = field(
            default=None,
            metadata={
                "name": "OkresFa",
                "type": "Element",
            },
        )
        p_13_1: None | str = field(
            default=None,
            metadata={
                "name": "P_13_1",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_1: None | str = field(
            default=None,
            metadata={
                "name": "P_14_1",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_1_w: None | str = field(
            default=None,
            metadata={
                "name": "P_14_1W",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_2: None | str = field(
            default=None,
            metadata={
                "name": "P_13_2",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_2: None | str = field(
            default=None,
            metadata={
                "name": "P_14_2",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_2_w: None | str = field(
            default=None,
            metadata={
                "name": "P_14_2W",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_3: None | str = field(
            default=None,
            metadata={
                "name": "P_13_3",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_3: None | str = field(
            default=None,
            metadata={
                "name": "P_14_3",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_3_w: None | str = field(
            default=None,
            metadata={
                "name": "P_14_3W",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_4: None | str = field(
            default=None,
            metadata={
                "name": "P_13_4",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_4: None | str = field(
            default=None,
            metadata={
                "name": "P_14_4",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_4_w: None | str = field(
            default=None,
            metadata={
                "name": "P_14_4W",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_5: None | str = field(
            default=None,
            metadata={
                "name": "P_13_5",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_14_5: None | str = field(
            default=None,
            metadata={
                "name": "P_14_5",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_6_1: None | str = field(
            default=None,
            metadata={
                "name": "P_13_6_1",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_6_2: None | str = field(
            default=None,
            metadata={
                "name": "P_13_6_2",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_6_3: None | str = field(
            default=None,
            metadata={
                "name": "P_13_6_3",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_7: None | str = field(
            default=None,
            metadata={
                "name": "P_13_7",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_8: None | str = field(
            default=None,
            metadata={
                "name": "P_13_8",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_9: None | str = field(
            default=None,
            metadata={
                "name": "P_13_9",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_10: None | str = field(
            default=None,
            metadata={
                "name": "P_13_10",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_13_11: None | str = field(
            default=None,
            metadata={
                "name": "P_13_11",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        p_15: str = field(
            metadata={
                "name": "P_15",
                "type": "Element",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            }
        )
        kurs_waluty_z: None | str = field(
            default=None,
            metadata={
                "name": "KursWalutyZ",
                "type": "Element",
                "total_digits": 22,
                "fraction_digits": 6,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
            },
        )
        adnotacje: Faktura.Fa.Adnotacje = field(
            metadata={
                "name": "Adnotacje",
                "type": "Element",
                "required": True,
            }
        )
        rodzaj_faktury: TrodzajFaktury = field(
            metadata={
                "name": "RodzajFaktury",
                "type": "Element",
                "required": True,
            }
        )
        przyczyna_korekty: None | str = field(
            default=None,
            metadata={
                "name": "PrzyczynaKorekty",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        typ_korekty: None | TtypKorekty = field(
            default=None,
            metadata={
                "name": "TypKorekty",
                "type": "Element",
            },
        )
        dane_fa_korygowanej: list[Faktura.Fa.DaneFaKorygowanej] = field(
            default_factory=list,
            metadata={
                "name": "DaneFaKorygowanej",
                "type": "Element",
                "max_occurs": 50000,
            },
        )
        okres_fa_korygowanej: None | str = field(
            default=None,
            metadata={
                "name": "OkresFaKorygowanej",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        nr_fa_korygowany: None | str = field(
            default=None,
            metadata={
                "name": "NrFaKorygowany",
                "type": "Element",
                "min_length": 1,
                "max_length": 256,
            },
        )
        podmiot1_k: None | Faktura.Fa.Podmiot1K = field(
            default=None,
            metadata={
                "name": "Podmiot1K",
                "type": "Element",
            },
        )
        podmiot2_k: list[Faktura.Fa.Podmiot2K] = field(
            default_factory=list,
            metadata={
                "name": "Podmiot2K",
                "type": "Element",
                "max_occurs": 101,
            },
        )
        p_15_zk: None | str = field(
            default=None,
            metadata={
                "name": "P_15ZK",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
            },
        )
        kurs_waluty_zk: None | str = field(
            default=None,
            metadata={
                "name": "KursWalutyZK",
                "type": "Element",
                "total_digits": 22,
                "fraction_digits": 6,
                "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
            },
        )
        zaliczka_czesciowa: list[Faktura.Fa.ZaliczkaCzesciowa] = field(
            default_factory=list,
            metadata={
                "name": "ZaliczkaCzesciowa",
                "type": "Element",
                "max_occurs": 31,
            },
        )
        fp: None | Twybor1 = field(
            default=None,
            metadata={
                "name": "FP",
                "type": "Element",
            },
        )
        tp: None | Twybor1 = field(
            default=None,
            metadata={
                "name": "TP",
                "type": "Element",
            },
        )
        dodatkowy_opis: list[TkluczWartosc] = field(
            default_factory=list,
            metadata={
                "name": "DodatkowyOpis",
                "type": "Element",
                "max_occurs": 10000,
            },
        )
        faktura_zaliczkowa: list[Faktura.Fa.FakturaZaliczkowa] = field(
            default_factory=list,
            metadata={
                "name": "FakturaZaliczkowa",
                "type": "Element",
                "max_occurs": 100,
            },
        )
        zwrot_akcyzy: None | Twybor1 = field(
            default=None,
            metadata={
                "name": "ZwrotAkcyzy",
                "type": "Element",
            },
        )
        fa_wiersz: list[Faktura.Fa.FaWiersz] = field(
            default_factory=list,
            metadata={
                "name": "FaWiersz",
                "type": "Element",
                "max_occurs": 10000,
            },
        )
        rozliczenie: None | Faktura.Fa.Rozliczenie = field(
            default=None,
            metadata={
                "name": "Rozliczenie",
                "type": "Element",
            },
        )
        platnosc: None | Faktura.Fa.Platnosc = field(
            default=None,
            metadata={
                "name": "Platnosc",
                "type": "Element",
            },
        )
        warunki_transakcji: None | Faktura.Fa.WarunkiTransakcji = field(
            default=None,
            metadata={
                "name": "WarunkiTransakcji",
                "type": "Element",
            },
        )
        zamowienie: None | Faktura.Fa.Zamowienie = field(
            default=None,
            metadata={
                "name": "Zamowienie",
                "type": "Element",
            },
        )

        @dataclass(kw_only=True)
        class Adnotacje:
            """
            :ivar p_16: W przypadku dostawy towarów lub świadczenia
                usług, w odniesieniu do których obowiązek podatkowy
                powstaje zgodnie z art. 19a ust. 5 pkt 1 lub art. 21
                ust. 1 ustawy - wyrazy "metoda kasowa"; należy podać
                wartość "1", w przeciwnym przypadku - wartość "2"
            :ivar p_17: W przypadku faktur, o których mowa w art. 106d
                ust. 1 ustawy - wyraz "samofakturowanie"; należy podać
                wartość "1", w przeciwnym przypadku - wartość "2"
            :ivar p_18: W przypadku dostawy towarów lub wykonania
                usługi, dla których obowiązanym do rozliczenia podatku
                od wartości dodanej lub podatku o podobnym charakterze
                jest nabywca towaru lub usługi - wyrazy "odwrotne
                obciążenie"; należy podać wartość "1", w przeciwnym
                przypadku - wartość "2"
            :ivar p_18_a: W przypadku faktur, w których kwota należności
                ogółem przekracza kwotę 15 000 zł lub jej równowartość
                wyrażoną w walucie obcej, obejmujących dokonaną na rzecz
                podatnika dostawę towarów lub świadczenie usług, o
                których mowa w załączniku nr 15 do ustawy - wyrazy
                "mechanizm podzielonej płatności", przy czym do
                przeliczania na złote kwot wyrażonych w walucie obcej
                stosuje się zasady przeliczania kwot stosowane w celu
                określenia podstawy opodatkowania; należy podać wartość
                "1", w przeciwnym przypadku - wartość "2"
            :ivar zwolnienie:
            :ivar nowe_srodki_transportu:
            :ivar p_23: W przypadku faktur wystawianych w procedurze
                uproszczonej przez drugiego w kolejności podatnika, o
                którym mowa w art. 135 ust. 1 pkt 4 lit. b i c oraz ust.
                2 ustawy, zawierającej adnotację, o której mowa w art.
                136 ust. 1 pkt 1 ustawy i stwierdzenie, o którym mowa w
                art. 136 ust. 1 pkt 2 ustawy, należy podać wartość "1",
                w przeciwnym przypadku - wartość "2"
            :ivar pmarzy:
            """

            p_16: Twybor12 = field(
                metadata={
                    "name": "P_16",
                    "type": "Element",
                    "required": True,
                }
            )
            p_17: Twybor12 = field(
                metadata={
                    "name": "P_17",
                    "type": "Element",
                    "required": True,
                }
            )
            p_18: Twybor12 = field(
                metadata={
                    "name": "P_18",
                    "type": "Element",
                    "required": True,
                }
            )
            p_18_a: Twybor12 = field(
                metadata={
                    "name": "P_18A",
                    "type": "Element",
                    "required": True,
                }
            )
            zwolnienie: Faktura.Fa.Adnotacje.Zwolnienie = field(
                metadata={
                    "name": "Zwolnienie",
                    "type": "Element",
                    "required": True,
                }
            )
            nowe_srodki_transportu: Faktura.Fa.Adnotacje.NoweSrodkiTransportu = field(
                metadata={
                    "name": "NoweSrodkiTransportu",
                    "type": "Element",
                    "required": True,
                }
            )
            p_23: Twybor12 = field(
                metadata={
                    "name": "P_23",
                    "type": "Element",
                    "required": True,
                }
            )
            pmarzy: Faktura.Fa.Adnotacje.Pmarzy = field(
                metadata={
                    "name": "PMarzy",
                    "type": "Element",
                    "required": True,
                }
            )

            @dataclass(kw_only=True)
            class Zwolnienie:
                """
                :ivar p_19: Znacznik dostawy towarów lub świadczenia
                    usług zwolnionych od podatku na podstawie art. 43
                    ust. 1 ustawy, art. 113 ust. 1 i 9 ustawy albo
                    przepisów wydanych na podstawie art. 82 ust. 3
                    ustawy lub na podstawie innych przepisów
                :ivar p_19_a: Jeśli pole P_19 równa się "1" - należy
                    wskazać przepis ustawy albo aktu wydanego na
                    podstawie ustawy, na podstawie którego podatnik
                    stosuje zwolnienie od podatku
                :ivar p_19_b: Jeśli pole P_19 równa się "1" - należy
                    wskazać przepis dyrektywy 2006/112/WE, który zwalnia
                    od podatku taką dostawę towarów lub takie
                    świadczenie usług
                :ivar p_19_c: Jeśli pole P_19 równa się "1" - należy
                    wskazać inną podstawę prawną wskazującą na to, że
                    dostawa towarów lub świadczenie usług korzysta ze
                    zwolnienia od podatku
                :ivar p_19_n: Znacznik braku dostawy towarów lub
                    świadczenia usług zwolnionych od podatku na
                    podstawie art. 43 ust. 1 ustawy, art. 113 ust. 1 i 9
                    ustawy albo przepisów wydanych na podstawie art. 82
                    ust. 3 ustawy lub na podstawie innych przepisów
                """

                p_19: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_19",
                        "type": "Element",
                    },
                )
                p_19_a: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_19A",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )
                p_19_b: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_19B",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )
                p_19_c: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_19C",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )
                p_19_n: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_19N",
                        "type": "Element",
                    },
                )

            @dataclass(kw_only=True)
            class NoweSrodkiTransportu:
                """
                :ivar p_22: Znacznik wewnątrzwspólnotowej dostawy nowych
                    środków transportu
                :ivar p_42_5: Jeśli występuje obowiązek, o którym mowa w
                    art. 42 ust. 5 ustawy, należy podać wartość "1", w
                    przeciwnym przypadku - wartość "2"
                :ivar nowy_srodek_transportu:
                :ivar p_22_n: Znacznik braku wewnątrzwspólnotowej
                    dostawy nowych środków transportu
                """

                p_22: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_22",
                        "type": "Element",
                    },
                )
                p_42_5: None | Twybor12 = field(
                    default=None,
                    metadata={
                        "name": "P_42_5",
                        "type": "Element",
                    },
                )
                nowy_srodek_transportu: list[
                    Faktura.Fa.Adnotacje.NoweSrodkiTransportu.NowySrodekTransportu
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "NowySrodekTransportu",
                        "type": "Element",
                        "max_occurs": 10000,
                    },
                )
                p_22_n: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_22N",
                        "type": "Element",
                    },
                )

                @dataclass(kw_only=True)
                class NowySrodekTransportu:
                    """
                    :ivar p_22_a: Data dopuszczenia nowego środka
                        transportu do użytku
                    :ivar p_nr_wiersza_nst: Numer wiersza faktury, w
                        którym wykazano dostawę nowego środka transportu
                    :ivar p_22_bmk: Marka nowego środka transportu
                    :ivar p_22_bmd: Model nowego środka transportu
                    :ivar p_22_bk: Kolor nowego środka transportu
                    :ivar p_22_bnr: Numer rejestracyjny nowego środka
                        transportu
                    :ivar p_22_brp: Rok produkcji nowego środka
                        transportu
                    :ivar p_22_b: Jeśli dostawa dotyczy pojazdów
                        lądowych, o których mowa w art. 2 pkt 10 lit. a
                        ustawy, należy podać przebieg pojazdu
                    :ivar p_22_b1: Jeśli dostawa dotyczy pojazdów
                        lądowych, o których mowa w art. 2 pkt 10 lit. a
                        ustawy, można podać numer VIN
                    :ivar p_22_b2: Jeśli dostawa dotyczy pojazdów
                        lądowych, o których mowa w art. 2 pkt 10 lit. a
                        ustawy, można podać numer nadwozia
                    :ivar p_22_b3: Jeśli dostawa dotyczy pojazdów
                        lądowych, o których mowa w art. 2 pkt 10 lit. a
                        ustawy, można podać numer podwozia
                    :ivar p_22_b4: Jeśli dostawa dotyczy pojazdów
                        lądowych, o których mowa w art. 2 pkt 10 lit. a
                        ustawy, można podać numer ramy
                    :ivar p_22_bt: Jeśli dostawa dotyczy pojazdów
                        lądowych, o których mowa w art. 2 pkt 10 lit. a
                        ustawy, można podać typ nowego środka transportu
                    :ivar p_22_c: Jeśli dostawa dotyczy jednostek
                        pływających, o których mowa w art. 2 pkt 10 lit.
                        b ustawy, należy podać liczbę godzin roboczych
                        używania nowego środka transportu
                    :ivar p_22_c1: Jeśli dostawa dotyczy jednostek
                        pływających, o których mowa w art. 2 pkt 10 lit.
                        b ustawy, można podać numer kadłuba nowego
                        środka transportu
                    :ivar p_22_d: Jeśli dostawa dotyczy statków
                        powietrznych, o których mowa w art. 2 pkt 10
                        lit. c ustawy, należy podać liczbę godzin
                        roboczych używania nowego środka transportu
                    :ivar p_22_d1: Jeśli dostawa dotyczy statków
                        powietrznych, o których mowa w art. 2 pkt 10
                        lit. c ustawy, można podać numer fabryczny
                        nowego środka transportu
                    """

                    p_22_a: str = field(
                        metadata={
                            "name": "P_22A",
                            "type": "Element",
                            "required": True,
                            "min_inclusive": "2006-01-01",
                            "max_inclusive": "2050-01-01",
                            "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                        }
                    )
                    p_nr_wiersza_nst: int = field(
                        metadata={
                            "name": "P_NrWierszaNST",
                            "type": "Element",
                            "required": True,
                            "min_exclusive": 0,
                            "total_digits": 14,
                            "white_space": "collapse",
                        }
                    )
                    p_22_bmk: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22BMK",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_bmd: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22BMD",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_bk: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22BK",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_bnr: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22BNR",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_brp: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22BRP",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_b: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22B",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_b1: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22B1",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_b2: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22B2",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_b3: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22B3",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_b4: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22B4",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_bt: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22BT",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_c: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22C",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_c1: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22C1",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_d: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22D",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )
                    p_22_d1: None | str = field(
                        default=None,
                        metadata={
                            "name": "P_22D1",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 256,
                        },
                    )

            @dataclass(kw_only=True)
            class Pmarzy:
                """
                :ivar p_pmarzy: Znacznik wystąpienia procedur marży, o
                    których mowa w art. 119 lub art. 120 ustawy
                :ivar p_pmarzy_2: Znacznik świadczenia usług turystyki,
                    dla których podstawę opodatkowania stanowi marża,
                    zgodnie z art. 119 ust. 1 ustawy, a faktura
                    dokumentująca świadczenie zawiera wyrazy "procedura
                    marży dla biur podróży"
                :ivar p_pmarzy_3_1: Znacznik dostawy towarów używanych,
                    dla których podstawę opodatkowania stanowi marża,
                    zgodnie z art. 120 ustawy, a faktura dokumentująca
                    dostawę zawiera wyrazy "procedura marży - towary
                    używane"
                :ivar p_pmarzy_3_2: Znacznik dostawy dzieł sztuki, dla
                    których podstawę opodatkowania stanowi marża,
                    zgodnie z art. 120 ustawy, a faktura dokumentująca
                    dostawę zawiera wyrazy "procedura marży - dzieła
                    sztuki"
                :ivar p_pmarzy_3_3: Znacznik dostawy przedmiotów
                    kolekcjonerskich i antyków, dla których podstawę
                    opodatkowania stanowi marża, zgodnie z art. 120
                    ustawy, a faktura dokumentująca dostawę zawiera
                    wyrazy "procedura marży - przedmioty kolekcjonerskie
                    i antyki"
                :ivar p_pmarzy_n: Znacznik braku wystąpienia procedur
                    marży, o których mowa w art. 119 lub art. 120 ustawy
                """

                p_pmarzy: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_PMarzy",
                        "type": "Element",
                    },
                )
                p_pmarzy_2: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_PMarzy_2",
                        "type": "Element",
                    },
                )
                p_pmarzy_3_1: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_PMarzy_3_1",
                        "type": "Element",
                    },
                )
                p_pmarzy_3_2: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_PMarzy_3_2",
                        "type": "Element",
                    },
                )
                p_pmarzy_3_3: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_PMarzy_3_3",
                        "type": "Element",
                    },
                )
                p_pmarzy_n: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_PMarzyN",
                        "type": "Element",
                    },
                )

        @dataclass(kw_only=True)
        class ZaliczkaCzesciowa:
            """
            :ivar p_6_z: Data otrzymania płatności, o której mowa w art.
                106b ust. 1 pkt 4 ustawy
            :ivar p_15_z: Kwota płatności, o której mowa w art. 106b
                ust. 1 pkt 4 ustawy, składająca się na kwotę w polu
                P_15. W przypadku faktur korygujących  - korekta kwoty
                wynikającej z faktury korygowanej
            :ivar kurs_waluty_zw: Kurs waluty stosowany do wyliczenia
                kwoty podatku w przypadkach, o których mowa w dziale VI
                ustawy
            """

            p_6_z: str = field(
                metadata={
                    "name": "P_6Z",
                    "type": "Element",
                    "required": True,
                    "min_inclusive": "2006-01-01",
                    "max_inclusive": "2050-01-01",
                    "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                }
            )
            p_15_z: str = field(
                metadata={
                    "name": "P_15Z",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                }
            )
            kurs_waluty_zw: None | str = field(
                default=None,
                metadata={
                    "name": "KursWalutyZW",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 6,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
                },
            )

        @dataclass(kw_only=True)
        class FakturaZaliczkowa:
            """
            :ivar nr_kse_fzn: Znacznik faktury zaliczkowej wystawionej
                poza KSeF
            :ivar nr_fa_zaliczkowej: Numer faktury zaliczkowej
                wystawionej poza KSeF. Pole obowiązkowe dla faktury
                wystawianej po wydaniu towaru lub wykonaniu usługi, o
                której mowa w art. 106f ust. 3 ustawy i ostatniej z
                faktur, o której mowa w art. 106f ust. 4 ustawy
            :ivar nr_kse_ffa_zaliczkowej: Numer identyfikujący fakturę
                zaliczkową w KSeF. Pole obowiązkowe w przypadku, gdy
                faktura zaliczkowa była wystawiona za pomocą KSeF
            """

            nr_kse_fzn: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "NrKSeFZN",
                    "type": "Element",
                },
            )
            nr_fa_zaliczkowej: None | str = field(
                default=None,
                metadata={
                    "name": "NrFaZaliczkowej",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 256,
                },
            )
            nr_kse_ffa_zaliczkowej: None | str = field(
                default=None,
                metadata={
                    "name": "NrKSeFFaZaliczkowej",
                    "type": "Element",
                    "pattern": r"([1-9]((\d[1-9])|([1-9]\d))\d{7}|M\d{9}|[A-Z]{3}\d{7})-(20[2-9][0-9]|2[1-9][0-9]{2}|[3-9][0-9]{3})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])-([0-9A-F]{6})-?([0-9A-F]{6})-([0-9A-F]{2})",
                },
            )

        @dataclass(kw_only=True)
        class FaWiersz:
            """
            :ivar nr_wiersza_fa: Kolejny numer wiersza faktury
            :ivar uu_id: Uniwersalny unikalny numer wiersza faktury
            :ivar p_6_a: Data dokonania lub zakończenia dostawy towarów
                lub wykonania usługi lub data otrzymania zapłaty, o
                której mowa w art. 106b ust. 1 pkt 4 ustawy, o ile taka
                data jest określona i różni się od daty wystawienia
                faktury. Pole wypełnia się w przypadku gdy dla
                poszczególnych pozycji faktury występują różne daty
            :ivar p_7: Nazwa (rodzaj) towaru lub usługi. Pole opcjonalne
                wyłącznie dla przypadku określonego w art 106j ust. 3
                pkt 2 ustawy (faktura korygująca)
            :ivar indeks: Pole przeznaczone do wpisania wewnętrznego
                kodu towaru lub usługi nadanego przez podatnika albo
                dodatkowego opisu
            :ivar gtin: Globalny numer jednostki handlowej
            :ivar pkwi_u: Symbol Polskiej Klasyfikacji Wyrobów i Usług
            :ivar cn: Symbol Nomenklatury Scalonej
            :ivar pkob: Symbol Polskiej Klasyfikacji Obiektów
                Budowlanych
            :ivar p_8_a: Miara dostarczonych towarów lub zakres
                wykonanych usług. Pole opcjonalne dla przypadku
                określonego w art. 106e ust. 5 pkt 3 ustawy
            :ivar p_8_b: Ilość (liczba) dostarczonych towarów lub zakres
                wykonanych usług. Pole opcjonalne dla przypadku
                określonego w art. 106e ust. 5 pkt 3 ustawy
            :ivar p_9_a: Cena jednostkowa towaru lub usługi bez kwoty
                podatku (cena jednostkowa netto). Pole opcjonalne dla
                przypadków określonych w art. 106e ust. 2 i 3 oraz ust.
                5 pkt 3 ustawy
            :ivar p_9_b: Cena wraz z kwotą podatku (cena jednostkowa
                brutto), w przypadku zastosowania art. 106e ust. 7 i 8
                ustawy
            :ivar p_10: Kwoty wszelkich opustów lub obniżek cen, w tym w
                formie rabatu z tytułu wcześniejszej zapłaty, o ile nie
                zostały one uwzględnione w cenie jednostkowej netto, a w
                przypadku stosowania art. 106e ust. 7 ustawy w cenie
                jednostkowej brutto. Pole opcjonalne dla przypadków
                określonych w art. 106e ust. 2 i 3 oraz ust. 5 pkt 1
                ustawy
            :ivar p_11: Wartość dostarczonych towarów lub wykonanych
                usług, objętych transakcją, bez kwoty podatku (wartość
                sprzedaży netto). Pole opcjonalne dla przypadków
                określonych w art. 106e ust. 2 i 3 oraz ust. 5 pkt 3
                ustawy
            :ivar p_11_a: Wartość sprzedaży brutto, w przypadku
                zastosowania art. 106e ust. 7 i 8 ustawy
            :ivar p_11_vat: Kwota podatku w przypadku, o którym mowa w
                art. 106e ust. 10 ustawy
            :ivar p_12: Stawka podatku. Pole opcjonalne dla przypadków
                określonych w art. 106e ust. 2, 3, ust. 4 pkt 3 i ust. 5
                pkt 3 ustawy
            :ivar p_12_xii: Stawka podatku od wartości dodanej w
                przypadku, o którym mowa w dziale XII w rozdziale 6a
                ustawy
            :ivar p_12_zal_15: Znacznik dla towaru lub usługi
                wymienionych w załączniku nr 15 do ustawy - wartość "1"
            :ivar kwota_akcyzy: Kwota podatku akcyzowego zawarta w cenie
                towaru
            :ivar gtu: Oznaczenie dotyczące dostawy towarów i
                świadczenia usług
            :ivar procedura: Oznaczenie dotyczące procedury
            :ivar kurs_waluty: Kurs waluty stosowany do wyliczenia kwoty
                podatku w przypadkach, o których mowa w dziale VI ustawy
            :ivar stan_przed: Znacznik stanu przed korektą w przypadku
                faktury korygującej lub faktury korygującej fakturę
                wystawioną w związku z art. 106f ust. 3 ustawy, w
                przypadku gdy korekta dotyczy danych wykazanych w
                pozycjach faktury i jest dokonywana w sposób polegający
                na wykazaniu danych przed korektą i po korekcie jako
                osobnych wierszy z odrębną numeracją oraz w przypadku
                potwierdzania braku zmiany wartości danej pozycji
            """

            nr_wiersza_fa: int = field(
                metadata={
                    "name": "NrWierszaFa",
                    "type": "Element",
                    "required": True,
                    "min_exclusive": 0,
                    "total_digits": 14,
                    "white_space": "collapse",
                }
            )
            uu_id: None | str = field(
                default=None,
                metadata={
                    "name": "UU_ID",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            p_6_a: None | str = field(
                default=None,
                metadata={
                    "name": "P_6A",
                    "type": "Element",
                    "min_inclusive": "2006-01-01",
                    "max_inclusive": "2050-01-01",
                    "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                },
            )
            p_7: None | str = field(
                default=None,
                metadata={
                    "name": "P_7",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 512,
                },
            )
            indeks: None | str = field(
                default=None,
                metadata={
                    "name": "Indeks",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            gtin: None | str = field(
                default=None,
                metadata={
                    "name": "GTIN",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 20,
                },
            )
            pkwi_u: None | str = field(
                default=None,
                metadata={
                    "name": "PKWiU",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            cn: None | str = field(
                default=None,
                metadata={
                    "name": "CN",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            pkob: None | str = field(
                default=None,
                metadata={
                    "name": "PKOB",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            p_8_a: None | str = field(
                default=None,
                metadata={
                    "name": "P_8A",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 256,
                },
            )
            p_8_b: None | str = field(
                default=None,
                metadata={
                    "name": "P_8B",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 6,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
                },
            )
            p_9_a: None | str = field(
                default=None,
                metadata={
                    "name": "P_9A",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 8,
                    "pattern": r"-?([1-9]\d{0,13}|0)(\.\d{1,8})?",
                },
            )
            p_9_b: None | str = field(
                default=None,
                metadata={
                    "name": "P_9B",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 8,
                    "pattern": r"-?([1-9]\d{0,13}|0)(\.\d{1,8})?",
                },
            )
            p_10: None | str = field(
                default=None,
                metadata={
                    "name": "P_10",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 8,
                    "pattern": r"-?([1-9]\d{0,13}|0)(\.\d{1,8})?",
                },
            )
            p_11: None | str = field(
                default=None,
                metadata={
                    "name": "P_11",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            p_11_a: None | str = field(
                default=None,
                metadata={
                    "name": "P_11A",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            p_11_vat: None | str = field(
                default=None,
                metadata={
                    "name": "P_11Vat",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            p_12: None | TstawkaPodatku = field(
                default=None,
                metadata={
                    "name": "P_12",
                    "type": "Element",
                },
            )
            p_12_xii: None | Decimal = field(
                default=None,
                metadata={
                    "name": "P_12_XII",
                    "type": "Element",
                    "min_inclusive": Decimal("0"),
                    "max_inclusive": Decimal("100"),
                    "total_digits": 9,
                    "fraction_digits": 6,
                    "white_space": "collapse",
                },
            )
            p_12_zal_15: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "P_12_Zal_15",
                    "type": "Element",
                },
            )
            kwota_akcyzy: None | str = field(
                default=None,
                metadata={
                    "name": "KwotaAkcyzy",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            gtu: None | Tgtu = field(
                default=None,
                metadata={
                    "name": "GTU",
                    "type": "Element",
                },
            )
            procedura: None | ToznaczenieProcedury = field(
                default=None,
                metadata={
                    "name": "Procedura",
                    "type": "Element",
                },
            )
            kurs_waluty: None | str = field(
                default=None,
                metadata={
                    "name": "KursWaluty",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 6,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
                },
            )
            stan_przed: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "StanPrzed",
                    "type": "Element",
                },
            )

        @dataclass(kw_only=True)
        class Rozliczenie:
            """
            :ivar obciazenia: Obciążenia
            :ivar suma_obciazen: Suma obciążeń
            :ivar odliczenia: Odliczenia
            :ivar suma_odliczen: Suma odliczeń
            :ivar do_zaplaty: Kwota należności do zapłaty równa polu
                P_15 powiększonemu o Obciazenia i pomniejszonemu o
                Odliczenia
            :ivar do_rozliczenia: Kwota nadpłacona do rozliczenia/zwrotu
            """

            obciazenia: list[Faktura.Fa.Rozliczenie.Obciazenia] = field(
                default_factory=list,
                metadata={
                    "name": "Obciazenia",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            suma_obciazen: None | str = field(
                default=None,
                metadata={
                    "name": "SumaObciazen",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            odliczenia: list[Faktura.Fa.Rozliczenie.Odliczenia] = field(
                default_factory=list,
                metadata={
                    "name": "Odliczenia",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            suma_odliczen: None | str = field(
                default=None,
                metadata={
                    "name": "SumaOdliczen",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            do_zaplaty: None | str = field(
                default=None,
                metadata={
                    "name": "DoZaplaty",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )
            do_rozliczenia: None | str = field(
                default=None,
                metadata={
                    "name": "DoRozliczenia",
                    "type": "Element",
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                },
            )

            @dataclass(kw_only=True)
            class Obciazenia:
                """
                :ivar kwota: Kwota doliczona do kwoty wykazanej w polu
                    P_15
                :ivar powod: Powód obciążenia
                """

                kwota: str = field(
                    metadata={
                        "name": "Kwota",
                        "type": "Element",
                        "required": True,
                        "total_digits": 18,
                        "fraction_digits": 2,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                    }
                )
                powod: str = field(
                    metadata={
                        "name": "Powod",
                        "type": "Element",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )

            @dataclass(kw_only=True)
            class Odliczenia:
                """
                :ivar kwota: Kwota odliczona od kwoty wykazanej w polu
                    P_15
                :ivar powod: Powód odliczenia
                """

                kwota: str = field(
                    metadata={
                        "name": "Kwota",
                        "type": "Element",
                        "required": True,
                        "total_digits": 18,
                        "fraction_digits": 2,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                    }
                )
                powod: str = field(
                    metadata={
                        "name": "Powod",
                        "type": "Element",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )

        @dataclass(kw_only=True)
        class Platnosc:
            """
            :ivar zaplacono: Znacznik informujący, że należność
                wynikająca z faktury została zapłacona: 1 - zapłacono
            :ivar data_zaplaty: Data zapłaty, jeśli do wystawienia
                faktury płatność została dokonana
            :ivar znacznik_zaplaty_czesciowej: Znacznik informujący, że
                należność wynikająca z faktury została zapłacona w
                części lub w całości:                                 1
                - zapłacono w części;                           2 -
                zapłacono w całości, jeśli należność wynikająca z
                faktury została zapłacona w dwóch lub więcej częściach,
                a ostatnia płatność jest płatnością końcową
            :ivar zaplata_czesciowa: Dane zapłat częściowych
            :ivar termin_platnosci:
            :ivar forma_platnosci: Forma płatności
            :ivar platnosc_inna: Znacznik innej formy płatności: 1 -
                inna forma płatności
            :ivar opis_platnosci: Uszczegółowienie innej formy płatności
            :ivar rachunek_bankowy: Numer rachunku
            :ivar rachunek_bankowy_faktora: Rachunek faktora
            :ivar skonto: Skonto
            :ivar link_do_platnosci: Link do płatności bezgotówkowej
            :ivar ipkse_f: Identyfikator płatności Krajowego Systemu
                e-Faktur
            """

            zaplacono: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "Zaplacono",
                    "type": "Element",
                },
            )
            data_zaplaty: None | str = field(
                default=None,
                metadata={
                    "name": "DataZaplaty",
                    "type": "Element",
                    "min_inclusive": "2016-07-01",
                    "max_inclusive": "2050-01-01",
                    "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                },
            )
            znacznik_zaplaty_czesciowej: None | Twybor12 = field(
                default=None,
                metadata={
                    "name": "ZnacznikZaplatyCzesciowej",
                    "type": "Element",
                },
            )
            zaplata_czesciowa: list[Faktura.Fa.Platnosc.ZaplataCzesciowa] = field(
                default_factory=list,
                metadata={
                    "name": "ZaplataCzesciowa",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            termin_platnosci: list[Faktura.Fa.Platnosc.TerminPlatnosci] = field(
                default_factory=list,
                metadata={
                    "name": "TerminPlatnosci",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            forma_platnosci: None | TformaPlatnosci = field(
                default=None,
                metadata={
                    "name": "FormaPlatnosci",
                    "type": "Element",
                },
            )
            platnosc_inna: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "PlatnoscInna",
                    "type": "Element",
                },
            )
            opis_platnosci: None | str = field(
                default=None,
                metadata={
                    "name": "OpisPlatnosci",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 256,
                },
            )
            rachunek_bankowy: list[TrachunekBankowy] = field(
                default_factory=list,
                metadata={
                    "name": "RachunekBankowy",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            rachunek_bankowy_faktora: list[TrachunekBankowy] = field(
                default_factory=list,
                metadata={
                    "name": "RachunekBankowyFaktora",
                    "type": "Element",
                    "max_occurs": 20,
                },
            )
            skonto: None | Faktura.Fa.Platnosc.Skonto = field(
                default=None,
                metadata={
                    "name": "Skonto",
                    "type": "Element",
                },
            )
            link_do_platnosci: None | str = field(
                default=None,
                metadata={
                    "name": "LinkDoPlatnosci",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 512,
                    "pattern": r"(https?)://([a-zA-Z0-9][a-zA-Z0-9-]*\.)+[a-zA-Z]{2,}(:[0-9]{1,5})?(/[^\s?#]*)?\?([^#\s]*&)?IPKSeF=[0-9]{3}[a-zA-Z0-9]{10}(&[^#\s]*)?(#.*)?",
                },
            )
            ipkse_f: None | str = field(
                default=None,
                metadata={
                    "name": "IPKSeF",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 13,
                    "pattern": r"[0-9]{3}[a-zA-Z0-9]{10}",
                },
            )

            @dataclass(kw_only=True)
            class TerminPlatnosci:
                """
                :ivar termin: Termin płatności
                :ivar termin_opis: Opis terminu płatności
                """

                termin: None | str = field(
                    default=None,
                    metadata={
                        "name": "Termin",
                        "type": "Element",
                        "min_inclusive": "2016-07-01",
                        "max_inclusive": "2050-01-01",
                        "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                    },
                )
                termin_opis: None | Faktura.Fa.Platnosc.TerminPlatnosci.TerminOpis = (
                    field(
                        default=None,
                        metadata={
                            "name": "TerminOpis",
                            "type": "Element",
                        },
                    )
                )

                @dataclass(kw_only=True)
                class TerminOpis:
                    ilosc: int = field(
                        metadata={
                            "name": "Ilosc",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    jednostka: str = field(
                        metadata={
                            "name": "Jednostka",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 50,
                        }
                    )
                    zdarzenie_poczatkowe: str = field(
                        metadata={
                            "name": "ZdarzeniePoczatkowe",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 256,
                        }
                    )

            @dataclass(kw_only=True)
            class Skonto:
                """
                :ivar warunki_skonta: Warunki, które nabywca powinien
                    spełnić, aby skorzystać ze skonta
                :ivar wysokosc_skonta: Wysokość skonta
                """

                warunki_skonta: str = field(
                    metadata={
                        "name": "WarunkiSkonta",
                        "type": "Element",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )
                wysokosc_skonta: str = field(
                    metadata={
                        "name": "WysokoscSkonta",
                        "type": "Element",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )

            @dataclass(kw_only=True)
            class ZaplataCzesciowa:
                """
                :ivar kwota_zaplaty_czesciowej: Kwota zapłaty częściowej
                :ivar data_zaplaty_czesciowej: Data zapłaty częściowej,
                    jeśli do wystawienia faktury płatność częściowa
                    została dokonana
                :ivar forma_platnosci: Forma płatności
                :ivar platnosc_inna: Znacznik innej formy płatności: 1 -
                    inna forma płatności
                :ivar opis_platnosci: Uszczegółowienie innej formy
                    płatności
                """

                kwota_zaplaty_czesciowej: str = field(
                    metadata={
                        "name": "KwotaZaplatyCzesciowej",
                        "type": "Element",
                        "required": True,
                        "total_digits": 18,
                        "fraction_digits": 2,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                    }
                )
                data_zaplaty_czesciowej: str = field(
                    metadata={
                        "name": "DataZaplatyCzesciowej",
                        "type": "Element",
                        "required": True,
                        "min_inclusive": "2016-07-01",
                        "max_inclusive": "2050-01-01",
                        "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                    }
                )
                forma_platnosci: None | TformaPlatnosci = field(
                    default=None,
                    metadata={
                        "name": "FormaPlatnosci",
                        "type": "Element",
                    },
                )
                platnosc_inna: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "PlatnoscInna",
                        "type": "Element",
                    },
                )
                opis_platnosci: None | str = field(
                    default=None,
                    metadata={
                        "name": "OpisPlatnosci",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )

        @dataclass(kw_only=True)
        class WarunkiTransakcji:
            """
            :ivar umowy:
            :ivar zamowienia:
            :ivar nr_partii_towaru: Numery partii towaru
            :ivar warunki_dostawy: Warunki dostawy towarów - w przypadku
                istnienia pomiędzy stronami transakcji, umowy
                określającej warunki dostawy tzw. Incoterms
            :ivar kurs_umowny: Kurs umowny - w przypadkach, gdy na
                fakturze znajduje się informacja o kursie, po którym
                zostały przeliczone kwoty wykazane na fakturze w
                złotych. Nie dotyczy przypadków, o których mowa w dziale
                VI ustawy
            :ivar waluta_umowna: Waluta umowna - kod waluty (ISO-4217) w
                przypadkach gdy na fakturze znajduje się informacja o
                kursie, po którym zostały przeliczone kwoty wykazane na
                fakturze w złotych. Nie dotyczy przypadków, o których
                mowa w dziale VI ustawy
            :ivar transport:
            :ivar podmiot_posredniczacy: Wartość "1" oznacza dostawę
                dokonaną przez podmiot, o którym mowa w art. 22 ust. 2d
                ustawy. Pole dotyczy przypadku, w którym podmiot
                uczestniczy w transakcji łańcuchowej innej niż procedura
                trójstronna uproszczona, o której mowa w art. 135 ust. 1
                pkt 4 ustawy
            """

            umowy: list[Faktura.Fa.WarunkiTransakcji.Umowy] = field(
                default_factory=list,
                metadata={
                    "name": "Umowy",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            zamowienia: list[Faktura.Fa.WarunkiTransakcji.Zamowienia] = field(
                default_factory=list,
                metadata={
                    "name": "Zamowienia",
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            nr_partii_towaru: list[str] = field(
                default_factory=list,
                metadata={
                    "name": "NrPartiiTowaru",
                    "type": "Element",
                    "max_occurs": 1000,
                    "min_length": 1,
                    "max_length": 256,
                },
            )
            warunki_dostawy: None | str = field(
                default=None,
                metadata={
                    "name": "WarunkiDostawy",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 256,
                },
            )
            kurs_umowny: None | str = field(
                default=None,
                metadata={
                    "name": "KursUmowny",
                    "type": "Element",
                    "total_digits": 22,
                    "fraction_digits": 6,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
                },
            )
            waluta_umowna: None | TkodWaluty = field(
                default=None,
                metadata={
                    "name": "WalutaUmowna",
                    "type": "Element",
                },
            )
            transport: list[Faktura.Fa.WarunkiTransakcji.Transport] = field(
                default_factory=list,
                metadata={
                    "name": "Transport",
                    "type": "Element",
                    "max_occurs": 20,
                },
            )
            podmiot_posredniczacy: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "PodmiotPosredniczacy",
                    "type": "Element",
                },
            )

            @dataclass(kw_only=True)
            class Umowy:
                """
                :ivar data_umowy: Data umowy
                :ivar nr_umowy: Numer umowy
                """

                data_umowy: None | str = field(
                    default=None,
                    metadata={
                        "name": "DataUmowy",
                        "type": "Element",
                        "min_inclusive": "1990-01-01",
                        "max_inclusive": "2050-01-01",
                        "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                    },
                )
                nr_umowy: None | str = field(
                    default=None,
                    metadata={
                        "name": "NrUmowy",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )

            @dataclass(kw_only=True)
            class Zamowienia:
                """
                :ivar data_zamowienia: Data zamówienia
                :ivar nr_zamowienia: Numer zamówienia
                """

                data_zamowienia: None | str = field(
                    default=None,
                    metadata={
                        "name": "DataZamowienia",
                        "type": "Element",
                        "min_inclusive": "1990-01-01",
                        "max_inclusive": "2050-01-01",
                        "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                    },
                )
                nr_zamowienia: None | str = field(
                    default=None,
                    metadata={
                        "name": "NrZamowienia",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )

            @dataclass(kw_only=True)
            class Transport:
                """
                :ivar rodzaj_transportu: Rodzaj zastosowanego transportu
                    w przypadku dokonanej dostawy towarów
                :ivar transport_inny: Znacznik innego rodzaju
                    transportu: 1 - inny rodzaj transportu
                :ivar opis_innego_transportu: Opis innego rodzaju
                    transportu
                :ivar przewoznik:
                :ivar nr_zlecenia_transportu: Numer zlecenia transportu
                :ivar opis_ladunku: Rodzaj ładunku
                :ivar ladunek_inny: Znacznik innego ładunku: 1 - inny
                    ładunek
                :ivar opis_innego_ladunku: Opis innego ładunku, w tym
                    ładunek mieszany
                :ivar jednostka_opakowania: Jednostka opakowania
                :ivar data_godz_rozp_transportu: Data i godzina
                    rozpoczęcia transportu
                :ivar data_godz_zak_transportu: Data i godzina
                    zakończenia transportu
                :ivar wysylka_z: Adres miejsca wysyłki
                :ivar wysylka_przez: Adres pośredni wysyłki
                :ivar wysylka_do: Adres miejsca docelowego, do którego
                    został zlecony transport
                """

                rodzaj_transportu: None | TrodzajTransportu = field(
                    default=None,
                    metadata={
                        "name": "RodzajTransportu",
                        "type": "Element",
                    },
                )
                transport_inny: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "TransportInny",
                        "type": "Element",
                    },
                )
                opis_innego_transportu: None | str = field(
                    default=None,
                    metadata={
                        "name": "OpisInnegoTransportu",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                przewoznik: None | Faktura.Fa.WarunkiTransakcji.Transport.Przewoznik = (
                    field(
                        default=None,
                        metadata={
                            "name": "Przewoznik",
                            "type": "Element",
                        },
                    )
                )
                nr_zlecenia_transportu: None | str = field(
                    default=None,
                    metadata={
                        "name": "NrZleceniaTransportu",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )
                opis_ladunku: None | Tladunek = field(
                    default=None,
                    metadata={
                        "name": "OpisLadunku",
                        "type": "Element",
                    },
                )
                ladunek_inny: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "LadunekInny",
                        "type": "Element",
                    },
                )
                opis_innego_ladunku: None | str = field(
                    default=None,
                    metadata={
                        "name": "OpisInnegoLadunku",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                jednostka_opakowania: None | str = field(
                    default=None,
                    metadata={
                        "name": "JednostkaOpakowania",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )
                data_godz_rozp_transportu: None | XmlDateTime = field(
                    default=None,
                    metadata={
                        "name": "DataGodzRozpTransportu",
                        "type": "Element",
                        "min_inclusive": XmlDateTime(2021, 10, 1, 0, 0, 0, 0, 0),
                        "max_inclusive": XmlDateTime(2050, 1, 1, 23, 59, 59, 0, 0),
                        "white_space": "collapse",
                    },
                )
                data_godz_zak_transportu: None | XmlDateTime = field(
                    default=None,
                    metadata={
                        "name": "DataGodzZakTransportu",
                        "type": "Element",
                        "min_inclusive": XmlDateTime(2021, 10, 1, 0, 0, 0, 0, 0),
                        "max_inclusive": XmlDateTime(2050, 1, 1, 23, 59, 59, 0, 0),
                        "white_space": "collapse",
                    },
                )
                wysylka_z: None | Tadres3 = field(
                    default=None,
                    metadata={
                        "name": "WysylkaZ",
                        "type": "Element",
                    },
                )
                wysylka_przez: list[Tadres3] = field(
                    default_factory=list,
                    metadata={
                        "name": "WysylkaPrzez",
                        "type": "Element",
                        "max_occurs": 20,
                    },
                )
                wysylka_do: None | Tadres3 = field(
                    default=None,
                    metadata={
                        "name": "WysylkaDo",
                        "type": "Element",
                    },
                )

                @dataclass(kw_only=True)
                class Przewoznik:
                    """
                    :ivar dane_identyfikacyjne: Dane identyfikacyjne
                        przewoźnika
                    :ivar adres_przewoznika: Adres przewoźnika
                    """

                    dane_identyfikacyjne: Tpodmiot2 = field(
                        metadata={
                            "name": "DaneIdentyfikacyjne",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    adres_przewoznika: Tadres3 = field(
                        metadata={
                            "name": "AdresPrzewoznika",
                            "type": "Element",
                            "required": True,
                        }
                    )

        @dataclass(kw_only=True)
        class Zamowienie:
            """
            :ivar wartosc_zamowienia: Wartość zamówienia lub umowy z
                uwzględnieniem kwoty podatku
            :ivar zamowienie_wiersz: Szczegółowe pozycje zamówienia lub
                umowy w walucie, w której wystawiono fakturę zaliczkową
            """

            wartosc_zamowienia: str = field(
                metadata={
                    "name": "WartoscZamowienia",
                    "type": "Element",
                    "required": True,
                    "total_digits": 18,
                    "fraction_digits": 2,
                    "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                }
            )
            zamowienie_wiersz: list[Faktura.Fa.Zamowienie.ZamowienieWiersz] = field(
                default_factory=list,
                metadata={
                    "name": "ZamowienieWiersz",
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 10000,
                },
            )

            @dataclass(kw_only=True)
            class ZamowienieWiersz:
                """
                :ivar nr_wiersza_zam: Kolejny numer wiersza zamówienia
                    lub umowy
                :ivar uu_idz: Uniwersalny unikalny numer wiersza
                    zamówienia lub umowy
                :ivar p_7_z: Nazwa (rodzaj) towaru lub usługi
                :ivar indeks_z: Pole przeznaczone do wpisania
                    wewnętrznego kodu towaru lub usługi nadanego przez
                    podatnika albo dodatkowego opisu
                :ivar gtinz: Globalny numer jednostki handlowej
                :ivar pkwi_uz: Symbol Polskiej Klasyfikacji Wyrobów i
                    Usług
                :ivar cnz: Symbol Nomenklatury Scalonej
                :ivar pkobz: Symbol Polskiej Klasyfikacji Obiektów
                    Budowlanych
                :ivar p_8_az: Miara zamówionego towaru lub zakres usługi
                :ivar p_8_bz: Ilość zamówionego towaru lub zakres usługi
                :ivar p_9_az: Cena jednostkowa netto
                :ivar p_11_netto_z: Wartość zamówionego towaru lub
                    usługi bez kwoty podatku
                :ivar p_11_vat_z: Kwota podatku od zamówionego towaru
                    lub usługi
                :ivar p_12_z: Stawka podatku
                :ivar p_12_z_xii: Stawka podatku od wartości dodanej w
                    przypadku, o którym mowa w dziale XII w rozdziale 6a
                    ustawy
                :ivar p_12_z_zal_15: Znacznik dla towaru lub usługi
                    wymienionych w załączniku nr 15 do ustawy - wartość
                    "1"
                :ivar gtuz: Oznaczenie dotyczące dostawy towarów i
                    świadczenia usług
                :ivar procedura_z: Oznaczenia dotyczące procedur
                :ivar kwota_akcyzy_z: Kwota podatku akcyzowego zawarta w
                    cenie towaru
                :ivar stan_przed_z: Znacznik stanu przed korektą w
                    przypadku faktury korygującej fakturę dokumentującą
                    otrzymanie zapłaty lub jej części przed dokonaniem
                    czynności oraz fakturę wystawioną w związku z art.
                    106f ust. 4 ustawy (faktura korygująca fakturę
                    zaliczkową), w przypadku gdy korekta dotyczy danych
                    wykazanych w pozycjach zamówienia i jest dokonywana
                    w sposób polegający na wykazaniu danych przed
                    korektą i po korekcie jako osobnych wierszy z
                    odrębną numeracją oraz w przypadku potwierdzania
                    braku zmiany wartości danej pozycji
                """

                nr_wiersza_zam: int = field(
                    metadata={
                        "name": "NrWierszaZam",
                        "type": "Element",
                        "required": True,
                        "min_exclusive": 0,
                        "total_digits": 14,
                        "white_space": "collapse",
                    }
                )
                uu_idz: None | str = field(
                    default=None,
                    metadata={
                        "name": "UU_IDZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                p_7_z: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_7Z",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 512,
                    },
                )
                indeks_z: None | str = field(
                    default=None,
                    metadata={
                        "name": "IndeksZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                gtinz: None | str = field(
                    default=None,
                    metadata={
                        "name": "GTINZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 20,
                    },
                )
                pkwi_uz: None | str = field(
                    default=None,
                    metadata={
                        "name": "PKWiUZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                cnz: None | str = field(
                    default=None,
                    metadata={
                        "name": "CNZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                pkobz: None | str = field(
                    default=None,
                    metadata={
                        "name": "PKOBZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                p_8_az: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_8AZ",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 256,
                    },
                )
                p_8_bz: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_8BZ",
                        "type": "Element",
                        "total_digits": 22,
                        "fraction_digits": 6,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,6})?",
                    },
                )
                p_9_az: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_9AZ",
                        "type": "Element",
                        "total_digits": 22,
                        "fraction_digits": 8,
                        "pattern": r"-?([1-9]\d{0,13}|0)(\.\d{1,8})?",
                    },
                )
                p_11_netto_z: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_11NettoZ",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                    },
                )
                p_11_vat_z: None | str = field(
                    default=None,
                    metadata={
                        "name": "P_11VatZ",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                    },
                )
                p_12_z: None | TstawkaPodatku = field(
                    default=None,
                    metadata={
                        "name": "P_12Z",
                        "type": "Element",
                    },
                )
                p_12_z_xii: None | Decimal = field(
                    default=None,
                    metadata={
                        "name": "P_12Z_XII",
                        "type": "Element",
                        "min_inclusive": Decimal("0"),
                        "max_inclusive": Decimal("100"),
                        "total_digits": 9,
                        "fraction_digits": 6,
                        "white_space": "collapse",
                    },
                )
                p_12_z_zal_15: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "P_12Z_Zal_15",
                        "type": "Element",
                    },
                )
                gtuz: None | Tgtu = field(
                    default=None,
                    metadata={
                        "name": "GTUZ",
                        "type": "Element",
                    },
                )
                procedura_z: None | ToznaczenieProceduryZ = field(
                    default=None,
                    metadata={
                        "name": "ProceduraZ",
                        "type": "Element",
                    },
                )
                kwota_akcyzy_z: None | str = field(
                    default=None,
                    metadata={
                        "name": "KwotaAkcyzyZ",
                        "type": "Element",
                        "total_digits": 18,
                        "fraction_digits": 2,
                        "pattern": r"-?([1-9]\d{0,15}|0)(\.\d{1,2})?",
                    },
                )
                stan_przed_z: None | Twybor1 = field(
                    default=None,
                    metadata={
                        "name": "StanPrzedZ",
                        "type": "Element",
                    },
                )

        @dataclass(kw_only=True)
        class OkresFa:
            """
            :ivar p_6_od: Data początkowa okresu, którego dotyczy
                faktura
            :ivar p_6_do: Data końcowa okresu, którego dotyczy faktura -
                data dokonania lub zakończenia dostawy towarów lub
                wykonania usługi
            """

            p_6_od: str = field(
                metadata={
                    "name": "P_6_Od",
                    "type": "Element",
                    "required": True,
                    "min_inclusive": "2006-01-01",
                    "max_inclusive": "2050-01-01",
                    "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                }
            )
            p_6_do: str = field(
                metadata={
                    "name": "P_6_Do",
                    "type": "Element",
                    "required": True,
                    "min_inclusive": "2006-01-01",
                    "max_inclusive": "2050-01-01",
                    "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                }
            )

        @dataclass(kw_only=True)
        class DaneFaKorygowanej:
            """
            :ivar data_wyst_fa_korygowanej: Data wystawienia faktury
                korygowanej
            :ivar nr_fa_korygowanej: Numer faktury korygowanej
            :ivar nr_kse_f: Znacznik numeru KSeF faktury korygowanej
            :ivar nr_kse_ffa_korygowanej: Numer identyfikujący fakturę
                korygowaną w KSeF
            :ivar nr_kse_fn: Znacznik faktury korygowanej wystawionej
                poza KSeF
            """

            data_wyst_fa_korygowanej: str = field(
                metadata={
                    "name": "DataWystFaKorygowanej",
                    "type": "Element",
                    "required": True,
                    "min_inclusive": "2006-01-01",
                    "max_inclusive": "2050-01-01",
                    "pattern": r"((\d{4})-(\d{2})-(\d{2}))",
                }
            )
            nr_fa_korygowanej: str = field(
                metadata={
                    "name": "NrFaKorygowanej",
                    "type": "Element",
                    "required": True,
                    "min_length": 1,
                    "max_length": 256,
                }
            )
            nr_kse_f: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "NrKSeF",
                    "type": "Element",
                },
            )
            nr_kse_ffa_korygowanej: None | str = field(
                default=None,
                metadata={
                    "name": "NrKSeFFaKorygowanej",
                    "type": "Element",
                    "pattern": r"([1-9]((\d[1-9])|([1-9]\d))\d{7}|M\d{9}|[A-Z]{3}\d{7})-(20[2-9][0-9]|2[1-9][0-9]{2}|[3-9][0-9]{3})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])-([0-9A-F]{6})-?([0-9A-F]{6})-([0-9A-F]{2})",
                },
            )
            nr_kse_fn: None | Twybor1 = field(
                default=None,
                metadata={
                    "name": "NrKSeFN",
                    "type": "Element",
                },
            )

        @dataclass(kw_only=True)
        class Podmiot1K:
            """
            :ivar prefiks_podatnika: Kod (prefiks) podatnika VAT UE dla
                przypadków określonych w art. 97 ust. 10 pkt 2 i 3
                ustawy oraz w przypadku, o którym mowa w art. 136 ust. 1
                pkt 3 ustawy
            :ivar dane_identyfikacyjne: Dane identyfikujące podatnika
            :ivar adres: Adres podatnika
            """

            prefiks_podatnika: None | TkodyKrajowUe = field(
                default=None,
                metadata={
                    "name": "PrefiksPodatnika",
                    "type": "Element",
                },
            )
            dane_identyfikacyjne: Tpodmiot1 = field(
                metadata={
                    "name": "DaneIdentyfikacyjne",
                    "type": "Element",
                    "required": True,
                }
            )
            adres: Tadres3 = field(
                metadata={
                    "name": "Adres",
                    "type": "Element",
                    "required": True,
                }
            )

        @dataclass(kw_only=True)
        class Podmiot2K:
            """
            :ivar dane_identyfikacyjne: Dane identyfikujące nabywcę
            :ivar adres: Adres nabywcy. Pola opcjonalne dla przypadków
                określonych w art. 106e ust. 5 pkt 3 ustawy
            :ivar idnabywcy: Unikalny klucz powiązania danych nabywcy na
                fakturach korygujących, w przypadku gdy dane nabywcy na
                fakturze korygującej zmieniły się w stosunku do danych
                na fakturze korygowanej
            """

            dane_identyfikacyjne: Tpodmiot2 = field(
                metadata={
                    "name": "DaneIdentyfikacyjne",
                    "type": "Element",
                    "required": True,
                }
            )
            adres: None | Tadres3 = field(
                default=None,
                metadata={
                    "name": "Adres",
                    "type": "Element",
                },
            )
            idnabywcy: None | str = field(
                default=None,
                metadata={
                    "name": "IDNabywcy",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 32,
                },
            )

    @dataclass(kw_only=True)
    class Stopka:
        """
        :ivar informacje: Pozostałe dane
        :ivar rejestry: Numery podmiotu lub grupy podmiotów w innych
            rejestrach i bazach danych
        """

        informacje: list[Faktura.Stopka.Informacje] = field(
            default_factory=list,
            metadata={
                "name": "Informacje",
                "type": "Element",
                "max_occurs": 3,
            },
        )
        rejestry: list[Faktura.Stopka.Rejestry] = field(
            default_factory=list,
            metadata={
                "name": "Rejestry",
                "type": "Element",
                "max_occurs": 100,
            },
        )

        @dataclass(kw_only=True)
        class Informacje:
            """
            :ivar stopka_faktury: Stopka faktury
            """

            stopka_faktury: None | str = field(
                default=None,
                metadata={
                    "name": "StopkaFaktury",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 3500,
                },
            )

        @dataclass(kw_only=True)
        class Rejestry:
            """
            :ivar pelna_nazwa: Pełna nazwa
            :ivar krs: KRS
            :ivar regon: REGON
            :ivar bdo: BDO
            """

            pelna_nazwa: None | str = field(
                default=None,
                metadata={
                    "name": "PelnaNazwa",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 256,
                },
            )
            krs: None | str = field(
                default=None,
                metadata={
                    "name": "KRS",
                    "type": "Element",
                    "pattern": r"\d{10}",
                },
            )
            regon: None | str = field(
                default=None,
                metadata={
                    "name": "REGON",
                    "type": "Element",
                    "pattern": r"\d{14}",
                },
            )
            bdo: None | str = field(
                default=None,
                metadata={
                    "name": "BDO",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 9,
                },
            )

    @dataclass(kw_only=True)
    class Zalacznik:
        """
        :ivar blok_danych: Szczegółowe dane załącznika
        """

        blok_danych: list[Faktura.Zalacznik.BlokDanych] = field(
            default_factory=list,
            metadata={
                "name": "BlokDanych",
                "type": "Element",
                "min_occurs": 1,
                "max_occurs": 1000,
            },
        )

        @dataclass(kw_only=True)
        class BlokDanych:
            """
            :ivar znaglowek: Nagłówek bloku danych
            :ivar meta_dane: Dane opisowe
            :ivar tekst: Część tekstowa bloku danych
            :ivar tabela: Tabele
            """

            znaglowek: None | str = field(
                default=None,
                metadata={
                    "name": "ZNaglowek",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 512,
                },
            )
            meta_dane: list[Faktura.Zalacznik.BlokDanych.MetaDane] = field(
                default_factory=list,
                metadata={
                    "name": "MetaDane",
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 1000,
                },
            )
            tekst: None | Faktura.Zalacznik.BlokDanych.Tekst = field(
                default=None,
                metadata={
                    "name": "Tekst",
                    "type": "Element",
                },
            )
            tabela: list[Faktura.Zalacznik.BlokDanych.Tabela] = field(
                default_factory=list,
                metadata={
                    "name": "Tabela",
                    "type": "Element",
                    "max_occurs": 1000,
                },
            )

            @dataclass(kw_only=True)
            class MetaDane:
                """
                :ivar zklucz: Klucz
                :ivar zwartosc: Wartość
                """

                zklucz: str = field(
                    metadata={
                        "name": "ZKlucz",
                        "type": "Element",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )
                zwartosc: str = field(
                    metadata={
                        "name": "ZWartosc",
                        "type": "Element",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )

            @dataclass(kw_only=True)
            class Tekst:
                """
                :ivar akapit: Opis
                """

                akapit: list[str] = field(
                    default_factory=list,
                    metadata={
                        "name": "Akapit",
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 10,
                        "min_length": 1,
                        "max_length": 512,
                    },
                )

            @dataclass(kw_only=True)
            class Tabela:
                """
                :ivar tmeta_dane: Dane opisowe dotyczące tabeli
                :ivar opis: Opis
                :ivar tnaglowek: Nagłówek tabeli
                :ivar wiersz: Wiersze tabeli
                :ivar suma: Podsumowania tabeli
                """

                tmeta_dane: list[Faktura.Zalacznik.BlokDanych.Tabela.TmetaDane] = field(
                    default_factory=list,
                    metadata={
                        "name": "TMetaDane",
                        "type": "Element",
                        "max_occurs": 1000,
                    },
                )
                opis: None | str = field(
                    default=None,
                    metadata={
                        "name": "Opis",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 512,
                    },
                )
                tnaglowek: Faktura.Zalacznik.BlokDanych.Tabela.Tnaglowek = field(
                    metadata={
                        "name": "TNaglowek",
                        "type": "Element",
                        "required": True,
                    }
                )
                wiersz: list[Faktura.Zalacznik.BlokDanych.Tabela.Wiersz] = field(
                    default_factory=list,
                    metadata={
                        "name": "Wiersz",
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 1000,
                    },
                )
                suma: None | Faktura.Zalacznik.BlokDanych.Tabela.Suma = field(
                    default=None,
                    metadata={
                        "name": "Suma",
                        "type": "Element",
                    },
                )

                @dataclass(kw_only=True)
                class TmetaDane:
                    """
                    :ivar tklucz: Klucz
                    :ivar twartosc: Wartość
                    """

                    tklucz: str = field(
                        metadata={
                            "name": "TKlucz",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 256,
                        }
                    )
                    twartosc: str = field(
                        metadata={
                            "name": "TWartosc",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 256,
                        }
                    )

                @dataclass(kw_only=True)
                class Tnaglowek:
                    kol: list[Faktura.Zalacznik.BlokDanych.Tabela.Tnaglowek.Kol] = field(
                            default_factory=list,
                            metadata={
                                "name": "Kol",
                                "type": "Element",
                                "min_occurs": 1,
                                "max_occurs": 20,
                            },
                        )
                   

                    @dataclass(kw_only=True)
                    class Kol:
                        """
                        :ivar nkom: Zawartość pola
                        :ivar typ:
                        """

                        nkom: str = field(
                            metadata={
                                "name": "NKom",
                                "type": "Element",
                                "required": True,
                                "min_length": 0,
                                "max_length": 256,
                            }
                        )
                        typ: KolTyp = field(
                            metadata={
                                "name": "Typ",
                                "type": "Attribute",
                                "required": True,
                            }
                        )

                @dataclass(kw_only=True)
                class Wiersz:
                    """
                    :ivar wkom: Zawartość pola
                    """

                    wkom: list[str] = field(
                        default_factory=list,
                        metadata={
                            "name": "WKom",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 20,
                            "min_length": 0,
                            "max_length": 256,
                        },
                    )

                @dataclass(kw_only=True)
                class Suma:
                    """
                    :ivar skom: Zawartość pola
                    """

                    skom: list[str] = field(
                        default_factory=list,
                        metadata={
                            "name": "SKom",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 20,
                            "min_length": 0,
                            "max_length": 256,
                        },
                    )


@dataclass(kw_only=True)
class Tadres1:
    """
    Dane określające adres - bez elementu Poczta w adresie polskim.
    """

    class Meta:
        name = "TAdres1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    adres_pol: None | TadresPolski1 = field(
        default=None,
        metadata={
            "name": "AdresPol",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    adres_zagr: None | TadresZagraniczny = field(
        default=None,
        metadata={
            "name": "AdresZagr",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )


@dataclass(kw_only=True)
class Tadres2:
    """
    Dane określające adres.
    """

    class Meta:
        name = "TAdres"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    adres_pol: None | TadresPolski = field(
        default=None,
        metadata={
            "name": "AdresPol",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    adres_zagr: None | TadresZagraniczny = field(
        default=None,
        metadata={
            "name": "AdresZagr",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )


@dataclass(kw_only=True)
class TosobaFizyczna:
    """
    Podstawowy zestaw danych o osobie fizycznej.
    """

    class Meta:
        name = "TOsobaFizyczna"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznej = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizyczna.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizyczna1:
    """
    Podstawowy zestaw danych o osobie fizycznej z identyfikatorem NIP albo
    PESEL.
    """

    class Meta:
        name = "TOsobaFizyczna1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznej1 = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizyczna1.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizyczna2:
    """
    Podstawowy zestaw danych o osobie fizycznej z identyfikatorem NIP.
    """

    class Meta:
        name = "TOsobaFizyczna2"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznej2 = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizyczna2.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizyczna3:
    """
    Podstawowy zestaw danych o osobie fizycznej z identyfikatorem NIP albo
    PESEL - bez elementu Poczta w adresie polskim.
    """

    class Meta:
        name = "TOsobaFizyczna3"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznej1 = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizyczna3.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizyczna4:
    """
    Podstawowy zestaw danych o osobie fizycznej z identyfikatorem NIP - bez
    elementu Poczta w adresie polskim.
    """

    class Meta:
        name = "TOsobaFizyczna4"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznej2 = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizyczna4.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizyczna5:
    """
    Podstawowy zestaw danych o osobie fizycznej - bez elementu Poczta w
    adresie polskim.
    """

    class Meta:
        name = "TOsobaFizyczna5"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznej = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizyczna5.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizycznaPelna:
    """
    Pełny zestaw danych o osobie fizycznej.
    """

    class Meta:
        name = "TOsobaFizycznaPelna"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznejPelny = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizycznaPelna.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaFizycznaPelna1:
    """
    Pełny zestaw danych o osobie fizycznej - bez elementu Poczta w adresie
    polskim.
    """

    class Meta:
        name = "TOsobaFizycznaPelna1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: TidentyfikatorOsobyFizycznejPelny = field(
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_zamieszkania: TosobaFizycznaPelna1.AdresZamieszkania = field(
        metadata={
            "name": "AdresZamieszkania",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkania(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaNiefizyczna:
    """
    Podstawowy zestaw danych o osobie niefizycznej.
    """

    class Meta:
        name = "TOsobaNiefizyczna"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_niefizyczna: TidentyfikatorOsobyNiefizycznej = field(
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_siedziby: TosobaNiefizyczna.AdresSiedziby = field(
        metadata={
            "name": "AdresSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresSiedziby(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaNiefizyczna1:
    """
    Podstawowy zestaw danych o osobie niefizycznej - bez elementu Poczta w
    adresie polskim.
    """

    class Meta:
        name = "TOsobaNiefizyczna1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_niefizyczna: TidentyfikatorOsobyNiefizycznej = field(
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_siedziby: TosobaNiefizyczna1.AdresSiedziby = field(
        metadata={
            "name": "AdresSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresSiedziby(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaNiefizyczna2:
    """
    Podstawowy zestaw danych o osobie niefizycznej - bez elementu Numer
    REGON oraz bez elementu Poczta w adresie polskim.
    """

    class Meta:
        name = "TOsobaNiefizyczna2"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_niefizyczna: TidentyfikatorOsobyNiefizycznej1 = field(
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_siedziby: TosobaNiefizyczna2.AdresSiedziby = field(
        metadata={
            "name": "AdresSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresSiedziby(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaNiefizycznaPelna:
    """
    Pełny zestaw danych o niefizycznej.
    """

    class Meta:
        name = "TOsobaNiefizycznaPelna"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_niefizyczna: TidentyfikatorOsobyNiefizycznejPelny = field(
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_siedziby: TosobaNiefizycznaPelna.AdresSiedziby = field(
        metadata={
            "name": "AdresSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresSiedziby(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TosobaNiefizycznaPelna1:
    """
    Pełny zestaw danych o osobie niefizycznej - bez elementu Poczta w
    adresie polskim.
    """

    class Meta:
        name = "TOsobaNiefizycznaPelna1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_niefizyczna: TidentyfikatorOsobyNiefizycznejPelny = field(
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )
    adres_siedziby: TosobaNiefizycznaPelna1.AdresSiedziby = field(
        metadata={
            "name": "AdresSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresSiedziby(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TpodmiotDowolny(TpodmiotDowolnyBezAdresu):
    """
    Podstawowy zestaw danych o osobie fizycznej lub niefizycznej.
    """


    adres_zamieszkania_siedziby: TpodmiotDowolny.AdresZamieszkaniaSiedziby = field(
        metadata={
            "name": "AdresZamieszkaniaSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkaniaSiedziby(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TpodmiotDowolny1(TpodmiotDowolnyBezAdresu):
    """
    Podstawowy zestaw danych o osobie fizycznej lub niefizycznej - bez
    elementu Poczta w adresie polskim.
    """


    adres_zamieszkania_siedziby: TpodmiotDowolny1.AdresZamieszkaniaSiedziby = field(
        metadata={
            "name": "AdresZamieszkaniaSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkaniaSiedziby(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TpodmiotDowolny2(TpodmiotDowolnyBezAdresu3):
    """
    Podstawowy zestaw danych o osobie fizycznej lub niefizycznej - bez
    elementu Numer REGON oraz bez elementu Poczta w adresie polskim.
    """

    adres_zamieszkania_siedziby: TpodmiotDowolny2.AdresZamieszkaniaSiedziby = field(
        metadata={
            "name": "AdresZamieszkaniaSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkaniaSiedziby(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TpodmiotDowolnyPelny:
    """
    Pełny zestaw danych o osobie fizycznej lub niefizycznej.
    """

    class Meta:
        name = "TPodmiotDowolnyPelny"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: None | TidentyfikatorOsobyFizycznejPelny = field(
        default=None,
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    osoba_niefizyczna: None | TidentyfikatorOsobyNiefizycznejPelny = field(
        default=None,
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    adres_zamieszkania_siedziby: TpodmiotDowolnyPelny.AdresZamieszkaniaSiedziby = field(
        metadata={
            "name": "AdresZamieszkaniaSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkaniaSiedziby(Tadres2):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class TpodmiotDowolnyPelny1:
    """
    Pełny zestaw danych o osobie fizycznej lub niefizycznej - bez elementu
    Poczta w adresie polskim.
    """

    class Meta:
        name = "TPodmiotDowolnyPelny1"
        target_namespace = (
            "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/"
        )

    osoba_fizyczna: None | TidentyfikatorOsobyFizycznejPelny = field(
        default=None,
        metadata={
            "name": "OsobaFizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    osoba_niefizyczna: None | TidentyfikatorOsobyNiefizycznejPelny = field(
        default=None,
        metadata={
            "name": "OsobaNiefizyczna",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
        },
    )
    adres_zamieszkania_siedziby: TpodmiotDowolnyPelny1.AdresZamieszkaniaSiedziby = field(
        metadata={
            "name": "AdresZamieszkaniaSiedziby",
            "type": "Element",
            "namespace": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2022/01/05/eD/DefinicjeTypy/",
            "required": True,
        }
    )

    @dataclass(kw_only=True)
    class AdresZamieszkaniaSiedziby(Tadres1):
        rodzaj_adresu: str = field(
            init=False,
            default="RAD",
            metadata={
                "name": "rodzajAdresu",
                "type": "Attribute",
                "required": True,
            },
        )
