from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
import przebieg_24 as run
registry=q.read(run.REG)
entry=next(e for e in registry['entries'] if e['id']=='RUN-2026-09-27-03-OBS-048')
entry['supplementary_record_ids']=['OBS-048-R02']
links=registry.setdefault('record_links',[])
if not any(x.get('record_id')=='OBS-048-R02' for x in links):
    links.append(dict(record_id='OBS-048-R02',basis_record_ids=['OBS-057-R02'],relation='DOPRECYZOWANIE_POGLADU_TEGO_SAMEGO_AUTORA',note='Brak dalszej oceny materialnej w art.27 jest już zapisany w OBS-057-R02. OBS-048-R02 dodaje dosłowne objaśnienie komentarza o braku rozróżnienia konfliktu potencjalnego i aktualnego. To uzupełnienie, nie niezależna reguła ani niezależne potwierdzenie.'))
registry['updated_at']=q.now();q.write(run.REG,registry)
p=run.RUN/'POWIAZANIA_ZAKRESOW.md';s=p.read_text(encoding='utf-8')
if 'OBS-048-R02' not in s:
    s+='\nOBS-048-R02 uzupełnia OBS-057-R02. Wcześniejszy rekord poradnika obejmuje już brak odrębnej oceny materialnej przy art. 27; nowy przytacza bezpośrednie objaśnienie komentarza o braku rozróżnienia konfliktu potencjalnego i aktualnego. Rejestr oznacza go jako uzupełnienie wcześniejszego poglądu tego samego autora, nie nową samodzielną regułę. Aktywna karta i jej odbiór zachowują integralność; powiązanie po dodatkowym audycie jest zapisane tutaj oraz w metadanych rejestru.\n'
    q.atomic_text(p,s)
print('OK')
