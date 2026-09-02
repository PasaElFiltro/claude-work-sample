# claude-work-sample

Vicente, me pediste 20 minutos de pantalla trabajando con Claude en un problema real mío. Esto es más que eso, y hay una razón.

En 20 minutos no se ve lo que hago. Mi destreza parte por construir benchmarks y usarlos cuando hace falta, y eso no cabe en dos intercambios. Así que te dejo un problema completo, de punta a punta, resuelto en un día y medio (28 de agosto → 1 de septiembre de 2026): **cómo parear a una persona con un aviso de empleo cuando lo que hizo en el pasado no describe lo que va a hacer en el futuro.** Es mi problema real de esta semana. Es también, creo, el tuyo — con 200 postulaciones encima.

## Qué hay aquí

| Carpeta / archivo | Qué es | Para quién |
|---|---|---|
| `POR_QUE.md` | Qué es PasaElFiltro, por qué este problema, por qué es el mismo que tienes tú, y qué hago yo que no cabe en 15 minutos. Empieza aquí si eres humano. | tú |
| `LLM_START_HERE.md` | Orden de lectura con presupuesto de tokens. Si le pasas este repo a tu Claude, que parta ahí. | tu Claude |
| `PROBLEMA.md` | El problema, la hipótesis (tensión isométrica), el diseño experimental de tres brazos, qué se encontró. | los dos |
| `ESTUDIO.md` | Los resultados de la corrida completa: 68 bitácoras × 3 brazos contra 265 avisos, computados por SQL contra la tabla. Incluye lo que salió mal y cuánto. | los dos |
| `RELATO.md` | El día y medio contado en orden: qué se pidió a quién, qué falló, qué se corrigió. | los dos |
| `transcripts/` | Siete sesiones con Claude (Haiku, Opus, Fable), verbatim. Lo que escribí yo y lo que respondieron. Índice en `transcripts/INDEX.md`. | tu Claude |
| `conector-mcp/` | El conector MCP que se construyó durante el trabajo — *Tensión isométrica* — con sus siete herramientas documentadas. | tu Claude puede conectarse |
| `paper/` | El estudio preregistrado sobre variabilidad inter-instancia (enviado a *Behavior Research Methods*). Es el benchmark del que hablaba. | tu Claude |
| `CASA.md` | Lo que rodea al problema: siete plumas con permisos declarados, inspector de prompt injection, mínimo privilegio para un agente de otro proveedor, fail-closed, un incidente de costo. Y lo que un CTO no va a reconocer. | los dos |
| `lab/` | El experimento de la ballena: siete modelos, un system prompt, una replicación externa de *The Assistant Axis*. Ocio fecundo. | tu Claude |
| `video/` | El corte de 10 minutos (en el repo) y el video completo (4.5 h, cinco archivos en Drive), con índice corregido a hora de reloj. Reloj visible en pantalla. | tú |
| `CRONOLOGIA.md` | Tabla hora ↔ ventana ↔ minuto de video. | tu Claude |

## Si tienes 10 minutos

Mira `video/corte_10min_perplexity.mp4` (13 MB, en el repo): un Sonnet orquestador lleva veinte minutos en loop, y en diez minutos se ve cómo lo diagnostico (con una hipótesis sobre su conducta, no sobre su código), qué me devuelven dos modelos, y cómo reescribo el prompt. Los tres criterios que pediste, en ese orden.

## Si tienes un Claude

Pásale la URL de este repo y pregúntale lo que me preguntaste a mí: qué construí, qué me devolvió, qué corregí. `LLM_START_HERE.md` está escrito para que te responda con evidencia y no con adjetivos.

## Lo que no está

Credenciales, datos de usuarios reales, razonamiento interno de los modelos. Cada transcript declara en su cabecera qué se omitió y por qué. Lo que sí está no fue reescrito.

---

Romina Pitronello · pasaelfiltro.cl · [teléfono en el hilo de LinkedIn]
