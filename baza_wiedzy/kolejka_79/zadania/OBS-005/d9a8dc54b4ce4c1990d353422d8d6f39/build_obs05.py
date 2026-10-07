import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
prior_path = root / "baza_wiedzy/kolejka_79/zadania/OBS-034/59dc6e49ceab405fb4a72d1325bfa425/wynik.json"
coverage = json.loads(prior_path.read_text(encoding="utf-8"))["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["read_ranges"] = "824-852"
        item["notes"] = "Komentarz redakcyjny P. Skuczyńskiego, wersja do korekty: w. 828 pogląd autora o bliskoznaczności; w. 848-852 wtórna relacja D 43/2016. Odczytano otoczenie, w tym wcześniejszą pomoc, związek stron, bliskie stosunki i kontakt z klientami; fragment nie podaje kwalifikacji ani rozstrzygnięcia D 43/2016."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "173-185"
        item["notes"] = "Lokalny art. 27: pkt 5 wymienia byłe lub obecne bliskie stosunki z przeciwnikiem klienta albo osobą zainteresowaną niekorzystnym rozstrzygnięciem; zachowano dwie alternatywy."
    elif item["source_id"] == "SRC-02":
        item["notes"] = "Wtórny wybór orzeczeń; wcześniejszy zakres 110-112 dotyczy WO-87/21, nie D 43/2016. Nie wykazano w tym fragmencie odrębnej tezy o dodatnim teście bliskich stosunków."
    elif item["source_id"] == "SRC-07":
        item["notes"] = "Wtórne streszczenia orzeczeń; przeczytany art. 30 dotyczy WO-87/21, nie stanowi rozstrzygnięcia D 43/2016. Nie łączę go z relacją z SRC-01 jako potwierdzenia."

src01_path = root / "_MD/komentarz_redakcyjny_2026-09-24/Dzial III Rozdzial 2 Zajecia niedopuszczalne oraz konflikt interesow_P. Skuczynski_do korekty autorskiej.docx.md"
src01_lines = src01_path.read_text(encoding="utf-8").splitlines()
quote_anchor = "Obwiniona świadczyła w przeszłości pomoc prawną na rzecz S (2), ponadto pozostawała także z nią w bliskich stosunkach i to S (2) skontaktowała Pokrzywdzonych z Obwinioną."
source_line = src01_lines[851]
start = source_line.find(quote_anchor)
if start < 0:
    raise ValueError("Nie znaleziono dosłownego fragmentu D 43/2016 w wierszu 852")
quote = source_line[start:start + len(quote_anchor)]

result = {
    "task_id": "d9a8dc54b4ce4c1990d353422d8d6f39",
    "concept_id": "OBS-005",
    "label": "bliskie stosunki",
    "points": ["S1-K2-05"],
    "scope": (
        "Punkt S1-K2-05 odpowiada art. 27 pkt 5 KERP: obecne lub byłe bliskie stosunki radcy z przeciwnikiem klienta albo z osobą "
        "zainteresowaną niekorzystnym dla klienta rozstrzygnięciem. OBS-043-R01 odtwarza normatywne alternatywy, a OBS-043-Q01 obejmuje "
        "odrębne pytanie o rozumienie przeciwnika i osoby zainteresowanej. ON-R06 to pogląd autora o bliskoznaczności określeń z pkt 3, 5 i 6, "
        "nie pozytywna definicja ani rozstrzygnięcie operatora; historyczne ON-P02 pyta o zakres tego argumentu, natomiast OBS-058-Q01 dotyczy "
        "osobno kryteriów zależności. Żadne z tych pytań nie ustala dodatnich cech bliskich stosunków. Fragment D 43/2016 w SRC-01 wnosi odmienny "
        "przykład faktów: obwiniona wcześniej udzielała pomocy S (2), pozostawała z nią w bliskich stosunkach, a S (2) skontaktowała ją z "
        "pokrzywdzonymi, których reprezentowała przeciw bankowi. Cytowany fragment nie ustala, że S (2) była przeciwnikiem klienta lub osobą "
        "zainteresowaną niekorzystnym rozstrzygnięciem, i nie przytacza oceny ani wyniku D 43/2016; jest to wtórna relacja w komentarzu, bez "
        "oryginału orzeczenia. Zachowuję w normie zarówno przeszłe, jak i obecne stosunki, ale nie formułuję teraz osobnego pytania o ich granicę "
        "czasową; ten aspekt należy do późniejszego OBS-009. Karta jest częściowa, bo materiał nie dostarcza dodatniego kryterium intensywności "
        "lub charakteru bliskich stosunków."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-043-R01", "ON-R06"],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-005-M01",
            "context": "S1-K2-05, art. 27 pkt 5 KERP, bliskie stosunki radcy z przeciwnikiem klienta albo osobą zainteresowaną niekorzystnym rozstrzygnięciem",
            "description": (
                "Norma obejmuje stosunki, które były albo pozostają aktualne, i wymienia dwie alternatywne osoby po drugiej stronie relacji "
                "(OBS-043-R01). Autor komentarza uważa bliskie stosunki za bliskoznaczne z osobą najbliższą i zależnością w odniesieniu do "
                "wymienionych punktów art. 27, ale jest to jego pogląd interpretacyjny, nie definicja ustawiona w tekście normy (ON-R06). "
                "D 43/2016 wnosi odrębny opis przypadku: obwiniona wcześniej pomagała S (2), pozostawała z nią w bliskich stosunkach, a S (2) "
                "skontaktowała ją z pokrzywdzonymi. Fragment nie wyjaśnia, czy S (2) była przeciwnikiem tych klientów lub osobą zainteresowaną "
                "niekorzystnym rozstrzygnięciem, ani jak OSD zakwalifikował bliskie stosunki. Nie wyprowadzam z niego testu prawnego ani "
                "niezreferowanego wyniku sprawy."
            ),
            "record_ids": ["OBS-043-R01", "ON-R06", "OBS-005-R01"]
        }
    ],
    "records": [
        {
            "id": "OBS-005-R01",
            "kind": "ograniczony_przyklad_faktyczny",
            "claim": (
                "W opisie oznaczonym jako fragment orzeczenia OSD D 43/2016 autor komentarza podaje, że obwiniona wcześniej świadczyła pomoc S (2), "
                "pozostawała z nią w bliskich stosunkach, a S (2) skontaktowała ją z pokrzywdzonymi; dalej opis dotyczy pomocy obwinionej dla "
                "pokrzywdzonych w sporze z bankiem. Ten fragment nie identyfikuje S (2) jako przeciwnika klientów ani osoby zainteresowanej "
                "niekorzystnym rozstrzygnięciem i nie podaje oceny lub rozstrzygnięcia OSD co do art. 27 pkt 5."
            ),
            "speaker": "P. Skuczyński, autor komentarza relacjonujący ustęp oznaczony jako orzeczenie OSD z 9.12.2016 r., D 43/2016",
            "role": "Wtórny opis faktów w komentarzu redakcyjnym do korekty autorskiej, nie oryginał orzeczenia ani samodzielna teza sądu.",
            "context": "Opis dotyczy pożyczki hipotecznej przekazanej S (2), wcześniejszej pomocy prawnej dla S (2), bliskich stosunków z nią oraz późniejszej reprezentacji pokrzywdzonych przeciw bankowi.",
            "court_treatment": "Nagłówek fragmentu wskazuje na orzeczenie OSD D 43/2016, ale przytoczone wiersze przedstawiają tylko opis faktów; nie zawierają oceny sądu ani sentencji w tym zakresie.",
            "source_status": "Nowe lustro komentarza redakcyjnego oznaczonego do korekty; oryginału D 43/2016 nie ma w korpusie.",
            "evidence": [
                {
                    "source_id": "SRC-01",
                    "line_start": 852,
                    "line_end": 852,
                    "quote": quote
                }
            ],
            "limits": "Przykład nie określa dodatniego testu bliskich stosunków; nie stwierdza, że S (2) mieściła się w jednej z alternatywnych kategorii art. 27 pkt 5, ani jaki był wynik postępowania. Nie ustalono z tego fragmentu czasu trwania bliskich stosunków."
        }
    ],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-005-G01",
            "issue": "Przejrzane teksty nie podają dodatnich cech ani progu bliskich stosunków w art. 27 pkt 5. ON-P02 pyta o bliskoznaczność kategorii, a OBS-058-Q01 o zależność; żadne z nich nie rozstrzyga kryteriów samych bliskich stosunków.",
            "needed": "Eksperckie kryteria relacji objętej zwrotem „był albo pozostaje w bliskich stosunkach”, oddzielone od definicji osoby najbliższej i od stosunku zależności."
        }
    ],
    "questions": [],
    "self_check": (
        "Nowy rekord ogranicza się do faktów podanych przy D 43/2016 i wprost nie przypisuje sądowi niewidocznego rozstrzygnięcia. Odróżniłem "
        "przykład od poglądu autora ON-R06 i normy OBS-043-R01. Nie powtórzyłem OBS-043-Q01, ON-P02 ani OBS-058-Q01. Zapis temporalny normy "
        "zachowany bez nowego pytania przed OBS-009. Coverage obejmuje dziewięć źródeł w jawnych zakresach, część lektury wykorzystano z wcześniejszych kart. Status OCZEKUJE."
    )
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "sources": len(coverage)}))
