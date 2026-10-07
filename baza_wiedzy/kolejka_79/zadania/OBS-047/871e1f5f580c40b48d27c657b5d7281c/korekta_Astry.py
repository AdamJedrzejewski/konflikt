from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / 'narzedzia/kolejka_pojec'))
import kolejka as q
from raport_30 import authored
p = Path(__file__).with_name('wynik.json')
c = q.read(p)
c['scope'] = c['scope'].replace('Dwie nowe tezy źródłowe dotyczą ustawowych przesłanek prawa wykonywania zawodu i normy art. 26a ust. 1.', 'Trzy nowe rekordy dotyczą ochrony tytułu i wymagań ustawowych, momentu powstania prawa wykonywania zawodu oraz normy art. 26a ust. 1.')
c['scope'] = c['scope'].replace('Fragment SRC-01 w. 568 zawiera markery zmian, których nie normalizowałem ani nie cytuję.', 'Fragment SRC-01 w. 568 zawiera znaczniki komentarzy 34/35 dotyczących poprawki językowej, odczytanej przez Astrę w w. 1585–1591; nie są one źródłem sporu o kwalifikację stosunku pracy.')
c['coverage'][0]['notes'] = c['coverage'][0]['notes'].replace('w. 568 zawiera markery zmian i komentarzy w lustrze.', 'w. 568 zawiera znaczniki komentarzy redakcyjnych 34/35 o poprawności językowej, a nie skreślenie lub dodanie merytoryczne.')
c['meanings'][1]['description'] = c['meanings'][1]['description'].replace('Znaczenie materialnej sprzeczności i znacznego ryzyka pozostaje poglądem autora, z granicami i otwartym progiem zapisanym w OBS-057-R03/Q01.', 'Materialne odczytanie konfliktu i jego relacji do znacznego ryzyka zachowuje autorski status OBS-057-R03; próg ryzyka pozostaje otwarty w OBS-057-Q01. Samo znaczne ryzyko jest wymienione w normie art. 30 ust. 1.')
c['gaps'][0] = {'id':'OBS-047-G01','issue':'W tej karcie opracowano ochronę tytułu, ogólne odesłanie do wymagań ustawy i moment powstania prawa wykonywania zawodu. Nie opracowano pełnego katalogu wymagań ani dalszych zmian prawa wykonywania zawodu.','needed':'Dla pełnego opisu statusu należy osobno opracować właściwe przepisy SRC-05 o wymaganiach, ograniczeniach, zawieszeniu i skreśleniu; brak tego rozwinięcia nie zmienia odebranego mapowania pięciu punktów schematu.'}
c['gaps'][1]['issue'] = 'Art. 26a ust. 1 wymaga faktycznego wspólnego wykonywania zawodu w kancelarii. Komentarz klasyfikuje formy, lecz wskazane fragmenty nie dostarczają pełnego kryterium dla każdego układu zatrudnienia lub współpracy. Komentarze 34/35 przy w. 568 mają charakter językowy, nie stanowią odrębnej luki merytorycznej.'
c['self_check'] = c['self_check'].replace('Braki obejmują weryfikację statusu konkretnej osoby oraz zastosowanie wspólnej praktyki do konkretnych faktów.', 'Braki obejmują nieopracowane części ustawowego statusu oraz pełne kryterium wspólnej praktyki dla różnych układów współpracy. Karta nie jest ustaleniem statusu konkretnej osoby.')
q.validate_result(q.load(q.DEFAULT_STATE), q.get_job(q.load(q.DEFAULT_STATE), 'OBS-047'), c)
authored(c)
q.write(p,c)
print('OK')
