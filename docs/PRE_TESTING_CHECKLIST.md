# Lista prac przed oficjalnymi testami OBSIL

> Sporządzono: 2026-05-05 wieczór
> Kontekst: pipeline 2.0 (sekwencyjna ewaluacja artykułów KERP) zaimplementowany i przeszedł 3 scenariusze e2e. Przed udostępnieniem narzędzia radcom prawnym do testów funkcjonalnych pozostają luki opisane poniżej.

Priorytety:
- **P0** — blokujące, bez tego testy nie mają sensu (radca nie zobaczy wyniku)
- **P1** — mocno zniekształcają wynik testów (fałszywe niskie confidence, brak regresji)
- **P2** — jakościowe, można robić równolegle z testami

---

## P0 — Blokery

### 1. Frontend nie wyświetla nowego formatu `final_result`

**Lokalizacja:** `frontend/types/analysis.ts`, `frontend/app/analyze/[id]/result/page.tsx`

**Problem:** Frontend nadal używa modelu z dual-analysis (poprzedni pipeline):
- `frontend/types/analysis.ts:1-5` — `ConflictClassification` ma polskie wartości (`"brak_konfliktu" | "potencjalny_konflikt" | "wysoki_poziom_ryzyka" | "konflikt_oczywisty"`), backend zwraca angielskie (`"NO_CONFLICT" | "CONFLICT_WAIVABLE" | "CONFLICT"`). `ConflictBadge` prawdopodobnie nie matchuje i pokazuje fallback.
- `result/page.tsx:94-97` renderuje `RiskCard` dla pól `confidential_information_risk`, `adversity_risk`, `successive_representation_risk`, `organizational_barriers` — **żadne z tych pól nie jest już zwracane** przez orchestrator (zniknęły wraz z dual-analysis).
- Brak renderowania kluczowych nowych pól: `article_evaluations` (lista 9 ocen z uzasadnieniem per artykuł), `discrepancies` (rozbieżności rule_engine vs LLM).

**Rekomendacja:**
1. Zaktualizować `types/analysis.ts` — dodać `ArticleEvaluation`, `Discrepancy`, dopasować enum klasyfikacji do backendu.
2. Stworzyć komponent `<ArticleEvaluationList>` — rozwijana lista per artykuł: status (applies/nie applies), pewność, matched/unmatched premises, uzasadnienie.
3. Stworzyć `<DiscrepancyBanner>` — żółta plansza gdy `discrepancies.length > 0`, z wyjaśnieniem co to oznacza.
4. Usunąć stare `RiskCard` lub przemapować na nowe pola, jeśli mają sens.
5. Zweryfikować mapping `ConflictBadge` na nowy enum.

**Estymacja:** 3-4h frontend

---

### 2. Brak harness'u do testów regresji mimo gotowego datasetu

**Lokalizacja:** `tests/cases/TC-001.json` ... `TC-020.json` (20 plików)

**Problem:** Istnieje 20 starannie przygotowanych golden test cases (każdy z `fact_pattern`, `expected_result`, `triggered_rules`, `legal_analysis`, `key_factors`). Format gotowy do automatyzacji. Ale brak skryptu który by je przepuścił przez API i porównał wyniki. Każda zmiana w prompcie / regułach może po cichu zepsuć któryś przypadek.

**Rekomendacja:** Stworzyć `scripts/run_test_cases.py`:
1. Iteracja po `tests/cases/*.json`
2. POST do lokalnego API, polling do `complete`
3. Porównanie:
   - `final_result.conflict_classification` vs `TC.expected_result`
   - `final_result.legal_basis` vs `TC.triggered_rules` (mapowanie article→rule_id)
4. Output: tabela pass/fail + JSON raport do `tests/reports/`
5. Exit code != 0 jeśli regresja (wpinalne do CI)

**Estymacja:** 2-3h backend

**Bonus:** dorobić `pytest` integration test dla orchestratora z mock LLM (mocki na `evaluate_article` zwracające stałe odpowiedzi), żeby nie wołać prawdziwego Gemini przy każdym uruchomieniu.

---

### 3. Brak backupów bazy danych

**Lokalizacja:** `infra/docker/docker-compose.yml`, hosting

**Problem:** `/home/adam/apps/backups/` nie istnieje. PostgreSQL `obsil-db` nie ma żadnego cron-backupu. W razie awarii VPS lub bug'u w migracji — stracimy wszystkie audyty (a one mają wartość prawną).

**Rekomendacja:**
1. Cron systemd timer `obsil-db-backup.timer` (codziennie 03:00):
   ```bash
   docker exec obsil-db pg_dump -U obsil obsil | gzip > /home/adam/apps/backups/obsil-$(date +%F).sql.gz
   find /home/adam/apps/backups -name "obsil-*.sql.gz" -mtime +30 -delete
   ```
2. Test restore na czystej bazie (manualnie raz, udokumentować procedurę).
3. Rozważyć off-VPS storage (np. rsync na Backblaze B2 / DO Spaces).

**Estymacja:** 1-2h ops

---

## P1 — Mocno zniekształca wyniki testów

### 4. Rule engine guardrails dają systematyczne false-positive

**Lokalizacja:** `backend/app/rules/engine.py:124-188` (keyword classification)

**Problem:** Każdy z 3 testowych scenariuszy ma `discrepancies > 0` mimo że klasyfikacja końcowa jest poprawna:
- S1 (klient=przeciwnik) — rule_engine flagował coś czego LLM słusznie nie potwierdził
- S2 (czysty case) — rule_engine flagował art. 28 ust. 2 dla niewinnej umowy z kontrahentem
- S3 (mediator) — rule_engine flagował dodatkowe artykuły poza art. 27

Skutek: każda analiza dostaje obniżoną pewność do "umiarkowany". Radca w testach zobaczy "system jest niepewny" nawet gdy wszystko gra.

**Diagnoza** (`engine.py:130`):
- Słowo "doradca" → tag `pelnomocnik_obronca`
- Słowo "kontrahent" / "umowa handlowa" → potencjalnie `strona_przeciwna` przez `_classify_entity` patrzące w opis

**Rekomendacja:**
1. Zawęzić keywordy do jednoznacznych (np. `pelnomocnik` ale nie `doradca` w `pelnomocnik_obronca`).
2. Dodać kontekst: tag aktywuje się tylko gdy entity ma rolę zgodną z tagiem (cross-check entity tag × role tag).
3. Wprowadzić poziom pewności guardrails (`high`/`low`) i pokazywać discrepancy tylko gdy obie strony są pewne.
4. Alternatywa: usunąć comparator "rule_engine_flagged_llm_disagreed" z discrepancies (zostawić tylko odwrotny kierunek, bo on jest faktycznie podejrzany — LLM widzi coś czego reguły nie znają).

**Estymacja:** 3-5h backend + iteracja na 20 test cases

---

### 5. Agregacja confidence — "słabe ogniwo" zbyt restrykcyjne

**Lokalizacja:** `backend/app/services/orchestrator.py:_aggregate_confidence`

**Problem:** Obecna logika: minimum z confidence wszystkich evaluowanych artykułów → mapping na `wysoki/umiarkowany/niski`. Skutek: NO_CONFLICT z 8/9 artykułów ocenianych "wysoka" i 1 "niska" daje `confidence_level: niski`. To prawnicy odbiorą jako "system nie wie" — mylące.

**Rekomendacja:**
1. Dla `NO_CONFLICT` agregować tylko po artykułach RELEVANTNYCH dla `matter_type` (nie ma sensu rozważać art. 26a kancelaryjnego dla solo radcy).
2. Albo: dla `NO_CONFLICT` używać większościowego głosu (≥75% wysoka → `wysoki`).
3. Dla `CONFLICT` brać confidence z artykułu który zaaplikował (decydujący) — to robi sens, ale obecna logika tego nie pokazuje wprost.
4. Dodać do final_result `confidence_breakdown` per kategoria (kluczowe vs poboczne).

**Estymacja:** 2h backend

---

### 6. Walidacja sanity LLM output

**Lokalizacja:** `backend/app/services/orchestrator.py:_evaluate_articles_sequentially`

**Problem:** Jeśli LLM zwróci `applies=true` ale `matched_premises=[]` — orchestrator zaakceptuje. Jeśli `applies=false` ale wszystkie premises matched — też. Brak sanity check.

**Rekomendacja:** Po `await self.llm.evaluate_article(...)`:
```python
if evaluation.get("applies") and not evaluation.get("matched_premises"):
    logger.warning("LLM applies=true bez matched_premises dla %s", article_id)
    evaluation["confidence"] = "niska"
    evaluation["_sanity_warning"] = "applies=true bez wskazanych przeslanek"
```
Plus odwrotny kierunek (premises_logic=AND_ALL & wszystkie matched & applies=false → flag).

**Estymacja:** 1h backend

---

### 7. Brak retry na LLM timeout / 5xx

**Lokalizacja:** `backend/app/adapters/llm_adapter.py:_call`

**Problem:** Retry istnieje TYLKO na błąd parsowania JSON / walidacji schemy. Jeśli Gemini API zwróci 503 / timeout — wyjątek przepada do orchestratora i analiza idzie w `error`. Sekwencyjna ewaluacja oznacza 9-10 wywołań LLM — szansa że któreś padnie jest realna.

**Rekomendacja:**
1. Dodać retry z exponential backoff dla `httpx.HTTPStatusError`, `asyncio.TimeoutError`, `genai.errors.ServerError`.
2. W orchestratorze: jeśli pojedynczy artykuł padł → kontynuuj resztę, oznacz ten artykuł jako `_error`, NIE przerywaj całej analizy. (Częściowo już zrobione w `_evaluate_articles_sequentially`, ale pokrywa tylko bardzo szeroki `Exception` — sprawdzić że łapie też transport-level błędy.)

**Estymacja:** 2h backend

---

## P2 — Jakościowe, można równolegle z testami

### 8. Rozszerzenie datasetu testowego

20 case'ów to dobry start, ale przejrzyj pokrycie:
- Czy są przypadki **art. 26a** (kancelaria, chinese wall)?
- Czy są przypadki **art. 30** z osobą najbliższą?
- Czy są **negatywne** przypadki (NO_CONFLICT z trickiem)?
- Czy są **CONFLICT_WAIVABLE** (art. 29 ust. 1 pkt 1/2 — doradztwo, zgoda)?
- Czy są scenariusze pełne **niejasności** (oczekiwane clarifying_questions)?

Cel: ~30-40 case'ów pokrywających każdą `configuration` w katalogu.

**Estymacja:** 1 dzień pracy z prawnikiem

### 9. Performance — równoległość niezależnych artykułów

Obecnie 9 artykułów × ~7-10s = 60-90s dla NO_CONFLICT. Artykuły są od siebie niezależne (oprócz early-stop). Można puścić je w `asyncio.gather` w batchach (np. 3 równolegle). To skróci NO_CONFLICT do ~30s.

Trade-off: tracimy early-stop (bo wszystkie uruchamiają się równolegle). Rozważyć hybrid: pierwsze 3 artykuły (KERP-30, KERP-27, KERP-28-2 — najczęstsze CONFLICT'y) sekwencyjnie z early-stop, reszta równolegle.

**Estymacja:** 2-3h backend + benchmark

### 10. Monitoring produkcji

- Health endpoint istnieje (`/health`), ale brak metryk (`/metrics`).
- Brak alertów na "analysis_error" w audit_log.
- Brak track'owania kosztu LLM (Gemini API calls / dzień).

**Rekomendacja minimum:**
- Cronjob który raz dziennie tweetuje liczbę errorów z ostatnich 24h do Slack/email.
- Dashboard w Grafanie? Albo prostszy: weekly summary script.

**Estymacja:** 4-6h ops

### 11. PII / dane wrażliwe

`fact_pattern_raw` zawiera dane osobowe klientów (imiona, sygnatury, opisy spraw). W bazie trzymane plain text.

**Pytania do prawnika RODO:**
- Czy potrzebujemy szyfrowania at-rest? (kolumna encrypted, klucz w KMS)
- Czy potrzebujemy retention policy (np. usuwanie po 90 dniach)?
- Czy log Gemini API zawiera prompt → trafia do Google? (sprawdzić politykę Vertex/AI Studio)
- Czy radca wie że jego stan faktyczny idzie do Google? (information notice + checkbox)

**Estymacja:** wymaga decyzji prawnej, nie estymujemy implementacji

### 12. Sanity disclaimers w UI

Strona wyniku powinna jasno komunikować:
- "To narzędzie wspomagające — nie zastępuje samodzielnej oceny radcy"
- "W razie wątpliwości skonsultuj z dziekanem OIRP"
- "Wynik oparty na art. 26-30a KERP, nie analizuje innych podstaw konfliktu"
- "Dane zostały przetworzone przez model AI Google Gemini" (jeśli RODO tego wymaga)

**Estymacja:** 1h frontend + treść od prawnika

### 13. Cleanup deprecated kodu

`backend/app/adapters/prompts/schematic_*.{txt,json}` i `independent_*.{txt,json}` — niewywoływane od pipeline 2.0. Można usunąć (oraz powiązane metody `evaluate_schematic` / `evaluate_independent` z LLMAdapter, jeśli nigdzie nie używane).

`backend/app/services/comparator.py` — sprawdzić czy nadal używane (orchestrator nie importuje).

**Estymacja:** 1h cleanup + git commit

### 14. Dokumentacja dla testerów (radców prawnych)

Stworzyć `docs/INSTRUKCJA_TESTOWA.md`:
- Jak otworzyć narzędzie (URL, login)
- Co wpisywać w fact_pattern (wskazówki: pełne dane, kontekst, role)
- Jak interpretować wynik (CONFLICT/CONFLICT_WAIVABLE/NO_CONFLICT, confidence, discrepancies)
- Co oznacza "discrepancies" / niska pewność
- Jak zgłaszać błędy (formularz / email / GitHub issue)
- Lista znanych ograniczeń (system nie analizuje art. 25, 25a; nie sprawdza zgody klienta proceduralnie itd.)

**Estymacja:** 1 dzień razem z prawnikiem

---

## Sugerowana kolejność prac

**Tydzień 1 (P0 — blokery):**
1. Frontend update — wyświetlanie article_evaluations + discrepancies (#1)
2. Test harness na 20 golden cases (#2)
3. Backupy DB (#3)

**Tydzień 2 (P1 — jakość wyniku):**
4. Strojenie rule_engine guardrails (#4) — uruchamiać z #2 jako loop
5. Agregacja confidence (#5)
6. Sanity check LLM output (#6)
7. Retry / robustness (#7)

**Tydzień 3 (P2 — pre-production polish, równolegle z testami radców):**
8. Rozszerzenie datasetu (#8) — z prawnikiem
9. Disclaimers UI (#12) — z prawnikiem
10. Dokumentacja testowa (#14)
11. Cleanup (#13)
12. Performance (#9), Monitoring (#10), PII (#11) — w miarę bandwidth

**Gate do oficjalnych testów:**
- ≥90% pass rate na golden 20 case'ów
- Frontend renderuje pełny final_result
- Backupy działają (manualne wykonanie + restore test)
- Disclaimers w UI zatwierdzone przez prawnika
- Co najmniej jeden "dry run" z 1-2 zaufanymi radcami przed szerszym testem
