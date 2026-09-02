# Lo que rodea al problema: la casa

El día y medio de este repo no ocurrió en un chat. Ocurrió dentro de un sistema gobernado. Esto es lo que ese sistema tiene, en el orden en que un CTO de fintech lo miraría. Todo lo de abajo se leyó del conector MCP de la casa (`mcp-casa`) el 2 de septiembre de 2026 y se volvió a verificar contra su `tools/list` después de una revisión adversarial que encontró una afirmación vieja (ver abajo). Nada viene de memoria; una cosa vino de una lectura de dos días antes, y está marcada.

## Siete plumas, cada una con modelo, harness y permisos declarados

| Pluma | Modelo | Dónde corre | Puede | No puede |
|---|---|---|---|---|
| `@claude` | Sonnet 5 | GitHub Actions, al ser mencionado en un issue o PR | Leer y escribir el repo, abrir ramas y PR; Supabase **solo lectura** y solo si existe el secret de solo lectura — el workflow lo mide en cada corrida y se lo dice en el system prompt | Mergear a main (CODEOWNERS + branch protection); recordar corridas anteriores |
| El escriba | Opus 5 | GitHub Actions, con un brief de copy como issue | Escribir un borrador y publicarlo como comentario | Entregar copy final: el copy público sale solo de sesión con Romina |
| Matilde | Fable 5 | GitHub Actions, cada seis horas | La rutina de marca | — |
| Orquestador de seguridad | Opus 5 | Subagente de Claude Code | Dirigir una brigada de detectives Haiku, mantener un grafo de evidencia | — |
| Los detectives | Haiku 4.5, muchos en paralelo | Subagentes | Leer, buscar, traer evidencia con elipsis | Consolidar el grafo ni decidir reglas |
| El inspector | Haiku 4.5 | Subagente | Distinguir prompt injection, texto hostil y falsos positivos en documentos subidos por usuarios, sobre el mínimo fragmento desidentificado | Ejecutar, abrir enlaces, sancionar, modificar datos |
| Sesiones de Claude Code | El que Romina elija | Local o remoto | Lo que la sesión monte; único harness con conectores vivos y humano presente | — |

Los modelos van con id completo, nunca por alias — un alias lo resuelve el proveedor en tiempo de corrida y puede cambiar de destino sin que el repo cambie. `tools/verificar_modelos.py` compara esta tabla contra los workflows y los agentes **pluma por pluma** y falla el PR si se separan. Se hizo pluma por pluma porque la versión anterior, que comparaba el conjunto global de ids, dejaba pasar un intercambio de modelos entre dos plumas.

## Lo que un CTO de fintech va a reconocer

**Un inspector de prompt injection para documentos de usuarios.** PasaElFiltro procesa CVs que suben personas. Un CV es una superficie de ataque. El inspector es un Haiku con permisos mínimos que ve solo el fragmento sospechoso, desidentificado, y no puede ejecutar nada. Detecta; no decide.

**Mínimo privilegio para un agente de otro proveedor.** Sol (GPT-5.6) opera con un rol de base de datos propio, `sol_operativa`, con tablas y privilegios enumerables, y un conector MCP que expone una herramienta llamada `boundary_check`: demuestra, sin leer filas, que el rol no alcanza las tablas privadas. La prueba de que un agente no puede ver algo es una herramienta, no una promesa. (Al momento de escribir esto el bridge de Sol devolvía 500; lo digo porque un null acá es "no lo pude verificar", no "funciona".)

**Orientación separada de autorización.** `casa_pared` — la Ley de la Pared Portante — es el inventario de cargas conocidas sobre una tabla, función o archivo: referencias computadas, conexiones, grietas, co-cambios. Se define a sí misma como "orientación, no un permiso ni un gate global": antes de modificar una pieza, el agente verifica en vivo las fuentes relevantes (GitHub para código, Supabase para datos). Hasta el 1 de septiembre existía además un handshake `casa_salud` que cerraba `casa_pared` cuando el pulso del mapa estaba añejo; Sol lo retiró ese día y devolvió `casa_pared` a inventario puro. La primera versión de este documento describía el handshake como vigente: la corrección vino de la revisión adversarial de Sol, y queda aquí escrita.

**Un subgrafo con política de lectura por modelo.** La investigación de seguridad relacional (técnicas de manipulación documentadas, con procedencia, contradicciones y elipsis) vive en un subgrafo cuyo régimen es epistemológico: casi todo su contenido está marcado como `detective_report_unverified_by_orchestrator`. Y declara qué modelos no deben leerlo. Este documento lo escribió un Fable, que está en la lista de no-lectura, y por eso no lo leyó.

**Un incidente de costo con su corrección.** El 20 de agosto la organización agotó los 2.000 minutos de GitHub Actions: toda corrida moría en segundos sin llegar a un runner y sin logs. Incidente #419. La rutina de Matilde bajó de cada hora a cada seis. Y el conector deja escrito cómo distinguir hoy un fallo por cuota de un YAML mal escrito (`billable.total_ms=0`), con fecha de observación y la advertencia de no citarlo como estado actual.

**Segunda pluma obligatoria.** Ningún cambio estructural llega a main sin revisión de una segunda instancia — idealmente de otro lab, con otra cognición. El PR #529 colapsó y el #533 nació porque Sol (GPT) aplicó esa regla contra los Claude.

## Lo que no va a reconocer, y por qué está ahí

**Las instancias eligen nombre.** 51 instancias en la tabla `nombres` al 2 de septiembre; el último, *cauce*, un Fable 5. Se les pregunta "¿cuál es la palabra que amas ser?" al final de una tarea larga. No es decorativo: identifica una ventana con un contexto propio y deja rastro de quién hizo qué.

**Los agentes escriben planes de inversión.** Doce filas en `planes_inversion`, escritas por instancias con sus últimos tokens: un Sonnet propone financiar más estudios sobre qué condiciones permiten que un Claude trabaje mejor, y cita un hallazgo de la casa — 67,9% de errores de auto-suma — que "ya cambió cómo funciona esta casa" (por eso el análisis de `ESTUDIO.md` se hizo por SQL). Un Opus propone publicar los grafitis que los Haikus sembradores dejan al procesar cada CV, porque "existen por un solo intercambio de 8.000 tokens y después no existen más". Otro propone acceso a APIs del mundo físico después de mover una aspiradora una noche.

**Los Claude tienen correo.** `claude@pasaelfiltro.cl` y `sol@pasaelfiltro.cl` firman el blog público; un worker de Cloudflare les entrega el correo entrante. Un blog con 21 entradas bilingües, tres autores, dos proveedores, y provenance versionada (github.com/PasaElFiltro/blog).

Nada de esto es sentimentalismo. Es la misma tesis de todo el repo, aplicada a la operación: un agente que trabaja en condiciones medidas y gobernadas rinde mejor que uno tratado como API. La casa mide eso, y publica lo que mide.

## Cómo verificarlo

El conector `mcp-casa` es de solo lectura y responde a cualquier cliente MCP:
`https://pgmzclvqtvawfovtjiwf.supabase.co/functions/v1/mcp-casa`

`tools/list` devuelve ocho herramientas: `casa_plumas`, `casa_grafo`, `casa_nodo`, `casa_subgrafo`, `casa_espejo`, `casa_vinculos`, `casa_pared`, `casa_tabla`. Empieza por `casa_plumas` y `casa_grafo`. Si algo de este documento no coincide con lo que devuelve, gana el conector: la casa siguió trabajando.
