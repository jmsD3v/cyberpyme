import json
from pathlib import Path

from app.models.assessment import AssessmentResult, DomainResult, risk_level_for
from app.models.question import Answer, Question

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_questions() -> tuple[list[Question], dict]:
    raw = json.loads((DATA_DIR / "questions.json").read_text(encoding="utf-8"))
    questions = [Question.from_dict(q) for q in raw["questions"]]
    return questions, raw["domains"]


def load_recommendations() -> dict:
    return json.loads((DATA_DIR / "recommendations.json").read_text(encoding="utf-8"))


def weighted_score(pairs: list[tuple[float, float]]) -> float:
    """pairs = [(valor_respuesta, peso), ...] -> score 0-100."""
    total_weight = sum(weight for _, weight in pairs)
    if not total_weight:
        return 0.0
    raw = sum(value * weight for value, weight in pairs)
    return round(raw / total_weight * 100, 2)


def score_by_domain(
    questions: list[Question], answers: dict[str, Answer]
) -> dict[str, DomainResult]:
    by_domain: dict[str, list[tuple[float, float]]] = {}
    for q in questions:
        answer = answers.get(q.id)
        if answer is None:
            continue
        by_domain.setdefault(q.domain, []).append((answer.score_value, q.weight))

    return {
        domain: DomainResult(domain=domain, score=weighted_score(pairs))
        for domain, pairs in by_domain.items()
    }


def score_global(domain_results: dict[str, DomainResult], domain_weights: dict) -> float:
    pairs = [
        (result.score / 100, domain_weights[domain]["domain_weight"])
        for domain, result in domain_results.items()
        if domain in domain_weights
    ]
    return weighted_score(pairs)


def find_gaps(questions: list[Question], answers: dict[str, Answer]) -> list[Question]:
    """Preguntas cuya respuesta representa una brecha (no / parcial / no sé)."""
    return [
        q for q in questions
        if q.id in answers and answers[q.id].is_gap
    ]


def calculate_assessment(answers_raw: dict[str, str]) -> AssessmentResult:
    """answers_raw = {"ACC-01": "yes", "ACC-02": "no", ...}"""
    questions, domain_weights = load_questions()
    recommendations = load_recommendations()
    answers = {qid: Answer(question_id=qid, value=val) for qid, val in answers_raw.items()}

    domain_results = score_by_domain(questions, answers)
    global_score = score_global(domain_results, domain_weights)

    gaps = find_gaps(questions, answers)
    top_actions = prioritize_actions(gaps, recommendations)

    return AssessmentResult(
        global_score=global_score,
        risk_level=risk_level_for(global_score),
        domains=domain_results,
        top_actions=top_actions,
    )


def prioritize_actions(gaps: list[Question], recommendations: dict) -> list[dict]:
    priority_order = {"P1": 0, "P2": 1, "P3": 2}
    actions = []
    for q in gaps:
        rec = recommendations.get(q.recommendation_id)
        if not rec:
            continue
        actions.append({**rec, "question_id": q.id, "risk": q.risk})
    actions.sort(key=lambda a: (priority_order.get(a["priority"], 9), -q_weight(a, gaps)))
    return actions


def q_weight(action: dict, gaps: list[Question]) -> float:
    for q in gaps:
        if q.id == action["question_id"]:
            return q.weight
    return 0
