import json,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
trial=Path(__file__).resolve().parent.parent
project=trial.parents[2]
manifest={s['id']:s for s in json.loads((trial/'00_MANIFEST_ZRODEL.json').read_text(encoding='utf-8'))}
texts={sid:(project/s['text']).read_text(encoding='utf-8').splitlines() for sid,s in manifest.items()}
p=trial/'03_osoba_najblizsza.json'
raw=trial/'00_wyniki_luny';raw.mkdir(exist_ok=True)
if not (raw/p.name).exists():shutil.copyfile(p,raw/p.name)
d=json.loads(p.read_text(encoding='utf-8-sig'))
r={x['id']:x for x in d['records']}
def proof(sid,a,b,q=None):
    body='\n'.join(texts[sid][a-1:b]);q=body if q is None else q
    assert q in body
    return {'source_id':sid,'line_start':a,'line_end':b,'quote':q}
for rid in ('ON-R03','ON-R04'):
    r[rid]['context']='Zakaz udzielenia pomocy prawnej z art. 27 KERP, według lokalnego tekstu.'
    r[rid]['evidence'].append(proof('SRC-04',173,173))
r['ON-R02']['speaker']='dr Paweł Skuczyński, według okładki poradnika (SRC-03, wiersz 23)'
r['ON-R09']['evidence'].append(proof('SRC-07',189,189,'KERP nie zakazuje wprost pomocy na rzecz członków rodziny, lecz musi być ona świadczona z poszanowaniem reguł kodeksu.'))
r['ON-R10']['evidence'].append(proof('SRC-04',53,53))
for rel in d['relations']:
    if rel['relation']=='ograniczane_przez_poglad_autora':rel['relation']='objasnienie_autora_do_odrebnej_oceny'
for rid in d['meanings'][0]['record_ids']:
    if not any(x['from']=='ON-M01' and x['to']==rid for x in d['relations']):
        d['relations'].append({'from':'ON-M01','relation':'wyjasniane_przez','to':rid,'status':'kandydat','record_ids':[rid]})
for point,rid in [('S1-K1-02','ON-R05'),('S1-K2-03','ON-R03'),('S1-K2-06','ON-R04')]:
    d['relations'].append({'from':point,'relation':'wymaga_pojecia_w_kontekscie','to':'ON-M01','status':'kandydat','record_ids':['ON-R01',rid]})
next(x for x in d['gaps'] if x['id']=='ON-G02')['issue']='Brak samodzielnych źródeł wyjaśniających zakres badanego pojęcia na gruncie konkretnej instytucji prawa cywilnego lub administracyjnego; nie ustalono odrębnych definicji ani tożsamości zakresów.'
next(x for x in d['proposals'] if x['id']=='ON-P03')['change']+=' Osobno rozstrzygnąć rozbieżność oznaczenia § 1 w SRC-02 i § 11 w SRC-04/SRC-07, bez automatycznej korekty źródła.'
d['control_results']['T1']['treatment_of_party']='odrzucone'
d['control_results']['T4']['court_treatment']='nieocenione'
d['review']={'reviewer':'Astra','status':'KANDYDAT_PO_KONTROLI_OCZEKUJE_OPERATORA','changes':['ON-R03 i ON-R04: doprecyzowano kontekst jako zakaz udzielenia pomocy prawnej; dodano zdanie wprowadzające art. 27.','ON-R09: dodano fragment uzasadniający obowiązek poszanowania reguł kodeksu.','ON-R10: do wykrytej przez Lunę rozbieżności oznaczeń dołączono tekst drugiego odesłania.','Nie utożsamiono poglądu autora o bliskoznaczności określeń z definicją legalną; relację nazwano objaśnieniem do oceny.','Dodano powiązania trzech punktów schematu, doprecyzowano brak materiału z innych instytucji prawa.','Odpowiedzi kontrolne Luny były znaczeniowo poprawne; ujednolicono nazwy statusów. Różnica CRLF/LF była konwencją końca wiersza, nie zmyślonym cytatem.'],'limits':'Odbiór dotyczy wierności lokalnym materiałom; bez aktualizacji prawa i bez oryginału WO–87/21.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
# Usuń nieaktualne opisy oczekiwania na kontrolę, która właśnie została wykonana.
for filename in ['01_klient.json','02_sprawa.json','03_osoba_najblizsza.json']:
    p=trial/filename;d=json.loads(p.read_text(encoding='utf-8'))
    for rec in d['records']:
        if any(e['source_id']=='SRC-01' for e in rec['evidence']):
            rec['source_status']+=' Cytat porównano z tekstem wewnętrznym DOCX w odbiorze Astry; dokument pozostaje wersją roboczą.'
        rec['limits']=rec['limits'].replace('Wybrany wiersz wymaga kontroli z XML ze względu na ograniczenia lustra.','Wybrany wiersz porównano z tekstem wewnętrznym DOCX; nie potwierdza to przyjęcia tekstu przez autora.').replace('Wiersze sąsiadujące należy porównać z XML przed zatwierdzeniem.','Wybrane cytaty porównano z tekstem wewnętrznym DOCX.')
    for cov in d['coverage']:
        cov['notes']=cov['notes'].replace('Kontrola wybranych cytatów z XML pozostaje do wykonania.','Wybrane cytaty porównano z tekstem wewnętrznym DOCX podczas odbioru Astry.').replace('Występują ślady błędów OCR/ekstrakcji.','Zachowano podziały wyrazów i wierszy warstwy tekstowej PDF.')
    for gap in d['gaps']:
        if gap['id']=='SP-G03':
            gap['issue']='SRC-01 jest wersją do korekty, a lustro pomija niektóre wstawki. Wybrane cytaty próby porównano z tekstem wewnętrznym DOCX, ale cała wersja redakcyjna wymaga pełnej, poprawionej ekstrakcji.'
            gap['needed']='Wierne lustro z rozróżnieniem zmian rejestrowanych i komentarzy przed opracowaniem całego materiału.'
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Odbiór ON i aktualizacja opisów kontroli zapisane.')
