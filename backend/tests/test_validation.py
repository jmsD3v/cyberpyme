import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.report import render_comparative_html
from app.services.scoring import load_questions
from app.services.validation import CASE_ORDER, is_monotonic, load_validation_cases, run_validation


def test_validation_cases_cover_all_questions():
    questions, _ = load_questions()
    valid_ids = {q.id for q in questions}
    cases = load_validation_cases()
    assert set(cases.keys()) == {"maduro", "medio", "debil"}
    for case in cases.values():
        assert set(case["answers"].keys()) == valid_ids


def test_scores_are_monotonic_debil_medio_maduro():
    results = run_validation()
    assert is_monotonic(results)
    debil = results["debil"]["result"]
    medio = results["medio"]["result"]
    maduro = results["maduro"]["result"]
    assert debil.risk_level == "CRITICO"
    assert maduro.risk_level in ("BAJO", "MEDIO")
    assert debil.global_score < medio.global_score < maduro.global_score


def test_debil_has_more_gaps_than_maduro():
    results = run_validation()
    debil_gaps = len(results["debil"]["result"].top_actions)
    maduro_gaps = len(results["maduro"]["result"].top_actions)
    assert debil_gaps > maduro_gaps


def test_comparative_report_renders_all_cases():
    results = run_validation()
    _, domain_labels = load_questions()
    report = render_comparative_html(results, domain_labels)
    assert "<!doctype html>" in report
    for case_id in CASE_ORDER:
        assert results[case_id]["label"] in report
