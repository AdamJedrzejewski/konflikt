import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
p=Path(__file__).with_name('wynik.json');c=q.read(p)
c['meanings'][0]['description']=c['meanings'][0]['description'].replace('że samo późniejsze wypowiedzenie pełnomocnictwa po skardze nie uchyliło przypisanego naruszenia','ocenę wypowiedzenia pełnomocnictwa po skardze jako spóźnionego i wymuszonego skargą')
r=c['records'][0];r['claim']=r['claim'].replace('opis zarzucanego czynu','opis czynu o statusie nieustalonym samodzielnie z fragmentu')
r['context']='Wybór opisuje wcześniejsze czynności na rzecz DN i KN jako wspólników spółki cywilnej oraz późniejszą reprezentację KN przeciw DN. Nie ustala się na tej podstawie jednego momentu zakończenia obu relacji. Odrębna późniejsza wypowiedź ocenia czas i okoliczności wypowiedzenia pełnomocnictwa.'
r['limits']+=' Nie ustalono z tego fragmentu pełnej sentencji, prawomocności ani tego, czy początkowy opis jest wyłącznie zarzutem czy opisem przypisanego czynu.'
c['gaps'][0]['issue']='Brak pełnego oryginału WO–25/24, potrzebnego do kontroli autorstwa poszczególnych zdań, statusu opisu czynu i pełnego rozstrzygnięcia. Fragment nie jest samodzielnym testem końca relacji; pytanie o takie kryterium pozostaje w OBS-002-Q01.'
q.write(p,c)
