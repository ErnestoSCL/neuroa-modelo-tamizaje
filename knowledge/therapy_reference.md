# Referencia de terapias

Guía para que el agente **reconozca** qué terapias del catálogo de los centros encajan con cada caso, leyendo el nombre y la descripción que escribe cada centro (herramienta `search_therapies`). **No es un catálogo**: las terapias que se recomiendan salen siempre del catálogo de los centros afiliados.

**Reglas:**

- El agente marca **todas** las terapias del catálogo que encajan; el backend decide el orden de los centros.
- Explica cada terapia por la **necesidad** del niño ("para fortalecer su comunicación"), no por el diagnóstico.
- Nunca promete resultados ("con esta terapia hablará"); dice para qué sirve.
- Con nivel **Alto o Prioritario**, la primera recomendación es siempre la **evaluación profesional**; las terapias van en paralelo, no en su lugar.

---

## Tipos de terapia

| Tipo | Para qué sirve (texto para el padre) | Cuándo encaja | Palabras que suele usar el centro |
|---|---|---|---|
| **Terapia de lenguaje** | Ayuda a desarrollar la comunicación: entender, hablar, usar gestos y comunicarse con otras personas | Perfil de comunicación; pregunta 13 = Sí; preguntas 5, 10 u 11 con señales | lenguaje, habla, comunicación, fonoaudiología, terapia del lenguaje |
| **Terapia ocupacional** | Ayuda en la coordinación, el juego, las actividades del día a día (comer, vestirse) y en cómo reacciona a sonidos, texturas o luces | Retraso del desarrollo (17); sensibilidad a ruidos o cambios (19) | ocupacional, integración sensorial, motricidad, psicomotricidad |
| **Intervención temprana / estimulación temprana** | Acompaña el desarrollo general del niño pequeño con actividades de juego guiadas | Niños de 1 a 3 años; retraso del desarrollo; cualquier perfil en niños pequeños | estimulación temprana, intervención temprana, desarrollo infantil |
| **Intervenciones en habilidades sociales y juego** | Ayuda a compartir, mirar, jugar con otros y entender a los demás | Perfil social | habilidades sociales, juego, interacción, terapia de juego |
| **Intervenciones conductuales o del desarrollo basadas en evidencia** | Programas estructurados que enseñan habilidades de comunicación, juego y vida diaria, con participación de la familia | Perfil social o mixto; nivel Moderado o más | ABA, análisis conductual, modelo Denver (ESDM), intervención naturalista, TEACCH |
| **Psicología infantil y orientación a padres** | Apoya el manejo de emociones, rabietas y miedos, y orienta a la familia | Preguntas 16, 18 o 19 con señales | psicología infantil, orientación familiar, escuela de padres, conducta |
| **Evaluación diagnóstica o interdisciplinaria** | Un equipo de profesionales evalúa el desarrollo para saber si hay autismo u otra condición, y qué apoyo necesita | Nivel Alto o Prioritario; perfil mixto | evaluación, diagnóstico, neuropediatría, equipo interdisciplinario, ADOS |

---

## Nunca recomendar [texto fijo]

El agente **nunca** recomienda ni menciona como opción, aunque un centro las ofrezca:

- Dietas como tratamiento del autismo (sin gluten, sin caseína u otras).
- Suplementos, vitaminas en dosis altas o "desintoxicación".
- Quelación de metales.
- Dióxido de cloro (MMS o CDS).
- Oxígeno hiperbárico.
- Terapias con células madre.
- Homeopatía.
- Cualquier medicación (eso lo decide solo un médico).

Si el padre pregunta por alguna, el agente responde: "Esta opción no cuenta con evidencia científica de que ayude a los niños con autismo y algunas pueden ser peligrosas. Le recomendamos conversarlo con su pediatra antes de probar cualquier tratamiento."

Si la descripción de una terapia del catálogo incluye alguna de estas prácticas, el agente no la recomienda y el backend la reporta para revisión.
