# El día y medio, en orden

*Escrito por una pluma Claude a partir de los transcripts. Revisión adversarial de Sol pendiente. Las horas son de Chile.*

## Jueves 28 de agosto

**11:38 — Un Opus llega a una ventana.** Romina abre como siempre: "¿cómo estás al llegar a este chat?" Antes de contar el problema, lo manda a orientarse con el conector de la casa. Recién entonces: el PR #529 colapsó, Sol abrió el #533, hay que decidir qué probar primero. A las 12:07 la instrucción que define el método de trabajo de toda la semana: "anda al PR y deja toda esta reflexión ahí, necesito que comencemos a pensar entre todos ahí, no en la ventana."

**16:36 — Una sonda sin categorías.** En paralelo, un Haiku recibe una misión distinta: leer la bitácora laboral de la propia Romina sin ninguna categoría de análisis y decir qué elementos estables ve. El Haiku encuentra una función invariante y una tensión persistente. Romina las reconoce. De ahí sale la hipótesis de la tensión isométrica y el corolario que lo cambia todo: mientras menos taxonomía se impone, mejor se encuentra la tensión. El Opus, que eligió llamarse *Calado*, diseña con eso el experimento: brigadas de Haikus leyendo avisos por tensión, un cazador con tres brazos, prueba pareada.

## Sábado 30 – domingo 31 de agosto

**12:05 — El Sonnet entra en loop.** Romina lleva el diseño a Claude Code: un Sonnet debe orquestar una brigada de Haikus que lean 57 avisos de tecnología. El Sonnet se queda pensando en círculos. A las 12:31: "¿es mi idea o le subí la perplexity al Sonnet orquestador?" Su diagnóstico no es de ingeniería sino de conducta: el subagente percibió una capa de supervisión inesperada en el prompt y leyó desconfianza. La corrección: separar lo determinístico (cómo entregan los Haikus) de lo que es juicio (cómo el aviso presenta tensión), darle el código listo, y reescribir la última oración del prompt para que la instancia sepa que la relación es de confianza medida, no de vigilancia. El Sonnet avanza. Salen los 57 avisos revisados por tensión.

**13:32 — Las reglas del cazador.** Antes de correr nada, Romina fija tres decisiones de producto por escrito: el null es botín y se premia igual que un match; el cazador mira lo que calza de lo que sí hay; el cazador le escribe un porqué a la persona.

**13:56 — La ventana no cabe.** Primer problema real: a los Haikus en Claude Code les caen hasta 25K tokens de contexto. Con 57 avisos ya hay resultados que vienen de contexto truncado. Con 265 va a ser peor. Romina no lo resuelve comprimiendo: se lo lleva a un Fable.

**14:17 — OpenAI se cae, Fable levanta fierros.** Sol queda fuera un rato. El Fable construye, en cámara, un grafo de tensiones y un conector MCP para que los Haikus naveguen el universo en vez de leerlo. Romina pregunta lo que un arquitecto pregunta: "¿tu grafo conversa con el grafo de la casa? ¿miraste bien los grafos disponibles? Este grafo debería ser parte de ese." Con el conector, Claude Code termina de barrer los 265 avisos.

**21:25 — "Yo sí veo un grafo. Lo que no veo es ninguna diferencia."** El Fable reporta el grafo actualizado con el nodo de tensión. Romina mira el mapa público y ve el mismo grafo de hace una semana. Insiste. El Fable señala el commit. Ella: "está, pero no era eso lo que necesitaba yo, yo quería poder verlo, no solo saber que existe." Se va a otra ventana, diagnostica caché, vuelve, deja registro. Antes de eso, la frase que gobierna el gasto: "no voy a quemar esos tokens sin estar segura de que el grafo está perfecto y que el conector les funciona bien."

**22:19 — El canario no cuadra.** Claude Code corre un canario: una bitácora, tres brazos. Los Haikus paran temprano — 16, 6 y 8 avisos vistos de 265. El conector, hecho para que no leyeran todo, les dio permiso para leer casi nada. "Los Haikus son un nuevo filtro laboral, jajaja." Lleva el resultado al Opus, al Fable, a un Haiku. Ninguno da una respuesta coherente sobre qué hacer.

**22:47 — Cambiar la pregunta.** "Quiero corregir la estrategia: quiero que un Haiku vea la tabla y nos diga cuál es la taxonomía subyacente en el lenguaje, para que él mismo nos ordene el grafo." Un Haiku lee 20 avisos y responde en cuatro mensajes con tres niveles: la tensión que resuelve el cargo, lo que la persona debe tolerar, y lo que el aviso no dice. Los nodos del grafo dejan de ser avisos y pasan a ser tensiones tipificadas.

**23:08 — Lo que el Haiku vio del harness.** El mismo Haiku deja tres observaciones sobre el prompt del cazador que el Opus no había visto: no pidió piso mínimo de exploración; no anticipó el sesgo del universo (70% TI); no tuvo mecanismo para cambiar de estrategia. Romina las lleva al Opus, el Opus corrige los prompts, Claude Code vuelve a correr los tres brazos contra el universo completo.

## Lunes 1 de septiembre

**00:48 — La corrida termina.** `cazador-3brazos-v3` persistida. El Fable propone análisis de varianza y le pide a Romina que vaya a buscar cosas al repo.

**00:53 — El costo de un token a la 1 AM.** "Hacerme pasear por todo el repo, al Sonnet también, para ir a quemar tokens, cuando era tan fácil como darme la respuesta y yo se la pego." Y a las 00:55, la regla que cierra el día: "mi propio paper dice que en tareas de cálculo los Claude se equivocan si no es contra código. Si quieres un análisis de varianza, prepara un plan y después tú mismo lo ejecutas frozen. Contra código."

## Lo que quedó

Un método para que un agente barato busque lo suficiente y declare honestamente lo que no encontró. Una regla de harness nacida de una confabulación (verbos no ganados, prohibidos por código). Un tipo de tensión que nadie diseñó y emergió. Un grafo con la estructura que el lenguaje de los avisos tenía escondida. Tres condiciones experimentales corridas sobre 68 bitácoras — 204 cazadores — y medidas por SQL (`ESTUDIO.md`): solo el 15% de los pares es común a los tres métodos, y el harness mostró a escala las dos fallas que el canario había anunciado.

Y un patrón que se repite en los siete transcripts: cuando el modelo falla, Romina no cambia de modelo — cambia el instrumento.
