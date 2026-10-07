import json
from pathlib import Path
trial=Path(__file__).resolve().parent.parent
p=trial/'01_klient.json'
d=json.loads(p.read_text(encoding='utf-8'))
m=next(x for x in d['meanings'] if x['id']=='KL-M03')
m['context']='Zagadnienia powiązane: lojalność, zgoda klienta i badanie konfliktu.'
m['description']='Wybrane rekordy wiążą klienta z obowiązkiem lojalności i ochroną jego praw, informowaniem przed uzyskaniem zgody oraz identyfikacją na potrzeby badania konfliktu. Nie stanowią odrębnej definicji klienta.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=trial/'02_sprawa.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['self_check']=d['self_check'].replace('12 rekordów','13 rekordów')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
