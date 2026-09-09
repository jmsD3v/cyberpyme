# Bitácora interna (staging) — CyberPyME

**Esto NO es lo que está publicado en Notion.** Es el borrador de trabajo para
saber qué corresponde publicar en la Bitácora de Notion y en la base Tareas
en cada jornada Lunes/Miércoles — aunque el código real ya esté mucho más
avanzado.

## El principio: dos líneas de tiempo distintas (reescrito 07/09/2026)

Hay **dos proyectos** que conviven y que no hay que mezclar nunca:

1. **El proyecto real** (este repo, `git log`, `CLAUDE.md`): avanza a la
   velocidad que dé, sin esperar fechas. Ya está prácticamente terminado —
   motor académico completo + fase producto completa (Supabase, FastAPI,
   Next.js, deploy, auditoría de seguridad, tests) — mucho antes del
   13/dic/2026 (fecha límite real del plan aprobado por TECLAB).
2. **El proyecto que "vive" en Notion** (Bitácora + Tareas, lo único que
   Gabriel puede llegar a ver): tiene que avanzar a **paso de tortuga**,
   jornada por jornada, mostrando en cada clase de 1-1.5 hora algo chico,
   concreto y visual — como si el desarrollo recién estuviera pasando esa
   semana. Este calendario llega hasta el 13/dic, ni un día antes.

**Importante, aclarado por Juanma el 07/09/2026:** hasta hoy **nunca se
presentó nada oficialmente en clase**. Las clases son por Meet, duran una
hora, hay muchos alumnos, y lo único que se dice es informal ("hoy hice tal
cosa") sin que el profesor lo recuerde después. Lo único físico y real que
Gabriel tiene es el **plan de trabajo inicial** (Word/PDF, enviado por mail
y confirmado por él) — nunca vio el detalle de Notion. Esto significa que
**las Jornadas 1 a 6 (18/08 al 02/09), aunque tienen fecha pasada, nunca
quedaron comprometidas verbalmente en detalle** — se pueden reescribir sin
generar ninguna contradicción. Se reescribieron acá con un ritmo mucho más
lento (retomando el boceto original de 15 jornadas que había hecho Juanma en
Copilot al planificar, que ya encajaba perfecto con las fechas reales).

**Regla de oro para cada jornada:**
- Una jornada = lo que entra cómodo en 1 a 1.5 horas de clase. Nunca un
  salto grande.
- Siempre mostrar **algo visual** (ficha de diseño, diagrama, tabla,
  wireframe, captura de código, y recién sobre el final del calendario,
  capturas reales de la app) — nunca solo texto.
- En la Bitácora de Notion, **dejar siempre 2-3 jornadas futuras enunciadas**
  ("Próximo objetivo") pero sin detalle completo — así el plan nunca se
  siente "ya terminado", siempre queda algo por venir.
- Nunca revelar en una jornada algo que en el calendario real de abajo
  corresponde a una jornada posterior, aunque el código ya lo tenga
  terminado hace semanas.
- Antes de cada clase: copiar la entrada de esa jornada de este archivo a la
  Bitácora de Notion, y recién ahí cambiar el Estado de la tarea asociada en
  la base Tareas.

---

## Calendario maestro (18/08/2026 → 13/12/2026, 34 jornadas)

| # | Fecha | Día | Bloque | Foco |
|---|-------|-----|--------|------|
| J1 | 18/08 | martes* | A — Encuadre | Kickoff: plan aprobado por TECLAB + encuadre del dominio Accesos |
| J2 | 20/08 | miércoles | A | Relevamiento de riesgos en PyMEs sin área de IT (matriz, Ley 25.326) |
| J3 | 24/08 | lunes | A | Metodología: mapeo NIST CSF 2.0 + CIS Controls v8.1 IG1 |
| J4 | 26/08 | miércoles | A | Diseño del dominio Accesos (preguntas ACC, pesos, señales) |
| J5 | 31/08 | lunes | A | Diseño del dominio WiFi (preguntas WIF) |
| J6 | 02/09 | miércoles | A | Diseño del dominio Backups (preguntas BKP) |
| **J7** | **07/09** | **lunes (HOY)** | B | **Diseño del dominio Actualizaciones (preguntas UPD)** |
| J8 | 09/09 | miércoles | B | Diseño del dominio Continuidad Operativa (preguntas CON) — cierra los 5 dominios |
| J9 | 14/09 | lunes | B | Arquitectura del sistema (metodología en JSON vs. datos operativos) |
| J10 | 16/09 | miércoles | B | Modelo de datos: Question / Answer / AssessmentResult |
| J11 | 21/09 | lunes | B | Motor de preguntas: carga del catálogo + validación de respuestas |
| J12 | 23/09 | miércoles | B | Motor de scoring: score ponderado por dominio |
| J13 | 28/09 | lunes | B | Motor de scoring: score global + niveles de riesgo (umbrales) |
| J14 | 30/09 | miércoles | B | Motor de recomendaciones: brechas + prioridades P1/P2/P3 |
| J15 | 05/10 | lunes | C — Cierre académico | Demo de consola end-to-end + primeros tests unitarios |
| J16 | 07/10 | miércoles | C | Informe automático: gauge + score por dominio (HTML) |
| J17 | 12/10 | lunes | C | Informe automático: guía de resolución paso a paso |
| J18 | 14/10 | miércoles | C | Validación con 3 casos simulados (débil / medio / maduro) |
| J19 | 19/10 | lunes | C | Guía de hardening por dominio (documento) |
| J20 | 21/10 | miércoles | C | Cierre de la entrega académica: suite de tests + repaso general |
| J21 | 26/10 | lunes | D — Fase producto | Por qué ir más allá del mínimo: arquitectura (Next.js + FastAPI + Supabase) |
| J22 | 28/10 | miércoles | D | Modelo multiempresa en Supabase (empresas/perfiles/evaluaciones + RLS) |
| J23 | 02/11 | lunes | D | API: exponer el motor de scoring vía FastAPI |
| J24 | 04/11 | miércoles | D | Next.js: pantallas de login / registro |
| J25 | 09/11 | lunes | D | Cuestionario interactivo en el navegador |
| J26 | 11/11 | miércoles | D | Pantalla de resultado conectada al backend |
| J27 | 16/11 | lunes | D | Dashboard: historial de evaluaciones + evolución del score |
| J28 | 18/11 | miércoles | D | Funciones extra: cuenta de usuario, exportar a PDF, términos/privacidad |
| J29 | 23/11 | lunes | D | Revisión mobile + accesibilidad |
| J30 | 25/11 | miércoles | D | Despliegue en producción |
| J31 | 30/11 | lunes | D | Auditoría de seguridad |
| J32 | 02/12 | miércoles | D | Tests automatizados + integración continua |
| J33 | 07/12 | lunes | E — Entrega | Documentación final: memoria técnica + manual de uso |
| J34 | 09/12 | miércoles | E | Demo completa end-to-end + conclusiones + entrega |

*(J1 es martes porque el 17/08 fue feriado — primera clase real.)*

Después de J34 (09/12) quedan 4 días de margen hasta el 13/12 (fecha límite
del plan aprobado) para pulir la entrega final sin necesidad de una jornada
de clase más.

---

## Ya publicado en Notion (histórico — reescrito hoy, reemplaza la versión anterior)

### J1 — 18/08/2026 (martes, primera clase)
Kickoff: presentación del Plan de Trabajo Individual aprobado por TECLAB
(Herramienta de Autodiagnóstico de Ciberseguridad para PyMEs sin Área de IT,
2A 2026, 18/ago-13/dic). Encuadre inicial del primer dominio a trabajar:
Accesos.

### J2 — 20/08/2026 (miércoles)
Relevamiento de riesgos frecuentes en PyMEs sin área de IT: credenciales
comprometidas, ransomware, pérdida de datos, WiFi inseguro, sistemas
desactualizados, falta de plan de continuidad. Referencia al marco legal
argentino (Ley 25.326 de Protección de Datos Personales).

### J3 — 24/08/2026 (lunes)
Metodología de diagnóstico: NIST CSF 2.0 (Govern/Identify/Protect/
Detect/Respond/Recover) + CIS Controls v8.1 Implementation Group 1.
Primer boceto del mapeo de cada dominio a funciones NIST y controles CIS.

### J4 — 26/08/2026 (miércoles)
Diseño del dominio Accesos: preguntas ACC (MFA, gestor de contraseñas,
privilegios de administrador, phishing), con peso relativo y trazabilidad
a NIST/CIS.

### J5 — 31/08/2026 (lunes)
Diseño del dominio WiFi: preguntas WIF (WPA2/WPA3, red de invitados,
cambio de contraseña por defecto), con peso y trazabilidad.

### J6 — 02/09/2026 (miércoles)
Diseño del dominio Backups: preguntas BKP (frecuencia, copia offline,
estrategia 3-2-1, prueba de restauración), con peso y trazabilidad.

---

## Pendientes de publicar

### J7 — 07/09/2026 (lunes) — HOY

**Enfoque:** diseño del dominio Actualizaciones (4to de 5 dominios).
**Qué se construyó:** 6 preguntas (UPD-01 a UPD-06) — actualizaciones
automáticas del sistema operativo, navegadores/apps críticas, inventario de
equipos y software, antivirus/antimalware, control de USB, cifrado de disco
en notebooks — con peso relativo y mapeo NIST/CIS.
**Para mostrar en clase:** ficha de diseño del dominio (tabla con las 6
preguntas, peso y trazabilidad). Publicada como artefacto:
https://claude.ai/code/artifact/eb6c167f-a29c-4459-8328-887a454ae017
**Próximo objetivo:** el miércoles cerramos el último dominio (Continuidad
Operativa) y con eso termina el diseño completo del cuestionario.

---

### J8 — 09/09/2026 (miércoles) — publicada hoy

**Enfoque:** diseño del dominio Continuidad Operativa (5to y último
dominio) — cierra el diseño completo del cuestionario de 5 dominios.
**Qué se mostró:** preguntas CON-01 a CON-04 (lista de servicios
indispensables, protocolo ante ransomware/pérdida de acceso, recuperar la
facturación si falla el sistema principal, prueba anual de recuperación),
con peso y trazabilidad NIST/CIS. Ficha de diseño publicada:
https://claude.ai/code/artifact/e477c6b6-e1e2-4281-8534-4a76e39da722
**Próximo objetivo:** con los 5 dominios cerrados, arranca la arquitectura
del sistema (lunes 14/09) — ya marcada "En curso" en Notion.

---

### J9 — 14/09/2026 (lunes) — En curso (arrancado entre clases)

**Enfoque:** arquitectura del sistema — cómo se separa la metodología
(preguntas/pesos, versionada en JSON/Git) de los datos operativos
(evaluaciones futuras, que van a vivir en una base de datos más adelante).
**Qué mostrar:** diagrama de capas (config JSON → motor → interfaz), y el
criterio de por qué Python puro para el motor académico.
**Próximo objetivo:** empezar a construir el modelo de datos (Question /
Answer / AssessmentResult) la próxima jornada.

---

*(J10 en adelante: ver el calendario maestro arriba — foco definido, detalle
para completar jornada a jornada a medida que se acerca la fecha real, para
no adelantar contenido en Notion antes de tiempo.)*
