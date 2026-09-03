"""
Validación de la metodología con 3 casos simulados de PyME (madura, media,
débil) — Fase 15 del plan. Corre el mismo motor de scoring sobre 3 perfiles
distintos y documenta que el resultado es coherente y monótono: a mejor
postura declarada, mejor score y menor riesgo.
"""
import json
from pathlib import Path

from app.services.scoring import calculate_assessment

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CASE_ORDER = ["debil", "medio", "maduro"]  # de peor a mejor postura


def load_validation_cases() -> dict:
    return json.loads((DATA_DIR / "validation_cases.json").read_text(encoding="utf-8"))


def run_validation() -> dict:
    """Corre los 3 casos -> {case_id: {"label", "descripcion", "result": AssessmentResult}}."""
    cases = load_validation_cases()
    out = {}
    for case_id, case in cases.items():
        out[case_id] = {
            "label": case["label"],
            "descripcion": case["descripcion"],
            "result": calculate_assessment(case["answers"]),
        }
    return out


def is_monotonic(results: dict) -> bool:
    """True si el score global mejora en el orden débil < medio < maduro."""
    scores = [results[c]["result"].global_score for c in CASE_ORDER]
    return scores[0] < scores[1] < scores[2]
