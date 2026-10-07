import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.stdout.reconfigure(encoding='utf-8')
trial = Path(__file__).resolve().parent.parent
project = trial.parents[2]
office = project.parent
spec = importlib.util.spec_from_file_location('ekstrakcja', office / '.agents/skills/lustro/ekstrakcja.py')
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)
selected = []
for pattern in ['Dzial III*.docx', 'Wyb*.docx', 'Konflikt interesow*.pdf']:
    found = list(project.glob(pattern))
    assert len(found) == 1, (pattern, found)
    source = found[0]
    mirror = project / '_MD' / (source.name + '.md')
    if not mirror.exists():
        status, metadata = extractor.przetworz(str(source), str(mirror), str(project), SimpleNamespace(ocr=False, lang='pol+eng'))
        assert status == 'ok', (source.name, status, metadata)
    selected.append((source, mirror))
for name in ['Kodeks-Etyki-Radcy-Prawnego.md', 'Ustawa-o-radcach-prawnych.md', 'Konflikt-interesow-przepisy-zrodlowe.md']:
    source = project / name
    selected.append((source, source))
for relative in ['aplikacja/docs/legal/Orzecznictwo-WSD-konflikt-interesow.md', 'aplikacja/backend/app/adapters/prompts/glossary/01-sprawa-ta-sama-zwiazana.md', 'aplikacja/backend/app/adapters/prompts/glossary/03-klient-aktualny-vs-byly.md']:
    source = project / relative
    selected.append((source, source))
manifest = []
for i, (source, textpath) in enumerate(selected, 1):
    body = textpath.read_text(encoding='utf-8')
    manifest.append({'id': f'SRC-{i:02}', 'source': str(source.relative_to(project)).replace('\\', '/'), 'text': str(textpath.relative_to(project)).replace('\\', '/'), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'text_sha256': hashlib.sha256(textpath.read_bytes()).hexdigest(), 'lines': len(body.splitlines()), 'characters': len(body)})
    print(f'SRC-{i:02}: {textpath.name}; {len(body)} characters; {len(body.splitlines())} lines')
(trial / '00_MANIFEST_ZRODEL.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('Manifest:', trial / '00_MANIFEST_ZRODEL.json')
