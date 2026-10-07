UWAGA: plik nieaktualny (stan z 14.05). Aktualny stan: docs/2026-09-27_model_i_baza.md i docs/projekt/

# CLAUDE.md — Instrukcje dla Claude Code

> Przeczytaj ten plik w całości przed wykonaniem jakiegokolwiek zadania w tym projekcie.
> Ostatnia aktualizacja: 2026-05-14 — uproszczenie do single-shot LLM + plan rozbudowy kontekstu (glosariusz pojęć + warstwy)

---

## Czym jest OBSIL

System wspomagania oceny konfliktu interesów dla radców prawnych (KIRP).
Narzędzie decision-support — nie autonomiczne. Radca prawny podejmuje finalną decyzję.

**URL produkcyjny:** `https://obsil.eubusinesscenter.com`
**Auth dostęp:** Basic Auth (tymczasowy, docelowo OIDC Ekstranet KIRP)

---

## Stack techniczny

| Warstwa | Technologia |
|---------|------------|
| Backend | FastAPI (Python 3.12) + SQLAlchemy 2.0 (async) + Alembic + Pydantic v2 |
| Frontend | Next.js 16 (App Router) + TypeScript + Tailwind CSS |
| Baza danych | PostgreSQL 16 (Docker: `obsil-db`, port 5432) |
| LLM | Provider-agnostic adapter (aktualnie: Google Gemini 2.5 Flash) |
| Reverse proxy | Traefik v2.11 (routing, TLS/Let's Encrypt) |
| Procesy | systemd user services (`obsil-backend`, `obsil-frontend`) |

---

## Struktura projektu

```
obsil/
├── CLAUDE.md              ← TEN PLIK — czytaj zawsze
├── README.md              ← Ogólny opis i roadmapa
├── backend/               ← FastAPI app (port 8001)
│   ├── .env               ← Zmienne środowiskowe (nie commituj!)
│   ├── .venv/             ← Virtualenv Python
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py        ← FastAPI app entry, CORS middleware
│   │   ├── api/
│   │   │   ├── analysis.py   ← POST /api/v1/analyze, GET /api/v1/analyze/{id}, POST /api/v1/analyze/{id}/clarify
│   │   │   └── history.py    ← GET /api/v1/history, GET /api/v1/history/{id}, GET /api/v1/admin/audit
│   │   ├── core/
│   │   │   ├── config.py     ← Settings (pydantic-settings, ładuje .env)
│   │   │   ├── database.py   ← AsyncEngine, AsyncSession, Base
│   │   │   └── deps.py       ← get_db dependency
│   │   ├── models/
│   │   │   ├── db_models.py  ← SQLAlchemy: User, Analysis, AuditLog, Clarification
│   │   │   └── schemas.py    ← Pydantic: AnalysisCreateRequest, AnalysisResponse, etc.
│   │   ├── services/
│   │   │   ├── orchestrator.py  ← 5-etapowy przepływ analizy (główna logika)
│   │   │   ├── comparator.py    ← Porównanie wyników schematic vs independent
│   │   │   └── audit.py         ← Audit log service
│   │   ├── adapters/
│   │   │   ├── llm_adapter.py   ← Provider-agnostic LLM adapter (Anthropic / Google)
│   │   │   └── prompts/
│   │   │       ├── extraction_system.txt + extraction_schema.json
│   │   │       ├── article_check_system.txt + article_check_schema.json   ← per-article eval (NEW)
│   │   │       ├── articles_catalog.json   ← 9 artykułów KERP do single-shot ewaluacji
│   │   │       ├── simple_analysis_system.txt + simple_analysis_schema.json   ← pipeline 3.0
│   │   │       ├── glossary/              ← Warstwa 2 kontekstu LLM — karty pojęć (W BUDOWIE)
│   │   │       └── schematic_*, independent_*, article_check_*, extraction_* (deprecated)
│   │   └── rules/
│   │       └── engine.py        ← Rule engine (keyword guardrails, JSON z rules/)
│   └── migrations/
│       └── versions/001_initial.py
├── frontend/              ← Next.js app (port 3000)
│   ├── .env               ← NEXT_PUBLIC_API_URL=https://obsil.eubusinesscenter.com/api/v1
│   ├── app/
│   │   ├── layout.tsx        ← Root layout (beta badge)
│   │   ├── page.tsx          ← Strona główna → redirect do /analyze
│   │   ├── analyze/
│   │   │   ├── page.tsx      ← Formularz + polling stanu analizy
│   │   │   └── [id]/result/page.tsx  ← Wynik analizy
│   │   └── history/page.tsx  ← Historia analiz
│   ├── components/ui/        ← shadcn/ui + custom komponenty
│   │   ├── FactPatternForm.tsx
│   │   ├── ClarificationForm.tsx
│   │   ├── AnalysisCard.tsx
│   │   ├── ConflictBadge.tsx
│   │   ├── RiskCard.tsx
│   │   └── LegalBasis.tsx
│   ├── lib/
│   │   ├── api.ts            ← API client (fetch wrappery)
│   │   └── utils.ts
│   └── types/analysis.ts     ← TypeScript typy odpowiedzi API
├── docs/
│   ├── architecture/      ← Architektura, diagramy, schemat JSON
│   ├── legal/             ← KERP, u.r.p., przepisy źródłowe
│   └── decisions/         ← ADR (Architecture Decision Records)
├── rules/                 ← Baza reguł (JSON) — serce systemu
│   ├── hard/              ← Zakazy bezwzględne (CONFLICT)
│   ├── soft/              ← Reguły uchylalne (CONFLICT_WAIVABLE)
│   └── ontology/          ← Słownik podmiotów i relacji
├── infra/
│   └── docker/docker-compose.yml  ← Tylko DB (obsil-db)
└── scripts/
    ├── start_dev.sh
    ├── test_rule_engine.py
    └── validate_rules.py
```

---

## Modele danych

### Tabele PostgreSQL

**`analyses`**
| Kolumna | Typ | Opis |
|---------|-----|------|
| id | UUID | PK |
| user_id | UUID | FK → users |
| status | enum | pending → extracting → analyzing → complete / error |
| fact_pattern_raw | Text | Wejście od użytkownika |
| extraction_result | JSONB | Wynik etapu 1 (wyciąg encji) |
| schematic_result | JSONB | Wynik analizy schematycznej (LLM) |
| independent_result | JSONB | Wynik analizy niezależnej (LLM) |
| final_result | JSONB | Wynik końcowy po komparatorze |
| conflict_classification | String | NO_CONFLICT / CONFLICT_WAIVABLE / CONFLICT |
| risk_level | String | niskie / umiarkowane / wysokie / krytyczny |
| confidence_level | String | wysoka / umiarkowana / niska |
| processing_time_ms | Int | Czas przetwarzania |

**`clarifications`** — pytania uzupełniające i odpowiedzi użytkownika

**`audit_log`** — zdarzenia systemowe (każda operacja)

**`users`** — użytkownicy (sub z OIDC, nr_wpisu, izba)

---

## Przepływ analizy (Orchestrator) — PIPELINE 3.0 SINGLE-SHOT (od 2026-05-14)

Filozofia: **jedno wywołanie LLM z pełnym katalogiem KERP w prompcie**. Bez extraction, bez rule_engine, bez sekwencyjnej ewaluacji 9 artykułów, bez comparatora. Powód: pipeline 2.0 był wolny (~85-130s), kruchy (9 niezależnych LLM calls), i rule_engine generował false-positive discrepancies. Single-shot daje wynik w ~25-31s.

```
POST /api/v1/analyze
  └─ Zapisz analysis (status=pending) → zwróć ID natychmiast (HTTP 202)
     └─ BackgroundTask: AnalysisOrchestrator.run_analysis()
          ├─ status=analyzing → llm.analyze_simple(fact_pattern, articles_catalog)
          │     payload: system prompt + 9 artykułów KERP (tekst+przesłanki) + casus
          │     odpowiedź: pełen JSON (entities, roles, classification, justification,
          │                article_evaluations[9], legal_basis, ...)
          └─ status=complete → zapis final_result (mode=llm_only zawsze)

GET /api/v1/analyze/{id}   ← Frontend polluje co 2s
POST /api/v1/analyze/{id}/clarify   ← (nadal istnieje, ale trigger out of scope w 3.0)
```

### Katalog artykułów (przekazywany do LLM w jednym prompcie)

| ID | Artykuł | Konfiguracja | Waivable |
|----|---------|--------------|----------|
| KERP-30 | art. 30 | Interes własny prawnika | nie |
| KERP-27 | art. 27 (pkt 1-6) | Zakazy bezwzględne | nie |
| KERP-28-2 | art. 28 ust. 2 | Klient = przeciwnik | nie |
| KERP-28-3 | art. 28 ust. 3 | Aktualny vs były klient — pełnomocnictwo | nie |
| KERP-28-1 | art. 28 ust. 1 | Aktualni klienci — pełnomocnictwo | nie |
| KERP-29-1-pkt1 | art. 29 ust. 1 pkt 1 | Aktualni klienci — doradztwo | tak |
| KERP-29-1-pkt2 | art. 29 ust. 1 pkt 2 | Aktualny vs były klient — doradztwo | tak |
| KERP-26 | art. 26 | Klauzula generalna (tajemnica/niezależność/przewaga) | nie |
| KERP-26a | art. 26a | Konflikt w kancelarii (chinese wall) | tak |

LLM sam decyduje o kolejności sprawdzania — w odpowiedzi zwraca `article_evaluations[]` dla wszystkich 9 + agregację (classification/risk/confidence/justification/legal_basis).

### Pole `mode` w final_result

- `llm_only` — tryb domyślny (jedyny aktywny w pipeline 3.0)
- `error_fallback` — exception w pipeline; status=complete + komunikat błędu w justification (frontend nie wisi)
- `anchored` — tryb z pipeline 2.0, obecnie nieużywany (rule_engine wyłączony)

### Format wyniku (final_result)

```json
{
  "entities": [...],
  "roles": [...],
  "relationships": [...],
  "matter_type": "...",
  "missing_information": ["..."],
  "analysis_completeness": "pelna" | "czesciowa",
  "risk_level": "krytyczny" | "umiarkowane" | "niskie",
  "conflict_classification": "CONFLICT" | "CONFLICT_WAIVABLE" | "NO_CONFLICT",
  "confidence_level": "wysoki" | "umiarkowany" | "niski",
  "justification": "[art. X] uzasadnienie | [art. Y] ...",
  "legal_basis": ["art. 28 ust. 2 KERP", ...],
  "rule_matches": [{"rule_id": "...", "article": "...", "result": "..."}],
  "article_evaluations": [
    {
      "article_id": "KERP-28-2",
      "article": "art. 28 ust. 2 KERP",
      "configuration": "Konfiguracja 3 — ...",
      "waivable": false,
      "applies": true,
      "confidence": "wysoka",
      "evaluation": {
        "matched_premises": [...],
        "unmatched_premises": [...],
        "missing_facts": [...],
        "justification": "...",
        "relevant_entities": ["entity_1", "entity_3"]
      }
    }
  ],
  "discrepancies": [
    {"type": "rule_engine_flagged_llm_disagreed" | "llm_applied_rule_engine_silent",
     "article": "...", "note": "..."}
  ],
  "source": "sequential_articles" | "rule_engine"
}
```

---

## API Endpoints

| Method | Path | Opis |
|--------|------|------|
| POST | `/api/v1/analyze` | Nowa analiza (min. 50 znaków) |
| GET | `/api/v1/analyze/{id}` | Status + wynik analizy |
| POST | `/api/v1/analyze/{id}/clarify` | Odpowiedzi na pytania uzupełniające |
| GET | `/api/v1/history` | Lista analiz (paginacja: skip/limit) |
| GET | `/api/v1/history/{id}` | Pełny wynik historycznej analizy |
| GET | `/api/v1/admin/audit` | Audit log (bez auth — tymczasowo) |
| GET | `/health` | Health check |

---

## Zmienne środowiskowe (backend/.env)

```
DATABASE_URL=postgresql+asyncpg://obsil:obsil@localhost:5432/obsil
SECRET_KEY=...
LLM_PROVIDER=google              # lub: anthropic
LLM_API_KEY=AIza...              # lub: sk-ant-...
LLM_MODEL_NAME=gemini-2.5-flash  # lub: claude-sonnet-4-5
LLM_ENDPOINT_URL=                # tylko dla Azure/Bedrock
ALLOWED_ORIGINS=["http://localhost:3000","https://obsil.eubusinesscenter.com"]
DEBUG=false
```

## Zmienne środowiskowe (frontend/.env)

```
NEXT_PUBLIC_API_URL=https://obsil.eubusinesscenter.com/api/v1
```

---

## Infrastruktura produkcyjna

### Procesy (systemd user services)
```bash
systemctl --user status obsil-backend   # FastAPI uvicorn :8001
systemctl --user status obsil-frontend  # Next.js :3000
systemctl --user restart obsil-backend
systemctl --user restart obsil-frontend
```

### Baza danych
```bash
docker ps | grep obsil-db          # PostgreSQL 16 na :5432
docker logs obsil-db               # Logi
```

### Traefik routing (obsil.eubusinesscenter.com)
- `/api/*`, `/health`, `/docs`, `/openapi` → backend :8001 (bez auth)
- `/*` → frontend :3000 (Basic Auth: ajedrzejewski)
- Konfiguracja: `/home/adam/apps/traefik/dynamic/obsil.yml`

### Logi
```bash
journalctl --user -u obsil-backend -f   # Logi backendu
journalctl --user -u obsil-frontend -f  # Logi frontendu
```

---

## Zasady pracy w tym projekcie

### Ogólne
- **Jeden krok na raz** — realizuj dokładnie to, co opisuje zadanie
- **Zawsze czytaj istniejący kod** przed pisaniem nowego
- **Commit po każdym etapie** z opisowym komunikatem (feat/fix/docs/chore/test)
- **Nie zmieniaj innych plików** niż wskazanych w zadaniu

### Backend
- Typowanie przez Pydantic v2 (nie v1)
- Async wszędzie gdzie możliwe (SQLAlchemy async session)
- Obsługa błędów przez HTTPException z odpowiednimi kodami
- Żadnych hardkodowanych sekretów — tylko zmienne środowiskowe
- Po zmianie modeli DB: `alembic revision --autogenerate -m "opis"` + `alembic upgrade head`
- Po zmianie kodu: `systemctl --user restart obsil-backend`

### Frontend
- App Router (nie Pages Router)
- TypeScript strict mode
- Komponenty w `components/ui/` — shadcn/ui, nie modyfikuj wnętrza podstawowych
- Paleta: granat `#1B2A4A`, biel `#FFFFFF`, czarny `#0A0A0A`
- Beta badge widoczny na każdej stronie
- Po zmianie kodu: `npm run build` + `systemctl --user restart obsil-frontend`

### Reguły (rules/)
- Klucze JSON: po angielsku (snake_case)
- Opisy dla prawnika: po polsku (pole `description_pl`)
- `waivable: false` + `result: "CONFLICT"` = zakaz bezwzględny
- `waivable: true` + `result: "CONFLICT_WAIVABLE"` = zakaz uchylalny za zgodą
- Każda reguła musi mieć `legal_basis` z dokładnym artykułem KERP/u.r.p.
- Nie wymyślaj reguł — wszystko musi wynikać z dokumentów źródłowych w docs/legal/

---

## Architektura kontekstu LLM (rozbudowa w toku, plan z 2026-05-14)

### Budżet tokenów (pomiar realny, Gemini 2.5 Flash)

Per zapytanie (single-shot pipeline 3.0):
| Składnik | Tokeny | Status |
|---|---|---|
| System prompt (instrukcje) | ~1 449 | aktualny |
| Katalog 9 art. KERP | ~2 453 | aktualny |
| Kazus użytkownika (max 3 000 zn.) | ~280-410 | aktualny |
| **Input łącznie** | **~4 300** | 0,4% limitu Gemini (1 048 576) |
| **Output (avg)** | **~2 537** | min 2 395, max 2 670 |
| **Razem per analiza** | **~6 850** | |

Przy szacowanym wolumenie ~100 zapytań/m-c (samorząd radców) koszt jest pomijalny. **Optymalizujemy nie pod budżet, tylko pod jakość analizy.** Mamy ~99% bufora kontekstu na rozbudowę.

### Docelowa architektura (4 warstwy kontekstu)

```
WARSTWA 1: PRZEPISY ŹRÓDŁOWE
  ├─ KERP (9 artykułów — JEST, articles_catalog.json)
  ├─ Wybrane art. u.r.p. (TODO: art. 3 tajemnica, art. 6, 11,
  │   art. 22³ niezależność, art. 24 zakazy łączenia)
  └─ Krótkie odwołania do KK (TODO: art. 115 § 11 osoba najbliższa)

WARSTWA 2: GLOSARIUSZ POJĘĆ KLUCZOWYCH (TODO — najważniejszy obszar pracy)
  ├─ ~10 kart definicyjnych (każda ≤ 1 strona A4, 10pt)
  ├─ Wzorzec karty: Definicja + Wykładnia OSD (tezy zanonimizowane)
  │   + Granice pojęcia (obejmuje/nie obejmuje) + Nie mylić z + Wskazówka
  └─ Cel: zaszczepić LLM przewidywalne ramy interpretacyjne

WARSTWA 3: ALGORYTM DECYZYJNY (TODO)
  ├─ Kolejność sprawdzania artykułów (np. najpierw zakazy bezwzględne)
  ├─ Reguły rozstrzygania (CONFLICT > CONFLICT_WAIVABLE > NO_CONFLICT)
  └─ Checklist kompletności faktów

WARSTWA 4: PRZYKŁADY (few-shot, TODO)
  ├─ 1× CONFLICT (były klient + sprawa związana, pełen tok rozumowania)
  ├─ 1× CONFLICT_WAIVABLE (dwóch klientów + zgoda)
  └─ 1× NO_CONFLICT z pułapką (pozornie podobny do konfliktowego)
```

### Glosariusz — priorytety (kolejność wg ryzyka błędu LLM)

Status: ✅ = karta utworzona w `glossary/`, ⬜ = do zrobienia.

| Priorytet | Status | Pojęcie | Występuje w | Notatki |
|---|---|---|---|---|
| 1 | ✅ | **Sprawa ta sama / sprawa z nią związana** | art. 28-3, art. 29 | KRYTYCZNE — najczęstsza oś sporu w KIRP |
| 2 | ✅ | **Nieuzasadniona przewaga** | art. 26 | KRYTYCZNE — pojęcie ocenne |
| 3 | ⬜ | **Osoba najbliższa** | art. 27 pkt 3,6 / art. 30 | def. zamknięta z KK art. 115 § 11 |
| 4 | ⬜ | **Bliskie stosunki** | art. 27 pkt 5 | mylone z relacjami biznesowymi |
| 5 | ✅ | **Klient aktualny vs były klient** | art. 28, 29 | moment zakończenia reprezentacji |
| 6 | ⬜ | **Pomoc prawna / doradztwo / reprezentacja** | art. 28 vs 29 | decyduje o waivable |
| 7 | ⬜ | **Tajemnica zawodowa** | art. 26, art. 3 u.r.p. | zakres osobowy/przedmiotowy |
| 8 | ⬜ | **Niezależność radcy prawnego** | art. 26, art. 22³ u.r.p. | |
| 9 | ⬜ | **Konflikt interesów (def. ogólna)** | wszystkie | nie mylić z kolizją interesów handlowych |
| 10 | ⬜ | **Wspólne wykonywanie zawodu** | art. 26a, art. 27 pkt 4 | kancelaria vs współpraca ad hoc |

### Wzorzec karty glosariusza

```markdown
## [POJĘCIE]
Występuje w: art. X KERP (oraz art. Y u.r.p. / art. Z KK)

### Definicja
[Tekst ustawowy lub konstrukcja doktrynalna — 3-5 zdań]

### Wykładnia OSD (tezy zanonimizowane)
- [Teza 1 — co orzeczono w sytuacji typowej]
- [Teza 2 — granica pojęcia od strony pozytywnej]
- [Teza 3 — co OSD wykluczył spod zakresu]
- [Teza 4 — wyjątek lub przypadek graniczny]

### Granice pojęcia
**Obejmuje:** [3-5 typowych sytuacji]
**Nie obejmuje:** [3-5 sytuacji bliskich, ale poza zakresem]

### Nie mylić z
- [Pokrewne pojęcie A] — różnica: [krótko]
- [Pokrewne pojęcie B] — różnica: [krótko]

### Praktyczna wskazówka dla analizy
[1-2 zdania: na co zwrócić uwagę przy ocenie]
```

### Szacunkowy budżet po pełnej rozbudowie

| Warstwa | Dodaje tokenów |
|---|---|
| W1 — u.r.p. + KK (uzupełnienie) | ~2 000 |
| W2 — 10 kart glosariusza × ~700 | ~7 000 |
| W3 — algorytm decyzyjny | ~1 000 |
| W4 — 3 przykłady few-shot | ~3 000 |
| **Razem nowo dodane** | **~13 000 tokenów** (1,3% bufora) |
| **Input docelowy** | **~17 300 tokenów** (1,7% limitu) |

### Plan technicznej implementacji (TODO, gdy treść kart gotowa)

- Katalog `backend/app/adapters/prompts/glossary/` z osobnymi `.md` na pojęcie
- Funkcja `_build_simple_payload` w `llm_adapter.py` doczyta i wklei wszystkie karty + warstwy 1/3/4 do prompta
- Cap kazusu **3 000 znaków** w `AnalysisCreateRequest` (pydantic) + walidacja na froncie (informacja dla użytkownika)
- Ograniczenie cap = dyscyplina UX, nie ratunek budżetu (różnica ~340 tokenów)

### Kierunkowe limity output

- Aktualnie article_evaluations dla 9 art. = ~37% sumy tokenów per analiza
- Potencjalna optymalizacja: skrócić eval do jednolinijkowego verdict gdy `applies=false`, pełen rozbiór tylko dla `applies=true`. Wykonać DOPIERO gdy będzie ku temu konkretny powód (koszt nie boli).

---

## Stan projektu (2026-05-14)

### Co działa na produkcji
- ✅ Backend FastAPI — przyjmuje analizy, single-shot LLM, zwraca wynik
- ✅ **Pipeline 3.0 single-shot** — jedno wywołanie LLM z pełnym katalogiem KERP (~25-31s)
- ✅ **Pole `mode` w final_result** — `llm_only` / `error_fallback` / (legacy) `anchored`
- ✅ **Error fallback** — wyjątek w pipeline daje czytelny wynik zamiast wiszącego frontendu
- ✅ **Frontend zawsze pokazuje wynik** — badge AnalysisModeBadge + naprawione mapowanie klasyfikacji backend↔frontend (CONFLICT → konflikt_oczywisty)
- ✅ Frontend Next.js — formularz, polling (timeout 240s), wynik, historia
- ✅ Baza danych PostgreSQL — analyses, clarifications, audit_log, users
- ✅ Traefik — routing HTTPS z certyfikatami Let's Encrypt
- ✅ Systemd services — autostart po restarcie VPS

### Weryfikacja end-to-end (Gemini 2.5 Flash, 2026-05-14 single-shot)

| Scenariusz | Wynik | Podstawa | Czas |
|---|---|---|---|
| Klient B = przeciwnik klienta A | CONFLICT | art. 28 ust. 2 + 28-1 + 26 KERP | ~31s |
| Czysty zachowek (nowy klient, brak relacji) | NO_CONFLICT | — | ~25s |

### Co jest zakomentowane / niegotowe
- ⚠️ Auth (OIDC Ekstranet KIRP) — zakomentowane, tymczasowo Basic Auth Traefik
- ⚠️ user_id w analizach — hardkodowany placeholder UUID (faza 7)
- ⚠️ Audit log — endpoint bez auth (faza 7)
- ⚠️ **Martwy kod do usunięcia** (pipeline 2.0): `_evaluate_articles_sequentially`, `_build_final_from_articles`, `_build_final_from_rules`, cały `comparator.py`, cały `rules/engine.py` + `rules/hard|soft/*.json`, stare prompty (schematic_*, independent_*, article_check_*, extraction_*). Zostawione tymczasowo na wypadek rollbacku. Sprzątanie w osobnym PR po stabilizacji.
- ⚠️ Pole `extraction_result` w DB — niewypełniane w pipeline 3.0
- ⚠️ Endpoint `/clarify` — istnieje, ale obecnie nie jest triggerowany (pipeline 3.0 nie pauzuje na pytania uzupełniające — model zwraca `missing_information[]` od razu)

### Roadmapa najbliższa (priorytet po 2026-05-14)

**Etap A — rozbudowa kontekstu (zob. sekcja „Architektura kontekstu LLM" wyżej):**
- [x] **Baza orzecznicza** — `docs/legal/Orzecznictwo-WSD-konflikt-interesow.md` (22 orzeczenia WSD 2020–2025, źródło tez dla W2/W4)
- [x] **Glosariusz pojęć — pierwsze karty** w `backend/app/adapters/prompts/glossary/`: 01 „Sprawa ta sama / związana", 02 „Nieuzasadniona przewaga", 03 „Klient aktualny vs były" (tezy zdestylowane z bazy orzeczniczej)
- [ ] Pozostałe karty wg priorytetu z tabeli (osoba najbliższa/bliskie stosunki, pomoc prawna vs doradztwo, tajemnica, niezależność, ...)
- [ ] Implementacja `_build_simple_payload` doczytująca karty glosariusza do promptu
- [ ] Wybrane art. u.r.p. + odwołania do KK (art. 115 § 11)
- [ ] Algorytm decyzyjny (warstwa 3) — krótki schemat kolejności i rozstrzygania
- [ ] 3 przykłady few-shot (warstwa 4)
- [ ] Cap kazusu **3 000 znaków** (walidacja backend + frontend)

**Etap B — porządkowanie kodu (po stabilizacji A):**
- [ ] Usunięcie martwego kodu pipeline 2.0
- [ ] Migracja DB usuwająca `schematic_result`, `independent_result`, `extraction_result`
- [ ] Konsolidacja `_build_final_*` (tylko `_build_final_from_simple` + `_build_error_fallback`)

**Etap C — auth + deployment finalny:**
- [ ] Faza 7: Auth OIDC (Ekstranet KIRP) + user management
- [ ] Faza 9: Deployment produkcyjny KIRP
- [ ] Faza 10: Governance i utrzymanie

### Historia istotnych zmian (chronologicznie wstecz)

**2026-05-14** (commity `15c8186`, `bc9d8c6`)
- feat(pipeline): pole `mode` (anchored/llm_only/error_fallback) w final_result; frontend zawsze pokazuje wynik
- refactor(pipeline 3.0): single-shot LLM — jeden call zamiast 5 etapów, czas analizy spadł z ~85-130s do ~25-31s
- fix: mapowanie klasyfikacji backend (CONFLICT/CONFLICT_WAIVABLE/NO_CONFLICT) → frontend ConflictBadge keys (konflikt_oczywisty/potencjalny_konflikt/brak_konfliktu)
- nowe pliki: `backend/app/adapters/prompts/simple_analysis_system.txt`, `simple_analysis_schema.json`; `frontend/components/ui/AnalysisModeBadge.tsx`
- pomiar tokenów: input ~4 300 + output ~2 537 = ~6 850 tokenów per analiza (0,7% bufora Gemini 2.5 Flash)
- plan rozbudowy kontekstu: 4 warstwy (przepisy + glosariusz pojęć + algorytm + few-shot)

**2026-05-05 wieczór** (commit `5735663`)
- feat: sekwencyjna ewaluacja per artykuł KERP — `articles_catalog.json` (9 artykułów), `article_check_system.txt` + schema, `evaluate_article()` w obu adapterach
- refactor: usunięty rule_engine short-circuit, dodany comparator z `discrepancies`
- fix: `premises_logic` (AND_ALL/OR_ANY) — bo art. 27 i art. 26 mają alternatywne klauzule
- fix: doprecyzowanie "bliskie stosunki" jako relacji osobistych (nie biznesowych)

**2026-05-05** (commity `0466983`, `0b25707`, `01bfa28`, `30eea5d`)
- refactor: keyword-based entity classification w rule_engine (już nie strict enum)
- fix: open extraction schema — `type/role_type/relationship_type` jako wolny tekst
- fix: rule engine matching, clarification flow, enum consistency
- fix: frontend pollowania, error handling 422

**Wcześniej** — Fazy 1-6: dokumentacja prawna, reguły JSON, prompty, backend FastAPI, frontend Next.js (zob. README.md).

---

## Przydatne komendy

```bash
# Backend dev
cd /home/adam/projects/obsil/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8001

# Migracje DB
alembic upgrade head
alembic revision --autogenerate -m "opis zmiany"

# Frontend dev
cd /home/adam/projects/obsil/frontend
npm run dev        # dev server :3000
npm run build      # build produkcyjny

# Testy reguł
cd /home/adam/projects/obsil
python scripts/test_rule_engine.py
python scripts/validate_rules.py

# API test
curl -s https://obsil.eubusinesscenter.com/api/v1/analyze \
  -X POST -H "Content-Type: application/json" \
  -d '{"fact_pattern":"Jestem radcą prawnym i prowadzę sprawę X dla klienta Y. Teraz klient Z chce mnie zatrudnić w sprawie przeciwko Y w tej samej kwestii."}'
```
