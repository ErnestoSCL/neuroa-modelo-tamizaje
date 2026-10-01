# Consideraciones para construir la app de tamizaje de TEA

**Solución 1: Plataforma de tamizaje**
Dirigido a: equipo de desarrollo y fundador(a).
Estado: documento vivo. Los puntos marcados como **[a validar con especialistas]** o **[a validar con asesoría legal]** no deben implementarse como definitivos sin esa revisión.

---

## 1. Resumen y alcance

### Qué es

Una aplicación web (mobile first) en la que madres, padres o tutores responden gratis un cuestionario sobre el desarrollo de su hijo/a. La app:

1. Estima la probabilidad de rasgos compatibles con TEA con un modelo de ML entrenado sobre el Q-CHAT-10.
2. Ajusta el **nivel** de prioridad con reglas clínicas explícitas (comorbilidades, antecedentes familiares).
3. Explica el resultado en lenguaje sencillo, sugiere tipos de terapia y conecta a la familia con centros aliados.

### Qué NO es

- **No es un diagnóstico.** El TEA lo diagnostica un profesional (neuropediatra, psiquiatra infantil, psicólogo clínico) con evaluación presencial e instrumentos como ADOS-2 / ADI-R y criterios DSM-5.
- No reemplaza la evaluación del desarrollo en el control de niño sano.
- No recomienda medicación ni tratamientos específicos para un niño concreto; solo sugiere **tipos** de terapia a explorar con un profesional.
- No es un instrumento validado para toda la infancia: el Q-CHAT-10 está validado para aproximadamente **18 a 36 meses**.

Toda pantalla de resultados, PDF y correo debe dejar esto claro (ver sección 8).

---

## 2. Formulario y preguntas

### 2.1 Estado actual

El formulario (`components/form-comp/questions.js` en el frontend compilado) tiene 20 preguntas:

- **id1**: edad en años (input 1–18).
- **id2**: sexo (Masculino/Femenino).
- **id3–id12**: los 10 ítems del Q-CHAT-10 (A1–A10) en el orden oficial, 5 opciones cada uno.
- **id13–id19**: 7 preguntas Sí/No de comorbilidades.
- **id20**: antecedente familiar de autismo.

Puntuación actual (`Forms.jsx`, `calculateScore`): ítems 1–9 suman 1 si la opción elegida tiene índice ≥ 2; el ítem 10 ("mira fijamente a la nada") suma 1 si el índice es ≤ 2. Esto coincide con la regla oficial del Q-CHAT-10 y debe mantenerse.

### 2.2 Tabla de mapeo pregunta → variable → uso

| id | Pregunta (resumen) | Variable | Modelo (capa 1) | Reglas (capa 2) | Agente (capa 3) | Perfiles |
|---|---|---|---|---|---|---|
| 1 | Edad | `edad_meses` | **No.** Se evaluó en el notebook v2 y no mejora el AUC clínico (0.9037 sin edad frente a 0.9038 con edad) | Aviso de validez fuera de 18–36 m | Sí (mensaje por edad) | No |
| 2 | Sexo | `sexo` | **No** | No | Sí (solo contexto, sin sesgar) | No |
| 3 | Responde a su nombre | `A1` | Sí | No | Sí | Social (10 %) |
| 4 | Contacto visual | `A2` | Sí | No | Sí | Social (10 %) |
| 5 | Señala para pedir | `A3` | Sí | No | Sí | Comunicación (20 %) |
| 6 | Señala para compartir interés | `A4` | Sí | No | Sí | Social (10 %) |
| 7 | Juego simbólico / finge | `A5` | Sí | No | Sí | Social (15 %) |
| 8 | Sigue la mirada | `A6` | Sí | No | Sí | Social (15 %) |
| 9 | Consuela | `A7` | Sí | No | Sí | Social (15 %) |
| 10 | Primeras palabras | `A8` | Sí | No | Sí | Comunicación (20 %) |
| 11 | Gestos simples | `A9` | Sí | No | Sí | Comunicación (20 %) |
| 12 | Mira fijamente a la nada | `A10` | Sí | No | Sí | Ninguno |
| 13 | Dificultad del habla/lenguaje | `c_habla` | **No** | Sí | Sí | Comunicación (25 %) |
| 14 | Dificultad de aprendizaje | `c_aprendizaje` | **No** | Sí | Sí | Comunicación (15 %) |
| 15 | Trastorno genético | `c_genetico` | **No** | Sí | Sí | No |
| 16 | Síntomas de depresión | `c_depresion` | **No** | Sí | Sí | No |
| 17 | Retraso del desarrollo | `c_retraso_desarrollo` | **No** | Sí | Sí | No |
| 18 | Problemas sociales/conducta | `c_social_conducta` | **No** | Sí | Sí | Social (20 %) |
| 19 | Ansiedad | `c_ansiedad` | **No** | Sí | Sí | Social (5 %) |
| 20 | Familiar con autismo | `antecedente_familiar` | **No** | Sí | Sí | No |

Guardar **la respuesta cruda (índice 0–4)** de cada ítem además del valor binario. Hoy la tabla `evaluaciones` solo guarda `a1..a10` binarizados (`app/db/models.py:17-26`), lo que impide reentrenar con la escala completa o cambiar el punto de corte en el futuro.

### 2.3 Edad en meses

- Preguntar **fecha de nacimiento** (preferido) o **años + meses**. Calcular `edad_meses` en el backend, no en el cliente.
- Rango aceptado sugerido: 12–216 meses (1–18 años) para no excluir a nadie, pero:
  - **18–36 meses**: resultado normal del Q-CHAT-10.
  - **< 18 meses**: aviso "el cuestionario está pensado para niños desde los 18 meses; el resultado es orientativo. Repita la prueba a los 18 meses y consulte a su pediatra".
  - **> 36 meses**: aviso "este cuestionario fue validado en niños pequeños; en su hijo/a el resultado es menos preciso. Le recomendamos una evaluación profesional". El nivel mostrado debe reflejar esta menor confianza.
- **Recomendación a evaluar con especialistas [a validar con especialistas]**: incorporar instrumentos según edad en fases futuras:
  - M-CHAT-R/F (16–30 meses; requiere entrevista de seguimiento para puntajes intermedios).
  - AQ-10 versión niño (4–11 años) y adolescente (12–15 años).
  - Verificar licencias y existencia de versiones validadas en español antes de usarlos.

### 2.4 Redacción de las preguntas de comorbilidad

Los padres no pueden autodiagnosticar un trastorno genético o una depresión en un niño de 2 años. Reformular como **diagnóstico ya recibido** o **conducta observada**:

| id | Redacción actual | Redacción propuesta [a validar con especialistas] |
|---|---|---|
| 13 | ¿Tiene dificultades para hablar o expresar ideas? | ¿Algún profesional le ha dicho que su hijo/a tiene retraso del habla o del lenguaje? / ¿Ha notado que habla mucho menos que otros niños de su edad? |
| 14 | ¿Tiene dificultades para aprender? | ¿Ha notado que le cuesta más que a otros niños aprender cosas nuevas (juegos, rutinas, palabras)? |
| 15 | ¿Tiene algún trastorno genético? | ¿Su hijo/a tiene un diagnóstico médico de una condición genética (por ejemplo, síndrome de Down, X frágil)? Opciones: Sí / No / No sé |
| 16 | ¿Presenta síntomas de depresión? | ¿Ha notado que en las últimas semanas está casi siempre triste, sin ganas de jugar o sin interés en lo que antes le gustaba? |
| 17 | ¿Ha notado un retraso en el desarrollo? | ¿Algún profesional le ha dicho que tiene retraso en su desarrollo? / ¿Se sentó, caminó o habló más tarde que otros niños? |
| 18 | ¿Tiene problemas de comportamiento o sociales? | ¿Ha notado que tiene rabietas muy frecuentes o intensas, o que casi nunca juega con otros niños? |
| 19 | ¿Muestra señales de ansiedad? | ¿Ha notado que se asusta o angustia mucho ante cambios, ruidos o lugares nuevos? |
| 20 | ¿Alguien en su familia ha sido diagnosticado con autismo? | ¿Algún hermano/a, padre o madre del niño tiene diagnóstico de autismo? (separar familia de primer grado de "otros familiares") |

Añadir la opción **"No sé"** donde tenga sentido y tratarla explícitamente en las reglas (nunca como "No" por defecto). Evitar "tiene comportamientos relacionados" en el ejemplo de id20: no es un antecedente diagnosticado.

### 2.5 Validación

- Validar en **frontend y backend**. El backend es la fuente de verdad: esquema Pydantic con tipos, rangos y enums (hoy `InputArray` acepta `List[Union[int, float, str]]` sin rangos, `app/schemas/input_data.py:5-6`).
- Rechazar con HTTP 422 cualquier respuesta faltante o fuera de rango. No devolver HTTP 200 con `{"error": ...}` (comportamiento actual en `app/api/api.py:33-34`).
- Enviar un **objeto con claves nombradas**, no un arreglo posicional de 25 valores.
- Las horas de inicio/fin se registran en el servidor (sesión de formulario), no se confía en la hora del cliente.

### 2.6 Accesibilidad, lectura y móvil

- **Mobile first**: la mayoría de padres usará celular. Una pregunta por pantalla, botones grandes (mín. 44×44 px), barra de progreso, sin scroll horizontal.
- **Nivel de lectura**: frases cortas, vocabulario de primaria, tuteo o usted de forma consistente (hoy se mezclan "tu hijo" y "su hijo/a"; elegir uno, se sugiere **usted**).
- Ejemplos concretos en cada ítem (ya existen; revisarlos con especialistas).
- Accesibilidad: contraste AA, etiquetas en controles, navegación por teclado, compatible con lector de pantalla, no depender solo del color para el nivel de riesgo.
- Permitir guardar y retomar; tiempo estimado visible ("unos 5 minutos").
- Considerar a futuro versión en quechua y audio de las preguntas **[a validar con especialistas]**.

---

## 3. Arquitectura de 3 capas

### 3.1 Diagrama

```mermaid
flowchart TD
    A[Formulario<br/>20 preguntas + edad en meses] --> B[API /predict<br/>validación Pydantic]
    B --> C[Capa 1: Modelo ML<br/>pipeline sklearn + metadata.json]
    C -->|probabilidad, umbral| D[Capa 2: Reglas clínicas<br/>deterministas y versionadas]
    B -->|comorbilidades, antecedente, edad| D
    D -->|nivel: Bajo / Moderado / Alto / Prioritario<br/>reglas activadas| E[Resultado determinista]
    B -->|A1-A10 + comorbilidades 13, 14, 18, 19| P[Perfiles de riesgo<br/>pesos validados por especialistas<br/>comunicación / social / mixto]
    P --> E
    E --> F[Capa 3: Agente LLM<br/>prompt especializado, JSON estricto]
    F -->|explicación, terapias sugeridas| G[Validador de salida<br/>guardrails]
    G -->|OK| H[Pantalla de resultados]
    G -->|falla / timeout| I[Fallback: textos plantilla<br/>con el resultado determinista]
    I --> H
    H --> J[Cuenta del padre/tutor] --> K[Terapias] --> L[Centros aliados] --> M[Contacto]
```

Principio clave: **las capas 1 y 2 deciden; la capa 3 solo explica.** El LLM nunca cambia la probabilidad, el nivel ni el perfil.

### 3.2 Contrato de datos: solicitud `/predict`

```json
{
  "schema_version": "2.0",
  "consentimiento_id": "uuid",
  "nino": {
    "fecha_nacimiento": "2024-03-15",
    "sexo": "M"
  },
  "qchat10": {
    "A1": 0, "A2": 1, "A3": 2, "A4": 3, "A5": 1,
    "A6": 0, "A7": 2, "A8": 4, "A9": 1, "A10": 4
  },
  "comorbilidades": {
    "habla": "si", "aprendizaje": "no", "genetico": "no_se",
    "depresion": "no", "retraso_desarrollo": "si",
    "social_conducta": "no", "ansiedad": "no"
  },
  "antecedente_familiar": { "primer_grado": "no", "otros": "si" }
}
```

- `qchat10.*` = índice crudo de la opción (0–4). La binarización se hace en el backend con la regla oficial.
- `sexo` ∈ {`M`, `F`}, `comorbilidades.*` ∈ {`si`, `no`, `no_se`}.

### 3.3 Contrato de datos: respuesta

```json
{
  "evaluacion_id": "uuid",
  "modelo": {
    "version": "v2.0.0",
    "sha256": "…",
    "probabilidad": 0.82,
    "umbral": 0.0,
    "positivo": true,
    "qchat10_puntaje": 6,
    "edad_meses": 26,
    "dentro_rango_validado": true
  },
  "reglas": {
    "version": "reglas-2026.1",
    "nivel_base": "Alto",
    "nivel_final": "Prioritario",
    "reglas_activadas": ["R02"]
  },
  "perfil": {
    "comunicacion_pct": 85.0,
    "social_pct": 55.0,
    "perfil": "Comunicación",
    "comorbilidades_sin_responder": []
  },
  "explicacion": {
    "fuente": "llm",
    "prompt_version": "agente-2026.1",
    "texto_padres": "…",
    "terapias_sugeridas": ["terapia_lenguaje", "terapia_ocupacional"],
    "siguientes_pasos": ["…"]
  },
  "avisos": ["Este resultado no es un diagnóstico…"]
}
```

- `umbral` se lee de `models/v2/metadata.json`; no se escribe en el código. El `0.0` del ejemplo es solo un marcador de posición.
- `probabilidad` es **siempre la probabilidad de la clase positiva** (hoy no es así, ver sección 10).
- `explicacion.fuente` ∈ {`llm`, `plantilla`} para saber si se usó el fallback.
- `perfil` es un indicador clínico orientativo (sección 7.1), no una salida del modelo.

---

## 4. Modelo ML en producción (capa 1)

### 4.1 Datos y modelo v2

- El CSV anterior (Kaggle, atribuido a "University of Arkansas") resultó ser el dataset de Nueva Zelanda de Thabtah (2018) con columnas alteradas (edad, sexo, ictericia, antecedente familiar) y columnas y ~930 filas añadidas/fabricadas (comorbilidades, CARS, SRS). **Se descarta por completo**, incluido todo artefacto entrenado con él (`model.pkl`, `pca_model.pkl`).
- Modelo v2: entrenado con los datasets públicos originales Q-CHAT-10 de **Nueva Zelanda** (Thabtah 2018, n=1054, 12–36 meses) y **Arabia Saudita** (n=506, 12–36 meses). Probado externamente en un dataset **polaco con diagnóstico clínico real** (n=252, 18–24 meses; ADOS-2 / ADI-R / DSM-5).
- Modelo elegido: **Regresión Logística con A1–A10**, calibrada (sigmoid) con la mitad de validación del dataset polaco. La edad se evaluó y se descartó porque no mejora el AUC clínico.
- Resultados en el test clínico polaco (n = 126, IC 95 % por bootstrap):

| Método | Sensibilidad | Especificidad | AUC |
|---|---|---|---|
| **Modelo v2 (umbral de `metadata.json`)** | **0.925** [0.85–0.98] | **0.847** [0.75–0.93] | **0.960** [0.93–0.98] |
| Regla oficial Q-CHAT-10 (suma ≥ 4) | 0.791 [0.69–0.89] | 0.932 [0.86–0.98] | 0.964 |
| Regla suma ≥ 3 | 0.925 | 0.847 | 0.964 |

Las cifras y el umbral están en `notebooks/desarrollo_modelo_ml_v2.ipynb` y `models/v2/metadata.json`. **Este documento no fija un umbral**: la fuente de verdad es `metadata.json`. La probabilidad está calibrada en una muestra con 54 % de TEA, así que sobreestima el riesgo poblacional: mostrar niveles, no el porcentaje exacto.

Implicación práctica: el ML **no supera claramente** a la regla oficial. Mostrar siempre también el puntaje Q-CHAT-10 y considerar la regla oficial como línea base y como verificación cruzada.

### 4.2 Entradas del modelo

- Solo **A1–A10**, binarizados según la regla oficial (A1–A9: 1 si la opción es la 3, 4 o 5; A10: 1 si es la 1, 2 o 3). La edad se evaluó y se descartó porque no aporta; se usa solo en las reglas (aviso de validez) y en el agente (mensaje según edad).
- **No** son entradas: sexo, etnia, ictericia, comorbilidades, antecedente familiar. Estas variables no existen con calidad en los datos de entrenamiento o no fueron validadas.

### 4.3 Carga y ejecución

- Un **único pipeline sklearn** serializado (preprocesamiento + modelo). Nada de min/max escritos a mano, nada de PCA separado, nada de reordenar columnas en el código de la API.
- Cargar el pipeline y `metadata.json` **una sola vez al iniciar** la aplicación (hoy se cargan en cada request, ver sección 10).
- `metadata.json` debe contener como mínimo:
  - `version`, `fecha_entrenamiento`, `sha256` del archivo del modelo.
  - `features` (nombres y orden), `edad_unidad: "meses"`.
  - `umbral` y criterio con que se eligió (p. ej. sensibilidad objetivo).
  - `bandas_nivel` (cortes de probabilidad para Bajo/Moderado/Alto), a definir con especialistas.
  - Versiones de `scikit-learn`, `numpy`, `python`.
  - Métricas en validación interna y en test externo polaco.
- Al iniciar, verificar el `sha256` y que la versión de scikit-learn coincida; si no, fallar al arrancar (no servir predicciones con un modelo inconsistente).

### 4.4 Versionado

- Estructura `models/vX/{model.joblib, metadata.json}`. Cada evaluación guardada registra `modelo_version`, `reglas_version` y `prompt_version`.
- Nunca sobrescribir un modelo publicado; publicar uno nuevo y cambiar la versión activa por configuración.

### 4.5 Test de reproducibilidad

- Exportar desde el notebook un archivo `models/vX/casos_referencia.json` con ~50 casos (entradas + probabilidad esperada).
- Test automatizado (pytest, en CI): la API devuelve la misma probabilidad (tolerancia 1e-6) y la misma clase para cada caso.
- Incluir casos límite: todo 0, todo 1, puntaje justo en el umbral, edad en los extremos.
- Los tests actuales (`tests/test_modelo_ml.py`, `tests/test_modelo_pca.py`) validan el modelo viejo con `Sex_M: 0` y PCA; deben reemplazarse.

### 4.6 Monitoreo y drift

- Métricas semanales: número de evaluaciones, distribución de edad, distribución del puntaje Q-CHAT-10, % positivos, % por nivel, % fuera de 18–36 meses.
- Alerta si el % de positivos o la distribución de ítems cambia fuertemente respecto a la línea base (p. ej. PSI > 0.2).
- Registrar latencia y errores de `/predict` y del LLM.

### 4.7 Política de reentrenamiento

- No reentrenar con datos de la app usando como etiqueta la salida del propio modelo (circularidad).
- Solo reentrenar con **etiquetas clínicas reales** (diagnóstico confirmado por un profesional en centros aliados), con consentimiento específico para ese uso.
- Cada reentrenamiento: nuevo notebook/versión, test externo, revisión con especialistas, aprobación documentada antes de activarlo.

### 4.8 Limitaciones conocidas (deben comunicarse en la tesis y en la app)

1. Las etiquetas de entrenamiento (NZ y Arabia Saudita) **son la propia regla Q-CHAT-10** (suma ≥ 4), no diagnósticos clínicos. El modelo aprende a imitar la regla.
2. La única validación clínica externa es de **252 niños polacos de 18–24 meses**.
3. **No hay validación en población peruana** (idioma, cultura, nivel educativo de los padres, forma de responder).
4. Fuera de 18–36 meses no hay evidencia de desempeño.
5. **Plan**: diseñar un estudio de validación local con centros aliados: aplicar la app antes de la evaluación diagnóstica estándar, comparar con el diagnóstico clínico, calcular sensibilidad/especificidad por edad y sexo. Requiere protocolo, consentimiento informado y, probablemente, aprobación de un comité de ética **[a validar con especialistas y asesoría legal]**.

---

## 5. Reglas clínicas (capa 2)

### 5.1 Principios

- **Deterministas, versionadas, documentadas y testeadas.** Viven en un archivo de configuración (YAML/JSON) con tests unitarios por regla.
- **Solo pueden subir el nivel**, nunca bajarlo, y **nunca modifican la probabilidad del modelo**. La app muestra la probabilidad original y, aparte, "nivel ajustado por: …".
- Cada regla cita literatura y tiene un responsable clínico que la aprobó.
- Respuestas "No sé" se tratan explícitamente (en general no activan reglas, pero pueden generar una recomendación de consulta).

### 5.2 Nivel base

El nivel base sale del modelo: bandas de probabilidad definidas en `metadata.json` (p. ej. Bajo < umbral de bajo riesgo ≤ Moderado < umbral ≤ Alto). **Prioritario** solo se alcanza por reglas. Las bandas se acuerdan con especialistas priorizando sensibilidad.

### 5.3 Plantilla de reglas

| ID | Condición | Efecto | Justificación / literatura | Aprobado por | Versión |
|---|---|---|---|---|---|
| R01 | Hermano/a, padre o madre con diagnóstico de TEA **y** nivel base Bajo | Subir a Moderado; recomendar vigilancia y repetir tamizaje | Riesgo de recurrencia en hermanos ~20% (Ozonoff et al., *Pediatrics* 2011; *JAMA Netw Open* 2024) | [pendiente] | reglas-2026.1 |
| R02 | Retraso del habla/lenguaje **y** retraso global del desarrollo (id13 y id17 = sí) | Subir a Prioritario; recomendar evaluación del desarrollo pronta | Signos de alarma que justifican evaluación independiente del tamizaje (AAP, Hyman et al., *Pediatrics* 2020) | [pendiente] | reglas-2026.1 |
| R03 | Diagnóstico de condición genética asociada (id15 = sí) | Subir un nivel; sugerir seguimiento con genética/neuropediatría | Mayor prevalencia de TEA en ciertos síndromes genéticos [citar con especialistas] | [pendiente] | reglas-2026.1 |
| R04 | Edad fuera de 18–36 meses | No cambia nivel; añade aviso de validez y recomendación de evaluación profesional | Rango de validación del Q-CHAT-10 (Allison et al., 2012) | [pendiente] | reglas-2026.1 |
| R05 | Regresión reportada (pérdida de palabras o habilidades) — pregunta a añadir | Prioritario | Signo de alarma clásico [citar con especialistas] | [pendiente] | — |

Las reglas anteriores son **ejemplos de formato**, no reglas aprobadas **[a validar con especialistas]**.

### 5.4 Gobernanza

- Comité mínimo: un(a) especialista clínico (neuropediatría o psicología clínica infantil), un(a) terapeuta y un(a) desarrollador(a).
- Todo cambio de reglas: pull request + acta de aprobación + tests + nueva versión.
- Revisión semestral con los datos de la app (qué reglas se activan y con qué frecuencia).

---

## 6. Agente de IA (capa 3)

### 6.1 Rol

Traducir el resultado determinista a una explicación comprensible y empática para padres, y proponer tipos de terapia y centros compatibles. **No decide nada clínico.**

### 6.2 Entradas

- `probabilidad`, `umbral`, `positivo`, `qchat10_puntaje`, `nivel_final`, `reglas_activadas` (con su texto explicativo).
- Perfil (comunicación / social / mixto) y porcentajes.
- Todas las respuestas (texto de la opción, no solo el índice), `edad_meses`, `dentro_rango_validado`.
- Catálogo cerrado de terapias y lista de centros candidatos ya filtrada por el backend (ubicación, servicios, disponibilidad). El LLM **elige y explica** dentro de esas listas; no inventa centros.
- No enviar al LLM nombres, DNI, correo, teléfono ni datos de contacto.

### 6.3 Salida (JSON estricto)

```json
{
  "resumen_padres": "string (máx. 120 palabras)",
  "que_significa": "string",
  "perfil_explicado": "string",
  "terapias_sugeridas": [
    { "codigo": "terapia_lenguaje", "motivo": "string" }
  ],
  "centros_sugeridos": [
    { "centro_id": "uuid", "motivo": "string" }
  ],
  "siguientes_pasos": ["string"],
  "aviso_no_diagnostico": "string"
}
```

- Validar contra JSON Schema. `codigo` ∈ catálogo (p. ej. `terapia_lenguaje`, `terapia_ocupacional`, `terapia_conductual_aba`, `terapia_juego`, `evaluacion_neuropediatrica`, `evaluacion_psicologica`). `centro_id` ∈ lista enviada.
- Temperatura 0, `max_tokens` acotado, uso de salida estructurada / tool-calling del proveedor.

### 6.4 Guardrails (en el prompt y verificados después)

- Nunca afirmar ni negar un diagnóstico ("su hijo tiene/no tiene autismo"). Usar "señales", "rasgos", "vale la pena una evaluación".
- Siempre recomendar evaluación profesional cuando el nivel ≥ Moderado, y mencionar el control de niño sano en todos los casos.
- Sin consejos de medicación, dietas, suplementos ni tratamientos no basados en evidencia.
- No contradecir la probabilidad ni el nivel recibidos; no inventar números.
- **Lenguaje de crisis/urgencia**: si alguna respuesta sugiere riesgo para el niño (p. ej. autolesiones, texto libre preocupante, regresión) mostrar un mensaje fijo, no generado, con indicación de acudir a un establecimiento de salud. El contenido de ese mensaje lo definen los especialistas.
- Español de Perú, trato de "usted", tono cálido, sin tecnicismos, sin alarmismo ni falsa tranquilidad.
- Post-validación automática: lista de frases prohibidas (p. ej. "tiene autismo", "diagnóstico", "cura", nombres de fármacos), presencia obligatoria del aviso, longitud máxima. Si falla → reintento único → fallback.

### 6.5 Mensajes según edad

| Edad | Enfoque del mensaje |
|---|---|
| < 18 meses | Resultado orientativo; repetir a los 18 meses; conversar con el pediatra en el control. |
| 18–36 meses | "Está en una muy buena etapa para intervenir: el cerebro a esta edad aprende muy rápido y la intervención temprana tiene los mejores resultados." |
| > 36 meses | "El cuestionario es menos preciso a esta edad; si tiene dudas, es importante no esperar y pedir una evaluación profesional pronto." |

Estos textos deben revisarlos especialistas **[a validar con especialistas]**.

### 6.6 Evaluación del agente

- **Set de pruebas** de 40–60 casos sintéticos que cubran: cada nivel, cada perfil, cada regla, cada banda de edad, respuestas "No sé", casos límite en el umbral.
- Métricas automáticas: JSON válido, 0 frases prohibidas, aviso presente, terapias/centros dentro del catálogo, coherencia con el nivel.
- **Revisión humana** por especialistas de una muestra (claridad, empatía, exactitud clínica) con rúbrica 1–5 antes del lanzamiento y en cada cambio de prompt o de modelo LLM.
- Ejecutar el set completo en CI cuando cambie `prompt_version`.

### 6.7 Costo, latencia y logging

- Una sola llamada por evaluación; presupuesto de latencia ~5–8 s con indicador de carga. Mostrar primero el resultado determinista y cargar la explicación después (streaming o carga diferida).
- Estimar costo por evaluación y fijar un tope mensual con alertas.
- Registrar: `prompt_version`, modelo LLM, tokens, latencia, resultado de la validación, uso de fallback. **No** registrar datos personales en los logs del proveedor; revisar su política de retención.

### 6.8 Fallback

Si el LLM falla, excede el tiempo o no pasa la validación: mostrar textos plantilla redactados y aprobados por especialistas para cada combinación nivel × perfil × banda de edad, con las terapias del mapeo determinista (sección 7). La app **siempre** debe poder entregar un resultado sin LLM.

---

## 7. Perfiles de riesgo, terapias y conexión con centros

### 7.1 Cálculo del perfil (pesos validados por especialistas)

El perfil se calcula **como fue diseñado originalmente**, combinando preguntas del Q-CHAT-10 y comorbilidades con los pesos validados por especialistas. Son los mismos pesos que ya usa el formulario actual (`calculateHabilidadPorcentajes` en `Forms.jsx`).

🟦 **Habilidades comunicativas** (suma 100 %)

| Variable | Pregunta | Peso |
|---|---|---|
| A3 | Señala para pedir | 20 % |
| A8 | Primeras palabras | 20 % |
| A9 | Gestos simples | 20 % |
| `c_habla` | Dificultad del habla/lenguaje (id13) | 25 % |
| `c_aprendizaje` | Dificultad de aprendizaje (id14) | 15 % |

🟩 **Interacción social** (suma 100 %)

| Variable | Pregunta | Peso |
|---|---|---|
| A1 | Responde a su nombre | 10 % |
| A2 | Contacto visual | 10 % |
| A4 | Señala para compartir interés | 10 % |
| A5 | Juego simbólico | 15 % |
| A6 | Sigue la mirada | 15 % |
| A7 | Consuela | 15 % |
| `c_social_conducta` | Problemas sociales/conducta (id18) | 20 % |
| `c_ansiedad` | Ansiedad (id19) | 5 % |

- `comunicacion_pct` = Σ (peso × valor) de su tabla, con cada variable en 0/1.
- `social_pct` = Σ (peso × valor) de su tabla.
- Perfil = **Mixto** si |com% − soc%| < 10; si no, el de mayor porcentaje (**Comunicación** o **Interacción social**).
- A10 y las comorbilidades 15, 16 y 17 no entran en ningún perfil (17 y 15 se usan en las reglas de la capa 2).
- **Respuesta "No sé"** en una comorbilidad: se cuenta como 0 en el porcentaje, pero se registra en `comorbilidades_sin_responder` para que el agente lo mencione ("no sabemos si…") **[a validar con especialistas]**.
- **Caso límite:** si ambos porcentajes son 0 (o muy bajos), la regla da "Mixto". Definir con especialistas si en ese caso se muestra "Sin perfil predominante" o no se muestra perfil **[a validar con especialistas]**.

### 7.2 Qué está validado con datos y qué no

- El perfil **no es una salida del modelo ML**: es un indicador clínico orientativo para explicar el resultado y orientar las terapias. El riesgo lo deciden las capas 1 y 2.
- La **parte del Q-CHAT-10** de los perfiles se evaluó en el notebook v2 con los niños polacos con diagnóstico clínico: el porcentaje social separa bien a los niños con TEA (AUC 0.91) y el comunicativo algo menos (AUC 0.83). Ahí se calculó solo con las preguntas, porque los datasets públicos no tienen comorbilidades.
- La **parte de las comorbilidades** se apoya en el criterio de los especialistas, no en datos. Cuando la plataforma acumule evaluaciones con diagnóstico confirmado por los centros, conviene revisar estos pesos con datos reales.

### 7.3 Mapeo determinista de terapias (base para el fallback y para acotar al LLM)

| Condición | Terapias sugeridas a explorar |
|---|---|
| Perfil Comunicación o id13 = sí | Terapia de lenguaje |
| Perfil Social | Terapia de juego / intervención en habilidades sociales; terapia conductual (ABA u otras basadas en evidencia) |
| Perfil Mixto | Evaluación interdisciplinaria; lenguaje + intervención social |
| Retraso del desarrollo, dificultades motoras o sensoriales | Terapia ocupacional |
| Nivel Alto o Prioritario | Evaluación diagnóstica (neuropediatría / psicología clínica) **antes** o en paralelo a iniciar terapias |

Tabla **[a validar con especialistas]**.

### 7.4 Flujo de la Solución 1

1. **Test** anónimo (sin registro) → resultado determinista inmediato.
2. **Cuenta** (opcional, para guardar resultado, recibir PDF o contactar centros) con consentimiento expreso.
3. **Terapias** sugeridas con explicación de qué es cada una.
4. **Centros** aliados filtrados por distrito/ciudad, servicios, modalidad (presencial/virtual), rango de precio, cobertura de seguro.
5. **Contacto**: la familia elige compartir su resultado con un centro concreto (consentimiento por centro, revocable). Registrar el estado del lead (enviado, contactado, cita agendada) para medir impacto.

Consideraciones:
- Criterios de orden de los centros transparentes (no solo quién paga más). Si hay centros patrocinados, indicarlo.
- Conflicto de interés: la herramienta es gratuita y los centros son clientes; el resultado nunca debe inflarse para generar derivaciones. Esto refuerza que capas 1–2 sean deterministas y auditables.
- Ofrecer siempre también la opción pública (MINSA/EsSalud, control CRED) para familias sin recursos.

---

## 8. Ética, sesgos y comunicación del riesgo

### 8.1 Sesgos

- Reportar sensibilidad/especificidad **por sexo** y **por banda de edad** en el notebook v2 y en el monitoreo. El TEA se subdiagnostica en niñas; comprobar que el desempeño no sea peor para ellas.
- El sexo **no** entra al modelo; se recoge solo para auditoría de sesgos.
- Revisar el funcionamiento por nivel educativo del cuidador y región cuando haya datos locales.

### 8.2 Comunicación del resultado

- Evitar "positivo/negativo" y porcentajes aislados. Preferir: "**Señales a conversar con un profesional**" (nivel) + puntaje Q-CHAT-10 + explicación.
- Si se muestra una probabilidad, contextualizarla: "no es la probabilidad de que su hijo tenga autismo, es qué tanto se parecen sus respuestas a las de niños que requirieron evaluación".
- Evitar alarmismo (colores rojos intensos, palabras como "grave") y evitar falsa tranquilidad en resultados bajos ("si sigue preocupado, consulte igual").
- Resultado bajo ≠ descarte: recomendar vigilancia del desarrollo y repetir el tamizaje.

### 8.3 Avisos obligatorios (resultado, PDF, correo)

> Este resultado es un tamizaje orientativo y **no es un diagnóstico**. Solo un profesional de la salud puede diagnosticar el trastorno del espectro autista. Si tiene cualquier preocupación sobre el desarrollo de su hijo/a, consulte a su pediatra o a un especialista, sin importar el resultado.

Añadir el aviso de validez por edad cuando corresponda.

---

## 9. Privacidad y aspectos legales (Perú)

Todos los puntos de esta sección son **[a validar con asesoría legal]**.

### 9.1 Marco

- **Ley N.º 29733**, Ley de Protección de Datos Personales, y su Reglamento vigente (el nuevo Reglamento aprobado por D.S. N.º 016-2024-JUS, que reemplazó al D.S. N.º 003-2013-JUS; confirmar vigencia y obligaciones concretas).
- Autoridad: **Autoridad Nacional de Protección de Datos Personales (ANPD)**, del Ministerio de Justicia y Derechos Humanos.

### 9.2 Obligaciones principales

| Tema | Qué implica para la app |
|---|---|
| Datos sensibles | Los datos de salud son sensibles; además son de **menores de edad**. |
| Consentimiento | Consentimiento **previo, expreso, informado, inequívoco y por escrito (medio digital válido)** del padre, madre o tutor. Casillas no premarcadas, separadas por finalidad. |
| Finalidades | Separar: (a) calcular el tamizaje; (b) guardar el historial en la cuenta; (c) compartir con un centro elegido; (d) uso anonimizado para mejorar el modelo / investigación. Cada una opcional salvo (a). |
| Información | Política de privacidad clara: responsable, finalidad, destinatarios (centros, proveedor LLM, hosting), transferencias internacionales, plazo de conservación, cómo ejercer derechos. |
| Registro | Inscribir el banco de datos personales ante el Registro Nacional de Protección de Datos Personales de la ANPD. |
| Flujo transfronterizo | El hosting y el proveedor del LLM probablemente estén fuera del Perú: informar y cumplir los requisitos de transferencia internacional. Minimizar lo que se envía al LLM (sin identificadores). |
| Seguridad | Medidas técnicas y organizativas: cifrado en tránsito y en reposo, control de acceso por roles, registro de accesos, contraseñas fuera del código, copias de seguridad. |
| Derechos ARCO | Acceso, rectificación, cancelación y oposición: canal y procedimiento con plazos; botón para descargar y eliminar los datos. |
| Oficial de datos | Evaluar si corresponde designar un oficial de datos personales según el nuevo reglamento. |

### 9.3 Retención y anonimización

- Test anónimo sin cuenta: guardar solo datos no identificables; definir plazo (p. ej. 24 meses) para métricas.
- Datos de cuenta: mientras la cuenta exista + plazo definido; borrado real al cancelar.
- Para reentrenamiento: dataset **anonimizado** (sin nombre, contacto, fecha exacta de nacimiento → edad en meses; sin identificadores de centro si no son necesarios), con consentimiento específico.
- No guardar respuestas de salud en `localStorage` del navegador más allá de la sesión (hoy se hace, ver sección 10).

### 9.4 Dispositivo médico

Si la app se presenta o comercializa como herramienta de **diagnóstico**, podría considerarse software como dispositivo médico y requerir evaluación ante **DIGEMID** (Ley N.º 29459 y normas de dispositivos médicos). Mantener el posicionamiento como tamizaje orientativo y **consultar asesoría legal/regulatoria** antes de lanzar y antes de cualquier material de marketing.

### 9.5 Investigación

Si la validación local o la tesis usan datos de niños, preparar protocolo, consentimiento informado y revisión por un comité de ética en investigación.

---

## 10. Bugs y deuda técnica del sistema actual

Verificados en el código del repositorio (backend en `app/`, frontend a partir del source map `app/frontend/static/js/main.c57643bb.js.map`).

### 10.1 Modelo e inferencia

| # | Problema | Ubicación | Acción |
|---|---|---|---|
| 1 | Se fuerza `Sex_M = 0` (todos tratados como niñas) al construir el vector del PCA y del SVM, aunque el frontend envía el sexo real. | `app/model/data_preprocessor.py:82` y `:128` | Eliminar; el sexo no es entrada del modelo v2. |
| 2 | Normalización min/max escrita a mano, incluida edad en años con rango (1, 18). | `app/model/data_preprocessor.py:16-50` | Reemplazar por pipeline sklearn único. |
| 3 | PCA separado (`pca_model.pkl`) calculado a mano y concatenado al vector. | `app/model/data_preprocessor.py:104-110` | Eliminar. |
| 4 | Vector de 20 features con comorbilidades y porcentajes derivados del dataset fabricado. | `app/model/data_preprocessor.py:113-147` | Reemplazar por A1–A10 (lista en `metadata.json`). |
| 5 | Umbral fijo 0.605 en código. En el notebook viejo hay 0.75 (celda 518), 0.605 (celda 520) y umbrales "óptimos" por ROC de 0.626 y 0.597 (celda 514). | `app/model/predictor.py:14` | Leer de `models/v2/metadata.json`. |
| 6 | `riesgo_autismo` es la probabilidad **de la clase predicha**, no de la clase positiva: un niño con 5% de probabilidad positiva aparece con "riesgo" 95%. | `app/model/predictor.py:17-19` | Devolver siempre `P(clase=1)`. |
| 7 | Ese mismo valor se guarda como `nivel_confianza` y el dashboard lo rotula como "riesgo de TEA". | `app/model/data_preprocessor.py:186`, `app/api/dashboard.py:64` y `:105` | Renombrar a `probabilidad` y migrar datos. |
| 8 | El modelo y el PCA se cargan desde disco en cada request. | `app/model/predictor.py:6-7`, `app/model/data_preprocessor.py:107-108` | Cargar una vez al inicio. |
| 9 | Tests validan el modelo viejo (PCA, `Sex_M: 0`). | `tests/test_modelo_ml.py:22`, `tests/test_modelo_pca.py:33` | Reemplazar por test de reproducibilidad v2. |

### 10.2 API y datos

| # | Problema | Ubicación | Acción |
|---|---|---|---|
| 10 | Entrada como arreglo posicional de 25 valores de tipo libre, sin validación de rangos. | `app/schemas/input_data.py:5-6`, `app/model/data_preprocessor.py:7-14` | Esquema Pydantic con claves nombradas (sección 3.2). |
| 11 | Longitud incorrecta devuelve HTTP 200 con `{"error": ...}`. | `app/api/api.py:33-34` | HTTP 422. |
| 12 | Edad almacenada en años (`SmallInteger`). | `app/db/models.py:14` | Guardar `edad_meses` (y fecha de nacimiento solo si hay cuenta y consentimiento). |
| 13 | Solo se guardan A1–A10 binarizados; se pierde la respuesta cruda. | `app/db/models.py:17-26` | Guardar índice 0–4. |
| 14 | No se guarda versión de modelo, reglas ni prompt. | `app/db/models.py:10-54` | Añadir columnas de versión. |
| 15 | La hora de inicio viene del cliente (`Time_Start`). | `app/model/data_preprocessor.py:178`, `app/api/api.py:53-56` | Registrar inicio en el servidor. |
| 16 | `/enviar-pdf` no requiere autenticación y usa `file.filename` sin sanear para construir la ruta temporal (riesgo de path traversal y de uso como relé de correo). | `app/api/api.py:69-85` (ruta en `:76`) | Autenticación o token de evaluación, nombre de archivo generado, límite de tamaño y de envíos. |
| 17 | Credenciales del usuario administrador por defecto escritas en el código. | `app/db/init_db.py:7-10` | Mover a variables de entorno, rotar la contraseña y eliminar la creación automática en producción. |
| 18 | Tablas creadas con `create_all` al importar la app (sin migraciones). | `app/main.py:16` | Usar Alembic (ya está en `requirements.txt`). |

### 10.3 Frontend (desde el source map)

| # | Problema | Ubicación | Acción |
|---|---|---|---|
| 19 | Edad en años, rango 1–18; `handleChange` además acepta 0 aunque `isValid` exige ≥ 1. | `components/Forms.jsx:45` y `:219` | Fecha de nacimiento o años+meses. |
| 20 | `evolSociales` y `evolComunicativas` invierten las preguntas Sí/No: marcan 1 cuando la respuesta es "No" (`r === 0 ? 1 : 0`), al contrario que los porcentajes, que usan `=== 1`. | `components/Forms.jsx:151` y `:154` | Usar `r === 1`. |
| 21 | Los porcentajes de habilidades se calculan en el frontend y no se indica que son un indicador orientativo (no salida del modelo). | `components/Forms.jsx:59-82` y `:113-144` | Mover el cálculo al backend (fuente única, sección 7.1) y presentarlo como indicador orientativo. |
| 22 | `onFinish()` se llama antes de que termine el `fetch` a `/predict`; si falla, solo hay `console.error` y el usuario no ve error. | `components/Forms.jsx:190-207` | Esperar la respuesta, manejar errores y reintentos. |
| 23 | Todas las respuestas de salud se guardan en `localStorage` (`reportData`). | `components/Forms.jsx:178-188` y `:200-203` | Usar estado en memoria o `sessionStorage` con limpieza; datos persistentes solo en el servidor con consentimiento. |
| 24 | Mezcla de "tu hijo" y "su hijo/a" en las preguntas. | `components/form-comp/questions.js` | Unificar a "usted". |
| 25 | El frontend servido desde `app/frontend` es un build compilado; el código fuente no está en este repositorio. | `app/frontend/` | Ubicar el repositorio del frontend y versionarlo junto con el contrato de la API. |

### 10.4 Datos y artefactos

- `model.pkl` y `pca_model.pkl` en la raíz del repo están entrenados con el dataset alterado; retirarlos de producción al activar v2 (conservar solo como referencia histórica en la tesis).
- `requirements.txt` está codificado en UTF-16 LE con CRLF; convertirlo a UTF-8 para evitar fallos de `pip` y de herramientas de CI en algunos entornos.

---

## 11. Checklist antes de lanzar

### Modelo y reglas
- [ ] Modelo v2 como pipeline único + `metadata.json` con umbral, bandas, versiones y hash.
- [ ] Test de reproducibilidad notebook ↔ API pasando en CI.
- [ ] Métricas por sexo y por edad documentadas; sin diferencias relevantes o con plan de mitigación.
- [ ] Reglas clínicas v1 aprobadas por especialistas, con citas y tests unitarios.
- [ ] Bandas de nivel (Bajo/Moderado/Alto) aprobadas por especialistas.
- [ ] Limitaciones del modelo redactadas para la app y para la tesis.
- [ ] Protocolo de validación local con centros aliados iniciado.

### Formulario y UX
- [ ] Edad en meses (o fecha de nacimiento) con avisos de validez fuera de 18–36 meses.
- [ ] Preguntas de comorbilidad reformuladas y opción "No sé".
- [ ] Respuestas crudas guardadas; validación Pydantic con claves nombradas.
- [ ] Prueba con 5–10 padres reales en celular (comprensión y tiempo).
- [ ] Accesibilidad AA verificada.

### Agente de IA
- [ ] Prompt versionado, salida JSON validada, temperatura 0.
- [ ] Set de 40–60 casos con 0 violaciones de guardrails.
- [ ] Revisión humana por especialistas con rúbrica aprobada.
- [ ] Fallback con plantillas aprobadas probado (simular caída del LLM).
- [ ] Sin datos identificables enviados al proveedor LLM.

### Comunicación y ética
- [ ] Aviso "no es un diagnóstico" en resultado, PDF y correo.
- [ ] Textos de resultados revisados por especialistas (sin alarmismo ni falsa tranquilidad).
- [ ] Criterios de orden de centros publicados; patrocinios señalados.

### Privacidad y legal [a validar con asesoría legal]
- [ ] Política de privacidad y consentimientos separados por finalidad.
- [ ] Banco de datos inscrito ante la ANPD.
- [ ] Transferencia internacional (hosting, LLM) informada y cubierta.
- [ ] Procedimiento ARCO operativo (descarga y eliminación de datos).
- [ ] Política de retención y anonimización implementada.
- [ ] Opinión legal sobre DIGEMID / dispositivo médico.

### Seguridad y operación
- [ ] Bugs de la sección 10 corregidos (como mínimo 1, 5, 6, 10, 16, 17, 20, 22, 23).
- [ ] Credenciales fuera del código y rotadas; HTTPS; cifrado en reposo.
- [ ] Migraciones con Alembic; backups probados.
- [ ] Monitoreo de métricas, drift, latencia, errores y costo del LLM con alertas.
- [ ] Registro de versión de modelo, reglas y prompt en cada evaluación.
