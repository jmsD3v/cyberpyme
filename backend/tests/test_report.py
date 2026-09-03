import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.report import render_html_report
from app.services.scoring import calculate_assessment, load_questions


def test_report_contains_score_and_risk():
    questions, domain_labels = load_questions()
    answers = {q.id: "no" for q in questions}
    result = calculate_assessment(answers)
    report = render_html_report(result, questions, domain_labels, business_name="Ferretería Test")

    assert "Ferretería Test" in report
    assert "Riesgo Crítico" in report
    assert "<!doctype html>" in report


def test_report_lists_all_gap_steps():
    questions, domain_labels = load_questions()
    answers = {q.id: "no" for q in questions}
    result = calculate_assessment(answers)
    report = render_html_report(result, questions, domain_labels)

    for action in result.top_actions:
        assert action["title"] in report
        for step in action["steps"]:
            # el paso puede llevar comillas simples -> html.escape las convierte a entidades
            assert html.escape(step, quote=True) in report


def test_report_with_no_gaps_shows_success_message():
    questions, domain_labels = load_questions()
    answers = {q.id: "yes" for q in questions}
    result = calculate_assessment(answers)
    report = render_html_report(result, questions, domain_labels)

    assert "Sin brechas detectadas" in report


def test_report_escapes_business_name():
    questions, domain_labels = load_questions()
    result = calculate_assessment({q.id: "yes" for q in questions})
    report = render_html_report(result, questions, domain_labels, business_name="<script>alert(1)</script>")

    assert "<script>alert(1)</script>" not in report
    assert "&lt;script&gt;" in report
