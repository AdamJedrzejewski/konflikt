from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['meanings'][0]['description']=c['meanings'][0]['description'].replace('Literalna norma wymaga, by rozstrzygnięcie sprawy było niekorzystne dla klienta i by istniała bliska relacja radcy z osobą zainteresowaną takim wynikiem (OBS-043-R01).','Druga alternatywa normy dotyczy zainteresowania osoby niekorzystnym dla klienta rozstrzygnięciem, przy dawnych lub obecnych bliskich stosunkach radcy z tą osobą (OBS-043-R01). Opis dotyczy kierunku jej zainteresowania; nie dopisuje przesłanki faktycznego wydania niekorzystnego rozstrzygnięcia.')
c['self_check']+=' Astra poprawiła skrót M01, który mógł sugerować wymaganie już wydanego rozstrzygnięcia; zachowano zainteresowanie takim wynikiem i obie czasowe alternatywy relacji.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
