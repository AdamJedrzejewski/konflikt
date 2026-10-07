from pathlib import Path
import sys
import shutil
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'narzedzia/kolejka_pojec'))
import kolejka as q
state = q.load(q.DEFAULT_STATE)
job = q.get_job(state, 'OBS-076')
path = q.DEFAULT_STATE / job['attempts'][-1]['artifact']
backup = path.with_name('wynik_przed_odbiorem.json')
if not backup.exists(): shutil.copy2(path, backup)
r = q.read(path)
sources = {s['id']: (q.PROJECT / s['text']).read_text(encoding='utf-8-sig').splitlines() for s in state['sources']}
records = {x['id']: x for x in r['records']}
for c in r['coverage']:
    if c['source_id'] == 'SRC-03':
        c['notes'] = 'Poradnik P. Skuczyńskiego, opracowanie wtórne. Wskazuje ustność i rekomenduje co najmniej formę dokumentową. Astra skontrolowała obraz strony 30 PDF: zapis „ustanej” występuje w oryginale jako literówka; rekomendacja dokumentowa jest czytelna.'
a = records['OBS-076-R03']
a['source_status'] = 'Lokalne lustro PDF, fragment sprawdzony wzrokowo przez Astrę na stronie 30; literówka „ustanej” występuje w oryginale.'
a['evidence'][0]['quote'] = '\n'.join(sources['SRC-03'][1174:1178])
a['limits'] = 'Zachowano dosłowny zapis „ustanej”, potwierdzony na obrazie PDF jako literówka źródła. Poradnik tego samego autora co SRC-01 nie jest niezależnym stanowiskiem. Rekomendacja dokumentowa różni się od rekomendacji pisemnej w SRC-01.'
records['OBS-076-R04']['evidence'][0]['quote'] = sources['SRC-04'][170]
b = records['OBS-076-R05']
b['claim'] = 'W selekcji WO–122/23 przypisano WSD stanowisko, że uniknięcie deliktu z art. 29 wymaga łącznie uprzedniego osobistego poinformowania o istocie i źródłach konfliktu, skutkach, zagrożeniach i alternatywach oraz uzyskania zgody przed doradztwem. Relacja dotyczy czynów z lat 2017–2018, z powołaniem dawnego art. 29 ust. 3; nie ustala aktualnego wymogu pisemności.'
b['context'] = 'Jednoczesne doradzanie w transakcji JM oraz spółek Z i V, lata 2017–2018. Selekcja opisuje brak pisemnej informacji i pisemnej zgody, następnie stanowisko WSD. Odesłania do ówczesnego art. 29 nie wolno przenosić bezpośrednio na późniejszy tekst KERP.'
b['limits'] = 'Źródło wtórne zawiera opuszczenia (…) i nie zastępuje pełnego uzasadnienia. Czyny z lat 2017–2018 kwalifikowano m.in. według art. 29 ust. 3; w lokalnym późniejszym tekście ustęp ten jest uchylony. Opis historycznego braku pisemnej zgody nie dowodzi obecnego powszechnego wymogu pisemności.'
line = sources['SRC-02'][101]
first = line.index('Wyższy Sąd Dyscyplinarny w zasadzie')
last = line.index(' Elementów takiego postępowania', first)
b['evidence'] = [{'source_id': 'SRC-02', 'line_start':102,'line_end':102,'quote':line[first:last]},
    {'source_id':'SRC-02','line_start':100,'line_end':100,'quote':sources['SRC-02'][99]},
    {'source_id':'SRC-02','line_start':102,'line_end':102,'quote':line[line.index('w okresie nie później'):line.index(', jednocześnie reprezentowała')]},
    {'source_id':'SRC-02','line_start':102,'line_end':102,'quote':'określony w art. 25 ust. 1 w zw. z art. 29 ust. 1 pkt 1, ust. 2 i ust. 3 KERP'}]
records['OBS-076-R06']['limits'] = records['OBS-076-R06']['limits'].replace('ustawowym wyjątkiem', 'wyjątkiem KERP')
for rel in r['relations']:
    if rel['to'] == 'OBS-076-R06': rel['relation'] = 'zakres_autorskiej_wykladni_do_konsultacji'
r['self_check'] = 'Luna opracowała częściową kartę i zgłosiła braki. Astra sprawdziła treść, przejęła końcową korektę zapisu cytatów i kodowania, zweryfikowała obraz strony 30 PDF, rozdzieliła historyczną formę zgody od późniejszego KERP. Sześć nowych rekordów, trzy pytania. Pozostają G01–G04; status operatora OCZEKUJE. Formalny odbiór zawiera odbior.json.'
for record in r['records']:
    for ev in record['evidence']:
        fragment = '\n'.join(sources[ev['source_id']][ev['line_start']-1:ev['line_end']])
        if ev['quote'] not in fragment: print('Niezgodny cytat', record['id'], ev['line_start'])
q.validate_result(state, job, r)
q.write(path, r)
print('OK')
