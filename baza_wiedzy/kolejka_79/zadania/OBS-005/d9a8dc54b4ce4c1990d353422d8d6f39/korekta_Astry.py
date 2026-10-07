from pathlib import Path
import json
p=Path(__file__).with_name('wynik.json');c=json.loads(p.read_text(encoding='utf-8'))
c['records'][0]['claim']=c['records'][0]['claim'].replace('dalej opis dotyczy','w tym samym akapicie opis dotyczy')
c['questions']=[dict(id='OBS-005-Q01',record_ids=['OBS-043-R01','ON-R06','OBS-005-R01'],
understanding='Norma obejmuje bliskie stosunki, lecz opis D 43/2016 nie podaje cech tej relacji. Argument autora o bliskoznaczności nie daje pozytywnego testu.',
variants='Możliwe kryteria wymagające oceny eksperta: więź emocjonalna, intensywność i trwałość kontaktu, więź ekonomiczna lub inne konkretne okoliczności. Sama znajomość albo wcześniejsza obsługa nie zostały w przejrzanym materiale uznane za kryterium wystarczające.',
consequences='Odpowiedź pozwoli odróżnić relację objętą art. 27 pkt 5 od zwykłej znajomości, bez automatycznego przenoszenia definicji osoby najbliższej lub zależności.',
question='Jakie pozytywne cechy relacji i jaki stopień jej intensywności uzasadniają określenie jej jako bliskich stosunków w art. 27 pkt 5? Jak odróżnić je od zwykłej znajomości albo wcześniejszego świadczenia pomocy prawnej?',
needed='Kryteria i przykłady graniczne dotyczące bliskich stosunków; osobno oryginał D 43/2016, jeżeli przykład ma służyć do oceny sądowej, a nie tylko opisu faktów.')]
c['gaps'].append(dict(id='OBS-005-G02',issue='Brak oryginału D 43/2016. Cytowany fragment nie wyjaśnia kwalifikacji S (2) ani wyniku w zakresie bliskich stosunków.',needed='Pełny tekst orzeczenia, jeśli ma być wykorzystany jako przykład zastosowania zakazu.'))
c['self_check']+=' Astra dopisała odrębne pytanie OBS-005-Q01 o pozytywne cechy stosunków, którego nie zawierają wcześniejsze pytania, oraz lukę oryginału D 43/2016. Cytat sprawdzono także w wewnętrznym tekście oryginalnego DOCX komentarza.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
