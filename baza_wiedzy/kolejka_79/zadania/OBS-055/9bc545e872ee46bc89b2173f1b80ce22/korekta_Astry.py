from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
for row in c['coverage']:
    if row['source_id'] not in ('SRC-08','SRC-09'): row['status']='CZESCIOWY'
    if row['source_id']=='SRC-03':row['notes']='Przeczytano wykaz art. 27, w tym pkt 4, oraz ogólny opis konfiguracji przez inną osobę. W tym fragmencie nie objaśniono progu „dotyczy”. Ten sam autor co SRC-01, nie niezależna opinia.'
c['meanings'][0]['context']='Art. 27 pkt 4 KERP: sprawa dotyczy radcy prawnego, adwokata lub innej osoby wymienionej w przepisie, przy zachowaniu warunków wspólnego wykonywania zawodu, czasu i klienta.'
c['questions'][0]['needed']='Wykładnia ekspercka lub źródła bezpośrednio odnoszące się do art. 27 pkt 4. Pytanie jest odrębne od tożsamości sprawy z OBS-054-Q01 i zakresu czynności zawodowych z OBS-008-Q01. Warunki czasu i tego samego klienta także pozostają odrębne.'
c['self_check']+=' Astra usunęła nieuprawniony skrót „jego samego” z opisu kręgu osób oraz poprawiła zakres odesłania do OBS-008-Q01. Częściową lekturę długich źródeł oznaczono jednolicie.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
