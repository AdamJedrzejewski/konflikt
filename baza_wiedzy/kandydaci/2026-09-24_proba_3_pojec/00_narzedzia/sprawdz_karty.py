import json,re,sys
from pathlib import Path
from urllib.parse import unquote
sys.stdout.reconfigure(encoding='utf-8')
trial=Path(__file__).resolve().parent.parent
for name in ['01_klient','02_sprawa','03_osoba_najblizsza']:
    d=json.loads((trial/(name+'.json')).read_text(encoding='utf-8'))
    bad=[]
    def walk(x,path=''):
        if isinstance(x,dict):
            for k,v in x.items(): walk(v,path+'.'+k)
        elif isinstance(x,list):
            for i,v in enumerate(x): walk(v,path+f'[{i}]')
        elif isinstance(x,str) and '\u2014' in x and not path.endswith('.quote'):
            bad.append(path)
    walk(d)
    print(name,'emdash poza cytatami:',bad)
    missing=[]
    for link in re.findall(r'\]\(([^)]+)\)',(trial/(name+'.md')).read_text(encoding='utf-8')):
        if link=='00_WYNIK_PROBY.md':continue
        if not (trial/unquote(link)).resolve().exists():missing.append(link)
    print(name,'brakujące cele:',missing)
