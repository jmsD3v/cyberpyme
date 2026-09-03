# CyberPyME — Backend (Fase 1-3: banco de preguntas, scoring, recomendaciones)

Motor determinista de autodiagnóstico de ciberseguridad para PyMEs sin área de IT.
Metodología: NIST CSF 2.0 + CIS Controls v8.1 IG1.

## Estructura

```
backend/
├── app/
│   ├── data/
│   │   ├── questions.json        # 19 preguntas, 5 dominios, mapeo NIST/CIS
│   │   └── recommendations.json  # catálogo de recomendaciones por pregunta
│   ├── models/
│   │   ├── question.py           # Question, Answer
│   │   └── assessment.py         # DomainResult, AssessmentResult
│   ├── services/
│   │   └── scoring.py            # motor de scoring + priorización
│   └── cli.py                    # demo de consola
└── tests/
    └── test_scoring.py           # 10 tests unitarios
```

## Uso

```bash
cd backend
pip install pytest --break-system-packages   # única dependencia por ahora

# correr los tests (evidencia para la clase de miércoles)
python -m pytest tests/ -v

# demo con caso simulado (evidencia para la clase de lunes)
python -m app.cli demo

# demo interactiva, respondiendo pregunta por pregunta
python -m app.cli interactivo
```

## Qué NO tiene todavía (a propósito)

Sin FastAPI, sin Supabase, sin frontend. Es la parte que TECLAB pide
literalmente en el plan de trabajo aprobado (tarea 4: "desarrollar en
Python la herramienta que procesa el cuestionario y genera el informe
con recomendaciones priorizadas"). Corre sola, no depende de infraestructura,
y ya es demostrable.

La capa de API (FastAPI) + Supabase + frontend (Next.js) es la Fase 4 en
adelante del plan de desarrollo — se construye después, sobre este motor
ya validado con tests, para convertir esto en la app real.

## Diseño

- **Determinismo:** misma respuesta → mismo score, siempre. Sin llamadas
  externas ni aleatoriedad.
- **Configuración sobre código:** preguntas, pesos y recomendaciones viven
  en JSON, no hardcodeados. Agregar una pregunta no toca el motor.
- **Trazabilidad:** cada recomendación se puede rastrear a la pregunta que
  la generó (`question_id` en `top_actions`).
