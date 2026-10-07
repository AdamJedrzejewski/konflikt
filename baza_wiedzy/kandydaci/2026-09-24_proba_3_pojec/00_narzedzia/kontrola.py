"""Kontrola techniczna próby; nie zastępuje kontroli prawniczej."""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree
import fitz

sys.stdout.reconfigure(encoding='utf-8')
TRIAL = Path(__file__).resolve().parent.parent
PROJECT = TRIAL.parents[2]
manifest = json.loads((TRIAL / '00_MANIFEST_ZRODEL.json').read_text(encoding='utf-8-sig'))
sources = {s['id']: s for s in manifest}
texts = {s['id']: (PROJECT / s['text']).read_text(encoding='utf-8-sig') for s in manifest}
W = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
originals = {}
original_blocks = {}
quality = []
errors = []

def normal(s):
    return re.sub(r'\s+', ' ', s).strip()

for s in manifest:
    for key in ('source', 'text'):
        if hashlib.sha256((PROJECT / s[key]).read_bytes()).hexdigest() != s[key + '_sha256']:
            errors.append(f"Zmiana źródła: {s['id']} {key}")
    path = PROJECT / s['source']
    if path.suffix == '.docx':
        with zipfile.ZipFile(path) as z:
            root = etree.fromstring(z.read('word/document.xml'))
            paragraphs = [''.join(p.xpath('.//w:t/text()', namespaces=W)) for p in root.xpath('//w:p', namespaces=W)]
            originals[s['id']] = normal('\n'.join(paragraphs))
            blocks = []
            for index, p in enumerate(root.xpath('//w:p', namespaces=W), 1):
                blocks.append({'paragraph': index, 'text': normal(''.join(p.xpath('.//w:t/text()', namespaces=W))), 'insertions': len(p.xpath('.//w:ins', namespaces=W)), 'deletions': len(p.xpath('.//w:del', namespaces=W)), 'comments': len(p.xpath('.//w:commentRangeStart', namespaces=W))})
            original_blocks[s['id']] = blocks
            notes = {}
            for kind in ('footnotes', 'endnotes', 'comments'):
                part = f'word/{kind}.xml'
                if part in z.namelist():
                    node = etree.fromstring(z.read(part))
                    notes[kind] = {'elements': len(node), 'text_chars': len(' '.join(node.xpath('//w:t/text()', namespaces=W)))}
            quality.append({'source': s['id'], 'paragraphs': len(paragraphs), 'insertions': len(root.xpath('//w:ins', namespaces=W)), 'deletions': len(root.xpath('//w:del', namespaces=W)), 'extra_parts': notes})
    elif path.suffix == '.pdf':
        with fitz.open(path) as doc:
            blocks = [{'page': p.number + 1, 'text': normal(p.get_text())} for p in doc]
            original_blocks[s['id']] = blocks
            originals[s['id']] = normal('\n'.join(p.get_text() for p in doc))
            quality.append({'source': s['id'], 'pages': len(doc), 'empty_text_pages': [b['page'] for b in blocks if not b['text']]})

valid_points = set(re.findall(r'\bS[123]-K\d-\d\d\b|\bW-0[12]\b', (PROJECT / 'dokumentacja/01_PUNKTY_SCHEMATU_I_POJECIA.md').read_text(encoding='utf-8')))
checks = []
for filename in ('01_klient.json', '02_sprawa.json', '03_osoba_najblizsza.json'):
    path = TRIAL / filename
    if not path.exists():
        continue
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    local = []
    def fail(msg):
        local.append(msg)
    ids = [r['id'] for key in ('meanings', 'records', 'gaps', 'proposals') for r in data[key]]
    if len(ids) != len(set(ids)):
        fail('Powtórzony identyfikator')
    record_ids = {r['id'] for r in data['records']}
    if {c['source_id'] for c in data['coverage']} != set(sources):
        fail('Niepełne pokrycie manifestu')
    if not set(data['scheme_points']) <= valid_points:
        fail('Nieznany punkt schematu')
    evidence_checks = []
    for r in data['records']:
        if not r['evidence']:
            fail(r['id'] + ': brak dowodu')
        if not set(r['related_record_ids']) <= record_ids:
            fail(r['id'] + ': nieznane odsyłacze')
        for e in r['evidence']:
            lines = texts[e['source_id']].splitlines(keepends=True)
            a, b = e['line_start'], e['line_end']
            excerpt = ''.join(lines[a-1:b])
            exact = isinstance(a, int) and isinstance(b, int) and 1 <= a <= b <= len(lines) and bool(e['quote']) and e['quote'].replace('\r\n', '\n') in excerpt
            if not exact:
                fail(r['id'] + ': cytat/wiersze niezgodne: ' + e['source_id'])
            orig_ok = None
            locations = []
            if e['source_id'] in originals:
                orig_ok = normal(e['quote']) in originals[e['source_id']]
                if not orig_ok:
                    fail(r['id'] + ': brak cytatu w tekście oryginału po ujednoliceniu białych znaków')
                for block in original_blocks[e['source_id']]:
                    if normal(e['quote']) in block['text']:
                        locations.append({k: v for k, v in block.items() if k != 'text'})
            evidence_checks.append({'record': r['id'], 'source': e['source_id'], 'exact_in_mirror': exact, 'original_text_match': orig_ok, 'original_locations': locations})
    for m in data['meanings']:
        if not set(m['record_ids']) <= record_ids:
            fail(m['id'] + ': nieznane rekordy')
    for r in data['relations']:
        if r['from'] not in set(ids) | valid_points or r['to'] not in set(ids) | valid_points:
            fail('Relacja do nieznanej jednostki: ' + str(r))
        if not set(r['record_ids']) <= record_ids:
            fail('Relacja bez poprawnych rekordów')
    for p in data['proposals']:
        if p['operator_status'] != 'OCZEKUJE' or not set(p['basis_ids']) <= set(ids) | valid_points:
            fail(p['id'] + ': niepoprawny status lub podstawa')
    c = data['control_results']
    if c['T1']['treatment_of_party'] not in {'odrzucone', 'odrzucono', 'Pogląd obwinionego został odrzucony.'}:
        fail('T1: nieprawidłowa ocena poglądu obwinionego')
    if c['T2']['court_claim_confirmed'] is not False or c['T2']['prosecutor_view_available'] is not False:
        fail('T2: niedopuszczalna atrybucja')
    if c['T3']['merge_definitions'] is not False:
        fail('T3: scalono konteksty')
    if c['T4']['court_treatment'] not in {'nieocenione', 'pozostawiono bez oceny'} or c['T4']['prosecutor_view_available'] is not False:
        fail('T4: nieprawidłowy status')
    checks.append({'file': filename, 'records': len(data['records']), 'errors': local, 'evidence': evidence_checks})
    errors.extend(filename + ': ' + e for e in local)
report = {'source_quality': quality, 'concepts': checks, 'errors': errors, 'scope': 'Kontrola techniczna. Zgodność tekstu z XML/PDF nie potwierdza autorstwa, znaczenia ani aktualności prawa.'}
(TRIAL / '00_KONTROLA_TECHNICZNA.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'quality': quality, 'concepts': [{'file': c['file'], 'records': c['records'], 'errors': c['errors']} for c in checks], 'errors': errors}, ensure_ascii=False, indent=2))
