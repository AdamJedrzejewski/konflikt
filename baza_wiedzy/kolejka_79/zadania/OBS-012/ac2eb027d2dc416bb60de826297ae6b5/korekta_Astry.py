from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['existing_record_refs']+=['ON-R01','ON-R08']
m=c['meanings'][1]
m['description']=m['description'].replace('zakres tej osoby wynika odrębnie z definicji art. 5 pkt 7 przyjętej w ON-R05','zakres osoby najbliższej wynika odrębnie z art. 5 pkt 7, utrwalonego w ON-R01; ON-R08 zachowuje autorskie odniesienie tej definicji do art. 30')
m['record_ids']+=['ON-R01','ON-R08']
c['scope']=c['scope'].replace('OBS-057-R01 daje ogólną definicję interesów','OBS-057-R01 objaśnia interesy w kontekście klientów')
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(m['description'])
