# Lokalne połączenie OBSIL z subskrypcją ChatGPT i bazą roboczą

## Ustawienia

Backend czyta `backend/.env`, następnie `backend/.env.local`; zmienne procesu mają pierwszeństwo. Nowy plik lokalny wybiera `LLM_PROVIDER=codex_chatgpt` i `LLM_MODEL_NAME=gpt-6-astra`. Nazwę modelu można zmienić na inną dostępną na koncie. Lista dostępnych modeli jest odczytywana przez `scripts/check_codex.py`.

Połączenie używa oficjalnego Codex App Server i istniejącego logowania Codexa przez ChatGPT. Tokeny pozostają pod kontrolą Codexa, nie są kopiowane do aplikacji. Ten dostawca wymaga konta typu ChatGPT i nie przełącza się na klucz API po błędzie lub wyczerpaniu limitu. Zużywa dostępne limity subskrypcji Codexa; nie odnawia limitów ani nie dokupuje kredytów.

`CODEX_EXECUTABLE` pozwala wskazać pełną ścieżkę programu, jeżeli nie jest wykrywany automatycznie. W Windows używany jest plik wykonywalny bez pośrednictwa powłoki. `CODEX_REASONING_EFFORT` oraz `LLM_TIMEOUT_SECONDS` określają wysiłek modelu i limit czasu. Każde zapytanie ma oddzielny, nietrwały wątek Codexa; wynik i jego źródła zapisuje OBSIL.

Fabryka zachowuje dostawców `anthropic` i `google`. Przepięcie wymaga jawnej zmiany dostawcy, modelu i właściwej konfiguracji danego dostawcy oraz jego zależności. Rozliczenie innych dostawców jest odrębne od subskrypcji ChatGPT. Nie ma automatycznego przełączania po błędzie. W tej integracji sprawdzono rzeczywiste wywołanie Codexa; nie wykonywano zapytań do pozostałych dostawców.

## Baza

`KNOWLEDGE_MODE=experimental` włącza opracowania z `OBSIL/baza_wiedzy`. Rejestr wskazuje odebrane karty, a osobne manifesty rozstrzygają pochodzenie historycznych i nowych cytatów. Import sprawdza integralność plików oraz odwołań, zachowuje ograniczenia i noty do odbioru. Obejmuje również karty bez nowych rekordów.

Materiał jest przekazywany modelowi jako pakiet do testów. Nowe karty nie uzyskują statusu zatwierdzonej wykładni: `OCZEKUJE` pozostaje jawne. Eksperymentalny przebieg omija dawny katalog z uproszczonymi definicjami. Identyfikator wersji, identyfikatory użytych rekordów, cytaty odczytane z bazy i informacja o modelu trafiają do `final_result`. Błąd importu zatrzymuje analizę, bez zastąpienia pakietu starszą wiedzą.

Wynik nie jest pełnym audytem diagramu. W tej zmianie podłączono model i materiał; panel ocen, decyzje operatora oraz pełna rozmowa z wersjonowaniem jej kolejnych tur pozostają w planie dalszej pracy. Ekran wyniku pokazuje model, wersję bazy, luki, zakres nieoceniony oraz rozwijane rekordy z cytatami, autorstwem i ograniczeniami.

Kontekst zawiera wszystkie opracowania i rekordy merytoryczne. Powtarzające się teksty mają wspólny słownik odwołań; pełne źródła są przypisane przez jednoznaczny klucz manifestu i źródła. Dzienniki sprawdzania (`coverage`, `self_check`, `control_results`, `review.checks`) pozostają w plikach objętych wersją, bez wysyłania do modelu; zakresy, ograniczenia odbioru i odrębne noty korekt pozostają w kontekście. Test odtworzenia potwierdza zachowanie wszystkich pozostałych pól kart i rekordów, cytatów oraz noty OBS-024.

Pierwsza udana próba zużyła 244 356 tokenów wejściowych i 2 013 wyjściowych według Codexa. Token to jednostka tekstu rozliczana przez model, często część słowa. Przekazywanie całej bazy zajmuje dużą część dostępnego kontekstu i limitu subskrypcji. Następnym usprawnieniem powinien być kontrolowany dobór materiału do pytania, z zachowaniem wyjątków, źródeł przeciwnych i jawnego zakresu. Zmiana na model o mniejszym kontekście wymaga osobnej próby; błąd nie powoduje automatycznego obcięcia treści.

## Uruchomienie i kontrola

Z katalogu `OBSIL/aplikacja`:

```powershell
.\backend\.venv\Scripts\python.exe .\scripts\check_codex.py
.\backend\.venv\Scripts\python.exe .\scripts\check_integration.py
.\backend\.venv\Scripts\python.exe .\scripts\check_integration.py --live
.\scripts\Start-Backend.ps1
.\scripts\Start-Frontend.ps1
```

Pierwsza komenda sprawdza logowanie i listę modeli, druga import i lokalną bazę. Trzecia wysyła jeden syntetyczny kazus w ramach subskrypcji, sprawdza źródła oraz zapis i ponowne odczytanie wyniku. Dwie ostatnie uruchom w osobnych oknach PowerShell: pierwsza uruchamia API na porcie 8001, druga stronę na porcie 3000. Otwórz `http://localhost:3000`. Zatrzymanie każdego procesu: Ctrl+C w jego oknie. Nie udostępniać tego uruchomienia w sieci: bieżący kod aplikacji nie ma jeszcze docelowego uwierzytelniania użytkowników.

Lokalny plik `frontend/.env.local` wskazuje `http://localhost:8001/api/v1`, zamiast wcześniejszego zdalnego adresu. Uruchomienie dotyczy komputera użytkownika; nie wdrażano zmian na zdalny serwer. Konfiguracja modelu jest odczytywana przy starcie backendu, więc po jej zmianie trzeba uruchomić backend ponownie.

Testy korzystają z osobnej bazy `backend/obsil-test.sqlite3`. Wariant SQLite służy lokalnemu uruchomieniu bez serwera PostgreSQL. Zachowano typy PostgreSQL dla docelowego połączenia. Nie przenoszono ani nie zmieniano starej bazy z VPS.

## Dokumentacja połączenia

- [Oficjalne logowanie Codexa](https://learn.chatgpt.com/docs/auth): dostęp subskrypcyjny przez ChatGPT i odrębne rozliczenie API.
- [Codex App Server](https://learn.chatgpt.com/docs/app-server): połączenie lokalne, wątki, odpowiedzi strukturalne, odczyt stanu konta.

Zweryfikowano z lokalną wersją Codex CLI 0.156.1. Zmiana wersji programu lub katalogu modeli wymaga ponownego testu połączenia.

## Wynik kontroli z 27.09.2026

Rzeczywista próba API: `533ec47f-79a2-4e0b-9d40-0f58f31d2cc8`, wynik `UNCLEAR`, osiem pytań, siedem rekordów źródłowych. Sprawdzono dosłowną zgodność zapisanych rekordów z pakietem i ponowny odczyt z historii. 21 testów mechanizmu przeszło; kontrola typów interfejsu przeszła. W przeglądarce sprawdzono ekran tego wyniku i rozwinięcie cytatu. To odbiór integracji na jednym kazusie, bez twierdzenia o sprawdzeniu jakości wszystkich odpowiedzi.
