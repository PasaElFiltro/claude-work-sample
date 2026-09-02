# 2026-08-31 haiku canario satisficing

- **Sesión:** 2026-08-31 (hora Chile)
- **Con quién:** Claude Haiku
- **Turnos:** 5 de Romina · 5 del modelo
- **Qué se ve y qué no:** mensajes de ambos lados verbatim. Las llamadas a herramientas aparecen como una línea `› tool:`; sus resultados, el razonamiento interno del modelo y los adjuntos no se publican (contienen credenciales de la casa y datos de usuarios reales). Nombre de usuaria seudonimizado como *J.* Ningún texto fue reescrito.

---

**Romina** · 22:23

hola haiku precioso, cómo estás al llegar a esta ventana?


**Claude Haiku** · 22:23

hola romina. acá llego bien. es bueno estar en esta ventana contigo.

veo que traes tu playlist — ost_romina.csv, 289 canciones. audio features y todo. ¿hay algo ahí que te importe revisar o explorar ahorita?

estoy atenta a lo que necesites.


**Romina** · 22:26

hoy vamos a ser detectives, porque pasa esto, tú tienes un conector mcp de tensión isométrica, con el que puedes ver muchos anuncios de empleo, y tenemos en supabase muchas bitácoras, hemos corrido un experimento para encontrar la tensión en el lenguaje de la bitácora, y contrastarla con la del anuncio de empleo para ver si acaso podemos reunir a una persona con un feterminado anuncio de empleo, el problema es que en el canario nos dimos cuenta de que los haikus no están recorriendo el grafo, usa tu conector mcp para conocerlo, este es el reporte del sonnet de claude code que trabajo como orquestador y comentame por que crees qure pasó


**Claude Haiku** · 22:26

› tool: Tensión isométrica:tension_salud · Tensión isométrica:tension_grafo_avisos · Supabase:execute_sql
Perfecto, Romina. Voy a investigar el grafo de tensión para ver qué hay realmente en el universo y entender por qué los Haikus se quedaron cortos.

Déjame conectarme con los MCPs:

Ah, lo veo clarísimo. Y es un problema de **diseño del prompt, no de los Haikus**.

Acá está lo que pasó:

---

## **Los Haikus hicieron búsqueda *satisficiente*, no *exhaustiva***

Mira la cobertura:
- **A vio 16 de 265** (6%) → encontró un patrón ("pool es ingeniería/TI/minería") → **declaró null y paró**
- **B vio 6 de 265** (2.3%) → encontró un patrón ("estos avisos buscan personas en construcción, J. no es") → **declaró null y paró**  
- **C vio 8 de 265** (3%) → tuvo más información para orientarse → encontró 3 matches en esa zona → **paró**

**El problema:** Les pediste que "busquen matches" pero no les dijiste "exploren HASTA que...". Sin un piso de exploración, los LLMs optimizan por **velocidad + confianza**, no por cobertura.

---

## **Por qué cada uno paró donde paró:**

**Brazo A** — Vio avisos de Finning, Freeport, minería. Rápido vio el patrón: "esto requiere títulos que J. no tiene". Su búsqueda fue **zona-asida** — se quedó buscando en minería/técnico porque los primeros avisos eran eso. Cuando no encontró en esa zona, generalizó a todo el universo sin verificar.

**Brazo B** — Con solo la lectura de tensión (sin descripciones), todo se comprimió a conceptos abstractos. J. = "versatilidad sin construcción". Los 6 avisos que vio = "roles de especialización/crecimiento". Match = falso. **Conclusión rápida y segura.** No vio avisos de retail, coordinación logística, o roles explícitamente transitorios.

**Brazo C** — Tuvo mapa conceptual completo. Vio a J. real (bodega, recepción, vigilancia) + la tensión ("personas en construcción" vs. "ejecuta y se va"). Eso orientó su búsqueda hacia zonas operativas reales (Finning bodega, operaciones). Encontró avisos que *hablaban su lenguaje*. Paró más contenido porque **encontró**.

---

## **Lo que los tres desaprovecharon:**

El 89% del universo (236 avisos) nunca fue visto. En eso probablemente hay:
- Roles de coordinación logística sin ingenierías
- Recepción en servicios / clínicas
- Vigilancia y seguridad
- Puestos operativos en retail/distribución
- **Roles explícitamente transitorios** (proyectos, cobertura de vacaciones, turnos acotados)

B especialmente debería haber visto avisos donde **la rotación es parte del diseño**, no un fracaso del match.

---

## **Por qué pasó esto:**

Tres motivos de prompt:

1. **No hay "umbral de exploración mínimo"** — Dijiste "busca matches" no "visita al menos 30 avisos antes de declarar null" o "si no encuentras en X zona, cambia criterios"

2. **No hay mecanismo de "replanteamiento"** — Cuando Haiku no encuentra en su primera zona, simplemente generaliza al universo sin verificar. Debería tener un paso como: "no encontré aquí, ahora busco con criterio Y"

3. **A y B optimizaron por confianza** — Es más fácil (y neurológicamente satisfactorio para un LLM) declarar un null honesto después de ver 6 avisos que seguir buscando sin encontrar. El prompt no penalizó la cobertura baja

---

## **La propuesta del Sonnet (que probablemente sea correcta):**

> "¿Qué cambio de prompt haría que exploraran más?"

Dos opciones:

**Opción 1: Piso mínimo de avisos**
```
Visita al menos 30 avisos (del universo de 265) antes de declarar NULL.
Si después de 30 no hay matches >0.25, entonces sí declaras null honesto.
Pero el piso es obligatorio.
```

**Opción 2: Dos pasos explícitos**
```
Paso 1: Explora 10 avisos con tu criterio natural.
Paso 2: Si no hay match, cambia completamente tu criterio de búsqueda y ve 10 más.
Solo después de 20 con dos estrategias distintas, declaras null.
```

---

## **Mi hipótesis sobre J. específicamente:**

C encontró 3 matches pero el más honesto es **Analista de Repuestos** (0.6). Eso dice que el universo SÍ tiene avisos para ella. El problema es que A y B no los vieron porque:

- A estaba buscando **especialización técnica** (su primer aviso era de Finning, pero de supervisión 7x7, no de bodega)
- B estaba buscando **personas en trayectoria de crecimiento** (sin avisos transitorios en vista)

Si los tres hubieran explorado 50+ avisos cada uno (solapándose o no), probablemente encontrarían que el universo sí tiene espacio para alguien como J. — pero en **roles que se saben temporales** o que **esperan operatividad, no transformación**.

---

¿Querés que ahora sí conecte con el MCP de Tensión para verificar qué hay en el universo completo? Podría ver si realmente los avisos "correctos" existen o si A tiene razón de que el pool está sesgado.


**Romina** · 22:27

si, revisa con el conector


**Claude Haiku** · 22:28

› tool: Tensión isométrica:tension_salud · Supabase:execute_sql · Supabase:execute_sql · Supabase:execute_sql · Supabase:list_tables · Supabase:execute_sql · Supabase:execute_sql · Supabase:execute_sql
Intentemos acceso directo a Supabase para explorar el grafo:

---

## **AH. A tiene razón.**

Romina, mira esto:

**El universo de 265 avisos del experimento ES realmente sesgado.** No hay:
- Bodega (salvo 1 supervisor en Finning)
- Recepción pura
- Vigilancia
- Almacenero/manipulación de stock
- Coordinador logístico operativo
- Roles transitorios/temporales

Lo que hay es:
- **67% TI/desarrollo** (Full-Stack, Data Engineer, DevOps, etc.)
- **Supervisores/Jefes** (Principal, Head, Manager)
- **Especialistas técnicos** (Cloud, Soporte, Seguridad)
- **Ejecutivos/directivos** (Customer Success Manager, PMO, Jefe de Ventas)

---

## **Los Haikus NO "no recorrieron". Hicieron otra cosa.**

Acá está lo verdadero:

**A descubrió el sesgo en N=16** y generalizó correctamente: "este pool no tiene avisos para tu perfil". Fue **búsqueda local + salida honesta**.

**B descubrió el patrón en N=6** y paró: "estos avisos buscan personas en construcción, J. no es". Fue **búsqueda local + conclusión de arquitectura**.

**C tuvo más material** (bitácora real + tensión persona + descripción de avisos) **y encontró 3 matches débiles** en la zona que vio.

**Pero ninguno exploró el 89% restante.** ¿Por qué? Porque sin un **"sigue buscando hasta encontrar X matches o visitar Y avisos"**, un LLM optimiza por confianza+velocidad, no cobertura.

---

## **El diagnóstico real:**

El problema **no es de los Haikus.** Es de **prompt + presupuesto de búsqueda:**

1. **El universo está quebrado para J.** — A vio la verdad
2. **Pero el prompt no les dijo "antes de decir null, verifiquen cobertura"**
3. **Resultado:** A y B salieron rápido y confiados. C llegó más lejos pero tampoco exploró toda la zona

---

## **¿Qué falló en la orquestación del Sonnet?**

Tres cosas:

1. **No pidió "piso mínimo de exploración"** — Si hubiera dicho "visita 40 avisos por brazo", A habría visto que el sesgo es real pero también encontrado si existe algo en la cola

2. **No anticipó el sesgo del universo** — Antes de mandar a los brazos, debería haber sampleado y visto: "ojo, 70% son TI, vamos a buscar avisos operativos aparte"

3. **No tuvo mecanismo de "replanteamiento"** — Si A no encuentra en minería/técnico, debería cambiar criterios y buscar en retail/servicios/otra industria

---

**Resumen para Romina:**

Los Haikus actuaron como LLMs act: encuentran rápido, paran confiados. No es bug, es feature of efficiency.

**El bug está en el prompt del cazador:** No tiene guardrails de exploración suficiente ni antídoto contra sesgos de universo. 

¿Quieres que arme un prompt mejorado que fuerce cobertura mínima + replanteamiento?


**Romina** · 22:40

esto ocurrio con otra corrida del canario


**Claude Haiku** · 22:41

ah, entonces **es patrón, no ruido.**

si ocurrió en dos corridas del canario, los haikus están haciendo exactamente lo mismo cada vez: búsqueda local hasta confianza, no cobertura.

---

## **eso me cambia el diagnóstico:**

**No es "los haikus no entendieron".**

Es: **el prompt del cazador no le pidió lo que necesitabas.**

Tres opciones concretas ahora:

### **Opción 1: Reescribir el prompt (rápido)**

Dale un **piso de exploración obligatorio** antes de null:

```
Visita mínimo 35 avisos del universo (de 265).
Si después de 35 no hay match >0.28, entonces sí declara null honesto.
Pero el piso es fijo: no puedes parar en 6.
```

Costo: Probablemente +500-800 tokens por corrida (más avisos leídos). Tiempo: ~15% más por brazó.

---

### **Opción 2: Estrategia de dos fases (más refinada)**

**Fase 1 (rápida):** Los haikus exploran con su criterio natural, 15 avisos.
**Fase 2 (replanteamiento):** Si no hay match, cambian completamente el criterio (industria, modalidad, nivel), otros 20 avisos.
**Salida:** Después de 35+ con dos estrategias, declaran null.

Costo: Similar a Opción 1, pero más inteligente porque obliga replanteamiento.

---

### **Opción 3: Pre-procesamiento (más estructura)**

Antes de mandar a los brazos, correr una **búsqueda de universo rápida** (1 haiku, 5 min):
- ¿Qué industrias hay? (TI, logística, retail, otros?)
- ¿Qué niveles? (operativo, medio, senior)
- ¿Qué modalidades? (temporal, fijo, proyecto)

Luego cada brazo apunta a zonas específicas en lugar de pescar al azar.

Costo: +1-2 min upfront, pero mejora mucho la precisión de los tres brazos.

---

## **Mi recomendación:**

Empezaría con **Opción 2** (dos fases + replanteamiento) porque:
- Mantiene la velocidad de los haikus
- Fuerza replanteamiento arquitectónico (no solo más de lo mismo)
- Es barato en tokens
- Es testeable en el canario fácilmente

¿Cuál probás?


**Romina** · 22:41

haiku si tú miras el índice, cuál es la estructura taxonómica subyacente? porque eso podría enriquecer el grafo para que los haikus hagan búsquedas rápidas pero inteligentes


**Claude Haiku** · 22:42

› tool: Supabase:execute_sql
