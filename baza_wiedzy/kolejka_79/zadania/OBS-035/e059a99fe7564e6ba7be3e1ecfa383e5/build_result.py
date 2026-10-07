import json
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
QUEUE_DIR = ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79"
PROJECT = ROOT / "OBSIL"
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka


state = kolejka.load(QUEUE_DIR)
job = kolejka.get_job(state, "OBS-035")
attempt = job["attempts"][-1]
source_paths = {s["id"]: PROJECT / s["text"] for s in state["sources"]}
source_lines = {
    source_id: path.read_text(encoding="utf-8-sig").splitlines()
    for source_id, path in source_paths.items()
}


def excerpt(source_id, line_no, start, end):
    line = source_lines[source_id][line_no - 1]
    start_at = line.find(start)
    if start_at < 0:
        raise ValueError(f"Brak początku cytatu: {source_id}:{line_no}")
    end_at = line.find(end, start_at)
    if end_at < 0:
        raise ValueError(f"Brak końca cytatu: {source_id}:{line_no}")
    return line[start_at : end_at + len(end)]


quote_public_roles = source_lines["SRC-01"][815]
quote_case_title = source_lines["SRC-02"][43]
quote_case_facts = excerpt(
    "SRC-02",
    46,
    "przed wpisem na listę radców prawnych obwiniony był funkcjonariuszem ABW",
    "przeprowadzenia oględzin.",
)
quote_wsd = excerpt(
    "SRC-02",
    46,
    "W ocenie WSD, OSD błędnie zinterpretował przepis art. 27 pkt 1 KERP",
    "nawet, gdy obwiniony nie wykonywał żadnych czynności obrończych i ostatecznie po rozmowie z prokuratorem odstąpił od świadczenia pomocy prawnej.",
)

result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-035",
    "label": "osoba pełniąca funkcję publiczną",
    "points": ["S1-K2-01"],
    "scope": (
        "Opracowano punkt S1-K2-01, z rozdzieleniem normy i ogólnego objaśnienia "
        "udziału w sprawie już ujętych w OBS-025-R01/R02. Nowe źródłowe uzupełnienie "
        "dotyczy wspólnego, niewyczerpującego katalogu ról autora oraz jednostkowego "
        "zastosowania art.27 pkt 1 przez WSD w sprawie byłego funkcjonariusza ABW. "
        "Autor nie rozdziela odrębnych testów dla przedstawiciela organu i osoby "
        "pełniącej funkcję publiczną. Wybór orzeczeń przedstawia osobno krytykowane "
        "stanowisko OSD i ocenę WSD. WO-52/24 omawia przede wszystkim art.26 i nie "
        "zostało użyte do wykładni pkt 1. Pytanie o wspólną granicę kategorii "
        "przedstawiciela organu i funkcji publicznej należy skoordynować z OBS-045; "
        "pytania o arbitra i biegłego "
        "(OBS-003-Q01, OBS-004-Q01) oraz mediatora (OBS-025-Q01) mają inny przedmiot. "
        "Oryginał WO-131/23 nie należy do manifestu. Zakres długich źródeł jest częściowy."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-025-R01", "OBS-025-R02"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "776; 812; 816; 820; 840", "notes": "W.816 (uwaga P0197) zawiera wspólny katalog przedstawicieli organów i osób pełniących funkcję publiczną; autor nie wyznacza oddzielnych testów. W.812 i 820 odczytano jako kontekst odebranej ogólnej wykładni udziału. W.840 dotyczy odpowiednika w KEA."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "44-50", "notes": "WO-131/23: rozdzielono opis faktów, przytoczone stanowisko OSD i ocenę WSD. WO-52/24 dotyczy głównie art.26: opisuje późniejsze sprawy przeciw organowi, w których radca nie występował wcześniej jako pracownik; nie są to te same sprawy. Nie wywodzę z tego ogólnego zwolnienia dawnych urzędników. Końcowe zdanie w.50 ma usterkę tekstową, pozostawioną bez korekty, i nie służy jako teza o art.27 pkt 1. Nie deklaruję pełnej lektury wyboru."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "758-760; 795-797", "notes": "Sprawdzono wyliczenie art.27 pkt 1 i ogólne ujęcie kategorii z art.27 pkt 1-2; nie stanowi ono odrębnego testu funkcji publicznej."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-175", "notes": "Sprawdzono brzmienie art.27 pkt 1, które wymienia przedstawiciela organu i osobę pełniącą funkcję publiczną. Norma jest już OBS-025-R01."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "wyszukanie trafień dla funkcji publicznej i art.27 pkt 1", "notes": "W sprawdzonych trafieniach brak odrębnego objaśnienia tej przesłanki; nie deklaruję pełnej lektury ustawy."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "102-104", "notes": "Tekst źródłowy powtarza wyliczenie art.27 pkt 1; brak dalszych kryteriów kategorii."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "77-87; 203-204", "notes": "Wtórne streszczenie WO-131/23 i WO-52/24; nie jest niezależnym potwierdzeniem orzeczeń. WO-52/24 streszczono przede wszystkim jako sprawę z art.26."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Krótki tekst przeczytany w całości; nie zawiera testu funkcji publicznej."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Krótki tekst przeczytany w całości; nie zawiera testu funkcji publicznej."},
    ],
    "meanings": [
        {
            "id": "OBS-035-M01",
            "context": "Kategoria przedstawiciela organu władzy publicznej lub osoby pełniącej funkcję publiczną w art.27 pkt 1",
            "description": "Autor komentarza wskazuje wspólny katalog obejmujący sędziów, ławników, referendarzy, asystentów sędziów, urzędników sądowych, komorników sądowych oraz urzędników państwowych i samorządowych. Zastrzega, że przepis nie precyzuje kategorii; słowo „itp.” nie zamyka katalogu. W komentarzu nie rozdzielono odrębnych kryteriów dla przedstawiciela organu i osoby pełniącej funkcję publiczną.",
            "record_ids": ["OBS-035-R01"],
        },
        {
            "id": "OBS-035-M02",
            "context": "Zastosowanie art.27 pkt 1 do wcześniejszej pracy funkcjonariusza ABW w tej samej sprawie, WO-131/23",
            "description": "W przytoczonym opisie sprawy wcześniejszy udział funkcjonariusza ABW obejmował przyjęcie zawiadomienia, protokołowanie przesłuchań, prowadzenie czynności i dostęp do materiałów. WSD odrzucił zreferowaną wykładnię OSD i w tej konfiguracji uznał za naruszenie art.27 pkt 1 podjęcie obrony osób zatrzymanych w tej sprawie, nawet bez późniejszych czynności obrończych i po odstąpieniu. Jest to zastosowanie jednostkowe, nie ogólna definicja funkcji publicznej.",
            "record_ids": ["OBS-035-R02"],
        },
    ],
    "records": [
        {
            "id": "OBS-035-R01",
            "kind": "poglad_autora",
            "claim": "W uwadze P0197 autor wskazuje wspólny, przykładowy katalog ról objętych określeniami przedstawiciela organu władzy publicznej lub osoby pełniącej funkcję publiczną, obejmujący m.in. sędziów, ławników, referendarzy, asystentów sędziów, urzędników sądowych, komorników oraz urzędników państwowych i samorządowych.",
            "speaker": "P. Skuczyński",
            "role": "autor komentarza, wypowiedź redakcyjna oznaczona P0197 w lustrze materiału do korekty autorskiej",
            "context": "Wykładnia zakresu dwóch pierwszych alternatywnych ról z art.27 pkt 1 KERP.",
            "court_treatment": "Nie jest wypowiedzią sądu ani normą; komentarz sam zaznacza brak precyzji przepisu i podaje przykłady.",
            "source_status": "Lustro DOCX komentarza z 24.09.2026; uwaga P0197 pozostaje materiałem redakcyjnym do oceny autorskiej.",
            "evidence": [{"source_id": "SRC-01", "line_start": 816, "line_end": 816, "quote": quote_public_roles}],
            "limits": "Autor łączy w jednym zdaniu przedstawiciela organu i osobę pełniącą funkcję publiczną, nie przypisuje poszczególnych przykładów osobno do każdej kategorii i nie formułuje zamkniętego katalogu ani kryterium dla innych ról. Nie jest to niezależne potwierdzenie normy.",
        },
        {
            "id": "OBS-035-R02",
            "kind": "zastosowanie_orzecznicze",
            "claim": "W przytoczonym fragmencie WO-131/23 WSD odrzucił stanowisko OSD i uznał, że w opisanej konfiguracji wcześniejszego udziału funkcjonariusza ABW w postępowaniu samo podjęcie obrony czterech zatrzymanych w tej samej sprawie narusza art.27 pkt 1, nawet gdy radca nie wykonał czynności obrończych i następnie odstąpił.",
            "speaker": "Wyższy Sąd Dyscyplinarny, w zakresie oceny wyraźnie przypisanej WSD w przytoczonym fragmencie",
            "role": "sąd dyscyplinarny odwoławczy, WO-131/23",
            "context": "Radca przed wpisem na listę był funkcjonariuszem ABW i wykonywał czynności w śledztwie; później podjął się obrony zatrzymanych w tej sprawie. Wyciąg odrębnie relacjonuje stanowisko OSD, które WSD następnie krytykuje.",
            "court_treatment": "Fragment źródła przytacza ocenę WSD, że OSD błędnie odczytał art.27 pkt 1; pogląd OSD o znaczeniu świadomości oraz zamiaru/gotowości/usiłowania jest przedstawiony jako pogląd odrzucony, nie stanowisko WSD.",
            "source_status": "Wybór fragmentów orzeczenia WSD w DOCX, linia 46; oryginalny tekst orzeczenia nie znajduje się w manifeście. SRC-07 zawiera wtórne streszczenie tej samej sprawy.",
            "evidence": [
                {"source_id": "SRC-02", "line_start": 44, "line_end": 44, "quote": quote_case_title},
                {"source_id": "SRC-02", "line_start": 46, "line_end": 46, "quote": quote_case_facts},
                {"source_id": "SRC-02", "line_start": 46, "line_end": 46, "quote": quote_wsd},
            ],
            "limits": "Jednostkowa konfiguracja WO-131/23, nie definicja wszystkich funkcji publicznych ani reguła, że sam status zatrudnienia publicznego wystarcza. WSD ocenia sprawę przy wcześniejszych czynnościach w tym samym postępowaniu; stanowisko OSD jest zreferowane jako odrębne i odrzucone. Nie wywodzę treści rozstrzygnięcia poza przytoczoną oceną. WO-52/24 dotyczy odrębnych spraw objętych przede wszystkim art.26 i nie ustanawia zwolnienia dla dawnych pracowników organu; wadliwe końcowe zdanie wyboru zachowano bez emendacji.",
        },
    ],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-035-G01",
            "issue": "Komentarz podaje przykłady i używa „itp.”, lecz sprawdzone źródła nie wyznaczają kryterium granicznego dla ról niewymienionych ani nie rozdzielają testu przedstawiciela organu od osoby pełniącej funkcję publiczną.",
            "needed": "Stanowisko eksperta co do kryterium kwalifikacji osób poza przykładami z uwagi P0197, przy osobnym badaniu rzeczywistego udziału w danej sprawie według OBS-025-R02.",
        },
        {
            "id": "OBS-035-G02",
            "issue": "Manifest zawiera wybór fragmentów WO-131/23 i wtórne streszczenie, a nie oryginalny tekst orzeczenia.",
            "needed": "Oryginał WO-131/23, jeżeli odbiór ma wymagać sprawdzenia pełnego uzasadnienia i końcowego rozstrzygnięcia poza cytowanym fragmentem.",
        },
    ],
    "questions": [
        {
            "id": "OBS-035-Q01",
            "record_ids": ["OBS-035-R01", "OBS-035-R02", "OBS-025-R02"],
            "understanding": "Autor przedstawia przykłady wspólnie dla przedstawicieli organów i osób pełniących funkcje publiczne, a WO-131/23 jest konkretnym zastosowaniem art.27 pkt 1 do byłego funkcjonariusza ABW, który wykonywał czynności w tej samej sprawie.",
            "variants": "Nieustalone pozostaje, czy wspólny katalog autora jest wyłącznie ilustracyjny, jak rozgraniczyć dwie wymienione kategorie oraz jakie kryterium obejmuje inne role; pojedynczy przykład ABW nie rozstrzyga tej granicy. Wcześniejsze uczestnictwo w konkretnej sprawie stanowi odrębny element oceniany według OBS-025-R02.",
            "consequences": "Kryterium pozwoli odróżnić osoby należące do kategorii funkcji publicznej od osób jedynie zatrudnionych w podmiocie publicznym, bez automatycznego przesądzania udziału w konkretnej sprawie.",
            "question": "Jak rozgraniczyć kategorie przedstawiciela organu władzy publicznej i osoby pełniącej funkcję publiczną w art.27 pkt 1? Czy wspólny katalog z uwagi P0197 jest otwarty i jakie kryterium obejmuje role niewymienione, przy zachowaniu osobnego wymogu wcześniejszego udziału w konkretnej sprawie?",
            "needed": "Wspólna wykładnia granic obu kategorii z art.27 pkt 1 do skoordynowania z OBS-045; odrębna od pytań o status arbitra, biegłego i mediatora oraz od ogólnego zakresu udziału.",
        }
    ],
    "self_check": (
        "Nowy rekord R01 zachowuje wspólne ujęcie dwóch kategorii i status uwagi redakcyjnej. "
        "Nowy rekord R02 jest wyłącznie zastosowaniem WO-131/23 i rozdziela stanowisko OSD "
        "od oceny WSD. WO-52/24 nie użyto do tezy art.27 pkt 1; usterki tekstu źródła nie "
        "korygowano. Długie źródła oznaczono jako częściowo sprawdzone; operator pozostaje OCZEKUJE."
    ),
}

validated = kolejka.validate_result(state, job, result)
out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "validation": "OK"}, ensure_ascii=True))
