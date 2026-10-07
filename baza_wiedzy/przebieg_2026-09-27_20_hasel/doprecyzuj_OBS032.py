from pathlib import Path
import sys
from zipfile import ZipFile
from lxml import etree
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
s=q.load(q.DEFAULT_STATE);j=q.get_job(s,'OBS-032')
p=q.DEFAULT_STATE/j['attempts'][-1]['artifact'];c=q.read(p)
src=next(x for x in s['sources'] if x['id']=='SRC-02')
quote=(q.PROJECT/src['text']).read_text(encoding='utf-8').splitlines()[67]
with ZipFile(q.PROJECT/src['source']) as archive:
    root=etree.fromstring(archive.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paragraphs=[''.join(x.xpath('.//w:t/text()',namespaces=ns)) for x in root.xpath('//w:p',namespaces=ns)]
assert any(quote in paragraph for paragraph in paragraphs), 'Cytat nie jest dosłownym fragmentem oryginału'
c['records'][2]['evidence']=[dict(source_id='SRC-02',line_start=68,line_end=68,quote=quote)]
c['records'][2]['limits']+=' Treść cytatu potwierdzono w oryginalnym DOCX wyboru. Nagłówek pozycji pozostaje lokalizacją, nie częścią cytatu.'
q.validate_result(s,j,c);q.write(p,c)
print('OBS-032: cytat pojedynczego akapitu zgodny z oryginalnym DOCX')
