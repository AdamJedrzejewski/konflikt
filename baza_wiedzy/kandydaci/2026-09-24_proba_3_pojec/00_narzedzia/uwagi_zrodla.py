import json
import sys
import zipfile
from pathlib import Path
from lxml import etree
import fitz

sys.stdout.reconfigure(encoding='utf-8')
trial = Path(__file__).resolve().parent.parent
project = trial.parents[2]
manifest = json.loads((trial / '00_MANIFEST_ZRODEL.json').read_text(encoding='utf-8'))
w = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(project / manifest[0]['source']) as z:
    comments = etree.fromstring(z.read('word/comments.xml'))
    for c in comments:
        print('COMMENT', c.get('{' + w['w'] + '}id'), ''.join(c.xpath('.//w:t/text()', namespaces=w)))
    root = etree.fromstring(z.read('word/document.xml'))
    for n, p in enumerate(root.xpath('//w:p', namespaces=w), 1):
        if p.xpath('.//w:ins|.//w:del', namespaces=w):
            print('REVISION paragraph', n, ''.join(p.xpath('.//w:t/text()', namespaces=w))[:700])
with fitz.open(project / manifest[2]['source']) as pdf:
    pdf[1].get_pixmap(matrix=fitz.Matrix(0.8, 0.8)).save(trial / '00_narzedzia/pdf_strona_2.png')
