import json
import sys
from pathlib import Path

task_dir = Path(__file__).parent
repo = task_dir.parents[5]
sys.path.insert(0, str(repo / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka

queue_dir = repo / "OBSIL" / "baza_wiedzy" / "kolejka_79"
state = kolejka.load(queue_dir)
job = kolejka.get_job(state, "OBS-016")
result = json.loads((task_dir / "wynik.json").read_text(encoding="utf-8"))
validated = kolejka.validate_result(state, job, result)
print(json.dumps({
    "valid": True,
    "task_id": validated["task_id"],
    "records": len(validated["records"]),
    "questions": len(validated["questions"]),
    "meanings": len(validated["meanings"]),
    "gaps": len(validated["gaps"]),
    "coverage": len(validated["coverage"]),
    "operator_status": validated["operator_status"],
}, ensure_ascii=True))
