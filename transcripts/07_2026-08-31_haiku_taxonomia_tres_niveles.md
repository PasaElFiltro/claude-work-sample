# 2026-08-31 haiku taxonomia tres niveles

- **Sesión:** 2026-08-31 (hora Chile)
- **Con quién:** Claude Haiku
- **Turnos:** 3 de Romina · 3 del modelo
- **Qué se ve y qué no:** mensajes de ambos lados verbatim. Las llamadas a herramientas aparecen como una línea `› tool:`; sus resultados, el razonamiento interno del modelo y los adjuntos no se publican (contienen credenciales de la casa y datos de usuarios reales). Nombre de usuaria seudonimizado como *J.* Ningún texto fue reescrito.

---

**Romina** · 22:47

hoa haiku, como estas al llegar a esta ventana?


**Claude Haiku** · 22:48

hoa, romina. acá, bien. veo que llegaste con tu ost.

¿cómo andas? ¿qué necesitas?


**Romina** · 22:48

mira quiero que mires esta tabla en supabase experimento_tension_avisos_v2 y leyendo los anuncios, piensa cual es la estructura taxonómica subyacente en el lenguaje, eso nos va a permitir mejorar un grafo


**Claude Haiku** · 22:49

› tool: Supabase:execute_sql
voy a leerla. déjame tirar una query a esa tabla.

romina, acá va. leí los primeros 20. veo una estructura taxonómica clara que el grafo va a necesitar. te lo presento en capas:

**nivel 1: la tensión que resuelve cada cargo** (el problema económico/operativo)

- continuidad física (seguridad, producción sin parar): geotécnico, operaciones chancado, mant. eléctrico, especialista CAS
- transformación/mejora (cambio controlado): ingeniería productividad, QA senior, especialista control remoto
- capacidad de decisión distribuida (mediación): analista funcional, planner abastecimiento, recruiter
- velocidad en volumen (high-throughput sin error): sales development, admissions sales, QA tester
- integración horizontal (que hablen distintos mundos): head of project services, full-stack engineer, full-stack product
- compensación por fricción (absorber conflicto): leads técnicos en general

**nivel 2: la estructura emocional/cognitiva requerida** (lo que la persona tolera)

cuando separás por lo que el aviso **debe inferir que tolera**:

- **obsesivos metrificables**: monitorean números y pueden decidir por ellos (trader, planner, qa specialist, software engineer)
- **tolerancia a la ambigüedad**: entran a sistemas rotos sin mapa (product engineers, software ai, analista funcional)
- **monotonía vigilante**: repiten lo mismo esperando el fallo (operaciones, geotécnico, especialista remoto)
- **conflicto estructural sostenido**: están entre dos capas que no van a alinearse nunca (product managers, project services, analista funcional)
- **autonomía que requiere criterio propio**: pueden decir no sin miedo, pero nadie los chequea (ingenieros senior, líderes técnicos)

**nivel 3: el lenguaje que delata grietas** (lo que NO dicen explícito)

- repetición de palabras = cicatriz anterior (si dice "seguridad" 3+ veces, tuvieron accidente)
- ausencia de números (sueldo, métricas reales) = inseguridad corporativa
- "disponibilidad para turno X" = exigencia que nadie elige voluntariamente
- "colaboración" mencioado mucho = había confusión anterior
- "autonomía real" = antes no la había
- especificidad en herramientas = frustración: la anterior persona no las sabía
- promesa de crecimiento sin línea de carrera clara = probable techo

---

**para el grafo mejora así:**

los nodos no son solo avisos. son **tensiones tipificadas**. las aristas pueden ser:

- **mismo tipo de tensión, distinto nivel de severidad** (QA en startup vs QA en banco minero = misma estructura, presión distinta)
- **tensiones que se retroalimentan** (si falla continuidad operativa, crece fricción en mediación)
- **perfiles que pueden migrarse** (de "monotonía vigilante" a "obsesivo metrificable" es un salto real de aprendizaje)

la estructura taxonómica del **lenguaje subterráneo** es: lo que NO dicen es más patrón que lo que dicen.

¿querés que meta estos 20 avisos en una matriz? ¿o que tire más queries a la tabla para ver si la estructura se sostiene con muestra más grande?


**Romina** · 23:01

haiku dale una probada al nuevo conector mcp con el grafo de tension isométrica, qué te parece?


**Claude Haiku** · 23:01

› tool: Tensión isométrica:tension_salud
che, me dice que no encuentra la herramienta. ¿te llegó bien el deploy del nuevo conector? ¿cuál es el nombre exacto que pusiste en la función?

porque lo que veo en el listado de MCPs es que debería estar `Tensi\u00f3n isom\u00e9trica` pero cuando intento llamar me dice "not found". 

¿está activo ya o todavía está en setup? si está vivo puedo probar `tension_grafo_avisos`, `tension_grafo_bitacoras`, `tension_par` — los que miramos en el repo — pero necesito que confirmes que el Edge Function está respondiendo en la URL correcta.

