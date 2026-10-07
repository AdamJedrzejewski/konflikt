from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['scope']=c['scope'].replace('Przykład mediatora z OBS-025-R02 i SP-R13','Przykład mediatora z SP-R13').replace('Wystąpienia arbitra w art. 42 ust. 5 i art. 44a KERP','Rola arbitra w art. 42 ust. 5 i wzmianka o trybie arbitrażowym w art. 44a KERP')
c['coverage'][1]['notes']=c['coverage'][1]['notes'].replace('Nie znaleziono trafienia dotyczącego arbitra.','Fragment wymienia arbitra w przytoczeniu normy, ale nie objaśnia tej roli.')
c['meanings'][0]['description']=c['meanings'][0]['description'].replace('Inne użycia słowa arbiter w art.42 ust.5 i art.44a KERP','Rola arbitra w art.42 ust.5 i wzmianka o trybie arbitrażowym w art.44a KERP')
c['questions'][0]['consequences']=c['questions'][0]['consequences'].replace('Użycia arbitra w art.42 ust.5 i art.44a','Rola arbitra w art.42 ust.5 i wzmianka o trybie arbitrażowym w art.44a')
c['self_check']+=' Astra poprawiła odwołanie do przykładu mediatora (SP-R13, nie ogólne OBS-025-R02), rozróżniła arbitra od wzmianki o trybie arbitrażowym oraz skorygowała opis trafienia w SRC-02:46.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
