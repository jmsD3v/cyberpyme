"""
Demo de consola de CyberPyME — Fase 1-3 del plan (banco de preguntas,
scoring, motor de recomendaciones), sin depender de FastAPI ni Supabase.

Uso:
    python -m app.cli demo          -> corre con un caso simulado
    python -m app.cli interactivo   -> te pregunta dominio por dominio
    python -m app.cli validacion    -> corre los 3 casos (débil/medio/maduro)
    python -m app.cli hardening     -> genera la guía de hardening completa (requiere --html)
    python -m app.cli app           -> genera la app interactiva (cuestionario + scoring en el navegador, requiere --html)
    (agregar --html <archivo> a cualquier modo genera además el informe HTML)
"""
import sys

from app.services.interactive_app import render_interactive_app_html
from app.services.report import render_comparative_html, render_hardening_guide_html, render_html_report
from app.services.scoring import calculate_assessment, load_questions, load_recommendations
from app.services.validation import CASE_ORDER, load_validation_cases, run_validation

# Caso "medio" de validation_cases.json: PyME de 12 empleados, brechas típicas
CASO_SIMULADO = load_validation_cases()["medio"]["answers"]


def print_result(result):
    print(f"\nSCORE GLOBAL: {result.global_score}/100  ->  RIESGO {result.risk_level}\n")
    print("Score por dominio:")
    for domain, r in result.domains.items():
        print(f"  - {domain:16s} {r.score:6.2f}  ({r.risk_level})")

    print("\nTop acciones priorizadas:")
    for a in result.top_actions[:5]:
        print(f"  [{a['priority']}] {a['title']}  (impacto {a['impact']}, esfuerzo {a['effort']}, {a['time']})")


def maybe_write_html(result, html_path: str | None) -> None:
    if not html_path:
        return
    questions, domain_labels = load_questions()
    report = render_html_report(result, questions, domain_labels)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nInforme HTML generado en: {html_path}")


def run_demo(html_path: str | None = None):
    print("=== CyberPyME — Demo caso simulado (12 empleados) ===")
    result = calculate_assessment(CASO_SIMULADO)
    print_result(result)
    maybe_write_html(result, html_path)


def run_validacion(html_path: str | None = None):
    print("=== CyberPyME — Validación con 3 casos simulados ===\n")
    results = run_validation()
    for case_id in CASE_ORDER:
        c = results[case_id]
        r = c["result"]
        print(f"[{case_id.upper():7s}] {c['label']:28s} score {r.global_score:6.2f}  RIESGO {r.risk_level}")
    scores = [results[c]["result"].global_score for c in CASE_ORDER]
    monotonic = scores[0] < scores[1] < scores[2]
    print(f"\nOrden monótono (débil < medio < maduro): {'OK' if monotonic else 'FALLÓ'}")

    if html_path:
        _, domain_labels = load_questions()
        report = render_comparative_html(results, domain_labels)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nInforme comparativo generado en: {html_path}")


def run_hardening(html_path: str | None = None):
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    if not html_path:
        html_path = "guia_hardening.html"
    report = render_hardening_guide_html(questions, domain_labels, recommendations)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"=== CyberPyME — Guía de hardening ({len(recommendations)} acciones) ===")
    print(f"Generada en: {html_path}")


def run_app(html_path: str | None = None):
    questions, domain_labels = load_questions()
    recommendations = load_recommendations()
    if not html_path:
        html_path = "cyberpyme_app.html"
    report = render_interactive_app_html(questions, domain_labels, recommendations)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"=== CyberPyME — App interactiva ({len(questions)} preguntas) ===")
    print(f"Generada en: {html_path}")


def run_interactivo(html_path: str | None = None):
    questions, _ = load_questions()
    answers = {}
    print("Respondé cada pregunta: yes / partial / no / unknown\n")
    for q in questions:
        while True:
            val = input(f"[{q.domain}] {q.question} > ").strip().lower()
            if val in ("yes", "partial", "no", "unknown"):
                answers[q.id] = val
                break
            print("  respuesta inválida, usá: yes / partial / no / unknown")
    result = calculate_assessment(answers)
    print_result(result)
    maybe_write_html(result, html_path)


if __name__ == "__main__":
    args = sys.argv[1:]
    modo = args[0] if args and not args[0].startswith("--") else "demo"
    html_path = None
    if "--html" in args:
        i = args.index("--html")
        html_path = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else "informe_cyberpyme.html"
    if modo == "interactivo":
        run_interactivo(html_path)
    elif modo == "validacion":
        run_validacion(html_path)
    elif modo == "hardening":
        run_hardening(html_path)
    elif modo == "app":
        run_app(html_path)
    else:
        run_demo(html_path)
