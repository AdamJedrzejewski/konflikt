from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
backup=p.with_name('wynik_przed_odbiorem.json')
if not backup.exists(): backup.write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
candidate=next(r for r in c['records'] if r['id']=='OBS-009-R02')
p.with_name('material_poza_zakresem.json').write_text(json.dumps(dict(status='NIEODEBRANY_NIENALICZONY',reason='Badanie konfliktu z byłym klientem i retencja, poza art.27 pkt5. Do oceny przy właściwym zakresie; nie przenosić terminu na relacje osobiste.',source_candidate=candidate),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c['records']=[]
c['existing_record_refs']+=['KL-R10']
c['scope']='S1-K2-05 odpowiada art. 27 pkt 5 KERP: tekst mówi „był albo pozostaje w bliskich stosunkach” z przeciwnikiem klienta lub osobą zainteresowaną niekorzystnym dla klienta rozstrzygnięciem (OBS-043-R01). Zachowuję obie alternatywy czasowe, bez dopisywania terminu ani skutku samego zerwania kontaktu. OBS-005-Q01 dotyczy pozytywnych cech relacji, nie czasu po jej ustaniu. KL-R10 dotyczy badania konfliktu z byłym klientem, więc nie wyznacza granic dawnej relacji osobistej. Fragment o retencji w SRC-01:1464 jest odrębnym kontekstem, zachowanym poza kartą jako materiał do późniejszej oceny; nie stanowi nowego rekordu tej karty ani terminu z art. 27 pkt 5. Karta częściowa z powodu nierozstrzygniętego znaczenia dawnej relacji po jej ustaniu.'
m=c['meanings'][0]
m['description']='Norma wymienia stosunki, w których radca był albo pozostaje (OBS-043-R01), bez wskazania okresu w latach. Brak liczby w tekście nie zastępuje wykładni znaczenia dawnej relacji. Nie utożsamiam tej kwestii z ustaniem aktualnej obsługi klienta ani z retencją danych. KL-R10 dotyczy innej konfiguracji. OBS-005-Q01 pyta o cechy bliskości; OBS-009-Q01 osobno o czas i znaczenie ustania takiej relacji.'
m['record_ids']=['OBS-043-R01','KL-R10']
c['gaps'][0]['issue']='Przejrzane źródła nie objaśniają znaczenia upływu czasu lub zerwania kontaktu dla alternatywy „był” w art. 27 pkt 5. Kwestia jest odrębna od pozytywnych cech bliskości i od badania konfliktu z byłym klientem.'
question=c['questions'][0]
question['record_ids']=['OBS-043-R01']
question['question']='Jak rozumieć słowo „był” w art. 27 pkt 5 po ustaniu bliskich stosunków: czy wystarcza wcześniejsze istnienie kwalifikowanej bliskości niezależnie od upływu czasu, czy znaczenie ma jej czasowy lub funkcjonalny związek z aktualną sprawą? Jak traktować zakończenie kontaktów, bez utożsamiania tej kwestii z końcem obsługi klienta lub retencją danych?'
c['self_check']='Astra usunęła R01 jako duplikat KL-R10 i wyłączyła R02 o retencji poza zakres tej karty. Materiał wyjściowy zachowano w jawnie oznaczonej kopii sprzed odbioru i pliku material_poza_zakresem.json, bez wpisu nowych rekordów do rejestru. Aktywna karta zawiera mapowanie art.27 pkt5 i jedno nowe pytanie o czas dawnej relacji, odrębne od OBS-005-Q01. Pokrycie opisuje rzeczywiście przejrzane zakresy, także odróżniające konteksty.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
