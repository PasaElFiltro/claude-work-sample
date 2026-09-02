# Video

Grabación de pantalla, 4.5 horas en 5 clips, sin narración: Romina trabaja en silencio y escribiendo; la pantalla es el guion. Cubre desde el sábado 30 de agosto al mediodía (el Sonnet orquestador en loop) hasta la tarde del domingo 31 (el conector MCP construido y verificado). **No cubre** el canario ni la taxonomía de tres niveles de la noche del 31: la grabación terminó antes. Esos momentos están en `../transcripts/05` y `07`, en texto, completos.

| Pieza | Dónde | Qué es |
|---|---|---|
| Video completo | `[enlace — Romina lo agrega]` | Los 5 clips. Los offsets de concatenación están en `timestamps.md`; el orden de los clips no es cronológico en hora de reloj (el clip 5 es la mañana del 31; los clips 3–4, la tarde). |
| Corte de 10 minutos | `[enlace — Romina lo agrega]` | **Clip 1, 00:18:42 → 00:29:13.** Ver abajo. |

## Los 10 minutos

Sábado 30, 12:31–12:41 hora Chile. Un Sonnet en Claude Code, encargado de orquestar una brigada de Haikus para leer 57 avisos, lleva veinte minutos pensando en círculos.

| Global | Qué pasa | Criterio de Vicente |
|---|---|---|
| 00:16:00 | Romina hace scroll por las trazas de razonamiento del Sonnet, auditando el loop a mano | contexto |
| 00:19:01 | Escribe a un Opus en claude.ai: "¿es mi idea o le subí la perplexity al Sonnet orquestador?" | contexto |
| 00:19:36 | El Opus confirma el bucle de indecisión y propone simplificar | devuelve |
| 00:20:32 | Segunda opinión, misma pregunta a otra ventana: "mm tengo mis dudas, ¿cómo lo ves tú?" | contexto |
| 00:21:17–00:23:42 | Redacta la instrucción: separar lo determinístico (cómo entregan los Haikus) de lo que es juicio (cómo el aviso presenta tensión); código listo; blindar contra alucinaciones | corrige |
| 00:24:26 | Revisa el desglose del modelo: fallos de código vs fallos semánticos | devuelve |
| 00:25:16 | Escribe su hipótesis: el subagente percibió una capa de supervisión inesperada y leyó desconfianza — vectores relacionales, geometría del modelo | corrige |
| 00:28:35 | El modelo valida la hipótesis del loop de ansiedad | devuelve |
| 00:29:13 | Romina observa la correlación con el cambio de idioma en el prompting | corrige |

Texto de la misma escena: `../transcripts/02`, turnos 12:31 a 12:50.

## Segunda ventana, si sobran doce minutos

**Clip 3, 02:03:44 → 02:15:45** (domingo 31, ~14:17–14:30). ChatGPT se cae en medio de una revisión adversarial con Sol; Romina pivota al Fable y le pide el conector MCP; el Fable lo diseña, despliega la edge function y prueba `tension_grafo_bitacoras` en vivo; Romina abre el mapa público, navega los nodos, y a las 02:15:45 escribe: "es raro porque no lo veo en el mapa". El conector estaba desplegado; el render no había cambiado. Texto: `../transcripts/04`, 14:17 en adelante.

## Índice

`timestamps.md`: 316 eventos, ~1 por minuto, generados por Gemini 3.7 Flash en 29 ventanas de 10 minutos. Cada evento tiene un `anchor`: texto literal visible en pantalla, para verificar sin mirar. Los null son null honesto. `index.json` es lo mismo, estructurado, para tu Claude. Límite declarado: entre 03:31 y 03:43 no hay video (pausa de grabación).

Verificación contra los transcripts: hecha para las dos ventanas de arriba (el evento 00:19:01 coincide con el turno de las 12:31 en `02`; el 02:03:44 con el de las 14:17 en `04`). El resto del índice queda como lo entregó el modelo.
