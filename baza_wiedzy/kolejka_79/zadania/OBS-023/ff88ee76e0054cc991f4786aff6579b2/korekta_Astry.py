import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
p=Path(__file__).with_name('wynik.json');c=q.read(p)
r=c['records'][1]
r['claim']='Autor wskazuje, że przed rozpoczęciem świadczenia pomocy badanie konfliktu należy przeprowadzić oddzielnie dla każdej osoby wspólnie wykonującej zawód. Przy wspólnym rejestrze dopuszcza jednokrotne sprawdzenie aktualnych i byłych klientów; odrębność badania osób nie oznacza więc powtarzania tego samego wyszukania.'
state=q.load(q.DEFAULT_STATE);src=next(s for s in state['sources'] if s['id']=='SRC-01')
lines=(q.PROJECT/src['text']).read_text(encoding='utf-8').splitlines()
r['evidence'].append(dict(source_id='SRC-01',line_start=608,line_end=608,quote=lines[607]))
r['limits']+=' Wspólny rejestr autor opisuje jako możliwość, a nie obowiązek jego wyboru; ograniczenia samego rejestru rozwija OBS-023-R03. Źródło regulaminowe pozostaje nieudostępnione.'
c['records'][2]['claim']=c['records'][2]['claim'].replace('wcześniejsza obsługa jednej z osób','wcześniejsze świadczenie pomocy przez jedną z osób wspólnie wykonujących zawód')
c['self_check']=c['self_check'].replace('Każdy cytat będzie pobrany','Każdy cytat pobrano')
q.write(p,c)
