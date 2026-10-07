import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-009" / "78503eaa7b904f7d99e655bc8b2817e4"
sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(ROOT / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-009")
attempt_id = job["attempts"][-1]["id"]

def lines(source_id):
    source = next(s for s in state["sources"] if s["id"] == source_id)
    return (ROOT / source["text"]).read_text(encoding="utf-8-sig").splitlines()

def quote(source_id, start, end):
    data = lines(source_id)
    return "\n".join(data[start - 1:end])

records = [
    {
        "id": "OBS-009-R01",
        "kind": "pogląd_autora",
        "claim": "W komentarzu do badania konfliktu interesów autor wskazuje, że KERP nie określa granicy czasowej badania obejmującego byłego klienta; wypowiedź dotyczy gromadzenia danych i badania konfliktu przed przyjęciem sprawy, nie temporalnego znaczenia art. 27 pkt 5.",
        "speaker": "autor opracowania SRC-03, P. Skuczyński według identyfikacji materiału projektowego",
        "role": "autor opracowania o rejestrze klientów i badaniu konfliktu interesów",
        "context": "Opis rutynowego gromadzenia danych aktualnych i byłych klientów na potrzeby badania konfliktu interesów przed rozpoczęciem pomocy prawnej.",
        "court_treatment": "nie dotyczy; to komentarz, nie wypowiedź sądu",
        "source_status": "Lokalny tekst opracowania w SRC-03. Nie jest to norma ani rozstrzygnięcie o art. 27 pkt 5; fragment nie podaje dodatniego testu ani czasu, po którym dawne bliskie stosunki przestają mieć znaczenie.",
        "evidence": [
            {"source_id": "SRC-03", "line_start": 383, "line_end": 392, "quote": quote("SRC-03", 383, 392)},
        ],
        "limits": "Wypowiedź dotyczy gromadzenia informacji i badania konfliktu przy relacji aktualny/były klient w kontekście rejestru. Nie można przenieść jej wprost na zwrot „był albo pozostaje w bliskich stosunkach” z art. 27 pkt 5. Nie ustanawia terminu zachowania ani wygaśnięcia dawnej relacji osobistej. SRC-03 i SRC-01 są materiałami tego samego autora i nie stanowią niezależnych opinii.",
    },
    {
        "id": "OBS-009-R02",
        "kind": "pogląd_autora",
        "claim": "W komentarzu roboczym autor przedstawia niepewność, czy obowiązek badania konfliktu między aktualnym i byłym klientem obejmuje także klientów obsługiwanych wcześniej niż okres przechowywania danych; przywołuje 10-letni okres danych zawodowych i skłania się ku ograniczeniu obowiązku badania do tego okresu.",
        "speaker": "P. Skuczyński, autor komentarza relacjonujący stanowisko z przywołanego opracowania (s. 254–255)",
        "role": "komentator przedstawiający argument i jego ograniczenie w kontekście rejestru danych",
        "context": "Art. 5c URP oraz obowiązek badania konfliktu w konfiguracji między aktualnym i byłym klientem; autor wyraźnie zaznacza niejasność co do klientów obsługiwanych wcześniej.",
        "court_treatment": "nie dotyczy; jest to argument autora, nie pogląd sądu",
        "source_status": "Nowe lustro komentarza oznaczonego do korekty autorskiej. Cytowany rozdział z 2022 r. nie znajduje się w manifeście; nie weryfikowano jego oryginału ani aktualności przytoczonego tekstu art. 5c URP.",
        "evidence": [
            {"source_id": "SRC-01", "line_start": 1464, "line_end": 1464, "quote": quote("SRC-01", 1464, 1464)},
        ],
        "limits": "Wypowiedź dotyczy obowiązku sprawdzania konfliktu w relacji aktualny/były klient i retencji danych osobowych, nie art. 27 pkt 5 ani trwania osobistych stosunków. Sam autor zaznacza, że kwestia starszych klientów nie jest do końca jasna. Wniosek o ograniczeniu badania jest jego stanowiskiem, a nie zweryfikowaną regułą, że dawna relacja osobista wygasa po 10 latach.",
    },
]

result = {
    "task_id": attempt_id,
    "concept_id": "OBS-009",
    "label": "dawna i aktualna relacja",
    "points": ["S1-K2-05"],
    "scope": "S1-K2-05 odpowiada art. 27 pkt 5 KERP: tekst mówi „był albo pozostaje w bliskich stosunkach” z przeciwnikiem klienta lub osobą zainteresowaną niekorzystnym rozstrzygnięciem (OBS-043-R01). Zachowuję obie alternatywy czasowe, ale nie wywodzę z samego „był” konkretnego terminu, automatycznej liczby lat ani skutku samego zerwania kontaktu. OBS-005-Q01 pyta o pozytywne cechy i intensywność bliskich stosunków, nie o ich temporalną granicę; nie powielam go. Źródła o badaniu konfliktu z udziałem byłych klientów dotyczą innej konfiguracji: SRC-03 stwierdza brak granicy czasowej w KERP dla badania, a SRC-01 omawia odrębnie możliwe ograniczenie tego badania okresem retencji danych i przyznaje niepewność co do starszych byłych klientów. Nie przenoszę tych stanowisk na art. 27 pkt 5. Karta jest częściowa, bo materiał nie określa, jak długo utrzymuje się znaczenie relacji już zakończonej w tej przesłance.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-043-R01", "OBS-005-R01"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "828; 848-860; 1458-1472", "notes": "W. 828 to pogląd autora o bliskoznaczności, nie kryterium temporalne. W. 848-860 zawiera wtórny opis D 43/2016 i D 33/18, bez wyznaczenia okresu. W. 1458-1472: kontekst rejestru, retencji danych i badania konfliktu; w. 1464 omawia tylko relację aktualny/były klient i wyraża niepewność co do starszych klientów."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "86-89", "notes": "WO-25/24 w wyborze orzeczeń opisuje wcześniejszą obsługę wspólników i późniejszą reprezentację jednego z nich w sprawie rozwodowej; rozstrzygnięcie jest przedstawione jako art. 26/28, nie art. 27 pkt 5 i nie podaje ogólnego okresu dla bliskich stosunków."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "372-392; 450-475; 520-535", "notes": "Przeczytano kontekst obowiązku badania przed pomocą, zbierania danych o obecnych/byłych klientach, dat końca obsługi oraz przechowywania danych. W. 389-390 mówi o braku granicy dla badania konfliktu z byłym klientem; w. 530-535 dotyczy retencji danych. Nie jest to wypowiedź o temporalnym zakresie art. 27 pkt 5."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "183", "notes": "Lokalny art. 27 pkt 5 literalnie obejmuje relacje, które „był albo pozostaje”; tekst nie podaje długości okresu ani reguły ustania skutku."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "67-82", "notes": "Sprawdzono lokalny tekst art. 5c URP o okresach przechowywania danych; w zakresie zawodowego przetwarzania wymienia 10 lat. To kontekst cytowany w SRC-01, nie podstawa do określenia terminu dla art. 27 pkt 5; aktualności tekstu nie weryfikowano."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "111", "notes": "Wtórne zestawienie przepisów powtarza brzmienie art. 27 pkt 5, bez objaśnienia granicy czasowej."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "143-148", "notes": "Wtórne streszczenie WO-25/24 podkreśla ochronę zaufania po ustaniu współpracy klienta z radcą; dotyczy art. 26/28, nie ustala czasu trwania relacji z art. 27 pkt 5."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały krótki glosariusz sprawy tej samej i związanej; nie określa trwania relacji osobistej."},
        {"source_id": "SRC-09", "status": "CZESCIOWY", "read_ranges": "9-20", "notes": "Odczytano fragment o byłych klientach i skutkach po ustaniu współpracy w sprawach WO-82/20 i WO-25/24; dotyczy statusu klienta i art. 28/29, a nie dawnej relacji osobistej z art. 27 pkt 5."}
    ],
    "meanings": [
        {
            "id": "OBS-009-M01",
            "context": "S1-K2-05, art. 27 pkt 5 KERP: czasowy aspekt bliskich stosunków z przeciwnikiem klienta lub osobą zainteresowaną niekorzystnym rozstrzygnięciem",
            "description": "Norma wymienia relacje, które były albo pozostają aktualne (OBS-043-R01), ale nie wskazuje okresu ani dodatkowej granicy dla relacji zakończonej. Nie utożsamiam tego z ustaniem statusu byłego klienta. Komentarz o braku granicy przy badaniu byłych klientów oraz odrębna wypowiedź o retencji danych (OBS-009-R01/R02) nie przesądzają znaczenia tej przesłanki. OBS-005-Q01 pozostaje pytaniem o cechy bliskości; to odrębna kwestia od czasu, jaki upłynął po ustaniu relacji.",
            "record_ids": ["OBS-043-R01", "OBS-009-R01", "OBS-009-R02"]
        }
    ],
    "records": records,
    "relations": [],
    "gaps": [
        {"id": "OBS-009-G01", "issue": "Przejrzane źródła nie wyznaczają temporalnej granicy zastosowania alternatywy „był” w art. 27 pkt 5 po ustaniu bliskich stosunków. Wypowiedzi o kontroli byłych klientów są odrębne i pozostają w napięciu: SRC-03 mówi o braku granicy w KERP dla badania konfliktu z byłym klientem, a SRC-01 omawia możliwe ograniczenie badania retencją danych, z jawną niepewnością dotyczącą klientów starszych.", "needed": "Interpretacja ekspercka temporalnego zakresu „był” w art. 27 pkt 5, oddzielona od testu bliskości z OBS-005-Q01 i od zasad badania/retencji w relacji były klient."}
    ],
    "questions": [
        {
            "id": "OBS-009-Q01",
            "record_ids": ["OBS-043-R01", "OBS-009-R01", "OBS-009-R02"],
            "understanding": "Art. 27 pkt 5 obejmuje zarówno bliskie stosunki aktualne, jak i takie, które były. Materiał nie mówi, jak oceniać dawną relację po jej ustaniu ani czy upływ czasu sam przez się zmienia jej znaczenie. OBS-005-Q01 dotyczy tego, jakie cechy czynią relację bliską, a nie jej temporalnej granicy. Komentarze o byłych klientach odnoszą się do badania konfliktu i przechowywania danych, nie bezpośrednio do art. 27 pkt 5.",
            "variants": "Możliwe jest odczytanie, że uprzednie istnienie kwalifikowanych bliskich stosunków mieści się wprost w słowie „był”, bez dodatkowego okresu. Możliwe jest też, że znaczenie dawnej relacji zależy od jej czasowego lub funkcjonalnego związku z aktualną sprawą lub interesem; dostępne źródła nie formułują takiego kryterium. Nie zakładam konkretnej liczby lat ani nie przenoszę 10-letniej retencji danych na art. 27 pkt 5.",
            "consequences": "Rozstrzygnięcie określi, czy fakt zakończenia relacji i czas, który od niego upłynął, mają samodzielne znaczenie dla zastosowania art. 27 pkt 5, niezależnie od ustalenia, czy relacja pierwotnie była bliska. Pozwoli też zachować odrębność od reguł dotyczących byłych klientów.",
            "question": "Jak należy rozumieć słowo „był” w art. 27 pkt 5 po ustaniu bliskich stosunków: czy wystarcza wcześniejsze istnienie relacji kwalifikowanej jako bliska niezależnie od czasu, jaki upłynął, czy też wymagany jest jej czasowy lub funkcjonalny związek z aktualną sprawą albo interesem? Czy wypowiedzi o badaniu konfliktu z udziałem byłych klientów i retencji danych mają tu jakiekolwiek znaczenie, czy pozostają odrębnym kontekstem?",
            "needed": "Odpowiedź eksperta dotycząca czasowego zakresu art. 27 pkt 5. Nie należy zastępować jej testem intensywności relacji z OBS-005-Q01 ani terminem przechowywania danych z art. 5c URP."
        }
    ],
    "self_check": "Zapisuję wyłącznie wynik i helper w katalogu zadania. Dosłowne cytaty nowych rekordów zostały pobrane programowo z dokładnie wskazanych wierszy SRC-03 i SRC-01. Oddzieliłem art. 27 pkt 5 od autorowych wypowiedzi o byłych klientach, badaniu konfliktu i przechowywaniu danych; nie przenoszę 10 lat jako terminu dla bliskich stosunków. Nie powielam OBS-005-Q01 o pozytywnych cechach relacji. Zakres dziewięciu źródeł jest jawnie ograniczony w coverage; nie weryfikowałem oryginałów cytowanych opracowań ani aktualności prawa. To samokontrola wykonawcy, nie odbiór Astry."
}

out = TASK / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
kolejka.validate_result(state, job, result)
print(json.dumps({"validated": True, "path": str(out), "records": len(records), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "attempt_id": attempt_id}, ensure_ascii=False))
