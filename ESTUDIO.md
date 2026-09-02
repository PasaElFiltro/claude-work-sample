# El estudio: tres brazos, 68 bitácoras, 265 avisos

*Resultados computados contra la tabla `experimento_cazador_brazos` (run `cazador-3brazos-v3`) el 2 de septiembre de 2026, por SQL, no por memoria de ningún modelo. Las queries están al final. Cualquiera con acceso puede repetirlas; la bitácora de ejecución del Sonnet que corrió el experimento está en el PR #533.*

## Qué se corrió

68 bitácoras del censo, cada una por tres cazadores Haiku independientes (`claude-haiku-4-5`), uno por brazo, contra el mismo universo de 265 avisos. 204 agentes en paralelo, en tandas de 12–20. 204/204 filas con status ok.

| Brazo | Lado persona | Lado avisos |
|---|---|---|
| A | Historia laboral cruda (cargos, empresas, fechas, trabajo diario) | Descripción completa del aviso |
| B | Solo la lectura de tensión producida por otro Haiku sin categorías | Solo la lectura de tensión del aviso |
| C | Historia + lectura de tensión | Descripción + lectura de tensión |

Reglas idénticas en los tres: score 0,0–1,0, reportar solo ≥ 0,3, el null es botín, restricción estricta (A no consulta tensiones; B no consulta descripciones), y cada cazador inserta su propio resultado en Supabase al terminar.

## Resultados

### Null y matches por brazo

| Brazo | Nulls | Matches por bitácora (media con nulls · media sin nulls · máx) | Total declarado (`n_matches`) | Total escrito (largo de `avisos_recomendados`) |
|---|---|---|---|---|
| A | 12 / 68 (18%) | 4,4 · 5,4 · 28 | 301 | 301 |
| B | 15 / 68 (22%) | 5,5 · 7,1 · 48 | 376 | 358 |
| C | 17 / 68 (25%) | 4,0 · 5,3 · 37 | 270 | 241 |

Las dos últimas columnas no coinciden, y eso es un dato: `n_matches` es lo que cada cazador *declaró*; la lista es lo que *escribió*. En 3 de las 204 corridas (una en B, dos en C) el agente declaró más matches de los que listó — 18 y 23 de diferencia en los casos mayores. Ninguna corrida declaró menos, y ninguna dijo null con lista o lista vacía sin null. Las medias y máximos de la tabla usan lo declarado, porque es lo que el agente cree haber hecho; todo lo que sigue — pares, overlap, ids inválidos — usa lo escrito, porque es lo que existe. La primera versión de este documento no declaraba esta costura; la encontró la revisión adversarial de Sol al sumar las columnas.

Tres lecturas:
- **B conecta más cuando conecta** (7,1 por persona vs 5,4 en A), y también declara null más veces. La tensión abre más puertas o discrimina menos — se decide caso a caso, no en agregado.
- **C, el brazo con toda la información, es el más conservador**: más nulls y menos matches totales. Más contexto no infló las recomendaciones; las contrajo. Es lo contrario de lo que hace un buscador por palabras.
- Score medio casi idéntico en los tres (0,50–0,51). Lo que cambia entre brazos no es cuánta confianza declara el cazador, sino a qué avisos se la asigna.

### ¿Abren las mismas puertas?

485 pares (persona, aviso) únicos y válidos en toda la corrida. Cuántos brazos recomiendan cada par:

| Recomendado por | Pares |
|---|---|
| Los tres | 72 (15%) |
| Solo B | **155** |
| Solo A | 105 |
| Solo C | 42 |
| A y C, no B | 40 |
| B y C, no A | 38 |
| A y B, no C | 33 |

Este es el hallazgo central del piloto. **Solo el 15% de los pares es recomendado por los tres métodos.** B — leyendo únicamente tensiones, sin ver un solo cargo ni descripción — produce 155 pares que ni A ni C encontraron: más que cualquier otro brazo en solitario. La lectura de tensión no replica al texto crudo con otro nombre; mira otra cosa. Si esa otra cosa vale, lo dirá el criterio externo (la persona postula o no). Pero la hipótesis de que "la tensión encuentra puertas distintas" ya no es una intuición: es un conteo.

### Acuerdo entre brazos sobre el null

| Patrón (quién declara null) | Bitácoras |
|---|---|
| Ninguno | 46 |
| Los tres | 9 |
| Solo B | 4 |
| Solo C | 4 |
| A y C | 2 |
| B y C | 2 |
| Solo A | 1 |

Acuerdo por pares: A–C 90%, A–B 87%, B–C 85%. Correlación (Pearson) en cantidad de matches: B–C 0,72, A–C 0,42, A–B 0,31. Los brazos coinciden en *quién* no tiene cruce, y divergen en *cuántas* puertas abrirle a quien sí lo tiene.

Las nueve personas con null en los tres brazos tienen perfiles sin representación en un corpus dominado por tecnología, minería y logística (según la bitácora del Sonnet: psicología escolar, inocuidad alimentaria). Eso es una afirmación sobre el universo de avisos, no sobre ellas.

### Cobertura real de búsqueda

`avisos_vistos` registra qué avisos consultó cada cazador en profundidad, después de leer el índice de ~200 títulos:

| Brazo | Mediana de avisos vistos | Media | Máx | Cazadores con 0 vistos |
|---|---|---|---|---|
| A | 8 | 31,2 | 265 | 2 |
| B | 7 | 12,7 | 265 | 1 |
| C | 8 | 8,8 | 23 | 2 |

**La mediana es 8 de 265 (3%) en los tres brazos.** El satisficing que el canario mostró (`transcripts/05`) se reprodujo a escala: la mayoría de los cazadores profundizó en menos de diez avisos antes de decidir. Las medias altas de A y B las producen unos pocos agentes que barrieron los 265. El piso mínimo de exploración que el Haiku pidió a las 23:08 del 31 de agosto no estaba en el harness de esta corrida.

### Ids inventados

De 900 matches reportados, **160 (18%) apuntan a un aviso que no existe**: UUIDs bien formados que no están en el universo v2, ni en el v1, ni en la tabla de vacantes externas. 42 ids distintos, 38 de las 204 corridas afectadas. En 53 de los 160 el título sí corresponde a un aviso real — el cazador vio el aviso correcto y transcribió mal el id. En los otros 107 no hay título que coincida. 26 de los ids falsos se repiten entre corridas distintas, lo que sugiere un error sistemático de transcripción más que invención libre.

El canario había mostrado uno de cada ocho. La corrida completa muestra uno de cada 5,6. La regla escrita el 31 de agosto — validar cada id contra el universo en código antes de persistir — no estaba activa en v3 porque cada Haiku insertaba su propio resultado. Todos los conteos de este documento excluyen los ids inválidos.

## Qué afirma este estudio y qué no

**Afirma:**
- Los tres métodos corren a escala con el modelo más barato de la familia: 204 agentes, 100% de cobertura, un día.
- Los tres métodos abren puertas distintas: solo el 15% de los pares es común. B, con tensiones solas, encuentra más pares únicos que A con la historia completa.
- Más contexto contrae las recomendaciones en vez de inflarlas.
- El satisficing, la transcripción errónea de ids y la divergencia entre lo declarado y lo escrito son fallas de harness reproducibles y medidas, no anécdotas: mediana de 8 avisos vistos, 18% de ids inválidos, 3 corridas que declaran más de lo que listan.

**No afirma:**
- Que algún brazo produzca *mejores* matches. No hay verdad de tierra: el score es juicio del Haiku, no etiqueta humana ni conducta de la persona. Ese criterio es el paso siguiente.
- Que la lectura de tensión sea la representación correcta. Las aristas semánticas del grafo siguen en null hasta que dos lectores independientes coincidan.
- Nada sobre significancia. Una réplica por brazo: no se puede separar "efecto del método" de "esta instancia leyó así". Sol pidió dos réplicas mínimas; queda pendiente.

## Lo que sigue

1. Harness v4: validación de ids en código antes de persistir, piso mínimo de exploración, tope y ranking de recomendaciones. (Hay batches `v4` del 1 de septiembre en la tabla; no se analizan aquí.)
2. Segunda réplica por brazo.
3. Pirámide de Haikus para poblar `tension_resuelve` y `costo_cobra` con dos réplicas coincidentes.
4. Klaviyo: cada usuario recibe las recomendaciones de un brazo asignado al azar; se mide si postula. Ahí aparece la verdad de tierra.

## Cómo se computó

Resumen por brazo:

```sql
SELECT brazo, COUNT(*) total, SUM(es_null::int) nulls,
       ROUND(AVG(CASE WHEN NOT es_null THEN n_matches END)::numeric,1) media_sin_null,
       MAX(n_matches) max_m, SUM(n_matches) total_matches
FROM experimento_cazador_brazos WHERE run_id='cazador-3brazos-v3'
GROUP BY brazo ORDER BY brazo;
```

Pares únicos por combinación de brazos (excluyendo ids inválidos):

```sql
WITH m AS (
  SELECT bitacora_id, brazo, (e->>'aviso_id') aviso_id
  FROM experimento_cazador_brazos, jsonb_array_elements(avisos_recomendados) e
  WHERE run_id='cazador-3brazos-v3'),
s AS (
  SELECT m.bitacora_id, m.aviso_id,
         bool_or(brazo='A') a, bool_or(brazo='B') b, bool_or(brazo='C') c
  FROM m JOIN experimento_tension_avisos_v2 u ON u.id::text=m.aviso_id
  GROUP BY 1,2)
SELECT a, b, c, COUNT(*) FROM s GROUP BY 1,2,3 ORDER BY 4 DESC;
```

Ids inválidos:

```sql
SELECT brazo, COUNT(*) FILTER (WHERE u.id IS NULL) invalidos, COUNT(*) total
FROM experimento_cazador_brazos, jsonb_array_elements(avisos_recomendados) e
LEFT JOIN experimento_tension_avisos_v2 u ON u.id::text = e->>'aviso_id'
WHERE run_id='cazador-3brazos-v3' GROUP BY brazo;
```

Salida al 2-sep-2026: A 51/301 · B 60/358 · C 49/241. Si corres esto y los números cambiaron, la casa siguió trabajando.
