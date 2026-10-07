from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
import przebieg_24 as run
registry=q.read(run.REG)
entry=next(e for e in registry['entries'] if e['id']=='RUN-2026-09-27-03-OBS-054')
entry['context_extension_record_ids']=['OBS-054-R01']
links=registry.setdefault('record_links',[])
if not any(x.get('record_id')=='OBS-054-R01' for x in links):
    links.append({'record_id':'OBS-054-R01','basis_record_ids':['SP-R01'],'relation':'ODREBNY_ZAKRES_ZASTOSOWANIA_POGLADU_AUTORA','note':'Wspólne formalne objaśnienie tożsamości, nowy zakres art.27 pkt1–6. Nie jest niezależnym potwierdzeniem ani drugą uniwersalną regułą. SP-R01 ma kontekst art.28.'})
registry['updated_at']=q.now();q.write(run.REG,registry)
q.atomic_text(run.RUN/'POWIAZANIA_ZAKRESOW.md','# Powiązania nowych zakresów z wcześniejszymi rekordami\n\nOBS-054-R01 zachowuje odrębne zastosowanie poglądu autora do art. 27 pkt 1–6 KERP. SP-R01 zawiera podobne formalne objaśnienie tożsamości sprawy w kontekście art. 28. To jeden autor i wspólne rozumienie, rozwinięte dla innego zakresu, nie dwa niezależne potwierdzenia ani dwie uniwersalne reguły. Zachowano odrębne identyfikatory, aby nie przenosić dawnej tezy poza jej przyjęty kontekst.\n\nOBS-056-R01 wyodrębnia definicje trzech kryteriów związku spraw. SP-R02 dotyczy ich alternatywnego stosowania, a SP-R03 szczególnej roli kryterium gospodarczego. Szeroki cytat SP-R03 zawiera te definicje, lecz jego przyjęta teza ich dotąd nie wyodrębniała.\n\nOBS-019-R01 jest literalną normą art. 28 ust. 2; SP-R05 pozostaje objaśnieniem autora o zakresie „jakiejkolwiek sprawy”.\n')
print('OK')
