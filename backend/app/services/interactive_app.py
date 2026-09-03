"""
App interactiva de autodiagnóstico — CyberPyME.

Genera un único archivo .html autocontenido donde el cuestionario se
responde EN EL NAVEGADOR: el motor de scoring (scoring.py) se porta a
JavaScript puro y corre del lado del cliente, con las preguntas y
recomendaciones embebidas como datos. Cero backend, cero build step, sigue
cumpliendo la restricción académica de "corre sola, sin infraestructura" —
pero a diferencia de report.py (que solo puede RENDERIZAR un resultado ya
calculado en Python), esta es la primera pieza que se puede abrir y usar de
punta a punta sin tocar la terminal.

La lógica de scoring en JS (abajo, en el template) es un espejo deliberado
de app/services/scoring.py: mismo algoritmo, mismos nombres de función
traducidos a camelCase. Si scoring.py cambia, este archivo hay que
actualizarlo a mano — no hay forma de compartir código Python/JS sin un
build step, y eso violaría la restricción de "sin infraestructura".
"""
from __future__ import annotations

import json

from app.models.question import Question
from app.services.report import CSS as BASE_CSS
from app.services.report import PRIORITY_LABEL, STATUS_COLOR, STATUS_LABEL

APP_CSS = '''
.screen { display: none; }
.screen.active { display: block; }
.intro-card { text-align: center; padding: 40px 28px; }
.intro-card h1 { margin: 0 0 12px; font-size: 26px; }
.intro-card p { color: var(--ink-2); max-width: 520px; margin: 0 auto 10px; }
.intro-card .disclaimer { font-size: 13px; color: var(--ink-muted); margin-top: 18px; }
.name-field { margin: 22px auto 6px; max-width: 360px; text-align: left; }
.name-field label { display: block; font-size: 13px; color: var(--ink-2); margin-bottom: 6px; }
.name-field input { width: 100%; padding: 10px 12px; border-radius: 8px; border: 1px solid var(--border);
  background: var(--card); color: var(--ink); font: inherit; }
.btn { display: inline-block; padding: 11px 22px; border-radius: 999px; border: none;
  font: inherit; font-weight: 600; cursor: pointer; font-size: 14px; }
.btn-primary { background: #2a78d6; color: #fff; }
.btn-primary:disabled { background: var(--track); color: var(--ink-muted); cursor: not-allowed; }
.btn-secondary { background: var(--track); color: var(--ink); }
.progress-wrap { margin-bottom: 22px; }
.progress-label { font-size: 13px; color: var(--ink-2); margin-bottom: 8px; display: flex; justify-content: space-between; }
.progress-bar { height: 6px; border-radius: 999px; background: var(--track); overflow: hidden; }
.progress-fill { height: 100%; background: #2a78d6; border-radius: 999px; transition: width .25s ease; }
.q-row { padding: 18px 0; border-bottom: 1px solid var(--border); }
.q-row:last-child { border-bottom: none; }
.q-text { margin: 0 0 12px; font-size: 15px; }
.q-options { display: flex; gap: 8px; flex-wrap: wrap; }
.q-btn { padding: 8px 16px; border-radius: 999px; border: 1px solid var(--border);
  background: var(--card); color: var(--ink-2); font: inherit; font-size: 13px; cursor: pointer; }
.q-btn.selected { background: #2a78d6; border-color: #2a78d6; color: #fff; font-weight: 600; }
.nav-row { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; }
.nav-hint { font-size: 12px; color: var(--ink-muted); }
'''

APP_JS_TEMPLATE = r'''
const QUESTIONS = __QUESTIONS__;
const DOMAIN_LABELS = __DOMAIN_LABELS__;
const RECOMMENDATIONS = __RECOMMENDATIONS__;
const DOMAIN_ORDER = __DOMAIN_ORDER__;
const STATUS_COLOR = __STATUS_COLOR__;
const STATUS_LABEL = __STATUS_LABEL__;
const PRIORITY_LABEL = __PRIORITY_LABEL__;

// --- Motor de scoring (espejo de app/services/scoring.py) ---
const ANSWER_VALUES = { yes: 1.0, partial: 0.5, no: 0.0, unknown: 0.0 };

function weightedScore(pairs) {
  const totalWeight = pairs.reduce((s, p) => s + p[1], 0);
  if (!totalWeight) return 0.0;
  const raw = pairs.reduce((s, p) => s + p[0] * p[1], 0);
  return Math.round((raw / totalWeight * 100) * 100) / 100;
}

function riskLevelFor(score) {
  if (score >= 80) return "BAJO";
  if (score >= 60) return "MEDIO";
  if (score >= 40) return "ALTO";
  return "CRITICO";
}

function scoreByDomain(questions, answers) {
  const byDomain = {};
  for (const q of questions) {
    const val = answers[q.id];
    if (val === undefined) continue;
    if (!byDomain[q.domain]) byDomain[q.domain] = [];
    byDomain[q.domain].push([ANSWER_VALUES[val], q.weight]);
  }
  const results = {};
  for (const domain in byDomain) {
    const score = weightedScore(byDomain[domain]);
    results[domain] = { domain: domain, score: score, risk_level: riskLevelFor(score) };
  }
  return results;
}

function scoreGlobal(domainResults, domainWeights) {
  const pairs = [];
  for (const domain in domainResults) {
    if (domainWeights[domain]) {
      pairs.push([domainResults[domain].score / 100, domainWeights[domain].domain_weight]);
    }
  }
  return weightedScore(pairs);
}

function findGaps(questions, answers) {
  return questions.filter(function (q) {
    const v = answers[q.id];
    return v === "no" || v === "unknown" || v === "partial";
  });
}

function prioritizeActions(gaps, recommendations) {
  const priorityOrder = { P1: 0, P2: 1, P3: 2 };
  const actions = gaps.map(function (q) {
    const rec = recommendations[q.recommendation_id];
    if (!rec) return null;
    return Object.assign({}, rec, { question_id: q.id, risk: q.risk, _weight: q.weight });
  }).filter(function (a) { return a !== null; });
  actions.sort(function (a, b) {
    const pa = priorityOrder[a.priority] ?? 9, pb = priorityOrder[b.priority] ?? 9;
    if (pa !== pb) return pa - pb;
    return b._weight - a._weight;
  });
  return actions;
}

function calculateAssessment(answersRaw) {
  const domainResults = scoreByDomain(QUESTIONS, answersRaw);
  const globalScore = scoreGlobal(domainResults, DOMAIN_LABELS);
  const gaps = findGaps(QUESTIONS, answersRaw);
  const topActions = prioritizeActions(gaps, RECOMMENDATIONS);
  return {
    global_score: globalScore,
    risk_level: riskLevelFor(globalScore),
    domains: domainResults,
    top_actions: topActions,
  };
}

// --- Estado y navegación ---
const answers = {};
let currentStep = 0; // 0 = intro, 1..N = dominios, N+1 = resultado
let businessName = "";
const steps = ["intro"].concat(DOMAIN_ORDER).concat(["resultado"]);

function esc(s) {
  const d = document.createElement("div");
  d.textContent = String(s);
  return d.innerHTML;
}

function questionsForDomain(domain) {
  return QUESTIONS.filter(function (q) { return q.domain === domain; });
}

function domainComplete(domain) {
  return questionsForDomain(domain).every(function (q) { return answers[q.id] !== undefined; });
}

function renderDomainScreen(domain) {
  const qs = questionsForDomain(domain);
  const label = DOMAIN_LABELS[domain].label;
  const domainIdx = DOMAIN_ORDER.indexOf(domain);
  const rows = qs.map(function (q) {
    const opts = ["yes", "partial", "no", "unknown"].map(function (val) {
      const optLabel = { yes: "Sí", partial: "Parcial", no: "No", unknown: "No sé" }[val];
      const sel = answers[q.id] === val ? " selected" : "";
      return '<button type="button" class="q-btn' + sel + '" data-qid="' + q.id + '" data-val="' + val + '">' + optLabel + "</button>";
    }).join("");
    return '<div class="q-row"><p class="q-text">' + esc(q.question) + '</p><div class="q-options">' + opts + "</div></div>";
  }).join("");

  const pct = Math.round(((domainIdx) / DOMAIN_ORDER.length) * 100);
  return '' +
    '<div class="progress-wrap">' +
    '<div class="progress-label"><span>' + label + '</span><span>Dominio ' + (domainIdx + 1) + ' de ' + DOMAIN_ORDER.length + '</span></div>' +
    '<div class="progress-bar"><div class="progress-fill" style="width:' + pct + '%"></div></div>' +
    '</div>' +
    '<div class="card">' + rows + '</div>' +
    '<div class="nav-row">' +
    '<button type="button" class="btn btn-secondary" id="btn-prev">Anterior</button>' +
    '<span class="nav-hint" id="nav-hint"></span>' +
    '<button type="button" class="btn btn-primary" id="btn-next" disabled>' +
    (domainIdx === DOMAIN_ORDER.length - 1 ? "Ver resultado" : "Siguiente") +
    '</button>' +
    '</div>';
}

function gaugeSvg(score, riskLevel) {
  const r = 85, circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - Math.max(0, Math.min(100, score)) / 100);
  const color = STATUS_COLOR[riskLevel];
  return '<svg viewBox="0 0 200 200" width="200" height="200" role="img" aria-label="Score global">' +
    '<circle cx="100" cy="100" r="' + r + '" fill="none" stroke="var(--track)" stroke-width="18"/>' +
    '<circle cx="100" cy="100" r="' + r + '" fill="none" stroke="' + color + '" stroke-width="18" stroke-linecap="round" ' +
    'stroke-dasharray="' + circumference.toFixed(2) + '" stroke-dashoffset="' + offset.toFixed(2) + '" transform="rotate(-90 100 100)"/>' +
    '<text x="100" y="94" text-anchor="middle" class="hero-figure">' + Math.round(score) + '</text>' +
    '<text x="100" y="122" text-anchor="middle" class="hero-sub">/100</text></svg>';
}

function domainBarsSvg(domainResults) {
  const rowH = 40, barH = 22, maxW = 380, left = 140;
  const domains = DOMAIN_ORDER;
  const height = rowH * domains.length + 10;
  let rows = "";
  domains.forEach(function (domain, i) {
    const r = domainResults[domain];
    const y = 10 + i * rowH;
    const barW = maxW * (r.score / 100);
    const color = STATUS_COLOR[r.risk_level];
    const label = DOMAIN_LABELS[domain].label;
    rows += '<text x="0" y="' + (y + barH / 2 + 4) + '" class="bar-label">' + esc(label) + '</text>' +
      '<rect x="' + left + '" y="' + y + '" width="' + maxW + '" height="' + barH + '" rx="4" class="bar-track"/>' +
      '<rect x="' + left + '" y="' + y + '" width="' + barW.toFixed(1) + '" height="' + barH + '" rx="4" fill="' + color + '"/>' +
      '<text x="' + (left + maxW + 10) + '" y="' + (y + barH / 2 + 4) + '" class="bar-value">' + Math.round(r.score) + '</text>';
  });
  return '<svg viewBox="0 0 ' + (left + maxW + 50) + ' ' + height + '" width="100%" role="img" aria-label="Score por dominio">' + rows + '</svg>';
}

function actionCard(action, idx) {
  const q = QUESTIONS.find(function (qq) { return qq.id === action.question_id; });
  const domainLabel = DOMAIN_LABELS[action.domain] ? DOMAIN_LABELS[action.domain].label : action.domain;
  const nist = q ? q.nist.join(", ") : "";
  const cis = q ? q.cis.join(", ") : "";
  const stepsHtml = (action.steps || []).map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("");
  const priority = action.priority || "P3";
  return '' +
    '<article class="action-card">' +
    '<button class="action-header" aria-expanded="false" data-target="steps-' + idx + '">' +
    '<span class="badge badge-' + priority + '">' + (PRIORITY_LABEL[priority] || priority) + '</span>' +
    '<span class="action-title">' + esc(action.title || "") + '</span>' +
    '<span class="chip-row">' +
    '<span class="chip">Dominio: ' + esc(domainLabel) + '</span>' +
    '<span class="chip">Impacto: ' + esc(action.impact || "") + '</span>' +
    '<span class="chip">Esfuerzo: ' + esc(action.effort || "") + '</span>' +
    '<span class="chip">Tiempo: ' + esc(action.time || "") + '</span>' +
    '</span><span class="chevron" aria-hidden="true">&#9662;</span></button>' +
    '<div class="action-body" id="steps-' + idx + '" hidden>' +
    '<p class="why">' + esc(action.why || "") + '</p>' +
    '<ol class="steps">' + stepsHtml + '</ol>' +
    '<p class="trace">Basado en la pregunta: &ldquo;' + esc(q ? q.question : "") + '&rdquo; &mdash; NIST CSF: ' + esc(nist) + ' &middot; CIS IG1: ' + esc(cis) + '</p>' +
    '</div></article>';
}

function renderResultScreen() {
  const displayName = businessName || "la PyME evaluada";
  const result = calculateAssessment(answers);
  const color = STATUS_COLOR[result.risk_level];
  const actionsHtml = result.top_actions.length
    ? result.top_actions.map(function (a, i) { return actionCard(a, i); }).join("")
    : '<p class="card">Sin brechas detectadas: todas las respuestas están en línea con la metodología. \u{1F389}</p>';

  return '' +
    '<header class="hero">' + gaugeSvg(result.global_score, result.risk_level) +
    '<div class="hero-text"><h1>Informe de autodiagnóstico &mdash; ' + esc(displayName) + '</h1>' +
    '<p class="subtitle">Generado el ' + new Date().toISOString().slice(0, 10) + ' &middot; Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1</p>' +
    '<span class="risk-pill" style="background:' + color + '">Riesgo ' + STATUS_LABEL[result.risk_level] + '</span>' +
    '</div></header>' +
    '<section><h2>Score por dominio</h2><div class="card">' + domainBarsSvg(result.domains) + '</div></section>' +
    '<section><h2>Acciones priorizadas &mdash; cómo resolver cada brecha</h2>' + actionsHtml + '</section>' +
    '<div class="nav-row"><button type="button" class="btn btn-secondary" id="btn-restart">Volver a empezar</button><span></span><span></span></div>';
}

function attachActionAccordion(root) {
  root.querySelectorAll(".action-header").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const body = document.getElementById(btn.dataset.target);
      const open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      body.hidden = open;
    });
  });
}

function goToStep(step) {
  currentStep = step;
  const container = document.getElementById("app-root");
  const stepName = steps[step];

  if (stepName === "intro") {
    container.innerHTML = document.getElementById("intro-template").innerHTML;
    document.getElementById("btn-start").addEventListener("click", function () {
      businessName = document.getElementById("business-name-input").value.trim();
      goToStep(1);
    });
  } else if (stepName === "resultado") {
    container.innerHTML = renderResultScreen();
    attachActionAccordion(container);
    document.getElementById("btn-restart").addEventListener("click", function () {
      Object.keys(answers).forEach(function (k) { delete answers[k]; });
      goToStep(0);
    });
  } else {
    container.innerHTML = renderDomainScreen(stepName);
    wireDomainScreen(stepName);
  }
  window.scrollTo(0, 0);
}

function wireDomainScreen(domain) {
  const container = document.getElementById("app-root");
  container.querySelectorAll(".q-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      answers[btn.dataset.qid] = btn.dataset.val;
      container.querySelectorAll('.q-btn[data-qid="' + btn.dataset.qid + '"]').forEach(function (b) {
        b.classList.toggle("selected", b === btn);
      });
      updateNextEnabled(domain);
    });
  });
  document.getElementById("btn-prev").addEventListener("click", function () { goToStep(currentStep - 1); });
  document.getElementById("btn-next").addEventListener("click", function () { goToStep(currentStep + 1); });
  updateNextEnabled(domain);
}

function updateNextEnabled(domain) {
  const btn = document.getElementById("btn-next");
  const complete = domainComplete(domain);
  btn.disabled = !complete;
  document.getElementById("nav-hint").textContent = complete ? "" : "Respondé todas las preguntas para continuar";
}

goToStep(0);
'''


def render_interactive_app_html(
    questions: list[Question],
    domain_labels: dict,
    recommendations: dict,
) -> str:
    """App interactiva: cuestionario + scoring + informe, todo en el
    navegador, sin backend. `questions`/`domain_labels`/`recommendations`
    se embeben como datos; el motor de scoring está portado a JS (ver
    APP_JS_TEMPLATE) como espejo de scoring.py."""
    questions_json = [
        {
            "id": q.id, "domain": q.domain, "question": q.question,
            "weight": q.weight, "risk": q.risk, "nist": q.nist, "cis": q.cis,
            "recommendation_id": q.recommendation_id,
        }
        for q in questions
    ]
    domain_order = list(domain_labels.keys())

    js = (
        APP_JS_TEMPLATE
        .replace("__QUESTIONS__", json.dumps(questions_json, ensure_ascii=False))
        .replace("__DOMAIN_LABELS__", json.dumps(domain_labels, ensure_ascii=False))
        .replace("__RECOMMENDATIONS__", json.dumps(recommendations, ensure_ascii=False))
        .replace("__DOMAIN_ORDER__", json.dumps(domain_order, ensure_ascii=False))
        .replace("__STATUS_COLOR__", json.dumps(STATUS_COLOR, ensure_ascii=False))
        .replace("__STATUS_LABEL__", json.dumps(STATUS_LABEL, ensure_ascii=False))
        .replace("__PRIORITY_LABEL__", json.dumps(PRIORITY_LABEL, ensure_ascii=False))
    )

    total_q = len(questions)

    return f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CyberPyME — Autodiagnóstico interactivo</title>
<style>{BASE_CSS}{APP_CSS}</style>
</head>
<body>
<div class="wrap">
  <div id="app-root" class="screen active"></div>

  <template id="intro-template">
    <div class="card intro-card">
      <h1>CyberPyME</h1>
      <p>Autodiagnóstico de ciberseguridad para PyMEs sin área de IT. Respondé {total_q} preguntas cortas sobre accesos, WiFi, backups, actualizaciones y continuidad — vas a obtener tu score, tu nivel de riesgo y un plan de acción priorizado, todo al instante.</p>
      <div class="name-field">
        <label for="business-name-input">Nombre de tu empresa (opcional)</label>
        <input type="text" id="business-name-input" placeholder="Ej: Ferretería Don José">
      </div>
      <button type="button" class="btn btn-primary" id="btn-start">Comenzar</button>
      <p class="disclaimer">Esto no reemplaza una auditoría profesional. Tarda unos 5 minutos. Nada de lo que respondas sale de tu navegador — no hay backend ni se envía a ningún servidor.</p>
    </div>
  </template>

  <footer>
    CyberPyME &mdash; herramienta de autodiagnóstico de ciberseguridad para PyMEs sin área de IT.<br>
    Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1.
  </footer>
</div>
<script>{js}</script>
</body>
</html>'''
