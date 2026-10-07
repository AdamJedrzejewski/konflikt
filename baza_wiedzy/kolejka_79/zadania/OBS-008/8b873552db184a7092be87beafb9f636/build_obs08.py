import json
from pathlib import Path

TASK = Path(__file__).parent
OBSIL = TASK.parents[4]
job = json.loads((TASK / "zlecenie.json").read_text(encoding="utf-8"))
sources = {s["id"]: (OBSIL / s["text"]).read_text(encoding="utf-8").splitlines() for s in job["sources"]}

def ev(source_id, start, end):
    return {"source_id": source_id, "line_start": start, "line_end": end,
            "quote": "\n".join(sources[source_id][start-1:end])}

result = {
  "task_id": job["task_id"], "concept_id": "OBS-008", "label": "czynności zawodowe",
  "points": job["points"],
  "scope": "Zakres obejmuje cztery punkty: S1-K2-04 oraz S2-K5-00, S2-K5-01 i S2-K5-02. Jedyny nowy zapis dotyczy szczególnej przesłanki art. 27 pkt 4 KERP, w której tekst łączy sprawę dotyczącą radcy lub osoby wspólnie wykonującej zawód, czynności zawodowe, ten sam czas i tego samego klienta. Nie tworzę ogólnej definicji czynności zawodowych. Dla art. 26 i tajemnicy wykorzystuję OBS-028-R01/R02/R03, OBS-007-R02 oraz OBS-040-R01/R02; art. 25 i granica wobec innych aktywności są już ujęte w OBS-040. ON-R07 odrębnie obejmuje węższe rozumienie udziału w rozstrzygnięciu z art. 27 pkt 3 wobec udziału w sprawie z pkt 1, nie przenoszę tej wykładni na pkt 4. Art. 15 KERP o tajemnicy i art. 15 u.r.p. o wyłączeniu to różne konteksty; ustawa art. 16 w badanym tekście dotyczy oceny pracy zawodowej. Karta jest częściowa, ponieważ dostępne źródła nie dają odrębnego testu dla zwrotu z art. 27 pkt 4. Oryginałów orzeczeń nie zastępują wtórne zestawienia.",
  "completeness": "partial", "operator_status": "OCZEKUJE",
  "existing_record_refs": ["OBS-028-R01", "OBS-028-R02", "OBS-028-R03", "OBS-007-R02", "OBS-040-R01", "OBS-040-R02", "ON-R03", "ON-R07", "KL-R08"],
  "coverage": [
    {"source_id":"SRC-01","status":"CZESCIOWY","read_ranges":"48-116; 396-468; 772-832","notes":"Nowe lustro komentarza. Czytano pełne bloki art. 25, art. 26 i art. 27 z otoczeniem; zachowano widoczne markery redakcyjne. P0198 dotyczy udziału w sprawie z pkt 1, a P0201 udziału w rozstrzygnięciu z pkt 3; nie przeniesiono ich automatycznie na pkt 4."},
    {"source_id":"SRC-02","status":"CZESCIOWY","read_ranges":"36-40; 60-64","notes":"Wtórne fragmenty o zeznaniu w sprawie, równoległej pomocy i uprzedniej obsłudze. Brak relewantnego omówienia art. 27 pkt 4 w sprawdzonych miejscach; nie użyto jako podstawy nowej tezy."},
    {"source_id":"SRC-03","status":"CZESCIOWY","read_ranges":"145-180; 950-1010; 1350-1395","notes":"Poradnik: granica zajęć z art. 25, przesłanki ogólne art. 26, reprezentacja/doradztwo i przypisanie konfliktu. Fragmenty z markerami '???' pozostawiono poza cytatami dowodowymi."},
    {"source_id":"SRC-04","status":"CZESCIOWY","read_ranges":"65-81; 111-121; 143-185","notes":"Lokalny tekst KERP: niezależność, tajemnica, art. 25-27. Nowy rekord opiera się na art. 27 pkt 4. Art. 15-16 KERP dotyczą tu tajemnicy, nie wyłączenia z art. 15 u.r.p."},
    {"source_id":"SRC-05","status":"CZESCIOWY","read_ranges":"157-167","notes":"Lokalny tekst u.r.p. art. 13-16; art. 15 reguluje wyłączenie w wymienionych sytuacjach, a art. 16 ocenę pracy. Nie utożsamiono ich z art. 15-16 KERP."},
    {"source_id":"SRC-06","status":"CZESCIOWY","read_ranges":"25-60; 292-323","notes":"Wtórne zestawienie definicji, zasad i mapy przepisów. Potwierdza lokalizację kontekstów art. 25-27, lecz nie stanowi samodzielnej podstawy nowej tezy."},
    {"source_id":"SRC-07","status":"CZESCIOWY","read_ranges":"35-58; 80-96; 175-190","notes":"Wtórne zestawienie orzeczeń o art. 26 i udziale radcy w sprawie przed wykonywaniem zawodu. Oryginałów nie ma w tym materiale; nie użyto do rozstrzygnięcia zakresu art. 27 pkt 4."},
    {"source_id":"SRC-08","status":"SPRAWDZONY","read_ranges":"1-35","notes":"Cała karta sprawy tej samej lub związanej; brak nowego znaczenia dla czynności zawodowych."},
    {"source_id":"SRC-09","status":"SPRAWDZONY","read_ranges":"1-37","notes":"Cała karta klienta aktualnego i byłego; wykorzystano istniejący kontekst, bez powielania definicji klienta lub zakończenia relacji."}
  ],
  "meanings": [
    {"id":"OBS-008-M01","context":"Czynności zawodowe jako warunek art. 27 pkt 4 KERP przy wspólnym wykonywaniu zawodu","description":"Lokalny tekst KERP wiąże zakaz udzielenia pomocy prawnej ze sprawą dotyczącą radcy prawnego, adwokata lub innej osoby, z którą może on wspólnie wykonywać zawód, jeżeli wykonują czynności zawodowe w tym samym czasie na rzecz tego samego klienta. Zachowuję wszystkie warunki przepisu i nie rozszerzam ich przez analogię do udziału w sprawie z art. 27 pkt 1 ani udziału w rozstrzygnięciu z pkt 3.","record_ids":["OBS-008-R01"]},
    {"id":"OBS-008-M02","context":"Czynności zawodowe w przesłankach ogólnych art. 26 KERP","description":"Dla przesłanek tajemnicy, niezależności i wiedzy dającej nieuzasadnioną przewagę odsyłam do istniejących zapisów OBS-028-R01/R02/R03 i OBS-007-R02; pojęcie pomocy prawnej oraz oddzielenie innych aktywności pokrywa OBS-040-R01/R02. Nie tworzę równoległej definicji.","record_ids":["OBS-028-R01","OBS-028-R02","OBS-028-R03","OBS-007-R02","OBS-040-R01","OBS-040-R02"]}
  ],
  "records": [
    {"id":"OBS-008-R01","kind":"NORMA","claim":"Art. 27 pkt 4 KERP zakazuje udzielenia pomocy prawnej, gdy sprawa dotyczy radcy prawnego, adwokata lub innej osoby, z którą radca może wspólnie wykonywać zawód, o ile wykonują czynności zawodowe w tym samym czasie na rzecz tego samego klienta.","speaker":"Normodawca samorządowy, lokalny tekst KERP","role":"przepis art. 27 pkt 4","context":"S1-K2-04: sprawa dotycząca osoby mogącej wspólnie wykonywać zawód; warunki jednoczesności czynności zawodowych i tego samego klienta.","court_treatment":"Nie dotyczy.","source_status":"lokalny tekst KERP z manifestu; bez zewnętrznej kontroli aktualności","evidence":[ev("SRC-04",181,181)],"limits":"Teza zachowuje wszystkie kwalifikatory przepisu. Źródła nie objaśniają odrębnie granic zwrotu 'czynności zawodowe' w pkt 4 ani nie uprawniają do przeniesienia autorskiej wykładni udziału w sprawie z pkt 1 lub udziału w rozstrzygnięciu z pkt 3."}
  ],
  "relations": [],
  "gaps": [
    {"id":"OBS-008-G01","issue":"Nie odnaleziono w sprawdzonych źródłach odrębnego testu dla zakresu 'czynności zawodowych' w art. 27 pkt 4 ani rozwinięcia, jak stosować warunki tego samego czasu i tego samego klienta do konkretnych konfiguracji wspólnego wykonywania zawodu.","needed":"Jeżeli OBSIL ma oceniać graniczne przypadki art. 27 pkt 4, potrzebne jest stanowisko eksperta o zakresie tych warunków; nie należy uzupełniać go przez analogię do art. 27 pkt 1 lub pkt 3."},
    {"id":"OBS-008-G02","issue":"Wybór orzeczeń i karta orzecznicza są opracowaniami wtórnymi, a pełne uzasadnienia nie są wskazane w lokalnym manifeście.","needed":"Pełne oryginały tylko wtedy, gdy dalsze opracowanie ma opierać się na konkretnym sądowym zastosowaniu pojęcia czynności zawodowych."}
  ],
  "questions": [
    {"id":"OBS-008-Q01","record_ids":["OBS-008-R01","OBS-040-R01","OBS-040-R02"],"understanding":"Literalna przesłanka z art. 27 pkt 4 wymaga równoczesnych czynności zawodowych na rzecz tego samego klienta przez radcę i osobę, z którą może on wspólnie wykonywać zawód. Art. 4 i 6 u.r.p. wskazują zakres pomocy prawnej, a komentarz do art. 25 odróżnia ją od aktywności bezpośrednio związanej lub podporządkowanej świadczeniu głównemu; brak materiału stosującego to rozróżnienie do pkt 4.","variants":"Wariant A: dla pkt 4 badać wyłącznie świadczenie pomocy prawnej w ramach czynności zawodowych. Wariant B: uwzględniać także czynności bezpośrednio związane lub podporządkowane świadczeniu pomocy prawnej jako głównemu. Wariant C: zakres zależy od okoliczności sprawy i rodzaju wspólnej aktywności; dostępny materiał nie daje reguły abstrakcyjnej.","consequences":"A zawęża zastosowanie przesłanki do wspólnego wykonywania pomocy prawnej; B może objąć czynności towarzyszące świadczeniu głównemu; C wymaga każdorazowego opisania konkretnych czynności i relacji z klientem bez automatycznego wniosku z samej formy współpracy.","question":"Czy na potrzeby art. 27 pkt 4 KERP pojęcie wykonywania czynności zawodowych obejmuje tylko czynności świadczenia pomocy prawnej, czy również czynności bezpośrednio związane lub podporządkowane jej jako świadczeniu głównemu, i jakie znaczenie mają w tym badaniu wymogi tego samego czasu i tego samego klienta?","needed":"Wykładnia ekspercka art. 27 pkt 4 w powiązaniu z art. 4 i 6 u.r.p. oraz art. 25 ust. 2-3 KERP, bez przenoszenia wykładni innych punktów art. 27."}
  ],
  "self_check":"Częściowy zakres obejmuje cztery punkty zlecenia. Cytat nowego rekordu pobrano programowo z dokładnego wiersza lokalnego KERP. Treść art. 27 pkt 4 oddzielono od komentarzowej wykładni art. 27 pkt 1 i pkt 3 oraz od art. 26, dla którego wskazano przyjęte zapisy. Zachowano różnicę między art. 15-16 KERP a art. 15-16 u.r.p. i nie wyprowadzano stanowiska sądu z wtórnego zestawienia. Brakuje źródłowego testu interpretacyjnego dla zwrotu art. 27 pkt 4; status OCZEKUJE, do odbioru Astry."
}

(TASK / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
