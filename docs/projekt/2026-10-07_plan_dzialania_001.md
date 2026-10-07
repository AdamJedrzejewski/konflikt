# OBSIL: plan działania do wersji 0.01

Data: 7.10.2026. Podstawa: [plan wersji 0.01](2026-10-07_plan_wersji_001.md), [inwentaryzacja](2026-10-07_inwentaryzacja_do_001.md), [model i baza](../2026-09-27_model_i_baza.md) oraz przegląd kodu po przeniesieniu repozytorium na GitHub.

Ten dokument przekłada plan wersji 0.01 na kolejne etapy pracy. Każdy etap kończy się osobną zmianą w repozytorium (pull request do `main`), którą AJ zatwierdza przed włączeniem.

## Stan wyjściowy (7.10.2026)

- Repozytorium `AdamJedrzejewski/konflikt`, gałąź `main`, jeden commit, 178 plików. Wcześniejsza historia zostaje lokalnie (`archiwum-master`).
- Testy backendu: 19 z 21 przechodzi. Pozostałe 2 wymagają katalogu `baza_wiedzy/`, którego nie ma w repozytorium.
- Frontend łączy się z `http://localhost:8001/api/v1` (`frontend/lib/api.ts`). Działa tylko na komputerze, na którym uruchomiono backend.
- Aplikacja działa w trybie deweloperskim (`next dev`, `uvicorn`). Nie ma konfiguracji wydania ani automatycznych testów na GitHubie.
- Brak logowania, ról i rozdzielenia historii użytkowników. Endpoint audytu nie jest zabezpieczony.
- Model: `gpt-6-astra` przez Codex App Server i logowanie ChatGPT AJ. Jedna analiza zużyła około 244 tys. tokenów wejściowych, bo do modelu trafia cała baza.
- Stara aplikacja na VPS jest wyłączona.

## Etapy

| Nr | Etap | Zakres | Sprawdzian | Wymaga decyzji lub danych |
|---|---|---|---|---|
| 0 | Porządek repozytorium | Nowy `CLAUDE.md`. Ścieżka bazy wiedzy jako ustawienie. Testy wymagające bazy pomijane z czytelnym komunikatem, gdy jej brak. Ustalone wersje zależności. Automatyczne testy na GitHubie (backend: pytest; frontend: typy, lint, build) | Każda zmiana na GitHubie przechodzi testy | Nie |
| 1 | Wspólny adres i paczka wydania | Frontend wywołuje `/api/v1` pod tym samym adresem, a Next.js przekazuje żądania do backendu. Kontenery produkcyjne dla frontendu i backendu (`next build`/`next start`, nie tryb deweloperski). Jeden plik `docker-compose` dla VPS i Windows, z bazą PostgreSQL na trwałym wolumenie i bazą wiedzy na osobnym wolumenie | Aplikacja uruchomiona z kontenerów działa tak samo na Linuksie i Windows; ze strony nie ma odwołań do `localhost` | Nie (próba na Windows wymaga Docker Desktop na PC AJ) |
| 2 | Tożsamość i role | Backend weryfikuje podpisany token Cloudflare Access (nagłówek `Cf-Access-Jwt-Assertion`), a nie sam adres e-mail z nagłówka. Tabela użytkowników tworzona po pierwszym wejściu. Role: tester i operator, przypisane w konfiguracji. Historia i odczyt analizy po identyfikatorze ograniczone do autora; operator widzi wszystko. Audyt tylko dla operatora. Tryb lokalny bez Cloudflare z jawnym użytkownikiem testowym | Tester nie odczyta cudzej analizy ani audytu, także bezpośrednim żądaniem; żądanie bez ważnego tokenu jest odrzucane | Adresy e-mail Pawła i operatora |
| 3 | Trwała rozmowa i rejestr uwag | Kolejne tury rozmowy zapisane osobno (pytanie, odpowiedź, wynik, wersja wiedzy). Pytania uzupełniające działają w trybie nowej bazy. Przycisk „Zgłoś uwagę” przy wyniku: rodzaj problemu, opis, oczekiwane rozstrzygnięcie, źródło; system dołącza analizę, wersję aplikacji i wiedzy. Widok „Moje uwagi” dla testera, widok zbiorczy i eksport CSV dla operatora | Kazus, doprecyzowanie i uwaga pozostają po restarcie; uwaga prowadzi do właściwej wersji odpowiedzi | Nie |
| 4 | Import konsultacji i propozycje modelu | Import tabeli 7 propozycji z 24.09 i czterech plików `KONSULTACJA.md` z zachowaniem treści, pochodzenia i statusu; ponowny import nie dubluje wpisów. Operator uruchamia przygotowanie propozycji zmiany przez model (co, dlaczego, gdzie w bazie, na jakim materiale, czego brakuje) | Ponowiony import daje tę samą liczbę wpisów; żaden wpis nie staje się zatwierdzony przez import | Pliki konsultacji (są poza repozytorium) |
| 5 | Panel operatora i wersje wiedzy | Decyzje: do uzupełnienia, zaakceptowana, odrzucona, odłożona. Publikacja nowej wersji wiedzy po próbach kontrolnych; przywrócenie poprzedniej. Wersja pilotażowa bazy zamrożona jako punkt wyjścia. Oczekujące i odrzucone propozycje nie wpływają na odpowiedź modelu | Tester nie zatwierdzi zmiany; zatwierdzona zmiana pojawia się dopiero w nowej wersji; stare wyniki zachowują swoją wersję | Nie |
| 6 | Wdrożenie na VPS | Cloudflare Tunnel (kontener `cloudflared`, bez otwierania portów na VPS) i Cloudflare Access dla listy adresów e-mail. GitHub Actions: po oznaczeniu wydania (tag, np. `v0.01`) testy, budowa kontenerów, wdrożenie przez SSH, migracje bazy, sprawdzenie działania i automatyczny powrót do poprzedniego wydania przy błędzie. Codzienna kopia bazy poza serwerem z próbą odtworzenia | Wydanie trafia na VPS bez ręcznych kroków; po błędzie wraca poprzednie; kopię da się odtworzyć | Dostęp SSH do VPS, domena w Cloudflare, decyzja w sprawie modelu (D1) |
| 7 | Odbiór 0.01 | Zestaw prób prawnych i technicznych (konflikt, brak konfliktu, wyjątek, brak faktu, luka w źródłach, korekta faktów; limit czasu, odświeżenie strony, dostęp do cudzych danych, publikacja przez testera). Wersja `0.01` w kodzie i w tagu. Instrukcja dla testera i lista ograniczeń | Cała ścieżka od logowania do obsługi uwagi przechodzi na VPS z innego komputera | Weryfikacja oczekiwanych wyników prawnych przez AJ |

Etapy 0, 1 i 3 nie wymagają żadnych danych i mogą ruszyć od razu. Etap 2 można zbudować i przetestować bez Cloudflare, a adresy e-mail podać przy wdrożeniu.

## Decyzje i dane potrzebne od AJ

**D1. Model na serwerze. Decyzja blokuje wdrożenie (etap 6).**
Obecna integracja korzysta z subskrypcji ChatGPT AJ przez Codexa. Na VPS wymaga to zalogowania Codexa na koncie AJ na serwerze i udostępniania analiz innym osobom przez osobistą subskrypcję. Trzeba sprawdzić, czy warunki subskrypcji na to pozwalają. Do tego dochodzą limity: przy około 244 tys. tokenów na analizę limit może się kończyć po kilku analizach. Warianty:
- a) Codex z subskrypcją AJ na VPS: bez dodatkowych kosztów, ale z ryzykiem regulaminowym i limitami; wymaga próby technicznej.
- b) Klucz API (OpenAI albo Anthropic; adapter Anthropic już istnieje w kodzie): rozliczenie za użycie, przewidywalne działanie bez komputera AJ; koszt do policzenia przed decyzją.
- c) Na czas pilotażu (a), z gotowym przełączeniem na (b).

Niezależnie od wariantu warto przyspieszyć dobór materiału do pytania zamiast wysyłania całej bazy (lista „Rozwój po uruchomieniu testów”). Zmniejszy to czas i koszt analizy.

**D2. Gdzie trzymać bazę wiedzy (`baza_wiedzy/`).**
Aplikacja bez niej nie działa w trybie nowej bazy, a VPS musi ją skądś dostać. Rekomendacja: dodać ją do tego repozytorium w osobnym katalogu `wiedza/` jako wersję pilotażową, zamrożoną i oznaczoną. Kolejne wersje publikowane przez operatora (etap 5) będą przechowywane na serwerze i objęte kopią zapasową. Alternatywa: osobne prywatne repozytorium tylko na bazę.

**D3. Dane do wdrożenia.**
- Dostęp do VPS: adres i użytkownik SSH. Klucz SSH trafia wyłącznie do ustawień „Secrets” repozytorium na GitHubie, nigdy do czatu ani plików.
- Domena: czy używamy `obsil.eubusinesscenter.com` lub innej subdomeny. Strefa DNS domeny musi być obsługiwana przez Cloudflare.
- Konto Cloudflare (Zero Trust, plan bezpłatny wystarcza do kilku użytkowników).
- Adresy e-mail: Pawła (tester) i operatora (AJ).

**D4. Materiały do importu (etap 4).** Tabela 7 propozycji z 24.09 i cztery pliki `KONSULTACJA.md` są poza repozytorium. Trzeba je dodać, np. do `wiedza/konsultacje/`.

## Zasady pracy

- Każdy etap to osobny pull request z opisem zmian i wynikiem testów. `main` zmienia się tylko po akceptacji AJ.
- Na VPS trafia wyłącznie oznaczone wydanie (tag). Zwykła zmiana w `main` nie aktualizuje serwera.
- Hasła i klucze tylko w ustawieniach GitHuba i w plikach `.env` na serwerze, nigdy w repozytorium.
- Baza danych i baza wiedzy leżą poza kontenerami aplikacji. Wymiana wydania ich nie nadpisuje.
- Te same kontenery na VPS i na Windows; różnice tylko w pliku ustawień środowiska.
