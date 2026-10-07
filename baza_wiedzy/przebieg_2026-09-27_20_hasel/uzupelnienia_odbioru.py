"""Jawne drobne korekty przy odbiorze; kopia wyniku sprzed korekty pozostaje obok."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
cid=sys.argv[1]
s=q.load(q.DEFAULT_STATE); j=q.get_job(s,cid)
p=q.DEFAULT_STATE/j['attempts'][-1]['artifact']; c=q.read(p)
backup=p.with_name('wynik_przed_odbiorem.json')
assert not backup.exists()
q.write(backup,c)
if cid=='OBS-040':
    question=c['questions'][0]
    question['variants']=question['variants'].replace('czynności prawnej świadczonej dla klienta','czynności wykonywanej dla klienta')
    question['variants'] += ' Wariant B wymaga rozróżnienia samej pomocy prawnej od czynności z nią związanych lub jej podporządkowanych; sam związek nie jest tu przyjęty jako dowód tożsamości.'
    question['consequences']='A skupia ocenę na treści czynności; B dodaje kontekst usługi i wymaga zachowania granicy między samą pomocą a działalnością z nią związaną; C pozostawia kwalifikację otwartą. Żadnego wariantu nie przyjęto jako rozstrzygnięcia.'
elif cid=='OBS-039':
    c['scope']=c['scope'].replace('udzielała jej innej pomocy prawnej','udzielała jej w tej sprawie innej pomocy prawnej')
    c['meanings'][0]['description']=c['meanings'][0]['description'].replace('pełnomocnik jest odrębną od doradcy kategorią czynności zawodowej','działanie jako pełnomocnik stanowi kategorię czynności odrębną od doradztwa')
elif cid=='OBS-030':
    c['records'][1]['claim']='Autor komentarza, na podstawie omówionego w literaturze orzecznictwa, wymienia sprzeczności w wyjaśnieniach, treściach wynikających z dowodów, twierdzeniach we wnioskach i możliwych skutkach dowodów, ocenach dowodów oraz poglądach na prawo, a także sprzeczność wynikającą z odmiennej sytuacji w zakresie środków zapobiegawczych.'
    c['questions'][0].update(
      record_ids=['OBS-030-R02','SP-R04'],
      understanding='Autor wymienia postacie sprzeczności przy obronie kilku oskarżonych, w tym w twierdzeniach ubocznych lub z różnych etapów. Sam katalog nie objaśnia sposobu odróżnienia rozbieżności od sprzeczności interesów w konkretnym układzie obrony.',
      variants='A: kategorie autora służą wykrywaniu sytuacji wymagających dalszej oceny niemożności pogodzenia interesów. B: stwierdzenie sprzeczności w jednej z wymienionych kategorii wystarcza do przyjęcia konfliktu, bez odrębnego wykazania skutku dla strategii obrony. Nie utożsamiamy samej różnicy wypowiedzi ze stwierdzoną sprzecznością.',
      consequences='Odpowiedź określi, czy zakwalifikowanie stanu faktycznego do jednej z kategorii kończy ocenę konfliktu, czy wymaga dalszego ustalenia wpływu na interesy poszczególnych oskarżonych. Nie przyjęto żadnego wariantu.',
      question='Jak na tle sześciu kategorii autora odróżniać samą rozbieżność od sprzeczności interesów, zwłaszcza przy twierdzeniach ubocznych lub z różnych etapów postępowania, i czy po stwierdzeniu jednej z tych postaci potrzebna jest dalsza ocena wpływu na interesy bronionych osób?',
      needed='Stanowisko eksperta i wskazane przezeń źródła dla praktycznego progu sprzeczności. Pełny art. 85 k.p.k. i orzeczenia z omówienia pozostają osobnym brakiem źródłowym.')
elif cid=='OBS-069':
    c['records'][0]['claim']='Art. 42 ust. 1 KERP zakazuje radcy świadczącemu pomoc osobie prawnej na podstawie umowy o pracę albo umowy o stałą pomoc utożsamiania jej interesu z interesami jej organów, ich członków i podmiotów grupy. Ust. 2 przewiduje wskazanie organów i osób upoważnionych do uzyskiwania stanowiska i wyrażania zgody. Ust. 3 pozwala umownie przewidzieć czynności na rzecz innych klientów grupy, z określonymi w nim zastrzeżeniami, oraz uwzględnianie interesu grupy obok interesu klienta. Ust. 6 nakazuje odpowiednio stosować ust. 1-5 do jednostki niebędącej osobą prawną.'
    c['records'][0]['limits'] += ' Czynności dla innych klientów grupy nie mogą naruszać form wykonywania zawodu, ograniczać niezależności, stwarzać zagrożenia naruszenia tajemnicy lub ryzyka konfliktu interesów ani uchybiać godności zawodu. Uwzględnianie interesu grupy następuje obok interesu klienta. Warunki dotyczące umowy o pracę lub stałej pomocy zapisane są w ust. 1; nie formułuje się tu odrębnej wykładni ich przeniesienia na pozostałe ustępy.'
    c['questions'][0].update(
      understanding='Art. 42 rozdziela interes osoby prawnej, organów i grupy. Upoważnienie do kontaktu i otrzymywania stanowisk oraz ustalenie beneficjenta pomocy są odrębnymi elementami. Pozostaje granica między działaniem osoby jako organu klienta a pomocą świadczoną tej osobie na jej własną rzecz.',
      variants='A: kwalifikację relacji oprzeć przede wszystkim na uzgodnionym adresacie i zakresie pomocy. B: rozstrzygające znaczenie nadać rzeczywistemu adresatowi i treści wykonanych czynności. C: wymagać łącznej oceny tych elementów, a rozbieżność między umową i wykonaniem ujmować jako nieustalony zakres relacji.',
      consequences='Odpowiedź wyznaczy kryteria odróżnienia działania w imieniu klienta-osoby prawnej od indywidualnej pomocy członkowi organu lub podmiotowi grupy. Ma to znaczenie dla wskazania osób objętych badaniem konfliktu; samo upoważnienie lub przynależność do grupy nie zostały przyjęte jako wystarczająca podstawa.',
      question='Jakimi kryteriami odróżniać udzielenie stanowiska osobie działającej jako organ lub upoważniony kontakt klienta od pomocy świadczonej jej na własną rzecz, zwłaszcza gdy uzgodniony zakres umowy i rzeczywiście wykonane czynności nie pokrywają się?',
      needed='Stanowisko eksperta na tle art. 5 pkt 4 i art. 42 KERP, najlepiej z przykładami granicznymi. W konkretnej relacji potrzebne pozostają dokumenty umowy i wykonanych czynności.')
elif cid=='OBS-070':
    c['scope']=c['scope'].replace('z kumulatywnymi warunkami ochrony tajemnicy','z kumulatywnymi warunkami zgody klientów, ochrony tajemnicy').replace('brak w korpusie przykładów sądowych dotyczących granicy','w przeczytanych fragmentach nie ustalono przykładu sądowego rozstrzygającego granicę')
elif cid=='OBS-043':
    c['scope']=c['scope'].replace('Korpus nie podaje samodzielnego testu granicy pojęcia','W przeczytanych fragmentach nie odnaleziono samodzielnego testu granicy pojęcia')
    c['records'][0]['claim']=c['records'][0]['claim'].replace('bliskie stosunki radcy','byłe lub obecne bliskie stosunki radcy')
    c['records'][0]['context']=c['records'][0]['context'].replace('lub inną osobą','lub osobą')
    c['questions'][0]['variants']='A: przeciwnik klienta z art. 27 pkt 5 oznacza wyłącznie formalnego przeciwnika procesowego; druga alternatywa zależy od zainteresowania niekorzystnym wynikiem, bez założenia, że dotyczy tylko osób poza postępowaniem. B: przeciwnik klienta obejmuje także faktyczną relację przeciwstawnych interesów poza postępowaniem; druga alternatywa pozostaje odrębną podstawą. W obu wariantach kategorie mogą pokrywać się faktycznie.'
elif cid=='OBS-057':
    c['records'][0]['context']='Omówienie ogólnego standardu art. 28 ust. 1 dla radcy będącego obrońcą lub pełnomocnikiem aktualnych klientów. Autor wymaga oceny sprzeczności odrębnej od tożsamości lub związku spraw.'
    c['records'][1]['claim']=c['records'][1]['claim'].replace('jako zobowiązanie radcy','jako sytuację, w której radca jest lub może być zobowiązany')
    c['records'][1]['limits']='W oryginalnej stronie 17 PDF sprawdzono wzrokowo marker „???”, wyróżniony kolorem. Odczyt jest potwierdzony; nie ustalono znaczenia redakcyjnego markera. Lokalny KERP pozwala porównać tekst art. 28-30, lecz nie usuwa tej niejasności autorskiej. Art. 27 i art. 28 ust. 2 pozostają odrębnymi kategoriami w ujęciu autora. SRC-01 i SRC-03 są tego samego autora, więc zbieżność nie stanowi niezależnego potwierdzenia.'
    c['records'][2]['limits'] += ' Ocena dotyczy danej sprawy lub sprawy z nią związanej; zakres osoby najbliższej pozostaje związany z art. 5 pkt 7. Potwierdzono wzrokowo odczyt akapitu na oryginalnej stronie 19 PDF.'
    c['meanings'][1]['description']=c['meanings'][1]['description'].replace('realizacja interesu radcy lub osoby najbliższej nie może następować bez uszczerbku dla klienta i odwrotnie','realizacja interesu radcy lub osoby najbliższej nie jest możliwa bez uszczerbku dla interesu klienta i odwrotnie')
    c['questions'][0]['variants']='A: materialny test niemożności realizacji jednego interesu bez uszczerbku dla drugiego stanowi treść konfliktu z art. 30 ust. 1. B: test ten jest analogią pomocniczą, a konflikt wymaga autonomicznej oceny. W obu ujęciach odrębnie pozostaje ocena znacznego ryzyka, której konkretnego progu materiał nie podaje.'
elif cid=='OBS-029':
    c['meanings'][2]['description']=c['meanings'][2]['description'].replace('zakazuje osobie kierującej innym radcą','zakazuje radcy sprawującemu kierownictwo nad innym radcą')
    c['records'][4]['speaker']='P. Skuczyński, autor komentarza redakcyjnego SRC-01 i poradnika SRC-03'
elif cid=='OBS-032':
    c['scope']=c['scope'].replace('ogólnej normy z OBS-029-R05','autorskiego objaśnienia z OBS-029-R05')
    c['questions'][0]['variants']='Materiał odróżnia przewidywane ograniczenie niezależności od znacznego zagrożenia jej naruszenia, lecz nie daje gotowych konkurencyjnych progów. Do oceny eksperta pozostaje, jakie znaczenie mają konkretność, siła i kontekst możliwego wpływu oraz zależność wynagrodzenia. Nie proponuje się arbitralnego poziomu prawdopodobieństwa ani nie utożsamia znaczności z dowolną możliwością wpływu.'
    c['questions'][0]['consequences']='Odpowiedź wyznaczy okoliczności, na których należy opierać ocenę przed wykonaniem czynności. Pozwoli odróżnić ocenę możliwego wpływu od dowodu, że radca już mu uległ, z zachowaniem słowa znaczne. Zależność wynagrodzenia wymaga oceny w konkretnym układzie; relacja zarzutu WO-54/21 sama nie ustanawia reguły zakazu.'
elif cid=='OBS-062':
    def polish(value):
        if isinstance(value,dict): return {k:(v if k=='quote' else polish(v)) for k,v in value.items()}
        if isinstance(value,list): return [polish(v) for v in value]
        if isinstance(value,str): return value.replace('cross-referenced','wskazanych przez odesłanie')
        return value
    c=polish(c)
    c['records'][0]['limits']='Przepis określa status i funkcję tajemnicy, nie jej pełny zakres przedmiotowy, czasowy ani procedurę zwolnienia. Zakres przedmiotowy i czasowy ujęto w OBS-007-R02; procedura zwolnienia pozostaje nieustalona.'
    src=next(x for x in s['sources'] if x['id']=='SRC-04')
    lines=(q.PROJECT/src['text']).read_text(encoding='utf-8').splitlines()
    rec=c['records'][3]
    rec['claim']+=' Odrębnie art. 19 KERP opisuje obowiązek podjęcia środków prawnych dla uniknięcia lub ograniczenia zwolnienia z tajemnicy, a w razie zwolnienia także poinformowania właściwej rady i działań zmierzających do wyłączenia jawności.'
    rec['speaker']='Lokalna ustawa o radcach prawnych, art. 3 ust. 5-6, oraz KERP, art. 19'
    rec['context']='Zestawienie treści lokalnych przepisów dotyczących tajemnicy, wyłączeń i zwolnienia; bez rekonstrukcji procedur spoza korpusu.'
    rec['evidence'].append(dict(source_id='SRC-04',line_start=127,line_end=129,quote='\n'.join(lines[126:129])))
    rec['limits']='Art. 3 ust. 6 ogranicza wyłączenia do zakresu określonego wskazanymi przepisami. Nie wyprowadza się z ust. 5 samodzielnego rozstrzygnięcia wszystkich sytuacji procesowych: art. 19 KERP przewiduje obowiązki w odniesieniu do określonego prawem zwolnienia. Ustalenie relacji wymaga właściwych przepisów proceduralnych, których tu nie rekonstruowano. Karta opisuje lokalne teksty, bez potwierdzenia ich aktualności.'
    c['coverage'][3]['read_ranges']+='; 125-129 (uzupełnienie Astry)'
    c['coverage'][3]['notes']+=' Astra odczytała art. 19 i zachowała go jako materiał wymagający konfrontacji z art. 3 ust. 5 ustawy.'
    c['meanings'][1]['description']+=' Art. 19 KERP nakazuje podejmowanie przewidzianych prawem środków wobec zwolnienia i po zwolnieniu; relacja z tekstem ustawy wymaga materiału proceduralnego i pozostaje odrębną luką.'
    c['gaps'].append(dict(id='OBS-062-G03',issue='Lokalny art. 3 ust. 5 ustawy mówi o niemożności zwolnienia co do wskazanych faktów, a art. 19 KERP przewiduje obowiązki związane z określonym w prawie zwolnieniem. Brak odpowiednich przepisów proceduralnych nie pozwala rozstrzygnąć ich relacji ani trybu.',needed='Właściwe i aktualne dla przyjętego stanu prawnego przepisy proceduralne oraz wykładnia relacji obu regulacji. Nie zastępować tekstów samą opinią eksperta.'))
    question=c['questions'][0]
    question['variants']='Sam lokalny tekst wymaga ograniczenia wyłączeń do zakresu przepisów, do których odsyła. Bez ich treści nie da się wskazać uzasadnionych konkurencyjnych zakresów. Do ustalenia pozostaje odrębnie dozwolone lub wymagane przekazanie informacji oraz ewentualna podstawa skorzystania z niej; żaden szerszy zakres nie został przyjęty.'
    question['consequences']='Odpowiedź wraz z tekstami przepisów pozwoli opisać adresata, cel, rodzaj informacji i granice konkretnego obowiązku lub uprawnienia. Samo odesłanie nie zostanie zamienione w ogólne zezwolenie na ujawnianie lub korzystanie z informacji.'
    question['question']='Jaki dokładnie zakres informacji i czynności obejmują odesłania z lokalnego art. 3 ust. 6 ustawy oraz jak odnoszą się do zastrzeżenia art. 16 KERP dotyczącego skorzystania z informacji? Jakie przepisy i stan prawny powinny stanowić podstawę uzupełnienia tej części bazy?'
    question['needed']='Teksty właściwych przepisów, do których ustawa odsyła, z ustalonym stanem prawnym, oraz ich wykładnia. Osobno określić przekazanie informacji i skorzystanie z niej; opinia eksperta nie zastępuje brakujących tekstów.'
    c['questions'].append(dict(id='OBS-062-Q02',record_ids=['OBS-062-R04'],understanding='Lokalny art. 3 ust. 5 ustawy zawiera formułę niemożności zwolnienia z tajemnicy, natomiast art. 19 KERP określa działania wobec zwolnienia oraz obowiązki po zwolnieniu. Samo zestawienie nie wystarcza do rozstrzygnięcia dopuszczalności i trybu w konkretnej procedurze.',variants='Brak podstaw do przyjęcia jednej ogólnej odpowiedzi dla wszystkich procedur. Należy ustalić właściwe przepisy, zakres informacji i charakter zwolnienia, a następnie wyjaśnić relację do obu lokalnych regulacji.',consequences='Uzupełnienie zapobiegnie wywodzeniu z jednego zdania ustawy uniwersalnej odpowiedzi procesowej albo traktowaniu art. 19 KERP jako samodzielnej podstawy zwolnienia.',question='Jak wyjaśnić relację art. 3 ust. 5 ustawy o radcach prawnych do art. 19 KERP i jakie przepisy proceduralne trzeba dodać do korpusu, aby rzetelnie opisać dopuszczalność, zakres oraz tryb zwolnienia z tajemnicy?',needed='Właściwe teksty proceduralne i ich zweryfikowany stan prawny oraz stanowisko eksperta. Nie ustalono procedury z obecnego materiału.'))
    c['self_check']+=' Astra uzupełniła art. 19 KERP, wskazała odrębne pytanie o relację do ustawy i zastąpiła pozorne warianty proceduralne w Q01 opisem brakującego materiału.'
elif cid=='OBS-026':
    c['scope']=c['scope'].replace('a granica użycia i potencjalności pozostaje przy OBS-028-Q01','natomiast OBS-028-Q01 dotyczy odrębnego kontekstu przewagi i zwrotu z SRC-01:464, a nie definicji z w. 448')
    c['meanings'][1]['description']=c['meanings'][1]['description'].replace('Pytanie o relację wykorzystania do potencjalności pozostaje w OBS-028-Q01.','OBS-028-Q01 dotyczy podobnego rozróżnienia w odrębnym kontekście przewagi i innego zdania autora z w. 464; nie rozszerza się tego pytania automatycznie na tajemnicę.')
    c['records'][1]['limits']=c['records'][1]['limits'].replace('relacja użycia do potencjalności jest już w OBS-028-Q01.','próg znacznego zagrożenia dla tajemnicy pozostaje do opracowania w OBS-077. OBS-028-Q01 dotyczy odrębnego kontekstu nieuzasadnionej przewagi.')
    c['self_check']+=' Astra doprecyzowała odwołanie do OBS-028-Q01: tamto pytanie dotyczy przewagi i w. 464, a nie definicji użycia informacji objętych tajemnicą z w. 448.'
elif cid=='OBS-077':
    c['coverage'][1]['notes']='Przeczytano fragment WO-31/24: najpierw opis przypisanego czynu, następnie odrębna aprobata uwagi OSD. Przypadek dotyczy pomocy BD przeciw EK/EK2 przy wcześniejszej reprezentacji opisanej w wyborze. Nie ustalono kompletnej chronologii z oryginału orzeczenia.'
    c['meanings'][0]['description']='Punkt mapuje literalną przesłankę i wcześniejsze objaśnienie, że nie trzeba wykazać dokonanego naruszenia, jeżeli istnieje znaczne zagrożenie. Określenie znaczne występuje w art. 26, lecz w sprawdzonych fragmentach nie otrzymuje odrębnego testu ani listy wskaźników. Wybór WO-31/24 opisuje pomoc BD przeciw EK/EK2 przy wcześniejszej reprezentacji i przytacza aprobatę uwagi OSD, że w tym przypadku zagrożenie było znaczne. Opis przypisanego czynu i aprobata oceny to odrębne wypowiedzi. Nie wynika z tego powszechna miara dla innych stanów faktycznych ani wymóg dowodu rzeczywistego użycia informacji.'
    c['gaps'][1]['issue']='W korpusie brak oryginału WO-31/24. Fragment wyboru zawiera opis przypisanego czynu i osobno aprobatę uwagi OSD, ale nie pozwala skontrolować pełnych motywów ani ustalić uniwersalnego testu.'
    c['self_check']=c['self_check'].replace('z rozróżnieniem opisu czynu/zarzutu i oceny przypisanej OSD','z rozróżnieniem opisu przypisanego czynu i odrębnej aprobaty uwagi OSD')
elif cid=='OBS-068':
    c['meanings'][1]['description']='W konfiguracji wspólnego wykonywania zawodu art. 26a ust. 2 łączy zgodę z rozwiązaniami organizacyjnymi i technicznymi chroniącymi tajemnicę oraz z warunkiem, że posiadana wiedza nie daje nieuzasadnionej przewagi. Możliwość ta jest wyłączona w sytuacjach art. 28 ust. 2. Autor komentarza opisuje wyznaczenie osoby do czynności i odrębne sprawdzenie jej wiedzy. W ramach polityki barier wskazuje uprzedni dostęp, zapobieganie dostępowi w czasie obsługi, zakaz kontaktów w tych sprawach z osobami znającymi informacje lub mającymi do nich dostęp oraz niekorzystanie z ich pomocy i współpracy. Sama zgoda ani późniejsze odseparowanie nie zastępują badania wiedzy. Są to objaśnienia autora, odrębne od literalnego brzmienia art. 26a; nie tworzą definicji wiedzy z art. 26 ust. 1. Wątpliwość co do kręgu wymaganych zgód pozostaje w OBS-076-Q02.'
    c['coverage'][3]['notes']+=' Możliwość z art. 26a ust. 2 jest wyłączona dla sytuacji art. 28 ust. 2; warunek zachowano wyraźnie w M02.'
    c['self_check']+=' Astra ponownie odczytała całe OBS-028-R06 i OBS-076-R04; doprecyzowała autorstwo opisu wyznaczenia osoby oraz wyłączenie art. 28 ust. 2.'
elif cid=='OBS-072':
    c['scope']=c['scope'].replace('wyłącznie użycia informacji objętej tajemnicą w ramach art. 16 KERP','użycia informacji objętej tajemnicą w omówieniu pierwszej przesłanki art. 26, w kontekście zakazu z art. 16 KERP')
    c['meanings'][0]['description']=c['meanings'][0]['description'].replace('autorskim objaśnieniem użycia informacji objętej tajemnicą z art. 16 KERP','autorskim objaśnieniem użycia informacji objętej tajemnicą przy pierwszej przesłance art. 26 i zakazie z art. 16 KERP')
    for rid in ['OBS-028-R04','OBS-002-R06','OBS-002-R07']:
        if rid not in c['existing_record_refs']: c['existing_record_refs'].append(rid)
        if rid not in c['meanings'][0]['record_ids']: c['meanings'][0]['record_ids'].append(rid)
    c['self_check']+=' Astra uzupełniła formalne odwołania do trzech rekordów wymienionych w opisie znaczenia i doprecyzowała kontekst w. 448 komentarza.'
else:
    raise ValueError(cid)
q.validate_result(s,j,c); q.write(p,c)
print(cid,'korekta i walidacja OK')
