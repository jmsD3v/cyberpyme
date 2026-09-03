import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.interactive_app import render_interactive_app_html
from app.services.scoring import load_questions, load_recommendations


def test_app_embeds_all_questions_and_recommendations():
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    html = render_interactive_app_html(questions, domain_labels, recommendations)

    assert "<!doctype html>" in html
    for q in questions:
        assert json.dumps(q.question, ensure_ascii=False) in html
    for rec in recommendations.values():
        assert json.dumps(rec["title"], ensure_ascii=False) in html


def test_app_has_no_backend_calls():
    """No debe haber fetch/XHR ni referencias a un servidor — todo corre en el navegador."""
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    html = render_interactive_app_html(questions, domain_labels, recommendations)

    assert "fetch(" not in html
    assert "XMLHttpRequest" not in html
    assert "http://" not in html
    assert "https://" not in html


def test_app_scoring_data_matches_python_engine():
    """Los datos embebidos deben alcanzar para reproducir el mismo cálculo
    que el motor Python (mismos ids, pesos y domain_weight)."""
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    html = render_interactive_app_html(questions, domain_labels, recommendations)

    start = html.index("const QUESTIONS = ") + len("const QUESTIONS = ")
    end = html.index(";\nconst DOMAIN_LABELS")
    embedded = json.loads(html[start:end])

    assert len(embedded) == len(questions)
    by_id = {q["id"]: q for q in embedded}
    for q in questions:
        assert by_id[q.id]["weight"] == q.weight
        assert by_id[q.id]["domain"] == q.domain
        assert by_id[q.id]["recommendation_id"] == q.recommendation_id
        assert by_id[q.id]["help"] == q.help


def test_app_embeds_help_text_for_jargon_questions():
    """Preguntas con jerga técnica (MFA, 3-2-1, WPA2/3, etc.) deben traer una
    aclaración en criollo — no alcanza con la pregunta sola."""
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    html = render_interactive_app_html(questions, domain_labels, recommendations)

    jargon_questions_with_help = [q for q in questions if q.id in ("ACC-02", "ACC-03", "BKP-03", "WIF-01")]
    assert len(jargon_questions_with_help) == 4
    for q in jargon_questions_with_help:
        assert q.help, f"{q.id} debería tener texto de ayuda"
        assert json.dumps(q.help, ensure_ascii=False) in html
