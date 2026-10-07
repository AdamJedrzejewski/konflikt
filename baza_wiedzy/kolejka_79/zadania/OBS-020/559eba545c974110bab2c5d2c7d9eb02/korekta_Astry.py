import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
p=Path(__file__).with_name('wynik.json')
c=q.read(p)
c['records'][0]['speaker']='Kodeks Etyki Radcy Prawnego, lokalny tekst uchwalony przez samorząd zawodowy'
q.write(p,c)
