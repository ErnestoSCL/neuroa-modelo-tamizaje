# Textos de las reglas clínicas

Cada regla activada (`docs/reglas_clinicas.md`) agrega su texto al resultado. Los textos marcados **[texto fijo]** se muestran tal cual, tanto en el resultado del agente como en los textos de respaldo.

| Regla | Cuándo | Texto para el padre [texto fijo] |
|---|---|---|
| **R01** Familia directa | Padre, madre o hermano/a con diagnóstico de autismo | "Como un familiar directo tiene diagnóstico de autismo, le recomendamos vigilar de cerca el desarrollo de su hijo/a y repetir esta prueba en unos 6 meses. Cuénteselo a su pediatra en cada control." |
| **R02** Habla + desarrollo | Retraso del habla y del desarrollo | "Usted mencionó señales en el habla y en el desarrollo. Los profesionales recomiendan revisar esto pronto, sin importar el resultado del cuestionario. Le sugerimos pedir una evaluación del desarrollo en los próximos días." |
| **R03** Condición genética | Diagnóstico de una condición genética | "Como su hijo/a tiene un diagnóstico genético, es importante que su desarrollo tenga un seguimiento cercano con su pediatra y, si aún no lo tiene, con genética o neuropediatría." |
| **R04** Edad | Fuera del rango validado | Aviso por edad (`age_messages.md`) |
| **R05** Regresión | Perdió habilidades que ya tenía | "Usted mencionó que su hijo/a dejó de hacer cosas que ya hacía. Los profesionales recomiendan revisar esto pronto. Le sugerimos pedir una cita con su pediatra en los próximos días y contarle qué dejó de hacer y desde cuándo." |
| **R06** Desarrollo solo | Retraso del desarrollo sin retraso del habla | "Usted mencionó señales de retraso en el desarrollo. Le recomendamos pedir una evaluación del desarrollo con su pediatra." |
| **R07** Ánimo | Tristeza o desinterés persistente | "Usted mencionó que su hijo/a ha estado casi siempre triste o sin ganas de jugar. Le recomendamos conversar con su pediatra sobre su estado de ánimo." |
| **R08** Otro familiar | Otro familiar con diagnóstico de autismo | "Mencione a su pediatra que hay un familiar con diagnóstico de autismo en el próximo control de su hijo/a." |
| **R09** "No sé" en una pregunta clave | 13 (habla), 15 (genética), 17 (desarrollo) o 21 (regresión) | "Si tiene dudas sobre [el habla / alguna condición genética / el desarrollo / si dejó de hacer cosas que ya hacía] de su hijo/a, consúltelo con su pediatra." |
| **R09b** Muchos "No sé" | 3 o más "No sé" en las preguntas 13 a 21 | "Algunas respuestas quedaron sin confirmar, así que este resultado puede estar incompleto. Si puede averiguar esa información, le recomendamos repetir la prueba." |

**Orden en pantalla:** primero las recomendaciones de reglas de nivel (R02, R05, R01, R03, R06) y luego las demás (R07, R08, R09, R09b, R04). Si se activan R02 y R05, se muestran las dos.
