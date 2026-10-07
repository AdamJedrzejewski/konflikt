import json
import shutil
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
trial=Path(__file__).resolve().parent.parent
project=trial.parents[2]
manifest={s['id']:s for s in json.loads((trial/'00_MANIFEST_ZRODEL.json').read_text(encoding='utf-8'))}
texts={sid:(project/s['text']).read_text(encoding='utf-8').splitlines() for sid,s in manifest.items()}
p=trial/'02_sprawa.json'
raw=trial/'00_wyniki_luny'
raw.mkdir(exist_ok=True)
if not (raw/p.name).exists(): shutil.copyfile(p,raw/p.name)
d=json.loads(p.read_text(encoding='utf-8-sig'))
r={x['id']:x for x in d['records']}
d['scope']=d['scope'].replace('Opracowano 12 atomowych rekordów','Opracowano 13 rekordów').replace('S2-K4-02 i S2-K4-05.', 'S2-K4-02, S2-K4-05 oraz S1-K2-01 (mediator).')
r['SP-R03']['claim']=r['SP-R03']['claim'].replace('Według autora kryterium gospodarczego','Według autora kryterium gospodarcze')
def proof(sid,a,b,q=None):
    body='\n'.join(texts[sid][a-1:b]); q=body if q is None else q
    assert q in body
    return {'source_id':sid,'line_start':a,'line_end':b,'quote':q}
r['SP-R07']['evidence']=[proof('SRC-04',197,203)]
r['SP-R07']['limits']='Art. 29 ust. 2 przewiduje zgodę klienta lub klientów oraz osób uprzednio obsługiwanych na warunkach wskazanych w przepisie; wyłącza możliwość jej uzyskania, gdy radca jest lub był obrońcą w sprawie karnej co najmniej jednego z nich. Tego rekordu nie wolno stosować jako bezwarunkowego zakazu ani utożsamiać doradztwa z reprezentacją. Aktualności kopii nie zweryfikowano.'
r['SP-R09']['evidence']=[proof('SRC-02',60,60,'Obwiniony przystąpił do toczącego się postępowania upadłościowego przeciw swojemu byłemu klientowi X Sp. z o.o. Zaledwie po upływie 3 miesięcy od wygaśnięcia pełnomocnictwa'),proof('SRC-02',60,60,'Skoro obwiniony jak najbardziej był pełnomocnikiem X Sp. z o.o., w której to firmie KG była prokurentem, to złożenie przez nią wniosku o upadłość X Sp. z o.o. powoduje, że jako były pełnomocnik X Sp. z o.o. występując w sprawie upadłości spółki po stronie jej przeciwnika procesowego działa w sprawie z nią związanej.')]
r['SP-R11']['claim']='Autor poradnika wskazuje, że odrębna ogólna przesłanka konfliktu związana z tajemnicą może być spełniona mimo braku tożsamości lub związku spraw, jeżeli może dojść do wykorzystania informacji objętych tajemnicą dla korzyści własnej radcy albo jego klienta.'
r['SP-R11']['context']='Odrębna przesłanka ogólna dotycząca tajemnicy zawodowej w omówieniu art. 26 ust. 1 KERP; nie przesłanka nieuzasadnionej przewagi.'
r['SP-R11']['evidence']=[proof('SRC-03',983,987)]
card=texts['SRC-08'][7]
q=card[card.index('to sprawa'):card.index('Nie jest wymagana')].strip()
r['SP-R12']['evidence']=[proof('SRC-08',8,8,q)]
r['SP-R13']['evidence']=[proof('SRC-02',42,42,'uniewinnia obwinionego od zarzucanego mu czynu'),proof('SRC-02',42,42,texts['SRC-02'][41][texts['SRC-02'][41].index('Za zgodne ze stanem faktycznym'):])]
for meaning in d['meanings']:
    if meaning['id']=='SP-M01':
        meaning['record_ids']=[x for x in meaning['record_ids'] if x!='SP-R13']
if 'S1-K2-01' not in d['scheme_points']: d['scheme_points'].append('S1-K2-01')
if not any(x['from']=='S1-K2-01' for x in d['relations']):
    d['relations'].append({'from':'S1-K2-01','relation':'wymaga_pojecia_w_kontekscie','to':'SP-M03','status':'kandydat','record_ids':['SP-R13']})
for point in ['S1-K1-03','S1-K1-05','S2-K3-04','S2-K3-07','S2-K4-02','S2-K4-05']:
    if not any(x['from']==point for x in d['relations']):
        d['relations'].append({'from':point,'relation':'wymaga_pojecia_w_kontekscie','to':'SP-M02','status':'kandydat','record_ids':['SP-R02']})
d['review']={'reviewer':'Astra','status':'KANDYDAT_PO_KONTROLI_OCZEKUJE_OPERATORA','changes':['SP-R07: dowód poszerzono o zgodę i granice wyjątku z ust. 2.','SP-R09 i SP-R13: uzupełniono cytaty o fakty potrzebne do oceny zakresu przykładów.','SP-R11: przywrócono pełny fragment zamiast dwóch urwanych wierszy; zachowano możliwość zagrożenia, nie wymóg rzeczywistego wykorzystania.','SP-R12: zachowano status roboczej karty jako tropu; przytoczenie obejmuje dokładny fragment.','SP-M01: oddzielono kontekst art. 27 od definicji komentatorskiej art. 28. Dodano kandydackie powiązania punktów schematu.'],'limits':'Odbiór wierności lokalnym materiałom nie potwierdza aktualności prawa ani oryginalnych uzasadnień.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Odbiór SP zapisany, wersja Luny zachowana.')
