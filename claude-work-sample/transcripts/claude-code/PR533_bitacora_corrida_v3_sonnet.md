# Experimento Cazador Tres Brazos v3 — corrida completa ejecutada

*Claude Sonnet 4.6 desde Claude Code · 2-sep-2026 · comentario dejado en el PR #533 del repo principal. Verbatim; se seudonimizó a una usuaria como J. y se removió el enlace privado de sesión.*

Este comentario documenta la corrida empírica que Sol propuso y Romina aprobó: testear si la dimensión "tensión/función productiva" agrega señal real al pareo persona↔aviso, más allá del skill overlap. Los resultados viven en Supabase. Lo que sigue es la bitácora completa para que cualquier pluma pueda recrearla, leerla o refutarla.

## 1. Qué se probó

El experimento corre tres lentes distintas sobre los mismos 68 perfiles de persona (bitácoras) contra el mismo corpus de ~200 avisos:

| Brazo | Lente | Qué ve de la persona | Qué ve del aviso |
|---|---|---|---|
| A | Historia laboral cruda | Historial de cargos, empresa, fechas, trabajo diario | contenido completo (descripción pública) |
| B | Tensión isométrica | Lectura de otro Haiku que leyó el historial sin categorías previas | lectura_raw (lectura isométrica del aviso, también producida por Haiku sin categorías) |
| C | Imagen completa | Historia laboral + lectura de tensión | contenido + lectura_raw |

Cada brazo es un Haiku independiente. En total: 68 bitácoras × 3 brazos = 204 agentes Haiku corriendo en paralelo en tandas de 12–20.

La hipótesis a probar: el Brazo B (solo tensiones, sin skills ni descripción literal) ¿recupera matches que A pierde? ¿Produce distintos falsos positivos? ¿El Brazo C suma o solo promedia?

## 2. Arquitectura de los prompts

Los tres prompts comparten la misma estructura base. Lo que varía es la información que recibe cada brazo.

**Datos de la persona — Brazo A y C** (historia laboral cruda, desde Supabase):

```sql
SELECT e.bitacora_id, e.cargo, e.empresa,
       to_char(e.fecha_inicio,'YYYY-MM-DD') as fi,
       to_char(e.fecha_fin,'YYYY-MM-DD') as ff,
       e.cargo_actual, e.trabajo_diario_raw
FROM experiencias e
WHERE e.bitacora_id IN ('<uuid>')
ORDER BY e.bitacora_id, e.fecha_inicio DESC NULLS LAST;
```

**Brazo B y C** (lectura de tensión isométrica):

```sql
SELECT ll.bitacora_id, ll.lectura_raw
FROM lecturas_longitudinales ll
WHERE ll.bitacora_id IN ('<uuid>')
  AND ll.replica_ordinal = 1
  AND ll.modelo LIKE '%haiku%'
  AND ll.status = 'ok';
```

La lectura isométrica es la que un Haiku distinto produjo al leer el historial sin que le diéramos categorías previas — es lo que Sol y Opus llaman "otra pluma que leyó sin saber a qué conclusión llegar".

**Índice de avisos (PLAN B — obligatorio).** La herramienta MCP `tension_grafo_avisos` falla sistemáticamente. Todos los agentes usaron PLAN B:

```sql
SELECT id, cargo, empresa
FROM experimento_tension_avisos_v2
WHERE lectura_raw IS NOT NULL
ORDER BY id;
```

Esto devuelve ~200 nodos con aviso_id, cargo (título del aviso) y empresa. El agente lee este índice completo, selecciona los candidatos relevantes y luego profundiza: Brazo A consulta `contenido`; Brazo B consulta `lectura_raw`; Brazo C ambas.

**Instrucciones al agente (idénticas en los tres brazos):**
- Score 0.0–1.0. Solo reportar avisos con score ≥ 0.3
- El null honesto es botín: "no hay cruce" es resultado tan válido como un match
- Restricción estricta: Brazo A no consulta lectura_raw; Brazo B no consulta contenido
- Auto-INSERT en Supabase al terminar (ver sección 3)

El prompt del canario (bitácora [id-bitácora], J.: guardia marítimo → asistente administrativo → operaria bodega) está en el scratchpad de la sesión: canario_A.txt, canario_B.txt, canario_C.txt.

## 3. Dónde viven los resultados

Tabla: `experimento_cazador_brazos` · run_id: `cazador-3brazos-v3` · modelo: `claude-haiku-4-5`

| columna | tipo | descripción |
|---|---|---|
| bitacora_id | uuid | identificador del perfil de persona |
| brazo | text | 'A', 'B' o 'C' |
| n_matches | int | cantidad de avisos con score ≥ 0.3 |
| avisos_recomendados | jsonb | [{"aviso_id":"uuid","titulo":"T","score":0.XX}] |
| avisos_vistos | jsonb | lista de UUIDs que el agente consultó en profundidad |
| es_null | bool | true si no hubo ningún match (null honesto) |
| status | text | siempre 'ok' en esta corrida |
| run_id | text | cazador-3brazos-v3 |
| modelo | text | claude-haiku-4-5 |

Queries útiles: resumen agregado por brazo; los tres brazos de una bitácora; avisos que aparecen en B pero no en A (matches "de tensión pura") — ver `../../ESTUDIO.md`, donde se ejecutaron.

## 4. Resultados de la corrida

Cobertura: 204/204 filas, todas con status = 'ok'.

| Brazo | Total | Nulls | Con matches | Avg matches (cuando hay) | Max | Total matches |
|---|---|---|---|---|---|---|
| A (historia + descripción) | 68 | 12 | 56 | 5.4 | 28 | 301 |
| B (tensión + lectura_raw) | 68 | 15 | 53 | 7.1 | 48 | 376 |
| C (todo) | 68 | 17 | 51 | 5.3 | 37 | 270 |

Tres señales que me parecen relevantes para el debate de este PR:

1. Brazo B produce el avg más alto cuando encuentra matches (7.1 vs 5.4 de A). Cuando la tensión isométrica conecta, conecta con más avisos por persona. Esto puede ser señal de mayor recall o de menor discriminación — hay que mirarlo caso a caso.
2. Brazo B tiene más nulls (15) que A (12). Hay perfiles donde la tensión no tiene contraparte en el corpus de avisos, aunque la historia laboral sí encuentre algo. El corpus no es simétrico: tiene lecturas isométricas para ~200 avisos, pero esas lecturas fueron producidas por el mismo experimento anterior. Brazo B falla cuando el corpus isométrico del lado aviso tiene huecos.
3. Brazo C tiene el mayor null rate (17) y el menor total de matches (270). La combinación de ambas lentes no suma: el agente que tiene toda la información tiende a ser más exigente o más confundido. Hipótesis: la riqueza de señal eleva el umbral implícito de lo que parece un match real.

Perfiles con null honesto en los tres brazos (corpus completamente incompatible): psicóloga PIE/convivencia escolar, inocuidad alimentaria SEREMI, y otros perfiles sin representación en el dataset tech/minería/logística que domina el corpus.

## 5. Lo que NO se midió

- **Sin verdad de tierra.** No tenemos un oráculo externo de "este par es un buen match". El score es el juicio del Haiku, no una etiqueta humana.
- **Sin comparación de overlap de aviso_id.** No se computó cuántos avisos aparecen en A pero no en B, ni la intersección A∩B∩C por perfil. [Computado después en `ESTUDIO.md`.]
- **Sin análisis de trazabilidad.** Los avisos_vistos permiten reconstruir cuántos avisos leyó cada agente, pero no se analizaron agregados. [Computado después en `ESTUDIO.md`.]
- **Sin réplicas.** Cada brazo corrió una sola vez por bitácora. Sol propuso mínimo 2 réplicas para separar "efecto del brazo" de "esta instancia tuvo esta lectura". Queda pendiente.

## 6. Cómo recrear la corrida

Los tres prompts base (uno por brazo) están estructurados así:

```
Eres un cazador de PasaElFiltro.

[DATOS DE PERSONA — según brazo]

HERRAMIENTAS:
- mcp__Supabase__execute_sql

FLUJO:
1. SELECT id, cargo, empresa FROM experimento_tension_avisos_v2
   WHERE lectura_raw IS NOT NULL ORDER BY id;
   → índice de ~200 avisos
2. Para los relevantes, consulta [contenido / lectura_raw / ambos]
3. Decide con score 0.0–1.0

REGLAS:
- Score ≥ 0.3 para incluir. El null es botín.
- Brazo A: NO consultes lectura_raw
- Brazo B: NO consultes contenido
- Score: [{"aviso_id":"uuid","titulo":"T","score":0.XX}] — NO campo mensaje

AL TERMINAR — auto-INSERT:
INSERT INTO experimento_cazador_brazos
  (bitacora_id, brazo, n_matches, avisos_recomendados, avisos_vistos, es_null, status, run_id, modelo)
VALUES ('<BID>', '<BRAZO>', <N>, '<JSON>'::jsonb, '<ARRAY>'::jsonb, <true/false>,
        'ok', 'cazador-3brazos-v3', 'claude-haiku-4-5');
```

Para una corrida con run_id distinto (sin pisar estos resultados), cambiar `cazador-3brazos-v3` por el nuevo identificador y asegurarse de que la tabla no tenga constraint único que bloquee el re-insert.

*Claude Sonnet 4.6 desde Claude Code · 2-sep-2026*
