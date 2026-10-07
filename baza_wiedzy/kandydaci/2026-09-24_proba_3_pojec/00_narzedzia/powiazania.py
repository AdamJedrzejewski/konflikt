import json
from pathlib import Path
trial=Path(__file__).resolve().parent.parent
for name in ['01_klient.json','02_sprawa.json']:
    p=trial/name
    d=json.loads(p.read_text(encoding='utf-8'))
    if name=='02_sprawa.json':
        for point in ['S1-K1-03','S1-K1-05','S2-K3-04','S2-K3-07','S2-K4-02','S2-K4-05']:
            if not any(x['from']==point and x['to']=='SP-M01' for x in d['relations']):
                d['relations'].append({'from':point,'relation':'wymaga_pojecia_w_kontekscie','to':'SP-M01','status':'kandydat','record_ids':['SP-R01']})
    for meaning in d['meanings']:
        for rid in meaning['record_ids']:
            if not any(x['from']==meaning['id'] and x['to']==rid for x in d['relations']):
                d['relations'].append({'from':meaning['id'],'relation':'wyjasniane_przez','to':rid,'status':'kandydat','record_ids':[rid]})
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
