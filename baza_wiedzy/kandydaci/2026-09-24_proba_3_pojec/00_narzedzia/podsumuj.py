import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import Counter
trial=Path(__file__).resolve().parent.parent
project=trial.parents[2]
office=project.parent
filenames=['01_klient','02_sprawa','03_osoba_najblizsza']
items=[json.loads((trial/(n+'.json')).read_text(encoding='utf-8-sig')) for n in filenames]
checks=json.loads((trial/'00_KONTROLA_TECHNICZNA.json').read_text(encoding='utf-8'))
assert len(checks['concepts'])==3 and not checks['errors'],checks['errors']
count=sum(len(d['records']) for d in items)
quotes=sum(len(r['evidence']) for d in items for r in d['records'])
proposals=sum(len(d['proposals']) for d in items)
report=[
'# Wynik próby trzech pojęć, 24.09.2026','',
'Przeprowadzono trzy odrębne zadania zlecone modelowi gpt-6-luna, z przygotowaniem i odbiorem przez Astrę. Jednocześnie pracowało najwyżej dwóch wykonawców. Wyniki są kandydatami po kontroli wierności lokalnym materiałom, oczekującymi na decyzję operatora.','',
f'Łącznie: **{count} zapisów, {quotes} przytoczeń źródłowych i {proposals} propozycji zmian/powiązań**. Każda karta ma zakres przeglądu wszystkich dziewięciu pozycji manifestu; duże dokumenty czytano w wybranych blokach. To ograniczona próba, nie pełne opracowanie pojęć.','',
'| Karta | Zapisy | Przytoczenia | Propozycje dla operatora |','|---|---:|---:|---:|']
for n,d in zip(filenames,items):
    report.append(f"| [{d['concept']}]({n}.md) | {len(d['records'])} | {sum(len(r['evidence']) for r in d['records'])} | {len(d['proposals'])} |")
report += ['', '## Wynik odbioru', '',
'Luna przygotowała użyteczne propozycje, lecz pierwsze wersje wymagały korekt. Część problemów usunięto w jednej rundzie uwag do wykonawcy, pozostałe poprawiła Astra. Zachowano [wyniki wykonawców](00_wyniki_luny/) przed końcowymi zmianami odbioru. Szczegóły zmian są także w polu review końcowych plików JSON.', '',
'- Klient: rozdzielono ocenę OSD, przyznanie faktów przez obwinionego oraz pogląd SN przytoczony przez OSD. Nie dopisano nieznanego stanowiska rzecznika. Doprecyzowano dowody dotyczące wyodrębnienia osiedla i sformułowania „były klient”.',
'- Sprawa ta sama lub związana: zachowano odrębność art. 27 w przykładzie wcześniejszej mediacji oraz konfiguracji art. 28–30. Przy doradztwie zachowano warunki zgody. Poprawiono zdanie, które zamiast możliwości wykorzystania tajemnicy wymagało rzeczywistego wykorzystania.',
'- Osoba najbliższa: Luna samodzielnie wskazała rozbieżność § 1/§ 11 w odesłaniu przytoczonym w wyborze orzeczeń. Zachowano ją do rozstrzygnięcia, bez poprawiania źródła. Odróżniono pogląd komentatora o bliskoznaczności relacji od definicji KERP. Brak materiału z innych instytucji prawa pozostaje luką.', '',
'Automatyczna kontrola potwierdziła zgodność wszystkich przytoczeń z podanymi wierszami (z ujednoliceniem wyłącznie konwencji końca wiersza CRLF/LF), poprawność odwołań i niezmienność plików z manifestu. Cytaty z nowych luster porównano także z tekstem wewnętrznym DOCX lub warstwą tekstową PDF. Odbiór Astry objął twierdzenia, role, konteksty i granice wybranych rekordów. Nie potwierdzano aktualności prawa ani oryginałów przywołanych orzeczeń.', '',
'Każdy wykonawca prawidłowo rozwiązał cztery krótkie ćwiczenia kontrolne: rozdzielenie obwinionego i sądu, brak wnioskowania o sądzie z samego zarzutu, rozdział kontekstów oraz pozostawienie stanowiska bez oceny. Były to jawne przykłady z briefu, a nie niezależny pomiar trafności prawnej.', '',
'## Co próba zmienia w organizacji kolejnej partii', '',
'Najważniejszy wniosek: zgodność cytatu nie wystarcza. W końcowych wynikach Luny zdarzyły się dokładne cytaty, które pomijały zdanie uzasadniające istotny element tezy. Odbiór musi osobno sprawdzać: czy cytat istnieje, czy podpiera całą tezę i czy wypowiedź należy do wskazanego autora. Dla kolejnych partii zachować rozdział pracy: Luna proponuje zapisy, Astra odbiera znaczenie i przypisanie, operator zatwierdza publikację.', '',
'Przed szerszą ekstrakcją naprawić przygotowanie komentarza Word: standardowe lustro pomija część wstawek ze zmian rejestrowanych. W tej próbie wyłączono dotknięte akapity, a wykorzystane fragmenty dodatkowo sprawdzono. Szczegóły: [jakość źródeł](00_JAKOSC_ZRODEL.md). Nie zmieniano oryginałów.', '',
'Karty pozwalają już prześledzić kandydackie powiązanie: punkt schematu → znaczenie w danym kontekście → odrębne twierdzenie → fragment materiału. Są to dane do dalszej budowy, nie działający mechanizm analizy w aplikacji. Nie mierzono kosztu tokenów ani oszczędności względem wykonania całości przez Astrę.', '',
'## Stan publikacji i samodoskonalenia', '',
f'Propozycje ({proposals}) mają status OCZEKUJE. Nie wprowadzono ich do zatwierdzonej wiedzy ani kodu aplikacji. Próba zapisuje wyniki prac agentów i propozycje w plikach. Nie wdraża jeszcze zapisu rozmów użytkowników, automatycznego wykrywania luk, panelu operatora, wersjonowanej publikacji ani cofania decyzji. Warunek tych funkcji od pierwszego testu użytkowego aplikacji nadal obowiązuje.', '',
'## Materiał kontroli', '',
'- [Zlecenie i kryteria](00_ZLECENIE_I_KRYTERIA.md).',
'- [Manifest dziewięciu pozycji](00_MANIFEST_ZRODEL.json).',
'- [Kontrola techniczna](00_KONTROLA_TECHNICZNA.json).',
'- Każda karta ma obok plik JSON ze źródłami, powiązaniami, lukami, propozycjami i uwagami odbioru.', '']
(trial/'00_WYNIK_PROBY.md').write_text('\n'.join(report),encoding='utf-8')
relative='baza_wiedzy/kandydaci/2026-09-24_proba_3_pojec/00_WYNIK_PROBY.md'
status=project/'STATUS_PROJEKTU.md'
s=status.read_text(encoding='utf-8')
s=s.replace('> **Ostatnia aktualizacja:** 23.09.2026 (doprecyzowanie głównego założenia przez użytkownika; bez ponownej weryfikacji całej aplikacji).','> **Ostatnia aktualizacja:** 24.09.2026 (próba opracowania trzech pojęć przez Lunę i odbiór Astry; bez ponownej weryfikacji całej aplikacji).')
a=s.index('**Aktualny punkt wznowienia:**')
b=s.index('\n\n',a)
s=s[:a]+f'**Aktualny punkt wznowienia:** ukończono [próbę trzech pojęć]({relative}): klient, sprawa ta sama lub związana, osoba najbliższa. Przygotowano {count} kandydackich zapisów i {proposals} propozycji oczekujących na operatora. Luna wykonała ekstrakcję, Astra sprawdziła materiał i naniosła poprawki odbioru. Zachowano wyniki wykonawców i końcowe karty. Przed następną partią potrzebne jest naprawienie lustra komentarza z rejestrowanymi zmianami; dalszy zakres można oprzeć na wykazie 46 punktów. Nie wdrożono jeszcze samodoskonalenia ani publikacji tych danych w aplikacji. Nie powtarzać migracji z VPS.'+s[b:]
line=f'- 24.09.2026: na zlecenie użytkownika wykonano próbę trzech pojęć, {count} zapisów i {proposals} propozycji. Wyniki po kontroli są kandydatami, nie zatwierdzoną bazą; szczegóły w raporcie próby.\n'
if line not in s:s+='\n'+line
status.write_text(s,encoding='utf-8')
p=project/'STAN_SPRAWY.md'
s=p.read_text(encoding='utf-8')
intro=f'**Aktualizacja 24.09.2026:** ukończono [próbę trzech pojęć]({relative}), obejmującą {count} kandydackich zapisów. Luna opracowała źródła, Astra wykonała odbiór i poprawki. Propozycje oczekują na operatora. Nie oznacza to wdrożenia bazy ani wymaganego mechanizmu samodoskonalenia w aplikacji.\n\n'
if '**Aktualizacja 24.09.2026:**' not in s:
    first,rest=s.split('\n\n',1);s=first+'\n\n'+intro+rest
p.write_text(s,encoding='utf-8')
p=project/'INDEKS_DOKUMENTOW.md';s=p.read_text(encoding='utf-8')
row=f'| 24.09.2026 | [Próba trzech pojęć]({relative}) | {count} kandydackich zapisów po odbiorze Astry; karty MD i JSON, manifest, wyniki wykonawców, kontrola i {proposals} oczekujących propozycji |\n'
anchor='| Data | Materiał | Status |\n|---|---|---|\n'
if row not in s:s=s.replace(anchor,anchor+row)
p.write_text(s,encoding='utf-8')
p=project/'dokumentacja/PLAN_BUDOWY_BAZY.md';s=p.read_text(encoding='utf-8')
if '## Próba wykonawcza 24.09.2026' not in s:
    s+=f'\n## Próba wykonawcza 24.09.2026\n\nNa zlecenie użytkownika opracowano trzy pojęcia. [Raport](../{relative}) dokumentuje {count} zapisów i {proposals} propozycji, po rundzie uwag do Luny i odbiorze Astry. Wyniki oczekują na decyzję operatora. Kontrola potwierdziła konieczność osobnego sprawdzania dosłowności cytatu, pokrycia całej tezy i atrybucji autora. Przed szerszą ekstrakcją poprawić lustro komentarza z rejestrowanymi zmianami. Próba nie zastępuje testu funkcji samodoskonalenia wymaganych w aplikacji.\n'
p.write_text(s,encoding='utf-8')
session=office/'_sesje/OBSIL/2026-09-24_proba_trzech_pojec.md'
session.write_text(f'''# Sesja 2026-09-24: próba trzech pojęć
> Katalog startowy: _KANCELARIA | Projekt: OBSIL | Agent: Codex | Skille użyte: lustro, retro (kompresja)

## 1. Cel sesji
Sprawdzić pracę Luny na trzech pojęciach według przygotowanych kryteriów, z odbiorem przez Astrę.

## 2. Decyzje użytkownika
„czy możemy w ramach testu puścić jakieś 3 pojęcia ?”. Wybrano: klient, sprawa ta sama lub związana, osoba najbliższa. Obowiązuje wcześniejsza decyzja: tylko operator zatwierdza publikację nauki w systemie.

## 3. Produkty
OBSIL/{relative} oraz trzy karty MD/JSON w tym samym folderze. {count} zapisów, {quotes} przytoczeń, {proposals} oczekujących propozycji. Manifest 9 źródeł, kontrola techniczna, jakość źródeł, zachowane wyniki wykonawców i narzędzia próby. Trzy nowe lustra w OBSIL/_MD. Zaktualizowano STATUS_PROJEKTU.md, STAN_SPRAWY.md, INDEKS_DOKUMENTOW.md i PLAN_BUDOWY_BAZY.md.

## 4. Korekty użytkownika
W tej próbie brak nowej korekty użytkownika. Poprawki odbioru Astry opisano w raporcie i polach review. Obejmowały rozdzielenie głosów, granice kontekstów, zachowanie możliwości zagrożenia oraz kompletność dowodów. Wyniki po jednej rundzie uwag do wykonawców i poprawkach prowadzącego pozostają kandydatami.

## 5. Sprawy otwarte i następny krok
Operator ocenia karty i propozycje. Przed szerszą partią poprawić ekstrakcję komentarza ze zmianami rejestrowanymi; standardowe lustro pomija wstawki. Brak pełnych oryginałów orzeczeń oraz potwierdzenia aktualności prawa. Nadal do wdrożenia zapis rozmów, rejestr propozycji, uprawnienia operatora i wersjonowana publikacja. Offline próba ekstrakcji nie oznacza pierwszego testu użytkowego aplikacji. Źródeł nie przenoszono, kodu nie zmieniano. Nie ustalono nowego terminu wobec OBSIL.

## 6. Kandydaci na lekcje
Wynik potwierdza już zapisaną L-038 i potrzebę kontroli oryginałów z lustro. Bez nowej zmiany skilla ani powielania lekcji. Szczegółową usterkę ekstrakcji zapisano jako otwarte zadanie projektu.
''',encoding='utf-8')
print(f'Raport i stan zapisane: {count} rekordów, {quotes} przytoczeń, {proposals} propozycji.')
