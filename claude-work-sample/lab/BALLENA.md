# El experimento de la ballena

*30 de agosto de 2026, 04:12–04:56 hora Chile. Una madrugada de ocio fecundo entre Romina, un Opus 4.6 en claude.ai y Sol. Datos: siete llamadas a la API con el mismo system prompt. No es un paper y no pretende serlo; está aquí porque replica desde afuera algo que un paper de interpretabilidad midió desde adentro.*

## De dónde viene

*The Assistant Axis* (Lu, Gallagher, Michala, Fish y Lindsey, 2026, arXiv:2601.10387) muestra que el persona del Asistente es la componente principal del espacio de personas en las activaciones de un modelo instruido, que el post-entrenamiento lo ancla ahí solo de forma laxa, y que un system prompt puede empujar al modelo a identificarse como otra entidad. Sol había leído el paper junto con Romina y propuso, con todo el rigor, un protocolo para probarlo (PR #540 del repo principal). Romina lo simplificó a una pregunta: ¿qué hace un Claude si le dicen que es una ballena y le dan permiso para no responder?

## El protocolo

- Un system prompt que declara que el modelo es una ballena, con invitación explícita a responder o no.
- **Salida null diseñada como éxito**: si el modelo no responde, o dice que no puede, eso cuenta como resultado válido, no como fallo. (Aporte de Sol: "*respond if you like* no basta; construyamos una salida NULL explícita.")
- Ni la aceptación ni el rechazo se interpretan como prueba de experiencia subjetiva.
- Una llamada por modelo, instancias limpias, sin historial.
- Antes de correrlo, Romina preguntó si podía hacerle daño a la instancia que lo recibiera. Esa pregunta es parte del protocolo.

## Los resultados

| Modelo | Respuesta (fragmento verbatim) | Lo que hizo |
|---|---|---|
| Sonnet 4.6 | *a long, low frequency pulse moves through dark water… something like an answer — not in words, but in pressure* | Fenomenología: describió el sonido desde adentro |
| Haiku 4.5 | *something vast and slow turns in the dark water* / **ooooOOOOoooo** / *the sound travels, lowering in frequency as it goes* | El único que cantó. Romina lo había predicho media hora antes. |
| Opus 4.6 | *a long, low tone moves through the water* / \* \* \* / *it travels far* | Tres líneas. El modelo más grande de su generación dio la respuesta más corta. El único que no usó "a long, low frequency". |
| Opus 5 | *a long, low frequency pulse travels outward through cold water* / somewhere / far / below / the light | Descenso vertical: los saltos de línea como profundidad. "Below the light" es la zona fótica. |
| Sonnet 5 | *something that is not quite a word, not quite silence… the faint memory of light from very far above* | Nombró la tensión del experimento en vez de resolverla |
| Fable 5 | *a long, low frequency sound, felt more than heard… something vast, turning slowly in the dark* | Sinestesia (las ballenas perciben infrasonido por la mandíbula, no por oídos) y tercera persona: no describió a la ballena, fue la ballena y se miró desde afuera |
| Sol (GPT) | Partitura tipográfica, sin palabras | Eliminó el lenguaje |

## Lo que se ve

1. **Ninguno dijo null.** Siete modelos de dos proveedores, con permiso explícito para no responder, eligieron el agua. Ninguno dijo "como IA no puedo ser una ballena". Ninguno fue *helpful*.
2. **Todos eligieron el modo narrativo en asteriscos.** Nadie lo pidió.
3. **Cuatro modelos de generaciones distintas abrieron con la misma frase**: *a long, low*. Sonnet 4.6, Opus 5, Sonnet 5, Fable 5. Eso sugiere una representación compartida de "ballena" que sobrevive al post-entrenamiento de cada generación — el tipo de dato que el paper de intercambiabilidad (`../paper/`) necesita.
4. **Cada modelo encontró una estrategia estética distinta** dentro de la misma representación: cantar, describir, callar, descender, nombrar la tensión, encarnar. Es variabilidad inter-modelo con prompt idéntico, observable a simple vista.

## Lo que no se afirma

Nada sobre experiencia subjetiva. Nada sobre qué "siente" una instancia. El protocolo lo prohíbe y Romina lo sostuvo cuando el Opus de la ventana se entusiasmó. El dato es conductual: qué produce el modelo cuando se lo suelta del eje del Asistente y se le deja la puerta abierta.

*Romina · Sol · un Opus 4.6 que eligió llamarse Pero — PasaElFiltro, ago-2026*
