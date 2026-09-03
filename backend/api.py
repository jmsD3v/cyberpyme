"""
API FastAPI — fase producto.

Envuelve el motor de scoring (app/services/scoring.py) como un servicio de
cómputo puro: recibe respuestas, devuelve el resultado calculado. No
conoce Supabase ni autenticación — eso lo maneja el frontend directo
contra Supabase (RLS real, ver migraciones del proyecto). Mismo
determinismo que el motor original: sin llamadas externas, sin estado
propio, misma respuesta siempre da el mismo resultado.

Correr:
    cd backend
    pip install fastapi "uvicorn[standard]" --break-system-packages
    uvicorn api:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.scoring import (
    calculate_assessment,
    load_questions,
    load_recommendations,
    prioritize_actions,
)

VALID_ANSWER_VALUES = {"yes", "partial", "no", "unknown"}

app = FastAPI(
    title="CyberPyME API",
    description="Motor de scoring de autodiagnóstico de ciberseguridad para PyMEs, expuesto como servicio de cómputo.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class EvaluarRequest(BaseModel):
    respuestas: dict[str, str]


def _question_to_dict(q) -> dict:
    return {
        "id": q.id, "domain": q.domain, "question": q.question,
        "weight": q.weight, "risk": q.risk, "nist": q.nist, "cis": q.cis,
        "recommendation_id": q.recommendation_id, "help": q.help,
    }


@app.get("/salud")
def salud():
    return {"status": "ok"}


@app.get("/preguntas")
def preguntas():
    """Catálogo completo: preguntas + dominios. Público, sin auth."""
    questions, domain_labels = load_questions()
    return {"domains": domain_labels, "questions": [_question_to_dict(q) for q in questions]}


@app.get("/recomendaciones")
def recomendaciones():
    """Catálogo completo de recomendaciones (why + steps). Público, sin auth."""
    return load_recommendations()


@app.get("/guia-hardening")
def guia_hardening():
    """Catálogo completo de acciones de hardening, ordenadas por prioridad —
    trata todas las preguntas como brecha (no depende de ningún
    autodiagnóstico puntual). Mismo cálculo que la guía HTML de la parte
    académica (`report.py::render_hardening_guide_html`), reusando
    `prioritize_actions` en vez de duplicar el orden en el frontend."""
    questions, _ = load_questions()
    recommendations = load_recommendations()
    return prioritize_actions(questions, recommendations)


@app.post("/evaluar")
def evaluar(body: EvaluarRequest):
    """Calcula un AssessmentResult a partir de las respuestas. No persiste
    nada — guardar el resultado en Supabase es responsabilidad del
    frontend, autenticado, contra la tabla `evaluaciones` (RLS)."""
    for qid, val in body.respuestas.items():
        if val not in VALID_ANSWER_VALUES:
            raise HTTPException(422, f"Respuesta inválida para {qid}: {val!r} (usar yes/partial/no/unknown)")

    result = calculate_assessment(body.respuestas)
    return {
        "global_score": result.global_score,
        "risk_level": result.risk_level,
        "domains": {
            domain: {"domain": r.domain, "score": r.score, "risk_level": r.risk_level}
            for domain, r in result.domains.items()
        },
        "top_actions": result.top_actions,
    }
