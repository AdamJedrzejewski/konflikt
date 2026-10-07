# OBSIL: zapis stanu na zakończenie pracy 27.09.2026

Dyspozycja użytkownika: „Zapisz aktualny stan projektu. Będziemy kontynuować pracę w najliższych dniach.”

## Stan zapisany

- Pierwsze opracowanie kolejki zakończone: 79/79 haseł. Łącznie z trzema wcześniejszymi próbami: 82 opracowania i 136 rekordów. Nie uruchamiać tej kolejki ponownie. Braki, konsultacje i decyzje operatora pozostają odrębne; status operatora `OCZEKUJE`.
- Lokalna aplikacja ma podłączony `gpt-6-astra` przez Codexa z logowaniem ChatGPT w subskrypcji. Zmiana modelu przez konfigurację, bez automatycznej podmiany na płatne API. Tokeny logowania pozostają w Codexie.
- Nowa baza działa w trybie eksperymentalnym. Zachowano odrębne źródła historyczne i aktualne, cytaty, ograniczenia i notę OBS-024-M02. Wersja: `c57cd83696bb54f52587cf573f9c120a7006b4ced1f4880e9d2167e042179519`.
- Wynik przechowuje model, wersję wiedzy i użyte rekordy. Ekran pokazuje źródła, pytania, luki oraz zakres nieoceniony. Rzeczywista próba na fikcyjnym kazusie przeszła; zapis i odczyt historii oraz widok w przeglądarce sprawdzone. 21 testów mechanizmu zaliczonych.
- Kod i dokumenty są zapisane na dysku. Repozytorium aplikacji zawiera lokalne zmiany, także wcześniejsze niż integracja; nie tworzono wspólnego zatwierdzenia zmian ani nie publikowano ich na serwer. Nie cofać tych plików do wersji repozytorium przy wznowieniu.

## Gdzie zacząć następnego dnia

1. Przeczytać [status projektu](../STATUS_PROJEKTU.md), niniejszy punkt wznowienia i [raport integracji](2026-09-27_integracja_modelu_i_bazy/RAPORT.md).
2. Korzystać z [instrukcji uruchomienia](../aplikacja/docs/2026-09-27_model_i_baza.md). Adres interfejsu: `http://localhost:3000`, API: port 8001. Procesy uruchomione w sesji nie są usługami startującymi automatycznie po restarcie komputera; sprawdzić dostępność przed ponownym uruchomieniem.
3. Zachować lokalne ustawienia `aplikacja/backend/.env.local` i `aplikacja/frontend/.env.local` oraz historię w `aplikacja/backend/obsil-test.sqlite3`. Nie kopiować tokenów Codexa do aplikacji. Kontrola logowania i importu nie wymaga nowego płatnego wywołania modelu; `check_integration.py --live` zużywa limit subskrypcji.
4. Punkt kontrolny: [wynik próby](2026-09-27_integracja_modelu_i_bazy/proba_api.json), analiza `533ec47f-79a2-4e0b-9d40-0f58f31d2cc8`: UNCLEAR, osiem pytań, siedem rekordów. To potwierdzenie połączenia, nie odbiór jakości całego systemu.

## Kolejne kroki do ustalenia i wykonania po powrocie

1. Ograniczyć materiał przekazywany przy pojedynczym pytaniu, zachowując właściwe znaczenia, wyjątki, przeciwne źródła i jawny zakres. Obecny pełny pakiet zużył w próbie 244 356 tokenów wejściowych, czyli jednostek tekstu liczonych do limitu modelu.
2. Uzupełnić rozmowę o kolejne pytania i odpowiedzi, zachowanie wszystkich tur oraz wersji wyników.
3. Dodać ocenę użytkownika i zgłaszanie luk/propozycji, a następnie obsługę decyzji operatora. Model ani zwykły tester nie zmieniają samodzielnie obowiązującej wiedzy.
4. Przygotować i przejść zestaw kontrolny przed testami użytkownika. Dotychczasowy cel: środa 30.09.2026; nowa dyspozycja zapowiada kontynuację w najbliższych dniach, bez wskazania innej daty. [Plan środowy](2026-09-27_plan_testow_na_srode.md).

Pełne odwzorowanie przejść diagramu, ocena poprawności prawnej wszystkich odpowiedzi i publikacja zewnętrzna pozostają niewykonane. Nie prowadzić dalszych przebiegów ani zmian w czasie przerwy bez nowej dyspozycji.
