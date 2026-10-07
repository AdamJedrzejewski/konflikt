from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
state=q.load(q.DEFAULT_STATE); job=q.get_job(state,'OBS-058')
path=q.DEFAULT_STATE/job['attempts'][-1]['artifact']
backup=path.with_name('wynik_przed_odbiorem.json')
if not backup.exists(): shutil.copy2(path,backup)
r=q.read(path)
r['coverage'][1]={'source_id':'SRC-02','status':'CZESCIOWY','read_ranges':'Próba odczytu 1–112 ucięta przez narzędzie. Kontrola Astry: 18–32, 64–78 i 94–104.','notes':'Nie deklaruje się lektury całego wyboru. W przeczytanych fragmentach brak pozytywnego testu zależności osoby od radcy; fragment WO–54/21 w 68 dotyczy zależności wynagrodzenia radcy i ma postać opisu zarzucanych czynów.'}
r['scope']='Przegląd uzupełniający ON-R03/06/07 dla S1-K2-03, bez nowych rekordów. Komentator w SRC-01 wiersz 832 wskazuje osobę zależną od radcy; samo brzmienie art. 27 pkt 3 mówi o stosunku zależności z radcą. Nie ustalono pozytywnego testu minimalnych cech tej zależności. Pogląd o bliskoznaczności pozostaje w ON-P02. Opisy D 43/2016 i D 33/18 dotyczą bliskości i nie zostały przeniesione na zależność. Zależność radcy od klienta lub osoby trzeciej w komentarzu art. 26 (SRC-01 452–456) jest odrębnym kontekstem zagrożenia niezależności; nie przyjęto jej jako definicji art. 27 pkt 3.'
r['gaps'][0]['issue']='Komentator wskazuje kierunek: osoba od radcy zależna (SRC-01 832, historyczny ON-R07). Nie ustalono pozytywnego testu cech wystarczających, progu i rodzajów relacji objętych art. 27 pkt 3 ani podstaw do poszerzenia kierunku względem tego objaśnienia. Bliskość i zagrożenie niezależności radcy nie zastępują tego testu.'
item=r['questions'][0]
item['understanding']='Art. 27 pkt 3 mówi o stosunku zależności z radcą, natomiast komentator przy opisie udziału w rozstrzygnięciu wyraźnie pisze o osobie od radcy zależnej. Jest to wskazówka kierunku, bez pozytywnego testu zależności. Art. 26 i objaśnienie silnej zależności ekonomicznej dotyczą wpływu na samego radcę.'
item['variants']='A: przyjąć kierunek wskazany przez komentatora, wymagając określenia faktycznych cech zależności osoby od radcy; B: objąć także inne kierunki relacji, ale wyłącznie po wskazaniu odrębnej podstawy i granic tej wykładni; do czasu uzupełnienia zachować brak definicji operacyjnej.'
item['question']='Jakie fakty i minimalne cechy pozwalają ustalić zależność osoby biorącej udział w rozstrzygnięciu od radcy, zgodnie z objaśnieniem autora? Czy istnieje podstawa do objęcia art. 27 pkt 3 także innych kierunków relacji, a jeśli tak, jaka?'
item['needed']='Źródła i przykłady wprost odnoszące się do art. 27 pkt 3. Powiązanie z ON-P02 pozostaje, ale nowe pytanie dotyczy pozytywnego kryterium i zakresu kierunkowego, nie ponownego zrównania bliskości z zależnością.'
r['self_check']='Przegląd wykonawcy bez nowych rekordów. Astra skorygowała stwierdzenie o nieustalonym kierunku: komentator wskazuje osobę od radcy zależną (832), co jest już w ON-R07. Pozostaje brak testu minimalnych cech. Zachowano historyczne rekordy i jedno doprecyzowane pytanie. Operator OCZEKUJE.'
q.validate_result(state,job,r); q.write(path,r); print('OK')
