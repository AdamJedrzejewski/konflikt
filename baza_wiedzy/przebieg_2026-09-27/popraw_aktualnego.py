from pathlib import Path
import sys, shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'narzedzia/kolejka_pojec'))
import kolejka as q
state=q.load(q.DEFAULT_STATE); job=q.get_job(state,'OBS-002')
path=q.DEFAULT_STATE/job['attempts'][-1]['artifact']
backup=path.with_name('wynik_przed_odbiorem.json')
if not backup.exists(): shutil.copy2(path,backup)
r=q.read(path)
r['existing_record_refs']=['KL-R01','KL-R04','KL-R05','KL-R06','KL-R08','KL-R10','KL-R11','KL-R12','KL-R13']
r['meanings'].append({'id':'OBS-002-M02','context':'Identyfikacja aktualnego odbiorcy pomocy, w tym pośrednictwo i jednostka organizacyjna; punkty S2-K3-00/02/03 i S2-K4-00.',
    'description':'Historyczna definicja i przykłady odbiorcy pomocy zachowują swoje ograniczenia. To, kto jest klientem, wymaga odrębnego ustalenia od tego, czy relacja nadal trwa. Karta łączy przyjęte wcześniej zakresy z nowym zagadnieniem czasu; nie utożsamia automatycznie strony umowy, beneficjenta i każdej jednostki grupy.',
    'record_ids':['KL-R01','KL-R05','KL-R06','KL-R12','KL-R13']})
r['coverage'][2]['notes']='Przeczytano wskazane bloki o byłym kliencie i rejestrze. Treści odpowiadające KL-R09–R11 pozostawiono jako materiał historyczny, bez ponownego zaliczenia.'
r['gaps'][1]['issue']+=' D 106/18 jest dostępne jedynie w przytoczeniu komentarza.'
r['self_check']+=' Odbiór Astry uzupełnił jawne odwołania do historycznych rekordów i mapowanie kontekstu odbiorcy pomocy, bez nowych rekordów.'
q.validate_result(state,job,r); q.write(path,r)
print('OK')
