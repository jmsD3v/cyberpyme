import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.scoring import calculate_assessment, weighted_score, load_questions


def test_weighted_score_zero():
    assert weighted_score([(0.0, 5), (0.0, 5)]) == 0.0


def test_weighted_score_full():
    assert weighted_score([(1.0, 5), (1.0, 5)]) == 100.0


def test_weighted_score_partial():
    assert weighted_score([(1.0, 5), (0.0, 5)]) == 50.0


def test_weighted_score_empty():
    assert weighted_score([]) == 0.0


def test_load_questions_covers_five_domains():
    questions, domains = load_questions()
    found_domains = {q.domain for q in questions}
    assert found_domains == set(domains.keys())


def test_all_yes_gives_bajo_risk():
    questions, _ = load_questions()
    answers = {q.id: "yes" for q in questions}
    result = calculate_assessment(answers)
    assert result.global_score == 100.0
    assert result.risk_level == "BAJO"
    assert result.top_actions == []


def test_all_no_gives_critico_risk():
    questions, _ = load_questions()
    answers = {q.id: "no" for q in questions}
    result = calculate_assessment(answers)
    assert result.global_score == 0.0
    assert result.risk_level == "CRITICO"
    assert len(result.top_actions) == len(questions)


def test_backups_domain_critical_when_no_backup():
    questions, _ = load_questions()
    answers = {q.id: "yes" for q in questions}
    for q in questions:
        if q.domain == "backups":
            answers[q.id] = "no"
    result = calculate_assessment(answers)
    assert result.domains["backups"].risk_level == "CRITICO"
    # el score global no debe ocultar la brecha crítica de un dominio
    assert result.domains["backups"].score < result.global_score


def test_top_actions_sorted_by_priority():
    questions, _ = load_questions()
    answers = {q.id: "no" for q in questions}
    result = calculate_assessment(answers)
    priorities = [a["priority"] for a in result.top_actions]
    assert priorities == sorted(priorities)  # P1 antes que P2 antes que P3


def test_invalid_answer_raises():
    import pytest
    from app.models.question import Answer

    with pytest.raises(ValueError):
        Answer(question_id="ACC-01", value="tal_vez").score_value
