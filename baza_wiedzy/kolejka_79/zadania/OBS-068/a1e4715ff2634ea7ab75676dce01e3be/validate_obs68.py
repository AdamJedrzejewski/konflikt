import json
import sys
from pathlib import Path

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
sys.path.insert(0, str(root / "narzedzia" / "kolejka_pojec"))
import kolejka

queue_dir = root / "baza_wiedzy" / "kolejka_79"
state = kolejka.load(queue_dir)
job = kolejka.get_job(state, "OBS-068")
result_path = Path(__file__).with_name("wynik.json")
result = json.loads(result_path.read_text(encoding="utf-8"))
kolejka.validate_result(state, job, result)
print("validate_result: OK")
print(f"records={len(result['records'])}; meanings={len(result['meanings'])}; questions={len(result['questions'])}; sources={len(result['coverage'])}")
