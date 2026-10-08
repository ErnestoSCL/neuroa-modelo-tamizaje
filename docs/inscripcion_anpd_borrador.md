# Borrador: inscripción del banco de datos de Conecta ante la ANPD

Respuestas preparadas para el formulario de inscripción del **Registro Nacional de Protección de Datos Personales**. Se basan en `datos_y_privacidad.md` y `arquitectura_conecta.md`.

Versión 1.0 · 2026-10-02

> El formulario oficial puede ordenar o nombrar los campos de otra forma. Este borrador reúne las respuestas para copiarlas; hay que revisarlo con el asesor legal antes de enviarlo. Los campos entre corchetes `[ ]` los completa la empresa.

---

## 1. Cómo es el trámite

| Tema | Detalle |
|---|---|
| Dónde | En línea, en la plataforma **SIPDP** del Ministerio de Justicia: [sipdp.minjus.gob.pe](https://sipdp.minjus.gob.pe/sipdp-virtual/public/login.xhtml). Ficha del trámite en [gob.pe](https://www.gob.pe/8060-inscribir-banco-de-datos-en-el-registro-nacional-de-proteccion-de-datos-personales) |
| Costo | **Gratuito** (D.S. 016-2024-JUS) |
| Aprobación | **Automática**, sujeta a fiscalización posterior: lo que se declara debe ser cierto y estar implementado |
| Requisitos | 1) Formulario de inscripción. 2) Si el titular es una empresa: documento que acredite las **facultades del representante legal** (por ejemplo, la vigencia de poder). Si es una persona natural: su DNI **[verificar en el SIPDP]** |
| Pasos | Crear un usuario en el SIPDP, acreditar la representación, registrar un correo de contacto, llenar el formulario y enviarlo |
| Consultas | (01) 204-8020, anexo 2410, de lunes a viernes |

**Antes de empezar:**

- **Hoy:** el titular es el fundador o fundadora como **persona natural con RUC 10**. Las obligaciones y posibles multas recaen sobre esa persona.
- **Cuando se constituya la empresa (RUC 20):** el titular pasa a ser la empresa; se inscribe a su nombre o se actualiza la inscripción. Ver `datos_y_privacidad.md`, sección 16.
- La plataforma ya debe tener implementado lo que se declara (consentimiento, medidas de seguridad, canal ARCO). Lo ideal es inscribir **poco antes del lanzamiento**, con la configuración de Azure ya hecha.
- Si algo cambia (un país nuevo, una finalidad nueva, un tipo de dato nuevo), hay que **actualizar** la inscripción.

---

## 2. Bancos de datos a inscribir

| Banco | ¿Se inscribe? | Motivo |
|---|---|---|
| **Usuarios y evaluaciones de Conecta** | **Sí** | Neuroa es el titular: cuentas de padres, evaluaciones y resultados |
| Pacientes y citas en el SGT | **No por Neuroa** | El titular es cada centro; Neuroa es encargado. Cada centro inscribe su propio banco |
| Contactos de los centros clientes (Panel Startup) | **Evaluar** | Nombres, correos y teléfonos de las personas de contacto de cada centro son datos personales. Probablemente es un banco aparte, "Clientes", de riesgo bajo |
| Personal de la startup | **Evaluar** | Si hay trabajadores o practicantes con planilla o contrato, ese banco también se inscribe |

El resto de este borrador cubre el banco **Usuarios y evaluaciones de Conecta**.

---

## 3. Respuestas del formulario

### 3.1 Titular del banco de datos

| Campo | Respuesta |
|---|---|
| Titular | Hoy: [nombre del fundador o fundadora], persona natural con negocio. Más adelante: [razón social de la empresa] |
| Documento | Hoy: [RUC 10] y [DNI]. Más adelante: [RUC 20] |
| Domicilio | [Dirección fiscal] |
| Representante legal | Solo si el titular es una empresa: [nombre, DNI] |
| Correo de contacto | [privacidad@dominio] |
| Oficial de datos personales | [Nombre y correo] (ver `guia_oficial_datos.md`) |

### 3.2 Identificación del banco

| Campo | Respuesta |
|---|---|
| Denominación | Usuarios y evaluaciones de Conecta |
| Tipo | Privado |
| Descripción | Datos de los padres, madres o tutores que usan la plataforma Conecta y de las evaluaciones de tamizaje de desarrollo de sus hijos e hijas |

### 3.3 Finalidad y usos previstos

1. Calcular un **tamizaje orientativo** de señales compatibles con el trastorno del espectro autista (TEA) a partir de un cuestionario respondido por el padre, madre o tutor (Q-CHAT-10 y preguntas complementarias), con apoyo de sistemas de inteligencia artificial. No es un diagnóstico.
2. Gestionar la cuenta del usuario y guardar el historial de sus evaluaciones.
3. Mostrar terapias y centros terapéuticos afiliados que ofrecen esas terapias.
4. Cuando un centro afiliado registra al usuario como paciente: preguntarle si llegó por la plataforma y, con su confirmación, informarlo al centro y, si lo autoriza, compartir con ese centro el resultado del tamizaje.
5. Con consentimiento expreso: recibir de ese centro el resultado de la evaluación profesional para mejorar la precisión de la herramienta.
6. Con consentimiento: usar datos anonimizados para mejorar el modelo y para investigación.
7. Generar estadísticas agregadas y anónimas de uso para los centros afiliados.
8. Seguridad de la plataforma y atención de los derechos de los titulares.

### 3.4 Tipos de datos

| Categoría | Datos | ¿Sensible? |
|---|---|---|
| Identificación y contacto del usuario | Correo electrónico (usuario de la cuenta). No se recogen nombre ni teléfono | No |
| Credenciales | Contraseña, guardada como hash | No |
| Características del niño o niña | Edad en años, sexo | No (pero son datos de un **menor de edad**) |
| **Salud** | Respuestas sobre el desarrollo del niño (cuestionario Q-CHAT-10), dificultades de habla, aprendizaje, desarrollo, conducta y ansiedad, condición genética diagnosticada, antecedente familiar de autismo, resultado del tamizaje, diagnóstico confirmado por un centro (con consentimiento) | **Sí** |
| Datos técnicos | Dirección IP, navegador, fecha y hora de acceso (logs de seguridad) | No |

**Datos de menores de edad:** sí. Titulares menores de 14 años; el consentimiento lo da quien ejerce la patria potestad o la tutela.

**Datos que no se recogen:** nombre, DNI ni foto del niño o niña; DNI del padre; ubicación exacta.

### 3.5 Origen y procedimiento de obtención

| Origen | Procedimiento |
|---|---|
| El propio titular (padre, madre o tutor) | Formulario web de la plataforma, previo consentimiento expreso con casillas no premarcadas por cada finalidad |
| Centros terapéuticos afiliados | Aviso de que registraron al usuario como paciente (correo), y diagnóstico confirmado solo si el padre lo autorizó (finalidades 4 y 5) |

### 3.6 Sistema de tratamiento

| Campo | Respuesta |
|---|---|
| Tipo | **Automatizado** (sistema informático), sin soporte en papel |
| Uso de inteligencia artificial | Sí. Un modelo de aprendizaje automático estima la probabilidad y un modelo de lenguaje redacta la explicación. El resultado es orientativo; no hay decisiones automatizadas con efectos jurídicos |

### 3.7 Ubicación física del banco de datos

| Campo | Respuesta |
|---|---|
| Ubicación | Servicio en la nube **Microsoft Azure**, región **Brazil South (São Paulo, Brasil)** |
| Proveedor (encargado del tratamiento) | Microsoft Corporation, con su contrato de protección de datos (Microsoft Products and Services Data Protection Addendum) |

### 3.8 Encargados del tratamiento

| Encargado | Servicio | País |
|---|---|---|
| Microsoft (Azure) | Alojamiento, base de datos, respaldos, monitoreo y servicio de inteligencia artificial (Azure OpenAI) | Brasil |
| [Proveedor de correo] | Envío de correos de la cuenta, sin datos de salud | [País] |

### 3.9 Transferencias

| Tipo | Destinatario | País | Finalidad | Base |
|---|---|---|---|---|
| Nacional | Centro terapéutico que registró al usuario como paciente | Perú | Confirmar que llegó por la plataforma y, si lo autoriza, compartir el tamizaje | Consentimiento expreso del usuario en cada vínculo |
| **Internacional (flujo transfronterizo)** | Microsoft (como encargado) | **Brasil** | Alojamiento y procesamiento | Consentimiento informado y contrato con cláusulas de protección **[verificar con el asesor si se requiere algo más]** |

**Importante:** si se usa un despliegue *Global* de Azure OpenAI o respaldos geo-redundantes, aparecen otros países (EE. UU. y otros). La configuración recomendada (`datos_y_privacidad.md`, sección 5.2) mantiene todo en Brasil. Hay que declarar **lo que realmente esté configurado**.

### 3.10 Medidas de seguridad

- Cifrado en tránsito (HTTPS/TLS 1.2 o superior) y en reposo (base de datos y respaldos).
- Base de datos sin acceso público, en red privada.
- Acceso del personal con autenticación multifactor, permisos mínimos y acceso temporal a producción.
- Contraseñas de los usuarios guardadas con hash robusto (argon2).
- Secretos y claves en un almacén seguro (Azure Key Vault).
- Registro y auditoría de accesos administrativos.
- Logs técnicos sin datos de salud, conservados 90 días.
- Respaldos dentro de Brasil.
- Entornos de desarrollo solo con datos sintéticos.
- Plan de respuesta a incidentes con notificación a la Autoridad y a los titulares en 48 horas.

### 3.11 Conservación

| Dato | Plazo |
|---|---|
| Cuenta del usuario | Mientras esté activa; se elimina a pedido |
| Evaluaciones y resultados | Mientras la cuenta esté activa o hasta 2 años sin actividad; luego se anonimizan o eliminan |
| Logs técnicos | 90 días |

### 3.12 Ejercicio de derechos (ARCO)

- Desde la cuenta: opción "Eliminar mi cuenta".
- Por correo a [privacidad@dominio], atendido por el oficial de datos personales.
- Plazos de respuesta según el reglamento.

---

## 4. Lista de verificación antes de enviar

- [ ] Titular definido: hoy, el fundador con RUC 10; más adelante, la empresa con RUC 20 y vigencia de poder.
- [ ] Oficial de datos designado y correo de privacidad activo.
- [ ] Azure configurado como se declara: región Brazil South, LLM regional, respaldos sin geo-redundancia.
- [ ] Consentimiento por finalidad implementado en la app.
- [ ] Política de privacidad publicada, coherente con este formulario.
- [ ] Opción "Eliminar mi cuenta" funcionando.
- [ ] Revisión del asesor legal.
- [ ] Guardar la constancia de inscripción y su código; publicarlo en la política de privacidad.
