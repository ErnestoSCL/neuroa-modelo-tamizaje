# Texto de respaldo (cuando el agente falla)

La app **siempre** entrega un resultado, aunque el agente no responda, exceda el tiempo o no pase la validación. El texto de respaldo se arma solo con textos fijos aprobados (`knowledge/`), sin personalización.

## Cómo se arma

| Parte | Con agente | Con texto de respaldo |
|---|---|---|
| Título del nivel | `knowledge/levels.md` | Igual |
| Resumen | `summary` del agente | "Qué significa" del nivel (`knowledge/levels.md`) |
| Perfil | Nombre + `profile_explanation` | Nombre + explicación del perfil (`knowledge/profiles.md`) |
| Recomendaciones de reglas | `knowledge/recommendations.md` | Igual |
| Próximos pasos | `next_steps` del agente | "Qué hacer" del nivel (`knowledge/levels.md`) |
| Terapias | Elegidas por el agente, con su motivo | Terapias del catálogo filtradas por edad, según el perfil (tabla de abajo), sin motivo personalizado |
| Avisos | `knowledge/notices.md` y `knowledge/age_messages.md` | Igual, más la nota de abajo |

**Nota adicional [texto fijo]:** "En este momento no pudimos preparar una explicación personalizada. Este resultado incluye la información principal; puede volver a consultarlo más tarde desde su cuenta."

## Terapias sin agente

El backend filtra el catálogo por edad y busca en el nombre y la descripción estas palabras, según el perfil:

| Perfil | Palabras clave |
|---|---|
| Comunicación | lenguaje, habla, comunicación, fonoaudiología |
| Interacción social | habilidades sociales, juego, interacción, ABA, Denver |
| Mixto o sin área predominante | evaluación, interdisciplinario, estimulación temprana |
| Siempre con nivel Alto o Prioritario | evaluación, diagnóstico, neuropediatría |

Se excluyen las terapias cuya descripción contenga prácticas de la lista "Nunca recomendar". Se muestran como máximo 6, con el orden habitual de la app (cercanía y rotación diaria).

## Reintento posterior

Si el agente falló por tiempo o por un error del proveedor, un job vuelve a intentarlo en segundo plano. Si funciona, la explicación personalizada aparece la próxima vez que el padre abra su resultado.
