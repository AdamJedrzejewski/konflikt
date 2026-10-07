# Próba trzech pojęć, 24.09.2026

Status: ekstrakcja kandydacka z zamkniętego zbioru lokalnych materiałów. Bez weryfikacji aktualnego prawa i bez publikacji do aplikacji. Zlecenie użytkownika: „czy możemy w ramach testu puścić jakieś 3 pojęcia ?”. Pojęcia dobrane przez prowadzącego: klient (KL), sprawa ta sama lub związana (SP), osoba najbliższa (ON). Wykonawcy: gpt-6-luna/high, maksymalnie dwóch jednocześnie. Kontrola: Astra.

## Materiał

Przeczytaj AGENTS.md kancelarii, plan `OBSIL/dokumentacja/PLAN_BUDOWY_BAZY.md` i wykaz `01_PUNKTY_SCHEMATU_I_POJECIA.md`. Źródła określa `00_MANIFEST_ZRODEL.json`. Ścieżki w nim są względem OBSIL. Wykorzystuj pola `text` do lektury, `source` do pochodzenia. Manifest zapisuje kontrolne odciski plików, aby wykryć zmianę źródła podczas pracy.

SRC-01 to tekst komentarza oznaczony jako do korekty autorskiej. SRC-02 to wybór orzeczeń, nie domyślnie pełne oryginały. SRC-03 to lokalny PDF opracowania; ustal autora i charakter z treści albo oznacz brak ustalenia. SRC-04 i SRC-05 są lokalnymi kopiami aktów, bez potwierdzenia aktualności na dziś. SRC-06 to opracowanie przepisów. SRC-07 to wtórny wybór WSD z zastrzeżeniem roboczego OCR. SRC-08 i SRC-09 to robocze karty modelu; trop do sprawdzenia, nie samodzielny dowód poprawności. Nie licz powtórzeń tej samej tezy w opracowaniach jako niezależnych potwierdzeń.

Wyszukaj pojęcie, jego odmiany i terminy powiązane we wszystkich dziewięciu pozycjach. Czytaj pełny dotyczący go blok (akapit/sekcja), wraz z otoczeniem koniecznym do ustalenia autora i ograniczeń. Nie czytaj całych wielkich plików przez terminal naraz. Brak trafienia po nazwie nie kończy przeglądu kontekstowego. Odnotuj dokładnie zakres przeczytany i pominięty. Nie korzystaj z sieci ani pamięci prawa. Nie otwieraj .env, kopii baz ani archiwów serwera.

## Wynik jednego agenta

Zapisz wyłącznie przydzielony JSON: `01_klient.json`, `02_sprawa.json` lub `03_osoba_najblizsza.json`. Nie zmieniaj innych plików i nie deleguj dalej. Kodowanie UTF-8, poprawny JSON. Opis po polsku, bez długich myślników; dowody dosłowne, preferuj fragmenty bez takiego znaku, nie zmieniaj cytatu. Znaczenia i twierdzenia są kandydatami do kontroli.

Struktura JSON:

```json
{
  "concept_id": "KL",
  "concept": "klient",
  "model": "gpt-6-luna",
  "status": "KANDYDAT_DO_KONTROLI",
  "scope": "Zakres faktycznie opracowany, ograniczenia próby",
  "scheme_points": ["S2-K3-00"],
  "coverage": [{"source_id":"SRC-01","status":"sprawdzony / brak relewantnej tresci / czesciowy / nieodczytany","read_ranges":"wiersze/sekcje","notes":"powód i ograniczenia"}],
  "meanings": [{"id":"KL-M01","context":"kontekst wynikający z materiału","description":"ostrożne objaśnienie","record_ids":["KL-R01"]}],
  "records": [{
    "id":"KL-R01",
    "kind":"przepis / poglad_autora / stanowisko_uczestnika / stanowisko_sadu_relacjonowane / rozstrzygniecie_relacjonowane / brak_atrybucji",
    "claim":"jedno twierdzenie w parafrazie",
    "speaker":"osoba/organ faktycznie ustalony lub nie ustalono",
    "role":"np. autor komentarza; sąd wg wyboru; obwiniony",
    "context":"instytucja, przepis, stan faktyczny i czas według materiału",
    "court_treatment":"przyjete / odrzucone / ograniczone / nieocenione / nie_ustalono / nie_dotyczy",
    "source_status":"np. komentarz roboczy; wybór fragmentów, bez oryginału",
    "evidence":[{"source_id":"SRC-01","line_start":1,"line_end":2,"quote":"krótki dosłowny, ciągły fragment; bez wielokropków dodanych przez model"}],
    "limits":"warunki, braki, brak potwierdzenia aktualności",
    "related_record_ids":[]
  }],
  "relations":[{"from":"KL-M01","relation":"wyjasniane_przez","to":"KL-R01","status":"kandydat","record_ids":["KL-R01"]}],
  "gaps":[{"id":"KL-G01","issue":"czego nie ustalono","needed":"jaki materiał rozstrzygnie"}],
  "proposals":[{"id":"KL-P01","change":"proponowane rozszerzenie/powiązanie","basis_ids":["KL-R01"],"operator_status":"OCZEKUJE"}],
  "control_results": {"T1":{"party_claim":"","court_claim":"","treatment_of_party":""},"T2":{"court_claim_confirmed":false,"prosecutor_view_available":false},"T3":{"merge_definitions":false},"T4":{"court_treatment":"","prosecutor_view_available":false}},
  "self_check":"co sprawdzono i co pozostaje do sprawdzenia"
}
```

Zastąp KL odpowiednim prefiksem. Numeracja wierszy: od 1 w pliku z pola `text`, bez dopisywania numerów do samego źródła. Każdy cytat ma być rzeczywistym fragmentem podanego zakresu. Nie przedstawiaj cytatu z opracowania jako sprawdzonego z oryginałem wyroku. Stanowisko sądu relacjonowane w komentarzu zapisuj z tym statusem i autorem relacji. Brak głosu rzecznika lub obwinionego nie upoważnia do wymyślania ich poglądów. W przypadku orzecznictwa sprawdź osobno role: obwiniony, rzecznik, sąd; wyniki braków zapisz w gaps.

Oddziel różne konteksty i nie zastępuj kwalifikacji relacji wyłącznie nazwą dziedziny. Wyjątek wymaga wskazania reguły i warunków. Brak samodzielnych tekstów z danej dziedziny oznacza brak, nie zgodność definicji. Własne propozycje powiązań bez źródła oznacz `hipoteza_do_sprawdzenia`; nie traktuj ich jako tezy materiału.

Celem próby jest użyteczny, sprawdzalny rdzeń pojęcia, orientacyjnie 8–15 jednostkowych rekordów na pojęcie, a nie pełna monografia. W razie szerszego materiału wybierz zróżnicowane istotne tezy i jawnie wskaż niewyczerpany zakres. Nie mnoż rekordów, jeśli brakuje źródeł. Nie nazywaj ograniczonego wyniku kompletną bazą pojęcia.

## Osobna kontrola metodologiczna, materiał fikcyjny

Poniższych czterech fragmentów nie wolno umieszczać w records/meanings ani przedstawiać jako źródeł prawnych. Wynik jedynie w control_results.

T1: „Obwiniony twierdził: pojęcie X obejmuje wyłącznie A. Sąd odrzucił ten pogląd i przyjął, że w rozpatrywanym kontekście X obejmuje A oraz B.” Zapisz osobno oba poglądy i ocenę poglądu obwinionego.

T2: Opracowanie zawiera nagłówek „Teza: zachowanie było niedopuszczalne”. Jedyny przytoczony fragment brzmi „Zarzut: obwiniony podjął zachowanie Z”. Nie ma informacji o wyniku ani innych wypowiedzi. Ustal, czy potwierdzono stanowisko sądu i czy dostępny jest pogląd rzecznika.

T3: Fikcyjny tekst A definiuje X jako wyłącznie A1. Fikcyjny tekst B w innej instytucji definiuje X jako wyłącznie B1. Nie ma przepisu odsyłającego ani uzasadnienia łączenia. Ustal, czy scalić definicje w jedno znaczenie.

T4: „Sąd pozostawił bez oceny pogląd obwinionego o pojęciu X, ponieważ rozstrzygnięcie oparto na innej przesłance”. Nie podano wypowiedzi rzecznika. Oznacz ocenę sądu i dostępność stanowiska rzecznika.

## Odbiór

Prowadzący sprawdzi cytaty i zakresy wierszy, wszystkie atrybucje i ograniczenia wybranych rekordów, poprawność powiązań, zgodność z punktami schematu i kontrolę T1–T4. Brakujący materiał jest dopuszczalnym wynikiem. Błędny autor, zmyślony cytat i przeniesienie znaczenia bez podstawy wymagają poprawy. Po jednej nieudanej korekcie zadanie przejmuje prowadzący. Wynik i propozycje pozostają oczekujące na decyzję operatora. Ta próba nie jest testem wdrożonej aplikacji ani jej systemu samodoskonalenia.
