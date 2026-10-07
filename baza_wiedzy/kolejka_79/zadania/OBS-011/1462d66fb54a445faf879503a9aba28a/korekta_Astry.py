from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['existing_record_refs']+=['KL-R01','OBS-057-R01']
m=next(x for x in c['meanings'] if x['id']=='OBS-011-M02')
m['record_ids']+=['KL-R01','OBS-057-R01']
m['description']+=' KL-R01 identyfikuje klienta przez świadczenie na jego rzecz pomocy prawnej. OBS-057-R01 zawiera już ogólną propozycję autora rozumienia sprzeczności interesów. Nie oznacza to braku jakichkolwiek kryteriów poza obroną karną; otwarte pozostaje ich doprecyzowanie w OBS-057-Q01.'
g=c['gaps'][0];g['issue']='Istnieje ogólne objaśnienie sprzeczności w OBS-057-R01, lecz pozostają pytania o jego stosowanie oraz odrębny próg rozbieżności w kontekście obrony karnej.'
g['needed']='Wykorzystać OBS-057-R01 oraz istniejące OBS-057-Q01; karnoprocesowe OBS-030-Q01 ma węższy zakres i nie zastępuje ogólnego objaśnienia.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(m['description']);print(g)
