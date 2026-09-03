# Bitácora interna (staging) — CyberPyME

**Esto NO es lo que está publicado en Notion.** Es el registro real de avance,
fecha por fecha, que se usa como borrador para saber **qué corresponde
publicar en la Bitácora de Notion y qué tarea marcar Finalizada cuando
llegue la fecha real de esa jornada** — aunque el trabajo ya esté terminado
hoy.

**Regla:** avanzamos el código a la velocidad que dé. Pero en Notion (Bitácora
+ Tareas) solo se muestra, en cada jornada Lunes/Miércoles, lo que
correspondería a ese día según el cronograma — nunca antes. Cuando llega la
fecha real: copiar la entrada de "Pendientes de publicar" de más abajo al
tope de la Bitácora de Notion, y cambiar el Estado de la tarea asociada a
Finalizada. Ver `feedback-cyberpyme-notion-pacing` en la memoria de Claude
para el porqué.

---

## Pendientes de publicar (ya construido, esperando la fecha real)

### Jornada 8 — 09/09/2026 (miércoles) — publicar ese día
**Tarea Notion asociada:** "Informe automático (Markdown/PDF con resumen ejecutivo)" → cambiar Estado a Finalizada ese día.

**Enfoque:** informe automático interactivo — de "diagnóstico" a "diagnóstico + cómo resolverlo".
**Qué se construyó:**
- `app/services/report.py`: genera un único `.html` autocontenido (sin backend, sin CDN) a partir de `AssessmentResult` — gauge de score global + barras por dominio (SVG, coloreadas por nivel de riesgo) + acordeón de acciones priorizadas.
- `recommendations.json` enriquecido: las 20 recomendaciones ahora tienen `why` (por qué importa) y `steps` (guía de resolución paso a paso, en criollo, sin jerga técnica) — esto es lo que convierte el informe en algo que ayuda a *resolver*, no solo a *diagnosticar*.
- Tema oscuro (gris, no negro) por defecto.
- 4 tests nuevos (`tests/test_report.py`), incluyendo uno de que el nombre de la empresa se escapa correctamente (XSS) pensando en la fase producto. Total: **14/14 tests en verde**.
- Uso: `python -m app.cli demo --html informe.html`.
**Por qué así:** configuración sobre código (preguntas, pesos y ahora también los pasos de resolución viven en JSON), scoring desacoplado de la interfaz, determinismo total. El informe interactivo responde a la necesidad de que la PyME no solo se autodiagnostique sino que sepa cómo resolver cada brecha — sin salir de la restricción de "corre sola, sin infraestructura" de la entrega académica.
**Para mostrar en clase:**
- Correr `python -m app.cli demo` en vivo — score global 42.61/100, RIESGO ALTO, top 5 acciones priorizadas.
- Abrir el `.html` generado en el navegador — mostrar el gauge, las barras por dominio y desplegar el acordeón de una acción P1 para ver la guía paso a paso.
- Correr `python -m pytest tests/ -v` — 14 passed.
**Próximo objetivo (a publicar cuando corresponda):** validación con 3 casos simulados de PyME (perfil maduro, medio, débil).

---

### Jornada 9 — 14/09/2026 (lunes) — publicar ese día
**Tarea Notion asociada:** "Validación con 3 casos simulados de PyME" → cambiar Estado a Finalizada ese día.

**Enfoque:** validar que el motor de scoring responde de forma coherente y monótona ante perfiles de postura de seguridad claramente distintos.
**Qué se construyó:**
- `app/data/validation_cases.json`: 3 perfiles simulados — *débil* (sin prácticas básicas), *medio* (el mismo caso de la demo, PyME de 12 empleados), *maduro* (buenas prácticas ya instaladas).
- `app/services/validation.py`: corre los 3 casos sobre el mismo motor (`calculate_assessment`) y verifica el orden monótono de scores (`is_monotonic`).
- `app/services/report.py` → `render_comparative_html()`: informe HTML comparativo con tabla de resultados, gráfico de barras agrupadas por dominio (3 series, paleta categórica de la skill `dataviz`) y conclusión automática.
- CLI: `python -m app.cli validacion [--html archivo.html]`.
- 4 tests nuevos (`tests/test_validation.py`): cubren los 3 casos con las 20 preguntas, orden monótono débil<medio<maduro, más brechas en débil que en maduro, y que el HTML comparativo renderiza los 3 casos. Total: **18/18 tests en verde**.
- Resultado real obtenido: débil 3.00/100 (CRÍTICO) → medio 42.61/100 (ALTO) → maduro 87.85/100 (BAJO). Orden monótono: OK.
- (03/09) Corregidos 2 bugs visuales del gráfico comparativo: la etiqueta "100" se cortaba arriba (falta de margen superior) y las etiquetas largas de dominio ("Continuidad Operativa") se pisaban con la del dominio vecino — ahora las etiquetas de dos palabras parten en dos líneas.
**Por qué así:** reutiliza el mismo motor determinista sin duplicar lógica de scoring; los 3 perfiles viven en JSON (config sobre código), igual que preguntas y recomendaciones. La validación demuestra empíricamente — no solo por argumento — que mejor postura declarada = mejor score = menor riesgo, en los 5 dominios y en el global.
**Para mostrar en clase:**
- Correr `python -m app.cli validacion` en vivo — muestra los 3 scores y confirma el orden monótono.
- Abrir el HTML comparativo — tabla + gráfico de barras agrupadas por dominio.
- Correr `python -m pytest tests/ -v` — 18 passed.
**Próximo objetivo (a publicar cuando corresponda):** guía de hardening por dominio como documento (due 16/09).

---

### Jornada 10 — 16/09/2026 (miércoles) — publicar ese día
**Tarea Notion asociada:** "Guía de hardening por dominio (documento)" → cambiar Estado a Finalizada ese día.

**Enfoque:** documentar la guía de hardening completa, generada del catálogo en vez de escrita a mano.
**Qué se construyó:**
- `app/services/report.py` → `render_hardening_guide_html()`: reutiliza `prioritize_actions()` pasándole **todas** las preguntas (no solo brechas de una evaluación puntual) para generar el catálogo completo de las 20 acciones, agrupadas por dominio y ordenadas por prioridad — mismo componente visual (acordeón con `why`+`steps`) que el informe de autodiagnóstico.
- CLI: `python -m app.cli hardening --html guia.html`.
- 3 tests nuevos (`tests/test_hardening.py`): las 20 recomendaciones aparecen, los 5 dominios aparecen, y la guía no depende de ningún `AssessmentResult`. Total: **21/21 tests en verde**.
**Por qué así:** la guía de hardening y el informe de autodiagnóstico son la misma pregunta ("¿cómo resuelvo esto?") aplicada a dos universos distintos (todas las acciones vs. solo las brechas detectadas) — reusar `prioritize_actions()` y `_action_card()` evita duplicar la lógica de priorización y el diseño de las tarjetas.
**Para mostrar en clase:**
- Correr `python -m app.cli hardening` en vivo — genera el HTML con las 20 acciones.
- Abrir el HTML — mostrar las 5 secciones por dominio y desplegar alguna tarjeta.
- Correr `python -m pytest tests/ -v` — 21 passed.
**Próximo objetivo (a publicar cuando corresponda):** documentación final + manual de uso (due 04/11).

---

## Ya publicado en Notion (histórico, para referencia — no duplicar)

### Jornada 6 — 02/09/2026 (miércoles)
Primer vertical slice funcional: banco de 20 preguntas (`questions.json`), motor de scoring determinista, motor de recomendaciones, 10 tests, demo de consola. Score global 42.61/100, RIESGO ALTO sobre el caso simulado de 12 empleados.

### Jornada 5 — 31/08/2026 (lunes)
Diseño final del cuestionario por dominio (escala Sí/Parcial/No/No sé) + plan de desarrollo con cronograma por sprint + backlog priorizado P0-P3 + Definition of Done del MVP.

### Jornada 4 — 26/08/2026 (miércoles)
Arquitectura en capas (metodología en JSON/Git vs. datos operativos en DB) + stack definido (Python puro para la entrega académica; Next.js+TypeScript+Tailwind+FastAPI+Supabase reservado para la fase producto).

### Jornada 3 — 24/08/2026 (lunes)
Metodología de diagnóstico: NIST CSF 2.0 + CIS Controls v8.1 IG1, mapeo de cada dominio a funciones NIST y controles CIS.

### Jornada 2 — 20/08/2026 (miércoles)
Relevamiento de riesgos frecuentes en PyMEs sin área de IT + referencia al marco legal argentino (Ley 25.326).

### Jornada 1 — 18/08/2026 (martes, primera clase — el 17 fue feriado)
Kickoff: presentación del Plan de Trabajo Individual aprobado por TECLAB.

---

## Otros hitos (fuera del ciclo de clase, no van a la Bitácora)

- **02/09/2026**: revisión completa del documento técnico entregable
  (`Herramienta_Autodiagnostico_Ciberseguridad_PyMEs.docx`) — se sacó un
  artefacto de IA sin limpiar, se recortaron 5 preguntas que estaban en el
  documento pero no en el código (25→20), se sincronizaron los números de la
  simulación con la salida real del motor, se regeneraron las Figuras 1 y 5,
  y se agregó un recuadro aclarando qué está construido hoy vs. qué es fase
  producto (redactado sin fechar el avance, para no adelantar tampoco ahí).
  **Enviado por mail a Gabriel (vpp.teclab.gg@gmail.com) el 02/09/2026.**
