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

La separación de **alcance** entre las dos entregas sigue en pie tal cual —
no hay que mezclar qué va en cada una. Lo que cambió es el **momento**: ver
"⚠️ Pivot de ritmo" más abajo, ambas se están construyendo ya, en paralelo.

## Estado actual (al 03/09/2026 — código real, ver nota de ritmo abajo)

Ya construido y funcionando (`backend/`):

- `app/data/questions.json` — **24** preguntas, 5 dominios (accesos, wifi,
  backups, actualizaciones, continuidad), con peso, mapeo NIST/CIS y
  `recommendation_id`. Auditado 2026-09-03 en dos pasadas contra NIST CSF
  2.0 (6 funciones) y los 15 controles de CIS Controls v8.1 aplicables a
  IG1 — faltaban malware defenses/antivirus (Control 10), USB/removable
  media (Safeguard 10.3, específicamente IG1), concientización de phishing
  (Control 14, pese a que "Phishing" ya estaba marcado como riesgo
  "Crítica" en la matriz de la sección 5 del documento técnico) y cifrado
  de disco en notebooks (Control 3, Protección de Datos). Se agregaron
  `ACC-06` (phishing), `UPD-04` (antivirus), `UPD-05` (USB) y `UPD-06`
  (cifrado de disco) — no se creó un 6to dominio a propósito, por
  KISS/YAGNI y para no rebalancear los `domain_weight` (25/15/25/15/20) ni
  reestructurar el documento técnico otra vez. Resto de controles IG1
  (logs, monitoreo de red, seguridad de apps, pentesting) quedan fuera de
  alcance a propósito — exceden lo sostenible para una PyME sin área de IT.
- `app/data/recommendations.json` — 24 recomendaciones con prioridad
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
  con chequeo de orden monótono (`is_monotonic`). Resultado real (tras la
  auditoría del cuestionario, ver abajo): débil 1.36/100 CRÍTICO → medio
  37.92/100 CRÍTICO → maduro 89.45/100 BAJO.
- `app/services/report.py` → `render_comparative_html()` — informe HTML
  comparativo de los 3 casos (tabla + gráfico de barras agrupadas por
  dominio, paleta categórica de `dataviz`, conclusión automática).
- `app/services/report.py` → `render_hardening_guide_html()` — guía de
  hardening completa (las 24 acciones, agrupadas por dominio), generada
  reusando `prioritize_actions()` sobre **todas** las preguntas en vez de
  solo las brechas de una evaluación puntual — no depende de ningún
  autodiagnóstico.
- `app/services/interactive_app.py` → `render_interactive_app_html()`
  (nuevo 2026-09-03) — **la app de verdad**: un único HTML donde el
  cuestionario se responde EN EL NAVEGADOR (5 pantallas, una por dominio,
  con barra de progreso) y el resultado (gauge + barras + acordeón) se
  calcula ahí mismo, sin Python. El motor de scoring está portado a JS
  puro como espejo deliberado de `scoring.py` (mismo algoritmo, mismos
  nombres en camelCase) — si `scoring.py` cambia, este archivo se
  actualiza a mano, no hay build step que los mantenga sincronizados
  automáticamente. Reusa el `CSS`/paleta de `report.py`. Verificado de
  punta a punta en el navegador: intro → 5 dominios → resultado →
  reiniciar, cero errores de consola, cero llamadas de red.
  **Pulida 2026-09-03 (feedback directo del usuario tras probarla):**
  (1) 6 preguntas con jerga técnica (MFA, gestor de contraseñas,
  privilegios de administrador, WPA2/WPA3, estrategia 3-2-1, cifrado de
  disco) ahora tienen un campo `help` en `questions.json` con una
  aclaración en criollo, mostrada con 💡 debajo de la pregunta en el
  cuestionario; (2) pase de diseño: ícono + color de acento propio por
  dominio (candado/wifi/nube/escudo/reciclaje, paleta categórica
  `dataviz`), fila de 5 "domain dots" mostrando el progreso real (no solo
  una barra), transición fade+slide entre pantallas, el gauge del
  resultado ahora arranca vacío y se llena animado (arco + número
  contando hacia arriba) en vez de aparecer ya completo, tarjetas de
  acciones con entrada escalonada, emoji según nivel de riesgo, glow
  radial detrás del gauge, micro-interacciones de hover/press en botones.
- `app/cli.py` — demo de consola (`python -m app.cli demo` /
  `interactivo` / `validacion` / `hardening` / `app`), con flag
  `--html <path>` en cualquier modo para generar también el HTML
  correspondiente.
- `tests/test_scoring.py` (10) + `tests/test_report.py` (4) +
  `tests/test_validation.py` (4) + `tests/test_hardening.py` (3) +
  `tests/test_interactive_app.py` (4) — **25/25 pasando**.

**No existe todavía:** documentación final/manual de uso.

**Repositorio:** [github.com/jmsD3v/cyberpyme](https://github.com/jmsD3v/cyberpyme)
(privado, creado 2026-09-03).

## Fase producto — construida y verificada 2026-09-03 (`backend/api.py` + `frontend/`)

Ya no está pausada hasta después del 13/dic — ver el pivot de ritmo más
abajo. Arquitectura, deliberada:

- **Supabase** (multi-tenant, RLS real): `empresas` / `perfiles` /
  `evaluaciones`, todas con RLS. Alta atómica de empresa vía RPC
  `crear_empresa(p_nombre)` (`SECURITY DEFINER`) — evita una condición de
  carrera de secuestro de tenant que existiría con inserts separados. Sin
  políticas de INSERT directo en `empresas`/`perfiles`, solo vía la RPC.
- **FastAPI** (`backend/api.py`) — microservicio de **cómputo puro** sobre
  el mismo `calculate_assessment()` de `app/services/scoring.py` (una sola
  fuente de verdad para el motor). No sabe nada de auth ni persistencia:
  eso lo maneja Next.js hablando directo con Supabase, protegido por RLS.
  Correr: `cd backend && uvicorn api:app --reload --port 8000`.
- **Next.js 16 + TypeScript + Tailwind v4** (`frontend/`) — App Router,
  `@supabase/ssr`. Ojo con `frontend/AGENTS.md`: Next 16 tiene breaking
  changes reales respecto a versiones anteriores (`middleware.ts` se
  renombró a `proxy.ts`, función `proxy` en vez de `middleware`, `cookies()`
  async, etc.) — leer `node_modules/next/dist/docs/` antes de tocar código
  nuevo ahí, no confiar en el entrenamiento previo.
  Correr: `cd frontend && pnpm dev` (puerto 3000, necesita `backend/api.py`
  corriendo en el 8000 y `.env.local` con las credenciales de Supabase).
- **Verificado de punta a punta en el navegador** (no solo tests):
  registro → confirmación de email → login → alta de empresa → cuestionario
  de 24 preguntas → `/evaluar` (FastAPI) → insert en `evaluaciones`
  (Supabase, cliente browser, respetando RLS) → resultado renderizado
  (gauge animado, barras por dominio, acordeón de acciones). Cero errores
  de consola bloqueantes.
- **Pendiente:** tipos TypeScript generados de Supabase (hoy hay un par de
  casteos manuales en los joins de `page.tsx`/`cuestionario/page.tsx`),
  página de guía de hardening en el frontend, manejo de errores más
  robusto.

## ⚠️ Ritmo de publicación — NO confundir "hecho en el código" con "mostrado en clase"

El desarrollo real va más rápido que el cronograma de clases. Eso está bien
para el código, pero:

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

## ⚠️ Pivot de ritmo (2026-09-03) — leer antes de asumir "recién después del 13/dic"

Juanma pidió explícitamente terminar **todo el proyecto**, no solo la
entrega académica, lo antes posible — no esperar al 13/dic para arrancar la
fase producto. Cita textual: *"no puedo estar sin desarrollar ni esperando
a las fechas para eso"* / *"cuando hablo de terminar ya, me refiero a todo
el proyecto, lo antes posible"*. Esto reemplaza cualquier plan anterior que
dijera "fase producto recién después de la entrega académica" — la
separación de *alcance* entre ambas entregas sigue firme, pero el
*calendario de desarrollo* ya no las secuencia. Lo único que sigue atado al
cronograma de clases es qué se **muestra en Notion**, no qué se construye
(ver sección de ritmo de publicación arriba).

## Próximos pasos, en este orden

1. **Documentación final + manual de uso**, sin artefactos de generación de
   IA sin limpiar (nada de texto tipo `fileciteturn0file0` — ya pasó una
   vez en el documento técnico, revisar siempre antes de enviar nada).
   Due Notion: 2026-11-04. Mencionar la app interactiva también acá.
   Deliberadamente no arrancada todavía — falta más de 2 meses y el
   proyecto va a seguir cambiando mucho más que hasta ahora.
2. Fase producto: núcleo ya construido y verificado (ver sección arriba) —
   lo que queda es pulido (tipos generados, página de hardening, manejo de
   errores), no las piezas grandes.

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

python -m pytest tests/ -v                          # 25 tests
python -m app.cli app --html cyberpyme_app.html     # LA APP: cuestionario + resultado en el navegador
python -m app.cli demo                              # demo con caso simulado
python -m app.cli interactivo                       # demo pregunta por pregunta
python -m app.cli validacion                        # corre los 3 casos débil/medio/maduro
python -m app.cli hardening --html guia.html        # guía de hardening completa (24 acciones)
python -m app.cli demo --html informe.html          # + informe HTML interactivo
python -m app.cli validacion --html comparativa.html  # + informe comparativo
```
