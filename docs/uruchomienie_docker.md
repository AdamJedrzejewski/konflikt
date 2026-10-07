# Uruchomienie OBSIL w kontenerach (Windows i VPS)

Ten sam zestaw kontenerów działa na Windows (Docker Desktop) i na VPS (Linux). Zawiera bazę PostgreSQL, backend z Codexem i stronę. Strona i API są pod jednym adresem: przeglądarka łączy się tylko ze stroną, a ta przekazuje zapytania `/api/v1` do backendu wewnątrz kontenerów.

## Jednorazowe przygotowanie

1. Zainstaluj Docker Desktop (Windows) albo Docker Engine z wtyczką Compose (VPS).
2. Na Windows przed klonowaniem repozytorium włącz długie ścieżki: `git config --global core.longpaths true`.
3. Skopiuj `infra/docker/.env.example` do `infra/docker/.env` i wpisz długie, losowe hasło w `POSTGRES_PASSWORD`. Plik `.env` nie trafia do repozytorium.

## Uruchomienie

Z katalogu głównego repozytorium (PowerShell lub terminal):

```powershell
docker compose -f infra/docker/docker-compose.yml --env-file infra/docker/.env up -d --build
```

Pierwsze budowanie trwa kilka minut. Strona: http://localhost:3000 (port zmienia `OBSIL_PORT` w `.env`).

## Logowanie Codexa (raz na komputer lub serwer)

Kontener ma własne logowanie Codexa, oddzielne od Codexa zainstalowanego w Windows. Zapisuje się na wolumenie `codex_home` i przetrwa restart oraz aktualizację aplikacji.

```powershell
docker compose -f infra/docker/docker-compose.yml exec backend codex login --device-auth
```

Polecenie wyświetli adres i kod. Otwórz adres w przeglądarce, zaloguj się kontem ChatGPT i wpisz kod. Sprawdzenie: `docker compose -f infra/docker/docker-compose.yml exec backend codex login status`.

Bez logowania strona działa, ale każda analiza kończy się komunikatem o braku logowania Codexa.

## Codzienna obsługa

| Czynność | Polecenie (z dopiskiem `-f infra/docker/docker-compose.yml --env-file infra/docker/.env` po `docker compose`) |
|---|---|
| Stan kontenerów | `docker compose ps` |
| Dzienniki backendu | `docker compose logs -f backend` |
| Zatrzymanie | `docker compose down` (dane zostają) |
| Aktualizacja po zmianach w kodzie | `git pull`, potem `docker compose up -d --build` |

`docker compose down -v` usuwa także bazę danych i logowanie Codexa. Nie używać bez kopii zapasowej.

## Logowanie i role

- `AUTH_MODE=local` (domyślnie): bez logowania, jedna osoba z rolą operatora. Tylko na komputerze, na którym strona jest dostępna wyłącznie lokalnie.
- `AUTH_MODE=cloudflare` (VPS): Cloudflare Access wpuszcza tylko osoby z listy, a backend sprawdza podpis tokenu Cloudflare przy każdym zapytaniu. Wymaga `CF_ACCESS_TEAM_DOMAIN` i `CF_ACCESS_AUD` z panelu Cloudflare Zero Trust.
- Role: adresy z `OPERATOR_EMAIL_LIST` są operatorami, pozostali zalogowani to testerzy. Tester widzi tylko własne analizy; operator widzi wszystkie oraz dziennik zdarzeń.

## Co gdzie leży

- Baza danych (analizy, w przyszłości uwagi i decyzje): wolumen `postgres_data`.
- Baza wiedzy: katalog repozytorium, podłączony do backendu tylko do odczytu.
- Logowanie Codexa: wolumen `codex_home`.
- Model: `LLM_MODEL_NAME` i `LLM_ALLOWED_MODELS` w `.env`; domyślnie `gpt-6-luna`.

## Uruchomienie bez Dockera

Dotychczasowe skrypty `scripts/Start-Backend.ps1` i `scripts/Start-Frontend.ps1` nadal działają. Strona domyślnie przekazuje zapytania do backendu na `http://localhost:8001`.
