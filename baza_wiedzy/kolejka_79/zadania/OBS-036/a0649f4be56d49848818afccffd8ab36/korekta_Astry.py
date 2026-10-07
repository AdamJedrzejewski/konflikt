from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
from raport_30 import authored
p=Path(__file__).with_name('wynik.json'); c=q.read(p)
c['scope']=c['scope'].replace('warunki tej samej sprawy dotyczącej osoby','warunki dotyczące sprawy odnoszącej się do osoby')
c['records'][1]['claim']=c['records'][1]['claim'].replace('spośród wymienionych zawodów, w tym prawników zagranicznych', 'spośród radców prawnych, adwokatów, rzeczników patentowych, doradców podatkowych lub prawników zagranicznych')
state=q.load(q.DEFAULT_STATE);q.validate_result(state,q.get_job(state,'OBS-036'),c);authored(c);q.write(p,c)
print('OK')
