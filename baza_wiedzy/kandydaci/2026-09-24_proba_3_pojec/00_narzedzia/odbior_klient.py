import json
import shutil
from pathlib import Path

trial = Path(__file__).resolve().parent.parent
project = trial.parents[2]
manifest = {s['id']: s for s in json.loads((trial/'00_MANIFEST_ZRODEL.json').read_text(encoding='utf-8'))}
texts = {sid: (project/s['text']).read_text(encoding='utf-8').splitlines() for sid,s in manifest.items()}
p = trial/'01_klient.json'
raw = trial/'00_wyniki_luny'
raw.mkdir(exist_ok=True)
if not (raw/p.name).exists():
    shutil.copyfile(p,raw/p.name)
d = json.loads(p.read_text(encoding='utf-8-sig'))
r = {x['id']:x for x in d['records']}
def proof(sid,a,b,quote=None):
    body='\n'.join(texts[sid][a-1:b])
    quote=body if quote is None else quote
    assert quote in body
    return {'source_id':sid,'line_start':a,'line_end':b,'quote':quote}
r['KL-R06']['evidence'][0]=proof('SRC-02',76,76,'Obwiniona świadczyła pomoc prawną na rzecz jej klienta, którym była administracja osiedla V. W przedmiotowym stanie faktycznym osiedle należało uznać za co prawda funkcjonującą w ramach spółdzielni, ale jednak wyodrębnioną organizacyjnie i gospodarczo jednostkę.')
r['KL-R09']['evidence']=[proof('SRC-03',317,320),proof('SRC-03',328,329)]
r['KL-R12']['court_treatment']='przyjete'
r['KL-R12']['limits']+=' W relacjonowanej wypowiedzi OSD okoliczność została uznana za pozostającą poza sporem; status przyjete dotyczy wyłącznie tego faktu, nie nieprzytoczonej wykładni obwinionego.'
r['KL-R13']['source_status']='komentarz roboczy cytujący OSD D 21/20, który przytacza SN; oryginałów orzeczeń nie sprawdzono, sygnatury SN w przytoczeniu brak'
r['KL-R10']['limits']+=' Nie jest to wniosek o braku jakichkolwiek ograniczeń wynikających z innych przepisów, w szczególności przepisów o danych osobowych.'
d['scheme_points']=['S2-K3-00','S2-K4-00']
d['scope']=d['scope'].replace('dla punktu S2-K3-00','dla punktów S2-K3-00 i S2-K4-00')
d['coverage'][2]['read_ranges']=d['coverage'][2]['read_ranges'].replace('linie 9-17 (tytuł, autor i rodzaj opracowania)','linie 19-23 (tytuł, autor i rodzaj opracowania)')+' Odbiór Astry objął również wiersze 317-329.'
d['records']=sorted(d['records'],key=lambda x:x['id'])
for point, meaning, bases in [('S2-K3-00','KL-M01',['KL-R01']),('S2-K4-00','KL-M02',['KL-R04','KL-R09'])]:
    if not any(x['from']==point for x in d['relations']):
        d['relations'].append({'from':point,'relation':'wymaga_pojecia_w_kontekscie','to':meaning,'status':'kandydat','record_ids':bases})
d['review']={'reviewer':'Astra','status':'KANDYDAT_PO_KONTROLI_OCZEKUJE_OPERATORA','changes':['KL-R06: poszerzono dowód o organizacyjne i gospodarcze wyodrębnienie osiedla.','KL-R09: dodano brakujący fragment o równoważności terminu z kolejnej strony PDF; sam test zgodności cytatu nie wykrywał luki uzasadnienia.','KL-R12: przyznany fakt oznaczono jako przyjęty w relacjonowanej wypowiedzi OSD, bez przypisywania obwinionemu wykładni prawnej.','KL-R10: doprecyzowano, że pogląd o samym KERP nie wyklucza ograniczeń z innych przepisów.','Dodano powiązania dwóch punktów schematu z opracowanymi kontekstami.'],'limits':'Odbiór dotyczy wierności wybranym lokalnym materiałom; nie potwierdza aktualności prawa ani treści oryginałów orzeczeń.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Odbiór KL zapisany, wynik Luny zachowany w 00_wyniki_luny.')
