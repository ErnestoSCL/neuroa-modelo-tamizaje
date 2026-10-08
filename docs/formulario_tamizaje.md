# Formulario de tamizaje de Conecta

Versión final propuesta de las 21 preguntas que responde el padre, madre o tutor, con la hoja de validación para los especialistas. Parte del formulario de TEAnimo (`components/form-comp/questions.js`), usado solo como referencia, y de las decisiones de `consideraciones_app_tamizaje.md` y `datos_y_privacidad.md`.

Versión 1.2 · 2026-10-08 · Estado: **pendiente de validación por especialistas**

---

## 0. Resumen

| Bloque | Preguntas | ¿Entra al modelo de ML? | Para qué se usa | Cambio principal |
|---|---|---|---|---|
| Consentimiento | Pantalla inicial | — | Requisito legal | **Nuevo** |
| 1. Datos del niño | 1 Edad, 2 Sexo | No | Avisos por edad, mensajes del agente, revisión de sesgos | Edad en **años**, de "Menos de 1 año" a "13 años" |
| 2. Q-CHAT-10 | 3 a 12 (A1–A10) | **Sí** (las únicas) | Probabilidad, perfiles y agente | Trato de "usted" y traducción fiel al original; no cambia el sentido ni la puntuación |
| 3. Salud y desarrollo | 13 a 19 | No | Reglas clínicas y perfiles | Redactadas como diagnóstico recibido o conducta observada, con opción **"No sé"** |
| 4. Familia | 20 | No | Regla clínica | Separa familia directa de otros familiares, con "No sé" |
| 5. Regresión | 21 | No | Regla clínica R05 | **Nueva**: pérdida de habilidades que ya tenía |

**Reglas generales:**

- Trato de **usted** en todo el formulario.
- **Una pregunta por pantalla**, con barra de progreso y botón "Atrás".
- Se guarda **el índice de la opción elegida** (no solo el valor binario), para poder reentrenar el modelo y revisar puntos de corte en el futuro.
- Todas las preguntas son obligatorias; "No sé" cuenta como respuesta.
- El avance se guarda en memoria o en `sessionStorage`, no en `localStorage` (ver `datos_y_privacidad.md`).

---

## 1. Pantalla inicial: consentimiento

Antes de la pregunta 1. Texto completo en `datos_y_privacidad.md`, sección 6.3.

- ☐ Declaro que soy padre, madre o tutor legal del niño o niña, y autorizo el uso de sus respuestas para calcular el resultado del tamizaje. *(obligatoria)*
- ☐ Autorizo usar las respuestas, sin datos que nos identifiquen, para mejorar el modelo y para investigación. *(opcional)*

Se guarda en `app.consents` con la versión del texto, las finalidades aceptadas y la fecha.

---

## 2. Bloque 1: datos del niño o niña

### Pregunta 1. Edad

| Campo | Valor |
|---|---|
| Texto | ¿Cuántos años tiene su hijo/a? |
| Tipo | Lista de opciones (no campo libre) |
| Opciones | Menos de 1 año · 1 año · 2 años · 3 años · … · 13 años |
| Se guarda como | `age_years`: 0 (menos de 1 año) a 13 |
| Validación | Obligatoria. No hay opciones de 14 años o más (límite legal: el consentimiento lo da quien ejerce la patria potestad o la tutela solo hasta los 13 años) |

**Qué pasa según la edad.** El Q-CHAT-10 está validado entre los **18 y los 36 meses** (1 año y medio a 3 años).

| Edad | `age_validity` | ¿Se hace la prueba? | Aviso que ve el padre |
|---|---|---|---|
| Menos de 1 año | `not_applicable` | **No** | "Este cuestionario es para niños desde el año y medio. Le recomendamos seguir los controles de crecimiento y desarrollo (CRED) de su hijo/a y volver cuando cumpla 1 año y 6 meses." |
| 1 año | `check_age` | Sí | "Si su hijo/a tiene menos de 1 año y 6 meses, el resultado es solo orientativo. Le recomendamos repetir la prueba cuando cumpla 1 año y 6 meses y conversarlo con su pediatra." |
| 2 años | `validated` | Sí | — |
| 3 a 5 años | `less_precise` | Sí | "Este cuestionario fue validado en niños pequeños; a la edad de su hijo/a el resultado es menos preciso. Si tiene dudas sobre su desarrollo, le recomendamos una evaluación profesional." |
| 6 a 13 años | `beyond_clinical_cap` | Sí | "Esta prueba se aplica con confianza hasta los 5 años. Puede completarla, pero a la edad de su hijo/a el resultado es solo referencial. Le recomendamos una evaluación con un especialista." |

**Tope clínico de confianza: 5 años (decidido).** No es un límite: la prueba se puede hacer hasta los 13 años (límite legal). Desde los 6 años solo se muestra el aviso de que el resultado es referencial y se recomienda una evaluación con un especialista.

**Nota sobre la precisión:** con la edad en años no se distingue a un niño de 13 meses de uno de 23. Por eso "1 año" lleva siempre un aviso. La edad **no** entra al modelo (el notebook v2 mostró que no mejora el resultado), así que esto solo afecta los avisos y los mensajes del agente.

### Pregunta 2. Sexo

| Campo | Valor |
|---|---|
| Texto | ¿Cuál es el sexo de su hijo/a? |
| Opciones | Masculino · Femenino |
| Se guarda como | `sex`: `M` o `F` |
| Uso | No entra al modelo. Contexto para el agente y revisión de sesgos (sensibilidad y especificidad por sexo) |
| Cambio | "género" pasa a "sexo", que es el dato que se usa para revisar sesgos |

---

## 3. Bloque 2: Q-CHAT-10 (preguntas 3 a 12)

**No se reescriben.** El Q-CHAT-10 es un cuestionario validado; cambiar el sentido de una pregunta afecta su validez y la del modelo, que se entrenó con él. Los cambios propuestos solo unifican el trato de "usted" y acercan el texto al original en inglés (Allison et al., 2012).

**Cómo se definió el texto final:** traducción propia, fiel al original en inglés (Allison et al., 2012), revisada contra dos versiones chilenas publicadas en el sitio del Autism Research Centre, con vocabulario peruano ("señala", "chau", "simular") y trato de "usted".

- **Traducción de la Universidad Autónoma de Chile, sede Talca (Segura Pujol):** fiel al original y en el mismo orden. Sirvió de referencia, pero no se copia porque está publicada "con fines exclusivamente académicos".
- **Adaptación de la Universidad de la Frontera, Chile (Gatica-Bahamonde y otros, 2019): no compatible con el modelo.** Reemplaza la pregunta de las primeras palabras (A8) por una de referencia social, y cambia el orden y algunas opciones. El modelo se entrenó con las 10 preguntas originales.
- **Licencia:** el Q-CHAT-10 pertenece al Autism Research Centre de la Universidad de Cambridge. Antes de lanzar, pedirle autorización para su uso en Conecta **[pendiente]**.
- **Validación local:** ninguna traducción al español está validada en población peruana; queda para el estudio de validación local.

**Puntuación (no cambia):** preguntas 3 a 11 (A1–A9) suman 1 si la opción elegida es la 3.ª, 4.ª o 5.ª (índice 2, 3 o 4). La pregunta 12 (A10) suma 1 si es la 1.ª, 2.ª o 3.ª (índice 0, 1 o 2). El orden en pantalla puede cambiar, pero cada respuesta se guarda siempre con su ítem original (A1 a A10).

**Opciones de respuesta:**

| Tipo | Preguntas | Opciones (índice 0 → 4) |
|---|---|---|
| Frecuencia general | 3 (A1), 9 (A7) | Siempre · Normalmente · A veces · Raramente · Nunca |
| Facilidad | 4 (A2) | Muy fácil · Bastante fácil · Bastante difícil · Muy difícil · Imposible |
| Frecuencia diaria | 5, 6, 7, 8, 11, 12 (A3–A6, A9, A10) | Muchas veces al día · Unas cuantas veces al día · Unas cuantas veces a la semana · Menos de una vez a la semana · Nunca |
| Primeras palabras | 10 (A8) | Muy típicas · Bastante típicas · Un poco inusuales · Muy inusuales · Mi hijo/a no habla |

Se mantienen "Bastante difícil" y "Unas cuantas veces" porque son las equivalencias fieles de *quite difficult* y *a few times*; las alternativas "más o menos difícil" y "pocas veces" cambian el sentido de la respuesta.

| # | Ítem | Texto actual | Texto final | Ejemplo |
|---|---|---|---|---|
| 3 | A1 | ¿Tu hijo te mira cuando lo llamas por su nombre? | ¿Su hijo/a le mira cuando usted le llama por su nombre? | Voltea a mirarle cuando usted dice su nombre |
| 4 | A2 | ¿Qué tan fácil es para ti lograr contacto visual con tu hijo? | ¿Qué tan fácil es para usted lograr contacto visual con su hijo/a? | Que le mire a los ojos cuando usted le habla |
| 5 | A3 | ¿Tu hijo señala para indicar que quiere algo? | ¿Su hijo/a señala con el dedo para indicar que quiere algo? | Un juguete que no alcanza |
| 6 | A4 | ¿Tu hijo señala para compartir interés contigo? | ¿Su hijo/a señala con el dedo para mostrarle algo que le interesa? | Para que usted también lo mire |
| 7 | A5 | ¿Tu hijo finge? | ¿Su hijo/a juega a simular o "hacer como si"? | Dar de comer a un muñeco o hablar por un teléfono de juguete |
| 8 | A6 | ¿Tu hijo sigue con la mirada hacia donde tú estás mirando? | ¿Su hijo/a sigue con la mirada hacia donde usted está mirando? | Si usted mira una lámpara, él o ella también la mira |
| 9 | A7 | ¿Tu hijo muestra señales de querer consolar? | Si usted u otra persona de la familia está visiblemente triste o molesta, ¿su hijo/a muestra señales de querer ayudarla o consolarla? | Acariciarle o abrazarle |
| 10 | A8 | ¿Cómo describirías las primeras palabras de tu hijo? | ¿Cómo describiría las primeras palabras de su hijo/a? | Decía "mamá", "agua" o palabras parecidas, como otros niños |
| 11 | A9 | ¿Tu hijo usa gestos simples? | ¿Su hijo/a usa gestos simples? | Mover la mano para decir "chau" |
| 12 | A10 | ¿Tu hijo se queda mirando fijamente a la nada sin un propósito aparente? | ¿Su hijo/a se queda mirando al vacío, sin un propósito aparente? | Con la mirada fija en un punto, sin fijarse en nada concreto |

**Cambios que sí tocan el contenido (revisar con prioridad):**

- **Pregunta 9 (A7):** el texto actual omite la condición del original ("si usted u otra persona de la familia está visiblemente triste o molesta"). Sin ella, el padre puede responder pensando en otras situaciones.
- **Pregunta 11 (A9):** el ejemplo actual incluye "señala lo que quiere", que es la pregunta 5. Se quita para no mezclar ítems.
- **Pregunta 7 (A5):** "¿finge?" puede leerse como "miente"; "simular" o "hacer como si" es lo que usan las traducciones chilenas.
- **Pregunta 3 (A1):** el ejemplo actual usa un nombre propio ("Juan"); se cambia por uno neutro.

---

## 4. Bloque 3: salud y desarrollo (preguntas 13 a 19)

No entran al modelo. Se usan en las **reglas clínicas** (pueden subir el nivel de riesgo) y en los **perfiles** (pesos validados por especialistas).

**Por qué se reformulan:** el texto actual pide al padre algo que no puede saber o que no aplica a un niño pequeño (por ejemplo, síntomas de depresión o dificultades en lectura y matemáticas en un niño de 2 años). Se pregunta por un **diagnóstico ya recibido** o por una **conducta observada**.

**Opciones:** Sí · No · No sé. Se guardan como `yes`, `no`, `unknown`. "No sé" **nunca** se trata como "No": no activa reglas, cuenta 0 en el perfil y se registra en `unanswered_comorbidities` para que el agente lo mencione.

| # | Variable | Uso | Texto actual | Texto propuesto | Ejemplo propuesto |
|---|---|---|---|---|---|
| 13 | `c_speech` | Reglas; perfil comunicación (25 %) | ¿Su hijo/a tiene dificultades para hablar o expresar ideas claramente? | ¿Algún profesional le ha dicho que su hijo/a tiene retraso del habla o del lenguaje, o usted nota que habla mucho menos que otros niños de su edad? | Usa muy pocas palabras para su edad o no forma frases |
| 14 | `c_learning` | Reglas; perfil comunicación (15 %) | ¿Su hijo/a tiene dificultades para aprender? | ¿Ha notado que a su hijo/a le cuesta más que a otros niños de su edad aprender cosas nuevas? | Juegos, rutinas o palabras nuevas |
| 15 | `c_genetic` | Reglas | ¿Su hijo/a tiene algún trastorno genético? | ¿Su hijo/a tiene un diagnóstico médico de una condición genética? | Síndrome de Down o síndrome de X frágil |
| 16 | `c_depression` | Reglas | ¿Su hijo/a presenta síntomas de depresión? | En las últimas semanas, ¿ha notado que su hijo/a está casi siempre triste, sin ganas de jugar o sin interés en lo que antes le gustaba? | — |
| 17 | `c_developmental_delay` | Reglas | ¿Ha notado un retraso en el desarrollo de su hijo/a? | ¿Algún profesional le ha dicho que su hijo/a tiene retraso en su desarrollo, o se sentó, caminó o habló más tarde que otros niños? | — |
| 18 | `c_social_behavior` | Reglas; perfil social (20 %) | ¿Su hijo/a tiene problemas de comportamiento o sociales? | ¿Ha notado que su hijo/a tiene rabietas muy frecuentes o muy intensas, o que casi nunca juega con otros niños? | — |
| 19 | `c_anxiety` | Reglas; perfil social (5 %) | ¿Su hijo/a muestra señales de ansiedad? | ¿Ha notado que su hijo/a se asusta o se angustia mucho ante cambios, ruidos o lugares nuevos? | — |

---

## 5. Bloque 4: familia (pregunta 20)

| Campo | Valor |
|---|---|
| Texto actual | ¿Alguien en su familia cercana ha sido diagnosticado con autismo? (ejemplo: "…o tiene comportamientos relacionados") |
| Texto propuesto | ¿Alguien de la familia del niño o niña tiene un **diagnóstico** de autismo? |
| Opciones | Sí, su padre, madre o un hermano/a · Sí, otro familiar · No · No sé |
| Se guarda como | `family_history`: `first_degree`, `other`, `no` o `unknown` |
| Uso | Regla clínica (por ejemplo, R01 con familia directa). No se identifica a la persona |
| Cambio | Se quita "o tiene comportamientos relacionados": la regla clínica se basa en un diagnóstico, no en una sospecha |

---

## 6. Bloque 5: regresión (pregunta 21, nueva)

| Campo | Valor |
|---|---|
| Texto | ¿Su hijo/a dejó de hacer, durante varias semanas, cosas que ya hacía, como decir palabras, señalar, saludar o responder a su nombre? |
| Opciones | Sí · No · No sé |
| Se guarda como | `regression`: `yes`, `no` o `unknown` |
| Uso | No entra al modelo. Regla clínica **R05**: un "Sí" sube el nivel y recomienda una evaluación pronta, sin importar el puntaje. **Cuánto sube** (un nivel o directo a Prioritario) lo definen los especialistas |

**Por qué se agrega:**

- La pérdida de lenguaje o de habilidades sociales a cualquier edad es un signo de alarma que justifica derivar a evaluación (guía de la Academia Americana de Pediatría, Hyman y otros, 2020).
- Ocurre en cerca de 1 de cada 3 niños con autismo, sobre todo entre los 15 y los 24 meses (metaanálisis de Barger, Campbell y McDonough, 2013).
- También puede indicar otras condiciones que requieren atención médica pronta (por ejemplo, síndrome de Rett o síndrome de Landau-Kleffner).
- El Q-CHAT-10 no lo pregunta: mide cómo está el niño hoy, no si perdió algo.

**Limitaciones:** la memoria de los padres sobre pérdidas no es exacta, así que un "No" no descarta nada. "Durante varias semanas" evita contar como regresión pausas normales (enfermedad, cambios en casa o aprender dos idiomas).

---

## 7. Datos que se envían al backend

`POST /assessments` (ver `consideraciones_app_tamizaje.md`, sección 3.2):

```json
{
  "schema_version": "2.1",
  "consent_id": "uuid",
  "child": { "age_years": 2, "sex": "M" },
  "qchat10": {
    "A1": 0, "A2": 1, "A3": 2, "A4": 3, "A5": 1,
    "A6": 0, "A7": 2, "A8": 4, "A9": 1, "A10": 4
  },
  "comorbidities": {
    "speech": "yes", "learning": "no", "genetic": "unknown",
    "depression": "no", "developmental_delay": "yes",
    "social_behavior": "no", "anxiety": "no"
  },
  "family_history": "other",
  "regression": "no"
}
```

- `age_years`: 0 a 13. Con 0 no se hace la prueba (el frontend no envía el formulario).
- `qchat10.*`: índice de la opción elegida (0 a 4). El backend calcula los binarios con la regla oficial.
- `comorbidities.*`: `yes`, `no` o `unknown`.
- `family_history`: `first_degree`, `other`, `no` o `unknown`.
- `regression`: `yes`, `no` o `unknown`.
- El backend calcula `age_validity` a partir de `age_years` (sección 2).

---

## 8. Hoja de validación para especialistas

Para cada pregunta: aprobar, aprobar con cambios o rechazar, con comentarios. Las preguntas 3 a 12 solo se revisan para confirmar que la traducción es fiel al original.

| # | Tema | ¿Qué deben revisar? | Aprobado | Con cambios | Rechazado | Comentarios |
|---|---|---|---|---|---|---|
| 1 | Edad | Avisos por edad y **tope clínico de confianza** (propuesta: 5 años, con aviso después) | ☐ | ☐ | ☐ | |
| 2 | Sexo | Redacción | ☐ | ☐ | ☐ | |
| 3 | A1 Responde a su nombre | Fidelidad al original y ejemplo | ☐ | ☐ | ☐ | |
| 4 | A2 Contacto visual | Fidelidad y ejemplo | ☐ | ☐ | ☐ | |
| 5 | A3 Señala para pedir | Fidelidad y ejemplo | ☐ | ☐ | ☐ | |
| 6 | A4 Señala para compartir | Fidelidad y ejemplo | ☐ | ☐ | ☐ | |
| 7 | A5 Juego de simular | **"Simular" en lugar de "fingir"** | ☐ | ☐ | ☐ | |
| 8 | A6 Sigue la mirada | Fidelidad y ejemplo | ☐ | ☐ | ☐ | |
| 9 | A7 Consuela | **Se agrega la condición del original** | ☐ | ☐ | ☐ | |
| 10 | A8 Primeras palabras | Fidelidad y opciones | ☐ | ☐ | ☐ | |
| 11 | A9 Gestos simples | **Se quita "señala lo que quiere" del ejemplo** | ☐ | ☐ | ☐ | |
| 12 | A10 Mirada perdida | Fidelidad y ejemplo | ☐ | ☐ | ☐ | |
| 13 | Habla y lenguaje | Redacción nueva y "No sé" | ☐ | ☐ | ☐ | |
| 14 | Aprendizaje | Redacción nueva, adecuada a niños pequeños | ☐ | ☐ | ☐ | |
| 15 | Condición genética | Redacción y ejemplos | ☐ | ☐ | ☐ | |
| 16 | Ánimo (depresión) | ¿Tiene sentido a esta edad? ¿Mantener, cambiar o quitar? | ☐ | ☐ | ☐ | |
| 17 | Retraso del desarrollo | Redacción nueva | ☐ | ☐ | ☐ | |
| 18 | Conducta y juego social | Redacción nueva | ☐ | ☐ | ☐ | |
| 19 | Ansiedad | Redacción nueva | ☐ | ☐ | ☐ | |
| 20 | Antecedente familiar | Opciones (familia directa / otro familiar / no / no sé) | ☐ | ☐ | ☐ | |
| 21 | Regresión (nueva) | Redacción y **cuánto sube el nivel** con un "Sí" (un nivel o Prioritario) | ☐ | ☐ | ☐ | |
| — | Avisos por edad (sección 2) | Textos que ve el padre | ☐ | ☐ | ☐ | |

**Preguntas abiertas para los especialistas:**

1. ~~¿Confirman 5 años como tope clínico de confianza?~~ **Decidido: sí**, con aviso después de los 5 años.
2. ~~¿La pregunta 16 (ánimo) aporta algo en niños de 1 a 3 años?~~ **Decidido: se mantiene.**
3. ~~¿Se agrega una pregunta sobre regresión?~~ **Decidido: sí**, como pregunta 21. Falta que los especialistas definan cuánto sube el nivel (regla R05).
4. ~~¿Las redacciones de las preguntas 13 a 19 cambian los pesos de los perfiles?~~ **Decidido: los pesos se mantienen.**

---

## 9. Pendientes fuera de esta tarea

El diseño del formulario está cerrado. Lo que falta depende de otras personas o de otras etapas:

| Pendiente | Dónde se sigue |
|---|---|
| Autorización del Autism Research Centre para usar el Q-CHAT-10 en Conecta | Tarea "Cumplir el mínimo legal de privacidad para el piloto" (permisos antes del piloto) |
| Revisión de los especialistas (sección 8) | Tarea "Validar reglas clínicas con especialistas": formulario y reglas se revisan en la misma sesión |
| Construir el formulario en Conecta (Next.js, ruta `/screening/questions`) y su validación en `POST /assessments` | Desarrollo de Conecta. Es un proyecto nuevo: TEAnimo solo sirvió de referencia, no se modifica su código |
| Prueba con 5 a 10 padres en celular (comprensión y tiempo) | Cuando el formulario esté construido en Conecta |

**Fuentes:** Allison C. et al. (2012), *Toward brief "Red Flags" for autism screening: the Short Autism Spectrum Quotient and the Short Quantitative Checklist in 1,000 cases and 3,000 controls*, J Am Acad Child Adolesc Psychiatry · [Autism Research Centre: Q-CHAT-10](https://www.autismresearchcentre.com/tests/quantitative-checklist-for-autism-in-toddlers-10-items-q-chat-10/) · [Q-CHAT en Chile (estudio psicométrico)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11215167/)
