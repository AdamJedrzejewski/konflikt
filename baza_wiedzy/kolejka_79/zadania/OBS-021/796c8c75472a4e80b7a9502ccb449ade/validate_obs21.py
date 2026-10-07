import json
import sys
from pathlib import Path

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
sys.path.insert(0, str(root / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(root / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-021")
result_path = Path(__file__).with_name("wynik.json")
result = json.loads(result_path.read_text(encoding="utf-8"))
validated = kolejka.validate_result(state, job, result)
print(json.dumps({"valid": True, "records": len(validated["records"]), "questions": len(validated["questions"]), "meanings": len(validated["meanings"]), "points": len(validated["points"])}, ensure_ascii=False))
