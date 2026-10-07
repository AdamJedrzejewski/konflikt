# Wynik próby trzech pojęć, 24.09.2026

Przeprowadzono trzy odrębne zadania zlecone modelowi gpt-6-luna, z przygotowaniem i odbiorem przez Astrę. Jednocześnie pracowało najwyżej dwóch wykonawców. Wyniki są kandydatami po kontroli wierności lokalnym materiałom, oczekującymi na decyzję operatora.

Łącznie: **36 zapisów, 46 przytoczeń źródłowych i 7 propozycji zmian/powiązań**. Każda karta ma zakres przeglądu wszystkich dziewięciu pozycji manifestu; duże dokumenty czytano w wybranych blokach. To ograniczona próba, nie pełne opracowanie pojęć.

| Karta | Zapisy | Przytoczenia | Propozycje dla operatora |
|---|---:|---:|---:|
| [klient](01_klient.md) | 13 | 16 | 3 |
| [sprawa ta sama lub związana](02_sprawa.md) | 13 | 16 | 1 |
| [osoba najbliższa](03_osoba_najblizsza.md) | 10 | 14 | 3 |

## Wynik odbioru

Luna przygotowała użyteczne propozycje, lecz pierwsze wersje wymagały korekt. Część problemów usunięto w jednej rundzie uwag do wykonawcy, pozostałe poprawiła Astra. Zachowano [wyniki wykonawców](00_wyniki_luny/) przed końcowymi zmianami odbioru. Szczegóły zmian są także w polu review końcowych plików JSON.

- Klient: rozdzielono ocenę OSD, przyznanie faktów przez obwinionego oraz pogląd SN przytoczony przez OSD. Nie dopisano nieznanego stanowiska rzecznika. Doprecyzowano dowody dotyczące wyodrębnienia osiedla i sformułowania „były klient”.
- Sprawa ta sama lub związana: zachowano odrębność art. 27 w przykładzie wcześniejszej mediacji oraz konfiguracji art. 28–30. Przy doradztwie zachowano warunki zgody. Poprawiono zdanie, które zamiast możliwości wykorzystania tajemnicy wymagało rzeczywistego wykorzystania.
- Osoba najbliższa: Luna samodzielnie wskazała rozbieżność § 1/§ 11 w odesłaniu przytoczonym w wyborze orzeczeń. Zachowano ją do rozstrzygnięcia, bez poprawiania źródła. Odróżniono pogląd komentatora o bliskoznaczności relacji od definicji KERP. Brak materiału z innych instytucji prawa pozostaje luką.

Automatyczna kontrola potwierdziła zgodność wszystkich przytoczeń z podanymi wierszami (z ujednoliceniem wyłącznie konwencji końca wiersza CRLF/LF), poprawność odwołań i niezmienność plików z manifestu. Cytaty z nowych luster porównano także z tekstem wewnętrznym DOCX lub warstwą tekstową PDF. Odbiór Astry objął twierdzenia, role, konteksty i granice wybranych rekordów. Nie potwierdzano aktualności prawa ani oryginałów przywołanych orzeczeń.

Każdy wykonawca prawidłowo rozwiązał cztery krótkie ćwiczenia kontrolne: rozdzielenie obwinionego i sądu, brak wnioskowania o sądzie z samego zarzutu, rozdział kontekstów oraz pozostawienie stanowiska bez oceny. Były to jawne przykłady z briefu, a nie niezależny pomiar trafności prawnej.

## Co próba zmienia w organizacji kolejnej partii

Najważniejszy wniosek: zgodność cytatu nie wystarcza. W końcowych wynikach Luny zdarzyły się dokładne cytaty, które pomijały zdanie uzasadniające istotny element tezy. Odbiór musi osobno sprawdzać: czy cytat istnieje, czy podpiera całą tezę i czy wypowiedź należy do wskazanego autora. Dla kolejnych partii zachować rozdział pracy: Luna proponuje zapisy, Astra odbiera znaczenie i przypisanie, operator zatwierdza publikację.

Przed szerszą ekstrakcją naprawić przygotowanie komentarza Word: standardowe lustro pomija część wstawek ze zmian rejestrowanych. W tej próbie wyłączono dotknięte akapity, a wykorzystane fragmenty dodatkowo sprawdzono. Szczegóły: [jakość źródeł](00_JAKOSC_ZRODEL.md). Nie zmieniano oryginałów.

Karty pozwalają już prześledzić kandydackie powiązanie: punkt schematu → znaczenie w danym kontekście → odrębne twierdzenie → fragment materiału. Są to dane do dalszej budowy, nie działający mechanizm analizy w aplikacji. Nie mierzono kosztu tokenów ani oszczędności względem wykonania całości przez Astrę.

## Stan publikacji i samodoskonalenia

Propozycje (7) mają status OCZEKUJE. Nie wprowadzono ich do zatwierdzonej wiedzy ani kodu aplikacji. Próba zapisuje wyniki prac agentów i propozycje w plikach. Nie wdraża jeszcze zapisu rozmów użytkowników, automatycznego wykrywania luk, panelu operatora, wersjonowanej publikacji ani cofania decyzji. Warunek tych funkcji od pierwszego testu użytkowego aplikacji nadal obowiązuje.

## Materiał kontroli

- [Zlecenie i kryteria](00_ZLECENIE_I_KRYTERIA.md).
- [Manifest dziewięciu pozycji](00_MANIFEST_ZRODEL.json).
- [Kontrola techniczna](00_KONTROLA_TECHNICZNA.json).
- Każda karta ma obok plik JSON ze źródłami, powiązaniami, lukami, propozycjami i uwagami odbioru.
