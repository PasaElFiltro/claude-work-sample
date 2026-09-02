# Conector MCP — Tensión isométrica

Un servidor MCP de solo lectura construido durante el trabajo (31 de agosto, `transcripts/04`) para que un Haiku con ventana corta pueda navegar 265 avisos y 69 bitácoras **sin leerlos enteros**: entra por región de tensión, aterriza en un aviso, y sale. Corre como Supabase Edge Function.

- **URL:** `https://pgmzclvqtvawfovtjiwf.supabase.co/functions/v1/mcp-tension`
- **Protocolo:** MCP (Model Context Protocol). Se conecta desde claude.ai, Claude Code, o cualquier cliente MCP.
- **Permisos:** lectura. No escribe nada. Los datos de bitácoras están desidentificados (lectores por hash, sin nombres).
- **Todo se computa en vivo:** el handshake no devuelve caché.

## Las siete herramientas

| Herramienta | Qué hace | Cuándo usarla |
|---|---|---|
| `tension_salud` | Handshake: censo de bitácoras, horizonte de avisos, avance del mapa de categorías, estado del piloto de tres brazos. | Primera llamada, siempre. |
| `tension_mapa` | El territorio por dimensión de la taxonomía emergente: qué dimensiones están pobladas, con qué valores, cuántos avisos en cada una. | Para elegir por dónde entrar. |
| `tension_avisos_indice` | Enumeración liviana (id, cargo, empresa). Filtro opcional `(dimension, valor)` para entrar por región de tensión en vez de por título. | Para listar sin gastar contexto. |
| `tension_aviso` | La lectura de tensión completa de **un** aviso, con procedencia y sus categorías. | Aterrizaje en un elegido. No para barrer. |
| `tension_grafo_bitacoras` | Grafo de bitácoras desidentificado: nodos con lectores por hash, aristas por co-recomendación del piloto. Filtro opcional por brazo A/B/C. | Para ver el lado de las personas. |
| `tension_par` | Archivo del piloto: un par bitácora–aviso bajo los tres brazos. | La unidad mínima de varianza entre métodos. |
| `tension_horizonte` | Vuelo de pájaro: destilados de ~250 caracteres por aviso. Devuelve null con razón si el destilador no pobló. | Cuando el destilador esté listo. |

## El flujo del cazador

```
tension_salud            → ¿puedo confiar en el mapa? ¿cuántos avisos hay?
tension_mapa             → ¿qué regiones existen? ¿cuántos avisos en cada una?
tension_avisos_indice    → entrar por (dimension, valor): lista corta
tension_aviso(id)        → leer completo solo los elegidos
```

Regla escrita en el propio conector: *las categorías ordenan la lectura, no la amurallan; ante null en tu región, ojear regiones vecinas es obligatorio.* Esa regla nació del canario (`transcripts/05`): los Haikus que paraban en su primera región.

## Cómo la taxonomía del Haiku quedó sellada en el esquema

Lo que un Haiku describió en cuatro mensajes (`transcripts/07`) es hoy el esquema de categorías del conector:

| Nivel | Dimensión en el esquema | Estado (al 2-sep-2026) |
|---|---|---|
| 1 — la tensión que resuelve el cargo | `tension_resuelve` (continuidad física, transformación controlada, decisión distribuida, velocidad en volumen, integración horizontal, compensación por fricción) | Pendiente de asignación por pirámide de Haikus: 2 réplicas, acuerdo = válido |
| 2 — lo que la persona debe tolerar | `costo_cobra` (obsesión metrificable, tolerancia a la ambigüedad, monotonía vigilante, conflicto estructural sostenido, autonomía con criterio) | Pendiente, mismo método |
| 3 — lo que el aviso no dice | `senal_enfasis_seguridad`, `senal_exige_turnos`, `senal_menciona_renta`, `senal_pide_autonomia`, `senal_promete_crecimiento` | **Poblado: 1.325 asignaciones sobre 265 avisos.** Son señales de énfasis contable con causa no confirmada: ordenan, no afirman. |

El nivel 3 se pobló primero porque es contable (cuántas veces dice "seguridad") y por tanto verificable en código. Los niveles 1 y 2 requieren juicio, y el juicio en esta casa exige dos réplicas independientes que coincidan antes de entrar al esquema.

## Estado vivo cuando se escribió esto

`tension_salud` a las 02:45 UTC del 2 de septiembre de 2026:

- Censo: 72 bitácoras, 210 lecturas válidas, 69 con dos lectores independientes.
- Horizonte: 265 de 265 avisos leídos por tensión.
- Piloto de tres brazos: A 90 completados / 19 nulls · B 88 / 18 · C 86 / 20. (Agrega varias corridas — piloto del 31-ago, canarios, v3 y batches v4. Los números de la corrida v3 sola están en `ESTUDIO.md`.)

Si te conectas y los números cambiaron, la casa siguió trabajando.

## Para conectarlo

En claude.ai: Configuración → Conectores → agregar servidor MCP con la URL de arriba. En Claude Code: `claude mcp add tension https://pgmzclvqtvawfovtjiwf.supabase.co/functions/v1/mcp-tension`. El endpoint responde a `tools/call` por HTTP sin autenticación (verificado el 2-sep-2026); solo lectura, sin datos personales.
