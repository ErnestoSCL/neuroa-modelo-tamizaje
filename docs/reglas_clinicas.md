# Reglas clínicas de Conecta (capa 2)

Cómo se pasa de la probabilidad del modelo y las respuestas del formulario al **nivel de riesgo** y las **recomendaciones** que ve el padre. Complementa `formulario_tamizaje.md` (las 21 preguntas) y `consideraciones_app_tamizaje.md` (sección 5).

Versión 1.0 · 2026-10-08 · Estado: **reglas aprobadas por el equipo; pendientes de validación por especialistas**

---

## 1. Principios

1. **Deterministas y versionadas.** Viven en un archivo de configuración (`rules_version`, por ejemplo `rules-2026.1`) con un test por regla.
2. **Nunca cambian la probabilidad del modelo.** La app muestra el nivel final y, aparte, "nivel ajustado por: …".
3. **Solo suben el nivel**, nunca lo bajan.
4. **Dos tipos de reglas:**
   - **De nivel:** suben el nivel de riesgo.
   - **De recomendación:** no cambian el nivel; agregan un consejo al resultado.
5. **No se acumulan.** Si se activan varias reglas de nivel, el nivel final es **el más alto que indique cualquiera de ellas**, no la suma.
6. **"Subir un nivel" llega como máximo a Alto.** **Prioritario** solo se alcanza con las señales de alarma fuertes (R02 y R05).
7. **Las recomendaciones sí se acumulan**, porque no cambian el nivel.
8. **"No sé" nunca cuenta como "No"** ni como "Sí": no activa reglas de nivel, pero en las preguntas clave genera una recomendación (R09).

---

## 2. Nivel base (del modelo)

El modelo da una probabilidad calibrada a partir de las 10 preguntas del Q-CHAT-10. **Propuesta de cortes [a validar con especialistas]:**

| Nivel base | Probabilidad del modelo | Equivale aprox. a (puntaje Q-CHAT-10) | Niños en la muestra clínica polaca (n = 252) | Con TEA confirmado |
|---|---|---|---|---|
| **Bajo** | menor que 0.20 | 0 a 1 | 82 | 4 (4.9 %) |
| **Moderado** | 0.20 a 0.50 | 2 a 3 | 49 | 21 (42.9 %) |
| **Alto** | 0.50 o más | 3 a 10 | 121 | 110 (90.9 %) |
| **Prioritario** | Solo por reglas (R02, R05) | — | — | — |

**Cómo se eligieron:**

- **Bajo < 0.20:** el 97 % de los niños con TEA de la muestra queda en Moderado o más (sensibilidad 0.97). Se prioriza no dejar pasar casos.
- **Alto ≥ 0.50:** coincide casi exactamente con la regla oficial del Q-CHAT-10 (puntaje de 4 o más), que es el estándar internacional.
- **El umbral del modelo (0.3251, en `metadata.json`) cae dentro de Moderado.** En la app el resultado se comunica por niveles, no como "positivo/negativo"; Moderado ya recomienda una evaluación profesional.

**Limitación:** la muestra polaca tiene 54 % de niños con TEA; en la población general hay muchos menos. Por eso, en la práctica, Bajo es aún más tranquilizador y Alto tiene más falsos positivos que en esta tabla. Hay que revisar los cortes con la validación local en el Perú.

---

## 3. Reglas

| Regla | Se activa si… | Efecto | Tipo | Fundamento |
|---|---|---|---|---|
| **R01** Familia directa | Pregunta 20 = padre, madre o hermano/a con diagnóstico de autismo | **Sube un nivel** (máximo Alto). Recomienda vigilar el desarrollo y repetir la prueba en 6 meses | Nivel | Los hermanos de un niño con TEA tienen cerca de 20 % de probabilidad de tenerlo (Ozonoff y otros, 2011) |
| **R02** Habla + desarrollo | Pregunta 13 = Sí **y** pregunta 17 = Sí | **Prioritario.** Recomienda una evaluación del desarrollo pronto | Nivel | La combinación justifica evaluación sin importar el tamizaje (Hyman y otros, 2020) |
| **R03** Condición genética | Pregunta 15 = Sí | **Sube un nivel** (máximo Alto). Sugiere seguimiento con genética o neuropediatría | Nivel | Varios síndromes genéticos (X frágil, esclerosis tuberosa, Down, entre otros) tienen una frecuencia de TEA muy superior a la población (Richards y otros, 2015) |
| **R04** Edad | `age_validity` distinto de `validated` (1 año, o 3 años o más) | No cambia el nivel; muestra el aviso por edad (`formulario_tamizaje.md`, sección 2) | Recomendación | Rango de validación del Q-CHAT-10: 18 a 36 meses (Allison y otros, 2012) |
| **R05** Regresión | Pregunta 21 = Sí | **Prioritario** (propuesta). Recomienda una evaluación pronto | Nivel | La pérdida de habilidades a cualquier edad es signo de alarma (Hyman y otros, 2020); ocurre en cerca de 1 de cada 3 niños con TEA (Barger y otros, 2013) |
| **R06** Desarrollo solo | Pregunta 17 = Sí **y** pregunta 13 ≠ Sí | **Sube un nivel** (máximo Alto). Recomienda una evaluación del desarrollo | Nivel | Un retraso del desarrollo justifica evaluación por sí solo (Hyman y otros, 2020) |
| **R07** Ánimo | Pregunta 16 = Sí | Recomienda: "Le recomendamos conversar con su pediatra sobre el estado de ánimo de su hijo/a" | Recomendación | No indica TEA, pero una tristeza persistente en un niño pequeño merece consulta |
| **R08** Otro familiar | Pregunta 20 = otro familiar con diagnóstico de autismo | Recomienda: "Mencione este antecedente a su pediatra en el próximo control" | Recomendación | El riesgo aumenta poco con familiares no directos (primos, cerca de 2 veces la población; hermanos, cerca de 10 veces; Sandin y otros, 2014) |
| **R09** "No sé" | "No sé" en la pregunta 13, 15, 17 o 21 | Recomienda: "Si tiene dudas sobre [tema], consúltelo con su pediatra" | Recomendación | Son las preguntas que alimentan reglas de nivel |
| **R09b** Muchos "No sé" | 3 o más respuestas "No sé" en las preguntas 13 a 21 | Avisa: "Algunas respuestas quedaron sin confirmar; el resultado puede estar incompleto" | Recomendación | El resultado se apoya en información incompleta |

**Preguntas sin regla (a propósito):**

| Pregunta | Uso | Por qué no tiene regla |
|---|---|---|
| 14 Aprendizaje | Perfil de comunicación (15 %) y explicación del agente | En niños pequeños es una señal muy general |
| 18 Conducta | Perfil social (20 %) y explicación del agente | Las rabietas son comunes a esta edad; subir el nivel daría muchas falsas alarmas |
| 19 Ansiedad | Perfil social (5 %) y explicación del agente | Igual que la 18 |

Así, **cada una de las 21 preguntas tiene un uso**: modelo, regla de nivel, recomendación o perfil.

---

## 4. Cálculo paso a paso

1. El modelo da la probabilidad → **nivel base** (sección 2).
2. Se evalúan todas las reglas de nivel que se activan y cada una propone un nivel:
   - R02 y R05 → Prioritario.
   - R01, R03 y R06 → nivel base + 1, con máximo Alto.
3. **Nivel final** = el más alto entre el nivel base y los niveles que proponen las reglas.
4. Se agregan **todas** las recomendaciones activadas (R04, R07, R08, R09, R09b y las de las reglas de nivel).
5. Se guardan en `app.results`: `base_level`, `final_level`, `triggered_rules` y `rules_version`.

---

## 5. Casos de ejemplo

| Caso | Nivel base | Reglas activadas | Nivel final y recomendaciones |
|---|---|---|---|
| Hermano con autismo; resto normal | Moderado | R01 | **Alto** + vigilar y repetir la prueba |
| Retraso del desarrollo y ánimo bajo | Bajo | R06, R07 | **Moderado** + evaluación del desarrollo + hablar del ánimo con el pediatra |
| Retraso del habla y del desarrollo | Moderado | R02 | **Prioritario** + evaluación pronto |
| Rabietas frecuentes y miedos; resto normal | Bajo | Ninguna | **Bajo**; el agente lo menciona en el perfil social |
| "No sé" en regresión y en condición genética | Bajo | R09 | **Bajo** + consultar esas dudas con el pediatra |
| Condición genética y hermano con autismo | Bajo | R01, R03 | **Moderado** (no se acumulan) + seguimiento con genética |
| Perdió palabras que ya decía | Bajo | R05 | **Prioritario** + evaluación pronto |
| Niño de 4 años, puntaje alto | Alto | R04 | **Alto** + aviso de menor precisión por edad |

Estos casos sirven también como **tests** de las reglas y como parte del set de pruebas del agente.

---

## 6. Hoja de validación para especialistas

| Ítem | Qué revisar | Aprobado | Con cambios | Rechazado | Comentarios |
|---|---|---|---|---|---|
| Cortes del nivel base | Bajo < 0.20; Moderado 0.20–0.50; Alto ≥ 0.50 | ☐ | ☐ | ☐ | |
| Principio de no acumulación | Nivel final = el más alto, no la suma | ☐ | ☐ | ☐ | |
| R01 Familia directa | Sube un nivel (máximo Alto) | ☐ | ☐ | ☐ | |
| R02 Habla + desarrollo | Prioritario | ☐ | ☐ | ☐ | |
| R03 Condición genética | Sube un nivel (máximo Alto) | ☐ | ☐ | ☐ | |
| R04 Edad | Solo aviso | ☐ | ☐ | ☐ | |
| R05 Regresión | **Prioritario o un nivel** | ☐ | ☐ | ☐ | |
| R06 Desarrollo solo | Sube un nivel (máximo Alto) | ☐ | ☐ | ☐ | |
| R07 Ánimo | Solo recomendación | ☐ | ☐ | ☐ | |
| R08 Otro familiar | Solo recomendación | ☐ | ☐ | ☐ | |
| R09 / R09b "No sé" | Recomendaciones | ☐ | ☐ | ☐ | |
| 14, 18 y 19 sin regla | Solo perfiles y agente | ☐ | ☐ | ☐ | |

---

## 7. Pendientes

- Validación de los especialistas, en la misma sesión que el formulario.
- Verificar las citas con los artículos originales antes de publicarlas en la app.
- Textos que ve el padre para cada nivel (qué significa y qué hacer): parte de la base de conocimiento del agente.
- Revisar los cortes y las reglas con los datos de la validación local en el Perú.

**Referencias:**

- Allison C, Auyeung B, Baron-Cohen S (2012). Toward brief "red flags" for autism screening. *J Am Acad Child Adolesc Psychiatry*, 51(2), 202–212.
- Barger BD, Campbell JM, McDonough JD (2013). Prevalence and onset of regression within autism spectrum disorders: a meta-analytic review. *J Autism Dev Disord*, 43(4), 817–828.
- Hyman SL, Levy SE, Myers SM (2020). Identification, evaluation, and management of children with autism spectrum disorder. *Pediatrics*, 145(1), e20193447.
- Ozonoff S y otros (2011). Recurrence risk for autism spectrum disorders: a Baby Siblings Research Consortium study. *Pediatrics*, 128(3), e488–e495.
- Richards C y otros (2015). Prevalence of autism spectrum disorder phenomenology in genetic disorders: a systematic review and meta-analysis. *Lancet Psychiatry*, 2(10), 909–916.
- Sandin S y otros (2014). The familial risk of autism. *JAMA*, 311(17), 1770–1777.
