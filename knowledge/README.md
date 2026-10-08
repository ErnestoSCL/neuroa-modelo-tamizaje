# Base de conocimiento del agente de Conecta

Textos curados que el agente IA recibe **completos** en cada evaluación (sin búsqueda, sin RAG). No le enseñan medicina: fijan **qué debe decir y cómo**, con definiciones y tono aprobados por el equipo clínico, para que no improvise. La app también los usa directamente cuando el agente falla (textos de respaldo).

Versión `kb-2026.1` · 2026-10-08 · Estado: **borrador; pendiente de aprobación por especialistas**

| Archivo | Contenido |
|---|---|
| `levels.md` | Qué significa cada nivel (Bajo, Moderado, Alto, Prioritario) y qué hacer |
| `profiles.md` | Perfiles comunicativo, social y mixto: cómo explicarlos |
| `recommendations.md` | Textos de cada regla clínica (R01 a R09) |
| `questions.md` | Cómo mencionar cada respuesta del formulario (preguntas 13 a 21) sin diagnosticar |
| `age_messages.md` | Mensajes según la edad del niño o niña |
| `therapy_reference.md` | Para qué sirve cada tipo de terapia y qué terapias no recomendar nunca |
| `notices.md` | Avisos obligatorios, frases prohibidas, estilo y mensaje de emergencia |
| `version.json` | Versión de la base; se guarda en cada evaluación (`knowledge_version`) |

## Reglas de uso

1. El agente **solo explica**: no cambia el nivel, la probabilidad ni el perfil, que vienen del modelo y de las reglas clínicas (`docs/reglas_clinicas.md`).
2. Los textos marcados como **[texto fijo]** se muestran tal cual; el agente no los reescribe.
3. El resto son **guías de contenido**: el agente puede adaptar la redacción al caso, pero sin salir de lo que dicen.
4. Todo en español del Perú, trato de **usted**, lenguaje simple (frases cortas, sin tecnicismos), tono cálido, sin alarmismo ni falsa tranquilidad.
5. Cualquier cambio en estos archivos sube la versión en `version.json` y requiere aprobación de un especialista.

## Cómo se arma la llamada al agente

```
[Instrucciones fijas del agente: rol, reglas, formato de salida]
[Esta base de conocimiento completa]              ← igual en todas las evaluaciones (se cachea)
[Datos de ESTA evaluación: nivel, perfil, reglas activadas, edad, respuestas]
```
