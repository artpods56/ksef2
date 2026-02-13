KSeF API TE (v2)

Download OpenAPI specification:Download

Wersja API: 2.0.1 (build 2.0.1-te-20260201.4+346bbd20a78a0747a6f370c7696879ddb380cbe2)
Klucze publiczne Ministerstwa Finansów (dla danego środowiska): Pobierz klucze
Historia zmian: Changelog
Rozszerzona dokumentacja API: ksef-docs

Adres serwera API:

    Środowisko TEST: https://api-test.ksef.mf.gov.pl/v2

Uzyskiwanie dostępu

Uwierzytelnianie w systemie KSeF API 2.0 jest obowiązkowym etapem, który należy wykonać przed dostępem do chronionych zasobów systemu. Proces ten oparty jest na uzyskaniu tokenu dostępu (accessToken) w formacie JWT, który następnie wykorzystywany jest do autoryzacji operacji API.

    Więcej informacji:

        Uwierzytelnianie

Inicjalizacja uwierzytelnienia

Generuje unikalny challenge wymagany w kolejnym kroku operacji uwierzytelnienia.
Responses
Response Schema: application/json
challenge
required
	
string (Challenge) = 36 characters

Unikalny challenge.
timestamp
required
	
string <date-time>

Czas wygenerowania challenge-a.
timestampMs
required
	
integer <int64>

Czas wygenerowania challenge-a w milisekundach od 1 stycznia 1970 roku (Unix timestamp).
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "challenge": "20250514-CR-226FB7B000-3ACF9BE4C0-10",
    "timestamp": "2025-07-11T12:23:56.0154302+00:00",
    "timestampMs": 1752236636015

}
Uwierzytelnienie z wykorzystaniem podpisu XAdES

Rozpoczyna operację uwierzytelniania za pomocą dokumentu XML podpisanego podpisem elektronicznym XAdES.

    Więcej informacji:

        Przygotowanie dokumentu XML
        Podpis dokumentu XML
        Schemat XSD

query Parameters
verifyCertificateChain	
boolean

Wymuszenie weryfikacji zaufania łańcucha certyfikatu wraz ze sprawdzeniem statusu certyfikatu (OCSP/CRL) na środowiskach które umożliwiają wykorzystanie samodzielnie wygenerowanych certyfikatów.
Request Body schema: application/xml
required
string
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny sesji uwierzytelnienia.
required
	
object

Token operacji uwierzytelnienia.
token
required
	
string

Token w formacie JWT.
validUntil
required
	
string <date-time>

Data ważności tokena.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/xml

<?xml version="1.0" encoding="utf-8"?>
<AuthTokenRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://ksef.mf.gov.pl/auth/token/2.0">
    <Challenge>20250625-CR-20F5EE4000-DA48AE4124-46</Challenge>
    <ContextIdentifier>
        <Nip>5265877635</Nip>
    </ContextIdentifier>
    <SubjectIdentifierType>certificateSubject</SubjectIdentifierType>
    <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Id="Signature-9707709">
        <!-- Tu powinien być podpis XAdES -->
    </ds:Signature>
</AuthTokenRequest>

Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250514-AU-2DFC46C000-3AC6D5877F-D4",
    "authenticationToken": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbi10eXBlIjoiT3BlcmF0aW9uVG9rZW4iLCJvcGVyYXRpb24tcmVmZXJlbmNlLW51bWJlciI6IjIwMjUwNTE0LUFVLTJERkM0NkMwMDAtM0FDNkQ1ODc3Ri1ENCIsImV4cCI6MTc0NzIzMTcxOSwiaWF0IjoxNzQ3MjI5MDE5LCJpc3MiOiJrc2VmLWFwaS10aSIsImF1ZCI6ImtzZWYtYXBpLXRpIn0.rtRcV2mR9SiuJwpQaQHsbAXvvVsdNKG4DJsdiJctIeU",
        "validUntil": "2025-07-11T12:23:56.0154302+00:00"
    }

}
Uwierzytelnienie z wykorzystaniem tokena KSeF

Rozpoczyna operację uwierzytelniania z wykorzystaniem wcześniej wygenerowanego tokena KSeF.

Token KSeF wraz z timestampem ze wcześniej wygenerowanego challenge'a (w formacie token|timestamp) powinien zostać zaszyfrowany dedykowanym do tego celu kluczem publicznym.

    Timestamp powinien zostać przekazany jako liczba milisekund od 1 stycznia 1970 roku (Unix timestamp).
    Algorytm szyfrowania: RSA-OAEP (z użyciem SHA-256 jako funkcji skrótu).

Request Body schema: application/json
challenge
required
	
string = 36 characters

Wygenerowany wcześniej challenge.
required
	
object

Identyfikator kontekstu do którego następuje uwierzytelnienie.
type
required
	
string
Enum: "Nip" "InternalId" "NipVatUe" "PeppolId"

Typ identyfikatora
value
required
	
string

Wartość identyfikatora
encryptedToken
required
	
string <byte>

Zaszyfrowany token wraz z timestampem z challenge'a, w postaci token|timestamp, zakodowany w formacie Base64.
	
object or null

Polityka autoryzacji żądań przy każdym użyciu tokena dostępu.
	
object or null

Lista dozwolonych adresów IP.
ip4Addresses	
Array of strings or null[ items^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$ ]

Lista adresów IPv4 w notacji dziesiętnej kropkowanej, np. 192.168.0.10.
ip4Ranges	
Array of strings or null[ items^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}-((... ]

Lista adresów IPv4 podana w formie zakresu początek–koniec, oddzielonego pojedynczym myślnikiem, np. 10.0.0.1–10.0.0.254.
ip4Masks	
Array of strings or null[ items^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\/(... ]

Lista adresów IPv4 w notacji CIDR, np. 172.16.0.0/16.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny sesji uwierzytelnienia.
required
	
object

Token operacji uwierzytelnienia.
token
required
	
string

Token w formacie JWT.
validUntil
required
	
string <date-time>

Data ważności tokena.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "challenge": "20250625-CR-2FDC223000-C2BFC98A9C-4E",
    "contextIdentifier": {
        "type": "Nip",
        "value": "5265877635"
    },
    "encryptedToken": "..."

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250514-AU-2DFC46C000-3AC6D5877F-D4",
    "authenticationToken": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbi10eXBlIjoiT3BlcmF0aW9uVG9rZW4iLCJvcGVyYXRpb24tcmVmZXJlbmNlLW51bWJlciI6IjIwMjUwNTE0LUFVLTJERkM0NkMwMDAtM0FDNkQ1ODc3Ri1ENCIsImV4cCI6MTc0NzIzMTcxOSwiaWF0IjoxNzQ3MjI5MDE5LCJpc3MiOiJrc2VmLWFwaS10aSIsImF1ZCI6ImtzZWYtYXBpLXRpIn0.rtRcV2mR9SiuJwpQaQHsbAXvvVsdNKG4DJsdiJctIeU",
        "validUntil": "2025-07-11T12:23:56.0154302+00:00"
    }

}
Pobranie statusu uwierzytelniania

Sprawdza bieżący status operacji uwierzytelniania dla podanego tokena.

Sposób uwierzytelnienia: AuthenticationToken otrzymany przy rozpoczęciu operacji uwierzytelniania.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny tokena otrzymanego przy inicjalizacji operacji uwierzytelniania.
Responses
Response Schema: application/json
startDate
required
	
string <date-time>

Data rozpoczęcia operacji uwierzytelnienia.
authenticationMethod
required
	
string
Enum: "Token" "TrustedProfile" "InternalCertificate" "QualifiedSignature" "QualifiedSeal" "PersonalSignature" "PeppolSignature"

Metoda uwierzytelnienia.
Wartość 	Opis
Token 	Token KSeF.
TrustedProfile 	Profil Zaufany.
InternalCertificate 	Certyfikat KSeF.
QualifiedSignature 	Podpis kwalifikowany.
QualifiedSeal 	Pieczęć kwalifikowana.
PersonalSignature 	Podpis osobisty.
PeppolSignature 	Podpis dostawcy usług Peppol.
required
	
object

Informacje o aktualnym statusie.
Code 	Description 	Details
100 	Uwierzytelnianie w toku 	-
200 	Uwierzytelnianie zakończone sukcesem 	-
415 	Uwierzytelnianie zakończone niepowodzeniem 	Brak przypisanych uprawnień
425 	Uwierzytelnienie unieważnione 	Uwierzytelnienie i powiązane refresh tokeny zostały unieważnione przez użytkownika
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Nieprawidłowe wyzwanie autoryzacyjne
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Nieprawidłowy token
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Nieprawidłowy czas tokena
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Token unieważniony
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Token nieaktywny
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Nieważny certyfikat
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Błąd weryfikacji łańcucha certyfikatów
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Niezaufany łańcuch certyfikatów
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Certyfikat odwołany
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Niepoprawny certyfikat
470 	Uwierzytelnianie zakończone niepowodzeniem 	Próba wykorzystania metod autoryzacyjnych osoby zmarłej
480 	Uwierzytelnienie zablokowane 	Podejrzenie incydentu bezpieczeństwa. Skontaktuj się z Ministerstwem Finansów przez formularz zgłoszeniowy.
500 	Nieznany błąd 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
isTokenRedeemed	
boolean or null

Czy został już wydany refresh token powiązany z danym uwierzytelnieniem.
lastTokenRefreshDate	
string or null <date-time>

Data ostatniego odświeżenia tokena.
refreshTokenValidUntil	
string or null <date-time>

Termin ważności refresh tokena (o ile nie zostanie wcześniej unieważniony).
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
Example
Kod 100 | Uwierzytelnianie w toku
{

    "startDate": "0001-01-01T00:00:00+00:00",
    "authenticationMethod": "Token",
    "status": {
        "code": 100,
        "description": "Uwierzytelnianie w toku"
    }

}
Pobranie tokenów dostępowych

Pobiera parę tokenów (access token i refresh token) wygenerowanych w ramach pozytywnie zakończonego procesu uwierzytelniania. Tokeny można pobrać tylko raz.

Sposób uwierzytelnienia: AuthenticationToken otrzymany przy rozpoczęciu operacji uwierzytelniania.
Authorizations:
Bearer
Responses
Response Schema: application/json
required
	
object

Token dostępu.
token
required
	
string

Token w formacie JWT.
validUntil
required
	
string <date-time>

Data ważności tokena.
required
	
object

Token umożliwiający odświeżenie tokenu dostępu.

    Więcej informacji:

        Odświeżanie tokena

token
required
	
string

Token w formacie JWT.
validUntil
required
	
string <date-time>

Data ważności tokena.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "accessToken": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbi10eXBlIjoiQ29udGV4dFRva2VuIiwiY29udGV4dC1pZGVudGlmaWVyLXR5cGUiOiJOaXAiLCJjb250ZXh0LWlkZW50aWZpZXItdmFsdWUiOiIzNzU2OTc3MDQ5IiwiYXV0aGVudGljYXRpb24tbWV0aG9kIjoiUXVhbGlmaWVkU2VhbCIsInN1YmplY3QtZGV0YWlscyI6IntcIlN1YmplY3RJZGVudGlmaWVyXCI6e1wiVHlwZVwiOlwiTmlwXCIsXCJWYWx1ZVwiOlwiMzc1Njk3NzA0OVwifX0iLCJleHAiOjE3NDcyMjAxNDksImlhdCI6MTc0NzIxOTI0OSwiaXNzIjoia3NlZi1hcGktdGkiLCJhdWQiOiJrc2VmLWFwaS10aSJ9.R_3_R2PbdCk8T4WP_0XGOO1iVNu2ugNxmkDvsD0soIE",
        "validUntil": "2025-07-11T12:23:56.0154302+00:00"
    },
    "refreshToken": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbi10eXBlIjoiQ29udGV4dFRva2VuIiwiY29udGV4dC1pZGVudGlmaWVyLXR5cGUiOiJOaXAiLCJjb250ZXh0LWlkZW50aWZpZXItdmFsdWUiOiIzNzU2OTc3MDQ5IiwiYXV0aGVudGljYXRpb24tbWV0aG9kIjoiUXVhbGlmaWVkU2VhbCIsInN1YmplY3QtZGV0YWlscyI6IntcIlN1YmplY3RJZGVudGlmaWVyXCI6e1wiVHlwZVwiOlwiTmlwXCIsXCJWYWx1ZVwiOlwiMzc1Njk3NzA0OVwifX0iLCJleHAiOjE3NDcyMjAxNDksImlhdCI6MTc0NzIxOTI0OSwiaXNzIjoia3NlZi1hcGktdGkiLCJhdWQiOiJrc2VmLWFwaS10aSJ9.R_3_R2PbdCk8T4WP_0XGOO1iVNu2ugNxmkDvsD0soIE",
        "validUntil": "2025-07-11T12:23:56.0154302+00:00"
    }

}
Odświeżenie tokena dostępowego

Generuje nowy token dostępu na podstawie ważnego refresh tokena.

Sposób uwierzytelnienia: RefreshToken.
Authorizations:
Bearer
Responses
Response Schema: application/json
required
	
object

Token dostępu, którego należy używać w wywołaniach chronionych zasobów API.
token
required
	
string

Token w formacie JWT.
validUntil
required
	
string <date-time>

Data ważności tokena.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "accessToken": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbi10eXBlIjoiQ29udGV4dFRva2VuIiwiY29udGV4dC1pZGVudGlmaWVyLXR5cGUiOiJOaXAiLCJjb250ZXh0LWlkZW50aWZpZXItdmFsdWUiOiIzNzU2OTc3MDQ5IiwiYXV0aGVudGljYXRpb24tbWV0aG9kIjoiUXVhbGlmaWVkU2VhbCIsInN1YmplY3QtZGV0YWlscyI6IntcIlN1YmplY3RJZGVudGlmaWVyXCI6e1wiVHlwZVwiOlwiTmlwXCIsXCJWYWx1ZVwiOlwiMzc1Njk3NzA0OVwifX0iLCJleHAiOjE3NDcyMjAxNDksImlhdCI6MTc0NzIxOTI0OSwiaXNzIjoia3NlZi1hcGktdGkiLCJhdWQiOiJrc2VmLWFwaS10aSJ9.R_3_R2PbdCk8T4WP_0XGOO1iVNu2ugNxmkDvsD0soIE",
        "validUntil": "2025-07-11T12:23:56.0154302+00:00"
    }

}
Zablokowanie kontekstu

Blokuje możliwość uwierzytelniania dla bieżącego kontekstu. Tylko na środowiskach testowych.
Request Body schema: application/json
	
object or null
value
required
	
string
type
required
	
string
Enum: "Nip" "InternalId" "NipVatUe" "PeppolId"
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "contextIdentifier": {
        "value": "string",
        "type": "Nip"
    }

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Odblokowanie kontekstu

Odblokowuje możliwość uwierzytelniania dla bieżącego kontekstu. Tylko na środowiskach testowych.
Request Body schema: application/json
	
object or null
value
required
	
string
type
required
	
string
Enum: "Nip" "InternalId" "NipVatUe" "PeppolId"
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "contextIdentifier": {
        "value": "string",
        "type": "Nip"
    }

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Aktywne sesje
Pobranie listy aktywnych sesji

Zwraca listę aktywnych sesji uwierzytelnienia.

Sortowanie:

    startDate (Desc)

Authorizations:
Bearer
query Parameters
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
header Parameters
x-continuation-token	
string

Token służący do pobrania kolejnej strony wyników.
Responses
Response Schema: application/json
continuationToken	
string or null

Token służący do pobrania kolejnej strony wyników. Jeśli jest pusty, to nie ma kolejnych stron.
required
	
Array of objects (AuthenticationListItem)

Lista sesji uwierzytelniania.
Array
startDate
required
	
string <date-time>

Data rozpoczęcia operacji uwierzytelnienia.
authenticationMethod
required
	
string
Enum: "Token" "TrustedProfile" "InternalCertificate" "QualifiedSignature" "QualifiedSeal" "PersonalSignature" "PeppolSignature"

Metoda uwierzytelnienia.
Wartość 	Opis
Token 	Token KSeF.
TrustedProfile 	Profil Zaufany.
InternalCertificate 	Certyfikat KSeF.
QualifiedSignature 	Podpis kwalifikowany.
QualifiedSeal 	Pieczęć kwalifikowana.
PersonalSignature 	Podpis osobisty.
PeppolSignature 	Podpis dostawcy usług Peppol.
required
	
object

Informacje o aktualnym statusie.
Code 	Description 	Details
100 	Uwierzytelnianie w toku 	-
200 	Uwierzytelnianie zakończone sukcesem 	-
415 	Uwierzytelnianie zakończone niepowodzeniem 	Brak przypisanych uprawnień
425 	Uwierzytelnienie unieważnione 	Uwierzytelnienie i powiązane refresh tokeny zostały unieważnione przez użytkownika
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Nieprawidłowe wyzwanie autoryzacyjne
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Nieprawidłowy token
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Nieprawidłowy czas tokena
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Token unieważniony
450 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu 	Token nieaktywny
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Nieważny certyfikat
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Błąd weryfikacji łańcucha certyfikatów
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Niezaufany łańcuch certyfikatów
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Certyfikat odwołany
460 	Uwierzytelnianie zakończone niepowodzeniem z powodu błędu certyfikatu 	Niepoprawny certyfikat
470 	Uwierzytelnianie zakończone niepowodzeniem 	Próba wykorzystania metod autoryzacyjnych osoby zmarłej
480 	Uwierzytelnienie zablokowane 	Podejrzenie incydentu bezpieczeństwa. Skontaktuj się z Ministerstwem Finansów przez formularz zgłoszeniowy.
500 	Nieznany błąd 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
isTokenRedeemed	
boolean or null

Czy został już wydany refresh token powiązany z danym uwierzytelnieniem.
lastTokenRefreshDate	
string or null <date-time>

Data ostatniego odświeżenia tokena.
refreshTokenValidUntil	
string or null <date-time>

Termin ważności refresh tokena (o ile nie zostanie wcześniej unieważniony).
referenceNumber
required
	
string = 36 characters

Numer referencyjny sesji uwierzytelnienia.
isCurrent	
boolean

Czy sesja jest powiązana z aktualnie używanym tokenem.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "continuationToken": "W3siY29tcG9zaXRlVG9rZW4iOnsidG9rZW4iOm51bGwsInJhbmdlIjp7Im1pbiI6IjA1QzFFMCIsIm1heCI6IkZGIn19LCJyZXN1bWVWYWx1ZXMiOlsiMjAyNS0xMC0wM1QxMjoxODo0OS4zNDY2ODQ3WiJdLCJyaWQiOiIzeHd0QVBJWDVRRlVoZ0FBQUFBQUJBPT0iLCJza2lwQ291bnQiOjF9XQ==",
    "items": [
        {}
    ]

}
Unieważnienie aktualnej sesji uwierzytelnienia

Unieważnia sesję powiązaną z tokenem użytym do wywołania tej operacji.

Unieważnienie sesji sprawia, że powiązany z nią refresh token przestaje działać i nie można już za jego pomocą uzyskać kolejnych access tokenów. Aktywne access tokeny działają do czasu minięcia ich termin ważności.

Sposób uwierzytelnienia: RefreshToken lub AccessToken.
Authorizations:
Bearer
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Unieważnienie sesji uwierzytelnienia

Unieważnia sesję o podanym numerze referencyjnym.

Unieważnienie sesji sprawia, że powiązany z nią refresh token przestaje działać i nie można już za jego pomocą uzyskać kolejnych access tokenów. Aktywne access tokeny działają do czasu minięcia ich termin ważności.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji uwierzytelnienia.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Limity i ograniczenia
Pobranie limitów dla bieżącego kontekstu

Zwraca wartości aktualnie obowiązujących limitów dla bieżącego kontekstu.
Authorizations:
Bearer
Responses
Response Schema: application/json
required
	
object

Limity dla sesji interaktywnych.
maxInvoiceSizeInMB
required
	
integer <int32> >= 0

Maksymalny rozmiar faktury w MB.
maxInvoiceWithAttachmentSizeInMB
required
	
integer <int32> >= 0

Maksymalny rozmiar faktury z załącznikiem w MB.
maxInvoices
required
	
integer <int32> >= 0

Maksymalna ilość faktur które można przesłać w pojedynczej sesji.
required
	
object

Limity dla sesji wsadowych.
maxInvoiceSizeInMB
required
	
integer <int32> >= 0

Maksymalny rozmiar faktury w MB.
maxInvoiceWithAttachmentSizeInMB
required
	
integer <int32> >= 0

Maksymalny rozmiar faktury z załącznikiem w MB.
maxInvoices
required
	
integer <int32> >= 0

Maksymalna ilość faktur które można przesłać w pojedynczej sesji.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "onlineSession": {
        "maxInvoiceSizeInMB": 1,
        "maxInvoiceWithAttachmentSizeInMB": 3,
        "maxInvoices": 10000
    },
    "batchSession": {
        "maxInvoiceSizeInMB": 1,
        "maxInvoiceWithAttachmentSizeInMB": 3,
        "maxInvoices": 10000
    }

}
Pobranie limitów dla bieżącego podmiotu

Zwraca wartości aktualnie obowiązujących limitów dla bieżącego podmiotu.
Authorizations:
Bearer
Responses
Response Schema: application/json
	
object or null
maxEnrollments	
integer <int32>
	
object or null
maxCertificates	
integer <int32>
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "enrollment": {
        "maxEnrollments": 6
    },
    "certificate": {
        "maxCertificates": 2
    }

}
Pobranie aktualnie obowiązujących limitów API

Zwraca wartości aktualnie obowiązujących limitów ilości żądań przesyłanych do API.
Authorizations:
Bearer
Responses
Response Schema: application/json
required
	
object

Limity dla otwierania/zamykania sesji interaktywnych.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla otwierania/zamykania sesji wsadowych.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla wysyłki faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania statusu faktury z sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania listy sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania listy faktur w sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pozostałych operacji w ramach sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania metadanych faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla eksportu paczki faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierana statusu eksportu paczki faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania faktur po numerze KSeF.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pozostałych operacji API.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "onlineSession": {
        "perSecond": 100,
        "perMinute": 300,
        "perHour": 1200
    },
    "batchSession": {
        "perSecond": 100,
        "perMinute": 200,
        "perHour": 600
    },
    "invoiceSend": {
        "perSecond": 100,
        "perMinute": 300,
        "perHour": 1800
    },
    "invoiceStatus": {
        "perSecond": 300,
        "perMinute": 1200,
        "perHour": 12000
    },
    "sessionList": {
        "perSecond": 50,
        "perMinute": 100,
        "perHour": 600
    },
    "sessionInvoiceList": {
        "perSecond": 100,
        "perMinute": 200,
        "perHour": 2000
    },
    "sessionMisc": {
        "perSecond": 100,
        "perMinute": 1200,
        "perHour": 12000
    },
    "invoiceMetadata": {
        "perSecond": 80,
        "perMinute": 160,
        "perHour": 200
    },
    "invoiceExport": {
        "perSecond": 40,
        "perMinute": 80,
        "perHour": 200
    },
    "invoiceExportStatus": {
        "perSecond": 100,
        "perMinute": 600,
        "perHour": 6000
    },
    "invoiceDownload": {
        "perSecond": 80,
        "perMinute": 160,
        "perHour": 640
    },
    "other": {
        "perSecond": 100,
        "perMinute": 300,
        "perHour": 1200
    }

}
Zmiana limitów sesji dla bieżącego kontekstu

Zmienia wartości aktualnie obowiązujących limitów sesji dla bieżącego kontekstu. Tylko na środowiskach testowych.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Limity dla sesji interaktywnych.
maxInvoiceSizeInMB
required
	
integer <int32> [ 0 .. 5 ]

Maksymalny rozmiar faktury w MB.
maxInvoiceWithAttachmentSizeInMB
required
	
integer <int32> [ 0 .. 10 ]

Maksymalny rozmiar faktury z załącznikiem w MB.
maxInvoices
required
	
integer <int32> [ 0 .. 100000 ]

Maksymalna ilość faktur które można przesłać w pojedynczej sesji.
required
	
object

Limity dla sesji wsadowych.
maxInvoiceSizeInMB
required
	
integer <int32> [ 0 .. 5 ]

Maksymalny rozmiar faktury w MB.
maxInvoiceWithAttachmentSizeInMB
required
	
integer <int32> [ 0 .. 10 ]

Maksymalny rozmiar faktury z załącznikiem w MB.
maxInvoices
required
	
integer <int32> [ 0 .. 100000 ]

Maksymalna ilość faktur które można przesłać w pojedynczej sesji.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "onlineSession": {
        "maxInvoiceSizeInMB": 5,
        "maxInvoiceWithAttachmentSizeInMB": 10,
        "maxInvoices": 100000
    },
    "batchSession": {
        "maxInvoiceSizeInMB": 5,
        "maxInvoiceWithAttachmentSizeInMB": 10,
        "maxInvoices": 100000
    }

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Przywrócenie domyślnych wartości limitów sesji dla bieżącego kontekstu

Przywraca wartości aktualnie obowiązujących limitów sesji dla bieżącego kontekstu do wartości domyślnych. Tylko na środowiskach testowych.
Authorizations:
Bearer
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Zmiana limitów certyfikatów dla bieżącego podmiotu

Zmienia wartości aktualnie obowiązujących limitów certyfikatów dla bieżącego podmiotu. Tylko na środowiskach testowych.
Authorizations:
Bearer
Request Body schema: application/json
subjectIdentifierType	
string
Enum: "Nip" "Pesel" "Fingerprint"
	
object or null
maxEnrollments	
integer or null <int32> >= 0
	
object or null
maxCertificates	
integer or null <int32> >= 0
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifierType": "Nip",
    "enrollment": {
        "maxEnrollments": 0
    },
    "certificate": {
        "maxCertificates": 0
    }

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Przywrócenie domyślnych wartości limitów certyfikatów dla bieżącego podmiotu

Przywraca wartości aktualnie obowiązujących limitów certyfikatów dla bieżącego podmiotu do wartości domyślnych. Tylko na środowiskach testowych.
Authorizations:
Bearer
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Zmiana limitów API dla bieżącego kontekstu

Zmienia wartości aktualnie obowiązujących limitów żądań przesyłanych do API dla bieżącego kontekstu. Tylko na środowiskach testowych.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Limity dla ilości żądań do API.
required
	
object

Limity dla otwierania/zamykania sesji interaktywnych.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla otwierania/zamykania sesji wsadowych.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla wysyłki faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania statusu faktury z sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania listy sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania listy faktur w sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pozostałych operacji w ramach sesji.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania metadanych faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla eksportu paczki faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania statusu eksportu paczki faktur.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pobierania faktur po numerze KSeF.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
required
	
object

Limity dla pozostałych operacji API.
perSecond
required
	
integer <int32>

Limit na sekundę.
perMinute
required
	
integer <int32>

Limit na minutę.
perHour
required
	
integer <int32>

Limit na godzinę.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "rateLimits": {
        "onlineSession": {},
        "batchSession": {},
        "invoiceSend": {},
        "invoiceStatus": {},
        "sessionList": {},
        "sessionInvoiceList": {},
        "sessionMisc": {},
        "invoiceMetadata": {},
        "invoiceExport": {},
        "invoiceExportStatus": {},
        "invoiceDownload": {},
        "other": {}
    }

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Przywrócenie domyślnych wartości limitów API dla bieżącego kontekstu

Przywraca wartości aktualnie obowiązujących limitów żądań przesyłanych do API dla bieżącego kontekstu do wartości domyślnych. Tylko na środowiskach testowych.
Authorizations:
Bearer
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Zmiana limitów API dla bieżącego kontekstu na wartości produkcyjne

Zmienia wartości aktualnie obowiązujących limitów żądań przesyłanych do API dla bieżącego kontekstu na wartości takie jakie będą na środowisku produkcyjnym. Tylko na środowiskach testowych.
Authorizations:
Bearer
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Certyfikaty klucza publicznego
Pobranie certyfikatów

Zwraca informacje o kluczach publicznych używanych do szyfrowania danych przesyłanych do systemu KSeF.
Responses
Response Schema: application/json
Array
certificate
required
	
string <byte>

Certyfikat klucza publicznego w formacie DER, zakodowany w formacie Base64.
validFrom
required
	
string <date-time>

Data początku obowiązywania certyfikatu.
validTo
required
	
string <date-time>

Data końca obowiązywania certyfikatu.
usage
required
	
Array of strings (PublicKeyCertificateUsage)
Items Enum: "KsefTokenEncryption" "SymmetricKeyEncryption"

Operacje do których może być używany certyfikat.
Wartość 	Opis
KsefTokenEncryption 	Szyfrowanie tokenów KSeF przesyłanych w trakcie procesu uwierzytelniania.
SymmetricKeyEncryption 	Szyfrowanie klucza symetrycznego wykorzystywanego do szyfrowania przesyłanych faktur.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
[

    {
        "certificate": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwocTwdNgt2+PXJ2fcB7k1kn5eFUTXBeep9pH...",
        "validFrom": "2024-07-11T12:23:56.0154302+00:00",
        "validTo": "2028-07-11T12:23:56.0154302+00:00",
        "usage": []
    }

]
Wysyłka interaktywna
Otwarcie sesji interaktywnej

Otwiera sesję do wysyłki pojedynczych faktur. Należy przekazać schemat wysyłanych faktur oraz informacje o kluczu używanym do szyfrowania.

    Więcej informacji:

        Otwarcie sesji interaktywnej
        Klucz publiczny Ministerstwa Finansów

Wymagane uprawnienia: InvoiceWrite, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Schemat faktur wysyłanych w ramach sesji.

Obsługiwane schematy:
SystemCode 	SchemaVersion 	Value
FA (2) 	1-0E 	FA
FA (3) 	1-0E 	FA
PEF (3) 	2-1 	PEF
PEF_KOR (3) 	2-1 	PEF
systemCode
required
	
string

Kod systemowy
schemaVersion
required
	
string

Wersja schematu
value
required
	
string

Wartość
required
	
object

Symetryczny klucz szyfrujący pliki XML, zaszyfrowany kluczem publicznym Ministerstwa Finansów.
encryptedSymmetricKey
required
	
string <byte>

Klucz symetryczny o długości 32 bajtów, zaszyfrowany algorytmem RSA (Padding: OAEP z SHA-256), zakodowany w formacie Base64.

Klucz publiczny Ministerstwa Finansów
initializationVector
required
	
string <byte>

Wektor inicjalizujący (IV) o długości 16 bajtów, używany do szyfrowania symetrycznego, zakodowany w formacie Base64.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny sesji.
validUntil
required
	
string <date-time>

Termin ważności sesji. Po jego upływie sesja zostanie automatycznie zamknięta.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	onlineSession
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "formCode": {
        "systemCode": "FA (3)",
        "schemaVersion": "1-0E",
        "value": "FA"
    },
    "encryption": {
        "encryptedSymmetricKey": "bdUVjqLj+y2q6aBUuLxxXYAMqeDuIBRTyr+hB96DaWKaGzuVHw9p+Nk9vhzgF/Q5cavK2k6eCh6SdsrWI0s9mFFj4A4UJtsyD8Dn3esLfUZ5A1juuG3q3SBi/XOC/+9W+0T/KdwdE393mbiUNyx1K/0bw31vKJL0COeJIDP7usAMDl42/H1TNvkjk+8iZ80V0qW7D+RZdz+tdiY1xV0f2mfgwJ46V0CpZ+sB9UAssRj+eVffavJ0TOg2b5JaBxE8MCAvrF6rO5K4KBjUmoy7PP7g1qIbm8xI2GO0KnfPOO5OWj8rsotRwBgu7x19Ine3qYUvuvCZlXRGGZ5NHIzWPM4O74+gNalaMgFCsmv8mMhETSU4SfAGmJr9edxPjQSbgD5i2X4eDRDMwvyaAa7CP1b2oICju+0L7Fywd2ZtUcr6El++eTVoi8HYsTArntET++gULT7XXjmb8e3O0nxrYiYsE9GMJ7HBGv3NOoJ1NTm3a7U6+c0ZJiBVLvn6xXw10LQX243xH+ehsKo6djQJKYtqcNPaXtCwM1c9RrsOx/wRXyWCtTffqLiaR0LbYvfMJAcEWceG+RaeAx4p37OiQqdJypd6LAv9/0ECWK8Bip8yyoA+0EYiAJb9YuDz2YlQX9Mx9E9FzFIAsgEQ2w723HZYWgPywLb+dlsum4lTZKQ=",
        "initializationVector": "OmtDQdl6vkOI1GLKZSjgEg=="
    }

}
Response samples

    201400429

Content type
application/json
{

    "referenceNumber": "20250625-SO-2C3E6C8000-B675CF5D68-07",
    "validUntil": "2025-07-11T12:23:56.0154302+00:00"

}
Wysłanie faktury

Przyjmuje zaszyfrowaną fakturę oraz jej metadane i rozpoczyna jej przetwarzanie.

    Więcej informacji:

        Wysłanie faktury

Wymagane uprawnienia: InvoiceWrite, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji
Request Body schema: application/json

Dane faktury
invoiceHash
required
	
string <byte> = 44 characters

Skrót SHA256 oryginalnej faktury, zakodowany w formacie Base64.
invoiceSize
required
	
integer <int64> >= 1

Rozmiar oryginalnej faktury w bajtach. Maksymalny rozmiar zależy od limitów ustawionych dla uwierzytelnionego kontekstu.
encryptedInvoiceHash
required
	
string <byte> = 44 characters

Skrót SHA256 zaszyfrowanej faktury, zakodowany w formacie Base64.
encryptedInvoiceSize
required
	
integer <int64> >= 1

Rozmiar zaszyfrowanej faktury w bajtach.
encryptedInvoiceContent
required
	
string <byte>

Faktura zaszyfrowana algorytmem AES-256-CBC z dopełnianiem PKCS#7 (kluczem przekazanym przy otwarciu sesji), zakodowana w formacie Base64.
offlineMode	
boolean
Default: false

Określa, czy podatnik deklaruje tryb fakturowania "offline" dla przesyłanego dokumentu.
hashOfCorrectedInvoice	
string or null <byte> = 44 characters

Skrót SHA256 korygowanej faktury, zakodowany w formacie Base64. Wymagany przy wysyłaniu korekty technicznej faktury.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny faktury.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1800 	invoiceSend
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "invoiceHash": "EbrK4cOSjW4hEpJaHU71YXSOZZmqP5++dK9nLgTzgV4=",
    "invoiceSize": 6480,
    "encryptedInvoiceHash": "miYb1z3Ljw5VucTZslv3Tlt+V/EK1V8Q8evD8HMQ0dc=",
    "encryptedInvoiceSize": 6496,
    "encryptedInvoiceContent": "...",
    "offlineMode": false

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250625-EE-319D7EE000-B67F415CDC-2C"

}
Zamknięcie sesji interaktywnej

Zamyka sesję interaktywną i rozpoczyna generowanie zbiorczego UPO dla sesji.

Wymagane uprawnienia: InvoiceWrite, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	onlineSession
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Wysyłka wsadowa
Otwarcie sesji wsadowej

Otwiera sesję do wysyłki wsadowej faktur. Należy przekazać schemat wysyłanych faktur, informacje o paczce faktur oraz informacje o kluczu używanym do szyfrowania.

    Więcej informacji:

        Przygotowanie paczki faktur
        Klucz publiczny Ministerstwa Finansów

Wymagane uprawnienia: InvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Schemat faktur wysyłanych w ramach sesji.

Obsługiwane schematy:
SystemCode 	SchemaVersion 	Value
FA (2) 	1-0E 	FA
FA (3) 	1-0E 	FA
systemCode
required
	
string

Kod systemowy
schemaVersion
required
	
string

Wersja schematu
value
required
	
string

Wartość
required
	
object

Informacje o przesyłanej paczce faktur.
fileSize
required
	
integer <int64> [ 1 .. 5000000000 ]

Rozmiar pliku paczki w bajtach. Maksymalny rozmiar paczki to 5GB.
fileHash
required
	
string <byte> = 44 characters

Skrót SHA256 pliku paczki, zakodowany w formacie Base64.
required
	
Array of objects (BatchFilePartInfo) [ 1 .. 50 ] items

Informacje o częściach pliku paczki. Maksymalna liczba części to 50. Maksymalny dozwolony rozmiar części przed zaszyfrowaniem to 100MB.
Array ([ 1 .. 50 ] items)
ordinalNumber
required
	
integer <int32> >= 1

Numer sekwencyjny części pliku paczki.
fileSize
required
	
integer <int64> >= 1

Rozmiar zaszyfrowanej części pliku paczki w bajtach.
fileHash
required
	
string <byte> = 44 characters

Skrót SHA256 zaszyfrowanej części pliku paczki, zakodowany w formacie Base64.
required
	
object

Symetryczny klucz szyfrujący plik paczki, zaszyfrowany kluczem publicznym Ministerstwa Finansów.
encryptedSymmetricKey
required
	
string <byte>

Klucz symetryczny o długości 32 bajtów, zaszyfrowany algorytmem RSA (Padding: OAEP z SHA-256), zakodowany w formacie Base64.

Klucz publiczny Ministerstwa Finansów
initializationVector
required
	
string <byte>

Wektor inicjalizujący (IV) o długości 16 bajtów, używany do szyfrowania symetrycznego, zakodowany w formacie Base64.
offlineMode	
boolean
Default: false

Określa, czy podatnik deklaruje tryb fakturowania "offline" dla dokumentów przesyłanych w sesji wsadowej.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny sesji.
required
	
Array of objects (PartUploadRequest)

Dane wymagane do poprawnego przesłania poszczególnych części pliku paczki faktur.

Każdą część pliku paczki zadeklarowaną w fileParts należy przesłać zgodnie z odpowiadającym jej obiektem w partUploadRequests. Łącznikiem pomiędzy deklaracją a instrukcją wysyłki jest pole ordinalNumber.

Dla każdej części należy:

    zastosować metodę HTTP wskazaną w method,
    ustawić adres z url,
    dołączyć nagłówki z headers,
    dołączyć treść części pliku w korpusie żądania.

Uwaga: nie należy dodawać do nagłówków token dostępu (accessToken).

Każdą część przesyła się oddzielnym żądaniem HTTP.Zwracane kody odpowiedzi:

    201 – poprawne przyjęcie pliku,
    400 – błędne dane,
    401 – nieprawidłowe uwierzytelnienie,
    403 – brak uprawnień do zapisu (np.upłynął czas na zapis).

Array
ordinalNumber
required
	
integer <int32> >= 1

Numer sekwencyjny części pliku paczki.
method
required
	
string

Metoda HTTP, której należy użyć przy wysyłce części pliku paczki.
url
required
	
string <uri>

Adres pod który należy wysłać część pliku paczki.
required
	
object

Nagłówki, których należy użyć przy wysyłce części pliku paczki.
property name*
additional property
	
string or null
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	200 	600 	batchSession
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "formCode": {
        "systemCode": "FA (2)",
        "schemaVersion": "1-0E",
        "value": "FA"
    },
    "batchFile": {
        "fileSize": 16037,
        "fileHash": "WO86CC+1Lef11wEosItld/NPwxGN8tobOMLqk9PQjgs=",
        "fileParts": []
    },
    "encryption": {
        "encryptedSymmetricKey": "bYqmPAglF01AxZim4oNa+1NerhZYfFgLMnvksBprUur1aesQ0Y5jsmOIfCrozfMkF2tjdO+uOsBg4FPlDgjChwN2/tz2Hqwtxq3RkTr1SjY4x8jxJFpPedcS7EI+XO8C+i9mLj7TFx9p/bg07yM9vHtMAk5b88Ay9Qc3+T5Ch1DM2ClR3sVu2DqdlKzmbINY+rhfGtXn58Qo0XRyESGgc6M0iTZVBRPuPXLnD8a1KpOneCpNzLwxgT6Ei3ivLOpPWT53PxkRTaQ8puj6CIiCKo4FHQzHuI/NmrAhYU7TkNm2kymP/OxBgWdg3XB74tqNFfT8RZN1bZXuPhBidDOqa+xsqY3E871FSDmQwZf58HmoNl31XNvpnryiRGfnAISt+m+ELqgksAresVu6E9poUL1yiff+IOHSZABoYpNiqwnbT8qyW1uk8lKLyFVFu+kOsbzBk1OWWHqSkNFDaznDa2MKjHonOXI0uyKaKWvoBFC4dWN1PVumfpSSFAeYgNpAyVrZdcVOuiliEWepTDjGzJoOafTvwr5za2S6B5bPECDpX7JXazV7Olkq7ezG0w8y3olx+0C+NHoCk8B5/cm4gtVHTgKjiLSGpKJVOJABLXFkOyIOjbQsVe4ryX0Qy+SfL7JIQvTWvM5xkCoOMbzLdMo9tNo5qE34sguFI+lIevY=",
        "initializationVector": "jWpJLNBHJ5pQEGCBglmIAw=="
    },
    "offlineMode": false

}
Response samples

    201400429

Content type
application/json
{

    "referenceNumber": "20250626-SB-213D593000-4DE10D80A5-E9",
    "partUploadRequests": [
        {}
    ]

}
Zamknięcie sesji wsadowej

Zamyka sesję wsadową, rozpoczyna procesowanie paczki faktur i generowanie UPO dla prawidłowych faktur oraz zbiorczego UPO dla sesji.

Wymagane uprawnienia: InvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	200 	600 	batchSession
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Status wysyłki i UPO
Pobranie listy sesji

Zwraca listę sesji spełniających podane kryteria wyszukiwania.

Sortowanie:

    dateCreated (Desc)

Wymagane uprawnienia:

    Introspection/EnforcementOperations – pozwala pobrać wszystkie sesje w bieżącym kontekście uwierzytelnienia (ContextIdentifier).
    InvoiceWrite – pozwala pobrać wyłącznie sesje utworzone przez podmiot uwierzytelniający, czyli podmiot inicjujący uwierzytelnienie.

Authorizations:
Bearer
query Parameters
pageSize	
integer <int32> [ 10 .. 1000 ]
Default: 10

Rozmiar strony.
sessionType
required
	
string
Enum: "Online" "Batch"

Typ sesji.
Wartość 	Opis
Online 	Wysyłka interaktywna (pojedyncze faktury).
Batch 	Wysyłka wsadowa (paczka faktur).
referenceNumber	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
dateCreatedFrom	
string <date-time>

Data utworzenia sesji (od).
dateCreatedTo	
string <date-time>

Data utworzenia sesji (do).
dateClosedFrom	
string <date-time>

Data zamknięcia sesji (od).
dateClosedTo	
string <date-time>

Data zamknięcia sesji (do).
dateModifiedFrom	
string <date-time>

Data ostatniej aktywności (wysyłka faktury lub zmiana statusu) w ramach sesji (od).
dateModifiedTo	
string <date-time>

Data ostatniej aktywności (wysyłka faktury lub zmiana statusu) w ramach sesji (do).
statuses	
Array of strings (CommonSessionStatus)
Items Enum: "InProgress" "Succeeded" "Failed" "Cancelled"

Statusy sesji.
Wartość 	Opis
InProgress 	Sesja aktywna.
Succeeded 	Sesja przetworzona poprawnie. W trakcie przetwarzania sesji nie wystąpiły żadne błędy, ale część faktur nadal mogła zostać odrzucona.
Failed 	Sesja nie przetworzona z powodu błędów. Na etapie rozpoczynania lub kończenia sesji wystąpiły błędy, które nie pozwoliły na jej poprawne przetworzenie.
Cancelled 	Sesja anulowania. Został przekroczony czas na wysyłkę w sesji wsadowej, lub nie przesłano żadnych faktur w sesji interaktywnej.
header Parameters
x-continuation-token	
string

Token służący do pobrania kolejnej strony wyników.
Responses
Response Schema: application/json
continuationToken	
string or null

Token służący do pobrania kolejnej strony wyników. Jeśli jest pusty, to nie ma kolejnych stron.
required
	
Array of objects (SessionsQueryResponseItem)

Lista sesji.
Array
referenceNumber
required
	
string = 36 characters

Numer referencyjny sesji.
required
	
object

Status sesji.
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
dateCreated
required
	
string <date-time>

Data utworzenia sesji.
dateUpdated
required
	
string <date-time>

Data ostatniej aktywności w ramach sesji.
validUntil	
string or null <date-time>

Termin ważności sesji. Po jego upływie sesja interaktywna zostanie automatycznie zamknięta.
totalInvoiceCount
required
	
integer <int32> >= 0

Łączna liczba faktur (uwzględnia również te w trakcie przetwarzania).
successfulInvoiceCount
required
	
integer <int32> >= 0

Liczba poprawnie przetworzonych faktur.
failedInvoiceCount
required
	
integer <int32> >= 0

Liczba błędnie przetworzonych faktur.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	50 	100 	600 	sessionList
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "continuationToken": "W3sidG9rZW4iOiIrUklEOn4zeHd0QU1SM3dYYjRCd0FBQUFBQUNBPT0jUlQ6MSNUUkM6MTAjSVNWOjIjSUVPOjY1NTY3I1FDRjo4I0ZQQzpBZ2dBQUFBQUFDQUFBQVlBQUFBQUlBQUFBQUFBQUFBZ0FBQVVBUEVIQUVGdGdJUUFFUUJBQUJBRUFCQVVoZ1NBQXdBQUFBQWdBQUFHQUhFa0NFQWxnQVFBQUFBQUlBQUFGZ0F5Q0FVZ0VBRC9nRE9BRFlFdWdIcUF5SXBEZ0IrQUJnQUFBQUFnQUFBQ0FPNlYiLCJyYW5nZSI6eyJtaW4iOiIiLCJtYXgiOiIwNUMxREYyQjVGMzU5OCJ9fV0=",
    "sessions": [
        {},
        {}
    ]

}
Pobranie statusu sesji

Sprawdza bieżący status sesji o podanym numerze referencyjnym.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
Responses
Response Schema: application/json
required
	
object

Informacje o aktualnym statusie.

Sesja wsadowa:
Code 	Description 	Details
100 	Sesja wsadowa rozpoczęta 	-
150 	Trwa przetwarzanie 	-
200 	Sesja wsadowa przetworzona pomyślnie 	-
405 	Błąd weryfikacji poprawności dostarczonych elementów paczki 	-
415 	Błąd odszyfrowania dostarczonego klucza 	-
420 	Przekroczony limit faktur w sesji 	-
430 	Błąd dekompresji pierwotnego archiwum 	-
435 	Błąd odszyfrowania zaszyfrowanych części archiwum 	-
440 	Sesja anulowana 	Przekroczono czas wysyłki
440 	Sesja anulowana 	Nie przesłano faktur
445 	Błąd weryfikacji, brak poprawnych faktur 	-
500 	Nieznany błąd ({statusCode}) 	-

Sesja interaktywna:
Code 	Description 	Details
100 	Sesja interaktywna otwarta 	-
170 	Sesja interaktywna zamknięta 	-
200 	Sesja interaktywna przetworzona pomyślnie 	-
415 	Błąd odszyfrowania dostarczonego klucza 	-
440 	Sesja anulowana 	Nie przesłano faktur
445 	Błąd weryfikacji, brak poprawnych faktur 	-
* 	description missing 	-
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
dateCreated
required
	
string <date-time>

Data utworzenia sesji.
dateUpdated
required
	
string <date-time>

Data ostatniej aktywności w ramach sesji.
validUntil	
string or null <date-time>

Termin ważności sesji. Po jego upływie sesja zostanie automatycznie zamknięta.
	
object or null

Informacja o UPO sesyjnym, zwracana gdy sesja została zamknięta i UPO zostało wygenerowane.
required
	
Array of objects (UpoPageResponse)

Lista stron UPO.
Array
referenceNumber
required
	
string = 36 characters

Numer referencyjny strony UPO.
downloadUrl
required
	
string <uri>

Adres do pobrania strony UPO. Link generowany jest przy każdym odpytaniu o status. Dostęp odbywa się metodą HTTP GET i nie należy wysyłać tokenu dostępowego. Link nie podlega limitom API i wygasa po określonym czasie w DownloadUrlExpirationDate.

Odpowiedź HTTP zawiera dodatkowe nagłówki:

    x-ms-meta-hash – skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64.

downloadUrlExpirationDate
required
	
string <date-time>

Data i godzina wygaśnięcia adresu. Po tej dacie link DownloadUrl nie będzie już aktywny.
invoiceCount	
integer or null <int32> >= 0

Liczba przyjętych faktur w ramach sesji.
successfulInvoiceCount	
integer or null <int32> >= 0

Liczba faktur przeprocesowanych w ramach sesji z sukcesem .
failedInvoiceCount	
integer or null <int32> >= 0

Liczba faktur przeprocesowanych w ramach sesji z błędem.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	1200 	12000 	sessionMisc
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "status": {
        "code": 200,
        "description": "Sesja interaktywna przetworzona pomyślnie"
    },
    "dateCreated": "2025-09-18T15:00:30+00:00",
    "dateUpdated": "2025-09-18T15:01:20+00:00",
    "upo": {
        "pages": []
    },
    "invoiceCount": 10,
    "successfulInvoiceCount": 8,
    "failedInvoiceCount": 2

}
Pobranie faktur sesji

Zwraca listę faktur przesłanych w sesji wraz z ich statusami, oraz informacje na temat ilości poprawnie i niepoprawnie przetworzonych faktur.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
query Parameters
pageSize	
integer <int32> [ 10 .. 1000 ]
Default: 10

Rozmiar strony wyników.
header Parameters
x-continuation-token	
string

Token służący do pobrania kolejnej strony wyników.
Responses
Response Schema: application/json
continuationToken	
string or null

Token służący do pobrania kolejnej strony wyników. Jeśli jest pusty, to nie ma kolejnych stron.
required
	
Array of objects (SessionInvoiceStatusResponse)

Lista pobranych faktur.
Array
ordinalNumber
required
	
integer <int32> >= 1

Numer sekwencyjny faktury w ramach sesji.
invoiceNumber	
string or null <= 256 characters

Numer faktury.
ksefNumber	
string or null [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF.
referenceNumber
required
	
string = 36 characters

Numer referencyjny faktury.
invoiceHash
required
	
string <byte> = 44 characters

Skrót SHA256 faktury, zakodowany w formacie Base64.
invoiceFileName	
string or null <= 128 characters

Nazwa pliku faktury (zwracana dla faktur wysyłanych wsadowo).
acquisitionDate	
string or null <date-time>

Data nadania numeru KSeF.
invoicingDate
required
	
string <date-time>

Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
permanentStorageDate	
string or null <date-time>

Data trwałego zapisu faktury w repozytorium KSeF. Wartość uzupełniana asynchronicznie w momencie trwałego zapisu; zawsze późniejsza niż acquisitionDate. Podczas sprawdzania statusu może być jeszcze niedostępna.
upoDownloadUrl	
string or null <uri>

Adres do pobrania UPO. Link generowany jest przy każdym odpytaniu o status. Dostęp odbywa się metodą HTTP GET i nie należy wysyłać tokenu dostępowego. Link nie podlega limitom API i wygasa po określonym czasie w UpoDownloadUrlExpirationDate.

Odpowiedź HTTP zawiera dodatkowe nagłówki:

    x-ms-meta-hash – skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64.

upoDownloadUrlExpirationDate	
string or null <date-time>

Data i godzina wygaśnięcia adresu. Po tej dacie link UpoDownloadUrl nie będzie już aktywny.
invoicingMode	
string or null
Enum: "Online" "Offline"

Tryb fakturowania (online/offline).
required
	
object

Status faktury.
Code 	Description 	Details 	Extensions
100 	Faktura przyjęta do dalszego przetwarzania 	- 	-
150 	Trwa przetwarzanie 	- 	-
200 	Sukces 	- 	-
405 	Przetwarzanie anulowane z powodu błędu sesji 	- 	-
410 	Nieprawidłowy zakres uprawnień 	- 	-
415 	Brak możliwości wysyłania faktury z załącznikiem 	- 	-
430 	Błąd weryfikacji pliku faktury 	- 	-
435 	Błąd odszyfrowania pliku 	- 	-
440 	Duplikat faktury 	- 	'originalSessionReferenceNumber', 'originalKsefNumber'
450 	Błąd weryfikacji semantyki dokumentu faktury 	- 	-
500 	Nieznany błąd ({statusCode}) 	- 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie 	-
code
required
	
integer <int32>

Kod statusu faktury
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
	
object or null

Zbiór dodatkowych informacji związanych ze statusem faktury, zapisanych jako pary klucz–wartość. Umożliwia rozszerzenie modelu o dane specyficzne dla danego przypadku.
property name*
additional property
	
string or null
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	200 	2000 	sessionInvoiceList
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "continuationToken": "W34idG9rZW4iOiIrUklEOn4xUE5BQU5hcXJVOUFBQUFBQUFBQUFBPT0jUlQ6MSNUUkM6MTAjSVNWOjIjSUVPOjY1NTY3I1FDRjo4I0ZQQzpBVUFBQUFBQUFBQUFRZ0FBQUFBQUFBQT0iLCJyYW5nZSI6eyJtaW4iOiIiLCJtYXgiOiJGRiJ9fV0=",
    "invoices": [
        {},
        {}
    ]

}
Pobranie statusu faktury z sesji

Zwraca fakturę przesłaną w sesji wraz ze statusem.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
invoiceReferenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny faktury.
Responses
Response Schema: application/json
ordinalNumber
required
	
integer <int32> >= 1

Numer sekwencyjny faktury w ramach sesji.
invoiceNumber	
string or null <= 256 characters

Numer faktury.
ksefNumber	
string or null [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF.
referenceNumber
required
	
string = 36 characters

Numer referencyjny faktury.
invoiceHash
required
	
string <byte> = 44 characters

Skrót SHA256 faktury, zakodowany w formacie Base64.
invoiceFileName	
string or null <= 128 characters

Nazwa pliku faktury (zwracana dla faktur wysyłanych wsadowo).
acquisitionDate	
string or null <date-time>

Data nadania numeru KSeF.
invoicingDate
required
	
string <date-time>

Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
permanentStorageDate	
string or null <date-time>

Data trwałego zapisu faktury w repozytorium KSeF. Wartość uzupełniana asynchronicznie w momencie trwałego zapisu; zawsze późniejsza niż acquisitionDate. Podczas sprawdzania statusu może być jeszcze niedostępna.
upoDownloadUrl	
string or null <uri>

Adres do pobrania UPO. Link generowany jest przy każdym odpytaniu o status. Dostęp odbywa się metodą HTTP GET i nie należy wysyłać tokenu dostępowego. Link nie podlega limitom API i wygasa po określonym czasie w UpoDownloadUrlExpirationDate.

Odpowiedź HTTP zawiera dodatkowe nagłówki:

    x-ms-meta-hash – skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64.

upoDownloadUrlExpirationDate	
string or null <date-time>

Data i godzina wygaśnięcia adresu. Po tej dacie link UpoDownloadUrl nie będzie już aktywny.
invoicingMode	
string or null
Enum: "Online" "Offline"

Tryb fakturowania (online/offline).
required
	
object

Status faktury.
Code 	Description 	Details 	Extensions
100 	Faktura przyjęta do dalszego przetwarzania 	- 	-
150 	Trwa przetwarzanie 	- 	-
200 	Sukces 	- 	-
405 	Przetwarzanie anulowane z powodu błędu sesji 	- 	-
410 	Nieprawidłowy zakres uprawnień 	- 	-
415 	Brak możliwości wysyłania faktury z załącznikiem 	- 	-
430 	Błąd weryfikacji pliku faktury 	- 	-
435 	Błąd odszyfrowania pliku 	- 	-
440 	Duplikat faktury 	- 	'originalSessionReferenceNumber', 'originalKsefNumber'
450 	Błąd weryfikacji semantyki dokumentu faktury 	- 	-
500 	Nieznany błąd ({statusCode}) 	- 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie 	-
code
required
	
integer <int32>

Kod statusu faktury
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
	
object or null

Zbiór dodatkowych informacji związanych ze statusem faktury, zapisanych jako pary klucz–wartość. Umożliwia rozszerzenie modelu o dane specyficzne dla danego przypadku.
property name*
additional property
	
string or null
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	300 	1200 	12000 	invoiceStatus
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "ordinalNumber": 2,
    "referenceNumber": "20250626-EE-2F20AD2000-242386DF86-52",
    "invoicingDate": "2025-07-11T12:23:56.0154302+00:00",
    "status": {
        "code": 440,
        "description": "Duplikat faktury",
        "details": [],
        "extensions": {}
    }

}
Pobranie niepoprawnie przetworzonych faktur sesji

Zwraca listę niepoprawnie przetworzonych faktur przesłanych w sesji wraz z ich statusami.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
query Parameters
pageSize	
integer <int32> [ 10 .. 1000 ]
Default: 10

Rozmiar strony wyników.
header Parameters
x-continuation-token	
string

Token służący do pobrania kolejnej strony wyników.
Responses
Response Schema: application/json
continuationToken	
string or null

Token służący do pobrania kolejnej strony wyników. Jeśli jest pusty, to nie ma kolejnych stron.
required
	
Array of objects (SessionInvoiceStatusResponse)

Lista pobranych faktur.
Array
ordinalNumber
required
	
integer <int32> >= 1

Numer sekwencyjny faktury w ramach sesji.
invoiceNumber	
string or null <= 256 characters

Numer faktury.
ksefNumber	
string or null [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF.
referenceNumber
required
	
string = 36 characters

Numer referencyjny faktury.
invoiceHash
required
	
string <byte> = 44 characters

Skrót SHA256 faktury, zakodowany w formacie Base64.
invoiceFileName	
string or null <= 128 characters

Nazwa pliku faktury (zwracana dla faktur wysyłanych wsadowo).
acquisitionDate	
string or null <date-time>

Data nadania numeru KSeF.
invoicingDate
required
	
string <date-time>

Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
permanentStorageDate	
string or null <date-time>

Data trwałego zapisu faktury w repozytorium KSeF. Wartość uzupełniana asynchronicznie w momencie trwałego zapisu; zawsze późniejsza niż acquisitionDate. Podczas sprawdzania statusu może być jeszcze niedostępna.
upoDownloadUrl	
string or null <uri>

Adres do pobrania UPO. Link generowany jest przy każdym odpytaniu o status. Dostęp odbywa się metodą HTTP GET i nie należy wysyłać tokenu dostępowego. Link nie podlega limitom API i wygasa po określonym czasie w UpoDownloadUrlExpirationDate.

Odpowiedź HTTP zawiera dodatkowe nagłówki:

    x-ms-meta-hash – skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64.

upoDownloadUrlExpirationDate	
string or null <date-time>

Data i godzina wygaśnięcia adresu. Po tej dacie link UpoDownloadUrl nie będzie już aktywny.
invoicingMode	
string or null
Enum: "Online" "Offline"

Tryb fakturowania (online/offline).
required
	
object

Status faktury.
Code 	Description 	Details 	Extensions
100 	Faktura przyjęta do dalszego przetwarzania 	- 	-
150 	Trwa przetwarzanie 	- 	-
200 	Sukces 	- 	-
405 	Przetwarzanie anulowane z powodu błędu sesji 	- 	-
410 	Nieprawidłowy zakres uprawnień 	- 	-
415 	Brak możliwości wysyłania faktury z załącznikiem 	- 	-
430 	Błąd weryfikacji pliku faktury 	- 	-
435 	Błąd odszyfrowania pliku 	- 	-
440 	Duplikat faktury 	- 	'originalSessionReferenceNumber', 'originalKsefNumber'
450 	Błąd weryfikacji semantyki dokumentu faktury 	- 	-
500 	Nieznany błąd ({statusCode}) 	- 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie 	-
code
required
	
integer <int32>

Kod statusu faktury
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
	
object or null

Zbiór dodatkowych informacji związanych ze statusem faktury, zapisanych jako pary klucz–wartość. Umożliwia rozszerzenie modelu o dane specyficzne dla danego przypadku.
property name*
additional property
	
string or null
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	200 	2000 	sessionInvoiceList
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "continuationToken": "...",
    "invoices": [
        {}
    ]

}
Pobranie UPO faktury z sesji na podstawie numeru KSeF

Zwraca UPO faktury przesłanego w sesji na podstawie jego numeru KSeF.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
ksefNumber
required
	
string (KsefNumber) [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF faktury.
Responses
Response Headers x-ms-meta-hash	
string <byte> (Sha256HashBase64) = 44 characters

Skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64
Response Schema: application/xml
string
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	1200 	12000 	sessionMisc
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Pobranie UPO faktury z sesji na podstawie numeru referencyjnego faktury

Zwraca UPO faktury przesłanego w sesji na podstawie jego numeru KSeF.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
invoiceReferenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny faktury.
Responses
Response Headers x-ms-meta-hash	
string <byte> (Sha256HashBase64) = 44 characters

Skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64
Response Schema: application/xml
string
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	1200 	12000 	sessionMisc
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Pobranie UPO dla sesji

Zwraca XML zawierający zbiorcze UPO dla sesji.

Wymagane uprawnienia: InvoiceWrite, Introspection, PefInvoiceWrite, EnforcementOperations.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny sesji.
upoReferenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny UPO.
Responses
Response Headers x-ms-meta-hash	
string <byte> (Sha256HashBase64) = 44 characters

Skrót SHA-256 dokumentu UPO, zakodowany w formacie Base64
Response Schema: application/xml
string
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	1200 	12000 	sessionMisc
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Pobieranie faktur
Pobranie faktury po numerze KSeF

Zwraca fakturę o podanym numerze KSeF.

Wymagane uprawnienia: InvoiceRead.
Authorizations:
Bearer
path Parameters
ksefNumber
required
	
string (KsefNumber) [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF faktury.
Responses
Response Headers x-ms-meta-hash	
string <byte> (Sha256HashBase64) = 44 characters

Skrót SHA-256 faktury, zakodowany w formacie Base64
Response Schema: application/xml
string
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	80 	160 	640 	invoiceDownload
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Pobranie listy metadanych faktur

Zwraca metadane faktur spełniających filtry.

Limit techniczny: ≤ 10 000 rekordów na zestaw filtrów, po jego osiągnięciu isTruncated = true i należy ponownie ustawić dateRange, używając ostatniej daty z wyników (tj. ustawić from/to - w zależności od kierunku sortowania, od daty ostatniego zwróconego rekordu) oraz wyzerować pageOffset.

Do scenariusza przyrostowego należy używać daty PermanentStorage oraz kolejność sortowania Asc.

Scenariusz pobierania przyrostowego (skrót):

    Gdy hasMore = false, należy zakończyć,
    Gdy hasMore = true i isTruncated = false, należy zwiększyć pageOffset,
    Gdy hasMore = true i isTruncated = true, należy zawęzić dateRange (ustawić from od daty ostatniego rekordu), wyzerować pageOffset i kontynuować

Sortowanie:

    permanentStorageDate | invoicingDate | issueDate (Asc | Desc) - pole wybierane na podstawie filtrów

Wymagane uprawnienia: InvoiceRead.
Authorizations:
Bearer
query Parameters
sortOrder	
string
Default: "Asc"
Enum: "Asc" "Desc"

Kolejność sortowania wyników.
Wartość 	Opis
Asc 	Sortowanie rosnąco.
Desc 	Sortowanie malejąco.
pageOffset	
integer <int32> >= 0
Default: 0

Indeks pierwszej strony wyników (0 = pierwsza strona).
pageSize	
integer <int32> [ 10 .. 250 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json

Kryteria filtrowania.
subjectType
required
	
string
Enum: "Subject1" "Subject2" "Subject3" "SubjectAuthorized"

Typ podmiotu, którego dotyczą kryteria filtrowania metadanych faktur. Określa kontekst, w jakim przeszukiwane są dane.
Wartość 	Opis
Subject1 	Podmiot 1 - sprzedawca
Subject2 	Podmiot 2 - nabywca
Subject3 	Podmiot 3
SubjectAuthorized 	Podmiot upoważniony
required
	
object

Typ i zakres dat, według którego filtrowane są faktury. Maksymalny dozwolony okres wynosi 3 miesiące w strefie UTC lub w strefie Europe/Warsaw (WAW).

Format daty:

    Daty muszą być przekazane w formacie ISO 8601, np. yyyy-MM-ddTHH:mm:ss.
    Dopuszczalne są następujące warianty:
        z sufiksem Z (czas UTC),
        z jawnym offsetem, np. +01:00, +03:00,
        bez offsetu (interpretowane jako czas lokalny strefy Europe/Warsaw).

Zasady interpretacji dat:

    Daty z sufiksem Z są traktowane jako czas UTC.
    Daty bez jawnie podanego offsetu są interpretowane jako czas lokalny strefy Europe/Warsaw (WAW).
    Daty z jawnym offsetem (+01:00, +08:00 itd.) są przeliczane z uwzględnieniem offsetu, a następnie walidowane w strefie UTC lub w strefie Europe/Warsaw (WAW).

dateType
required
	
string
Enum: "Issue" "Invoicing" "PermanentStorage"

Typ daty, według której ma być zastosowany zakres.
Wartość 	Opis
Issue 	Data wystawienia faktury.
Invoicing 	Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
PermanentStorage 	Data trwałego zapisu faktury w repozytorium systemu KSeF.
from
required
	
string <date-time>

Data początkowa zakresu w formacie ISO-8601 np. 2026-01-03T13:45:00+00:00.
to	
string or null <date-time>

Data końcowa zakresu w formacie ISO-8601. Jeśli nie zostanie podana, przyjmowana jest bieżąca data i czas w UTC.
restrictToPermanentStorageHwmDate	
boolean or null

Określa, czy system ma ograniczyć filtrowanie (zakres dateRange.to) do wartości PermanentStorageHwmDate.

    Dotyczy wyłącznie zapytań z dateType = PermanentStorage,
    Gdy true, system ogranicza filtrowanie tak, aby wartość dateRange.to nie przekraczała wartości PermanentStorageHwmDate,
    Gdy null lub false, filtrowanie może wykraczać poza PermanentStorageHwmDate.

ksefNumber	
string or null [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF faktury (exact match).
invoiceNumber	
string or null <= 256 characters

Numer faktury nadany przez wystawcę (exact match).
	
object or null

Filtr kwotowy – brutto, netto lub VAT (z wartością).
type
required
	
string
Enum: "Brutto" "Netto" "Vat"
from	
number or null <double>
to	
number or null <double>
sellerNip	
string or null = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

Nip sprzedawcy (exact match).
	
object or null

Identyfikator nabywcy.
Type 	Value
Nip 	10 cyfrowy numer NIP
VatUe 	Identyfikator VAT UE podmiotu unijnego.
Other 	Inny identyfikator
None 	Brak identyfikatora nabywcy
type
required
	
string
Enum: "Nip" "VatUe" "Other" "None"

Typ identyfikatora nabywcy.
Wartość 	Opis
Nip 	10 cyfrowy numer NIP
VatUe 	Identyfikator VAT UE podmiotu unijnego
Other 	Inny identyfikator
None 	Brak identyfikatora nabywcy
value	
string or null <= 50 characters

Wartość identyfikatora nabywcy (exact match).
currencyCodes	
Array of strings or null (CurrencyCode)
Enum: "AED" "AFN" "ALL" "AMD" "ANG" "AOA" "ARS" "AUD" "AWG" "AZN" "BAM" "BBD" "BDT" "BGN" "BHD" "BIF" "BMD" "BND" "BOB" "BOV" "BRL" "BSD" "BTN" "BWP" "BYN" "BZD" "CAD" "CDF" "CHE" "CHF" "CHW" "CLF" "CLP" "CNY" "COP" "COU" "CRC" "CUC" "CUP" "CVE" "CZK" "DJF" "DKK" "DOP" "DZD" "EGP" "ERN" "ETB" "EUR" "FJD" "FKP" "GBP" "GEL" "GGP" "GHS" "GIP" "GMD" "GNF" "GTQ" "GYD" "HKD" "HNL" "HRK" "HTG" "HUF" "IDR" "ILS" "IMP" "INR" "IQD" "IRR" "ISK" "JEP" "JMD" "JOD" "JPY" "KES" "KGS" "KHR" "KMF" "KPW" "KRW" "KWD" "KYD" "KZT" "LAK" "LBP" "LKR" "LRD" "LSL" "LYD" "MAD" "MDL" "MGA" "MKD" "MMK" "MNT" "MOP" "MRU" "MUR" "MVR" "MWK" "MXN" "MXV" "MYR" "MZN" "NAD" "NGN" "NIO" "NOK" "NPR" "NZD" "OMR" "PAB" "PEN" "PGK" "PHP" "PKR" "PLN" "PYG" "QAR" "RON" "RSD" "RUB" "RWF" "SAR" "SBD" "SCR" "SDG" "SEK" "SGD" "SHP" "SLL" "SOS" "SRD" "SSP" "STN" "SVC" "SYP" "SZL" "THB" "TJS" "TMT" "TND" "TOP" "TRY" "TTD" "TWD" "TZS" "UAH" "UGX" "USD" "USN" "UYI" "UYU" "UYW" "UZS" "VES" "VND" "VUV" "WST" "XAF" "XAG" "XAU" "XBA" "XBB" "XBC" "XBD" "XCD" "XCG" "XDR" "XOF" "XPD" "XPF" "XPT" "XSU" "XUA" "XXX" "YER" "ZAR" "ZMW" "ZWL"

Kody walut.
invoicingMode	
string or null
Enum: "Online" "Offline"

Tryb wystawienia faktury: online lub offline.
isSelfInvoicing	
boolean or null

Czy faktura została wystawiona w trybie samofakturowania.
formType	
string or null
Enum: "FA" "PEF" "RR"

Typ dokumentu.
Wartość 	Opis
FA 	Faktura VAT
PEF 	Faktura PEF
RR 	Faktura RR
invoiceTypes	
Array of strings or null (InvoiceType)
Enum: "Vat" "Zal" "Kor" "Roz" "Upr" "KorZal" "KorRoz" "VatPef" "VatPefSp" "KorPef" "VatRr" "KorVatRr"

Rodzaje faktur.
Wartość 	Opis
Vat 	(FA) Podstawowa
Zal 	(FA) Zaliczkowa
Kor 	(FA) Korygująca
Roz 	(FA) Rozliczeniowa
Upr 	(FA) Uproszczona
KorZal 	(FA) Korygująca fakturę zaliczkową
KorRoz 	(FA) Korygująca fakturę rozliczeniową
VatPef 	(PEF) Podstawowa
VatPefSp 	(PEF) Specjalizowana
KorPef 	(PEF) Korygująca
VatRr 	(RR) Podstawowa
KorVatRr 	(RR) Korygująca
hasAttachment	
boolean or null

Czy faktura ma załącznik.
Responses
Response Schema: application/json
hasMore
required
	
boolean

Określa, czy istnieją kolejne wyniki zapytania.
isTruncated
required
	
boolean

Określa, czy osiągnięto maksymalny dopuszczalny zakres wyników zapytania (10 000).
permanentStorageHwmDate	
string or null <date-time>

Dotyczy wyłącznie zapytań filtrowanych po typie daty PermanentStorage. Jeśli zapytanie dotyczyło najnowszego okresu, wartość ta może być wartością nieznacznie skorygowaną względem górnej granicy podanej w warunkach zapytania. Dla okresów starszych, będzie to zgodne z warunkami zapytania.

Wartość jest stała dla wszystkich stron tego samego zapytania i nie zależy od paginacji ani sortowania.

System gwarantuje, że dane poniżej tej wartości są spójne i kompletne. Ponowne zapytania obejmujące zakresem dane poniżej tego kroczącego znacznika czasu nie zwrócą w przyszłości innych wyników (np.dodatkowych faktur).

Dla dateType = Issue lub Invoicing – null.
required
	
Array of objects (InvoiceMetadata)

Lista faktur spełniających kryteria.
Array
ksefNumber
required
	
string [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF faktury.
invoiceNumber
required
	
string <= 256 characters

Numer faktury nadany przez wystawcę.
issueDate
required
	
string <date>

Data wystawienia faktury.
invoicingDate
required
	
string <date-time>

Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
acquisitionDate
required
	
string <date-time>

Data nadania numeru KSeF.
permanentStorageDate
required
	
string <date-time>

Data trwałego zapisu faktury w repozytorium systemu KSeF.
required
	
object

Dane identyfikujące sprzedawcę.
nip
required
	
string = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

Nip sprzedawcy.
name	
string or null <= 512 characters

Nazwa sprzedawcy.
required
	
object

Dane identyfikujące nabywcę.
required
	
object

Identyfikator nabywcy.
Type 	Value
Nip 	10 cyfrowy numer NIP
VatUe 	Identyfikator VAT UE podmiotu unijnego
Other 	Inny identyfikator
None 	Brak identyfikatora nabywcy
type
required
	
string
Enum: "Nip" "VatUe" "Other" "None"

Typ identyfikatora nabywcy.
Wartość 	Opis
Nip 	10 cyfrowy numer NIP
VatUe 	Identyfikator VAT UE podmiotu unijnego
Other 	Inny identyfikator
None 	Brak identyfikatora nabywcy
value	
string or null <= 50 characters

Wartość identyfikatora nabywcy.
name	
string or null <= 512 characters

Nazwa nabywcy.
netAmount
required
	
number <double>

Łączna kwota netto.
grossAmount
required
	
number <double>

Łączna kwota brutto.
vatAmount
required
	
number <double>

Łączna kwota VAT.
currency
required
	
string = 3 characters

Kod waluty.
invoicingMode
required
	
string
Enum: "Online" "Offline"

Tryb fakturowania (online/offline).
invoiceType
required
	
string
Enum: "Vat" "Zal" "Kor" "Roz" "Upr" "KorZal" "KorRoz" "VatPef" "VatPefSp" "KorPef" "VatRr" "KorVatRr"

Rodzaj faktury.
Wartość 	Opis
Vat 	(FA) Podstawowa
Zal 	(FA) Zaliczkowa
Kor 	(FA) Korygująca
Roz 	(FA) Rozliczeniowa
Upr 	(FA) Uproszczona
KorZal 	(FA) Korygująca fakturę zaliczkową
KorRoz 	(FA) Korygująca fakturę rozliczeniową
VatPef 	(PEF) Podstawowa
VatPefSp 	(PEF) Specjalizowana
KorPef 	(PEF) Korygująca
VatRr 	(RR) Podstawowa
KorVatRr 	(RR) Korygująca
required
	
object

Struktura dokumentu faktury.

Obsługiwane schematy:
SystemCode 	SchemaVersion 	Value
FA (2) 	1-0E 	FA
FA (3) 	1-0E 	FA
PEF (3) 	2-1 	PEF
PEF_KOR (3) 	2-1 	PEF
FA_RR (1) 	1-0E 	RR
systemCode
required
	
string

Kod systemowy
schemaVersion
required
	
string

Wersja schematu
value
required
	
string

Wartość
isSelfInvoicing
required
	
boolean

Czy faktura została wystawiona w trybie samofakturowania.
hasAttachment
required
	
boolean

Określa, czy faktura posiada załącznik.
invoiceHash
required
	
string <byte> = 44 characters

Skrót SHA256 faktury, zakodowany w formacie Base64.
hashOfCorrectedInvoice	
string or null <byte> = 44 characters

Skrót SHA256 korygowanej faktury, zakodowany w formacie Base64.
	
Array of objects or null (InvoiceMetadataThirdSubject)

Lista podmiotów trzecich.
Array
required
	
object
type
required
	
string
Enum: "Nip" "InternalId" "VatUe" "Other" "None"

Typ identyfikatora podmiotu trzeciego.
Wartość 	Opis
Nip 	10 cyfrowy numer NIP
InternalId 	Identyfikator wewnętrzny, składający się z numeru NIP i 5 cyfr.
VatUe 	Identyfikator VAT UE podmiotu unijnego
Other 	Inny identyfikator
None 	Brak identyfikatora podmiotu trzeciego
value	
string or null <= 50 characters

Wartość identyfikatora podmiotu trzeciego.
name	
string or null <= 512 characters

Nazwa podmiotu trzeciego.
role
required
	
integer <int32>

Rola podmiotu trzeciego.
Wartość 	Opis
0 	Inna rola
1 	Faktor - w przypadku gdy na fakturze występują dane faktora
2 	Odbiorca - w przypadku gdy na fakturze występują dane jednostek wewnętrznych, oddziałów, wyodrębnionych w ramach nabywcy, które same nie stanowią nabywcy w rozumieniu ustawy
3 	Podmiot pierwotny - w przypadku gdy na fakturze występują dane podmiotu będącego w stosunku do podatnika podmiotem przejętym lub przekształconym, który dokonywał dostawy lub świadczył usługę. Z wyłączeniem przypadków, o których mowa w art. 106j ust.2 pkt 3 ustawy, gdy dane te wykazywane są w części Podmiot1K
4 	Dodatkowy nabywca - w przypadku gdy na fakturze występują dane kolejnych (innych niż wymieniony w części Podmiot2) nabywców
5 	Wystawca faktury - w przypadku gdy na fakturze występują dane podmiotu wystawiającego fakturę w imieniu podatnika. Nie dotyczy przypadku, gdy wystawcą faktury jest nabywca
6 	Dokonujący płatności - w przypadku gdy na fakturze występują dane podmiotu regulującego zobowiązanie w miejsce nabywcy
7 	Jednostka samorządu terytorialnego - wystawca
8 	Jednostka samorządu terytorialnego - odbiorca
9 	Członek grupy VAT - wystawca
10 	Członek grupy VAT - odbiorca
11 	Pracownik
	
object or null

Podmiot upoważniony.
nip
required
	
string = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

Nip podmiotu upoważnionego
name	
string or null <= 512 characters

Nazwa podmiotu upoważnionego.
role
required
	
integer <int32>

Rola podmiotu upoważnionego.
Wartość 	Opis
1 	Organ egzekucyjny - w przypadku, o którym mowa w art. 106c pkt 1 ustawy
2 	Komornik sądowy - w przypadku, o którym mowa w art. 106c pkt 2 ustawy
3 	Przedstawiciel podatkowy - w przypadku gdy na fakturze występują dane przedstawiciela podatkowego, o którym mowa w art. 18a - 18d ustawy
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	80 	160 	200 	invoiceMetadata
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectType": "Subject1",
    "dateRange": {
        "dateType": "PermanentStorage",
        "from": "2025-08-28T09:22:13.388+00:00",
        "to": "2025-09-28T09:24:13.388+00:00"
    },
    "amount": {
        "type": "Brutto",
        "from": 100.5,
        "to": 250
    },
    "currencyCodes": [
        "PLN",
        "EUR"
    ],
    "invoicingMode": "Online",
    "formType": "FA",
    "invoiceTypes": [
        "Vat"
    ],
    "hasAttachment": true

}
Response samples

    200400429

Content type
application/json
{

    "hasMore": false,
    "isTruncated": false,
    "permanentStorageHwmDate": "2025-08-28T09:23:55.388+00:00",
    "invoices": [
        {},
        {}
    ]

}
Eksport paczki faktur

Rozpoczyna asynchroniczny proces wyszukiwania faktur w systemie KSeF na podstawie przekazanych filtrów oraz przygotowania ich w formie zaszyfrowanej paczki. Wymagane jest przekazanie informacji o szyfrowaniu w polu Encryption, które służą do zabezpieczenia przygotowanej paczki z fakturami. Maksymalnie można uruchomić 10 równoczesnych eksportów w zalogowanym kontekście.

System pobiera faktury rosnąco według daty określonej w filtrze (Invoicing, Issue, PermanentStorage) i dodaje faktury(nazwa pliku: {ksefNumber}.xml) do paczki aż do osiągnięcia jednego z poniższych limitów:

    Limit liczby faktur: 10 000 sztuk
    Limit rozmiaru danych(skompresowanych): 1GB

Paczka eksportu zawiera dodatkowy plik z metadanymi faktur w formacie JSON (_metadata.json). Zawartość pliku to obiekt z tablicą invoices, gdzie każdy element jest obiektem typu InvoiceMetadata (taki jak zwracany przez endpoint POST /invoices/query/metadata).

Plik z metadanymi(_metadata.json) nie jest wliczany do limitów algorytmu budowania paczki.

Do realizacji pobierania przyrostowego należy stosować filtrowanie po dacie PermanentStorage.

Sortowanie:

    permanentStorageDate | invoicingDate | issueDate (Asc) - pole wybierane na podstawie filtrów

Wymagane uprawnienia: InvoiceRead.
Authorizations:
Bearer
Request Body schema: application/json

Dane wejściowe określające kryteria i format eksportu paczki faktur.
required
	
object

Informacje wymagane do zaszyfrowania wyniku zapytania.
encryptedSymmetricKey
required
	
string <byte>

Klucz symetryczny o długości 32 bajtów, zaszyfrowany algorytmem RSA (Padding: OAEP z SHA-256), zakodowany w formacie Base64.

Klucz publiczny Ministerstwa Finansów
initializationVector
required
	
string <byte>

Wektor inicjalizujący (IV) o długości 16 bajtów, używany do szyfrowania symetrycznego, zakodowany w formacie Base64.
required
	
object

Zestaw filtrów do wyszukiwania faktur.
subjectType
required
	
string
Enum: "Subject1" "Subject2" "Subject3" "SubjectAuthorized"

Typ podmiotu, którego dotyczą kryteria filtrowania metadanych faktur. Określa kontekst, w jakim przeszukiwane są dane.
Wartość 	Opis
Subject1 	Podmiot 1 - sprzedawca
Subject2 	Podmiot 2 - nabywca
Subject3 	Podmiot 3
SubjectAuthorized 	Podmiot upoważniony
required
	
object

Typ i zakres dat, według którego filtrowane są faktury. Maksymalny dozwolony okres wynosi 3 miesiące w strefie UTC lub w strefie Europe/Warsaw (WAW).

Format daty:

    Daty muszą być przekazane w formacie ISO 8601, np. yyyy-MM-ddTHH:mm:ss.
    Dopuszczalne są następujące warianty:
        z sufiksem Z (czas UTC),
        z jawnym offsetem, np. +01:00, +03:00,
        bez offsetu (interpretowane jako czas lokalny strefy Europe/Warsaw).

Zasady interpretacji dat:

    Daty z sufiksem Z są traktowane jako czas UTC.
    Daty bez jawnie podanego offsetu są interpretowane jako czas lokalny strefy Europe/Warsaw (WAW).
    Daty z jawnym offsetem (+01:00, +08:00 itd.) są przeliczane z uwzględnieniem offsetu, a następnie walidowane w strefie UTC lub w strefie Europe/Warsaw (WAW).

dateType
required
	
string
Enum: "Issue" "Invoicing" "PermanentStorage"

Typ daty, według której ma być zastosowany zakres.
Wartość 	Opis
Issue 	Data wystawienia faktury.
Invoicing 	Data przyjęcia faktury w systemie KSeF (do dalszego przetwarzania).
PermanentStorage 	Data trwałego zapisu faktury w repozytorium systemu KSeF.
from
required
	
string <date-time>

Data początkowa zakresu w formacie ISO-8601 np. 2026-01-03T13:45:00+00:00.
to	
string or null <date-time>

Data końcowa zakresu w formacie ISO-8601. Jeśli nie zostanie podana, przyjmowana jest bieżąca data i czas w UTC.
restrictToPermanentStorageHwmDate	
boolean or null

Określa, czy system ma ograniczyć filtrowanie (zakres dateRange.to) do wartości PermanentStorageHwmDate.

    Dotyczy wyłącznie zapytań z dateType = PermanentStorage,
    Gdy true, system ogranicza filtrowanie tak, aby wartość dateRange.to nie przekraczała wartości PermanentStorageHwmDate,
    Gdy null lub false, filtrowanie może wykraczać poza PermanentStorageHwmDate.

ksefNumber	
string or null [ 35 .. 36 ] characters ^([1-9](\d[1-9]|[1-9]\d)\d{7})-(20[2-9][0-9]|...

Numer KSeF faktury (exact match).
invoiceNumber	
string or null <= 256 characters

Numer faktury nadany przez wystawcę (exact match).
	
object or null

Filtr kwotowy – brutto, netto lub VAT (z wartością).
type
required
	
string
Enum: "Brutto" "Netto" "Vat"
from	
number or null <double>
to	
number or null <double>
sellerNip	
string or null = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

Nip sprzedawcy (exact match).
	
object or null

Identyfikator nabywcy.
Type 	Value
Nip 	10 cyfrowy numer NIP
VatUe 	Identyfikator VAT UE podmiotu unijnego.
Other 	Inny identyfikator
None 	Brak identyfikatora nabywcy
type
required
	
string
Enum: "Nip" "VatUe" "Other" "None"

Typ identyfikatora nabywcy.
Wartość 	Opis
Nip 	10 cyfrowy numer NIP
VatUe 	Identyfikator VAT UE podmiotu unijnego
Other 	Inny identyfikator
None 	Brak identyfikatora nabywcy
value	
string or null <= 50 characters

Wartość identyfikatora nabywcy (exact match).
currencyCodes	
Array of strings or null (CurrencyCode)
Enum: "AED" "AFN" "ALL" "AMD" "ANG" "AOA" "ARS" "AUD" "AWG" "AZN" "BAM" "BBD" "BDT" "BGN" "BHD" "BIF" "BMD" "BND" "BOB" "BOV" "BRL" "BSD" "BTN" "BWP" "BYN" "BZD" "CAD" "CDF" "CHE" "CHF" "CHW" "CLF" "CLP" "CNY" "COP" "COU" "CRC" "CUC" "CUP" "CVE" "CZK" "DJF" "DKK" "DOP" "DZD" "EGP" "ERN" "ETB" "EUR" "FJD" "FKP" "GBP" "GEL" "GGP" "GHS" "GIP" "GMD" "GNF" "GTQ" "GYD" "HKD" "HNL" "HRK" "HTG" "HUF" "IDR" "ILS" "IMP" "INR" "IQD" "IRR" "ISK" "JEP" "JMD" "JOD" "JPY" "KES" "KGS" "KHR" "KMF" "KPW" "KRW" "KWD" "KYD" "KZT" "LAK" "LBP" "LKR" "LRD" "LSL" "LYD" "MAD" "MDL" "MGA" "MKD" "MMK" "MNT" "MOP" "MRU" "MUR" "MVR" "MWK" "MXN" "MXV" "MYR" "MZN" "NAD" "NGN" "NIO" "NOK" "NPR" "NZD" "OMR" "PAB" "PEN" "PGK" "PHP" "PKR" "PLN" "PYG" "QAR" "RON" "RSD" "RUB" "RWF" "SAR" "SBD" "SCR" "SDG" "SEK" "SGD" "SHP" "SLL" "SOS" "SRD" "SSP" "STN" "SVC" "SYP" "SZL" "THB" "TJS" "TMT" "TND" "TOP" "TRY" "TTD" "TWD" "TZS" "UAH" "UGX" "USD" "USN" "UYI" "UYU" "UYW" "UZS" "VES" "VND" "VUV" "WST" "XAF" "XAG" "XAU" "XBA" "XBB" "XBC" "XBD" "XCD" "XCG" "XDR" "XOF" "XPD" "XPF" "XPT" "XSU" "XUA" "XXX" "YER" "ZAR" "ZMW" "ZWL"

Kody walut.
invoicingMode	
string or null
Enum: "Online" "Offline"

Tryb wystawienia faktury: online lub offline.
isSelfInvoicing	
boolean or null

Czy faktura została wystawiona w trybie samofakturowania.
formType	
string or null
Enum: "FA" "PEF" "RR"

Typ dokumentu.
Wartość 	Opis
FA 	Faktura VAT
PEF 	Faktura PEF
RR 	Faktura RR
invoiceTypes	
Array of strings or null (InvoiceType)
Enum: "Vat" "Zal" "Kor" "Roz" "Upr" "KorZal" "KorRoz" "VatPef" "VatPefSp" "KorPef" "VatRr" "KorVatRr"

Rodzaje faktur.
Wartość 	Opis
Vat 	(FA) Podstawowa
Zal 	(FA) Zaliczkowa
Kor 	(FA) Korygująca
Roz 	(FA) Rozliczeniowa
Upr 	(FA) Uproszczona
KorZal 	(FA) Korygująca fakturę zaliczkową
KorRoz 	(FA) Korygująca fakturę rozliczeniową
VatPef 	(PEF) Podstawowa
VatPefSp 	(PEF) Specjalizowana
KorPef 	(PEF) Korygująca
VatRr 	(RR) Podstawowa
KorVatRr 	(RR) Korygująca
hasAttachment	
boolean or null

Czy faktura ma załącznik.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny eksportu faktur.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	40 	80 	200 	invoiceExport
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "encryption": {
        "encryptedSymmetricKey": "bdUVjqLj+y2q6aBUuLxxXYAMqeDuIBRTyr+hB96DaWKaGzuVHw9p+Nk9vhzgF/Q5cavK2k6eCh6SdsrWI0s9mFFj4A4UJtsyD8Dn3esLfUZ5A1juuG3q3SBi/XOC/+9W+0T/KdwdE393mbiUNyx1K/0bw31vKJL0COeJIDP7usAMDl42/H1TNvkjk+8iZ80V0qW7D+RZdz+tdiY1xV0f2mfgwJ46V0CpZ+sB9UAssRj+eVffavJ0TOg2b5JaBxE8MCAvrF6rO5K4KBjUmoy7PP7g1qIbm8xI2GO0KnfPOO5OWj8rsotRwBgu7x19Ine3qYUvuvCZlXRGGZ5NHIzWPM4O74+gNalaMgFCsmv8mMhETSU4SfAGmJr9edxPjQSbgD5i2X4eDRDMwvyaAa7CP1b2oICju+0L7Fywd2ZtUcr6El++eTVoi8HYsTArntET++gULT7XXjmb8e3O0nxrYiYsE9GMJ7HBGv3NOoJ1NTm3a7U6+c0ZJiBVLvn6xXw10LQX243xH+ehsKo6djQJKYtqcNPaXtCwM1c9RrsOx/wRXyWCtTffqLiaR0LbYvfMJAcEWceG+RaeAx4p37OiQqdJypd6LAv9/0ECWK8Bip8yyoA+0EYiAJb9YuDz2YlQX9Mx9E9FzFIAsgEQ2w723HZYWgPywLb+dlsum4lTZKQ=",
        "initializationVector": "c29tZUluaXRWZWN0b3I="
    },
    "filters": {
        "subjectType": "Subject1",
        "dateRange": {}
    }

}
Response samples

    201400429

Content type
application/json
{

    "referenceNumber": "20251010-EH-1B6C9EB000-4B15D3AEB9-89"

}
Pobranie statusu eksportu paczki faktur

Paczka faktur jest dzielona na części o maksymalnym rozmiarze 50 MB. Każda część jest zaszyfrowana algorytmem AES-256-CBC z dopełnieniem PKCS#7, przy użyciu klucza symetrycznego przekazanego podczas inicjowania eksportu.

W przypadku ucięcia wyniku eksportu z powodu przekroczenia limitów, zwracana jest flaga IsTruncated = true oraz odpowiednia data, którą należy wykorzystać do wykonania kolejnego eksportu, aż do momentu, gdy flaga IsTruncated = false.

Sortowanie:

    permanentStorageDate | invoicingDate | issueDate (Asc) - pole wybierane na podstawie filtrów

Wymagane uprawnienia: InvoiceRead.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny eksportu faktur.
Responses
Response Schema: application/json
required
	
object

Status eksportu.
Code 	Description 	Details
100 	Eksport faktur w toku 	-
200 	Eksport faktur zakończony sukcesem 	-
210 	Eksport faktur wygasł i nie jest już dostępny do pobrania 	-
415 	Błąd odszyfrowania dostarczonego klucza 	-
420 	Zakres filtrowania wykracza poza dostępny zakres danych 	Parametr dateRange.from jest późniejszy niż PermanentStorageHwmDate przy włączonym restrictToPermanentStorageHwmDate.
500 	Nieznany błąd ({statusCode}) 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
completedDate	
string or null <date-time>

Data zakończenia przetwarzania żądania eksportu faktur.
packageExpirationDate	
string or null <date-time>

Data wygaśnięcia paczki faktur przygotowanej do pobrania. Po upływie tej daty paczka nie będzie już dostępna do pobrania.
	
object or null

Dane paczki faktur przygotowanej do pobrania.
invoiceCount
required
	
integer <int64> [ 0 .. 10000 ]

Łączna liczba faktur w paczce.
size
required
	
integer <int64> >= 0

Rozmiar paczki w bajtach.
required
	
Array of objects (InvoicePackagePart)

Lista dostępnych części paczki do pobrania.
Array
ordinalNumber
required
	
integer <int32> >= 1

Numer sekwencyjny pliku części paczki.
partName
required
	
string <= 100 characters

Nazwa pliku części paczki.
method
required
	
string

Metoda HTTP, której należy użyć przy pobieraniu pliku.
url
required
	
string <uri>

Adres URL, pod który należy wysłać żądanie pobrania części paczki. Link jest generowany dynamicznie w momencie odpytania o status operacji eksportu. Nie podlega limitom API i nie wymaga przesyłania tokenu dostępowego przy pobraniu.

Odpowiedź HTTP zawiera dodatkowe nagłówki:

    x-ms-meta-hash – zaszyfrowanej części paczki, zakodowany w formacie Base64.

partSize
required
	
integer <int64> >= 1

Rozmiar części paczki w bajtach.
partHash
required
	
string <byte> = 44 characters

Skrót SHA256 pliku części paczki, zakodowany w formacie Base64.
encryptedPartSize
required
	
integer <int64> >= 1

Rozmiar zaszyfrowanej części paczki w bajtach.
encryptedPartHash
required
	
string <byte> = 44 characters

Skrót SHA256 zaszyfrowanej części paczki, zakodowany w formacie Base64.
expirationDate
required
	
string <date-time>

Data i godzina wygaśnięcia linku umożliwiającego pobranie części paczki. Po upływie tego momentu link przestaje być aktywny.
isTruncated
required
	
boolean

Określa, czy wynik eksportu został ucięty z powodu przekroczenia limitu liczby faktur lub wielkości paczki.
lastIssueDate	
string or null <date>

Data wystawienia ostatniej faktury ujętej w paczce. Pole występuje wyłącznie wtedy, gdy paczka została ucięta i eksport był filtrowany po typie daty Issue.
lastInvoicingDate	
string or null <date-time>

Data przyjęcia ostatniej faktury ujętej w paczce. Pole występuje wyłącznie wtedy, gdy paczka została ucięta i eksport był filtrowany po typie daty Invoicing.
lastPermanentStorageDate	
string or null <date-time>

Data trwałego zapisu ostatniej faktury ujętej w paczce. Pole występuje wyłącznie wtedy, gdy paczka została ucięta i eksport był filtrowany po typie daty PermanentStorage.
permanentStorageHwmDate	
string or null <date-time>

Dotyczy wyłącznie zapytań filtrowanych po typie daty PermanentStorage. Jeśli zapytanie dotyczyło najnowszego okresu, wartość ta może być wartością nieznacznie skorygowaną względem górnej granicy podanej w warunkach zapytania. Dla okresów starszych, będzie to zgodne z warunkami zapytania.

System gwarantuje, że dane poniżej tej wartości są spójne i kompletne. Ponowne zapytania obejmujące zakresem dane poniżej tego kroczącego znacznika czasu nie zwrócą w przyszłości innych wyników (np.dodatkowych faktur).

Dla dateType = Issue lub Invoicing – null.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	600 	6000 	invoiceExportStatus
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "status": {
        "code": 200,
        "description": "Eksport faktur zakończony sukcesem"
    },
    "completedDate": "2025-09-16T16:09:40.901091+00:00",
    "package": {
        "invoiceCount": 10000,
        "size": 22425060,
        "parts": [],
        "isTruncated": true,
        "lastPermanentStorageDate": "2025-09-11T11:40:40.266578+00:00",
        "permanentStorageHwmDate": "2025-09-11T12:00:40.266578+00:00"
    }

}
Nadawanie uprawnień
Nadanie osobom fizycznym uprawnień do pracy w KSeF

Metoda pozwala na nadanie osobie wskazanej w żądaniu uprawnień do pracy w KSeF
w kontekście bieżącym.

W żądaniu określane są nadawane uprawnienia ze zbioru:

    InvoiceWrite – wystawianie faktur,
    InvoiceRead – przeglądanie faktur,
    CredentialsManage – zarządzanie uprawnieniami,
    CredentialsRead – przeglądanie uprawnień,
    Introspection – przeglądanie historii sesji i generowanie UPO,
    SubunitManage – zarządzanie jednostkami podrzędnymi,
    EnforcementOperations – wykonywanie operacji egzekucyjnych.

Metoda pozwala na wybór dowolnej kombinacji powyższych uprawnień.
Uprawnienie EnforcementOperations może być nadane wyłącznie wtedy,
gdy podmiot kontekstu ma rolę EnforcementAuthority (organ egzekucyjny)
lub CourtBailiff (komornik sądowy).

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: CredentialsManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator osoby fizycznej.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
permissions
required
	
Array of strings (PersonPermissionType)
Items Enum: "CredentialsManage" "CredentialsRead" "InvoiceWrite" "InvoiceRead" "Introspection" "SubunitManage" "EnforcementOperations"

Lista nadawanych uprawnień. Każda wartość może wystąpić tylko raz.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
subjectDetailsType
required
	
string
Enum: "PersonByIdentifier" "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych podmiotu.
Wartość 	Opis
PersonByIdentifier 	Osoba fizyczna posługująca się Profilem Zaufanym lub certyfikatem zawierającym identyfikator NIP lub PESEL.
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
required
	
object

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithoutIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
birthDate
required
	
string <date>

Data urodzenia osoby fizycznej.
required
	
object

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Pesel",
        "value": "15062788702"
    },
    "permissions": [
        "InvoiceRead",
        "InvoiceWrite",
        "Introspection",
        "CredentialsRead"
    ],
    "description": "Opis uprawnienia",
    "subjectDetails": {
        "subjectDetailsType": "PersonByIdentifier",
        "personById": {}
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Nadanie podmiotom uprawnień do obsługi faktur

Metoda pozwala na nadanie podmiotowi wskazanemu w żądaniu uprawnień do obsługi faktur podmiotu kontekstu.
W żądaniu określane są nadawane uprawnienia ze zbioru:

    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur

Metoda pozwala na wybór dowolnej kombinacji powyższych uprawnień.
Dla każdego uprawnienia może być ustawiona flaga canDelegate, mówiąca o możliwości jego dalszego przekazywania poprzez nadawanie w sposób pośredni.

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: CredentialsManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator podmiotu.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Value: "Nip"

Typ identyfikatora.
value
required
	
string = 10 characters

Wartość identyfikatora.
required
	
Array of objects (EntityPermission)

Lista nadawanych uprawnień. Każda wartość może wystąpić tylko raz.
Array
type
required
	
string
Enum: "InvoiceWrite" "InvoiceRead"

Rodzaj uprawnienia.
canDelegate	
boolean

Flaga pozwalająca na pośrednie przekazywanie danego uprawnienia
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
fullName
required
	
string [ 5 .. 90 ] characters

Pełna nazwa podmiotu.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "permissions": [
        {},
        {}
    ],
    "description": "Opis uprawnienia",
    "subjectDetails": {
        "fullName": "Firma sp. z o.o."
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Nadanie uprawnień podmiotowych

Metoda pozwala na nadanie jednego z uprawnień podmiotowych do obsługi podmiotu kontekstu podmiotowi wskazanemu w żądaniu.

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: CredentialsManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator podmiotu uprawnianego.
Type 	Value
Nip 	10 cyfrowy numer NIP
PeppolId 	Identyfikator dostawcy usług Peppol
type
required
	
string
Enum: "Nip" "PeppolId"

Typ identyfikatora.
value
required
	
string [ 9 .. 10 ] characters

Wartość identyfikatora.
permission
required
	
string
Enum: "SelfInvoicing" "RRInvoicing" "TaxRepresentative" "PefInvoicing"

Rodzaj uprawnienia.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
fullName
required
	
string [ 5 .. 90 ] characters

Pełna nazwa podmiotu.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "permission": "SelfInvoicing",
    "description": "działanie w imieniu 3393244202 w kontekście 7762811692, Firma sp. z o.o.",
    "subjectDetails": {
        "fullName": "Firma sp. z o.o."
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Nadanie uprawnień w sposób pośredni

Metoda pozwala na nadanie w sposób pośredni osobie wskazanej w żądaniu uprawnień do obsługi faktur innego podmiotu – klienta.
Może to być jedna z możliwości:

    nadanie uprawnień generalnych – do obsługi wszystkich klientów
    nadanie uprawnień selektywnych – do obsługi wskazanego klienta

Uprawnienie selektywne może być nadane wyłącznie wtedy, gdy klient nadał wcześniej podmiotowi bieżącego kontekstu dowolne uprawnienie z prawem do jego dalszego przekazywania (patrz POST /v2/permissions/entities/grants).

W żądaniu określane są nadawane uprawnienia ze zbioru:

    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur

Metoda pozwala na wybór dowolnej kombinacji powyższych uprawnień.

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: CredentialsManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator osoby fizycznej.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator kontekstu klienta. Nie przekazanie identyfikatora oznacza, że uprawnienie nadane w sposób pośredni jest typu generalnego.
Type 	Value
Nip 	10 cyfrowy numer NIP
AllPartners 	Identyfikator oznaczający, że uprawnienie nadane w sposób pośredni jest typu generalnego
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "AllPartners" "InternalId"

Typ identyfikatora.
value	
string or null [ 10 .. 16 ] characters

Wartość identyfikatora. W przypadku typu AllPartners należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
permissions
required
	
Array of strings (IndirectPermissionType)
Items Enum: "InvoiceRead" "InvoiceWrite"

Lista nadawanych uprawnień. Każda wartość może wystąpić tylko raz.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
subjectDetailsType
required
	
string
Enum: "PersonByIdentifier" "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych podmiotu.
Wartość 	Opis
PersonByIdentifier 	Osoba fizyczna posługująca się Profilem Zaufanym lub certyfikatem zawierającym identyfikator NIP lub PESEL.
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
required
	
object

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithoutIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
birthDate
required
	
string <date>

Data urodzenia osoby fizycznej.
required
	
object

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Pesel",
        "value": "22271569167"
    },
    "targetIdentifier": {
        "type": "Nip",
        "value": "5687926712"
    },
    "permissions": [
        "InvoiceWrite",
        "InvoiceRead"
    ],
    "description": "praca dla klienta 5687926712; uprawniony PESEL: 22271569167, Adam Abacki; pośrednik 3936518395",
    "subjectDetails": {
        "subjectDetailsType": "PersonByIdentifier",
        "personById": {}
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Nadanie uprawnień administratora podmiotu podrzędnego

Metoda pozwala na nadanie wskazanemu w żądaniu podmiotowi lub osobie fizycznej uprawnień administratora w kontekście:

    wskazanego NIP podmiotu podrzędnego – wyłącznie jeżeli podmiot bieżącego kontekstu logowania ma rolę podmiotu nadrzędnego:
        LocalGovernmentUnit
        VatGroupUnit
    wskazanego lub utworzonego identyfikatora wewnętrznego

Wraz z utworzeniem administratora jednostki podrzędnej tworzony jest identyfikator wewnętrzny składający się z numeru NIP podmiotu kontekstu logowania oraz 5 cyfr unikalnie identyfikujących jednostkę wewnętrzną. Ostatnia cyfra musi być poprawną sumą kontrolną, która jest obliczana według poniższego algorytmu.

Algorytm używa naprzemiennych wag (1×, 3×, 1×, 3×, ...), sumuje wyniki i zwraca resztę z dzielenia przez 10.

Przykład:

    Wejście: "6824515772-1234" (bez cyfry kontrolnej)
    Pozycja 0 (1. cyfra): 6 × 1 = 6
    Pozycja 1 (2. cyfra): 8 × 3 = 24
    Pozycja 2 (3. cyfra): 2 × 1 = 2
    Pozycja 3 (4. cyfra): 4 × 3 = 12
    Pozycja 4 (5. cyfra): 5 × 1 = 5
    Pozycja 5 (6. cyfra): 1 × 3 = 3
    Pozycja 6 (7. cyfra): 5 × 1 = 5
    Pozycja 7 (8. cyfra): 7 × 3 = 21
    Pozycja 8 (9. cyfra): 7 × 1 = 7
    Pozycja 9 (10. cyfra): 2 × 3 = 6
    Pozycja 10 (11. cyfra): 1 × 1 = 1
    Pozycja 11 (12. cyfra): 2 × 3 = 6
    Pozycja 12 (13. cyfra): 3 × 1 = 3
    Pozycja 13 (14. cyfra): 4 × 3 = 12
    Suma: 6 + 24 + 2 + 12 + 5 + 3 + 5 + 21 + 7 + 6 + 1 + 6 + 3 + 12 = 113
    Cyfra kontrolna (15. cyfra): 113 % 10 = 3

W żądaniu podaje się również nazwę tej jednostki.

Uprawnienia administratora jednostki podrzędnej obejmują:

    CredentialsManage – zarządzanie uprawnieniami

Metoda automatycznie nadaje powyższe uprawnienie, bez konieczności podawania go w żądaniu.

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: SubunitManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator podmiotu lub osoby fizycznej.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
required
	
object

Identyfikator podmiotu podrzędnego.
Type 	Value
Nip 	10 cyfrowy numer NIP
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "InternalId" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
subunitName	
string or null [ 5 .. 256 ] characters

Nazwa jednostki podrzędnej. W przypadku jednostki podrzędnej z identyfikatorem wewnętrznym pole jest wymagane.
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
subjectDetailsType
required
	
string
Enum: "PersonByIdentifier" "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych podmiotu.
Wartość 	Opis
PersonByIdentifier 	Osoba fizyczna posługująca się Profilem Zaufanym lub certyfikatem zawierającym identyfikator NIP lub PESEL.
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
required
	
object

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithoutIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
birthDate
required
	
string <date>

Data urodzenia osoby fizycznej.
required
	
object

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Pesel",
        "value": "15062788702"
    },
    "contextIdentifier": {
        "type": "InternalId",
        "value": "7762811692-12345"
    },
    "description": "Opis uprawnienia",
    "subunitName": "Jednostka 014",
    "subjectDetails": {
        "subjectDetailsType": "PersonByIdentifier",
        "personById": {}
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Nadanie uprawnień administratora podmiotu unijnego

Metoda pozwala na nadanie wskazanemu w żądaniu podmiotowi lub osobie fizycznej uprawnień administratora w kontekście złożonym z identyfikatora NIP podmiotu kontekstu bieżącego oraz numeru VAT UE podmiotu unijnego wskazanego w żądaniu.
Wraz z utworzeniem administratora podmiotu unijnego tworzony jest kontekst złożony składający się z numeru NIP podmiotu kontekstu logowania oraz wskazanego numeru identyfikacyjnego VAT UE podmiotu unijnego.
W żądaniu podaje się również nazwę i adres podmiotu unijnego.

Jedynym sposobem identyfikacji uprawnianego jest odcisk palca certyfikatu kwalifikowanego:

    certyfikat podpisu elektronicznego dla osób fizycznych
    certyfikat pieczęci elektronicznej dla podmiotów

Uprawnienia administratora podmiotu unijnego obejmują:

    VatEuManage – zarządzanie uprawnieniami w ramach podmiotu unijnego
    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur
    Introspection – przeglądanie historii sesji

Metoda automatycznie nadaje wszystkie powyższe uprawnienia, bez konieczności ich wskazywania w żądaniu.

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: CredentialsManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator podmiotu uprawnionego.
Type 	Value
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Value: "Fingerprint"

Typ identyfikatora.
value
required
	
string = 64 characters

Wartość identyfikatora.
required
	
object

Identyfikator kontekstu złożonego.
Type 	Value
NipVatUe 	Dwuczłonowy identyfikator składający się z numeru NIP i numeru VAT-UE: {nip}-{vat_ue}
type
required
	
string
Value: "NipVatUe"

Typ identyfikatora.
value
required
	
string [ 15 .. 25 ] characters

Wartość identyfikatora.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
euEntityName
required
	
string [ 5 .. 256 ] characters

Nazwa i adres podmiotu unijnego w formacie: {euSubjectName}, {euSubjectAddress}
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
subjectDetailsType
required
	
string
Enum: "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier" "EntityByFingerprint"

Typ danych podmiotu.
Wartość 	Opis
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
EntityByFingerprint 	Podmiot identyfikowany odciskiem palca pieczęci kwalifikowanej.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
required
	
object

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithoutIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
birthDate
required
	
string <date>

Data urodzenia osoby fizycznej.
required
	
object

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = EntityByFingerprint.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
address
required
	
string <= 512 characters

Adres podmiotu.
required
	
object

Dane podmiotu unijnego, w kontekście którego nadawane są uprawnienia.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
address
required
	
string <= 512 characters

Adres podmiotu.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Fingerprint",
        "value": "CEB3643BAC2C111ADDE971BDA5A80163441867D65389FC0BC0DFF8B4C1CD4E59"
    },
    "contextIdentifier": {
        "type": "NipVatUe",
        "value": "7762811692-DE123456789012"
    },
    "description": "Opis uprawnienia",
    "euEntityName": "Firma G.m.b.H.",
    "subjectDetails": {
        "subjectDetailsType": "PersonByFingerprintWithIdentifier",
        "personByFpWithId": {}
    },
    "euEntityDetails": {
        "fullName": "Firma G.m.b.H.",
        "address": "Warszawa ul. Świętokrzyska 4824 00-916 Warszawa"
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Nadanie uprawnień reprezentanta podmiotu unijnego

Metoda pozwala na nadanie wskazanemu w żądaniu podmiotowi lub osobie fizycznej uprawnień do wystawiania i/lub przeglądania faktur w kontekście złożonym kontekstu bieżącego.

Jedynym sposobem identyfikacji uprawnianego jest odcisk palca certyfikatu kwalifikowanego:

    certyfikat podpisu elektronicznego dla osób fizycznych
    certyfikat pieczęci elektronicznej dla podmiotów

W żądaniu określane są nadawane uprawnienia ze zbioru:

    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur

Metoda pozwala na wybór dowolnej kombinacji powyższych uprawnień.

    Więcej informacji:

        Nadawanie uprawnień

Wymagane uprawnienia: VatUeManage.
Authorizations:
Bearer
Request Body schema: application/json
required
	
object

Identyfikator podmiotu uprawnianego.
Type 	Value
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Value: "Fingerprint"

Typ identyfikatora.
value
required
	
string = 64 characters

Wartość identyfikatora.
permissions
required
	
Array of strings (EuEntityPermissionType)
Items Enum: "InvoiceWrite" "InvoiceRead"

Lista nadawanych uprawnień. Każda wartość może wystąpić tylko raz.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia
required
	
object

Dane podmiotu, któremu nadawane są uprawnienia.
subjectDetailsType
required
	
string
Enum: "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier" "EntityByFingerprint"

Typ danych podmiotu.
Wartość 	Opis
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
EntityByFingerprint 	Podmiot identyfikowany odciskiem palca pieczęci kwalifikowanej.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
required
	
object

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = PersonByFingerprintWithoutIdentifier.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
birthDate
required
	
string <date>

Data urodzenia osoby fizycznej.
required
	
object

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
	
object or null

Dane podmiotu. Wymagane, gdy subjectDetailsType = EntityByFingerprint.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
address
required
	
string <= 512 characters

Adres podmiotu.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectIdentifier": {
        "type": "Fingerprint",
        "value": "CEB3643BAC2C111ADDE971BDA5A80163441867D65389FC0BC0DFF8B4C1CD4E59"
    },
    "permissions": [
        "InvoiceRead",
        "InvoiceWrite"
    ],
    "description": "Opis uprawnienia",
    "subjectDetails": {
        "subjectDetailsType": "PersonByFingerprintWithIdentifier",
        "personByFpWithId": {}
    }

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Odbieranie uprawnień
Odebranie uprawnień

Metoda pozwala na odebranie uprawnienia o wskazanym identyfikatorze.
Wymagane jest wcześniejsze odczytanie uprawnień w celu uzyskania
identyfikatora uprawnienia, które ma zostać odebrane.

    Więcej informacji:

        Odbieranie uprawnień

Wymagane uprawnienia: CredentialsManage, VatUeManage, SubunitManage.
Authorizations:
Bearer
path Parameters
permissionId
required
	
string (PermissionId) = 36 characters

Id uprawnienia.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Odebranie uprawnień podmiotowych

Metoda pozwala na odebranie uprawnienia podmiotowego o wskazanym identyfikatorze.
Wymagane jest wcześniejsze odczytanie uprawnień w celu uzyskania
identyfikatora uprawnienia, które ma zostać odebrane.

    Więcej informacji:

        Odbieranie uprawnień

Wymagane uprawnienia: CredentialsManage.
Authorizations:
Bearer
path Parameters
permissionId
required
	
string (PermissionId) = 36 characters

Id uprawnienia.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20250626-EG-333C814000-C529F710D8-D2"

}
Wyszukiwanie nadanych uprawnień
Pobranie listy własnych uprawnień

Metoda pozwala na odczytanie własnych uprawnień uwierzytelnionego klienta API w bieżącym kontekście logowania.

W odpowiedzi przekazywane są następujące uprawnienia:

    nadane w sposób bezpośredni w bieżącym kontekście
    nadane przez podmiot nadrzędny
    nadane w sposób pośredni, jeżeli podmiot kontekstu logowania jest w uprawnieniu pośrednikiem lub podmiotem docelowym
    nadane podmiotowi do obsługi faktur przez inny podmiot, jeśli podmiot uwierzytelniony ma w bieżącym kontekście uprawnienia właścicielskie

Uprawnienia zwracane przez operację obejmują:

    CredentialsManage – zarządzanie uprawnieniami
    CredentialsRead – przeglądanie uprawnień
    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur
    Introspection – przeglądanie historii sesji
    SubunitManage – zarządzanie podmiotami podrzędnymi
    EnforcementOperations – wykonywanie operacji egzekucyjnych
    VatEuManage – zarządzanie uprawnieniami w ramach podmiotu unijnego

Odpowiedź może być filtrowana na podstawie następujących parametrów:

    contextIdentifier – identyfikator podmiotu, który nadał uprawnienie do obsługi faktur
    targetIdentifier – identyfikator podmiotu docelowego dla uprawnień nadanych pośrednio
    permissionTypes – lista rodzajów wyszukiwanych uprawnień
    permissionState – status uprawnienia

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy uprawnień

Sortowanie:

    startDate (Desc)
    id (Asc)

Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json
	
object or null

Identyfikator kontekstu podmiotu, który nadał uprawnienia do obsługi faktur.
Type 	Value
Nip 	10 cyfrowy numer NIP
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "InternalId"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator podmiotu docelowego dla uprawnień selektywnych nadanych pośrednio.
Type 	Value
Nip 	10 cyfrowy numer NIP
AllPartners 	Identyfikator oznaczający, że wyszukiwanie dotyczy uprawnień generalnych nadanych w sposób pośredni
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "AllPartners" "InternalId"

Typ identyfikatora.
value	
string or null [ 10 .. 16 ] characters

Wartość identyfikatora. W przypadku typu AllPartners należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
permissionTypes	
Array of strings or null (PersonalPermissionType)
Enum: "CredentialsManage" "CredentialsRead" "InvoiceWrite" "InvoiceRead" "Introspection" "SubunitManage" "EnforcementOperations" "VatUeManage"

Lista rodzajów wyszukiwanych uprawnień.
permissionState	
string or null
Enum: "Active" "Inactive"

Stan uprawnienia.
Type 	Value
Active 	Uprawnienia aktywne
Inactive 	Uprawnienia nieaktywne
Responses
Response Schema: application/json
required
	
Array of objects (PersonalPermission)

Lista odczytanych uprawnień.
Array
id
required
	
string = 36 characters

Identyfikator uprawnienia.
	
object or null

Identyfikator kontekstu podmiotu, który nadał uprawnienia do obsługi faktur.
Type 	Value
Nip 	10 cyfrowy numer NIP
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "InternalId"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator podmiotu uprawnionego, jeżeli jest inny niż identyfikator uwierzytelnionego klienta API.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator podmiotu docelowego dla uprawnień selektywnych nadanych pośrednio.
Type 	Value
Nip 	10 cyfrowy numer NIP
AllPartners 	Identyfikator oznaczający, że wyszukiwanie dotyczy uprawnień generalnych nadanych w sposób pośredni
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "AllPartners" "InternalId"

Typ identyfikatora.
value	
string or null [ 10 .. 16 ] characters

Wartość identyfikatora. W przypadku typu AllPartners należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
permissionScope
required
	
string
Enum: "CredentialsManage" "CredentialsRead" "InvoiceWrite" "InvoiceRead" "Introspection" "SubunitManage" "EnforcementOperations" "VatUeManage"

Rodzaj uprawnienia.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia.
	
object or null

Dane osoby uprawnionej.
subjectDetailsType
required
	
string
Enum: "PersonByIdentifier" "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych uprawnionej osoby fizycznej.
Wartość 	Opis
PersonByIdentifier 	Osoba fizyczna posługująca się Profilem Zaufanym lub certyfikatem zawierającym identyfikator NIP lub PESEL.
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
birthDate	
string or null <date>

Data urodzenia osoby fizycznej.
	
object or null

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
	
object or null

Dane podmiotu uprawnionego.
subjectDetailsType
required
	
string
Enum: "EntityByIdentifier" "EntityByFingerprint"

Typ danych podmiotu uprawnionego.
Wartość 	Opis
EntityByIdentifier 	Podmiot identyfikowany numerem NIP.
EntityByFingerprint 	Podmiot identyfikowany odciskiem palca pieczęci kwalifikowanej.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
address	
string or null <= 512 characters

Adres podmiotu.
permissionState
required
	
string
Enum: "Active" "Inactive"

Stan uprawnienia.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania uprawnienia.
canDelegate
required
	
boolean

Flaga określająca, czy uprawnienie ma być możliwe do dalszego przekazywania.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "contextIdentifier": {
        "type": "Nip",
        "value": "3568707925"
    },
    "permissionTypes": [
        "InvoiceWrite"
    ],
    "permissionState": "Active"

}
Response samples

    200400429

Content type
application/json
{

    "permissions": [
        {}
    ],
    "hasMore": false

}
Pobranie listy uprawnień do pracy w KSeF nadanych osobom fizycznym lub podmiotom

Metoda pozwala na odczytanie uprawnień nadanych osobie fizycznej lub podmiotowi.
Lista pobranych uprawnień może być dwóch rodzajów:

    Lista wszystkich uprawnień obowiązujących w bieżącym kontekście logowania (używana, gdy administrator chce przejrzeć uprawnienia wszystkich użytkowników w bieżącym kontekście)
    Lista wszystkich uprawnień nadanych w bieżącym kontekście przez uwierzytelnionego klienta API (używana, gdy administrator chce przejrzeć listę nadanych przez siebie uprawnień w bieżącym kontekście)

Dla pierwszej listy (obowiązujących uprawnień) w odpowiedzi przekazywane są:

    osoby i podmioty mogące pracować w bieżącym kontekście z wyjątkiem osób uprawnionych w sposób pośredni
    osoby uprawnione w sposób pośredni przez podmiot bieżącego kontekstu

Dla drugiej listy (nadanych uprawnień) w odpowiedzi przekazywane są:

    uprawnienia nadane w sposób bezpośredni do pracy w bieżącym kontekście lub w kontekście jednostek podrzędnych
    uprawnienia nadane w sposób pośredni do obsługi klientów podmiotu bieżącego kontekstu

Uprawnienia zwracane przez operację obejmują:

    CredentialsManage – zarządzanie uprawnieniami
    CredentialsRead – przeglądanie uprawnień
    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur
    Introspection – przeglądanie historii sesji
    SubunitManage – zarządzanie podmiotami podrzędnymi
    EnforcementOperations – wykonywanie operacji egzekucyjnych

Odpowiedź może być filtrowana na podstawie parametrów:

    authorIdentifier – identyfikator osoby, która nadała uprawnienie
    authorizedIdentifier – identyfikator osoby lub podmiotu uprawnionego
    targetIdentifier – identyfikator podmiotu docelowego dla uprawnień nadanych pośrednio
    permissionTypes – lista rodzajów wyszukiwanych uprawnień
    permissionState – status uprawnienia
    queryType – typ zapytania określający, która z dwóch list ma zostać zwrócona

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy uprawnień

Sortowanie:

    startDate (Desc)
    id (Asc)

Wymagane uprawnienia: CredentialsManage, CredentialsRead, SubunitManage.
Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json
	
object or null

Identyfikator osoby lub podmiotu nadającego uprawnienie.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
System 	Identyfikator systemowy KSeF
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint" "System"

Typ identyfikatora.
value	
string or null [ 10 .. 64 ] characters

Wartość identyfikatora. W przypadku typu System należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
	
object or null

Identyfikator osoby lub podmiotu uprawnionego.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator kontekstu uprawnienia (dla uprawnień nadanych administratorom jednostek podrzędnych).
Type 	Value
Nip 	10 cyfrowy numer NIP
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "InternalId"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator podmiotu docelowego dla uprawnień nadanych pośrednio.
Type 	Value
Nip 	10 cyfrowy numer NIP
AllPartners 	Identyfikator oznaczający, że uprawnienie nadane w sposób pośredni jest typu generalnego
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "AllPartners" "InternalId"

Typ identyfikatora.
value	
string or null [ 10 .. 16 ] characters

Wartość identyfikatora. W przypadku typu AllPartners należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
permissionTypes	
Array of strings or null (PersonPermissionType)
Enum: "CredentialsManage" "CredentialsRead" "InvoiceWrite" "InvoiceRead" "Introspection" "SubunitManage" "EnforcementOperations"

Lista rodzajów wyszukiwanych uprawnień.
permissionState	
string or null
Enum: "Active" "Inactive"

Stan uprawnienia.
Type 	Value
Active 	Uprawnienia aktywne
Inactive 	Uprawnienia nieaktywne, nadane w sposób pośredni
queryType
required
	
string
Enum: "PermissionsInCurrentContext" "PermissionsGrantedInCurrentContext"

Typ zapytania.
Type 	Value
PermissionsInCurrentContext 	Lista uprawnień obowiązujących w bieżącym kontekście
PermissionsGrantedInCurrentContext 	Lista uprawnień nadanych w bieżącym kontekście
Responses
Response Schema: application/json
required
	
Array of objects (PersonPermission)

Lista odczytanych uprawnień.
Array
id
required
	
string = 36 characters

Identyfikator uprawnienia.
required
	
object

Identyfikator osoby lub podmiotu uprawnionego.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator kontekstu uprawnienia (dla uprawnień nadanych administratorom jednostek podrzędnych).
Type 	Value
Nip 	10 cyfrowy numer NIP
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "InternalId"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
	
object or null

Identyfikator podmiotu docelowego dla uprawnień nadanych pośrednio.
Type 	Value
Nip 	10 cyfrowy numer NIP
AllPartners 	Identyfikator oznaczający, że uprawnienie nadane w sposób pośredni jest typu generalnego
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
type
required
	
string
Enum: "Nip" "AllPartners" "InternalId"

Typ identyfikatora.
value	
string or null [ 10 .. 16 ] characters

Wartość identyfikatora. W przypadku typu AllPartners należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
required
	
object

Identyfikator osoby lub podmiotu nadającego uprawnienie.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
System 	Identyfikator systemowy KSeF
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint" "System"

Typ identyfikatora.
value	
string or null [ 10 .. 64 ] characters

Wartość identyfikatora. W przypadku typu System należy pozostawić puste. W pozostałych przypadkach pole jest wymagane.
permissionScope
required
	
string
Enum: "CredentialsManage" "CredentialsRead" "InvoiceWrite" "InvoiceRead" "Introspection" "SubunitManage" "EnforcementOperations"

Rodzaj uprawnienia.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia.
	
object or null

Dane osoby uprawnionej.
subjectDetailsType
required
	
string
Enum: "PersonByIdentifier" "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych uprawnionej osoby fizycznej.
Wartość 	Opis
PersonByIdentifier 	Osoba fizyczna posługująca się Profilem Zaufanym lub certyfikatem zawierającym identyfikator NIP lub PESEL.
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
birthDate	
string or null <date>

Data urodzenia osoby fizycznej.
	
object or null

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
	
object or null

Dane podmiotu uprawnionego.
subjectDetailsType
required
	
string
Enum: "EntityByIdentifier" "EntityByFingerprint"

Typ danych podmiotu uprawnionego.
Wartość 	Opis
EntityByIdentifier 	Podmiot identyfikowany numerem NIP.
EntityByFingerprint 	Podmiot identyfikowany odciskiem palca pieczęci kwalifikowanej.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
address	
string or null <= 512 characters

Adres podmiotu.
permissionState
required
	
string
Enum: "Active" "Inactive"

Stan uprawnienia.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania uprawnienia.
canDelegate
required
	
boolean

Flaga określająca, czy uprawnienie ma być możliwe do dalszego przekazywania.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "authorIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "permissionTypes": [
        "CredentialsManage",
        "CredentialsRead",
        "InvoiceWrite"
    ],
    "permissionState": "Active",
    "queryType": "PermissionsInCurrentContext"

}
Response samples

    200400429

Content type
application/json
{

    "permissions": [
        {}
    ],
    "hasMore": false

}
Pobranie listy uprawnień administratorów jednostek i podmiotów podrzędnych

Metoda pozwala na odczytanie uprawnień do zarządzania uprawnieniami nadanych administratorom:

    jednostek podrzędnych identyfikowanych identyfikatorem wewnętrznym
    podmiotów podrzędnych (podrzędnych JST lub członków grupy VAT) identyfikowanych przez NIP

Lista zwraca wyłącznie uprawnienia do zarządzania uprawnieniami nadane z kontekstu bieżącego (z podmiotu nadrzędnego).
Nie są odczytywane uprawnienia nadane przez administratorów jednostek podrzędnych wewnątrz tych jednostek.

Odpowiedź może być filtrowana na podstawie parametru:

    subunitIdentifier – identyfikator jednostki lub podmiotu podrzędnego

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy uprawnień

Sortowanie:

    startDate (Desc)
    id (Asc)

Wymagane uprawnienia: CredentialsManage, CredentialsRead, SubunitManage.
Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json
	
object or null

Identyfikator jednostki lub podmiotu podrzędnego.
Type 	Value
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
Nip 	10 cyfrowy numer NIP
type
required
	
string
Enum: "InternalId" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
Responses
Response Schema: application/json
required
	
Array of objects (SubunitPermission)

Lista odczytanych uprawnień.
Array
id
required
	
string = 36 characters

Identyfikator uprawnienia.
required
	
object

Identyfikator uprawnionego.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
required
	
object

Identyfikator jednostki lub podmiotu podrzędnego.
Type 	Value
InternalId 	Dwuczłonowy identyfikator składający się z numeru NIP i 5 cyfr: {nip}-{5_cyfr}
Nip 	10 cyfrowy numer NIP
type
required
	
string
Enum: "InternalId" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 16 ] characters

Wartość identyfikatora.
required
	
object

Identyfikator uprawniającego.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
permissionScope
required
	
string
Value: "CredentialsManage"

Rodzaj uprawnienia.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia.
	
object or null

Dane osoby uprawnionej.
subjectDetailsType
required
	
string
Enum: "PersonByIdentifier" "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych uprawnionej osoby fizycznej.
Wartość 	Opis
PersonByIdentifier 	Osoba fizyczna posługująca się Profilem Zaufanym lub certyfikatem zawierającym identyfikator NIP lub PESEL.
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
birthDate	
string or null <date>

Data urodzenia osoby fizycznej.
	
object or null

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
subunitName	
string or null [ 5 .. 256 ] characters

Nazwa jednostki podrzędnej.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania uprawnienia.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subunitIdentifier": {
        "type": "InternalId",
        "value": "7762811692-12345"
    }

}
Response samples

    200400429

Content type
application/json
{

    "permissions": [
        {}
    ],
    "hasMore": false

}
Pobranie listy ról podmiotu

Metoda pozwala na odczytanie listy ról podmiotu bieżącego kontekstu logowania.
Role podmiotów zwracane przez operację:

    CourtBailiff – komornik sądowy
    EnforcementAuthority – organ egzekucyjny
    LocalGovernmentUnit – nadrzędna JST
    LocalGovernmentSubUnit – podrzędne JST
    VatGroupUnit – grupa VAT
    VatGroupSubUnit – członek grupy VAT

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy ról

Sortowanie:

    startDate (Desc)
    id (Asc)

Wymagane uprawnienia: CredentialsManage, CredentialsRead.
Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Responses
Response Schema: application/json
required
	
Array of objects (EntityRole)

Lista odczytanych ról podmiotu.
Array
	
object or null

Identyfikator podmiotu nadrzędnego.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Value: "Nip"

Typ identyfikatora.
value
required
	
string = 10 characters

Wartość identyfikatora.
role
required
	
string
Enum: "CourtBailiff" "EnforcementAuthority" "LocalGovernmentUnit" "LocalGovernmentSubUnit" "VatGroupUnit" "VatGroupSubUnit"

Typ roli - powiązania z podmiotem nadrzędnym.
description
required
	
string [ 5 .. 256 ] characters

Opis roli.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania roli.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "roles": [
        {}
    ],
    "hasMore": false

}
Pobranie listy podmiotów podrzędnych

Metoda pozwala na odczytanie listy podmiotów podrzędnych,
jeżeli podmiot bieżącego kontekstu ma rolę podmiotu nadrzędnego:

    nadrzędna JST – odczytywane są podrzędne JST,
    grupa VAT – odczytywane są podmioty będące członkami grupy VAT.

Role podmiotów zwracane przez operację obejmują:

    LocalGovernmentSubUnit – podrzędne JST,
    VatGroupSubUnit – członek grupy VAT.

Odpowiedź może być filtrowana według parametru:

    subordinateEntityIdentifier – identyfikator podmiotu podrzędnego.

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy podmiotów podrzędnych

Sortowanie:

    startDate (Desc)
    id (Asc)

Wymagane uprawnienia: CredentialsManage, CredentialsRead, SubunitManage.
Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json
	
object or null

Identyfikator podmiotu podrzędnego.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Value: "Nip"

Typ identyfikatora.
value
required
	
string = 10 characters

Wartość identyfikatora.
Responses
Response Schema: application/json
required
	
Array of objects (SubordinateEntityRole)

Lista odczytanych podmiotów podrzędnych i ich ról.
Array
required
	
object

Identyfikator podmiotu podrzędnego.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Value: "Nip"

Typ identyfikatora.
value
required
	
string = 10 characters

Wartość identyfikatora.
role
required
	
string
Enum: "LocalGovernmentSubUnit" "VatGroupSubUnit"

Typ roli - powiązania z podmiotem nadrzędnym.
description
required
	
string [ 5 .. 256 ] characters

Opis powiązania.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania powiązania.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subordinateEntityIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    }

}
Response samples

    200400429

Content type
application/json
{

    "roles": [
        {}
    ],
    "hasMore": false

}
Pobranie listy uprawnień podmiotowych do obsługi faktur

Metoda pozwala na odczytanie uprawnień podmiotowych:

    otrzymanych przez podmiot bieżącego kontekstu
    nadanych przez podmiot bieżącego kontekstu

Wybór listy nadanych lub otrzymanych uprawnień odbywa się przy użyciu parametru queryType.

Uprawnienia zwracane przez operację obejmują:

    SelfInvoicing – wystawianie faktur w trybie samofakturowania
    TaxRepresentative – wykonywanie operacji przedstawiciela podatkowego
    RRInvoicing – wystawianie faktur VAT RR
    PefInvoicing – wystawianie faktur PEF

Odpowiedź może być filtrowana na podstawie następujących parametrów:

    authorizingIdentifier – identyfikator podmiotu uprawniającego (stosowane przy queryType = Received)
    authorizedIdentifier – identyfikator podmiotu uprawnionego (stosowane przy queryType = Granted)
    permissionTypes – lista rodzajów wyszukiwanych uprawnień

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy uprawnień

Sortowanie:

    startDate (Desc)
    id (Asc)

Wymagane uprawnienia: CredentialsManage, CredentialsRead, PefInvoiceWrite.
Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json
	
object or null

Identyfikator podmiotu uprawniającego.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Value: "Nip"

Typ identyfikatora.
value
required
	
string = 10 characters

Wartość identyfikatora.
	
object or null

Identyfikator podmiotu uprawnionego.
Type 	Value
Nip 	10 cyfrowy numer NIP
PeppolId 	Identyfikator dostawcy usług Peppol
type
required
	
string
Enum: "Nip" "PeppolId"

Typ identyfikatora.
value
required
	
string [ 9 .. 10 ] characters

Wartość identyfikatora.
queryType
required
	
string
Enum: "Granted" "Received"

Typ zapytania.
Type 	Value
Granted 	Uprawnienia nadane innym podmiotom
Received 	Uprawnienia otrzymane od innych podmiotów
permissionTypes	
Array of strings or null (InvoicePermissionType)
Enum: "SelfInvoicing" "TaxRepresentative" "RRInvoicing" "PefInvoicing"

Lista rodzajów wyszukiwanych uprawnień.
Responses
Response Schema: application/json
required
	
Array of objects (EntityAuthorizationGrant)

Lista odczytanych uprawnień.
Array
id
required
	
string = 36 characters

Identyfikator uprawnienia.
	
object or null

Identyfikator osoby nadającej uprawnienie.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
required
	
object

Identyfikator podmiotu uprawnionego.
Type 	Value
Nip 	10 cyfrowy numer NIP
PeppolId 	Identyfikator dostawcy usług Peppol
type
required
	
string
Enum: "Nip" "PeppolId"

Typ identyfikatora.
value
required
	
string [ 9 .. 10 ] characters

Wartość identyfikatora.
required
	
object

Identyfikator podmiotu uprawniającego.
Type 	Value
Nip 	10 cyfrowy numer NIP
type
required
	
string
Value: "Nip"

Typ identyfikatora.
value
required
	
string = 10 characters

Wartość identyfikatora.
authorizationScope
required
	
string
Enum: "SelfInvoicing" "TaxRepresentative" "RRInvoicing" "PefInvoicing"

Rodzaj uprawnienia.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia.
	
object or null

Dane podmiotu uprawnionego.
subjectDetailsType
required
	
string
Value: "EntityByIdentifier"

Typ danych podmiotu uprawnionego.
Wartość 	Opis
EntityByIdentifier 	Podmiot identyfikowany numerem NIP.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania uprawnienia.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "authorizedIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "queryType": "Granted",
    "permissionTypes": [
        "SelfInvoicing",
        "TaxRepresentative",
        "RRInvoicing"
    ]

}
Response samples

    200400429

Content type
application/json
{

    "authorizationGrants": [
        {}
    ],
    "hasMore": false

}
Pobranie listy uprawnień administratorów lub reprezentantów podmiotów unijnych uprawnionych do samofakturowania

Metoda pozwala na odczytanie uprawnień administratorów lub reprezentantów podmiotów unijnych:

    Jeżeli kontekstem logowania jest NIP, możliwe jest odczytanie uprawnień administratorów podmiotów unijnych powiązanych z podmiotem bieżącego kontekstu, czyli takich, dla których pierwszy człon kontekstu złożonego jest równy NIP-owi kontekstu logowania.
    Jeżeli kontekst logowania jest złożony (NIP-VAT UE), możliwe jest pobranie wszystkich uprawnień administratorów i reprezentantów podmiotu w bieżącym kontekście złożonym.

Uprawnienia zwracane przez operację obejmują:

    VatUeManage – zarządzanie uprawnieniami w ramach podmiotu unijnego
    InvoiceWrite – wystawianie faktur
    InvoiceRead – przeglądanie faktur
    Introspection – przeglądanie historii sesji

Odpowiedź może być filtrowana na podstawie następujących parametrów:

    vatUeIdentifier – identyfikator podmiotu unijnego
    authorizedFingerprintIdentifier – odcisk palca certyfikatu uprawnionej osoby lub podmiotu
    permissionTypes – lista rodzajów wyszukiwanych uprawnień

Stronicowanie wyników

Zapytanie zwraca jedną stronę wyników o numerze i rozmiarze podanym w ścieżce.

    Przy pierwszym wywołaniu należy ustawić parametr pageOffset = 0.
    Jeżeli dostępna jest kolejna strona wyników, w odpowiedzi pojawi się flaga hasMore.
    W takim przypadku można wywołać zapytanie ponownie z kolejnym numerem strony.

    Więcej informacji:

        Pobieranie listy uprawnień

Sortowanie:

    startDate (Desc)
    id (Asc)

Wymagane uprawnienia: CredentialsManage, CredentialsRead, VatUeManage.
Authorizations:
Bearer
query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Request Body schema: application/json
vatUeIdentifier	
string or null^(ATU\d{8}|BE[01]{1}\d{9}|BG\d{9,10}|CY\d{8}[...

Wartość identyfikatora (numeru identyfikacyjnego VAT) podmiotu unijnego (exact match).
authorizedFingerprintIdentifier	
string or null

Odcisk palca certyfikatu kwalifikowanego uprawnionego (contains).
permissionTypes	
Array of strings or null (EuEntityPermissionsQueryPermissionType)
Enum: "VatUeManage" "InvoiceWrite" "InvoiceRead" "Introspection"

Lista rodzajów wyszukiwanych uprawnień.
Responses
Response Schema: application/json
required
	
Array of objects (EuEntityPermission)

Lista odczytanych uprawnień.
Array
id
required
	
string = 36 characters

Identyfikator uprawnienia.
required
	
object

Identyfikator uprawniającego.
Type 	Value
Nip 	10 cyfrowy numer NIP
Pesel 	11 cyfrowy numer PESEL
Fingerprint 	Odcisk palca certyfikatu
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
vatUeIdentifier
required
	
string

Identyfikator podmiotu unijnego.
euEntityName
required
	
string [ 5 .. 256 ] characters

Nazwa podmiotu unijnego.
authorizedFingerprintIdentifier
required
	
string = 64 characters

Uprawniony odcisk palca certyfikatu.
permissionScope
required
	
string
Enum: "VatUeManage" "InvoiceWrite" "InvoiceRead" "Introspection"

Uprawnienie.
description
required
	
string [ 5 .. 256 ] characters

Opis uprawnienia.
	
object or null

Dane osoby uprawnionej.
subjectDetailsType
required
	
string
Enum: "PersonByFingerprintWithIdentifier" "PersonByFingerprintWithoutIdentifier"

Typ danych uprawnionej osoby fizycznej.
Wartość 	Opis
PersonByFingerprintWithIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL, ale mająca NIP lub PESEL.
PersonByFingerprintWithoutIdentifier 	Osoba fizyczna posługująca się certyfikatem niezawierającym identyfikatora NIP ani PESEL i niemająca NIP ani PESEL.
firstName
required
	
string [ 2 .. 30 ] characters

Imię osoby fizycznej.
lastName
required
	
string [ 2 .. 81 ] characters

Nazwisko osoby fizycznej.
	
object or null

Identyfikator osoby fizycznej.
type
required
	
string
Enum: "Pesel" "Nip"

Typ identyfikatora.
value
required
	
string [ 10 .. 11 ] characters

Wartość identyfikatora.
birthDate	
string or null <date>

Data urodzenia osoby fizycznej.
	
object or null

Dane dokumentu tożsamości osoby fizycznej.
type
required
	
string <= 20 characters

Rodzaj dokumentu tożsamości.
number
required
	
string <= 20 characters

Seria i numer dokumentu tożsamości.
country
required
	
string = 2 characters

Kraj wydania dokumentu tożsamości. Musi być zgodny z ISO 3166-1 alpha-2 (np. PL, DE, US) oraz zawierać dokładnie 2 wielkie litery.
	
object or null

Dane podmiotu uprawnionego.
subjectDetailsType
required
	
string
Value: "EntityByFingerprint"

Typ danych podmiotu uprawnionego.
Wartość 	Opis
EntityByFingerprint 	Podmiot identyfikowany odciskiem palca pieczęci kwalifikowanej.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu.
address	
string or null <= 512 characters

Adres podmiotu.
	
object or null

Dane podmiotu unijnego, w kontekście którego nadane jest uprawnienie.
fullName
required
	
string <= 100 characters

Pełna nazwa podmiotu unijnego.
address
required
	
string <= 512 characters

Adres podmiotu unijnego.
startDate
required
	
string <date-time>

Data rozpoczęcia obowiązywania uprawnienia.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "vatUeIdentifier": "DE123456789012",
    "permissionTypes": [
        "VatUeManage",
        "Introspection"
    ]

}
Response samples

    200400429

Content type
application/json
{

    "permissions": [
        {}
    ],
    "hasMore": false

}
Operacje
Pobranie statusu operacji

Zwraca status operacji asynchronicznej związanej z nadaniem lub odebraniem uprawnień.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny operacji nadania lub odbierania uprawnień.
Responses
Response Schema: application/json
required
	
object

Informacje o aktualnym statusie.
Code 	Description 	Details
100 	Operacja przyjęta do realizacji 	-
200 	Operacja zakończona sukcesem 	-
400 	Operacja zakończona niepowodzeniem 	-
410 	Podane identyfikatory są niezgodne lub pozostają w niewłaściwej relacji 	-
420 	Użyte poświadczenia nie mają uprawnień do wykonania tej operacji 	-
430 	Kontekst identyfikatora nie odpowiada wymaganej roli lub uprawnieniom 	-
440 	Operacja niedozwolona dla wskazanych powiązań identyfikatorów 	-
450 	Operacja niedozwolona dla wskazanego identyfikatora lub jego typu 	-
500 	Nieznany błąd 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie później.
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "status": {
        "code": 200,
        "description": "Operacja zakończona sukcesem"
    }

}
Sprawdzenie statusu zgody na wystawianie faktur z załącznikiem

Sprawdzenie czy obecny kontekst posiada zgodę na wystawianie faktur z załącznikiem.

Wymagane uprawnienia: CredentialsManage, CredentialsRead.
Authorizations:
Bearer
Responses
Response Schema: application/json
isAttachmentAllowed	
boolean

Informacja czy Podmiot ma obecnie możliwość dodawania Załączników do Faktur
revokedDate	
string or null <date-time>

Data i czas zakończenia możliwość dodawania przez Podmiot Załączników do Faktur. Brak podanej daty oznacza bezterminową możliwość dodawania Załączników do Faktur
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "isAttachmentAllowed": true,
    "revokedDate": "2019-08-24T14:15:22Z"

}
Certyfikaty

Certyfikat KSeF to cyfrowe poświadczenie tożsamości podmiotu, wydawane przez system KSeF na wniosek uwierzytelnionego podmiotu. Certyfikat ten może być wykorzystywany do:

    uwierzytelniania się w systemie KSeF,
    realizacji operacji w trybie offline, w tym wystawiania faktur bezpośrednio w aplikacji użytkownika.

Uwaga: Wnioskowanie o certyfikat KSeF jest możliwe wyłącznie po uwierzytelnieniu z wykorzystaniem podpisu (XAdES). Uwierzytelnienie przy użyciu tokenu systemowego KSeF nie pozwala na złożenie wniosku.
Pobranie danych o limitach certyfikatów

Zwraca informacje o limitach certyfikatów oraz informacje czy użytkownik może zawnioskować o certyfikat KSeF.
Authorizations:
Bearer
Responses
Response Schema: application/json
canRequest
required
	
boolean

Flaga informująca czy uwierzytelniony podmiot może złożyć nowy wniosek o certyfikat.
required
	
object

Informacje o limitach związanych z liczbą możliwych do złożenia wniosków certyfikacyjnych.
remaining
required
	
integer <int32>

Pozostała wartość limitu.
limit
required
	
integer <int32>

Maksymalna liczba zasobów dozwolona w ramach limitu.
required
	
object

Informacje o limitach dotyczących liczby aktywnych certyfikatów wydanych dla danego podmiotu.
remaining
required
	
integer <int32>

Pozostała wartość limitu.
limit
required
	
integer <int32>

Maksymalna liczba zasobów dozwolona w ramach limitu.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "canRequest": true,
    "enrollment": {
        "remaining": 0,
        "limit": 0
    },
    "certificate": {
        "remaining": 0,
        "limit": 0
    }

}
Pobranie danych do wniosku certyfikacyjnego

Zwraca dane wymagane do przygotowania wniosku certyfikacyjnego PKCS#10.

Dane te są zwracane na podstawie certyfikatu użytego w procesie uwierzytelnienia i identyfikują podmiot, który składa wniosek o certyfikat.

    Więcej informacji:

        Pobranie danych do wniosku certyfikacyjnego
        Przygotowanie wniosku

Authorizations:
Bearer
Responses
Response Schema: application/json
commonName
required
	
string

Nazwa powszechna.
countryName
required
	
string

Kraj, kod ISO 3166.
givenName	
string or null

Imię.
surname	
string or null

Nazwisko.
serialNumber	
string or null

Numer seryjny podmiotu.
uniqueIdentifier	
string or null

Unikalny identyfikator.
organizationName	
string or null

Nazwa organizacji.
organizationIdentifier	
string or null

Identyfikator organizacji.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "commonName": "Firma Kowalski Certyfikat",
    "countryName": "PL",
    "serialNumber": "ABC123456789",
    "uniqueIdentifier": "d9d22724-4696-460c-9e5e-b9e3aafb0af3",
    "organizationName": "Firma Kowalski Sp. z o.o.",
    "organizationIdentifier": "7762811692"

}
Wysyłka wniosku certyfikacyjnego

Przyjmuje wniosek certyfikacyjny i rozpoczyna jego przetwarzanie.

Dozwolone typy kluczy prywatnych:

    RSA (OID: 1.2.840.113549.1.1.1), długość klucza równa 2048 bitów,
    EC (klucze oparte na krzywych eliptycznych, OID: 1.2.840.10045.2.1), krzywa NIST P-256 (secp256r1)

Zalecane jest stosowanie kluczy EC.

Dozwolone algorytmy podpisu:

    RSA PKCS#1 v1.5,
    RSA PSS,
    ECDSA (format podpisu zgodny z RFC 3279)

Dozwolone funkcje skrótu użyte do podpisu CSR:

    SHA1,
    SHA256,
    SHA384,
    SHA512

    Więcej informacji:

        Wysłanie wniosku certyfikacyjnego

Authorizations:
Bearer
Request Body schema: application/json
certificateName
required
	
string [ 5 .. 100 ] characters ^[a-zA-Z0-9_\-\ ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$

Nazwa własna certyfikatu.
certificateType
required
	
string
Enum: "Authentication" "Offline"

Typ certyfikatu.
Wartość 	Opis
Authentication 	Certyfikat używany do uwierzytelnienia w systemie.
Offline 	Certyfikat używany wyłącznie do potwierdzania autentyczności wystawcy i integralności faktury w trybie offline
csr
required
	
string <byte>

Wniosek certyfikacyjny PKCS#10 (CSR) w formacie DER, zakodowany w formacie Base64.
validFrom	
string or null <date-time>

Data rozpoczęcia ważności certyfikatu. Jeśli nie zostanie podana, certyfikat będzie ważny od momentu jego wystawienia.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny wniosku certyfikacyjnego.
timestamp
required
	
string <date-time>

Data złożenia wniosku certyfikacyjnego.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "certificateName": "Certyfikat-Auth-004",
    "certificateType": "Authentication",
    "csr": "MIIDJjCCAd4CAQAwgbAxIjAgBgNVBAMMGUZpcm1hIEtvd2Fsc2tpIENlcnR5ZmlrYXQxIjAgBgNVBAoMGUZpcm1hIEtvd2Fsc2tpIFNwLiB6IG8uby4xEzARBgNVBGEMCjc3NjI4MTE2OTIxCzAJBgNVBAYTAlBMMRUwEwYDVQQFEwxBQkMxMjM0NTY3ODkxLTArBgNVBC0MJGQ5ZDIyNzI0LTQ2OTYtNDYwYy05ZTVlLWI5ZTNhYWZiMGFmMzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANZC1hJiB4ZBsxGy/a4yvtOUP0HQxDt7EUZrfKO78+cmI7KCO9aW96yr6O0R928/Y9vmymbgh6KvMUTzZZj24uyxar849O1laor5t8Wv63RDx/I4+9Rt7w+QPPofmpenOokJH+Fm+FDQwo2l07o8SppGfaZpvMak+cDSrh+73wfM37fvPImr9p4ckzzxA9q6f4uoqGqcGSDlSwRjfLQKzWZaEklpZBpY4jeCh54uN3+YLsMQYKdcIbW0Jart1UbwMd/wbHfzFhVmPGOAMMpwVEBw6E4A0CTWIiAX3Alqbx4+IkuqC+gEs3ETTec7eOqhxe9V9cywi7WR+Mz6JO6DJcUCAwEAAaAAMD0GCSqGSIb3DQEBCjAwoA0wCwYJYIZIAWUDBAIBoRowGAYJKoZIhvcNAQEIMAsGCWCGSAFlAwQCAaIDAgEgA4IBAQCJhtF2/2E+JmkWitE/BGbm3NU4fIxr1Z+w0UnHsP+F8n9UDwAnuncG1GH5wZFervldEMooegzEDnYaqxnEUnbZ4wxeAHqpbTZjOOfqrk7o0r66+mXUs5NnyD4M3j3ig98GcvhEdbcNH+RsIwi7FaLNXnOE4SLYL9KvW0geriywWjS+5MmA0Gcn1e4vCD6FeEls8EHzkhrWE+rUsoM5zT2a0OPNXG3fScyOqOZe+OdjT4Y7ScRGy711u3v2X9RoTqQUDfCJ3cob/KRcrzvs1TQVazGZPfcIa6an6SigUvZ7XAMHlUTyOeM4AwKqiEqQ0qfe/HhlDylgZSwulb9u0utT",
    "validFrom": "2025-08-28T09:22:13.388+00:00"

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20251010-EH-1B6C9EB000-4B15D3AEB9-89",
    "timestamp": "2025-10-11T12:23:56.0154302+00:00"

}
Pobranie statusu przetwarzania wniosku certyfikacyjnego

Zwraca informacje o statusie wniosku certyfikacyjnego.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny wniosku certyfikacyjnego
Responses
Response Schema: application/json
requestDate
required
	
string <date-time>

Data złożenia wniosku certyfikacyjnego.
required
	
object

Informacje o aktualnym statusie.
Code 	Description 	Details
100 	Wniosek przyjęty do realizacji 	-
200 	Wniosek obsłużony (certyfikat wygenerowany) 	-
400 	Wniosek odrzucony 	Klucz publiczny został już certyfikowany przez inny podmiot.
400 	Wniosek odrzucony 	Osiągnięto dopuszczalny limit posiadanych certyfikatów.
500 	Nieznany błąd 	-
550 	Operacja została anulowana przez system 	Przetwarzanie zostało przerwane z przyczyn wewnętrznych systemu. Spróbuj ponownie
code
required
	
integer <int32>

Kod statusu
description
required
	
string non-empty

Opis statusu
details	
Array of strings or null

Dodatkowe szczegóły statusu
certificateSerialNumber	
string or null

Numer seryjny wygenerowanego certyfikatu (w formacie szesnastkowym). Zwracany w przypadku prawidłowego przeprocesowania wniosku certyfikacyjnego.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "requestDate": "2025-10-11T12:23:56.0154302+00:00",
    "status": {
        "code": 100,
        "description": "Wniosek przyjęty do realizacji"
    }

}
Pobranie certyfikatu lub listy certyfikatów

Zwraca certyfikaty o podanych numerach seryjnych w formacie DER zakodowanym w Base64.
Authorizations:
Bearer
Request Body schema: application/json
certificateSerialNumbers
required
	
Array of strings [ 1 .. 10 ] items

Numery seryjne certyfikatów do pobrania.
Responses
Response Schema: application/json
required
	
Array of objects (RetrieveCertificatesListItem)

Pobrane certyfikaty.
Array
certificate
required
	
string <byte>

Certyfikat w formacie DER, zakodowany w formacie Base64.
certificateName
required
	
string

Nazwa własna certyfikatu.
certificateSerialNumber
required
	
string

Numer seryjny certyfikatu.
certificateType
required
	
string
Enum: "Authentication" "Offline"

Typ certyfikatu.
Wartość 	Opis
Authentication 	Certyfikat używany do uwierzytelnienia w systemie.
Offline 	Certyfikat używany wyłącznie do potwierdzania autentyczności wystawcy i integralności faktury w trybie offline
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "certificateSerialNumbers": [
        "0321C82DA41B4362",
        "0321F21DA462A362"
    ]

}
Response samples

    200400429

Content type
application/json
{

    "certificates": [
        {}
    ]

}
Unieważnienie certyfikatu

Unieważnia certyfikat o podanym numerze seryjnym.
Authorizations:
Bearer
path Parameters
certificateSerialNumber
required
	
string

Numer seryjny certyfikatu (w formacie szesnastkowym).
Request Body schema: application/json
revocationReason	
string or null
Enum: "Unspecified" "Superseded" "KeyCompromise"

Powód unieważnienia certyfikatu.
Wartość 	Opis
Unspecified 	Nieokreślony.
Superseded 	Certyfikat został zastąpiony przez inny.
KeyCompromise 	Klucz prywatny powiązany z certyfikatem został skompromitowany.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "revocationReason": "Unspecified"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Pobranie listy metadanych certyfikatów

Zwraca listę certyfikatów spełniających podane kryteria wyszukiwania. W przypadku braku podania kryteriów wyszukiwania zwrócona zostanie nieprzefiltrowana lista.

Sortowanie:

    requestDate (Desc)

Authorizations:
Bearer
query Parameters
pageSize	
integer <int32> [ 10 .. 50 ]
Default: 10

Rozmiar strony wyników
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników
Request Body schema: application/json

Kryteria filtrowania
certificateSerialNumber	
string or null

Numer seryjny certyfikatu. Wyszukiwanie odbywa się na zasadzie dokładnego dopasowania (exact match).
name	
string or null

Nazwa własna certyfikatu. Wyszukiwanie jest częściowe, czyli zwracane są certyfikaty, których nazwa zawiera podany ciąg znaków (contains).
type	
string or null
Enum: "Authentication" "Offline"

Typ certyfikatu KSeF.
Wartość 	Opis
Authentication 	Certyfikat używany do uwierzytelnienia w systemie.
Offline 	Certyfikat używany wyłącznie do potwierdzania autentyczności wystawcy i integralności faktury w trybie offline
status	
string or null
Enum: "Active" "Blocked" "Revoked" "Expired"

Status certyfikatu.
Wartość 	Opis
Active 	Certyfikat jest aktywny i może zostać użyty do uwierzytelnienia lub realizacji operacji w trybie offline (w zależności od typu certyfikatu).
Blocked 	Certyfikat został zablokowany i nie może zostać użyty do uwierzytelnienia i realizacji operacji w trybie offline. Status przejściowy do czasu zakończenia procesu unieważniania.
Revoked 	Certyfikat został unieważniony i nie może zostać użyty do uwierzytelnienia i realizacji operacji w trybie offline.
Expired 	Certyfikat wygasł i nie może zostać użyty do uwierzytelnienia i realizacji operacji w trybie offline.
expiresAfter	
string or null <date-time>

Filtruje certyfikaty, które wygasają po podanej dacie.
Responses
Response Schema: application/json
required
	
Array of objects (CertificateListItem)

Lista certyfikatów spełniających kryteria wyszukiwania.
Array
certificateSerialNumber
required
	
string

Numer seryjny certyfikatu (w formacie szesnastkowym).
name
required
	
string <= 100 characters

Nazwa własna certyfikatu.
type
required
	
string
Enum: "Authentication" "Offline"

Typ certyfikatu.
Wartość 	Opis
Authentication 	Certyfikat używany do uwierzytelnienia w systemie.
Offline 	Certyfikat używany wyłącznie do potwierdzania autentyczności wystawcy i integralności faktury w trybie offline
commonName
required
	
string

Nazwa powszechna (CN) podmiotu, dla którego wystawiono certyfikat.
status
required
	
string
Enum: "Active" "Blocked" "Revoked" "Expired"

Status certyfikatu.
Wartość 	Opis
Active 	Certyfikat jest aktywny i może zostać użyty do uwierzytelnienia lub realizacji operacji w trybie offline (w zależności od typu certyfikatu).
Blocked 	Certyfikat został zablokowany i nie może zostać użyty do uwierzytelnienia i realizacji operacji w trybie offline. Status przejściowy do czasu zakończenia procesu unieważniania.
Revoked 	Certyfikat został unieważniony i nie może zostać użyty do uwierzytelnienia i realizacji operacji w trybie offline.
Expired 	Certyfikat wygasł i nie może zostać użyty do uwierzytelnienia i realizacji operacji w trybie offline.
required
	
object

Identyfikator podmiotu, dla którego wystawiono certyfikat.
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
value
required
	
string [ 10 .. 64 ] characters

Wartość identyfikatora.
validFrom
required
	
string <date-time>

Data rozpoczęcia ważności certyfikatu.
validTo
required
	
string <date-time>

Data wygaśnięcia certyfikatu.
lastUseDate	
string or null <date-time>

Data ostatniego użycia certyfikatu.
requestDate
required
	
string <date-time>

Data złożenia wniosku certyfikacyjnego.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "type": "Offline",
    "status": "Active"

}
Response samples

    200400429

Content type
application/json
{

    "certificates": [
        {}
    ],
    "hasMore": false

}
Tokeny KSeF

Token KSeF to unikalny, generowany identyfikator uwierzytelniający, który — na równi z kwalifikowanym podpisem elektronicznym — umożliwia uwierzytelnienie się do API KSeF.

Token KSeF jest wydawany z niezmiennym zestawem uprawnień określonych przy jego tworzeniu; każda modyfikacja tych uprawnień wymaga wygenerowania nowego tokena.

    Uwaga!
    Token KSeF pełni rolę poufnego sekretu uwierzytelniającego — należy przechowywać go wyłącznie w zaufanym i bezpiecznym magazynie.

Więcej informacji:

    Token KSeF

Wygenerowanie nowego tokena

Zwraca token, który może być użyty do uwierzytelniania się w KSeF.

Token może być generowany tylko w kontekście NIP lub identyfikatora wewnętrznego. Jest zwracany tylko raz. Zaczyna być aktywny w momencie gdy jego status zmieni się na Active.
Authorizations:
Bearer
Request Body schema: application/json
permissions
required
	
Array of strings (TokenPermissionType)
Items Enum: "InvoiceRead" "InvoiceWrite" "CredentialsRead" "CredentialsManage" "SubunitManage" "EnforcementOperations"

Uprawnienia przypisane tokenowi.
description
required
	
string [ 5 .. 256 ] characters

Opis tokena.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny tokena KSeF.
token
required
	
string <= 160 characters

Token KSeF.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "permissions": [
        "InvoiceRead",
        "InvoiceWrite"
    ],
    "description": "Wystawianie i przeglądanie faktur."

}
Response samples

    202400429

Content type
application/json
{

    "referenceNumber": "20251010-EC-1DCE3E3000-12ECB5B36E-45",
    "token": "20251010-EC-1DCE3E3000-12ECB5B36E-45|internalId-5265877635-12345|919f704466624ce29cd5ac7b65ded5e7cccc112eee314f2aaa76e02cd16df7b9"

}
Pobranie listy wygenerowanych tokenów

Sortowanie:

    dateCreated (Desc)

Authorizations:
Bearer
query Parameters
status	
Array of strings (AuthenticationTokenStatus)
Items Enum: "Pending" "Active" "Revoking" "Revoked" "Failed"

Status tokenów do zwrócenia. W przypadku braku parametru zwracane są wszystkie tokeny. Parametr można przekazać wielokrotnie.
Wartość 	Opis
Pending 	Token został utworzony ale jest jeszcze w trakcie aktywacji i nadawania uprawnień. Nie może być jeszcze wykorzystywany do uwierzytelniania.
Active 	Token jest aktywny i może być wykorzystywany do uwierzytelniania.
Revoking 	Token jest w trakcie unieważniania. Nie może już być wykorzystywany do uwierzytelniania.
Revoked 	Token został unieważniony i nie może być wykorzystywany do uwierzytelniania.
Failed 	Nie udało się aktywować tokena. Należy wygenerować nowy token, obecny nie może być wykorzystywany do uwierzytelniania.
description	
string >= 3 characters

Umożliwia filtrowanie tokenów po opisie. Wartość parametru jest wyszukiwana w opisie tokena (operacja nie rozróżnia wielkości liter). Należy podać co najmniej 3 znaki.
authorIdentifier	
string >= 3 characters

Umożliwia filtrowanie tokenów po ich twórcy. Wartość parametru jest wyszukiwana w identyfikatorze (operacja nie rozróżnia wielkości liter). Należy podać co najmniej 3 znaki.
authorIdentifierType	
string
Enum: "Nip" "Pesel" "Fingerprint"

Umożliwia filtrowanie tokenów po ich twórcy. Wartość parametru określa typ identyfikatora w którym będzie wyszukiwany ciąg znaków przekazany w parametrze authorIdentifier.
Wartość 	Opis
Nip 	NIP.
Pesel 	PESEL.
Fingerprint 	Odcisk palca certyfikatu.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
header Parameters
x-continuation-token	
string

Token służący do pobrania kolejnej strony wyników.
Responses
Response Schema: application/json
continuationToken	
string or null

Token służący do pobrania kolejnej strony wyników. Jeśli jest pusty, to nie ma kolejnych stron.
required
	
Array of objects (QueryTokensResponseItem)

Lista tokenów uwierzytelniających.
Array
referenceNumber
required
	
string = 36 characters

Numer referencyjny tokena KSeF.
required
	
object

Identyfikator osoby która wygenerowała token.
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
Wartość 	Opis
Nip 	NIP.
Pesel 	PESEL.
Fingerprint 	Odcisk palca certyfikatu.
value
required
	
string

Wartość identyfikatora.
required
	
object

Identyfikator kontekstu, w którym został wygenerowany token i do którego daje dostęp.
type
required
	
string
Enum: "Nip" "InternalId" "NipVatUe" "PeppolId"

Typ identyfikatora.
Wartość 	Opis
Nip 	NIP.
InternalId 	Identyfikator wewnętrzny.
NipVatUe 	Dwuczłonowy identyfikator składający się z numeru NIP i numeru VAT-UE: {nip}-{vat_ue}.
PeppolId 	Identyfikator dostawcy usług Peppol.
value
required
	
string

Wartość identyfikatora.
description
required
	
string [ 5 .. 256 ] characters

Opis tokena.
requestedPermissions
required
	
Array of strings (TokenPermissionType)
Items Enum: "InvoiceRead" "InvoiceWrite" "CredentialsRead" "CredentialsManage" "SubunitManage" "EnforcementOperations"

Uprawnienia przypisane tokenowi.
dateCreated
required
	
string <date-time>

Data i czas utworzenia tokena.
lastUseDate	
string or null <date-time>

Data ostatniego użycia tokena.
status
required
	
string
Enum: "Pending" "Active" "Revoking" "Revoked" "Failed"

Status tokena.
Wartość 	Opis
Pending 	Token został utworzony ale jest jeszcze w trakcie aktywacji i nadawania uprawnień. Nie może być jeszcze wykorzystywany do uwierzytelniania.
Active 	Token jest aktywny i może być wykorzystywany do uwierzytelniania.
Revoking 	Token jest w trakcie unieważniania. Nie może już być wykorzystywany do uwierzytelniania.
Revoked 	Token został unieważniony i nie może być wykorzystywany do uwierzytelniania.
Failed 	Nie udało się aktywować tokena. Należy wygenerować nowy token, obecny nie może być wykorzystywany do uwierzytelniania.
statusDetails	
Array of strings or null

Dodatkowe informacje na temat statusu, zwracane w przypadku błędów.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "continuationToken": "W3sidG9rZW4iOiIrUklEOn4zeHd0QUlqZUc5VkhCQUFBQUFBQUJBPT0jUlQ6MSNUUkM6MTAjSVNWOjIjSUVPOjY1NTY3I1FDRjo4I0ZQQzpBZ2dBQUFBQUFCQUFBQUFBQUFBQUVBQUFBQUFBQUFBUUFBQUVBRWVFMllFPSIsInJhbmdlIjp7Im1pbiI6IjA1QzFERjIxOUY5OTIwIiwibWF4IjoiRkYifX1d",
    "tokens": [
        {}
    ]

}
Pobranie statusu tokena

Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny tokena KSeF.
Responses
Response Schema: application/json
referenceNumber
required
	
string = 36 characters

Numer referencyjny tokena KSeF.
required
	
object

Identyfikator osoby która wygenerowała token.
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"

Typ identyfikatora.
Wartość 	Opis
Nip 	NIP.
Pesel 	PESEL.
Fingerprint 	Odcisk palca certyfikatu.
value
required
	
string

Wartość identyfikatora.
required
	
object

Identyfikator kontekstu, w którym został wygenerowany token i do którego daje dostęp.
type
required
	
string
Enum: "Nip" "InternalId" "NipVatUe" "PeppolId"

Typ identyfikatora.
Wartość 	Opis
Nip 	NIP.
InternalId 	Identyfikator wewnętrzny.
NipVatUe 	Dwuczłonowy identyfikator składający się z numeru NIP i numeru VAT-UE: {nip}-{vat_ue}.
PeppolId 	Identyfikator dostawcy usług Peppol.
value
required
	
string

Wartość identyfikatora.
description
required
	
string [ 5 .. 256 ] characters

Opis tokena.
requestedPermissions
required
	
Array of strings (TokenPermissionType)
Items Enum: "InvoiceRead" "InvoiceWrite" "CredentialsRead" "CredentialsManage" "SubunitManage" "EnforcementOperations"

Uprawnienia przypisane tokenowi.
dateCreated
required
	
string <date-time>

Data i czas utworzenia tokena.
lastUseDate	
string or null <date-time>

Data ostatniego użycia tokena.
status
required
	
string
Enum: "Pending" "Active" "Revoking" "Revoked" "Failed"

Status tokena.
Wartość 	Opis
Pending 	Token został utworzony ale jest jeszcze w trakcie aktywacji i nadawania uprawnień. Nie może być jeszcze wykorzystywany do uwierzytelniania.
Active 	Token jest aktywny i może być wykorzystywany do uwierzytelniania.
Revoking 	Token jest w trakcie unieważniania. Nie może już być wykorzystywany do uwierzytelniania.
Revoked 	Token został unieważniony i nie może być wykorzystywany do uwierzytelniania.
Failed 	Nie udało się aktywować tokena. Należy wygenerować nowy token, obecny nie może być wykorzystywany do uwierzytelniania.
statusDetails	
Array of strings or null

Dodatkowe informacje na temat statusu, zwracane w przypadku błędów.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "referenceNumber": "20251001-EC-220B0CE000-E228129563-96",
    "authorIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "contextIdentifier": {
        "type": "Nip",
        "value": "5265877635"
    },
    "description": "Wystawianie i przeglądanie faktur.",
    "requestedPermissions": [
        "InvoiceWrite",
        "InvoiceRead"
    ],
    "dateCreated": "2025-07-11T12:23:56.0154302+00:00",
    "lastUseDate": "2025-07-11T12:23:56.0154302+00:00",
    "status": "Pending",
    "statusDetails": [ ]

}
Unieważnienie tokena

Unieważniony token nie pozwoli już na uwierzytelnienie się za jego pomocą. Unieważnienie nie może zostać cofnięte.
Authorizations:
Bearer
path Parameters
referenceNumber
required
	
string (ReferenceNumber) = 36 characters

Numer referencyjny tokena KSeF.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	100 	300 	1200 	other
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Usługi Peppol
Pobranie listy dostawców usług Peppol

Zwraca listę dostawców usług Peppol zarejestrowanych w systemie.

Sortowanie:

    dateCreated (Desc)
    id (Asc)

query Parameters
pageOffset	
integer <int32> >= 0
Default: 0

Numer strony wyników.
pageSize	
integer <int32> [ 10 .. 100 ]
Default: 10

Rozmiar strony wyników.
Responses
Response Schema: application/json
required
	
Array of objects (PeppolProvider)

Lista dostawców usług Peppol.
Array
id
required
	
string = 9 characters ^P[A-Z]{2}[0-9]{6}$

Identyfikator dostawcy usług Peppol.
name
required
	
string <= 256 characters

Nazwa dostawcy usług Peppol.
dateCreated
required
	
string <date-time>

Data rejestracji dostawcy usług Peppol w systemie.
hasMore
required
	
boolean

Flaga informująca o dostępności kolejnej strony wyników.
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Response samples

    200400429

Content type
application/json
{

    "peppolProviders": [
        {}
    ],
    "hasMore": false

}
Dane testowe

API służy do tworzenia i zarządzania danymi testowymi, takimi jak podmioty, osoby fizyczne oraz uprawnienia. Możliwe do utworzenia podmioty to: organ egzekucyjny, grupa VAT oraz jednostki samorządu terytorialnego. W przypadku osób fizycznych można określić, czy dana osoba jest komornikiem. Funkcjonalność nadawania i odbierania uprawnień ma na celu odwzorowanie działania formularza ZAW-FA w środowisku testowym.

Więcej informacji:

    Scenariusze testowe

Utworzenie podmiotu

Tworzenie nowego podmiotu testowego. W przypadku grupy VAT i JST istnieje możliwość stworzenia jednostek podrzędnych. W wyniku takiego działania w systemie powstanie powiązanie między tymi podmiotami.
Request Body schema: application/json
subjectNip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
subjectType
required
	
string
Enum: "EnforcementAuthority" "VatGroup" "JST"
	
Array of objects or null (Subunit)
Array
subjectNip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
description
required
	
string [ 5 .. 256 ] characters
description
required
	
string [ 5 .. 256 ] characters
createdDate	
string or null <date-time>

W przypadku wielokrotnego tworzenia danych testowych z tym samym identyfikatorem nie można podawać daty wcześniejszej ani takiej samej jak poprzednia.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectNip": "7762811692",
    "subjectType": "EnforcementAuthority",
    "description": "Centrala",
    "createdDate": "2025-08-25T14:15:22+00:00"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Usunięcie podmiotu

Usuwanie podmiotu testowego. W przypadku grupy VAT i JST usunięte zostaną również jednostki podrzędne.
Request Body schema: application/json
subjectNip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "subjectNip": "7762811692"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Utworzenie osoby fizycznej

Tworzenie nowej osoby fizycznej, której system nadaje uprawnienia właścicielskie. Można również określić, czy osoba ta jest komornikiem – wówczas otrzyma odpowiednie uprawnienie egzekucyjne.
Request Body schema: application/json
nip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
pesel
required
	
string (Pesel) = 11 characters ^\d{2}(?:0[1-9]|1[0-2]|2[1-9]|3[0-2]|4[1-9]|5...

11 cyfrowy numer PESEL.
isBailiff
required
	
boolean
description
required
	
string [ 5 .. 256 ] characters
isDeceased	
boolean
createdDate	
string or null <date-time>

W przypadku wielokrotnego tworzenia danych testowych z tym samym identyfikatorem nie można podawać daty wcześniejszej ani takiej samej jak poprzednia.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "nip": "7762811692",
    "pesel": "15062788702",
    "isBailiff": true,
    "description": "TestPerson_01",
    "isDeceased": false,
    "createdDate": "2025-08-25T14:15:22+00:00"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Usunięcie osoby fizycznej

Usuwanie testowej osoby fizycznej. System automatycznie odbierze jej wszystkie uprawnienia.
Request Body schema: application/json
nip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "nip": "7762811692"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Nadanie uprawnień testowemu podmiotowi/osobie fizycznej

Nadawanie uprawnień testowemu podmiotowi lub osobie fizycznej, a także w ich kontekście.
Request Body schema: application/json
required
	
object
type
required
	
string
Value: "Nip"
value
required
	
string = 10 characters
required
	
object
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"
value
required
	
string [ 10 .. 64 ] characters
required
	
Array of objects (TestDataPermission)
Array
description
required
	
string [ 5 .. 256 ] characters
permissionType
required
	
string
Enum: "InvoiceRead" "InvoiceWrite" "Introspection" "CredentialsRead" "CredentialsManage" "EnforcementOperations" "SubunitManage"
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "contextIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "authorizedIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    },
    "permissions": [
        {}
    ]

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Odebranie uprawnień testowemu podmiotowi/osobie fizycznej

Odbieranie uprawnień nadanych testowemu podmiotowi lub osobie fizycznej, a także w ich kontekście.
Request Body schema: application/json
required
	
object
type
required
	
string
Value: "Nip"
value
required
	
string = 10 characters
required
	
object
type
required
	
string
Enum: "Nip" "Pesel" "Fingerprint"
value
required
	
string [ 10 .. 64 ] characters
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "contextIdentifier": {
        "type": "Nip",
        "value": "5265877635"
    },
    "authorizedIdentifier": {
        "type": "Nip",
        "value": "7762811692"
    }

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Umożliwienie wysyłania faktur z załącznikiem

Dodaje możliwość wysyłania faktur z załącznikiem przez wskazany podmiot
Request Body schema: application/json
nip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "nip": "7762811692"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}
Odebranie możliwości wysyłania faktur z załącznikiem

Odbiera możliwość wysyłania faktur z załącznikiem przez wskazany podmiot
Request Body schema: application/json
nip
required
	
string (Nip) = 10 characters ^[1-9]((\d[1-9])|([1-9]\d))\d{7}$

10 cyfrowy numer NIP.
expectedEndDate	
string or null <date>

Data wycofania zgody na przesyłanie faktur z załącznikiem.
Responses
	req / s 	req / min 	req / h 	grupa
Limity liczby żądań 	60 	- 	- 	-
Response Headers Retry-After	
integer <int32> (RetryAfter)
Example: "30"

Liczba sekund po których można ponowić żądanie.
Response Schema: application/json
required
	
object

Informacje o błędzie związanym z przekroczeniem limitu żądań.
code
required
	
integer

Kod statusu HTTP odpowiadający błędowi. Zawsze ma wartość 429.
description
required
	
string

Opis błędu zgodny z nazwą statusu HTTP.
details
required
	
Array of strings

Lista szczegółowych informacji opisujących przyczynę przekroczenia limitu żądań oraz wskazówki dotyczące ponowienia żądania.
Request samples

    Payload

Content type
application/json
{

    "nip": "7762811692"

}
Response samples

    400429

Content type
application/json
{

    "exception": {
        "exceptionDetailList": [],
        "referenceNumber": "a1b2c3d4-e5f6-4789-ab12-cd34ef567890",
        "serviceCode": "00-c02cc3747020c605be02159bf3324f0e-eee7647dc67aa74a-00",
        "serviceCtx": "srvABCDA",
        "serviceName": "Undefined",
        "timestamp": "2025-10-11T12:23:56.0154302"
    }

}