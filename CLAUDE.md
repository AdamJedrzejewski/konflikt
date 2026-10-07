# OBSIL: instrukcje dla agentów

Aktualizacja: 7.10.2026. Poprzednia wersja tego pliku (stan z 14.05: VPS, Gemini, wieloetapowy pipeline) jest w historii repozytorium i nie opisuje obecnego działania.

## Czym jest projekt

OBSIL pomaga radcy prawnemu ocenić konflikt interesów na podstawie Kodeksu Etyki Radcy Prawnego i ustawy o radcach prawnych. Ostateczną decyzję zawsze podejmuje radca. Baza wiedzy jest zbudowana wokół schematu P. Skuczyńskiego (`docs/architecture/Diagram_Konflikt_interesow.pdf`). Każdy punkt schematu ma opracowania pojęć oparte na komentarzu i wybranych orzeczeniach WSD. Projekt jest realizowany z udziałem i na rzecz OBSIL. Materiały merytoryczne pochodzą od OBSIL. Kancelaria (AJ) odpowiada za kod i frontend.

## Gdzie jest bieżący stan

- `docs/projekt/2026-10-07_plan_dzialania_001.md`: etapy do wersji 0.01 i decyzje AJ. Zacznij od tego pliku.
- `docs/projekt/2026-10-07_plan_wersji_001.md`: wymagania wersji 0.01.
- `docs/projekt/2026-10-07_inwentaryzacja_do_001.md`: co działa, a czego brakuje w kodzie.
- `docs/2026-09-27_model_i_baza.md`: połączenie z modelem i bazą wiedzy.
- `docs/STATUS.md` i `README.md` częściowo opisują dawny stan na VPS.

## Architektura

- `backend/`: FastAPI, SQLAlchemy (async), Alembic. Lokalnie SQLite (`obsil-test.sqlite3`), docelowo PostgreSQL.
- `frontend/`: Next.js 16, React 19, Tailwind 4. Przed zmianami we frontendzie przeczytaj `frontend/AGENTS.md`: ta wersja Next.js różni się od wcześniejszych.
- Analiza: jedno wywołanie modelu (`services/orchestrator.py` → `services/knowledge_analysis.py`). Przy `KNOWLEDGE_MODE=experimental` model dostaje całą bazę wiedzy (`services/knowledge_bundle.py`, `knowledge_context.py`). Tryb `off` używa starego katalogu artykułów.
- Model: dostawca `codex_chatgpt` (`adapters/codex_adapter.py`, `codex_transport.py`) przez Codex App Server i logowanie ChatGPT AJ. Bez klucza API i bez automatycznego przełączania dostawcy. Adaptery `anthropic` i `google` istnieją, ale nie są używane.
- Baza wiedzy: katalog `baza_wiedzy/` w katalogu głównym repozytorium (`KNOWLEDGE_PROJECT_PATH`, domyślnie katalog główny). Status opracowań to `OCZEKUJE` i nie wolno go zmieniać bez decyzji operatora.
- Logowanie i role: `backend/app/core/auth.py`. `AUTH_MODE=local` (komputer AJ, rola operatora) albo `cloudflare` (weryfikacja podpisu tokenu Cloudflare Access). Operatorzy z `OPERATOR_EMAIL_LIST`, pozostali to testerzy. Każdy nowy endpoint z danymi analiz musi używać `get_current_user` i `get_owned_analysis`.
- Stare elementy: `rules/`, `services/comparator.py`, prompty pipeline 2.0 w `adapters/prompts/`. Nie rozwijać ich bez potrzeby.

## Decyzje, których trzeba przestrzegać

- Model do czasu licencji KIRP: subskrypcja ChatGPT przez Codexa. Ograniczenie do modelu nie wyższego niż Luna ustawia `LLM_ALLOWED_MODELS`; nie zmieniaj tej listy bez decyzji AJ.
- Wersja 0.01 trafia do Pawła Skuczyńskiego do samodzielnych testów. Docelowo: VPS, Cloudflare Tunnel i Access, automatyczne wdrażanie oznaczonych wydań z GitHuba. Najpierw wszystko ma działać na GitHubie i na Windows, VPS na końcu.
- Przenośność: aplikacja ma działać i wyglądać tak samo na VPS i na Windows. Końce wierszy LF (`.gitattributes`).
- Nic, co analizuje model, nie staje się zatwierdzoną wiedzą bez decyzji operatora.

## Uruchomienie i testy

Testy (z katalogu głównego):
```bash
pip install -r backend/requirements.txt pytest
python -m pytest -q tests
cd frontend && npm ci && npx tsc --noEmit && npm run lint && npm run build
```
Testy na prawdziwej bazie wiedzy są pomijane, gdy brak `baza_wiedzy/`. GitHub Actions (`.github/workflows/ci.yml`) uruchamia te same kroki.

Kontenery (Windows i VPS, ten sam zestaw): `docs/uruchomienie_docker.md`. Strona i API pod jednym adresem; Next.js przekazuje `/api/v1` do backendu (`frontend/next.config.ts`, `BACKEND_URL`). Na PostgreSQL tabele tworzy `alembic upgrade head` przy starcie backendu.

Bez kontenerów, na Windows (PowerShell, z katalogu głównego): `backend/.env.local` na wzór `backend/.env.local.example`, potem `scripts/check_codex.py` (logowanie i lista modeli), `scripts/check_integration.py`, `scripts/Start-Backend.ps1` (API, port 8001) i `scripts/Start-Frontend.ps1` (strona, port 3000).

## Zasady

- Dokumentacja i komunikaty w interfejsie po polsku, prostym językiem. AJ jest radcą prawnym, nie programistą.
- Hasła, klucze i pliki `.env` nigdy nie trafiają do repozytorium.
- Zmiany przez pull request do `main`; `main` zmienia się po akceptacji AJ.
- Każda zmiana zachowania ma test.
