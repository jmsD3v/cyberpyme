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
@keyframes fadeSlideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes cardIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
@keyframes softPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }
@keyframes popIn { from { opacity: 0; transform: scale(.85); } to { opacity: 1; transform: scale(1); } }

.screen { display: none; }
.screen.active { display: block; animation: fadeSlideIn .35s ease; }
.intro-card { text-align: center; padding: 44px 28px; position: relative; overflow: hidden; }
.intro-card::before { content: ""; position: absolute; inset: -40% -20% auto -20%; height: 220px;
  background: radial-gradient(closest-side, rgba(42,120,214,.35), transparent 70%); pointer-events: none; }
.intro-icon { font-size: 44px; margin-bottom: 6px; animation: softPulse 3.2s ease-in-out infinite; }
.intro-card h1 { margin: 0 0 12px; font-size: 28px; position: relative; }
.intro-card p { color: var(--ink-2); max-width: 520px; margin: 0 auto 10px; position: relative; }
.intro-card .disclaimer { font-size: 13px; color: var(--ink-muted); margin-top: 18px; position: relative; }
.domain-teaser { display: flex; justify-content: center; gap: 18px; margin: 22px 0 6px; flex-wrap: wrap; position: relative; }
.domain-teaser .d-icon-wrap { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.domain-teaser span.d-label { font-size: 11px; color: var(--ink-muted); }
.name-field { margin: 22px auto 6px; max-width: 360px; text-align: left; position: relative; }
.name-field label { display: block; font-size: 13px; color: var(--ink-2); margin-bottom: 6px; }
.name-field input { width: 100%; padding: 10px 12px; border-radius: 8px; border: 1px solid var(--border);
  background: var(--card); color: var(--ink); font: inherit; transition: border-color .15s ease; }
.name-field input:focus { outline: none; border-color: #2a78d6; }
.btn { display: inline-block; padding: 11px 22px; border-radius: 999px; border: none;
  font: inherit; font-weight: 600; cursor: pointer; font-size: 14px;
  transition: transform .12s ease, box-shadow .12s ease, filter .12s ease; }
.btn:hover:not(:disabled) { filter: brightness(1.08); transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,.25); }
.btn:active:not(:disabled) { transform: translateY(0) scale(.97); }
.btn-primary { background: #2a78d6; color: #fff; }
.btn-primary:disabled { background: var(--track); color: var(--ink-muted); cursor: not-allowed; }
.btn-secondary { background: var(--track); color: var(--ink); }
.domain-dots { display: flex; justify-content: center; gap: 10px; margin-bottom: 16px; }
.domain-dot { display: flex; flex-direction: column; align-items: center; gap: 4px; opacity: .45; transition: opacity .2s ease, transform .2s ease; }
.domain-dot.done { opacity: .85; }
.domain-dot.current { opacity: 1; transform: scale(1.12); }
.domain-dot .dot-circle { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: var(--card); border: 2px solid var(--border); }
.domain-dot.current .dot-circle { border-color: var(--accent); box-shadow: 0 0 0 4px color-mix(in srgb, var(--accent) 22%, transparent); }
.domain-dot.done .dot-circle { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 18%, var(--card)); }
.domain-dot svg { width: 16px; height: 16px; stroke: var(--ink-2); }
.domain-dot.current svg, .domain-dot.done svg { stroke: var(--accent); }
.progress-wrap { margin-bottom: 10px; }
.progress-label { font-size: 13px; color: var(--ink-2); margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.progress-label .d-icon { width: 20px; height: 20px; stroke: var(--accent); }
.progress-bar { height: 6px; border-radius: 999px; background: var(--track); overflow: hidden; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 999px; transition: width .35s ease; }
.q-row { padding: 18px 0; border-bottom: 1px solid var(--border); transition: background .15s ease; border-radius: 8px; }
.q-row:last-child { border-bottom: none; }
.q-text { margin: 0 0 6px; font-size: 15px; }
.q-help { margin: 0 0 12px; font-size: 12.5px; color: var(--ink-muted); display: flex; gap: 6px; align-items: flex-start; }
.q-help .bulb { flex-shrink: 0; }
.q-options { display: flex; gap: 8px; flex-wrap: wrap; }
.q-btn { padding: 8px 16px; border-radius: 999px; border: 1px solid var(--border);
  background: var(--card); color: var(--ink-2); font: inherit; font-size: 13px; cursor: pointer;
  transition: transform .1s ease, border-color .15s ease, background .15s ease; }
.q-btn:hover { border-color: var(--accent); transform: translateY(-1px); }
.q-btn:active { transform: translateY(0) scale(.96); }
.q-btn.selected { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600; animation: popIn .18s ease; }
.nav-row { display: flex; justify-content: space-between; align-items: center; margin-top: 24px; }
.nav-hint { font-size: 12px; color: var(--ink-muted); }
.gauge-glow { position: relative; display: inline-block; }
.gauge-glow::before { content: ""; position: absolute; inset: 10%; border-radius: 50%; filter: blur(22px); opacity: .35;
  background: var(--glow-color, #2a78d6); z-index: 0; }
.gauge-glow svg { position: relative; z-index: 1; }
.action-card { animation: cardIn .4s ease both; }
.result-emoji { font-size: 15px; margin-left: 4px; }
'''

APP_JS_TEMPLATE = r'''
const QUESTIONS = __QUESTIONS__;
const DOMAIN_LABELS = __DOMAIN_LABELS__;
const RECOMMENDATIONS = __RECOMMENDATIONS__;
const DOMAIN_ORDER = __DOMAIN_ORDER__;
const STATUS_COLOR = __STATUS_COLOR__;
const STATUS_LABEL = __STATUS_LABEL__;
const PRIORITY_LABEL = __PRIORITY_LABEL__;

// --- Identidad visual por dominio: un ícono + un color de acento fijo
// (paleta categórica dataviz, pasos oscuros) por cada uno de los 5 dominios.
const DOMAIN_ICONS = {
  accesos: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  wifi: '<path d="M2 9a16 16 0 0 1 20 0"/><path d="M5 12.5a11 11 0 0 1 14 0"/><path d="M8.5 16a6 6 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1.2" fill="currentColor" stroke="none"/>',
  backups: '<path d="M7 18a4 4 0 0 1-1-7.9A5 5 0 0 1 16 7a4.5 4.5 0 0 1 1 8.9"/><path d="M12 12v7"/><path d="M9 16l3 3 3-3"/>',
  actualizaciones: '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
  continuidad: '<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/>'
};
const DOMAIN_ACCENT = {
  accesos: "#3987e5", wifi: "#d95926", backups: "#199e70",
  actualizaciones: "#c98500", continuidad: "#9085e9"
};

function domainIconSvg(domain, size) {
  size = size || 20;
  return '<svg viewBox="0 0 24 24" width="' + size + '" height="' + size + '" fill="none" ' +
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="d-icon">' +
    (DOMAIN_ICONS[domain] || '') + '</svg>';
}

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
let lastResult = null;
const RISK_EMOJI = { BAJO: "\u{1F389}", MEDIO: "\u{1F642}", ALTO: "\u{1F61F}", CRITICO: "\u{1F6A8}" };
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

function renderDomainDots(currentDomain) {
  const currentIdx = DOMAIN_ORDER.indexOf(currentDomain);
  return '<div class="domain-dots">' + DOMAIN_ORDER.map(function (d, i) {
    const state = i < currentIdx ? "done" : (i === currentIdx ? "current" : "");
    return '<div class="domain-dot ' + state + '" title="' + esc(DOMAIN_LABELS[d].label) + '">' +
      '<span class="dot-circle">' + domainIconSvg(d, 16) + '</span></div>';
  }).join("") + '</div>';
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
    const help = q.help ? '<p class="q-help"><span class="bulb">\u{1F4A1}</span>' + esc(q.help) + '</p>' : "";
    return '<div class="q-row"><p class="q-text">' + esc(q.question) + '</p>' + help + '<div class="q-options">' + opts + "</div></div>";
  }).join("");

  const pct = Math.round(((domainIdx) / DOMAIN_ORDER.length) * 100);
  return '' +
    renderDomainDots(domain) +
    '<div class="progress-wrap">' +
    '<div class="progress-label"><span style="display:flex;align-items:center;gap:8px;">' + domainIconSvg(domain, 20) + label + '</span><span>Dominio ' + (domainIdx + 1) + ' de ' + DOMAIN_ORDER.length + '</span></div>' +
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

function gaugeSvg(riskLevel) {
  // Arranca vacío (dashoffset = circunferencia completa); animateGauge()
  // lo lleva al valor real apenas el SVG entra al DOM, para el efecto de
  // "llenado". El número también arranca en 0 y cuenta hacia arriba.
  const r = 85, circumference = 2 * Math.PI * r;
  const color = STATUS_COLOR[riskLevel];
  return '<div class="gauge-glow" style="--glow-color:' + color + '">' +
    '<svg viewBox="0 0 200 200" width="200" height="200" role="img" aria-label="Score global">' +
    '<circle cx="100" cy="100" r="' + r + '" fill="none" stroke="var(--track)" stroke-width="18"/>' +
    '<circle id="gauge-circle" cx="100" cy="100" r="' + r + '" fill="none" stroke="' + color + '" stroke-width="18" stroke-linecap="round" ' +
    'stroke-dasharray="' + circumference.toFixed(2) + '" stroke-dashoffset="' + circumference.toFixed(2) + '" transform="rotate(-90 100 100)" ' +
    'style="transition: stroke-dashoffset 1s cubic-bezier(.22,1,.36,1);"/>' +
    '<text id="gauge-num" x="100" y="94" text-anchor="middle" class="hero-figure">0</text>' +
    '<text x="100" y="122" text-anchor="middle" class="hero-sub">/100</text></svg></div>';
}

function animateGauge(score, riskLevel) {
  const r = 85, circumference = 2 * Math.PI * r;
  const target = circumference * (1 - Math.max(0, Math.min(100, score)) / 100);
  const circle = document.getElementById("gauge-circle");
  const numEl = document.getElementById("gauge-num");
  if (!circle || !numEl) return;
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { circle.style.strokeDashoffset = target.toFixed(2); });
  });
  const duration = 900, start = performance.now();
  function step(now) {
    const t = Math.min(1, (now - start) / duration);
    const eased = 1 - Math.pow(1 - t, 3);
    numEl.textContent = Math.round(score * eased);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
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
    '<article class="action-card" style="animation-delay:' + (idx * 70) + 'ms">' +
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
  lastResult = result;
  const color = STATUS_COLOR[result.risk_level];
  const actionsHtml = result.top_actions.length
    ? result.top_actions.map(function (a, i) { return actionCard(a, i); }).join("")
    : '<p class="card">Sin brechas detectadas: todas las respuestas están en línea con la metodología. \u{1F389}</p>';

  return '' +
    '<header class="hero">' + gaugeSvg(result.risk_level) +
    '<div class="hero-text"><h1>Informe de autodiagnóstico &mdash; ' + esc(displayName) + '</h1>' +
    '<p class="subtitle">Generado el ' + new Date().toISOString().slice(0, 10) + ' &middot; Metodología NIST CSF 2.0 + CIS Controls v8.1 IG1</p>' +
    '<span class="risk-pill" style="background:' + color + '">Riesgo ' + STATUS_LABEL[result.risk_level] +
    '<span class="result-emoji">' + (RISK_EMOJI[result.risk_level] || "") + '</span></span>' +
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
    document.getElementById("domain-teaser-slot").innerHTML = DOMAIN_ORDER.map(function (d, i) {
      return '<div class="d-icon-wrap" style="color:' + DOMAIN_ACCENT[d] + '">' + domainIconSvg(d, 22) +
        '<span class="d-label">' + esc(DOMAIN_LABELS[d].label) + '</span></div>';
    }).join("");
    document.getElementById("btn-start").addEventListener("click", function () {
      businessName = document.getElementById("business-name-input").value.trim();
      goToStep(1);
    });
  } else if (stepName === "resultado") {
    container.innerHTML = renderResultScreen();
    attachActionAccordion(container);
    if (lastResult) animateGauge(lastResult.global_score, lastResult.risk_level);
    document.getElementById("btn-restart").addEventListener("click", function () {
      Object.keys(answers).forEach(function (k) { delete answers[k]; });
      goToStep(0);
    });
  } else {
    container.style.setProperty("--accent", DOMAIN_ACCENT[stepName]);
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
            "recommendation_id": q.recommendation_id, "help": q.help,
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
      <div class="intro-icon">&#128737;&#65039;</div>
      <h1>CyberPyME</h1>
      <p>Autodiagnóstico de ciberseguridad para PyMEs sin área de IT. Respondé {total_q} preguntas cortas sobre accesos, WiFi, backups, actualizaciones y continuidad — vas a obtener tu score, tu nivel de riesgo y un plan de acción priorizado, todo al instante.</p>
      <div class="domain-teaser" id="domain-teaser-slot"></div>
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
