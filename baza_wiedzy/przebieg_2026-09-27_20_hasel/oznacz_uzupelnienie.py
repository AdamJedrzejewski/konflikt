from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
import przebieg_20 as run
registry=q.read(run.REG)
entry=next(e for e in registry['entries'] if e['id']=='RUN-2026-09-27-02-OBS-018')
assert 'OBS-018-R05' in entry['accepted_record_ids']
link={'from':'OBS-018-R05','to':'ON-R09','relation':'uzupelnienie_dokumentacyjne',
 'decision_by':'Astra','decision_at':q.now(),
 'basis':'ON-R09 opisuje ogólną tezę wtórnego opracowania o pomocy rodzinie i naruszeniu niezależności. OBS-018-R05 dodaje konkretną konfigurację darowizny, córki i wnuka oraz wzmiankę o zainteresowaniu radcy, z bliższego źródła SRC-02:112. Nie liczy się go jako nowej samodzielnej reguły.',
 'limits':'Powiązanie nie potwierdza prawdziwości ogólnej tezy ON-R09 ani jej przyjęcia przez sąd. Brak pełnego oryginału. Oryginalne karty i ich historyczne odwołania pozostają zachowane.'}
entry['supplementary_record_ids']=['OBS-018-R05']
registry.setdefault('record_links',[])
registry['record_links']=[x for x in registry['record_links'] if x.get('from')!='OBS-018-R05']+[link]
registry['updated_at']=q.now();q.write(run.REG,registry)
q.write(run.RUN/'powiazania_uzupelnien.json',[link])
q.atomic_text(run.RUN/'UZUPELNIENIA.md','# Uzupełnienia wcześniejszych opisów\n\nOBS-018-R05 → ON-R09: '+link['basis']+'\n\n'+link['limits']+'\n\nW drugiej partii przyjęto 36 nowych identyfikatorów rekordów: 35 nowych rekordów oraz jedno uzupełnienie dokumentacyjne. Licznik identyfikatorów nie oznacza 36 całkowicie nowych tez prawnych. Decyzja klasyfikacyjna odbioru nie jest zatwierdzeniem operatora.\n')
print('OBS-018-R05 powiązano z ON-R09 jako uzupełnienie dokumentacyjne')
