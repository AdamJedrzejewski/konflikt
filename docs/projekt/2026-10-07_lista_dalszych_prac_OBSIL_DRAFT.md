# DRAFT: do weryfikacji przed wysłaniem

# OBSIL: prace pozostające do wykonania

Stan na 7 października 2026 r. Wersja 0.01 jest planowanym wydaniem do zamkniętych testów. Poniższa kolejność jest propozycją wykonawczą; terminu wydania nie ustalono.

## Przed przekazaniem wersji 0.01

| Zadanie | Co ma otrzymać użytkownik | Warunek zakończenia |
|---|---|---|
| Rejestr uwag przy analizie | Możliwość wskazania, co jest błędne lub niejasne, wpisania proponowanej poprawki i odniesienia do źródła | Uwaga zachowuje związek z kazusem, wynikiem, autorem i wersją wiedzy; można ją ponownie odczytać i wyeksportować |
| Podłączenie dotychczasowych konsultacji | Wspólny przegląd wcześniejszych pytań i nowych uwag | Zachowane identyfikatory, źródła i statusy; ponowny import nie mnoży tych samych wpisów |
| Moduł samouczenia | Propozycje zmian tworzone z uwag i rozpoznanych luk | Wykryta luka tworzy propozycję z uzasadnieniem; model nie zatwierdza jej samodzielnie |
| Decyzje operatora i wersje wiedzy | Zatwierdzenie, korekta, odrzucenie albo odłożenie propozycji | Zmiana wiąże się z konkretną decyzją i nową wersją; poprzednie wyniki zachowują swoją podstawę, a poprzednią wersję można przywrócić |
| Dalsza rozmowa o kazusie | Odpowiedź na pytanie aplikacji lub korekta faktów bez utraty wcześniejszej treści | Kolejne wypowiedzi i wyniki są zapisane oddzielnie, z oznaczeniem użytej wersji wiedzy |
| Dostęp dla Pawła | Jeden adres do testów z logowaniem i dostępem do własnych analiz oraz zgłoszeń | Wejście osoby nieuprawnionej jest zablokowane; tester nie może wykonywać operacji operatora ani odczytywać cudzej historii |
| Przygotowanie wydania | Oznaczenie 0.01, krótka instrukcja, kopia danych testowych i odtwarzalne uruchomienie | Wersję można uruchomić ponownie, odtworzyć po błędzie i zidentyfikować w każdym zgłoszeniu |
| Sprawdzian działania i odpowiedzi | Sprawdzone przykłady oraz jawna lista ograniczeń | Przechodzą próby analizy, zapisu uwagi, decyzji operatora, zmiany wersji i dostępu z innego komputera; oczekiwane wyniki prawne są sprawdzone w źródłach |

Wydanie testowe zachowa oznaczenie roboczego charakteru bazy. Udostępnienie wersji 0.01 nie zastąpi zatwierdzenia wszystkich oczekujących tez.

## Rozwój po uruchomieniu testów

| Obszar | Pozostały zakres |
|---|---|
| Schemat analizy | Pełne odwzorowanie i sprawdzenie punktów, przejść, wyjątków i zakończeń diagramu; wyjaśnienie niejednoznaczności |
| Wizualizacja | Czytelna mapa sprawdzonych punktów, zastosowanych podstaw i brakujących ustaleń w konkretnym kazusie |
| Dobór wiedzy | Przekazywanie modelowi materiału właściwego dla pytania z zachowaniem wyjątków, ograniczeń i stanowisk przeciwnych; pomiar czasu i zużycia limitu |
| Zestaw prób prawnych | Przypadki konfliktu, dopuszczalnej pomocy, wyjątków, brakujących faktów i rozbieżności źródeł; ponawianie po zmianach wiedzy |
| Źródła | Oryginały orzeczeń, szerszy materiał komentarzowy, aktualność przepisów i rozstrzygnięcie istniejących pytań konsultacyjnych |
| Organizacja korzystania | Docelowe role użytkowników, czas przechowywania danych, zasady obsługi rzeczywistych kazusów, dostępność i utrzymanie systemu |
| Wydanie docelowe | Środowisko niezależne od komputera roboczego, docelowa integracja z uwierzytelnianiem samorządu i formalny odbiór jakości |

Ograniczenie wielkości materiału dla modelu należy przesunąć przed wydanie 0.01, jeżeli próby wykażą, że czas odpowiedzi lub zużycie limitu uniemożliwia samodzielne testowanie.

## Podział pracy

Po mojej stronie pozostają rozwój aplikacji, podłączenie rejestru, opracowanie i wdrażanie zmian wiedzy oraz organizacja testów. Po stronie Pawła przewidziane są testy eksperckie, uwagi do wyników i poszerzanie materiału merytorycznego. Zgodnie z relacją AJ z 7.10.2026 Paweł zna już zadanie poszerzania bazy. Szczegółowy zakres nowych materiałów i terminy pozostają do ustalenia.

Proponowana rola Pawła w aplikacji to tester i ekspert zgłaszający uwagi. Uprawnienie do zatwierdzania zmian pozostaje osobną rolą operatora; samo autorstwo uwagi nie nadaje tego uprawnienia.

---

## Podstawy zestawienia, nie wprowadzać do materiału wysyłanego

Źródła: [notatka po spotkaniu](2026-10-07_notatka_po_spotkaniu.md), [plan budowy bazy](PLAN_BUDOWY_BAZY.md), [punkt wznowienia](2026-09-27_punkt_wznowienia.md), [inwentaryzacja kodu](2026-10-07_inwentaryzacja_do_001.md), [bieżący status](../STATUS_PROJEKTU.md). Warunki odbioru są propozycją wykonawczą opartą na istniejącym wymaganiu kontroli operatora. Nie stanowią nowych uzgodnień z Pawłem.
