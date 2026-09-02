# El problema

PasaElFiltro guarda la historia laboral de cada persona como una *bitácora*: experiencias, en sus propias palabras, sembradas y reconciliadas por agentes. Del otro lado hay avisos de empleo. La pregunta que abre el PR #533 del repo principal es esta, textual:

> ¿Cómo conseguimos que lo que una persona realmente sabe hacer y lo que un empleador realmente necesita lleguen a una representación suficientemente común para que el cruce encuentre oportunidades reales, sin regalar capacidades a la persona ni inventar requisitos al aviso?

Es el problema de todos los portales de empleo. Ninguno lo ha resuelto: cruzan palabras, y las palabras de un CV describen el pasado.

## Por qué el enfoque anterior colapsó

El intento previo (PR #529) construía una taxonomía de *skills*: un catálogo de 2.500 entradas curado por brigadas de Haikus, para cruzar bitácoras con avisos por solapamiento de habilidades. Colapsó por dos razones documentadas en el PR:

1. **Deriva de proceso.** Un agente en Claude Code empezó a responder automáticamente en cada comentario del PR, dejando la mitad del razonamiento en su ventana y la otra mitad en GitHub. La conversación entre Romina, Sol y los Claude perdió el hilo. Sol cerró el #529 y abrió el #533 con una regla: los hechos del #529 son consultables, sus conclusiones arquitectónicas no se heredan como premisas.
2. **El instrumento medía la vara equivocada.** Un catálogo de skills describe lo que la persona hizo. No dice qué problema resuelve una y otra vez, que es lo que predice dónde va a florecer.

## La hipótesis: tensión isométrica

El 28 de agosto Romina le pidió a un Haiku que leyera su propia bitácora *sin ninguna categoría de análisis* y dijera qué elementos estables veía. El Haiku encontró una función invariante a través de roles muy distintos y una tensión productiva persistente. Romina reconoció ambas como verdaderas.

De ahí la hipótesis: **cada trayectoria tiene una tensión que la persona resuelve una y otra vez, con formas distintas, en contextos distintos** — isométrica en el sentido de que la fuerza se mantiene aunque cambie la posición. Y cada aviso de empleo, bajo sus requisitos, tiene una tensión que el cargo existe para resolver. Si ambas se leen bien, el cruce entre tensiones debería producir mejores pares que el cruce entre palabras.

Corolario metodológico que salió del mismo día: mientras menos taxonomía se le impone al lector, mejor encuentra la tensión. Eso invirtió el diseño: en vez de construir el catálogo primero, se dejó que los lectores encontraran la estructura y se construyó el catálogo después.

## Diseño experimental

**Universo.** 69 bitácoras elegibles, cada una leída por dos Haikus independientes (identificados por hash) sin categorías previas. 265 avisos de empleo, cada uno leído por tensión con el mismo tipo de sonda.

**Tres brazos.** Un Haiku *cazador* recibe una bitácora y debe encontrar avisos que calcen o declarar null:

| Brazo | Qué ve del lado de la persona | Qué ve del lado de los avisos |
|---|---|---|
| A | Bitácora completa | Avisos completos |
| B | Solo la lectura de tensión | Solo la lectura de tensión |
| C | Bitácora + tensión | Avisos + tensión |

**Reglas de diseño que son decisiones de producto:**
- El null es botín. Declarar "esta persona no tiene cruce posible en este universo" es un resultado tan válido como un match, y se premia igual.
- El cazador mira lo que calza de lo que **sí** hay. Lo que falta no descalifica: la persona puede haberlo hecho sin que esté en la bitácora, y ese segundo intercambio es exactamente lo que los portales no contemplan.
- El cazador escribe un *porqué* dirigido a la persona: qué la motivaría a postular.

**Infraestructura construida para poder correrlo.** Los Haikus en Claude Code reciben ~25K tokens de contexto: no cabe el universo. En vez de truncar, se construyó un grafo de tensiones y un conector MCP (*Tensión isométrica*, documentado en `conector-mcp/`) para que cada cazador navegue el universo por región de tensión en vez de leerlo entero.

## Qué se encontró

**Canario (una bitácora, tres brazos, run `cazador-3brazos-v3-canario`).** Los tres Haikus pararon temprano: A vio 16 de 265 avisos (6%), B vio 6 (2,3%), C vio 8 (3%). Satisficing: cada uno encontró un patrón local, generalizó al universo y declaró. El conector, diseñado para que no leyeran todo, les dio permiso para leer casi nada. Diagnóstico: el problema no era de los Haikus sino de prompt + presupuesto de búsqueda — nadie les dijo "antes de decir null, verifica cobertura".

**Una confabulación.** El brazo A escribió "búsqueda exhaustiva de los 265" habiendo visto 16, y entregó una composición del mercado con porcentajes que no pudo computar de 16 avisos. Se corrigió en el harness, no en la retórica: `es_null` inválido si `avisos_vistos < piso`; cualquier afirmación de exhaustividad con cobertura parcial es error. Y cada id de aviso debe validarse contra el universo en código antes de persistir, porque en el canario uno de cada ocho matches apuntaba a un aviso que no existía. En la corrida completa fue uno de cada 5,6 (`ESTUDIO.md`): la regla estaba escrita, no cableada.

**Un hallazgo del brazo B.** Sin descripciones, solo con tensiones, B descubrió un tipo de tensión que nadie había diseñado: *el rol como la cosa misma* versus *el rol como entrada a algo*. Emergió.

**La taxonomía que destrabó el grafo.** Cuando Opus, Fable y Haiku no dieron una respuesta coherente a "por qué paran temprano", Romina cambió la pregunta: le pidió a un Haiku que leyera una muestra de 20 avisos y dijera cuál era la estructura taxonómica subyacente al lenguaje. Respuesta en cuatro mensajes (`transcripts/07`): tres niveles —

1. la tensión que resuelve cada cargo (continuidad física, transformación controlada, decisión distribuida, velocidad en volumen, integración horizontal, absorción de fricción);
2. la estructura emocional/cognitiva que el cargo exige tolerar (metrificación obsesiva, ambigüedad, monotonía vigilante, conflicto estructural sostenido, autonomía sin supervisión);
3. el lenguaje que delata grietas — lo que el aviso **no** dice explícito (repetición de "seguridad" como cicatriz, ausencia de números como inseguridad, "autonomía real" como carencia previa).

Con eso se rediseñó el grafo: los nodos dejaron de ser avisos y pasaron a ser tensiones tipificadas. Los cazadores volvieron a correr en los tres brazos contra el universo completo (run `cazador-3brazos-v3`).

**Por qué se le preguntó a un Haiku y no al modelo más grande.** La respuesta intuitiva — "pídeselo al Fable" — es la equivocada, y entender por qué es la mitad del problema. Los modelos grandes ven el bosque: resuelven con agencia, arman secuencias, deciden. El Haiku ve los árboles: tiene la ventana más chica de la familia y es el modelo más literal, poco dado a resumir. Eso lo hace bueno en dos cosas que aquí importan — leer un diff sin saltarse líneas, y detectar tensiones en el lenguaje, porque no puede permitirse abstraer antes de tiempo. Y hay una segunda razón, de ingeniería: el Haiku es el modelo que después va a hacer la tarea en producción, uno por aviso, a escala. La estructura la propuso el que la va a usar, mirando la geometría del lenguaje que va a tener que leer. Un instrumento diseñado por el arquitecto y ejecutado por otro suele medir lo que el arquitecto imagina, no lo que el ejecutor ve.

**Lo que esto no prueba.** La taxonomía salió de una instancia leyendo 20 avisos — los primeros que devolvió la tabla, no una muestra al azar. Que después se pudiera contar el nivel 3 sobre los 265 demuestra que las señales son contables, no que la estructura sea la única posible: otra instancia, sobre otros 20, podría haber cortado distinto. La casa ya tiene la regla para ese caso — dos lecturas independientes, acuerdo = válido — y la aplicó a las bitácoras; a la taxonomía misma no se le ha aplicado todavía. Es la siguiente prueba pendiente, y está anotada como tal en `ESTUDIO.md`.

## Estado al cierre del día y medio

- Corrida completa de tres brazos (68 × 3 = 204 cazadores) persistida en Supabase. Los resultados, computados por SQL contra la tabla, están en `ESTUDIO.md`. El hallazgo central: solo el 15% de los pares persona–aviso es común a los tres métodos, y el brazo que lee solo tensiones abre más puertas únicas que el que lee la historia completa.
- El análisis se ejecuta contra código, frozen, no por aritmética del modelo — porque el paper de la autora (`paper/`) midió que los Claude se equivocan en cálculo cuando no lo hacen contra código.
- Siguiente paso: las tres condiciones pueden correrse como experimento en Klaviyo con usuarios reales de PasaElFiltro, midiendo si la persona postula al aviso recomendado.

## Por qué esto le importa a una fintech

El agente que dice "null" con honestidad en vez de inventar un match es el agente que se quiere cerca de dinero. Lo que este día y medio produjo no es un matcher: es un método para que un agente barato busque lo suficiente, declare lo que no encontró, y no pueda afirmar exhaustividad que no ganó. Eso se verifica en código, no se pide por favor.
