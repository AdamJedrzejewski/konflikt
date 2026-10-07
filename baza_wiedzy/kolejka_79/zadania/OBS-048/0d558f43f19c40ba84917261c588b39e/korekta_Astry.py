from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['scope']=c['scope'].replace('lub świadczącej jej inną pomoc w tej sprawie','lub takiej, która wykonywała na jej rzecz inną pomoc w tej sprawie')
c['meanings'][0]['description']=c['meanings'][0]['description'].replace('Punkt zbiorczy obejmuje tu odrębną konfigurację','Dla wyznaczenia granic zbiorczej etykiety wskazano odrębną konfigurację')
c['records'][0]['source_status']=c['records'][0]['source_status'].replace('analogiczny podział/ogólny opis','analogiczny ogólny opis')
c['gaps']=[dict(id='OBS-048-G01',issue='Otwarte są wcześniej zapisane kwestie: ON-P02 o zakresie autorskiej bliskoznaczności, OBS-005-Q01 o pozytywnych cechach bliskich stosunków, OBS-058-Q01 o zależności oraz OBS-008-G01 o granicach czynności zawodowych w pkt 4. Sam fakt, że wykładnia autora oczekuje na decyzję operatora, nie tworzy nowej luki źródłowej.',needed='Rozstrzygnięcia wskazanych wcześniejszych pytań i uzupełnienie zakresów pkt 4, z zachowaniem ich odrębnych przesłanek.')]
c['self_check']+=' Astra skorygowała skrót pkt 6 do formy przeszłej i oddzieliła oczekiwanie na operatora od rzeczywistych luk. Nowe cytaty sprawdzono w tekście oryginalnego DOCX komentarza.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
