from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
brief=json.loads(p.with_name('zlecenie.json').read_text(encoding='utf-8'))
src=next(s for s in brief['sources'] if s['id']=='SRC-01')
with ZipFile(Path(brief['project'])/src['source']) as z:
    root=etree.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
text='\n'.join(''.join(x.xpath('.//w:t/text()',namespaces=ns)) for x in root.xpath('//w:p',namespaces=ns))
assert c['records'][0]['evidence'][0]['quote'] in text
c['records'][0]['context']='Objaśnienie łączników przy ocenie powiązania różnych spraw, w komentarzu do art. 28 KERP.'
c['records'][0]['source_status']='Komentarz do korekty autorskiej. Nowe lustro z manifestu zachowuje oznaczenia zmian i komentarzy; nie oznacza zatwierdzenia redakcji. Astra dodatkowo potwierdziła dosłowny cytat z wiersza 924 w tekście wewnętrznym oryginalnego DOCX. SRC-01 i SRC-03 są opracowaniami tego samego autora.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p.with_name('kontrola_oryginalu_DOCX.json').write_text(json.dumps({'record':'OBS-056-R01','source':src['source'],'quote_in_original':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(c['records'][0]['context']);print(c['records'][0]['source_status'])
