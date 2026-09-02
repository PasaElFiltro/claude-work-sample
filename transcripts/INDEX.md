# Índice de transcripts

Siete sesiones en claude.ai entre el 28 de agosto y el 1 de septiembre de 2026. Verbatim: lo que escribió Romina y lo que respondió cada modelo, con hora de Chile. Sin resultados de herramientas, sin razonamiento interno, sin adjuntos. Una usuaria real seudonimizada como *J.*

Las sesiones en Claude Code (Sonnet orquestador, brigadas de Haikus) no tienen export: sus outputs aparecen pegados por Romina dentro de los turnos de `02` y `04`, que es como viajaron en la realidad. La bitácora que el Sonnet dejó en el PR al terminar la corrida está en `claude-code/`.

| # | Archivo | Modelo | Turnos | ~tokens | Momento clave (hora) |
|---|---|---|---|---|---|
| 01 | `01_2026-08-28_haiku_sonda_sin_categorias.md` | Haiku | 14 + 14 | 22K | **16:39** — "no en qué palabras, en qué categorías conceptuales". Romina pide una lectura de su propia bitácora sin categorías. El Haiku encuentra la invariante. Origen de la hipótesis. Cierra con Romina preguntando al Haiku qué prefirió: el prompt cerrado o la sonda exploratoria. |
| 02 | `02_2026-08-28_opus_calado_pr533.md` | Opus (*Calado*) | 60 + 60 | 30K | **12:31–12:50** — "¿le subí la perplexity al Sonnet orquestador?" Diagnóstico conductual del loop y reescritura del prompt. **13:32** — las tres reglas del cazador (null como botín). **23:02** — la taxonomía del Haiku llevada al Opus para corregir prompts. |
| 03 | `03_2026-08-31_haiku_rendija_indice_pr533.md` | Haiku (*rendija*) | 6 + 7 | 3K | **11:24** — un Haiku lee el PR #533 completo (25 commits, 13 archivos, 45 comentarios) y produce un índice JSON para que un Opus entre sin gastar contexto. Economía de tokens como diseño. |
| 04 | `04_2026-08-31_fable_grafo_y_conector_mcp.md` | Fable 5 | 40 + 41 | 31K | **14:17** — se construye el grafo y el conector MCP en cámara. **21:25–21:34** — "yo sí veo un grafo, lo que no veo es ninguna diferencia": Romina pilla que el render no cambió. **22:19** — el canario no cuadra. **00:53–00:55** — costo de tokens a la 1 AM y "contra código, frozen". |
| 05 | `05_2026-08-31_haiku_canario_satisficing.md` | Haiku | 5 + 5 | 3K | **22:23** — diagnóstico del canario: 16/265, 6/265, 8/265. "El problema no es de los Haikus. Es de prompt + presupuesto de búsqueda." Tres omisiones del harness nombradas. |
| 06 | `06_2026-08-31_haiku_pregunta_taxonomia.md` | Haiku | 2 + 3 | 0.4K | **22:43** — la pregunta que no cupo en la ventana. Se reformula en `07`. |
| 07 | `07_2026-08-31_haiku_taxonomia_tres_niveles.md` | Haiku | 3 + 3 | 1.2K | **22:49** — la taxonomía de tres niveles del lenguaje de los avisos, en un mensaje. Rediseña el grafo. Cabe en una pantalla. |

## Si solo vas a leer dos

`07` y `05`, en ese orden. Después `02` desde las 12:31.

## Cómo se produjeron estos archivos

Export de claude.ai → script de conversión que conserva texto de ambos lados y nombres de herramientas, descarta resultados de herramientas, razonamiento interno y adjuntos, y redacta por patrón credenciales, correos, teléfonos, identificadores y el nombre de una usuaria → verificación automática en cero hallazgos → lectura humana. Ningún mensaje fue reescrito o reordenado.
