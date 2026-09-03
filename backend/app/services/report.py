"""
Generador de informe HTML interactivo para CyberPyME.

Produce un único archivo .html autocontenido (sin CDN, sin build step, sin
backend) a partir de un AssessmentResult ya calculado — se abre en cualquier
navegador y corre sola, cumpliendo la restricción de la entrega académica
("corre sola, sin infraestructura").

Incluye, además del resumen de score, una guía de resolución paso a paso por
cada brecha detectada (campo "steps" de recommendations.json) — es lo que
convierte el informe de "diagnóstico" en "diagnóstico + cómo resolverlo".
"""
from __future__ import annotations

import html
import math
from datetime import date

from app.models.assessment import AssessmentResult
from app.models.question import Question

# Paleta de estado (skill dataviz — referencia validada, nunca se "tematiza"
# por marca: good/warning/serious/critical son fijos).
STATUS_COLOR = {
    "BAJO": "#0ca30c",
    "MEDIO": "#fab219",
    "ALTO": "#ec835a",
    "CRITICO": "#d03b3b",
}
STATUS_LABEL = {"BAJO": "Bajo", "MEDIO": "Medio", "ALTO": "Alto", "CRITICO": "Crítico"}
PRIORITY_LABEL = {"P1": "Urgente", "P2": "Importante", "P3": "A planificar"}


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _gauge_svg(score: float, risk_level: str) -> str:
    r = 85
    circumference = 2 * math.pi * r
    offset = circumference * (1 - max(0.0, min(100.0, score)) / 100)
    color = STATUS_COLOR[risk_level]
    return f'''<svg viewBox="0 0 200 200" width="200" height="200" role="img"
  aria-label="Score global {score:.0f} de 100, riesgo {STATUS_LABEL[risk_level]}">
  <circle cx="100" cy="100" r="{r}" fill="none" stroke="var(--track)" stroke-width="18"/>
  <circle cx="100" cy="100" r="{r}" fill="none" stroke="{color}" stroke-width="18"
    stroke-linecap="round" stroke-dasharray="{circumference:.2f}"
    stroke-dashoffset="{offset:.2f}" transform="rotate(-90 100 100)"/>
  <text x="100" y="94" text-anchor="middle" class="hero-figure">{score:.0f}</text>
  <text x="100" y="122" text-anchor="middle" class="hero-sub">/100</text>
</svg>'''


def _domain_bars_svg(domain_results: dict, domain_labels: dict) -> str:
    row_h = 40
    bar_h = 22
    max_w = 380
    left = 140
    n = len(domain_results)
    height = row_h * n + 10
    rows = []
    for i, (domain, r) in enumerate(domain_results.items()):
        y = 10 + i * row_h
        bar_w = max_w * (r.score / 100)
        color = STATUS_COLOR[r.risk_level]
        label = domain_labels.get(domain, {}).get("label", domain)
        rows.append(f'''
  <text x="0" y="{y + bar_h / 2 + 4}" class="bar-label">{_esc(label)}</text>
  <rect x="{left}" y="{y}" width="{max_w}" height="{bar_h}" rx="4" class="bar-track"/>
  <rect x="{left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="4" fill="{color}"/>
  <text x="{left + max_w + 10}" y="{y + bar_h / 2 + 4}" class="bar-value">{r.score:.0f}</text>''')
    return f'''<svg viewBox="0 0 {left + max_w + 50} {height}" width="100%" role="img"
  aria-label="Score por dominio">{''.join(rows)}
</svg>'''


def _action_card(action: dict, question_by_id: dict[str, Question], domain_labels: dict, idx: int) -> str:
    q = question_by_id.get(action["question_id"])
    domain_label = domain_labels.get(action.get("domain", ""), {}).get("label", action.get("domain", ""))
    nist = ", ".join(q.nist) if q else ""
    cis = ", ".join(q.cis) if q else ""
    steps = action.get("steps", [])
    steps_html = "".join(f"<li>{_esc(s)}</li>" for s in steps)
    priority = action.get("priority", "P3")
    return f'''
<article class="action-card">
  <button class="action-header" aria-expanded="false" data-target="steps-{idx}">
    <span class="badge badge-{priority}">{PRIORITY_LABEL.get(priority, priority)}</span>
    <span class="action-title">{_esc(action.get("title", ""))}</span>
    <span class="chip-row">
      <span class="chip">Dominio: {_esc(domain_label)}</span>
      <span class="chip">Impacto: {_esc(action.get("impact", ""))}</span>
      <span class="chip">Esfuerzo: {_esc(action.get("effort", ""))}</span>
      <span class="chip">Tiempo: {_esc(action.get("time", ""))}</span>
    </span>
    <span class="chevron" aria-hidden="true">&#9662;</span>
  </button>
  <div class="action-body" id="steps-{idx}" hidden>
    <p class="why">{_esc(action.get("why", ""))}</p>
    <ol class="steps">{steps_html}</ol>
    <p class="trace">Basado en la pregunta: &ldquo;{_esc(q.question if q else "")}&rdquo;
      &mdash; NIST CSF: {_esc(nist)} &middot; CIS IG1: {_esc(cis)}</p>
  </div>
</article>'''


CSS = '''
:root {
  color-scheme: dark;
  --surface: #262626; --page: #1e1e1e; --ink: #ffffff; --ink-2: #c9c9c9;
  --ink-muted: #9a9a9a; --track: #3a3a3a; --border: rgba(255,255,255,0.12);
  --card: #2a2a2a;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--page); color: var(--ink);
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  line-height: 1.5;
}
.wrap { max-width: 880px; margin: 0 auto; padding: 32px 20px 80px; }
header.hero { display: flex; align-items: center; gap: 32px; flex-wrap: wrap;
  background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
  padding: 28px; margin-bottom: 28px; }
.hero-figure { font-size: 40px; font-weight: 600; fill: var(--ink); }
.hero-sub { font-size: 14px; fill: var(--ink-muted); }
.hero-text h1 { margin: 0 0 4px; font-size: 22px; }
.hero-text .subtitle { color: var(--ink-2); margin: 0 0 12px; font-size: 14px; }
.risk-pill { display: inline-block; padding: 6px 14px; border-radius: 999px;
  font-weight: 600; font-size: 14px; color: #fff; }
section { margin-bottom: 32px; }
h2 { font-size: 17px; margin: 0 0 14px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
.bar-label { font-size: 13px; fill: var(--ink-2); }
.bar-track { fill: var(--track); }
.bar-value { font-size: 13px; fill: var(--ink); font-weight: 600; }
.action-card { background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; margin-bottom: 10px; overflow: hidden; }
.action-header { width: 100%; text-align: left; background: none; border: none;
  color: var(--ink); cursor: pointer; padding: 16px 18px; display: flex;
  align-items: center; gap: 12px; flex-wrap: wrap; font: inherit; }
.action-title { font-weight: 600; flex: 1 1 220px; }
.chip-row { display: flex; gap: 6px; flex-wrap: wrap; }
.chip { font-size: 12px; color: var(--ink-muted); background: var(--track);
  padding: 2px 8px; border-radius: 999px; }
.badge { font-size: 12px; font-weight: 700; color: #fff; padding: 4px 10px; border-radius: 999px; }
.badge-P1 { background: #d03b3b; }
.badge-P2 { background: #fab219; color: #3a2a00; }
.badge-P3 { background: #898781; }
.chevron { transition: transform .15s ease; color: var(--ink-muted); margin-left: auto; }
.action-header[aria-expanded="true"] .chevron { transform: rotate(180deg); }
.action-body { padding: 0 18px 18px; border-top: 1px solid var(--border); }
.action-body .why { font-style: italic; color: var(--ink-2); margin: 14px 0; }
.action-body .steps { margin: 0 0 12px; padding-left: 20px; }
.action-body .steps li { margin-bottom: 6px; }
.trace { font-size: 12px; color: var(--ink-muted); margin: 0; }
footer { color: var(--ink-muted); font-size: 12px; text-align: center; margin-top: 40px; }
'''

JS = '''
document.querySelectorAll(".action-header").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var body = document.getElementById(btn.dataset.target);
    var open = btn.getAttribute("aria-expanded") === "true";
    btn.setAttribute("aria-expanded", String(!open));
    body.hidden = open;
  });
});
'''


def render_html_report(
    result: AssessmentResult,
    questions: list[Question],
    domain_labels: dict,
    business_name: str = "la PyME evaluada",
) -> str:
    question_by_id = {q.id: q for q in questions}
    color = STATUS_COLOR[result.risk_level]
    actions_html = "".join(
        _action_card(a, question_by_id, domain_labels, i)
        for i, a in enumerate(result.top_actions)
    )
    today = date.today().isoformat()

    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Informe CyberPyME — {_esc(business_name)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    {_gauge_svg(result.global_score, result.risk_level)}
    <div class="hero-text">
      <h1>Informe de autodiagnóstico &mdash; {_esc(business_name)}</h1>
      <p class="subtitle">Generado el {today} &middot; Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1</p>
      <span class="risk-pill" style="background:{color}">Riesgo {STATUS_LABEL[result.risk_level]}</span>
    </div>
  </header>

  <section>
    <h2>Score por dominio</h2>
    <div class="card">{_domain_bars_svg(result.domains, domain_labels)}</div>
  </section>

  <section>
    <h2>Acciones priorizadas &mdash; cómo resolver cada brecha</h2>
    {actions_html if actions_html else '<p class="card">Sin brechas detectadas: todas las respuestas están en línea con la metodología. 🎉</p>'}
  </section>

  <footer>
    CyberPyME &mdash; herramienta de autodiagnóstico de ciberseguridad para PyMEs sin área de IT.<br>
    Este informe no reemplaza una auditoría profesional; es un punto de partida priorizado.
  </footer>
</div>
<script>{JS}</script>
</body>
</html>'''


# Paleta categórica (skill dataviz, pasos oscuros de la referencia validada) —
# acá el color identifica al CASO (débil/medio/maduro), no al riesgo, por eso
# es categórica y no la paleta de estado.
CASE_COLOR = {"debil": "#3987e5", "medio": "#d95926", "maduro": "#199e70"}
CASE_ORDER = ["debil", "medio", "maduro"]


def _comparative_bars_svg(results: dict, domain_labels: dict) -> str:
    domains = list(next(iter(results.values()))["result"].domains.keys())
    bar_w, bar_gap, cluster_gap = 20, 2, 54
    cluster_w = len(CASE_ORDER) * bar_w + (len(CASE_ORDER) - 1) * bar_gap
    left_margin, top_margin, chart_h = 10, 26, 240
    label_area_h = 46  # espacio bajo el eje para 1 o 2 líneas de etiqueta de dominio
    width = left_margin + len(domains) * (cluster_w + cluster_gap)
    height = top_margin + chart_h + label_area_h

    bars = []
    for di, domain in enumerate(domains):
        cluster_x = left_margin + di * (cluster_w + cluster_gap)
        for ci, case_id in enumerate(CASE_ORDER):
            score = results[case_id]["result"].domains[domain].score
            bar_h = chart_h * (score / 100)
            x = cluster_x + ci * (bar_w + bar_gap)
            y = top_margin + (chart_h - bar_h)
            color = CASE_COLOR[case_id]
            bars.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" rx="3" fill="{color}"/>')
            bars.append(f'<text x="{x + bar_w / 2}" y="{max(y - 4, 12):.1f}" text-anchor="middle" class="bar-value" font-size="10">{score:.0f}</text>')

        label = domain_labels.get(domain, {}).get("label", domain)
        label_x = cluster_x + cluster_w / 2
        label_y = top_margin + chart_h + 18
        if " " in label:
            first, second = label.split(" ", 1)
            bars.append(
                f'<text x="{label_x}" y="{label_y}" text-anchor="middle" class="bar-label">'
                f'<tspan x="{label_x}" dy="0">{_esc(first)}</tspan>'
                f'<tspan x="{label_x}" dy="14">{_esc(second)}</tspan></text>'
            )
        else:
            bars.append(f'<text x="{label_x}" y="{label_y}" text-anchor="middle" class="bar-label">{_esc(label)}</text>')

    baseline_y = top_margin + chart_h
    bars.append(f'<line x1="0" y1="{baseline_y}" x2="{width}" y2="{baseline_y}" stroke="var(--track)" stroke-width="1"/>')

    return f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="Comparación de score por dominio entre los 3 casos">{"".join(bars)}</svg>'


def render_comparative_html(results: dict, domain_labels: dict) -> str:
    """results = salida de app.services.validation.run_validation()."""
    today = date.today().isoformat()

    rows = []
    for case_id in CASE_ORDER:
        c = results[case_id]
        r = c["result"]
        color = STATUS_COLOR[r.risk_level]
        rows.append(f'''
    <tr>
      <td><span class="dot" style="background:{CASE_COLOR[case_id]}"></span>{_esc(c["label"])}</td>
      <td>{_esc(c["descripcion"])}</td>
      <td class="num">{r.global_score:.2f}</td>
      <td><span class="risk-pill" style="background:{color}">{STATUS_LABEL[r.risk_level]}</span></td>
    </tr>''')

    scores = [results[c]["result"].global_score for c in CASE_ORDER]
    monotonic = scores[0] < scores[1] < scores[2]
    conclusion = (
        "El motor responde de forma coherente y monótona: a mejor postura declarada, "
        "mayor score y menor riesgo, en los tres perfiles."
        if monotonic else
        "Atención: el orden de scores no fue monótono entre los tres casos — revisar pesos o casos."
    )

    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CyberPyME — Validación con 3 casos simulados</title>
<style>{CSS}
table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 14px; }}
td.num {{ font-variant-numeric: tabular-nums; font-weight: 600; }}
.dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }}
.legend {{ display: flex; gap: 18px; margin: 10px 0 0; font-size: 13px; color: var(--ink-2); }}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero" style="display:block;">
    <h1>Validación de la metodología &mdash; 3 casos simulados de PyME</h1>
    <p class="subtitle">Generado el {today} &middot; mismo motor determinista (`app/services/scoring.py`), tres perfiles de entrada distintos</p>
  </header>

  <section>
    <h2>Resultado global por caso</h2>
    <div class="card">
      <table>
        <thead><tr><th>Caso</th><th>Descripción</th><th>Score global</th><th>Riesgo</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>
  </section>

  <section>
    <h2>Score por dominio, comparado</h2>
    <div class="card">
      {_comparative_bars_svg(results, domain_labels)}
      <div class="legend">
        {"".join(f'<span><span class="dot" style="background:{CASE_COLOR[c]}"></span>{_esc(results[c]["label"])}</span>' for c in CASE_ORDER)}
      </div>
    </div>
  </section>

  <section>
    <h2>Conclusión de la validación</h2>
    <p class="card">{_esc(conclusion)}</p>
  </section>

  <footer>
    CyberPyME &mdash; validación con casos simulados, Fase 15 del plan de trabajo.
  </footer>
</div>
</body>
</html>'''


def render_hardening_guide_html(
    questions: list[Question],
    domain_labels: dict,
    recommendations: dict,
) -> str:
    """Guía de hardening completa: las 20 recomendaciones agrupadas por
    dominio, generada directamente de recommendations.json (no depende de
    ningún autodiagnóstico puntual — es el catálogo completo)."""
    from app.services.scoring import prioritize_actions

    question_by_id = {q.id: q for q in questions}
    all_actions = prioritize_actions(questions, recommendations)

    by_domain: dict[str, list[dict]] = {}
    for a in all_actions:
        by_domain.setdefault(a["domain"], []).append(a)

    today = date.today().isoformat()
    idx = 0
    sections = []
    for domain, label_info in domain_labels.items():
        actions = by_domain.get(domain, [])
        if not actions:
            continue
        cards = []
        for a in actions:
            cards.append(_action_card(a, question_by_id, domain_labels, idx))
            idx += 1
        sections.append(f'''
  <section>
    <h2>{_esc(label_info.get("label", domain))} <span class="chip">{len(actions)} acciones</span></h2>
    {"".join(cards)}
  </section>''')

    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CyberPyME — Guía de hardening por dominio</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="hero" style="display:block;">
    <h1>Guía de hardening por dominio</h1>
    <p class="subtitle">Generado el {today} &middot; catálogo completo de {len(all_actions)} acciones, independiente de cualquier autodiagnóstico puntual &middot; Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1</p>
  </header>

  <p class="card">Esta guía reúne <strong>todas</strong> las acciones de hardening del catálogo de CyberPyME, agrupadas por dominio y ordenadas por prioridad. A diferencia del informe de autodiagnóstico (que solo muestra las brechas detectadas en una evaluación puntual), esta guía sirve como referencia permanente: úsala como checklist aunque no hayas completado el cuestionario, o como plan de trabajo completo para llevar cualquier PyME al perfil "maduro".</p>
  {"".join(sections)}

  <footer>
    CyberPyME &mdash; guía de hardening, Fase 14.1 del plan de trabajo.<br>
    Generada automáticamente a partir de <code>recommendations.json</code> &mdash; agregar una recomendación no requiere tocar esta guía.
  </footer>
</div>
<script>{JS}</script>
</body>
</html>'''
