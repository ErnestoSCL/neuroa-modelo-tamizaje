# Validación de la respuesta del agente

El backend revisa cada respuesta **antes** de mostrarla. Si falla, reintenta **una vez** con el mismo contexto más el motivo del error; si vuelve a fallar o pasan más de 15 segundos, usa el texto de respaldo (`fallback.md`). El resultado del modelo y de las reglas se muestra siempre, con o sin agente.

## Controles automáticos

| # | Control | Falla si… |
|---|---|---|
| V1 | Formato | El JSON no cumple `output_schema.json` |
| V2 | Longitud | `summary` supera 120 palabras o `profile_explanation` supera 80 |
| V3 | Frases prohibidas | Aparece alguna expresión de la lista de `knowledge/notices.md` (sin distinguir mayúsculas ni tildes) |
| V4 | Números | Aparece un porcentaje, una probabilidad o un puntaje (`%`, "por ciento", "probabilidad de", "puntaje", "puntos") |
| V5 | Terapias reales | Algún `therapy_id` no está entre los devueltos por `search_therapies` en esta evaluación |
| V6 | Herramienta usada | Hay terapias sugeridas sin que se haya llamado a `search_therapies` |
| V7 | Coherencia | `no_matching_therapies` es `true` y hay terapias, o es `false` y la lista está vacía |
| V8 | Terapias prohibidas | Una terapia sugerida menciona en su nombre o descripción una práctica de la lista "Nunca recomendar" (dieta, quelación, dióxido de cloro, MMS, CDS, hiperbárica, células madre, homeopatía, suplementos) |
| V9 | Datos personales | Aparece un correo, un teléfono o un DNI |
| V10 | Opciones públicas | `next_steps` no menciona el sistema público (CRED, establecimiento de salud, MINSA o EsSalud) |

## Red de seguridad clínica (después de validar)

Con nivel **Alto o Prioritario**, si la respuesta válida no incluye ninguna terapia de evaluación (nombre o descripción con "evaluación", "diagnóstico", "neuropediatría" o "interdisciplinaria") y la herramienta devolvió alguna, **el backend la agrega primera**, con el motivo fijo: "Para conocer cómo va su desarrollo con una evaluación profesional." Así, la recomendación clínica más importante no depende del modelo de IA.

## Registro

Por cada evaluación se guarda en `app.explanations`: `source` (`llm` o `template`), `prompt_version`, `knowledge_version`, los controles que fallaron y si hubo reintento. Nunca se guardan datos personales en los registros del proveedor.

## Alertas

- Si más del 5 % de las respuestas de un día usa el texto de respaldo, se alerta al equipo.
- Cualquier fallo de V3, V5, V8 o V9 se registra para revisión humana, aunque el reintento lo corrija.
