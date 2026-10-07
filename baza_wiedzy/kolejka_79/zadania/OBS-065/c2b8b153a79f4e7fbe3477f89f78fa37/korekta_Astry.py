from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
for row in c['coverage']:
    if row['source_id'] in ('SRC-01','SRC-03','SRC-04','SRC-06'): row['status']='CZESCIOWY'
    if row['source_id']=='SRC-02':
        row['read_ranges']='44–46; próba wyświetlenia 1–112 z uciętym wyjściem'
        row['notes']='Wykonawca potwierdził ucięcie wyjścia przy próbie wyświetlenia 1–112, więc nie deklaruje pełnej lektury. Astra osobno odczytała cały fragment 44–46 o WO–131/23, dotyczący szerokiego udziału samego radcy z pkt 1. Nie przeniesiono go na udział osoby bliskiej lub zależnej z pkt 3. Nie wyciąga się z uciętego przeglądu wniosku o braku wszystkich możliwych objaśnień w całym wyborze.'
c['gaps'][0]['issue']=c['gaps'][0]['issue'].replace('Przejrzany wybór orzeczeń nie dostarczył takiego testu.','Odczytany fragment wyboru orzeczeń dotyczy pkt 1 i nie daje testu pkt 3; pełnego wyboru nie przeczytano w tym zadaniu bez ucięcia wyjścia.')
c['meanings'][0]['context']='Art. 27 pkt 3: osoba najbliższa albo pozostająca z jakichkolwiek przyczyn w stosunku zależności z radcą brała lub bierze udział w rozstrzygnięciu sprawy.'
c['self_check']+=' Astra ujednoliciła oznaczenie częściowej lektury długich źródeł i wyraźnie zachowała przeszły oraz obecny udział osoby w opisie normy.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
