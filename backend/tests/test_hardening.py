import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.report import render_hardening_guide_html
from app.services.scoring import load_questions, load_recommendations


def test_hardening_guide_includes_all_recommendations():
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    report = render_hardening_guide_html(questions, domain_labels, recommendations)

    assert "<!doctype html>" in report
    for rec in recommendations.values():
        assert rec["title"] in report


def test_hardening_guide_groups_by_all_five_domains():
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    report = render_hardening_guide_html(questions, domain_labels, recommendations)

    for domain_info in domain_labels.values():
        assert domain_info["label"] in report


def test_hardening_guide_independent_of_any_assessment():
    """La guía no depende de un AssessmentResult puntual, solo de las 20
    preguntas y el catálogo de recomendaciones."""
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    report = render_hardening_guide_html(questions, domain_labels, recommendations)
    assert report.count("action-card") > 0
