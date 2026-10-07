# OBSIL: plan dojścia do testów w środę 30.09.2026

## Aktualizacja po decyzji użytkownika i integracji 27.09

Użytkownik zmienił kolejność: najpierw model w miesięcznej subskrypcji GPT z możliwością przepięcia, następnie nowa baza. Oba podłączenia wykonano lokalnie i sprawdzono na rzeczywistym zapytaniu przez API. Ekran wyniku pokazuje model, wersję bazy, cytaty, ograniczenia i luki. [Raport i zakres sprawdzenia](2026-09-27_integracja_modelu_i_bazy/RAPORT.md).

Wykonane elementy poniższego planu: połączenie modelu, import całego merytorycznego pakietu z weryfikacją integralności, oznaczenie wersji przy wyniku, zapis użytych rekordów, podstawowy ekran źródeł i jawne błędy. Odbiór dotyczy jednej próby integracyjnej; dalszy sprawdzian jakości pozostaje konieczny. Status operatora nie został automatycznie zmieniony.

Kolejny zakres: dobór mniejszego kontekstu przy zachowaniu wyjątków (pełny pakiet zużył około 244 tys. tokenów wejścia), pełna rozmowa z zachowaniem tur, oceny i rejestr propozycji, decyzje operatora, kontrolowany zestaw kazusów. Poniższa diagnoza stanu jest historycznym punktem wyjścia, a ta aktualizacja określa, które braki już usunięto.

Status: propozycja wykonawcza po przeglądzie plików i kodu 27.09.2026. Nie jest potwierdzeniem uruchomienia ani zakończenia wdrożenia.

## Cel i przyjęte założenia

Dyspozycja użytkownika: „chciałbym na środę (za 2 dni) mieć możliwość testowych zapytań i oceny wyników”. Użytkownik zakłada, że baza pozostaje niedoskonała i będzie usprawniana.

Według daty środowiska dzisiaj jest niedziela 27.09. Plan obejmuje dwa dni pracy, poniedziałek 28.09 i wtorek 29.09, oraz testy w środę 30.09. Zakładamy pierwszy test lokalny na komputerze użytkownika, na kazusach przykładowych lub zanonimizowanych. Dostęp dla testerów spoza tego komputera wymaga odrębnego przygotowania środowiska i uprawnień.

Stan docelowy: użytkownik opisuje sytuację, aplikacja dobiera wiedzę, zadaje potrzebne pytania, przedstawia ocenę wraz z podstawami i ograniczeniami, zapisuje przebieg i pozwala ocenić wynik. Wykryta luka tworzy propozycję poprawki. Operator może ją rozpatrzyć i opublikować nową wersję; poprzednia analiza zachowuje swoją wersję.

Niepełność bazy jest dopuszczalnym stanem testowym. Brak faktu, brak źródła albo nieobsługiwany zakres muszą być rozpoznawalne i nie mogą automatycznie prowadzić do wyniku „brak konfliktu”.

## Co już mamy i co trzeba połączyć

1. Odebrane zakresy wszystkich 79 haseł, 136 rekordów, źródła, cytaty, ograniczenia i konsultacje. Rejestr obejmuje 82 opracowania wraz z trzema próbami historycznymi. Odbiór opracowań pozostaje odrębny od decyzji operatora o dopuszczeniu do użycia.
2. Wykaz 46 punktów schematu i potrzebnych pojęć. Sam wykaz nie odtwarza wszystkich strzałek ani warunków przejścia.
3. Istniejący kod formularza, prezentacji wyniku, historii i zapisu analiz. Aktualny `run_analysis` wykonuje jedno wywołanie modelu z opisem sprawy i katalogiem artykułów. Starszy opis wieloetapowego przebiegu w README nie odpowiada aktywnej metodzie.
4. Nowe karty nie są jeszcze podłączone do aktywnego przebiegu. Instrukcja modelu zawiera własne skrótowe definicje. Trzeba wyeliminować sytuację, w której te skróty zastępują opracowane znaczenia i ograniczenia.
5. Nie potwierdzono lokalnego uruchomienia całej aplikacji po migracji. Dostępność bazy aplikacji i skutecznego wywołania dostawcy modelu trzeba sprawdzić na początku realizacji.
6. Istnieje 20 starszych kazusów: 15 z oczekiwanym konfliktem, 3 z konfliktem uchylalnym i 2 niejednoznaczne, bez kazusu z oczekiwanym brakiem konfliktu. Oczekiwania wymagają ponownej oceny wobec nowej bazy. Trzy testy samego mechanizmu reguł nie sprawdzają aktywnej analizy modelowej, interfejsu ani całej rozmowy.
7. W kodzie nie ma jeszcze ocen użytkownika, propozycji zmiany wiedzy, decyzji operatora ani powiązania analizy z wersją wiedzy. Istniejąca tabela historii i dziennik zdarzeń mogą posłużyć do rozbudowy, lecz nie realizują tych wymagań samodzielnie. Aktywna analiza nie zapisuje pytań uzupełniających; istniejące fragmenty obsługi odpowiedzi wymagają połączenia i sprawdzenia wieloetapowej rozmowy.

## Minimum przed środą

| Element | Zakres konieczny | Warunek odbioru |
|---|---|---|
| 1. Działające środowisko testowe | Powtarzalny lokalny start, osobne dane testowe, rzeczywiste zapytanie do modelu, kontrola czasu i błędów. | Można otworzyć aplikację, wykonać analizę i odczytać ją po ponownym uruchomieniu. Awaria nie wygląda jak zakończona ocena prawna. |
| 2. Jedna oznaczona wersja wiedzy do testów | Import odebranych kart, rozwinięcie odwołań, znaczeń i wyjątków, zachowanie statusów, różnych manifestów źródeł i not odbioru, w tym OBS-024-M02. Wersja testowa ma jawny zakres dopuszczenia przez operatora; odbiór karty nie jest automatycznym zatwierdzeniem jej jako obowiązującej wykładni. | Rekord z pytania prowadzi do właściwego fragmentu źródła. Żadne odwołanie nie ginie. Oczekująca interpretacja nie jest prezentowana jako rozstrzygnięta. |
| 3. Dobór wiedzy według problemu | Przypisanie do punktu schematu, dobór właściwego znaczenia, odczyt ograniczeń, wyjątków i materiału przeciwnego. Przegląd zakresu nie może zależeć wyłącznie od podobieństwa słów w pytaniu. | Dla kazusu wiadomo, jakie punkty sprawdzono, jakie źródła wykorzystano i czego nie zbadano. Osiągnięcie limitu odczytu pozostaje jawnym przerwaniem analizy. |
| 4. Dopytywanie i granice wyniku | Rozdzielenie faktów podanych, ustaleń warunkowych, brakujących faktów i luk wiedzy. Zachowanie wszystkich kolejnych odpowiedzi. Wyraźne rozróżnienie braku stwierdzonego konfliktu w zbadanym zakresie od dopuszczalności pomocy pod warunkami wyjątku. | Brak istotnego faktu powoduje pytanie lub ocenę warunkową. Luka wiedzy powoduje oznaczenie ograniczenia. Brak pola odpowiedzi modelu nie daje domyślnie „braku konfliktu”. |
| 5. Wynik możliwy do oceny | Wnioski, zastosowane przesłanki, fakty spełniające przesłanki, źródła, autor i status tezy, niewyjaśnione kwestie, zakres wykonanej analizy. Cytaty wyświetlane z bazy przez identyfikatory. | Użytkownik może przejść od konkretnego wniosku do konkretnego rekordu i cytatu. Nie musi odgadywać podstawy odpowiedzi modelu. |
| 6. Ocena i samodoskonalenie | Ocena wyniku i pytania uzupełniającego, komentarz, automatyczne zgłoszenie luki, rejestr propozycji, prosty widok operatora, decyzja, publikacja i przywrócenie poprzedniej wersji. Korekta faktów kazusu oddzielona od zmiany wspólnej wiedzy. | Poprawka ma pochodzenie w rozmowie. Model i zwykły tester nie publikują wiedzy. Zatwierdzona konkretna treść tworzy nową wersję; odrzucona propozycja nie zmienia odpowiedzi. |
| 7. Zestaw kontrolny i porównywanie wyników | Przykłady z oczekiwanymi przesłankami, pytaniami i źródłami, nie tylko etykietą wyniku. Porównanie odpowiedzi przed i po zmianie na tym samym zestawie. | Widać osobno błąd faktów, doboru wiedzy, zastosowania przesłanki, źródła, dopytywania i prezentacji. Historyczne odpowiedzi nie są nadpisywane. |

## Kolejność prac i ograniczenie zakresu

**Poniedziałek rano:** potwierdzić uruchomienie lokalne i jedno rzeczywiste zapytanie. Równolegle przygotować pakiet wiedzy z oznaczeniem wersji i wstępną listę przypadków kontrolnych. Już ten etap rozstrzyga, czy istniejące środowisko jest podstawą wersji środowej.

**Poniedziałek, dalsza część:** podłączyć pakiet do analizy, pokazać rzeczywiste źródła przy odpowiedzi i zapisać pierwszy kompletny przypadek. Odtworzyć i sprawdzić przejścia dla pierwszej obsługiwanej konfiguracji diagramu. Uruchomić zapisywanie rozmowy, wersji, użytych rekordów i ocen od początku, aby wtorkowe próby pozostawiały materiał do poprawy.

**Wtorek:** dopytywanie wieloetapowe, wyraźne braki i wyniki warunkowe; rejestr propozycji oraz decyzje operatora; kontrola zmiany i przywrócenia wersji. Przejść zestaw kontrolny, naprawić błędy uniemożliwiające ocenę, powtórzyć dotknięte poprawką przypadki. Wieczorem zamrozić oznaczoną wersję do testów i przygotować prostą instrukcję uruchomienia.

**Środa:** testy prowadzone przez użytkownika, oceny odpowiedzi i lista poprawek uporządkowana według wpływu na wniosek. Powtarzalne przykłady pozwalają odróżnić poprawę bazy od przypadkowej zmiany odpowiedzi modelu.

Rekomendowany zakres pierwszej wersji: cała opracowana baza dostępna do doboru materiału, a pełna ocena tylko dla jawnie wskazanych, sprawdzonych konfiguracji schematu. Dla pozostałych zakresów odpowiedź częściowa z listą nieprzeprowadzonych sprawdzeń. W pierwszej kolejności wybrać reprezentatywne przypadki relacji z aktualnym i byłym klientem, związku spraw oraz warunków wyjątków; dokładne przejścia muszą mieć odbiór przed uruchomieniem. Liczba opracowanych haseł nie jest miarą pokrycia wszystkich ścieżek analizy.

Jeżeli zabraknie czasu, ograniczamy liczbę obsługiwanych konfiguracji i rozbudowę ekranu. Zachowujemy źródła przy wnioskach, jawne luki, zapis ocen oraz kontrolowaną publikację wiedzy. Pełna wizualizacja diagramu, nowe serwery, integracja z Ekstranetem i rozbudowane wyszukiwanie podobieństwa nie są warunkiem lokalnego testu.

## Sprawdzian gotowości

Przygotować około 12–15 krótkich kazusów. Liczba jest propozycją planistyczną. Oczekiwane wyniki wymagają sprawdzenia na materiale, a kwestie otwarte mają oczekiwany brak rozstrzygnięcia, nie arbitralnie wybraną odpowiedź.

- Przypadki z uzasadnionym konfliktem, brakiem stwierdzonego konfliktu w badanym zakresie i dopuszczalnością pod warunkami.
- Przypadki z brakującym faktem oraz z luką lub rozbieżnością w samej wiedzy.
- Para opisów różniących się jednym istotnym faktem oraz ten sam opis napisany inaczej.
- Pomocnicza teza autora albo uczestnika nie może stać się rzekomym rozstrzygnięciem sądu; wyjątek zachowuje wszystkie warunki.
- Dwa kolejne doprecyzowania zachowują wcześniejsze odpowiedzi i historię wniosków.
- Nieprawidłowa lub przerwana odpowiedź modelu nie skutkuje wynikiem „brak konfliktu”.
- Sugestia testera tworzy propozycję, oczekiwanie i odrzucenie nie zmieniają wersji używanej przez analizę, a decyzja operatora i cofnięcie wersji są odtwarzalne.

Gotowość do testów nie oznacza bezbłędności każdej oceny merytorycznej. Oznacza, że można odtworzyć odpowiedź, sprawdzić jej podstawę, nazwać błąd i ocenić skutki poprawki. Zmyślone źródło, ukryty brak danych, utrata historii albo samoczynna publikacja poprawki blokują gotowość.

## Podstawa planu i granice sprawdzenia

- [Stan projektu](../STATUS_PROJEKTU.md) i [raport ostatniej partii](../baza_wiedzy/przebieg_2026-09-27_30_hasel/RAPORT.md).
- [Wymagania bazy i samodoskonalenia](PLAN_BUDOWY_BAZY.md), zwłaszcza sekcje 2, 6 i 7. Wymagania kontroli zmian obowiązują od pierwszego testu użytkowego.
- [Wykaz punktów](01_PUNKTY_SCHEMATU_I_POJECIA.md), który jawnie nie odtwarza jeszcze przejść.
- [Aktywny przebieg analizy](../aplikacja/backend/app/services/orchestrator.py), `run_analysis`, `resume_after_clarification` oraz `_build_final_from_simple`.
- [Instrukcja aktualnej analizy](../aplikacja/backend/app/adapters/prompts/simple_analysis_system.txt) i [modele zapisu](../aplikacja/backend/app/models/db_models.py).
- [Obsługa doprecyzowań](../aplikacja/backend/app/api/analysis.py), [historia w interfejsie](../aplikacja/frontend/app/history/page.tsx), [starsze kazusy](../aplikacja/tests/cases/) i [testy samego mechanizmu reguł](../aplikacja/scripts/test_rule_engine.py).
- [Stan przeniesienia aplikacji](../2026-09-21_PRZENIESIENIE_Z_VPS.md).

Przegląd dotyczy lokalnego kodu i dokumentacji. Nie uruchomiono aplikacji, nie sprawdzano kluczy, połączeń ani kont zewnętrznych, nie wywołano płatnej analizy. Nie przeprowadzono w tej turze audytu aktualności prawa. Ocena możliwości dojścia do środowych testów jest warunkowa do czasu pierwszego udanego uruchomienia i próby z nową wiedzą.

Podział pracy: dwie Luny wykonały odrębne przeglądy tylko do odczytu, backendu oraz interfejsu i testów. Astra sprawdziła istotne ustalenia w kodzie, określiła zakres minimalny, kolejność i kryteria odbioru oraz sporządziła plan. Nie zmieniano kodu aplikacji.
