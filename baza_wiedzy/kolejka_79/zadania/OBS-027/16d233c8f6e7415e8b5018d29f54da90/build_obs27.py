import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-027" / "16d233c8f6e7415e8b5018d29f54da90"
sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(ROOT / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-027")
attempt_id = job["attempts"][-1]["id"]

result = {
    "task_id": attempt_id,
    "concept_id": "OBS-027",
    "label": "niekorzystne rozstrzygnięcie",
    "points": ["S1-K2-05"],
    "scope": "S1-K2-05 posługuje się w art. 27 pkt 5 zwrotem „niekorzystnym dla klienta rozstrzygnięciem sprawy”; literalną normę ujęto w OBS-043-R01. Przejrzane fragmenty nie definiują niekorzystności ani nie przesądzają, czy wymaga ona formalnej przegranej, majątkowej straty lub innego konkretnego skutku. OBS-015-R01/R02 opisuje cel pomocy i interes klienta, a OBS-057-R01/R02 materialną sprzeczność i odrębność formalnych przesłanek; są to konteksty ogólne lub inne konfiguracje, nie definicja art. 27 pkt 5. OBS-037-Q01 dotyczy kryterium zainteresowania osoby wynikiem; niniejsze pytanie dotyczy znaczenia samej niekorzystności dla klienta i może być skoordynowane z tamtą konsultacją, ale zachowuje odmienny element normy. Nie utożsamiam jej automatycznie z formalną przegraną ani stratą ekonomiczną. Karta jest częściowa, bo korpus nie dostarcza testu niekorzystnego rozstrzygnięcia w tej przesłance.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "OBS-043-R01",
        "OBS-015-R01", "OBS-015-R02",
        "OBS-057-R01", "OBS-057-R02"
    ],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "792; 804-808; 1224-1244", "notes": "W. 792 to tekst pkt 5, a w. 804–808 ogólne objaśnienie art. 27, bez definicji niekorzystnego wyniku. W. 1224–1228 opisuje zarzut/stanowisko w D 24/2015 dotyczące niekorzystnej umowy i restrukturyzacji, a w. 1240–1244 fragment D 59/20 o sprzecznych interesach w odrębnych układach; te przykłady nie są wykładnią art. 27 pkt 5."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "110-112", "notes": "WO-87/21 zawiera relacjonowaną ocenę bezpośredniego zainteresowania samego radcy w kontekście art. 30; nie definiuje niekorzystnego dla klienta rozstrzygnięcia z art. 27 pkt 5."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "754-784", "notes": "Odczytano listę art. 27 pkt 5 i ogólną autorską charakterystykę tej konfiguracji. Autor nie definiuje w tym fragmencie niekorzystności; SRC-03 i SRC-01 to materiały tego samego autora, nie niezależne opinie."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "79-81; 183", "notes": "Art. 10 opisuje cele obowiązku unikania konfliktu, a art. 27 pkt 5 używa badanego zwrotu; żaden z tych fragmentów nie określa testu niekorzystności."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "47; 93-123", "notes": "Wcześniej sprawdzony zakres o ustawowej pomocy prawnej i wykonywaniu zawodu. Nie wykorzystuję go do wyprowadzania znaczenia „niekorzystnego rozstrzygnięcia” z KERP."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "99-113", "notes": "Wtórne zestawienie konfiguracji art. 27 powtarza brzmienie pkt 5, bez objaśnienia badanego zwrotu."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "185-189", "notes": "Wtórne omówienie WO-87/21 opisuje interes samego radcy w sporze rodzinnym; kontekst art. 30 nie stanowi testu dla art. 27 pkt 5."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały krótki glosariusz sprawy tej samej i związanej; nie wyjaśnia znaczenia niekorzystności wyniku."},
        {"source_id": "SRC-09", "status": "CZESCIOWY", "read_ranges": "9-20", "notes": "Odczytano fragmenty o ochronie byłego klienta i skutkach po ustaniu współpracy w kontekście art. 28/29; to nie objaśnia badanego zwrotu art. 27 pkt 5."}
    ],
    "meanings": [
        {
            "id": "OBS-027-M01",
            "context": "S1-K2-05, art. 27 pkt 5 KERP: niekorzystny dla klienta wynik, który może interesować osobę bliską radcy",
            "description": "Literalna norma wymaga, by rozstrzygnięcie sprawy było niekorzystne dla klienta i by istniała bliska relacja radcy z osobą zainteresowaną takim wynikiem (OBS-043-R01). W przejrzanych fragmentach nie znaleziono definicji niekorzystności ani przesądzenia, czy chodzi wyłącznie o formalną przegraną lub stratę majątkową. Pojęcie interesu klienta (OBS-015-R01/R02) i materialnej sprzeczności interesów (OBS-057-R01/R02) są pomocniczym kontekstem, lecz same nie zastępują wykładni tego elementu art. 27 pkt 5. OBS-037-Q01 dotyczy osobno, jaki interes wiąże osobę z wynikiem.",
            "record_ids": ["OBS-043-R01", "OBS-015-R01", "OBS-015-R02", "OBS-057-R01", "OBS-057-R02"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {"id": "OBS-027-G01", "issue": "Przejrzane źródła przytaczają zwrot „niekorzystnym dla klienta rozstrzygnięciem”, ale nie określają, jakie skutki dla klienta czynią wynik niekorzystnym w rozumieniu art. 27 pkt 5. Przykłady sporów umownych lub materialnej sprzeczności z innych konfiguracji nie rozstrzygają tego elementu.", "needed": "Ekspercka wykładnia pojęcia niekorzystnego dla klienta rozstrzygnięcia w art. 27 pkt 5, z rozróżnieniem formalnego wyniku sprawy i skutków dla interesów klienta oraz bez zakładania, że warunkiem jest strata majątkowa."}
    ],
    "questions": [
        {
            "id": "OBS-027-Q01",
            "record_ids": ["OBS-043-R01", "OBS-015-R01", "OBS-015-R02", "OBS-057-R01", "OBS-057-R02"],
            "understanding": "Art. 27 pkt 5 wymaga zainteresowania osoby rozstrzygnięciem niekorzystnym dla klienta. Materiał nie objaśnia, co jest niekorzystne. OBS-037-Q01 pyta o to, jaki interes musi wiązać osobę z wynikiem; tutaj pytanie dotyczy charakteru samego wyniku dla klienta. Ogólne ujęcie interesu klienta i materialnej sprzeczności pozostaje kontekstem, nie gotową definicją.",
            "variants": "Do rozstrzygnięcia pozostaje, czy zwrot odnosi się tylko do formalnego wyniku postępowania, czy może także do skutku rozstrzygnięcia dla pozycji prawnej lub innych interesów klienta mimo formalnie korzystnego wyniku. Nie wiadomo też z przejrzanych tekstów, czy konieczny jest uszczerbek majątkowy; nie przyjmuję takiego wymogu ani jego braku jako ustalonej reguły.",
            "consequences": "Wykładnia określi, jaki wynik może stanowić przedmiot zainteresowania osoby z drugiej alternatywy art. 27 pkt 5. Pozwoli oddzielić ocenę wyniku dla klienta od oceny interesu osoby oraz od definicji materialnej sprzeczności w innych przepisach.",
            "question": "Co oznacza „niekorzystne dla klienta rozstrzygnięcie sprawy” w art. 27 pkt 5: czy musi chodzić o formalnie niekorzystny wynik postępowania, czy może również o rozstrzygnięcie formalnie korzystne, lecz niekorzystne dla konkretnego interesu klienta? Czy niekorzystność wymaga skutku majątkowego, czy może dotyczyć także innego interesu klienta? Proszę wskazać kryterium właściwe dla tej przesłanki, bez automatycznego przenoszenia testu z art. 30 lub art. 28–29.",
            "needed": "Ekspercka wykładnia znaczenia niekorzystności dla klienta w art. 27 pkt 5. Można skoordynować odpowiedź z OBS-037-Q01, zachowując osobno test interesu osoby oraz test wyniku dla klienta."
        }
    ],
    "self_check": "Nie dodałem nowych rekordów, bo przejrzane materiały nie zawierają odrębnej definicji zwrotu z art. 27 pkt 5, a literalną normę odtwarza OBS-043-R01. Zachowałem oddzielnie interes klienta z OBS-015, materialną sprzeczność z OBS-057 i pytanie OBS-037 o interes osoby. Przykładów dotyczących umów, art. 30 ani interesu samego radcy nie uznałem za definicję niekorzystnego wyniku. Coverage wskazuje rzeczywiście przejrzane zakresy dziewięciu źródeł. To samokontrola wykonawcy, nie odbiór Astry."
}

out = TASK / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
kolejka.validate_result(state, job, result)
print(json.dumps({"validated": True, "path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "attempt_id": attempt_id}, ensure_ascii=False))
