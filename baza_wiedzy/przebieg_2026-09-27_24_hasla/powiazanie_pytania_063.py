from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
import przebieg_24 as run
registry=q.read(run.REG)
entry=next(e for e in registry['entries'] if e['id']=='RUN-2026-09-27-03-OBS-063')
entry['refinement_question_ids']=['OBS-063-Q01']
links=registry.setdefault('question_links',[])
if not any(x.get('question_id')=='OBS-063-Q01' for x in links):
    links.append(dict(question_id='OBS-063-Q01',basis_question_ids=['OBS-008-Q01'],relation='DOPRECYZOWANIE_WCZESNIEJSZEGO_PYTANIA',note='OBS-008-Q01 pyta głównie o rodzaj czynności, ale obejmuje też znaczenie tego samego czasu i klienta. OBS-063-Q01 rozwija szczegółowo czasowy podproblem. Odpowiedź skoordynować, bez podwójnego naliczania nowego zagadnienia.'))
registry['updated_at']=q.now();q.write(run.REG,registry)
p=run.RUN/'POWIAZANIA_ZAKRESOW.md';s=p.read_text(encoding='utf-8')
if 'OBS-063-Q01' not in s:
    s+='\nOBS-063-Q01 rozwija czasowy podproblem wcześniejszego OBS-008-Q01. Starsze pytanie koncentruje się na rodzaju czynności zawodowych, lecz wprost pyta także o znaczenie tego samego czasu i klienta. Skróty w kartach 055/063 i notatkach odbioru nie wyczerpują tego szerszego pytania. Rejestr oraz końcowa konsultacja wiążą oba zapisy; nowy zapis jest doprecyzowaniem, nie nowym niezależnym problemem.\n'
    q.atomic_text(p,s)
print('OK')
