from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
m=c['meanings'][0]
m['description']=m['description'].replace('Sam status strony, osoby najbliższej, osoby mającej interes własny radcy albo osoby powiązanej z klientem nie przesądza, że spełnia ona tę alternatywę.','Na podstawie samego statusu strony, osoby najbliższej lub powiązanej z klientem nie ustalono w materiale spełnienia tej alternatywy. Własny interes radcy z art. 30 jest osobną konfiguracją. Nie zakłada się rozłączności kategorii przeciwnika i osoby zainteresowanej niekorzystnym wynikiem.')
question=c['questions'][0]
question['consequences']=question['consequences'].replace('kto poza przeciwnikiem klienta może wejść w drugą alternatywę','kto może spełniać drugą alternatywę, bez założenia, że jej zakres jest rozłączny z kategorią przeciwnika,')
question['question']=question['question'].replace(', i jak odróżnić tę kategorię od przeciwnika klienta','')
c['self_check']+=' Astra doprecyzowała brak założenia rozłączności alternatyw i usunęła z nowego pytania powtórzenie zakresu OBS-043-Q01.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
