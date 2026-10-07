import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'narzedzia/kolejka_pojec'))
import kolejka as q
p=Path(__file__).with_name('wynik.json');c=q.read(p)
c['meanings'][0]['record_ids'] += ['KL-R02','SP-R07','OBS-076-R01','OBS-076-R02','OBS-076-R03','OBS-046-R02']
c['meanings'][1]['record_ids'] += ['KL-R02','OBS-076-R04']
c['self_check']=c['self_check'].replace('nie utworzono nowych pytań, ponieważ wcześniejsze pytania obejmują formę, krąg zgody, art. 26a i relację do art. 28.','Nowe poglądy zapisano z autorskimi zastrzeżeniami, bez tworzenia pytania jedynie o ich zatwierdzenie. Wcześniejsze pytania dotyczą odrębnie formy, kręgu zgody, art. 26a i relacji do art. 28; nie zastępują weryfikacji kwalifikacji cywilnoprawnej z R02, jeśli miałaby stanowić podstawę decyzji.')
q.write(p,c)
