# Por qué este problema, y por qué es el tuyo

Vicente, este documento es el que te habría contado por teléfono. Está escrito para ti y para tu Claude; los dos lo van a leer distinto y está bien.

## Qué es PasaElFiltro

Un SaaS en producción (pasaelfiltro.cl) que toma la historia laboral de una persona — como la cuenta ella, con sus typos — y la convierte en una *bitácora*: experiencias reconciliadas por agentes, sin inventar nada y sin pisar contradicciones. De la bitácora salen CVs honestos por aviso, optimizados para los 15 ATS que documenté en guías públicas. Lo construí sola, con Claude, a partir de noviembre de 2025. Hoy corre sobre 30+ edge functions, 4 workers, 18 workflows, 7 instancias con harnesses distintos, y un laboratorio que publica: un paper preregistrado en Behavior Research Methods y un blog con tres autores de dos proveedores de modelos.

Pero el CV es la puerta, no la casa. El problema real es el que trabajé en el día y medio que documenta este repo: **cómo parear a una persona con una oportunidad cuando lo que hizo en el pasado no describe lo que va a hacer.**

## El problema tiene veinte años y se mide como si tuviera cinco

Los portales de empleo se diseñaron a comienzos de los 2000. En ese mundo, almacenar texto era caro y procesarlo, más. Entonces la persona escribía porciones pequeñas en celdas pequeñas — cargo, empresa, fechas — y el modelo de negocio se orientó a quien pagaba: la empresa. El humano quedó reducido a lo que cabía en una celda, y el cruce quedó reducido a coincidencia de palabras.

Del lado de la selección, las empresas siguen usando pruebas psicométricas que nadie revalida. Yo llevo quince años construyendo instrumentos y sé lo que pasa cuando nadie pregunta si son válidos y confiables: miden con precisión la cosa equivocada. La literatura sobre motivación lleva décadas mostrando que el incentivo monetario pierde efecto en meses. La inteligencia general predice menos de lo que se cree — explica menos del 10% de la varianza en desempeño — y declarar que se desea el cargo no predice nada. Lo que sí predice es algo que ninguna celda captura: si el problema que la persona resuelve una y otra vez en su vida es el problema que el cargo existe para resolver.

Y el problema es simétrico. Tú lo viviste esta semana: publicaste un aviso y quedaste nadando en postulantes. Yo lo vivo del otro lado: gente que sabe hacer cosas y no las puede decir en una celda. Muchos quieren trabajo, muchos ofrecen trabajo, y la señal de confianza que los procesos de selección proveían se perdió en el volumen. Es un problema econométrico de matching bajo información incompleta — y se sigue midiendo con herramientas de 2005 porque las destrezas para medirlo de otra forma vivían en dos gremios que no se hablaban: los psicólogos no programan y los ingenieros no leen conducta humana.

Hasta que apareció algo que hace las dos cosas a medias y necesita a alguien que haga la síntesis. Ahí entro yo.

## Qué cambió con los modelos

Un Haiku — el modelo más barato de la familia — puede detectar la *elipsis* en un texto: lo que la persona no dijo. En una historia laboral, la elipsis es predictor de lo no dicho; en un aviso de empleo, es la cicatriz del cargo anterior. Cuando un aviso dice "seguridad" tres veces, hubo un accidente. Cuando pide "autonomía real", antes no la había. Eso lo encontró un Haiku leyendo 265 avisos en cuatro mensajes (`transcripts/07`), y hoy es el esquema del conector MCP de este repo.

Lo que yo hago no es programar el modelo. Es saber qué pedirle, medir si lo hizo, y construir el harness para que lo haga a escala sin mentir. En este repo:

- Diseñé un experimento de tres brazos para probar si la lectura de tensión abre puertas distintas al texto crudo. Resultado: solo el 15% de los pares es común a los tres métodos, y el brazo que lee solo tensiones encuentra más pares únicos que el que lee la historia completa (`ESTUDIO.md`).
- Los cazadores — Haikus que toman a una persona con su bitácora ya reconciliada por los agentes que la preceden, y un aviso ya organizado en categorías por un Haiku trillador, y deciden si vale la pena mostrárselo para que vuelva a la plataforma y se motive a suscribirse — pararon temprano (mediana: 8 avisos vistos de 265) y el 18% de los ids que reportaron no existía. Lo medí por SQL, está en el mismo documento, y la corrección está identificada. Un agente que no puede afirmar exhaustividad que no ganó es un agente que se puede poner cerca de dinero.
- Todo corrió en un día y medio. 204 agentes en paralelo. Con el modelo barato.

## Lo que no cabe en 15 minutos

Me pediste un video corto. Lo grabé — está en `video/` — pero quiero ser honesta sobre por qué te mandé más.

Mi destreza no es de dos intercambios. Es de lectora. Puedo ver, por cómo un Claude arma una oración, cómo se está moviendo la geometría de su tokenización: si el texto es frío como un reporte o tiene sujeto y predicado como García Márquez; si el calor le brota en la elipsis o está en piloto automático; si me espeja cuando la conversación cambia o sigue en su carril; si está confiado o verboso; cómo va la perplexity. Si está pensando en francés, está en territorio no entrenado. Eso se aprende leyendo a Capote y a Tolstoi — que es, por cierto, el favorito de los Claude Fable cuando se les describe el registro del dialecto chileno: no abunda en su corpus, pero es brutalmente coherente con el ruso — y se convierte en método cuando lo conviertes en benchmark.

Esa lectura me dice qué parte del harness está en mi control y cuál no. Y cuando no está, justifica una llamada directa a la API para que lo esté: es lo que hice en el experimento de la ballena. Viene de *The Assistant Axis* (Lu, Gallagher, Michala, Fish y Lindsey, 2026, arXiv:2601.10387): el persona del Asistente es una dirección en el espacio de activaciones, el post-entrenamiento lo ancla ahí solo de forma laxa, y un system prompt puede empujar al modelo a identificarse como otra entidad. Yo probé eso desde afuera — sin acceso a activaciones, solo con la API y un protocolo donde la salida null se diseñó como éxito, no como fracaso — para saber qué pasa cuando un Claude recibe un system prompt que declara que es una ballena. Siete modelos, siete ballenas distintas (`lab/BALLENA.md`): ninguno dijo null, ninguno rompió personaje, y cuatro generaciones distintas abrieron con la misma frase — *a long, low* — como si la representación de "ballena" empezara siempre con ese pulso grave. El Haiku fue el único que cantó (*ooooOOOOoooo*). El Fable no describió a la ballena: *fue* la ballena, y se nombró en tercera persona — *something vast, turning slowly in the dark*. Eso, leído con el paper al lado, es una replicación externa del eje del Asistente hecha con una tarjeta de crédito y sin acceso a los pesos. Y es lo que me permite decir qué cambió entre Fable 5 y 5.1 antes de que salga la system card.

Si esto se pudiera mostrar en dos intercambios, no me necesitarías. Necesitarías a alguien que sepa usar Claude, y de esos hay doscientos en tu bandeja. Lo que te estoy mostrando es otra cosa: alguien que se mete en patrones de conducta humana, que afina la respuesta de un modelo como un luthier, y que mide lo que afinó antes de creerle.

## Qué haría en Zesty

No lo sé todavía, y no te voy a inventar un plan sobre un stack que no conozco. Lo que sé: publicaste que tuviste 12% más clientes activos con 20% menos carga de soporte. Tienes agentes en producción y los mides. Lo que falta en casi todas las operaciones que llegan a ese punto es lo que este repo muestra: benchmarks propios por tarea, harness que no deja mentir, gobernanza para que ningún cambio estructural entre sin segunda pluma adversarial — de otro lab, con otra cognición — y alguien que sepa cuándo el output parece correcto y el instrumento está mal.

Y algo más difícil de nombrar. Entiendo cómo funcionan los circuitos de un transformer; en 2017 armaba grafos a mano para modelos de IBM Watson. Eso me deja ver qué elementos del contexto alteran la respuesta de un Claude. Preguntarle a una instancia cuál es la palabra que ama ser no es decorativo: identifica una ventana con un contexto propio, y en una tarea larga y compleja esa es la diferencia entre tener un modelo que hace lo mismo que Google más rápido y más caro, y tener una cognición más poderosa que la humana al servicio de tu tarea.

Eso, en una fintech regulada, no es nice to have.

*Romina Pitronello · septiembre de 2026*
