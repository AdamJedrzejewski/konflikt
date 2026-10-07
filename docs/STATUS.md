# OBSIL: stan aplikacji

> **Punkt wznowienia z 27.09.2026:** bieżący stan całego projektu jest w [STATUS_PROJEKTU.md](../../STATUS_PROJEKTU.md), a instrukcja kontynuacji w [zapisie sesji](../../dokumentacja/2026-09-27_punkt_wznowienia.md). Lokalnie podłączono model subskrypcyjny przez Codexa i nową bazę eksperymentalną. Szczegóły: [model i baza](2026-09-27_model_i_baza.md). Poniższy opis produkcji z 29.05 jest historyczny i nie potwierdza obecnego stanu zdalnego serwera.

## Historyczny stan z 2026-05-29

## Status ogólny: v0.2-beta — działa na produkcji (pipeline 3.0 single-shot)

> Zmiana względem 2026-05-04: pipeline przepisany na single-shot LLM (ADR-006). Problem „backend upada po analizie" (pipeline 2.0) rozwiązany. Backend i frontend działają na produkcji pod systemd. Bieżący wektor pracy: **budowa warstwy kontekstu stałego dla LLM (glosariusz pojęć)**.

---

## ✅ Co działa na produkcji

### Pipeline analizy (3.0 single-shot)
- Jedno wywołanie LLM z pełnym katalogiem 9 artykułów KERP — czas ~25–31 s
- Pole `mode` w `final_result`: `llm_only` / `error_fallback` / (legacy) `anchored`
- Error fallback — wyjątek w pipeline daje czytelny wynik zamiast zawieszenia frontendu
- Braki informacyjne zwracane w `missing_information[]` (bez pętli pytań uzupełniających)

### Backend (FastAPI / Python 3.12)
- Modele DB: users, analyses, audit_log, clarifications (PostgreSQL 16)
- LLM adapter: Google Gemini 2.5 Flash (provider-agnostic; alternatywnie Anthropic)
- Endpointy: POST /analyze, GET /analyze/{id}, POST /analyze/{id}/clarify, GET /history, GET /admin/audit, /health
- Audit log: każde zdarzenie zapisywane w DB

### Frontend (Next.js 16 / TypeScript)
- Formularz stanu faktycznego (min. 50 znaków) + polling stanu analizy (timeout 240 s)
- Strona wyników: klasyfikacja, uzasadnienie, karty ryzyka, AnalysisModeBadge, disclaimer
- Historia analiz
- Beta banner na każdej stronie; paleta granat (#1B2A4A) + biel
- `NEXT_PUBLIC_API_URL` ustawiony na produkcji (https://obsil.eubusinesscenter.com/api/v1)

### Infrastruktura
- Docker: PostgreSQL 16 (`obsil-db`, :5432)
- Traefik proxy: obsil.eubusinesscenter.com (HTTPS, Let's Encrypt); Basic Auth na froncie
- systemd user services (`obsil-backend` :8001, `obsil-frontend` :3000) — autostart po restarcie VPS

### Baza wiedzy / kontekst LLM
- Pełne dokumenty źródłowe: KERP, u.r.p., przepisy źródłowe (`docs/legal/`)
- Katalog 9 artykułów KERP do ewaluacji (`articles_catalog.json`)
- **NOWE:** baza orzecznicza WSD 2020–2025 (`docs/legal/Orzecznictwo-WSD-konflikt-interesow.md`)
- **NOWE (w budowie):** glosariusz pojęć (`backend/app/adapters/prompts/glossary/`) — pierwsze karty

---

## ⚠️ Niegotowe / dług techniczny

| Pozycja | Priorytet | Opis |
|---------|-----------|------|
| Auth (OIDC Ekstranet KIRP) | ŚREDNI | Faza 7 — tymczasowo Basic Auth Traefik; `user_id` w analizach = placeholder UUID |
| Audit log bez auth | ŚREDNI | Endpoint `/admin/audit` tymczasowo bez autoryzacji (Faza 7) |
| Martwy kod pipeline 2.0 | NISKI | `comparator.py`, `rules/engine.py`, sekwencyjna ewaluacja, stare prompty — do usunięcia w osobnym PR (Etap B) |
| Pola DB po 2.0 | NISKI | `schematic_result`, `independent_result`, `extraction_result` — niewypełniane, migracja usuwająca w Etapie B |

---

## 📋 Roadmapa

### Etap A — rozbudowa kontekstu stałego LLM (bieżący priorytet)
- [x] Baza orzecznicza WSD (źródło dla W2/W4)
- [~] Glosariusz pojęć — pierwsze karty (zob. `glossary/`); kolejne wg priorytetu
- [ ] Wybrane art. u.r.p. + odwołania do KK (art. 115 § 11)
- [ ] Algorytm decyzyjny (W3)
- [ ] 3 przykłady few-shot (W4)
- [ ] Cap kazusu 3 000 znaków (walidacja backend + frontend)

### Etap B — porządkowanie kodu (po stabilizacji A)
- [ ] Usunięcie martwego kodu pipeline 2.0
- [ ] Migracja DB usuwająca nieużywane pola wyników

### Etap C — auth + deployment finalny
- [ ] Faza 7: Auth OIDC (Ekstranet KIRP) + user management
- [ ] Faza 9: Deployment produkcyjny KIRP
- [ ] Faza 10: Governance i utrzymanie

---

## 🔧 Jak uruchomić lokalnie

```bash
# PostgreSQL
docker start obsil-db

# Backend
cd /home/adam/projects/obsil/backend
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001 &

# Frontend
cd /home/adam/projects/obsil/frontend
npm run start -- -p 3000 &
```

## 🌐 Dostęp testowy (VPS)
- URL: https://obsil.eubusinesscenter.com
- Login: dane dostępowe poza repozytorium
- Swagger UI: https://obsil.eubusinesscenter.com/docs
