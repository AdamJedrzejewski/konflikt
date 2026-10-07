# OBSIL — System Wspomagania Oceny Konfliktu Interesów

> Wersja: 0.9-beta | Produkcja: https://obsil.eubusinesscenter.com

System decision-support dla radców prawnych (KIRP). Analiza stanów faktycznych pod kątem art. 26–30a KERP i u.r.p. Narzędzie wspiera decyzję radcy — nie podejmuje jej autonomicznie.

## Stack techniczny

| Warstwa | Technologia |
|---------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2 |
| Frontend | Next.js 16 (App Router), TypeScript, Tailwind CSS |
| Baza danych | PostgreSQL 16 (Docker: `obsil-db`, port 5432) |
| LLM | Provider-agnostic adapter (aktualnie: Google Gemini 2.5 Flash) |
| Reverse proxy | Traefik v2.11 (routing, TLS/Let's Encrypt) |
| Hosting | DigitalOcean VPS (Frankfurt), Ubuntu 24.04 |
| Procesy | systemd user services |

## Struktura projektu

```
obsil/
├── CLAUDE.md              ← Instrukcje dla Claude Code (czytaj zawsze)
├── README.md              ← Ten plik
├── backend/               ← FastAPI app (port 8001)
│   ├── app/
│   │   ├── main.py            ← Entry point, CORS middleware
│   │   ├── api/
│   │   │   ├── analysis.py    ← POST /analyze, GET /analyze/{id}, POST /analyze/{id}/clarify
│   │   │   └── history.py     ← GET /history, GET /admin/audit
│   │   ├── core/
│   │   │   ├── config.py      ← Settings (pydantic-settings)
│   │   │   ├── database.py    ← AsyncEngine, AsyncSession
│   │   │   └── deps.py        ← get_db dependency
│   │   ├── models/
│   │   │   ├── db_models.py   ← SQLAlchemy: Analysis, Clarification, AuditLog, User
│   │   │   └── schemas.py     ← Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── orchestrator.py   ← 4-etapowy przepływ analizy
│   │   │   ├── comparator.py     ← Porównanie wyników dual-analysis
│   │   │   └── audit.py          ← Audit log service
│   │   ├── adapters/
│   │   │   └── llm_adapter.py    ← Provider-agnostic (Anthropic/Google/Azure)
│   │   └── rules/
│   │       └── engine.py         ← Rule engine (JSON rules)
│   ├── migrations/
│   └── .env                   ← Zmienne (nie commituj!)
├── frontend/              ← Next.js app (port 3000)
│   ├── app/
│   │   ├── layout.tsx         ← Root layout (beta badge)
│   │   ├── page.tsx           ← Redirect → /analyze
│   │   ├── analyze/
│   │   │   ├── page.tsx       ← Formularz + polling
│   │   │   └── [id]/result/page.tsx  ← Wynik analizy
│   │   └── history/page.tsx   ← Historia analiz
│   ├── components/ui/         ← shadcn/ui + custom
│   ├── lib/api.ts             ← API client
│   └── types/analysis.ts      ← TypeScript typy
├── docs/
│   ├── architecture/          ← Architektura, diagramy
│   ├── legal/                 ← KERP, u.r.p., przepisy źródłowe
│   └── decisions/             ← ADR (Architecture Decision Records)
├── rules/                 ← Baza reguł JSON — serce systemu
│   ├── hard/                  ← Zakazy bezwzględne (CONFLICT)
│   ├── soft/                  ← Reguły uchylalne (CONFLICT_WAIVABLE)
│   └── ontology/              ← Słownik podmiotów i relacji
├── infra/
│   └── docker/docker-compose.yml  ← PostgreSQL (obsil-db)
└── scripts/
    ├── start_dev.sh
    ├── test_rule_engine.py
    └── validate_rules.py
```

## Przepływ analizy

```
POST /api/v1/analyze (fact_pattern, min 50 znaków)
  → Zapis do DB (status=pending), zwrot ID (HTTP 202)
  → BackgroundTask:
      1. Extraction (LLM) → encje, role, relacje
      2. Rule Engine (JSON) → twarde reguły KERP
      3. Dual LLM Analysis → schematic + independent
      4. Comparator → final_result, conflict_classification

GET /api/v1/analyze/{id}
  → Frontend polluje co 2s → pending → extracting → analyzing → complete

POST /api/v1/analyze/{id}/clarify
  → Odpowiedzi na pytania uzupełniające → re-analiza
```

## Fazy projektu

- [x] Faza 1–2: Analiza przepisów, dokumentacja prawna
- [x] Faza 3: Formalizacja reguł JSON + ontologia
- [x] Faza 4: System prompty + LLM adapter
- [x] Faza 5: Backend FastAPI (API, orchestrator, DB)
- [x] Faza 6: Frontend Next.js (formularz, wynik, historia)
- [ ] **Faza 7: Auth OIDC (Ekstranet KIRP) + user management** ← NASTĘPNA
- [ ] Faza 8: Testy E2E + kalibracja reguł
- [ ] Faza 9: Deployment produkcyjny KIRP
- [ ] Faza 10: Governance i utrzymanie

## Uruchomienie (produkcja)

```bash
# Serwisy
systemctl --user start obsil-backend    # FastAPI :8001
systemctl --user start obsil-frontend   # Next.js :3000

# Logi
journalctl --user -u obsil-backend -f
journalctl --user -u obsil-frontend -f

# Baza danych
docker compose -f infra/docker/docker-compose.yml up -d
```

## Uruchomienie (dev)

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload --port 8001

# Frontend
cd frontend && npm run dev

# Testy reguł
python scripts/test_rule_engine.py
python scripts/validate_rules.py
```

## Auth (tymczasowo)

- Basic Auth na Traefik (użytkownik: `ajedrzejewski`)
- Docelowo: OIDC Ekstranet KIRP (faza 7)
- API endpoints (`/api/*`) bez auth — dostępne bezpośrednio

## Infrastruktura

- **Traefik**: routing + TLS (Let's Encrypt) — config: `/home/adam/apps/traefik/dynamic/obsil.yml`
- **PostgreSQL**: Docker container `obsil-db` na porcie 5432
- **Systemd**: user services z `Restart=always`
- **Domena**: `obsil.eubusinesscenter.com`
