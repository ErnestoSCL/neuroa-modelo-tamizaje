# Guía del oficial de datos personales de Neuroa

Qué hace, cuánto tiempo le toma y qué tiene que tener listo la persona responsable de la privacidad en la startup.

Versión 1.0 · 2026-10-02

---

## 1. Qué es

El **oficial de datos personales (ODP)** es la persona que vela por que Neuroa cumpla la Ley N.º 29733 y su reglamento (D.S. 016-2024-JUS). Es el contacto de la Autoridad Nacional de Protección de Datos Personales (ANPD), de los padres que usan Conecta y de los centros.

| Pregunta | Respuesta |
|---|---|
| ¿Es obligatorio? | Lo exige el reglamento a quienes tratan **datos sensibles como parte de su actividad**, como Conecta con datos de salud de niños |
| ¿Desde cuándo? | Hay plazos según el tamaño de la empresa, contados desde la publicación del reglamento (30-11-2024): **pequeña empresa** (ventas de 150 a 1700 UIT al año) hasta **noviembre de 2027**; **microempresa** (hasta 150 UIT) hasta **noviembre de 2028** **[verificar con el asesor]**. **Recomendación:** designarlo desde el lanzamiento; cuesta poco y ordena todo lo demás |
| ¿Tiene que ser exclusivo? | **No.** Puede tener otras funciones en la empresa, o ser una persona externa |
| ¿Qué perfil necesita? | Conocimientos y práctica en protección de datos **debidamente acreditados**. En la práctica: un curso o diplomado en protección de datos personales (hay opciones cortas y virtuales en el Perú) |
| ¿Quién puede ser? | Alguien del equipo con criterio y tiempo, por ejemplo el fundador o un desarrollador senior, o un abogado externo por horas |
| ¿Cuánto tiempo toma? | Al inicio, **unas 10 a 15 horas** para dejar todo listo. Luego **2 a 4 horas al mes**, más lo que tome un incidente si ocurre |

---

## 2. Funciones

### 2.1 Antes del lanzamiento (una sola vez)

| # | Tarea | Documento de apoyo |
|---|---|---|
| 1 | Leer `datos_y_privacidad.md` y aclarar dudas con el equipo técnico | `datos_y_privacidad.md` |
| 2 | Coordinar la revisión del asesor legal (13 preguntas preparadas) | `datos_y_privacidad.md`, sección 14 |
| 3 | Aprobar el texto final del consentimiento y la política de privacidad | Secciones 6 y 7 |
| 4 | Inscribir el banco de datos en el SIPDP y guardar la constancia | `inscripcion_anpd_borrador.md` |
| 5 | Crear y atender el correo de privacidad (por ejemplo, privacidad@dominio) | — |
| 6 | Archivar los contratos de protección de datos de Microsoft y del proveedor de correo | Sección 13 |
| 7 | Revisar el contrato modelo con los centros (cláusulas de datos) | Sección 3 |
| 8 | Conocer y practicar una vez el plan de incidentes | Sección 11.3 |
| 9 | Hacer firmar acuerdos de confidencialidad al equipo con acceso a producción | Sección 11.2 |

### 2.2 Día a día

**Atender a los padres (derechos ARCO):**

1. Registrar cada solicitud: fecha, quién la pide, qué pide y cuándo vence.
2. Comprobar que quien escribe es el dueño de la cuenta: el pedido debe venir del correo registrado, o se le pide confirmar desde ese correo.
3. Resolver con el equipo técnico y responder dentro del plazo:

| Pedido | Qué hacer | Plazo |
|---|---|---|
| "Quiero saber qué datos tienen de mí" (acceso) | Exportar la cuenta, las evaluaciones, los consentimientos y los envíos a centros | ~20 días hábiles **[verificar]** |
| "Quiero corregir mi correo" (rectificación) | Indicarle cómo cambiarlo desde la cuenta, o hacerlo por él | ~10 días hábiles **[verificar]** |
| "Quiero que borren mis datos" (cancelación) | Indicarle la opción "Eliminar mi cuenta", o ejecutarla. Informarle qué centros recibieron su resultado, para que les pida la eliminación a ellos | ~10 días hábiles **[verificar]** |
| "No quiero que usen mis datos para mejorar el modelo" (oposición) | Revocar la finalidad desde la cuenta, o hacerlo por él | ~10 días hábiles **[verificar]** |

4. Guardar la respuesta enviada como prueba.

**Revisar cambios del producto:** el equipo le consulta **antes** de:

- agregar una pregunta o un dato nuevo al formulario;
- usar los datos para algo nuevo;
- contratar un proveedor nuevo que reciba datos;
- cambiar de región o de tipo de despliegue en Azure, o de modelo de LLM;
- compartir datos con alguien nuevo.

Si el cambio es relevante, actualiza `datos_y_privacidad.md`, la política de privacidad y, si corresponde, la inscripción en el SIPDP.

**Vigilar las prácticas internas:** que nadie copie datos reales de padres o niños a Notion, hojas de cálculo, WhatsApp o correos personales, y que los entornos de prueba usen solo datos sintéticos.

### 2.3 Si hay un incidente (filtración, acceso indebido, pérdida de datos)

| Momento | Qué hace el oficial |
|---|---|
| Al enterarse | Activa el plan: avisa al líder técnico para contener y anota la hora exacta en que se conoció el incidente |
| Primeras 24 horas | Con el equipo técnico: qué datos, cuántas personas, si hay datos de salud de niños y qué riesgo corren |
| **Antes de 48 horas** | **Notifica a la ANPD**, aunque el incidente ya esté resuelto |
| **Antes de 48 horas** | Si afecta los derechos de los padres, **les avisa**: qué pasó, qué datos y qué pueden hacer |
| Si involucra datos del SGT | Avisa a los centros afectados, porque Neuroa es su encargado |
| Después | Documenta el incidente, la causa y las medidas tomadas, **aunque no se haya notificado** |

Plantilla del aviso a los padres (a validar con el asesor):

> Hola. El [fecha] detectamos [qué pasó, en una frase]. Los datos involucrados son [cuáles]. Ya [qué se hizo para detenerlo]. Le recomendamos [qué hacer, por ejemplo cambiar su contraseña]. Si tiene dudas, escríbanos a [privacidad@dominio]. Lamentamos lo ocurrido.

### 2.4 Periódico

| Frecuencia | Tarea |
|---|---|
| Mensual | Revisar el registro de solicitudes ARCO y los plazos |
| Trimestral | Revisar con el líder técnico quién tiene acceso a producción y quitar los accesos que sobren |
| Semestral | Actualizar `datos_y_privacidad.md`; revisar las métricas de sesgo por sexo y edad con el equipo de ML |
| Anual | Simulacro de incidente; capacitación corta al equipo; revisar los contratos de proveedores; renovar su propia formación |

---

## 3. Registros que debe mantener

| Registro | Contenido | Dónde |
|---|---|---|
| Solicitudes ARCO | Fecha, solicitante, pedido, respuesta y fecha de respuesta | Hoja privada con acceso restringido. **Sin datos de salud** |
| Incidentes | Fecha, descripción, datos y personas afectadas, medidas, notificaciones hechas | Documento privado |
| Proveedores | Nombre, servicio, datos que recibe, país, contrato firmado | `datos_y_privacidad.md`, sección 13 |
| Cambios del producto revisados | Fecha, cambio, decisión | Notas o issue en el repositorio |
| Constancias | Inscripción en el SIPDP, designación del oficial, capacitaciones | Carpeta de cumplimiento |

---

## 4. Lo que **no** hace el oficial

- No es el abogado de la empresa: identifica las dudas legales y las lleva al asesor.
- No implementa la seguridad técnica: la pide y la verifica, y la ejecuta el equipo de desarrollo.
- No decide solo: si un cambio de producto choca con la privacidad, lo eleva al fundador o fundadora con una recomendación.

---

## 5. Para designarlo

1. Elegir a la persona y confirmar que tiene, o tomará pronto, una formación acreditada en protección de datos.
2. Dejar constancia escrita de la designación (un acta o una carta firmada por el representante legal) con fecha y funciones; esta guía puede ir como anexo.
3. Publicar su contacto (puede ser el correo de privacidad) en la política de privacidad.
4. Registrarlo como contacto en el SIPDP si la plataforma lo pide **[verificar]**.

**Fuentes:** [LP Derecho, D.S. 016-2024-JUS](https://lpderecho.pe/reglamento-ley-proteccion-datos-personales-decreto-supremo-016-2024-jus/) · [Caro & Asociados, plazos del oficial de datos](https://ccfirma.com/empresas-deberan-nombrar-a-su-oficial-de-datos-personales-o-enfrentar-multas-decreto-supremo-no-016-2024-jus/) · [El Peruano, cuándo nombrar un ODP](https://elperuano.pe/noticia/288028-suplemento-legal-juridica-tratas-datos-sensibles-o-grandes-volumenes-evalua-si-debes-nombrar-un-odp) · [EY, nuevo reglamento](https://www.ey.com/es_pe/insights/law/proteccion-datos-personales-peru-nuevo-reglamento)
