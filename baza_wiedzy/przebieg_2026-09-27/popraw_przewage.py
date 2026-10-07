from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
state=q.load(q.DEFAULT_STATE); job=q.get_job(state,'OBS-028')
path=q.DEFAULT_STATE/job['attempts'][-1]['artifact']
backup=path.with_name('wynik_przed_odbiorem.json')
if not backup.exists(): shutil.copy2(path,backup)
r=q.read(path)
source=next(s for s in state['sources'] if s['id']=='SRC-02')
line=(q.PROJECT/source['text']).read_text(encoding='utf-8-sig').splitlines()[23]
start=line.index('Celnie OSD podniósł')
end=line.index(' (…) zebrany materiał',start)
r['records'].append({'id':'OBS-028-R07','kind':'stanowisko_relacjonowane',
 'claim':'W wyborze, w fragmencie WO–31/24, przytoczono aprobatę uwagi OSD, że przy art. 25 ust. 1 i art. 26 ust. 1 nie musi dojść do naruszenia tajemnicy lub wykorzystania wiedzy od poprzedniego klienta; w opisanej sprawie za istotne uznano samo znaczne zagrożenie takiego stanu.',
 'speaker':'Głos aprobujący ocenę OSD w przytoczeniu opisanym jako WO–31/24',
 'role':'relacjonowana aprobata oceny sądu niższej instancji; przypisanie i pełne motywy wymagają oryginału',
 'context':'Przypadek pomocy BD przeciwko EK/EK2 przy wcześniejszej reprezentacji; art. 25 i 26 rozpatrywane łącznie. Początek akapitu opisuje przypisany czyn, osobno następuje aprobata uwagi OSD.',
 'court_treatment':'Przytoczenie aprobuje wskazaną uwagę OSD. Nie wywiedziono jej z samego wyniku sprawy ani z opisu zarzutu.',
 'source_status':'Wybór orzeczeń, nie pełne uzasadnienie. Kontrola cytatu z oryginałem wyboru DOCX nie zastępuje kontroli oryginału orzeczenia.',
 'evidence':[{'source_id':'SRC-02','line_start':24,'line_end':24,'quote':line[start:end]}],
 'limits':'To materiał przemawiający przeciw bezwarunkowemu wymaganiu faktycznego wykorzystania wiedzy. Nie ustala samodzielnie jednolitego progu dla każdego wariantu trzeciej przesłanki, ponieważ omawia art. 25 i 26 oraz tajemnicę łącznie. Nie przekształcono znacznego zagrożenia w dodatkowy dosłowny element ostatniej części art. 26 ust. 1.'})
r['meanings'][0]['description']='Brzmienie art. 26 ust. 1, ogólne objaśnienie autora i przytoczenie WO–31/24 przemawiają za oceną potencjalnej przewagi bez oczekiwania na faktyczne wykorzystanie wiedzy. Autor w innym akapicie opisuje wykorzystanie na niekorzyść klienta lub byłego klienta. Sam ten zwrot nie tworzy równorzędnej podstawy do wymagania udowodnionego użycia; jego znaczenie i granice można wyjaśnić z autorem.'
r['meanings'][0]['record_ids'].append('OBS-028-R07')
r['records'][5]['limits']+=' Stosowanie barier nadal podlega wyłączeniu w art. 28 ust. 2; sama zgoda ani późniejsze odseparowanie nie zastępują kontroli posiadanej wiedzy (OBS-076-R04).'
r['coverage'][2]['notes']+=' Astra skontrolowała obraz strony 25 PDF: słowa i znaki zapytania są widoczne w oryginale jako wyróżniony fragment redakcyjny.'
r['gaps'][1]['issue']='Komentarz w wierszu 464 mówi o wykorzystaniu wiedzy, podczas gdy przepis, objaśnienie w 436 i przytoczenie WO–31/24 wspierają ocenę potencjalności. Do wyjaśnienia pozostaje zamierzony zakres sformułowania autora, nie ustalona sprzeczność norm. Zapis „zorganizowania???” potwierdzono na obrazie strony 25 oryginalnego PDF; nie jest nierozstrzygniętym błędem ekstrakcji.'
r['gaps'][1]['needed']='Wyjaśnienie zamierzonego sensu słowa wykorzystanie i jego granic; ewentualnie końcowa redakcja obu opracowań autora.'
item=r['questions'][0]
item['record_ids'].append('OBS-028-R07')
item['understanding']='Tekst art. 26 ust. 1 używa „dawałaby”, komentator akcentuje zagrożenie, a przytoczenie WO–31/24 aprobuje brak potrzeby rzeczywistego wykorzystania. Sformułowanie autora w 464 o wykorzystaniu należy odczytać w tym kontekście; samo nie potwierdza odmiennej reguły.'
item['variants']='A: słowo wykorzystanie opisuje mechanizm lub możliwy skutek, przy ocenie potencjalnej przewagi; B: autor zamierzał węższy zakres wypowiedzi, który trzeba wskazać i uzasadnić. Nie przyjmować automatycznego wymogu faktycznego użycia na podstawie jednego zdania.'
item['consequences']='Wyjaśnienie pozwoli zapisać warunki oceny przed przyjęciem sprawy, bez oczekiwania na ujawnienie informacji lub wyrządzenie szkody. Materiał WO–31/24 pozostanie ograniczony do przytoczonego kontekstu, a tajemnica, przewaga i związek spraw zachowają odrębność.'
item['question']='Czy autorskie „dochodzi do wykorzystania” w wierszu 464 opisuje możliwy mechanizm przewagi, zgodnie z „dawałaby” i oceną zagrożenia, czy ma węższy zamierzony zakres? Jak zapisać tę granicę bez sugerowania ogólnego wymogu rzeczywistego użycia wiedzy?'
r['questions'].append({'id':'OBS-028-Q03','record_ids':['OBS-028-R01','OBS-028-R04','OBS-028-R06'],
 'understanding':'Korpus wiąże przewagę z wiedzą o innym kliencie i podaje przykłady organizacji przedsiębiorcy oraz kontroli dostępu. Nie podaje kompletnego kryterium odróżniającego przewagę nieuzasadnioną od zwykłego doświadczenia zawodowego.',
 'variants':'A: sformułować po uzupełnieniu źródeł test oparty na rodzaju informacji, jej związku z obsługą i przydatności przeciw innemu klientowi; B: zachować wyłącznie przykłady i otwartą ocenę indywidualną. Żaden wariant nie uzasadnia automatycznego progu liczby lat obsługi.',
 'consequences':'Rozstrzygnięcie określi, jakie fakty trzeba ustalić, aby zastosować przesłankę, oraz co można wyjaśnić na podstawie ogólnych kryteriów, a co wymaga indywidualnej oceny.',
 'question':'Jakie cechy informacji i jej znaczenia w nowej sprawie czynią przewagę „nieuzasadnioną”? Jak odróżnić taką wiedzę o innym kliencie od ogólnego doświadczenia prawnika, także przy ocenie osoby wyznaczonej w kancelarii?',
 'needed':'Źródła lub uzasadniona wykładnia kryteriów nieuzasadnienia przewagi; pełne uzasadnienia przykładów, bez zastępowania ich samym poglądem eksperta.'})
r['self_check']+=' Astra dodała R07 jako materiał istotny dla oceny potencjalności, zawęziła Q01 do wyjaśnienia języka autora, dodała Q03 o brakującym kryterium nieuzasadnienia i sprawdziła oryginalną stronę 25 PDF. Wynik po odbiorze: siedem nowych rekordów, trzy pytania.'
q.validate_result(state,job,r); q.write(path,r); print('OK')
