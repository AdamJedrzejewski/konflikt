"""Czytelne karty z wyników; JSON pozostaje zapisem strukturalnym."""
import json
from pathlib import Path
from urllib.parse import quote

trial = Path(__file__).resolve().parent.parent
manifest = {s['id']: s for s in json.loads((trial / '00_MANIFEST_ZRODEL.json').read_text(encoding='utf-8'))}
for name in ('01_klient', '02_sprawa', '03_osoba_najblizsza'):
    path = trial / (name + '.json')
    if not path.exists():
        continue
    d = json.loads(path.read_text(encoding='utf-8-sig'))
    out = [
        f"# Próba: {d['concept']}",
        '',
        '24.09.2026. Materiał kandydacki, oczekuje na decyzję operatora. Ekstrakcja: Luna; odbiór: Astra. Wynik odbioru i ograniczenia: [raport próby](00_WYNIK_PROBY.md).',
        '',
        d['scope'],
        '',
        '**Punkty schematu:** ' + ', '.join(d['scheme_points']),
        '',
        '## Znaczenia i konteksty',
        '',
    ]
    for m in d['meanings']:
        out += [f"### {m['id']}: {m['context']}", '', m['description'], '', 'Podstawy: ' + ', '.join(m['record_ids']) + '.', '']
    out += ['## Twierdzenia i stanowiska', '']
    for r in d['records']:
        out += [f"### {r['id']}", '', '**Twierdzenie:** ' + r['claim'], '', f"**Kto mówi:** {r['speaker']}. **Rola:** {r['role']}.", '', f"**Rodzaj zapisu:** {r['kind']}. **Ocena przez sąd:** {r['court_treatment']}.", '', '**Kontekst:** ' + r['context'], '', '**Status materiału:** ' + r['source_status'], '']
        for e in r['evidence']:
            s = manifest[e['source_id']]
            link = quote('../../../' + s['text'], safe='/')
            out += [f"Źródło {e['source_id']}, wiersze {e['line_start']}–{e['line_end']}: [tekst źródłowy]({link}).", '', '> ' + e['quote'].replace('\r\n', '\n').replace('\n', '\n> '), '']
        out += ['**Granice:** ' + r['limits'], '']
        if r['related_record_ids']:
            out += ['Powiązane stanowiska: ' + ', '.join(r['related_record_ids']) + '.', '']
    out += ['## Proponowane powiązania', '']
    for r in d['relations']:
        out += [f"- {r['from']} → {r['relation']} → {r['to']}; status: {r['status']}; podstawy: {', '.join(r['record_ids'])}."]
    out += ['', '## Braki', '']
    for g in d['gaps']:
        out += [f"- **{g['id']}:** {g['issue']} Potrzebne: {g['needed']}"]
    out += ['', '## Rejestr propozycji dla operatora', '']
    for p in d['proposals']:
        out += [f"- **{p['id']}, {p['operator_status']}:** {p['change']} Podstawy: {', '.join(p['basis_ids'])}."]
    out += ['', '## Zakres przeglądu źródeł', '', '| Źródło | Status | Przeczytany zakres | Ograniczenia |', '|---|---|---|---|']
    for c in d['coverage']:
        out.append('| ' + ' | '.join(str(c[k]).replace('|', '/').replace('\n', ' ') for k in ('source_id', 'status', 'read_ranges', 'notes')) + ' |')
    out += ['', '## Odbiór Astry', '']
    review = d.get('review', {})
    for change in review.get('changes', []):
        out.append('- ' + change)
    out += ['', review.get('limits', ''), '', 'Wyniki ćwiczeń kontrolnych i zapis samooceny wykonawcy pozostają w pliku JSON. Bieżący stan odbioru określa powyższy opis i raport próby.', '']
    (trial / (name + '.md')).write_text('\n'.join(out), encoding='utf-8')
    print(name + '.md')
