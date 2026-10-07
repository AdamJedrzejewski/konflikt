# OBSIL: model subskrypcyjny i nowa baza, 27.09.2026

Wykonano kolejność wskazaną przez użytkownika: najpierw połączenie modelu, następnie nowej bazy. Lokalna aplikacja używa `gpt-6-astra` przez oficjalny Codex App Server i istniejące logowanie ChatGPT. Dostawca `codex_chatgpt` nie używa klucza API ani automatycznego zastępczego dostawcy. Model można zmienić w `backend/.env.local`, po czym zrestartować backend. Pozostałe adaptery zachowano, ale ich rzeczywistych wywołań nie testowano.

## Zakres wykonany

- Baza eksperymentalna: 82 opracowania, 136 rekordów, 46 punktów schematu. Statusy pozostają częściowe i `OCZEKUJE`.
- Osobne manifesty źródeł historycznych i obecnych; kontrola pełnych plików, kart, cytatów, identyfikatorów i not odbioru. Zachowano korektę OBS-024-M02.
- Wersja pakietu: `c57cd83696bb54f52587cf573f9c120a7006b4ced1f4880e9d2167e042179519`.
- Każdy wynik zapisuje model, wersję wiedzy, użyte rekordy i dosłowne cytaty. Nieznane identyfikatory źródeł powodują odrzucenie odpowiedzi. Błędy połączenia/importu mają status błędu, bez podmiany wiedzy.
- Ekran wyniku pokazuje połączenie modelu, bazę, luki, nieoceniony zakres i rozwijane źródła. Lokalny interfejs wskazuje teraz lokalne API.
- Osobna baza SQLite do testów, bez zmiany starej bazy VPS. Serwisy uruchomiono tylko na adresie lokalnym.

## Dowody wykonania

1. Odczyt logowania: konto typu ChatGPT. Rzeczywista krótka próba modelu: poprawny JSON.
2. [Próba API](proba_api.json): fikcyjny kazus Alfy i Bety, `UNCLEAR`, osiem pytań uzupełniających i siedem rekordów. Zapis i odczyt przez historię zgodny; rekordy w wyniku identyczne z załadowanym pakietem.
3. 21 testów: transport i błędy, integralność importu, zachowanie treści kontekstu, kontrola źródeł/wyniku i błędy inicjalizacji.
4. Kontrola typów interfejsu oraz przeglądarka: model, status, wersja i rekordy widoczne; rozwinięcie cytatu działa.

Pierwsze dwie próby integracyjne wykryły błędny typ UUID w wariancie SQLite i parametr protokołu odrzucany przez zainstalowany Codex. Obie zatrzymały się przed analizą modelową. Poprawiono typ przenośny między bazami i użyto obsługiwanego trybu `readOnly`; narzędzia, sieć modelu i serwery integracyjne są wyłączone. Nie jest to deklaracja pełnej izolacji systemowej procesu Codexa.

Kontekst udanej próby: 244 356 tokenów wejściowych, 2 013 wyjściowych. Przekazano wszystkie znaczenia, rekordy i ograniczenia; pominięto dzienniki pracy i powtarzające się kopie tekstów, zachowując ich treść merytoryczną i odrębne noty. Dobór mniejszego zakresu do pytania jest kolejnym usprawnieniem potrzebnym do oszczędniejszego wykorzystania subskrypcji.

## Ograniczenia i dalsza praca

To sprawdzone podłączenie modelu i bazy na jednym kazusie, nie odbiór jakości prawnej całego systemu. Kontrola identyfikatora źródła nie dowodzi poprawności zastosowania tezy. Baza pozostaje niepełna; potrzebne dalsze testy przeciwne i ocena wyników. Do środowego planu pozostają pełna rozmowa z wersjonowaniem, oceny użytkownika, rejestr propozycji i decyzje operatora. Pełne przejścia diagramu nie zostały wdrożone.

Przy imporcie ujawniono stary licznik znaków obecnego SRC-01: 143 987 zamiast 165 430. Pełna suma kontrolna i 1 759 wierszy są zgodne. Loader zachowuje deklarowaną i rzeczywistą liczbę; źródła i manifesty pozostawiono bez zmian.

Astra wykonała integrację, próbę rzeczywistą, interfejs i odbiór. Luna przygotowała loader oraz testy transportu/importu i poprawkę błędów inicjalizacji; Astra sprawdziła mapowanie partii, dołączenie noty i wersjonowanie.

[Instrukcja uruchomienia i zmiany modelu](../../aplikacja/docs/2026-09-27_model_i_baza.md).
