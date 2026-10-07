import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK_DIR = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-010" / "cdda4dd48d1e4f0b86268504ac7e7c9e"
MANIFEST = json.loads((TASK_DIR / "zlecenie.json").read_text(encoding="utf-8"))
SOURCE = {s["id"]: (ROOT / s["text"]).read_text(encoding="utf-8-sig").splitlines() for s in MANIFEST["sources"]}

def exact_line(source_id, line_no):
    return SOURCE[source_id][line_no - 1]

result = {
    "task_id": "cdda4dd48d1e4f0b86268504ac7e7c9e",
    "concept_id": "OBS-010",
    "label": "doradztwo prawne",
    "points": ["S2-K3-06", "S2-K3-09", "S2-K4-04", "S2-K4-07"],
    "scope": "Uzupełniam znaczenie doradztwa w punktach S2-K3-06, S2-K3-09, S2-K4-04 i S2-K4-07 o komentarzowe rozróżnienie doradzania od reprezentacji oraz o zbieg standardów, gdy wobec klientów wykonywano różne czynności zawodowe. Nie powielam ustawowego katalogu pomocy prawnej z OBS-040-R01, normy i wyjątków art. 29 z SP-R07, opracowanych konfiguracji zgody z OBS-076-R01/R06 ani rozbieżności odesłania z OBS-007-R01. OBS-076-R06 już opisuje jako pogląd autora rozszerzenie art. 28 ust. 2 na doradzanie przeciwnikowi procesowemu; wspólne pytanie jest ujęte w OBS-076-Q03 i grupie K-03 konsultacji, dlatego nie tworzę duplikatu. Lektura obejmowała wskazane fragmenty i kontekst źródeł, nie cały korpus ani pełne oryginały orzeczeń.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-040-R01", "SP-R07", "OBS-076-R01", "OBS-076-R06", "OBS-007-R01", "KL-R02", "KL-R08"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "904-916; 964-992; 1116-1156", "notes": "Komentarz roboczy autora. Czytano akapity o kryterium rodzaju czynności, art. 6 u.r.p., art. 28-29 oraz zbiegu standardów; zachowano markery i status poglądu."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "80-103", "notes": "Wtórny wybór orzeczeń, fragmenty o reprezentacji i doradztwie; nie traktowano selekcji jako pełnych oryginałów ani ogólnej definicji."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "950-1010; 1113-1178", "notes": "Fragmenty poradnika i opracowania o art. 28-29, doradztwie oraz zgodzie; wnioski przypisywane autorowi, nie przepisowi."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "167-205", "notes": "Tekst art. 26a-29 KERP czytany w całości dla normatywnego kontekstu; źródło nie definiuje szerzej doradztwa."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "47-123", "notes": "Ustawa o radcach prawnych, w tym art. 4 i 6 oraz ich otoczenie, dla odróżnienia ustawowego katalogu od komentarzowej klasyfikacji."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "119-179; 293-321", "notes": "Fragmenty tekstów źródłowych i tabela relacji art. 26a, 28 i 29; wykorzystane jako kontekst norm, nie jako nowa teza."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "157-190", "notes": "Wtórne zestawienie orzecznictwa i oznaczenia spraw dotyczące art. 29; bez przypisywania sądowi komentarzowej klasyfikacji doradztwa."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały plik, definicja sprawy tej samej lub związanej; kontekst pojęć, bez nowej tezy o doradztwie."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Cały plik, definicja klienta aktualnego i byłego; kontekst relacji klienta, bez nowej tezy o doradztwie."}
    ],
    "meanings": [
        {"id": "OBS-010-M01", "context": "Rozróżnienie doradztwa od reprezentacji dla S2-K3-06, S2-K3-09, S2-K4-04 i S2-K4-07", "description": "Komentator odczytuje przykłady z art. 6 ust. 1 u.r.p. tak, że porady i konsultacje, opinie oraz projekty aktów prawnych należą do doradztwa, natomiast występowanie przed urzędami i sądami jako pełnomocnik lub obrońca jest odrębnym rodzajem czynności. To klasyfikacja autora komentarza oparta na ustawowym wyliczeniu, nie wyczerpująca definicja każdej czynności doradczej. Dalsza kwalifikacja konfliktu pozostaje zależna od konfiguracji KERP i nie przenosi automatycznie reguł reprezentacji na doradztwo.", "record_ids": ["OBS-010-R01", "OBS-040-R01", "SP-R07"]},
        {"id": "OBS-010-M02", "context": "Mieszane czynności zawodowe dla różnych klientów, szczególnie S2-K3-09 i S2-K4-07", "description": "Komentator wskazuje, że gdy wobec jednego klienta radca jest lub był obrońcą albo pełnomocnikiem, a drugiemu świadczy doradztwo, pojawia się zbieg standardów z art. 28 i 29 KERP. Jest to mapa właściwych reżimów i odesłanie do komentarza art. 28, a nie samodzielny wynik co do dopuszczalności konkretnej sprawy. Dalsza analiza powinna zachować odrębnie normę art. 29, wyjątek KERP i pogląd OBS-076-R06 o przeciwniku procesowym.", "record_ids": ["OBS-010-R02", "SP-R07", "OBS-076-R06", "OBS-007-R01"]}
    ],
    "records": [
        {"id": "OBS-010-R01", "kind": "poglad_autora", "claim": "Autor komentarza klasyfikuje trzy pierwsze czynności wymienione w art. 6 ust. 1 u.r.p. jako doradztwo prawne, a występowanie przed urzędami i sądami jako pełnomocnik lub obrońca jako kategorię reprezentacji lub obrony.", "speaker": "P. Skuczyński, autor komentarza SRC-01", "role": "autor komentarza roboczego do korekty autorskiej", "context": "Rozróżnienie rodzaju czynności dla zastosowania standardów konfliktu z art. 28 i 29 KERP; kontekst art. 6 ust. 1 u.r.p.", "court_treatment": "nie_dotyczy; klasyfikacja autora, nie wypowiedź sądu ani sam tekst przepisu", "source_status": "komentarz roboczy; cytowany fragment zawiera wyraźne rozróżnienie, ale nie stanowi pełnej definicji legalnej doradztwa", "evidence": [{"source_id": "SRC-01", "line_start": 908, "line_end": 908, "quote": exact_line("SRC-01", 908)}], "limits": "Ustawa podaje przykładowe czynności pomocy prawnej, a teza o zakwalifikowaniu pierwszych trzech do doradztwa jest interpretacją komentatora. Nie należy z niej wyprowadzać, że katalog jest zamknięty ani że każda czynność poza występowaniem procesowym jest doradztwem. Różnica pełnomocnik-obrońca i kwestie umocowania są odrębnie omówione przez autora w sąsiednim akapicie."},
        {"id": "OBS-010-R02", "kind": "poglad_autora", "claim": "Autor komentarza wskazuje na zbieg standardów art. 28 i 29 KERP, gdy różnym klientom świadczono różne czynności: wobec jednego klienta radca był lub jest obrońcą albo pełnomocnikiem, a drugiemu udzielał doradztwa.", "speaker": "P. Skuczyński, autor komentarza SRC-01", "role": "autor komentarza roboczego do korekty autorskiej", "context": "Mieszana konfiguracja relacji klientów i rodzaju czynności; odesłanie autora do uwag nr 4 i 5 do art. 28 KERP.", "court_treatment": "nie_dotyczy; twierdzenie autora komentarza, nie rozstrzygnięcie sądu", "source_status": "komentarz roboczy; nie sprawdzano wskazanych w tym zdaniu uwag nr 4 i 5 jako niezależnej podstawy nowego wniosku", "evidence": [{"source_id": "SRC-01", "line_start": 1148, "line_end": 1148, "quote": exact_line("SRC-01", 1148)}], "limits": "Zdanie identyfikuje zbieg regulacyjnych standardów i miejsce dalszego omówienia, ale nie samo rozstrzygnięcie, czy konkretne świadczenie jest dopuszczalne. Nie utożsamia doradztwa z reprezentacją i nie usuwa różnicy między art. 28 a art. 29. Dla konfiguracji doradzania przeciwnikowi zachować status interpretacyjny OBS-076-R06 i istniejące pytanie OBS-076-Q03/K-03; dla art. 29 zachować normę i wyjątek opisane w SP-R07."}
    ],
    "relations": [],
    "gaps": [
        {"id": "OBS-010-G01", "issue": "Komentarz rozdziela przykłady doradztwa od reprezentacji, ale nie podaje w przytoczonym fragmencie kryteriów kwalifikacji wszystkich czynności mieszanych lub granicznych.", "needed": "Przykłady graniczne albo stanowisko eksperta, czy podział z art. 6 ust. 1 u.r.p. ma być używany wyłącznie jako orientacyjny, czy także do kwalifikowania innych form pomocy."},
        {"id": "OBS-010-G02", "issue": "Komentator odsyła przy zbiegu standardów do uwag nr 4 i 5 do art. 28; niniejsza karta nie rozstrzyga na ich podstawie konkretnych skutków dla każdej mieszanej konfiguracji.", "needed": "Odrębna ocena konfiguracji po ustaleniu faktów sprawy i właściwych standardów. Pytanie o doradzanie przeciwnikowi już jest OBS-076-Q03/K-03 i nie jest tu powielane."}
    ],
    "questions": [],
    "self_check": "Sprawdzono dziewięć źródeł w zakresach podanych w coverage; pełne odczytanie zadeklarowano tylko dla SRC-08 i SRC-09. Nowe tezy mają cytaty pobrane programowo jako dokładne wiersze lustra SRC-01. Rozdzielono stanowisko komentatora od ustawy, KERP i orzeczeń. Nie skopiowano istniejącej tezy o katalogu pomocy prawnej, normy zgody ani interpretacji art. 28 ust. 2. Nie utworzono pytania powielającego OBS-076-Q03/K-03. Status pozostaje OCZEKUJE; odbiór należy do Astry."
}

out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out)

sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka
queue_dir = ROOT / "baza_wiedzy" / "kolejka_79"
state = kolejka.load(queue_dir)
job = kolejka.get_job(state, result["concept_id"])
kolejka.validate_result(state, job, result)
print("validate_result: OK (bez zapisu do kolejki)")
