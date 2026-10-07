from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
state=q.load(q.DEFAULT_STATE); job=q.get_job(state,'OBS-007')
path=q.DEFAULT_STATE/job['attempts'][-1]['artifact']
backup=path.with_name('wynik_przed_odbiorem.json')
if not backup.exists(): shutil.copy2(path,backup)
r=q.read(path)
r['existing_record_refs']=['KL-R04','KL-R07','KL-R08','KL-R09','KL-R10']
r['scope']+=' Powiązanie konsultacyjne: KL-P02 w tabeli z 24.09 i jej doprecyzowanie OBS-002-Q01. Ochrona tajemnicy pozostaje odrębnym zagadnieniem; wybór pól aplikacji nie jest nową wątpliwością prawną dla eksperta.'
r['records'][0]['kind']='porownanie_zrodel'
r['records'][0]['limits']='Nowością rekordu jest rozbieżność odsyłacza w komentarzu, nie ponowna definicja uprzednich czynności z KL-R04/R08. Art. 29 ust. 2 przewiduje zgodę właściwych osób na warunkach tego przepisu, z wyłączeniem gdy radca jest lub był obrońcą w sprawie karnej co najmniej jednej z nich; szczegóły w SP-R07 i odebranej OBS-076. Nie przenosić tej możliwości na art. 28 ust. 3.'
r['meanings'][0]['description']='Art. 28 ust. 3 dotyczy obecnej reprezentacji lub obrony klienta przy konflikcie z osobą uprzednio obsługiwaną. Art. 29 ust. 1 pkt 2 dotyczy obecnego doradzania klientowi przy konflikcie z interesami takiej osoby. Komentarz w drugim kontekście odsyła do pkt 1; numer wymaga wyjaśnienia. Warunki zgody i wyjątek karny zachowano w granicach R01 oraz karcie OBS-076.'
r['meanings'][0]['record_ids']+=['KL-R04','KL-R08','KL-R09']
r['questions']=r['questions'][:1]
r['questions'][0]['question']='Czy odesłanie komentarza do art. 29 ust. 1 pkt 1 przy obecnym doradzaniu klientowi w konflikcie z interesami osoby uprzednio obsługiwanej jest omyłką i powinno wskazywać pkt 2? Jaka jest zamierzona podstawa tego fragmentu?'
r['self_check']+=' Astra usunęła Q02 z konsultacji: dotyczyło wyłącznie sposobu zapisania w aplikacji odrębności już wynikającej ze źródeł. Doprecyzowano adresata obecnego doradztwa, zachowano warunki zgody, dodano odwołania historyczne. Dwa nowe rekordy i jedno pytanie po odbiorze.'
q.validate_result(state,job,r); q.write(path,r); print('OK')
