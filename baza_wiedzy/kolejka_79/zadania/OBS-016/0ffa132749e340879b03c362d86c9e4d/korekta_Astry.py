from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['scope']=c['scope'].replace('Brak tekstu art. 115 § 11 w korpusie i brak oryginału orzeczenia pozostają jawne','W dziewięciopozycyjnym manifeście nie ma odrębnego pierwotnego tekstu k.k., lecz późniejsza tabela ON-P01 zawiera pełny cytat art. 115 § 11 i dokumentuje kontrolę publikacji urzędowej z 24.09.2026; tej wykonanej kontroli nie zeruję. Brak oryginału orzeczenia pozostaje jawny')
c['gaps'][0]['issue']='W dziewięciopozycyjnym manifeście brak odrębnego pierwotnego tekstu k.k. Późniejsza tabela konsultacji ON-P01 zawiera pełny katalog z art. 115 § 11, cytat z publikacji urzędowej i kontrolę z 24.09.2026. Otwarte pozostają objaśnienia stosowania poszczególnych kategorii do faktów, nie samo istnienie tekstu definicji w materiałach projektu.'
c['gaps'][0]['needed']='Zachować późniejszą kontrolę oraz odsyłacz do publikacji urzędowej w tabeli ON-P01. W konsultacji doprecyzować kategorie wymagające przykładów, zwłaszcza powinowactwo i wspólne pożycie. Nie przedstawiać historycznej kontroli jako nowego audytu aktualności prawa.'
v=next(v for v in c['coverage'] if v['source_id']=='SRC-07');v['read_ranges']='175-190';v['notes']+=' Astra przy odbiorze przeczytała pełny fragment do wiersza 190, z otoczeniem i rozróżnieniem relacji od pierwotnego uzasadnienia.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(c['gaps'][0])
