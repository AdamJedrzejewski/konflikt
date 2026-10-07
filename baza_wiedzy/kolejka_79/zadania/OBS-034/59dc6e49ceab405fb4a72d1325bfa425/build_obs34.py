import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
prior_path = root / "baza_wiedzy/kolejka_79/zadania/OBS-016/0ffa132749e340879b03c362d86c9e4d/wynik.json"
coverage = json.loads(prior_path.read_text(encoding="utf-8"))["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["read_ranges"] = "828; 832; 1276"
        item["notes"] = "Komentarz roboczy, nie tekst normy: w. 828 przedstawia jako pogląd autora bliskoznaczność określeń art. 27 pkt 3, 5 i 6; w. 832 odrębnie ujmuje węższy sens udziału w rozstrzygnięciu z pkt 3. W. 1276 odnosi definicję art. 5 pkt 7 do art. 30."
    elif item["source_id"] == "SRC-02":
        item["read_ranges"] = "110-112"
        item["notes"] = "Wtórny wybór WO-87/21: w. 112 opisuje przypisany czyn i nie daje samoistnej normy o art. 27. Oryginału orzeczenia brak; zakres ten nie służy do wyprowadzania ogólnego zakazu pomocy rodzinie."
    elif item["source_id"] == "SRC-03":
        item["read_ranges"] = "723-730"
        item["notes"] = "Poradnik tego samego autora objaśnia art. 30: interes osoby najbliższej, realny konflikt lub oceniane przez radcę znaczne ryzyko. Nie jest niezależnym potwierdzeniem komentarza SRC-01."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "39-53; 173-185; 207-209"
        item["notes"] = "Lokalny tekst: definicyjne odesłanie art. 5 pkt 7, odrębne brzmienie art. 27 pkt 3 i 6 oraz art. 30 ust. 1. Zachowano różne osoby i dodatkowe warunki."
    elif item["source_id"] == "SRC-07":
        item["read_ranges"] = "175-190"
        item["notes"] = "Wtórne opracowanie przy art. 30 streszcza pojedynczy przypadek WO-87/21 i formułuje tezę o pomocy rodzinie. ON-R09 i OBS-018-R05 dokumentują jedną relację, nie są niezależnymi potwierdzeniami; zakres atrybucji pozostaje ograniczony."
    elif item["source_id"] == "SRC-08":
        item["notes"] = "Przeczytano cały plik w poprzednich kartach; definicja sprawy tej samej/związanej, bez objaśnienia statusu osoby najbliższej lub zależnej."
    elif item["source_id"] == "SRC-09":
        item["notes"] = "Przeczytano cały plik w poprzednich kartach; dotyczy klienta aktualnego/byłego, nie różnic z art. 27 pkt 3 i 6."

result = {
    "task_id": "59dc6e49ceab405fb4a72d1325bfa425",
    "concept_id": "OBS-034",
    "label": "osoba najbliższa",
    "points": ["S1-K1-02", "S1-K2-03", "S1-K2-06"],
    "scope": (
        "Mapuję trzy punkty do odmiennych przepisów: S1-K1-02 do art. 30 ust. 1, S1-K2-03 do art. 27 pkt 3 i S1-K2-06 do art. 27 pkt 6. "
        "Dla art. 30 osoba najbliższa jest odrębną stroną relacji interesów z klientem; literalna rama to pomoc „w danej sprawie lub w sprawie z nią związanej”, "
        "a konflikt lub znaczne ryzyko występuje między klientem a radcą lub osobą mu najbliższą. Art. 27 pkt 3 dotyczy osoby najbliższej albo odrębnie osoby pozostającej z jakichkolwiek przyczyn w stosunku "
        "zależności z radcą, gdy brała lub bierze udział w rozstrzygnięciu sprawy. Art. 27 pkt 6 dotyczy wyłącznie osoby najbliższej i wymaga, "
        "by była pełnomocnikiem strony przeciwnej albo wykonywała na jej rzecz w tej sprawie inną pomoc prawną. Nie przenoszę przesłanki "
        "rozstrzygnięcia z pkt 3 na pkt 6 ani dodatkowych wymagań art. 30 na pkt 3/6. ON-R01/02 opisują definicyjne odesłanie i komentarzową listę, "
        "ON-R03/04/05 odtwarzają odpowiednie normy, ON-R06 zachowuje pogląd autora o bliskoznaczności, a ON-R07 odrębne węższe znaczenie udziału "
        "w rozstrzygnięciu. OBS-016 i OBS-017 mapują już znaczenie art. 30; OBS-057-R03 zawiera autorską wykładnię konfliktu i ryzyka. Tabela konsultacji ON-P01 zawiera pełny tekst art. 115 § 11 k.k. i odnotowaną 24.09 kontrolę publikacji urzędowej; otwarte pozostaje szczegółowe zastosowanie kategorii do relacji osób. ON-R10 i OBS-016-G02 zachowują węższy problem: SRC-02 przy WO-87/21 podaje § 1, a oryginału orzeczenia brak; ten problem jest również odnotowany w ON-P03. Historyczna "
        "ON-P02 oraz późniejsza tabela konsultacji pozostawiają do rozstrzygnięcia pogląd o bliskoznaczności; odrębne OBS-058-Q01 dotyczy pozytywnego "
        "testu zależności i kierunku relacji, nie ponawiam tych pytań. Nie traktuję definicji osoby najbliższej jako samodzielnego zakazu pomocy ani "
        "nie uznaję każdej bliskiej lub zależnej osoby za objętą wszystkimi trzema przepisami. ON-R09 i OBS-018-R05 odnoszą się do jednej relacji "
        "wtórnie opisanej przy WO-87/21, nie do dwóch niezależnych potwierdzeń; pierwotne uzasadnienie nie jest w korpusie. Karta jest częściowa, "
        "bo nie rozstrzyga zakresu autorskiej tezy o bliskoznaczności ani pozytywnego kryterium zależności."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "ON-R01", "ON-R02", "ON-R03", "ON-R04", "ON-R05", "ON-R06", "ON-R07", "ON-R08", "ON-R09", "ON-R10",
        "OBS-018-R05", "OBS-057-R03", "SP-R08"
    ],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-034-M01",
            "context": "S1-K1-02, art. 30 ust. 1 KERP, osoba najbliższa radcy jako odrębna strona konfliktu z klientem",
            "description": (
                "Art. 5 pkt 7 KERP odsyła przy osobie najbliższej do art. 115 § 11 k.k. (ON-R01), a autor komentarza wskazuje, że to znaczenie "
                "stosuje się w art. 30 ust. 1 (ON-R08); ON-R05 odtwarza normę. Sam status osoby najbliższej nie wystarcza: art. 30 wymaga danej "
                "lub związanej sprawy oraz istniejącego konfliktu interesów albo znacznego ryzyka jego wystąpienia. Ujęcie materialnej sprzeczności "
                "i ryzyka w OBS-057-R03 jest poglądem autora, nie dodatkową normą. Nie wynika stąd ogólny zakaz pomocy rodzinie."
            ),
            "record_ids": ["ON-R01", "ON-R05", "ON-R08", "OBS-057-R03", "SP-R08"]
        },
        {
            "id": "OBS-034-M02",
            "context": "S1-K2-03, art. 27 pkt 3 KERP, udział w rozstrzygnięciu sprawy",
            "description": (
                "Norma wymienia alternatywnie osobę najbliższą oraz osobę pozostającą z jakichkolwiek przyczyn w stosunku zależności z radcą; "
                "osoba ta brała lub bierze udział w rozstrzygnięciu sprawy (ON-R03). Autor uznaje określenia z pkt 3, 5 i 6 za bliskoznaczne "
                "(ON-R06), ale odrębnie wyjaśnia, że udział w rozstrzygnięciu z pkt 3 jest węższy niż udział w sprawie z pkt 1, bo dotyczy osoby "
                "najbliższej albo zależnej, a nie samego radcy (ON-R07). Pogląd o bliskoznaczności nie zastępuje definicji art. 5 pkt 7 ani nie "
                "rozstrzyga pozytywnego kryterium zależności. ON-P02 pozostaje odrębnym historycznym pytaniem o zakres tej bliskoznaczności; "
                "OBS-058-Q01 pyta o minimalne cechy i kierunek zależności."
            ),
            "record_ids": ["ON-R01", "ON-R03", "ON-R06", "ON-R07"]
        },
        {
            "id": "OBS-034-M03",
            "context": "S1-K2-06, art. 27 pkt 6 KERP, osoba najbliższa radcy i strona przeciwna",
            "description": (
                "Pkt 6 dotyczy osoby najbliższej radcy, jeżeli jest ona pełnomocnikiem strony przeciwnej albo wykonywała na jej rzecz inną pomoc "
                "prawną w tej sprawie (ON-R04). To odmienna konfiguracja od pkt 3: nie obejmuje tamtej alternatywy o osobie zależnej ani udziału "
                "w rozstrzygnięciu. Definicję osoby najbliższej określa art. 5 pkt 7, ale wymienione w pkt 6 role i ramę tej sprawy trzeba ustalić "
                "osobno. ON-P02 obejmuje także zwrot z pkt 6 w zakresie autorskiej tezy o bliskoznaczności; OBS-043-Q01 odrębnie dotyczy rozumienia "
                "przeciwnika i strony przeciwnej, więc nie tworzę nowego pytania."
            ),
            "record_ids": ["ON-R01", "ON-R04", "ON-R06"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-034-G01",
            "issue": "ON-P01 pozostaje otwarte co do szczegółowego zastosowania kategorii art. 115 § 11 k.k. do konkretnej relacji; tekst paragrafu i kontrola publikacji urzędowej są już w późniejszej tabeli z 24.09, więc nie są brakiem materiału.",
            "needed": "Wykładnia ekspercka zastosowania wskazanej kategorii do konkretnego stanu faktycznego, bez odtwarzania katalogu z intuicji."
        },
        {
            "id": "OBS-034-G02",
            "issue": "Nie ma rozstrzygnięcia eksperckiego, czy i w jakim zakresie można przyjąć autorską bliskoznaczność osoby najbliższej, zależności i bliskich stosunków w art. 27 pkt 3, 5 i 6. Pozostają historyczne ON-P02 i odrębne pytanie OBS-058-Q01 o pozytywne cechy zależności.",
            "needed": "Rozstrzygnięcie ON-P02 co do zakresu argumentu autora, przy zachowaniu literalnych alternatyw pkt 3 i przesłanek pkt 6; osobno odpowiedź na OBS-058-Q01 o kierunek i kryterium zależności."
        },
        {
            "id": "OBS-034-G03",
            "issue": "Fragment SRC-02 o WO-87/21 podaje art. 115 § 1 k.k. i opisuje przypisany czyn, nie pozwala ustalić autorstwa wzmianki o definicji; brak oryginału orzeczenia. ON-R10 i historyczne ON-P03 odnotowują ten problem.",
            "needed": "Oryginał WO-87/21 lub pełny tekst pozwalający ustalić, kto przywołuje § 1 i jaką rolę ten fragment ma w rozumowaniu; nie traktować tego jako odpowiedzi na ON-P01."
        }
    ],
    "questions": [],
    "self_check": (
        "Zmapowałem wszystkie trzy punkty i zachowałem różnice podmiotów oraz dodatkowych przesłanek art. 30, art. 27 pkt 3 i pkt 6. "
        "Autorską bliskoznaczność oznaczyłem jako nierozstrzygnięty pogląd, odróżniając ON-P02 od OBS-058-Q01. Nie dodałem twierdzeń "
        "ani pytań powielających wcześniejsze karty; ON-R09 i OBS-018-R05 potraktowałem jako jedną wtórną relację. Status OCZEKUJE."
    )
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": 0, "questions": 0, "meanings": len(result["meanings"]), "gaps": len(result["gaps"]), "sources": len(coverage)}))
