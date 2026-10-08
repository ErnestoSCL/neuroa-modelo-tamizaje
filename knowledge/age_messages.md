# Mensajes según la edad

La edad se pide en años (0 a 13). El aviso de validez lo muestra la app ([texto fijo], `docs/formulario_tamizaje.md`, sección 2); el agente agrega un mensaje de enfoque según la edad.

| Edad | `age_validity` | Aviso de validez [texto fijo] | Enfoque del mensaje del agente |
|---|---|---|---|
| Menos de 1 año | `not_applicable` | "Este cuestionario es para niños desde el año y medio. Le recomendamos seguir los controles de crecimiento y desarrollo (CRED) de su hijo/a y volver cuando cumpla 1 año y 6 meses." | No hay prueba ni agente |
| 1 año | `check_age` | "Si su hijo/a tiene menos de 1 año y 6 meses, el resultado es solo orientativo. Le recomendamos repetir la prueba cuando cumpla 1 año y 6 meses y conversarlo con su pediatra." | Etapa de muchos cambios; repetir la prueba al año y medio |
| 2 años | `validated` | — | "Está en una muy buena etapa para apoyar su desarrollo: a esta edad el cerebro aprende muy rápido y la intervención temprana tiene los mejores resultados." |
| 3 a 5 años | `less_precise` | "Este cuestionario fue validado en niños pequeños; a la edad de su hijo/a el resultado es menos preciso. Si tiene dudas sobre su desarrollo, le recomendamos una evaluación profesional." | Nunca es tarde para apoyar su desarrollo; si hay dudas, no esperar para pedir una evaluación |
| 6 a 13 años | `beyond_clinical_cap` | "Esta prueba se aplica con confianza hasta los 5 años. Puede completarla, pero a la edad de su hijo/a el resultado es solo referencial. Le recomendamos una evaluación con un especialista." | El resultado es solo referencial; recomendar evaluación con un especialista; mencionar el colegio como fuente de información útil para el profesional |

**Regla:** en `less_precise` y `beyond_clinical_cap` el agente nunca transmite el nivel con más certeza de la que tiene; siempre recuerda que la evaluación profesional es el paso más confiable.
