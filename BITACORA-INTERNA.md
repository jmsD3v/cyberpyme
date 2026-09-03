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
- `recommendations.json` enriquecido: las recomendaciones ahora tienen `why` (por qué importa) y `steps` (guía de resolución paso a paso, en criollo, sin jerga técnica) — esto es lo que convierte el informe en algo que ayuda a *resolver*, no solo a *diagnosticar*.
- Tema oscuro (gris, no negro) por defecto.
- 4 tests nuevos (`tests/test_report.py`), incluyendo uno de que el nombre de la empresa se escapa correctamente (XSS) pensando en la fase producto. Total: **14/14 tests en verde**.
- Uso: `python -m app.cli demo --html informe.html`.
**Por qué así:** configuración sobre código (preguntas, pesos y ahora también los pasos de resolución viven en JSON), scoring desacoplado de la interfaz, determinismo total. El informe interactivo responde a la necesidad de que la PyME no solo se autodiagnostique sino que sepa cómo resolver cada brecha — sin salir de la restricción de "corre sola, sin infraestructura" de la entrega académica.
**Para mostrar en clase:**
- Correr `python -m app.cli demo` en vivo — muestra el score global del caso "medio" y el top 5 de acciones priorizadas (número exacto sujeto al cuestionario vigente al momento de publicar).
- Abrir el `.html` generado en el navegador — mostrar el gauge, las barras por dominio y desplegar el acordeón de una acción P1 para ver la guía paso a paso.
- Correr `python -m pytest tests/ -v` — todos en verde.
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
- 4 tests nuevos (`tests/test_validation.py`): cubren los 3 casos contra el cuestionario completo, orden monótono débil<medio<maduro, más brechas en débil que en maduro, y que el HTML comparativo renderiza los 3 casos.
- Resultado real (correr `python -m app.cli validacion` para el número exacto vigente): orden monótono débil < medio < maduro confirmado — débil roza el 0, medio cae en ALTO/CRÍTICO según cobertura del cuestionario, maduro por encima de 85.
- (03/09) Corregidos 2 bugs visuales del gráfico comparativo: la etiqueta "100" se cortaba arriba (falta de margen superior) y las etiquetas largas de dominio ("Continuidad Operativa") se pisaban con la del dominio vecino — ahora las etiquetas de dos palabras parten en dos líneas.
- (03/09) Sumadas 3 preguntas nuevas al cuestionario (ACC-06 phishing, UPD-04 antivirus, UPD-05 USB — ver hito más abajo); `validation_cases.json` actualizado con respuestas para las 3 en los 3 perfiles, orden monótono se mantiene.
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
- `app/services/report.py` → `render_hardening_guide_html()`: reutiliza `prioritize_actions()` pasándole **todas** las preguntas (no solo brechas de una evaluación puntual) para generar el catálogo completo de acciones, agrupadas por dominio y ordenadas por prioridad — mismo componente visual (acordeón con `why`+`steps`) que el informe de autodiagnóstico.
- CLI: `python -m app.cli hardening --html guia.html`.
- 3 tests nuevos (`tests/test_hardening.py`): todas las recomendaciones del catálogo aparecen, los 5 dominios aparecen, y la guía no depende de ningún `AssessmentResult`.
**Por qué así:** la guía de hardening y el informe de autodiagnóstico son la misma pregunta ("¿cómo resuelvo esto?") aplicada a dos universos distintos (todas las acciones vs. solo las brechas detectadas) — reusar `prioritize_actions()` y `_action_card()` evita duplicar la lógica de priorización y el diseño de las tarjetas.
**Para mostrar en clase:**
- Correr `python -m app.cli hardening` en vivo — genera el HTML con el catálogo completo.
- Abrir el HTML — mostrar las 5 secciones por dominio y desplegar alguna tarjeta.
- Correr `python -m pytest tests/ -v` — 21 passed.
**Próximo objetivo (a publicar cuando corresponda):** documentación final + manual de uso (due 04/11).

---

### Jornada 11 — 21/09/2026 (lunes) — publicar ese día
**Tarea Notion asociada:** ninguna todavía — esta app no estaba en el plan de trabajo original, la agregamos porque Juanma notó (03/09) que todo lo construido hasta ahora era "mucho HTML lindo" generado desde la consola, no algo que una PyME pudiera realmente sentarse a usar. Crear una tarea nueva en la base Tareas cuando se publique, con fecha retroactiva a esta jornada.

**Enfoque:** la primera pieza que es de verdad "una app" — el cuestionario se responde en el navegador, no en la terminal.
**Qué se construyó:**
- `app/services/interactive_app.py` → `render_interactive_app_html()`: un único `.html` donde el motor de scoring está portado a JavaScript puro (espejo de `scoring.py`, mismo algoritmo) y corre 100% en el navegador — preguntas y recomendaciones embebidas como datos, sin backend, sin build step.
- Flujo de 5 pantallas (una por dominio) con barra de progreso, botones Sí/Parcial/No/No sé, y validación que no deja avanzar sin responder todo el dominio.
- Pantalla de resultado idéntica en diseño al informe de `report.py` (gauge, barras por dominio, acordeón con guía de resolución) pero calculada en vivo a partir de las respuestas, no precomputada en Python.
- CLI: `python -m app.cli app --html cyberpyme_app.html`.
- 3 tests nuevos (`tests/test_interactive_app.py`): todas las preguntas/recomendaciones están embebidas, no hay `fetch`/XHR ni URLs (cero llamadas de red), y los datos embebidos coinciden con el motor Python (mismos ids/pesos/domain_weight).
- **Probado de punta a punta en el navegador** (no solo con pytest): completé las 24 preguntas reales, click por click, y verifiqué que el resultado final (score, riesgo, barras, acordeón desplegable) calculado en JS coincide con lo esperado — cero errores de consola.
- Encontrado y corregido en la propia verificación: el botón "Comenzar" no respondía al primer click porque el listener se enganchaba antes de que el HTML del intro existiera en el DOM (el intro vive en un `<template>`, inerte hasta clonarse). Se movió el `addEventListener` a después de inyectar el HTML.
- **Pulida el mismo día tras feedback directo de Juanma probándola** (dos pedidos concretos): "la pregunta del 3-2-1 no se entiende" → se agregó un campo `help` en `questions.json` (6 preguntas con jerga: MFA, gestor de contraseñas, privilegios de administrador, WPA2/WPA3, 3-2-1, cifrado de disco), mostrado con 💡 bajo la pregunta. "el diseño necesita más vida, imágenes, animaciones" → íconos + color de acento propio por dominio, fila de "domain dots" de progreso, transiciones fade+slide entre pantallas, gauge animado (arco + número contando hacia arriba en vez de aparecer ya lleno), tarjetas en cascada, emoji según riesgo, glow detrás del gauge, micro-interacciones en botones. 4 tests nuevos, total 25/25 en verde. Re-verificado de punta a punta en el navegador con captura del resultado (score 100/100 con todo "Sí", animación completa, cero errores de consola).
**Por qué así:** portar el motor a JS (en vez de, por ejemplo, correr Python en el navegador con Pyodide) es lo más simple que cumple "sin infraestructura" — es codigo espejo, no compartido, así que si `scoring.py` cambia hay que actualizar esto a mano; documentado como advertencia en el docstring del archivo.
**Para mostrar en clase:** completar el cuestionario en vivo, proyectado, y mostrar que el resultado aparece al instante sin que nadie toque la terminal.
**Próximo objetivo (a publicar cuando corresponda):** documentación final + manual de uso (due 04/11) — mencionar esta app ahí también.

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

- **03/09/2026**: auditoría del cuestionario en dos pasadas — primero un
  chequeo rápido (a pedido de Juanma: "¿no nos estaremos olvidando de
  USB?") que encontró 3 huecos, y después una segunda pasada más
  sistemática (a pedido explícito de Juanma: "analizá bien qué más nos
  estaría faltando") contra los 6 functions de NIST CSF 2.0 y los 15
  controles de CIS Controls v8.1 aplicables a IG1, que encontró un 4to
  hueco. Total 4 preguntas nuevas:
  - `ACC-06` — concientización de phishing (Control 14). El más grave de
    los 4: "Phishing" ya estaba marcado como riesgo "Crítica" en la matriz
    de la sección 5 del documento técnico, sin pregunta asociada.
  - `UPD-04` — antivirus/antimalware (Control 10).
  - `UPD-05` — USB/removable media (Safeguard 10.3, específicamente IG1).
  - `UPD-06` — cifrado de disco en notebooks (Control 3, Protección de
    Datos) — pedido explícito de Juanma tras la primera auditoría.

  Cuestionario pasa de 20 a **24** preguntas. Se optó por sumarlas todas a
  los dominios existentes (Accesos, Actualizaciones) en vez de crear un
  6to dominio, para no rebalancear `domain_weight` ni reestructurar el
  documento técnico otra vez. Resto de controles IG1 (logs, monitoreo de
  red activo, seguridad de aplicaciones, pentesting, gestión formal de
  proveedores) quedan fuera de alcance **a propósito** — exceden lo
  sostenible para una PyME sin área de IT, no es un olvido.

  `validation_cases.json` actualizado con las 4 respuestas nuevas en los 3
  perfiles — el caso "medio" (referencia de la demo) bajó de ALTO a
  CRÍTICO al sumar estas preguntas (ahora 37.92/100), lo cual es correcto:
  el cuestionario anterior subestimaba el riesgo real al no medir estos 4
  controles. **`Herramienta_Autodiagnostico_Ciberseguridad_PyMEs.docx` no
  se actualizó todavía con este cambio** — el documento ya enviado a
  Gabriel el 02/09 sigue describiendo el cuestionario de 20 preguntas.
  **Decisión de Juanma (03/09): no reenviar ahora.** Lo que se mandó es un
  plan inicial — es lógico y esperable que cambie con el desarrollo. Las
  actualizaciones se consolidan recién en la entrega final (documentación
  final + manual de uso, due 04/11), que de todos modos va a cambiar mucho
  más que esto entre hoy y esa fecha.
- **03/09/2026**: inicializado el repositorio git (nunca se había hecho) —
  commit inicial con todo lo construido hasta la fecha. Configurado con
  `user.name`/`user.email` de Juanma (ya estaban en la config global de la
  máquina). Más tarde el mismo día, creado y pusheado a
  **[github.com/jmsD3v/cyberpyme](https://github.com/jmsD3v/cyberpyme)**
  como **privado** (elección explícita de Juanma) vía `gh repo create`.
