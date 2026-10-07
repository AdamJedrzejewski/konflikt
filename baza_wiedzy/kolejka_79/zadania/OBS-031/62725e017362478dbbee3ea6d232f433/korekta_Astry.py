import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
p=Path(__file__).with_name('wynik.json');c=q.read(p)
c['coverage'][0]['notes']=c['coverage'][0]['notes'].replace('Claim OBS-028-R06 i jego limits obejmują ten zakres.','OBS-028-R06 obejmuje wyznaczenie osoby oraz wymienione zasady dostępu, kontaktu i współpracy. Nie przypisuje mu się automatycznie wszystkich treści szerokiego cytatu688-732.')
c['coverage'][6]['notes']=c['coverage'][6]['notes'].replace('pytanie o próg z art. 26 należy do OBS-028-Q01.','pytanie o znaczne zagrożenie tajemnicy pozostaje w OBS-077-Q01; OBS-028-Q01 dotyczy odrębnie wykorzystania wiedzy i potencjalności przewagi.')
c['self_check']=c['self_check'].replace('który jest już ujęty w OBS-028-Q01','dotyczący znacznego zagrożenia tajemnicy, który jest już ujęty w OBS-077-Q01')
q.write(p,c)
