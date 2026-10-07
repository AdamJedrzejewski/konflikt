import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
p=Path(__file__).with_name('wynik.json');c=q.read(p)
c['scope']='Punkt S3-K6-02 uzupełniono o autorskie objaśnienie przeszkody przekazania sprawy osobie wspólnie wykonującej zawód (SRC-01:640) i o pogląd dotyczący ogólnej zgody na doradzanie przez taką grupę (644). Norma przypisania pozostaje w OBS-047-R03, a objaśnienie samego mechanizmu w OBS-023-R01. Autor w dalszym fragmencie672/680/684 wyraźnie oddziela doradztwo objęte art. 29 ust. 2 od zastosowania barier; nie przedstawiono więc braku objaśnienia w samym644 jako nowej luki całego materiału. Norma zgody i wyjątek obrońcy karnego są w SP-R07, szczególne warunki art. 26a ust. 2 w OBS-076-R04. OBS-076-Q02 o kręgu zgód i OBS-076-Q03 o rozszerzeniu na doradztwo przeciwnikowi oraz wadliwym odesłaniu pozostają odrębnymi wcześniejszymi pytaniami. Nie rozwinięto procedury dołączania nowej osoby624-636 poza punktem zlecenia. Nowych pytań nie dodano.'
c['existing_record_refs'].remove('OBS-010-R02')
c['coverage'][0]['read_ranges']='624-648; 672-684'
c['coverage'][0]['notes']+=' Astra uzupełniła kontrolę o672/680/684, które wprost objaśniają relację doradztwa do barier w poglądzie autora.'
m=c['meanings'][0];m['description']=m['description'].replace('Relacja obu ścieżek wymaga konsultacji.','Autor dalej wyraźnie odnosi doradztwo do ogólnego dopuszczenia z art. 29 ust. 2, a nie do barier. Poglądu tego nie rozszerza się na reprezentację ani pozostałe zakazy.');m['record_ids'].remove('OBS-010-R02')
r=c['records'][1]
r['claim']+=' W dalszym wyliczeniu autor nie zalicza doradztwa z art. 29 ust. 1 pkt 1-2 do stosowania barier, powołując dopuszczenie z art. 29 ust. 2.'
r['limits']='Jest to wywód autora, nie literalne brzmienie art. 29 ust. 2 ani reguła, że sama zgoda wystarcza dla każdej postaci konfliktu. Autor wyraźnie rozdziela ścieżki w672/680/684. Zgoda dotyczy doradzania objętego art. 29 ust. 1; zachowuje wyjątek osoby, która jest lub była obrońcą w sprawie karnej co najmniej jednego z zainteresowanych (SP-R07). Nie usuwa innych przeszkód z art. 26 ani nie uprawnia do reprezentacji. Szczególne warunki art. 26a ust. 2 pozostają w OBS-076-R04. Wątpliwe rozszerzenie autora na doradztwo przeciwnikowi jest już objęte OBS-076-Q03.'
state=q.load(q.DEFAULT_STATE);src=next(s for s in state['sources'] if s['id']=='SRC-01');lines=(q.PROJECT/src['text']).read_text(encoding='utf-8').splitlines()
for line in (672,680,684):r['evidence'].append(dict(source_id='SRC-01',line_start=line,line_end=line,quote=lines[line-1]))
c['questions']=[]
c['self_check']='Sprawdzono640/644 wraz z dalszym objaśnieniem672/680/684. Zachowano odrębność normy, wywodu autora oraz istniejących pytań076. Usunięto pozorne nowe pytanie o brak wyjaśnienia relacji ścieżek, ponieważ pomijało dalszy ciąg tego samego źródła. SP-R07 obejmuje normę zgody i jej wyjątek, OBS-010-R02 jest poglądem o zbiegu ról, nie normą zgody. Odbiór zakresu należy do Astry; operator pozostaje OCZEKUJE.'
q.write(p,c)
