from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['gaps'][0]['issue']='Nie ustalono jednego zdarzenia kończącego aktualną relację z klientem i pozwalającego zakwalifikować osobę jako uprzednio obsługiwaną we wszystkich konfiguracjach. Trwanie tajemnicy jest odrębne od tej zmiany statusu. Luka nie dotyczy daty wygaśnięcia statusu byłego klienta.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
