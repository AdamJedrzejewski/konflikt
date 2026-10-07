import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
previous = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-068" / "a1e4715ff2634ea7ab75676dce01e3be" / "wynik.json"
source_result = json.loads(previous.read_text(encoding="utf-8"))

result = {
    "task_id": "862589d6abb246889565a39b7e2a67e1",
    "concept_id": "OBS-038",
    "label": "osoba, na rzecz której uprzednio wykonywano czynności zawodowe",
    "points": ["S2-K5-03", "S3-K6-06"],
    "scope": (
        "Mapuję oba punkty na odebrane już znaczenia OBS-068-M01 i OBS-068-M02, bez nowych tez. "
        "W S2-K5-03 chodzi o wiedzę o sprawach osoby, na rzecz której wcześniej wykonywano czynności zawodowe, "
        "jako odrębnej kategorii tekstu art. 26 ust. 1; nie ograniczam wcześniejszych czynności do reprezentacji "
        "ani wiedzy do informacji objętych tajemnicą. KL-R08 dotyczy szerokiego rozumienia wcześniejszych czynności "
        "w art. 28 ust. 3, a KL-R09 odnotowuje autorską równoważność tej formuły z określeniem byłego klienta; "
        "nie przenoszę ich ograniczeń na art. 26. OBS-007-R02 rozdziela czas ochrony tajemnicy od statusu klienta. "
        "Nie ustalam daty zakończenia relacji ani okresu odcięcia; wspólny problem końca relacji pozostaje w KL-G02 "
        "i OBS-002-Q01. W S3-K6-06 zachowuję szczególną konfigurację art. 26a ust. 2: ocenę wiedzy wyznaczonej osoby "
        "oraz warunki barier, bez założenia, że sama uprzednia obsługa innej osoby przesądza o wiedzy tej osoby lub "
        "że odseparowanie usuwa przewagę. Nie tworzę ponownych pytań: granice wykorzystania wiedzy, jej oceny oraz "
        "kręgu zgód pozostają w OBS-028-Q01/Q02/Q03 i OBS-076-Q02. Zakres jest częściowy wobec całego korpusu, "
        "a mapowanie punktów jest kompletne przez istniejące karty."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "KL-R04", "KL-R08", "KL-R09", "OBS-002-R06", "OBS-002-R07",
        "OBS-007-R01", "OBS-007-R02", "OBS-028-R01", "OBS-028-R03",
        "OBS-028-R04", "OBS-028-R05", "OBS-028-R06", "OBS-076-R04"
    ],
    "coverage": source_result["coverage"],
    "meanings": [
        {
            "id": "OBS-038-M01",
            "context": "S2-K5-03, art. 26 ust. 1 KERP, osoba wcześniej obsługiwana i wiedza o jej sprawach",
            "description": (
                "Punkt mapuje się na OBS-068-M01 i art. 26 ust. 1: kategoria obejmuje osobę, na rzecz której radca "
                "uprzednio wykonywał czynności zawodowe. Nie ograniczam tych czynności do reprezentacji ani tej wiedzy "
                "do tajemnicy zawodowej. KL-R08 objaśnia szeroki zakres czynności w odrębnym kontekście art. 28 ust. 3, "
                "a KL-R09 zapisuje stanowisko autora co do równoważności z terminem były klient; nie są one samodzielną "
                "definicją art. 26. OBS-007-R02 oddziela trwanie tajemnicy od statusu klienta. OBS-028-R01/R03/R04/R05 "
                "oraz OBS-002-R06/R07 zachowują element przewagi i ograniczenia przykładów. Nie wynika z nich ogólny "
                "termin ustania statusu, okres odcięcia ani automatyczny wyjątek, gdy nowy klient sam zna sprawę. "
                "Istniejące granice wykorzystania i oceny wiedzy pozostają w OBS-028-Q01/Q02/Q03; koniec relacji pozostaje "
                "w KL-G02 i OBS-002-Q01."
            ),
            "record_ids": [
                "OBS-028-R01", "OBS-028-R03", "OBS-028-R04", "OBS-028-R05",
                "OBS-002-R06", "OBS-002-R07", "OBS-007-R02", "KL-R08", "KL-R09"
            ]
        },
        {
            "id": "OBS-038-M02",
            "context": "S3-K6-06, art. 26a ust. 2 KERP, badanie wiedzy przy barierach informacyjnych",
            "description": (
                "Punkt mapuje się na OBS-068-M02 oraz OBS-028-R06 i OBS-076-R04. W konfiguracji wspólnego wykonywania "
                "zawodu należy odrębnie zbadać wiedzę osoby wyznaczonej do czynności i zachować warunki art. 26a ust. 2, "
                "w tym ochronę tajemnicy i brak nieuzasadnionej przewagi. Opis autora o osobie wyznaczonej i barierach "
                "nie tworzy ogólnej definicji osoby uprzednio obsługiwanej ani nie dowodzi, że wiedza innego prawnika "
                "jest wiedzą osoby wyznaczonej. Sama zgoda lub późniejsze odseparowanie nie zastępują sprawdzenia wiedzy. "
                "Ograniczenie dotyczące sytuacji art. 28 ust. 2 i pytanie o krąg zgód zachowuje OBS-076-R04/Q02."
            ),
            "record_ids": ["OBS-028-R06", "OBS-076-R04"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": (
        "Sprawdzono zakresy dotyczące art. 26 ust. 1 oraz art. 26a ust. 2 i ponownie wykorzystano faktycznie przeczytane "
        "coverage z OBS-068. Nie dodano nowych rekordów ani pytań, ponieważ oba punkty pokrywają już OBS-068-M01/M02 "
        "wraz z podanymi rekordami i otwartymi pytaniami. Nie utożsamiono czasu tajemnicy z czasem statusu klienta, "
        "nie założono okresu odcięcia ani uniwersalnego wyjątku opartego na wiedzy nowego klienta. Wynik pozostaje "
        "OCZEKUJE na odbiór Astry."
    )
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": len(result["records"]), "questions": len(result["questions"]), "sources": len(result["coverage"])}, ensure_ascii=False))
