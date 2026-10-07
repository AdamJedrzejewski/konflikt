# OBSIL: próba kazusu 7.10.2026

Dyspozycja użytkownika: „Przepuść jakiś testowy kazus”.

Wprowadzono przez przeglądarkę fikcyjny kazus: radca reprezentuje Alfę w trwającym procesie przeciwko Becie o 100 000 zł; Beta proponuje mu reprezentowanie jej w tym samym sporze. Pełny opis i odpowiedź aplikacji zapisano w `wynik.json`, widok w `wynik.png`.

Wynik aplikacji: CONFLICT, na ekranie „Konflikt oczywisty”. Model gpt-6-astra, baza 82 opracowań i 136 rekordów, wersja c57cd83696bb. Odpowiedź wskazuje odmowę przyjęcia nowego zlecenia i odwołuje się do siedmiu rekordów. To próba działania aplikacji, bez niezależnego odbioru prawnego wszystkich tez i cytatów. Status operatora pozostaje OCZEKUJE.

Analiza: a62b2658-6e25-4ebb-abc1-c568f7962e65. Ekran: http://localhost:3000/analyze/a62b2658-6e25-4ebb-abc1-c568f7962e65/result.

Pierwsza próba zakończyła się błędem technicznym przed odpowiedzią modelu: Codex nie mógł ustalić katalogu użytkownika w ograniczonym środowisku uruchomienia. Diagnostyka poza tym ograniczeniem potwierdziła istniejące logowanie ChatGPT i dostępność modelu. Po ponownej weryfikacji tożsamości procesu uruchomiono backend ponownie z normalnym dostępem do konfiguracji. Nie zmieniano kodu, modelu ani danych logowania. Test ponowiono przez ten sam formularz, wynik wyświetlono i odczytano ponownie przez lokalne API.

Model główny wykonał próbę i diagnostykę; Luna przejrzała transport i pokrycie istniejących testów, bez zmian plików. Nie było podstaw do zmiany opcji --stdio. Aktualny backend uruchomiono przez Start-Backend.ps1; dzienniki w katalogu tymczasowym użytkownika: obsil-Backend-20261007-restart3.out.log oraz .err.log. Procesy lokalne nie mają zapewnionego startu po restarcie komputera.
