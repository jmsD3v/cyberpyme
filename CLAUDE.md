# CyberPyME — Contexto para Claude Code

## Qué es esto

Herramienta de autodiagnóstico de ciberseguridad para PyMEs sin área de IT.
Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1. Es el entregable de la
Práctica Profesionalizante de Juanma (Tecnicatura en Seguridad Informática,
TECLAB, período 2A 2026: 18/ago al 13/dic/2026), con intención de convertirla
después en producto real, potencialmente monetizable.

**Hay dos entregas distintas y NO hay que mezclarlas:**

1. **Entrega académica (obligatoria, vence 13/dic)** — cuestionario + motor de
   scoring en Python + informe + validación con 3 casos + guía de hardening.
   Corre sola, sin infraestructura.
2. **Fase producto (sin fecha límite académica)** — FastAPI + Supabase +
   Next.js sobre el mismo motor, para el objetivo de app monetizable.

Si no se aclara lo contrario, priorizar siempre la entrega académica primero.

## Estado actual (al 03/09/2026 — código real, ver nota de ritmo abajo)

Ya construido y funcionando (`backend/`):

- `app/data/questions.json` — **20** preguntas, 5 dominios (accesos, wifi,
  backups, actualizaciones, continuidad), con peso, mapeo NIST/CIS y
  `recommendation_id`.
- `app/data/recommendations.json` — 20 recomendaciones con prioridad
  P1/P2/P3, impacto, esfuerzo, plazo, **`why`** (por qué importa) y
  **`steps`** (guía de resolución paso a paso en criollo, sin jerga
  técnica) — esto es lo que alimenta la guía de resolución del informe.
- `app/models/question.py` — `Question`, `Answer` (valores yes=1.0,
  partial=0.5, no=0.0, unknown=0.0).
- `app/models/assessment.py` — `DomainResult`, `AssessmentResult`,
  `risk_level_for()` (BAJO ≥80, MEDIO ≥60, ALTO ≥40, CRÍTICO <40).
- `app/services/scoring.py` — motor determinista: `weighted_score()`,
  `score_by_domain()`, `score_global()`, `find_gaps()`,
  `prioritize_actions()`, `calculate_assessment()`.
- `app/services/report.py` — genera un informe **HTML interactivo
  autocontenido** (sin backend, sin CDN) a partir de `AssessmentResult`:
  gauge de score global + barras por dominio (coloreadas por riesgo,
  paleta de la skill `dataviz`) + acordeón de acciones priorizadas con
  guía de resolución paso a paso. Tema oscuro gris (no negro) por defecto
  — preferencia explícita del usuario, ver memoria `feedback-dark-gray-not-black`.
- `app/data/validation_cases.json` + `app/services/validation.py` — 3
  perfiles simulados (débil/medio/maduro) corridos sobre el mismo motor,
  con chequeo de orden monótono (`is_monotonic`). Resultado real: débil
  3.00/100 CRÍTICO → medio 42.61/100 ALTO → maduro 87.85/100 BAJO.
- `app/services/report.py` → `render_comparative_html()` — informe HTML
  comparativo de los 3 casos (tabla + gráfico de barras agrupadas por
  dominio, paleta categórica de `dataviz`, conclusión automática).
- `app/services/report.py` → `render_hardening_guide_html()` — guía de
  hardening completa (las 20 acciones, agrupadas por dominio), generada
  reusando `prioritize_actions()` sobre **todas** las preguntas en vez de
  solo las brechas de una evaluación puntual — no depende de ningún
  autodiagnóstico.
- `app/cli.py` — demo de consola (`python -m app.cli demo` /
  `interactivo` / `validacion` / `hardening`), con flag `--html <path>` en
  cualquier modo para generar también el informe HTML correspondiente.
- `tests/test_scoring.py` (10) + `tests/test_report.py` (4) +
  `tests/test_validation.py` (4) + `tests/test_hardening.py` (3) —
  **21/21 pasando**.

**No existe todavía:** documentación final/manual de uso, FastAPI,
Supabase, frontend.

## ⚠️ Ritmo de publicación — NO confundir "hecho en el código" con "mostrado en clase"

El desarrollo real va más rápido que el cronograma de clases (Juanma estima
terminar el grueso en un par de días, contra un plazo que llega al 13/dic).
Eso está bien para el código, pero:

- **`BITACORA-INTERNA.md`** (raíz del proyecto) es el registro real de
  avance, con una entrada pre-escrita por cada jornada futura, lista para
  publicar el día que corresponda.
- **Notion (Bitácora + Tareas) nunca debe mostrar algo terminado antes de
  la fecha real de esa jornada Lunes/Miércoles**, aunque el código ya esté
  100% listo. Cuando la fecha llega: copiar la entrada correspondiente de
  `BITACORA-INTERNA.md` a la Bitácora de Notion y recién ahí marcar la
  tarea asociada como Finalizada.
- Si en una sesión se termina algo "adelantado", anotarlo en
  `BITACORA-INTERNA.md` bajo la fecha real que le corresponde, no tocar
  Notion todavía.

Este documento (`CLAUDE.md`) sí se mantiene siempre al día con el estado
real del código — es `BITACORA-INTERNA.md` y Notion los que se pausan.

## Próximos pasos, en este orden

1. **Documentación final + manual de uso**, sin artefactos de generación de
   IA sin limpiar (nada de texto tipo `fileciteturn0file0` — ya pasó una
   vez en el documento técnico, revisar siempre antes de enviar nada).
   Due Notion: 2026-11-04.
2. Recién después del 13/dic: API FastAPI sobre el motor ya validado,
   Supabase con RLS real (políticas por operación, `auth.uid()`, nunca
   `user_metadata`), frontend Next.js.

## Principios de diseño a respetar

- **Determinismo:** misma respuesta → mismo score, siempre. Nada de
  llamadas externas ni aleatoriedad en el scoring.
- **Configuración sobre código:** preguntas, pesos y recomendaciones viven
  en JSON. Agregar una pregunta no debe tocar el motor.
- **KISS/YAGNI:** no anticipar infraestructura de producto (DB, API, auth)
  dentro del alcance académico. Esa parte tiene su propio momento.
- Resto de principios de ingeniería: ver preferencias del usuario (DRY,
  Security by Design, Least Privilege, Single Responsibility, etc.) —
  aplican igual acá.

## Seguimiento

El progreso se trackea en Notion, no en Trello: página "Prácticas
Profesionalizantes TECLAB" (base "Proyectos") → base "Tareas" filtrada por
este proyecto, y una subpágina "Bitácora de avances (Lunes/Miércoles)" con
una entrada por jornada de clase (cadencia lunes/miércoles desde el
18/ago). Si Claude Code hace avances relevantes, conviene reflejarlos ahí
también (vía el conector de Notion si está disponible en esa sesión, o
avisarle a Juanma para que lo actualice él).

## Cómo correr lo que ya existe

```bash
cd backend
pip install pytest --break-system-packages

python -m pytest tests/ -v                          # 21 tests
python -m app.cli demo                              # demo con caso simulado
python -m app.cli interactivo                       # demo pregunta por pregunta
python -m app.cli validacion                        # corre los 3 casos débil/medio/maduro
python -m app.cli hardening --html guia.html        # guía de hardening completa (20 acciones)
python -m app.cli demo --html informe.html          # + informe HTML interactivo
python -m app.cli validacion --html comparativa.html  # + informe comparativo
```
