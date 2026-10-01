# Arquitectura de Conecta

Arquitectura técnica de la **Solución 1: Conecta** (plataforma de tamizaje), con su frontend, su backend y su base de datos, y cómo se integra con el SGT y el Panel Startup.

Versión 1.0 · 2026-10-01

---

## 0. Vista general

### 0.1 Los tres espacios

| Espacio | Tecnología | Base de datos | Dueño de… |
|---|---|---|---|
| **Conecta** | Next.js (frontend) + FastAPI (backend) | PostgreSQL | Tamizajes, resultados, modelo de ML, agente IA, contactos de padres, métricas de uso |
| **SGT** | C# | SQL Server 2022+ | Centros, sedes, terapias, pacientes, citas. Incluye la versión limitada del SGT (panel de autogestión) para los centros que solo contratan Conecta |
| **Panel Startup** | ASP.NET Core + React/TypeScript | Propia | **TenantId**, estado de cada centro, productos habilitados (Conecta, SGT), suscripciones, vista de modelos y métricas |

**Regla principal:** cada espacio es dueño de su base de datos. Los demás obtienen esos datos **a través de su API**, nunca entrando directo a la base.

### 0.2 TenantId y productos habilitados

- El **TenantId** identifica a cada centro cliente en los tres espacios.
- Lo crea el **Panel Startup** al registrar un centro, junto con los productos que contrató. Un centro no puede habilitarse productos a sí mismo.
- El Panel crea el centro en el **SGT** con el mismo TenantId: en versión limitada si solo tiene Conecta, completa si tiene SGT.
- **Conecta consulta al Panel** qué tenants tienen Conecta activo (opción A acordada). Si un centro deja de tener Conecta, desaparece de las recomendaciones aunque sus terapias sigan en el SGT.

**Alta de un centro:**

1. El equipo registra el centro en el Panel → se genera su TenantId y se marcan sus productos.
2. El Panel crea el centro en el SGT con ese TenantId.
3. El centro carga sus sedes y terapias en el SGT (completo o limitado).
4. Conecta copia el catálogo del SGT: cada sede y terapia trae su TenantId.
5. Conecta copia del Panel la lista de tenants con Conecta activo y solo muestra esos centros a los padres.

### 0.3 Diagrama general

```mermaid
flowchart LR
    subgraph Usuarios
        P["Padres"]
        C["Centros"]
        E["Equipo startup"]
    end

    subgraph Conecta
        WEB["Frontend<br>Next.js"]
        API["Backend<br>FastAPI"]
        WK["Workers"]
        PG[("PostgreSQL")]
        ML["MLflow"]
    end

    subgraph SGT
        SAPI["API SGT<br>C#"]
        SQL[("SQL Server")]
    end

    subgraph Panel
        PAPI["API Panel<br>ASP.NET Core"]
        PDB[("Base del Panel")]
    end

    LLM["Proveedor LLM"]

    P --> WEB --> API
    C --> SAPI
    E --> PAPI
    API --> PG
    WK --> PG
    API --> LLM
    WK -- "catálogo, diagnósticos" --> SAPI
    WK -- "pacientes nuevos (Integral)" --> SAPI
    WK -- "tenants activos" --> PAPI
    PAPI -- "/internal: modelos, métricas" --> API
    PAPI -- "alta de centros" --> SAPI
    SAPI --> SQL
    PAPI --> PDB
    WK --> ML
```

---

## 1. Alcance de Conecta

| Incluido | Fuera de Conecta |
|---|---|
| Landing y páginas públicas de los centros | Panel de autogestión de los centros (es la versión limitada del SGT, en C#) |
| Prueba de tamizaje, registro del padre y resultado | Alta de centros, TenantId, productos y suscripciones (Panel Startup) |
| Modelo de ML, reglas clínicas, perfiles y agente IA | Gestión de citas y pacientes (SGT) |
| Terapias sugeridas, comparación de sedes y contacto con centros | Programa de referidos y puntos (fase posterior, solo para centros con SGT) |
| Métricas de uso para el reporte mensual de los centros | Facturación (Panel Startup) |
| Endpoints internos de modelos y métricas para el Panel | |

---

## 2. Frontend (Next.js)

### 2.1 Tecnologías

| Tema | Elección | Motivo |
|---|---|---|
| Framework | **Next.js** (App Router) + **TypeScript** | Páginas públicas generadas en el servidor (aparecen en Google) y app interactiva en el mismo proyecto |
| Estilos | Tailwind CSS + librería de componentes accesible (p. ej. shadcn/ui) | Rápido de construir, consistente y accesible |
| Datos del servidor | TanStack Query | Caché, reintentos y estados de carga |
| Formularios | React Hook Form + Zod | Validación en el cliente con los mismos esquemas que espera el backend |
| Sesión | Cookie `httpOnly` emitida por el backend | El token no queda expuesto al JavaScript del navegador |
| Pruebas | Vitest (componentes) + Playwright (recorridos completos) | |

### 2.2 Rutas

| Ruta | Pantalla | Tipo |
|---|---|---|
| `/` | Landing de Conecta | Pública, generada en servidor |
| `/centros` | Directorio de centros | Pública, generada en servidor |
| `/centros/[slug]` | Página del centro: información, sedes, terapias y contacto | Pública, regenerada al cambiar el catálogo |
| `/tamizaje` | Inicio de la prueba: qué es, cuánto dura, consentimiento | Pública |
| `/tamizaje/preguntas` | Las 20 preguntas, una por pantalla, con progreso | Pública; se puede retomar |
| `/registro` | Crear cuenta antes de ver el resultado | Pública |
| `/resultado/[id]` | Nivel de riesgo, perfil y explicación | Requiere sesión |
| `/resultado/[id]/terapias` | Terapias sugeridas y sedes que las ofrecen | Requiere sesión |
| `/resultado/[id]/sedes` | Comparación de sedes | Requiere sesión |
| `/contacto/[sede]` | Formulario de contacto con la sede | Requiere sesión |
| `/cuenta` | Historial de pruebas y datos del padre | Requiere sesión |
| `/privacidad`, `/terminos` | Textos legales | Pública |

### 2.3 Criterios

- **Mobile first:** una pregunta por pantalla, botones grandes y barra de progreso.
- El frontend **solo habla con el backend de Conecta**; nunca con el SGT, el Panel ni el proveedor del LLM.
- El avance de la prueba se guarda para poder retomarla. Las respuestas se envían al backend al terminar.
- El resultado se muestra en dos tiempos: primero el nivel y el perfil (instantáneo) y luego la explicación del agente IA (carga diferida).
- Accesibilidad AA, español de Perú y avisos obligatorios ("esto no es un diagnóstico") en el resultado.
- Las visitas a las páginas de los centros y los clics en "contactar" se registran como eventos para el reporte mensual, sin datos personales.

---

## 3. Backend (FastAPI)

### 3.1 Tecnologías

| Tema | Elección |
|---|---|
| Lenguaje y framework | Python 3.12, FastAPI, Pydantic v2 |
| Base de datos | PostgreSQL con SQLAlchemy 2 y migraciones con Alembic |
| Procesos en segundo plano | Redis + workers (Celery o arq) |
| Modelo | scikit-learn 1.6.1 (`models/v2/modelo_tamizaje_tea.pkl` + `metadata.json`) |
| Seguimiento de modelos | MLflow (almacenamiento en PostgreSQL) |
| Llamadas a otras APIs | httpx, con reintentos y tiempos límite |
| Agente IA | SDK del proveedor del LLM con *tool calling* (LangGraph cuando el flujo crezca) |

### 3.2 Estructura de módulos

```
conecta-api/
├── app/
│   ├── auth/          ← registro, login y sesión de padres
│   ├── tamizaje/      ← evaluaciones, respuestas, puntuación Q-CHAT-10
│   ├── riesgo/        ← capa 1 (modelo), capa 2 (reglas) y perfiles
│   ├── agente/        ← capa 3: prompt, base de conocimiento, buscar_terapias
│   ├── catalogo/      ← copia de centros, sedes y terapias del SGT + tenants activos del Panel
│   ├── contactos/     ← contacto padre → sede y envío de pacientes nuevos al SGT
│   ├── metricas/      ← eventos y reportes mensuales por centro
│   ├── modelos/       ← versiones, métricas, reentrenamiento (MLflow)
│   ├── internal/      ← endpoints para el Panel Startup
│   ├── integraciones/ ← clientes HTTP del SGT, del Panel, del LLM y de correo
│   └── core/          ← configuración, seguridad, base de datos, logs
├── workers/           ← tareas en segundo plano
├── conocimiento/      ← base de conocimiento curada del agente (versionada)
└── models/            ← modelo y metadata.json
```

### 3.3 Endpoints públicos (para el frontend)

| Método y ruta | Uso |
|---|---|
| `POST /auth/registro`, `POST /auth/login`, `POST /auth/logout` | Cuenta del padre |
| `POST /consentimientos` | Registrar el consentimiento del padre o tutor |
| `POST /evaluaciones` | Enviar las respuestas de la prueba; devuelve el id de la evaluación |
| `GET /evaluaciones/{id}/resultado` | Nivel, probabilidad, perfil y reglas activadas |
| `GET /evaluaciones/{id}/explicacion` | Explicación y terapias sugeridas por el agente IA |
| `GET /evaluaciones` | Historial del padre |
| `GET /centros`, `GET /centros/{slug}` | Directorio y página pública de un centro (solo tenants activos) |
| `GET /sedes?terapia=…&distrito=…` | Sedes que ofrecen una terapia |
| `POST /contactos` | El padre contacta a una sede |
| `POST /eventos` | Visitas y clics para las métricas de los centros |

### 3.4 Endpoints internos (para el Panel Startup)

Bajo `/internal`, con autenticación entre servicios. Devuelven **agregados**, nunca datos individuales de niños.

| Método y ruta | Uso |
|---|---|
| `GET /internal/modelos` | Versión en producción y candidatos |
| `GET /internal/modelos/{version}/metricas` | AUC, sensibilidad y especificidad: de validación y reales |
| `GET /internal/metricas/uso` | Tamizajes por día y distribución de niveles de riesgo |
| `GET /internal/metricas/centros/{tenant_id}` | Visitas, contactos y conversión por centro (reporte mensual) |
| `GET /internal/metricas/sesgos` | Rendimiento por sexo y edad |
| `POST /internal/entrenamientos`, `GET /internal/entrenamientos/{id}` | Lanzar y seguir un reentrenamiento |
| `POST /internal/modelos/{version}/promover` | Pasar un candidato a producción (queda registrado quién lo aprobó) |
| `POST /internal/webhooks/tenants` | El Panel avisa que cambió el estado de un tenant |

### 3.5 Integraciones

| Con | Qué | Cómo |
|---|---|---|
| **API SGT** | Copia de centros, sedes y terapias (con TenantId) | Worker cada 5 minutos con `actualizado_desde` |
| **API SGT** | Paciente nuevo cuando un padre contacta una sede de un centro con SGT completo | Cola con reintentos |
| **API SGT** | Diagnósticos confirmados (con consentimiento) para reentrenar | Worker diario |
| **API Panel** | Tenants con Conecta activo | Worker cada 5 minutos + webhook del Panel ante cambios |
| **Proveedor LLM** | Explicación del resultado y elección de terapias | Llamada con *tool calling*; textos plantilla si falla |
| **Correo** | Confirmaciones, resultado en PDF y aviso de contacto a la sede | Cola |

### 3.6 Cálculo del resultado

`POST /evaluaciones` ejecuta en orden:

1. **Validación** de las 20 respuestas (Pydantic) y del consentimiento.
2. **Puntuación** de A1–A10 igual que el Q-CHAT-10 oficial.
3. **Capa 1 (modelo):** probabilidad calibrada y comparación con el umbral de `metadata.json`.
4. **Capa 2 (reglas clínicas):** comorbilidades, antecedente familiar y edad pueden subir el nivel (Bajo / Moderado / Alto / Prioritario).
5. **Perfil:** porcentajes comunicativo y social con los pesos validados por especialistas.
6. Se guarda todo con las **versiones** del modelo y de las reglas, y se devuelve el resultado.
7. **Capa 3 (agente IA):** se genera la explicación aparte. El agente llama a `buscar_terapias`, que consulta la copia del catálogo filtrando por tenants activos, edad y zona. El backend valida la salida; si falla, se usan textos plantilla.

### 3.7 Seguridad

- Sesión de padres con cookie `httpOnly` y `SameSite`; contraseñas con hash robusto (argon2).
- Autenticación entre servicios (API key o credenciales de cliente) para `/internal` y para las llamadas al SGT y al Panel.
- Límite de peticiones en el login, el registro y el envío de evaluaciones.
- Logs sin datos personales; las respuestas de salud nunca van a los logs.
- Cifrado en tránsito (HTTPS) y en reposo (base de datos y respaldos).
- Al proveedor del LLM solo se envían los datos necesarios, sin nombre ni contacto del padre.

---

## 4. Base de datos (PostgreSQL)

### 4.1 Esquemas

| Esquema | Contenido |
|---|---|
| `app` | Datos propios de Conecta: padres, evaluaciones, resultados, contactos, eventos |
| `catalogo` | Copias de solo lectura: tenants activos (del Panel) y centros, sedes y terapias (del SGT) |
| `ml` | Versiones del modelo, métricas, entrenamientos y diagnósticos confirmados |
| `mlflow` | Almacenamiento interno de MLflow |

### 4.2 Tablas principales

| Tabla | Campos clave |
|---|---|
| `app.padres` | id, correo, nombre, teléfono, distrito, creado_en |
| `app.consentimientos` | id, padre_id, version_texto, finalidades, aceptado_en, revocado_en |
| `app.evaluaciones` | id, padre_id, edad_meses, sexo, estado, iniciada_en, finalizada_en |
| `app.respuestas` | evaluacion_id, pregunta_id, opcion_indice (0–4 o sí/no/no sé), valor_binario |
| `app.resultados` | evaluacion_id, qchat10_puntaje, probabilidad, umbral, positivo, nivel_base, nivel_final, reglas_activadas, comunicacion_pct, social_pct, perfil, version_modelo, version_reglas |
| `app.explicaciones` | evaluacion_id, fuente (llm o plantilla), texto, terapias_sugeridas, version_prompt, version_conocimiento |
| `app.contactos` | id, padre_id, evaluacion_id, tenant_id, sede_id, terapia_id, mensaje, estado_envio_sgt, creado_en |
| `app.eventos` | id, tipo (visita, clic_contacto), tenant_id, sede_id, fecha (sin datos personales) |
| `catalogo.tenants` | tenant_id, nombre, conecta_activo, sgt_completo, actualizado_en |
| `catalogo.sedes` | sede_id, tenant_id, nombre, slug, distrito, direccion, contacto, actualizado_en |
| `catalogo.terapias` | terapia_id, tenant_id, sede_id, nombre, descripcion, edad_min_meses, edad_max_meses, modalidad, activa, actualizado_en |
| `ml.diagnosticos_confirmados` | evaluacion_id, diagnostico, fecha_diagnostico, origen (SGT), consentimiento_id |
| `ml.modelos` | version, estado (candidato, produccion, retirado), metricas, mlflow_run_id, aprobado_por, promovido_en |
| `ml.entrenamientos` | id, estado, version_resultante, iniciado_por, iniciado_en, finalizado_en |

### 4.3 Diagrama entidad-relación

```mermaid
erDiagram
    PADRES ||--o{ CONSENTIMIENTOS : otorga
    PADRES ||--o{ EVALUACIONES : realiza
    EVALUACIONES ||--|{ RESPUESTAS : contiene
    EVALUACIONES ||--|| RESULTADOS : produce
    EVALUACIONES ||--o| EXPLICACIONES : tiene
    EVALUACIONES ||--o{ CONTACTOS : origina
    PADRES ||--o{ CONTACTOS : envia
    TENANTS ||--o{ SEDES : tiene
    SEDES ||--o{ TERAPIAS : ofrece
    SEDES ||--o{ CONTACTOS : recibe
    TENANTS ||--o{ EVENTOS : acumula
    EVALUACIONES ||--o| DIAGNOSTICOS_CONFIRMADOS : confirma
    MODELOS ||--o{ RESULTADOS : calcula
```

### 4.4 Datos sensibles y retención

- Los datos de salud del niño (respuestas y resultados) son **datos sensibles** según la Ley N.º 29733: requieren consentimiento expreso del padre o tutor (a validar con asesoría legal).
- **No se guarda el nombre del niño**; solo edad en meses y sexo.
- Para reentrenar y para las métricas se usan **datos anonimizados** (sin padre ni contacto).
- Plazos de conservación y de borrado a pedido del padre: a definir con asesoría legal.

---

## 5. Flujos principales

### 5.1 Tamizaje de principio a fin

```mermaid
sequenceDiagram
    participant Pa as Padre
    participant W as Frontend
    participant A as Backend
    participant DB as PostgreSQL
    participant L as LLM
    Pa->>W: Responde las 20 preguntas
    W->>A: POST /auth/registro + /consentimientos
    W->>A: POST /evaluaciones
    A->>A: Puntuación, modelo, reglas, perfil
    A->>DB: Guarda evaluación y resultado
    A-->>W: Nivel, perfil, reglas
    W->>A: GET /evaluaciones/{id}/explicacion
    A->>L: Resultado + base de conocimiento
    L->>A: buscar_terapias
    A->>DB: Terapias de tenants activos por edad y zona
    A-->>L: Lista de terapias
    L-->>A: Explicación y terapias elegidas
    A->>A: Valida la salida o usa plantilla
    A-->>W: Explicación y terapias
```

### 5.2 Copia del catálogo y de los tenants activos

```mermaid
sequenceDiagram
    participant WK as Worker
    participant P as API Panel
    participant S as API SGT
    participant DB as PostgreSQL
    loop Cada 5 minutos
        WK->>P: GET tenants con Conecta activo
        P-->>WK: Lista de tenants
        WK->>DB: Actualiza catalogo.tenants
        WK->>S: GET terapias y sedes actualizadas desde la última copia
        S-->>WK: Sedes y terapias con TenantId
        WK->>DB: Actualiza catalogo.sedes y catalogo.terapias
    end
    P->>WK: Webhook: cambió un tenant
    WK->>DB: Actualiza ese tenant al instante
```

### 5.3 El padre contacta una sede

```mermaid
sequenceDiagram
    participant Pa as Padre
    participant A as Backend
    participant DB as PostgreSQL
    participant Q as Cola
    participant S as API SGT
    Pa->>A: POST /contactos
    A->>DB: Guarda el contacto
    A->>Q: Encola el aviso
    alt Centro con SGT completo
        Q->>S: POST paciente nuevo con evaluación resumida
    else Centro solo con Conecta
        Q->>Q: Aviso por correo a la sede
    end
    Q->>DB: Actualiza estado_envio_sgt
```

### 5.4 Reentrenamiento del modelo

```mermaid
sequenceDiagram
    participant E as Equipo startup
    participant P as API Panel
    participant A as Backend
    participant WK as Worker
    participant M as MLflow
    E->>P: Reentrenar
    P->>A: POST /internal/entrenamientos
    A->>WK: Encola el entrenamiento
    WK->>M: Registra el candidato y sus métricas
    E->>P: Revisa y aprueba
    P->>A: POST /internal/modelos/{version}/promover
    A->>A: Carga la nueva versión en producción
```

---

## 6. Despliegue

| Contenedor | Rol |
|---|---|
| `conecta-web` | Frontend Next.js |
| `conecta-api` | Backend FastAPI |
| `conecta-worker` | Copias, colas, correos, reentrenamiento |
| `redis` | Cola de tareas y caché |
| `postgres` | Base de datos (servicio administrado en producción) |
| `mlflow` | Seguimiento de modelos (acceso con login solo para el equipo) |

- **Ambientes:** desarrollo, pruebas (*staging*) y producción, cada uno con su base de datos.
- **CI/CD:** en cada cambio se ejecutan pruebas, lint y migraciones en pruebas; el despliegue a producción requiere aprobación.
- **Monitoreo:** logs centralizados, métricas de la API (latencia y errores), alertas si fallan las copias del SGT o del Panel y alertas de costo del LLM.

---

## 7. Decisiones pendientes

| Tema | Opciones |
|---|---|
| Proveedor del LLM | A definir según costo, calidad en español y política de datos |
| Nube y región | Dónde se alojan los datos de salud (requisitos de la Ley N.º 29733) |
| Librería de workers | Celery o arq |
| Contactos de centros solo con Conecta | ¿Solo correo, o también se ven en la versión limitada del SGT? |
| Orden de las sedes en las recomendaciones | Cercanía, edad o aleatorio entre empates, para no favorecer siempre a los mismos centros |
| Plazos de conservación de datos | A definir con asesoría legal |

Más detalle sobre el modelo, las reglas clínicas, el agente y los aspectos legales: `docs/consideraciones_app_tamizaje.md`.
