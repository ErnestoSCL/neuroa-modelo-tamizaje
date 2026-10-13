# Guía de implementación: mínimo legal de privacidad

Versión 1.0 · Cómo hacer las tareas del mínimo legal que no son un documento, sino algo que se configura o se programa.

| # | Tarea | Quién | Cuándo |
|---|---|---|---|
| 1 | Correo de privacidad | Fundador | Ya (5 minutos a 1 hora) |
| 2 | Casillas de consentimiento | Equipo de desarrollo | Al construir el formulario y la cuenta |
| 3 | Seguridad de la base de datos | Equipo de desarrollo | Al crear los recursos de Azure |

Textos que se usan aquí: `consentimiento.md`, `politica_privacidad.md` y `plan_incidentes.md`.

---

## 1. Correo de privacidad

**Para qué:** es el canal oficial para los derechos ARCO y para incidentes. Aparece en la política, el consentimiento, la inscripción ante la ANPD y el convenio con los centros.

**Cómo crearlo:**

1. Usar una dirección **del dominio de Neuroa**, no una de Gmail personal: `privacidad@[dominio]`. Transmite seriedad y no depende de una persona.
2. Elegir cómo crearla:

    | Opción | Cuándo conviene | Costo |
    |---|---|---|
    | Alias o grupo en Google Workspace o Microsoft 365 | Si el dominio ya usa uno de los dos | Incluido |
    | Buzón en Zoho Mail (plan gratuito) | Si el dominio no tiene correo todavía | Gratis **[verificar condiciones actuales]** |
    | Reenvío del dominio a un buzón existente (por ejemplo, Cloudflare Email Routing) | Solución rápida para empezar | Gratis; para responder desde `privacidad@` hay que configurar el envío aparte |

3. Darle acceso al oficial de datos (hoy, Ernesto) y a una persona de respaldo.
4. Activar la verificación en dos pasos en esa cuenta.

**Cómo atenderlo:**

- Revisarlo **al menos una vez por día hábil**.
- Responder primero con un acuse de recibo: "Recibimos su solicitud del [fecha]. Le responderemos dentro del plazo del Reglamento".
- Verificar la identidad: la solicitud debe venir del correo de la cuenta. Si no, pedir que escriba desde ese correo.
- Anotar cada solicitud en una hoja de registro con: fecha, derecho pedido, cuenta (id, no correo), respuesta y fecha de cierre. La hoja **no lleva datos de salud**.
- Los plazos corren en días hábiles desde que llega el correo **[verificar plazos exactos del reglamento: 20 días hábiles para acceso y 10 para el resto]**.

**Después de crearlo:** reemplazar `[privacidad@dominio]` en la política, el consentimiento, el plan de incidentes y los borradores de la ANPD y del convenio.

---

## 2. Casillas de consentimiento

**Requisito legal:** los datos de salud de un menor necesitan el consentimiento expreso de quien ejerce la patria potestad, con un registro que pruebe qué aceptó, cuándo y con qué texto. Una casilla no premarcada guardada en la base de datos cumple ese papel.

### 2.1 Qué ve el padre

| Pantalla | Finalidades | Texto |
|---|---|---|
| `/screening` | (a) calcular el tamizaje, (b) guardar en la cuenta. Necesarias | `consentimiento.md`, sección 1 |
| Al terminar las preguntas | (e) mejorar el modelo. Opcional | `consentimiento.md`, sección 2 |
| `/account` → "Mis autorizaciones" | (f) novedades. Opcional. Lista de todas y botón "Retirar" | `consentimiento.md`, secciones 3 y 5 |
| `/account/centers` (fase 2) | (c) vínculo, (d) resultado profesional. Opcionales | `consentimiento.md`, sección 4 |

**Reglas de interfaz:**

- Casillas reales (`<input type="checkbox">`), **sin marcar** al cargar la página. Nunca un solo botón "Acepto todo".
- El botón **[Empezar]** queda desactivado hasta marcar (a) y (b).
- El enlace a la política abre `/privacy` en una pestaña nueva, sin perder lo marcado.
- Accesible: cada casilla con su `<label>`, navegable con teclado.
- El estado de las casillas y las respuestas se guardan **solo en memoria** mientras el padre responde. Nada en `localStorage` ni `sessionStorage`.

### 2.2 Cómo se guarda

El consentimiento de `/screening` se da **antes** de que exista la cuenta. Para que la fecha quede registrada por el servidor:

1. Al pulsar **[Empezar]**, el frontend llama a `POST /consents` con las finalidades marcadas y la versión del texto.
2. El backend crea una **sesión de tamizaje** anónima, guarda el consentimiento con la hora del servidor y devuelve una cookie `httpOnly` con el id de la sesión.
3. Al crear la cuenta (`POST /auth/register`), el backend asocia a la cuenta los consentimientos de esa sesión.
4. Las autorizaciones posteriores, (e) y (f), se guardan con la cuenta ya creada.

**Tabla** (reemplaza la definición de `app.consents` en `arquitectura_conecta.md`): una fila por finalidad aceptada.

| Columna | Tipo | Detalle |
|---|---|---|
| `id` | uuid | |
| `parent_id` | uuid, puede ser nulo | Nulo hasta que se crea la cuenta |
| `screening_session_id` | uuid, puede ser nulo | Sesión anónima de `/screening` |
| `purpose` | enum | `screening`, `store_result`, `model_improvement`, `marketing`, `center_link`, `diagnosis_return` |
| `text_version` | texto | Por ejemplo, `consent-2026.1` |
| `center_link_id` | uuid, puede ser nulo | Solo para `center_link` y `diagnosis_return` |
| `granted_at` | timestamptz | Hora del servidor |
| `revoked_at` | timestamptz, puede ser nulo | Se llena al retirar |

**Reglas de la tabla:**

- **Nunca se borra ni se edita una fila**, salvo para llenar `revoked_at`. El usuario de base de datos de la API tiene permiso de `INSERT` y de `UPDATE (revoked_at)` solamente.
- Aceptar de nuevo después de retirar crea una fila nueva.
- Un texto nuevo crea una versión nueva. Si cambia el texto de una finalidad necesaria, al iniciar sesión se pide aceptar la versión nueva antes de seguir.
- Al eliminar la cuenta, las filas se conservan sin `parent_id` durante el plazo que indique el asesor legal, como prueba **[verificar plazo]**.

### 2.3 Qué controla el backend

| Acción | Condición |
|---|---|
| `POST /assessments` | Debe haber `screening` y `store_result` vigentes (sin `revoked_at`) con la versión actual del texto. Si no, responde 403 |
| Job de reentrenamiento | Solo usa evaluaciones cuya cuenta tenga `model_improvement` vigente |
| Envío de novedades | Solo a cuentas con `marketing` vigente |
| Compartir con un centro (fase 2) | Solo con `center_link` vigente para ese vínculo |

**Endpoints:**

| Endpoint | Para qué |
|---|---|
| `POST /consents` | Registrar una o más finalidades (con sesión anónima o con cuenta) |
| `GET /consents` | Listar las autorizaciones de la cuenta, para "Mis autorizaciones" |
| `DELETE /consents/{purpose}` | Retirar una finalidad opcional: llena `revoked_at` y aplica sus efectos (`consentimiento.md`, sección 5) |

### 2.4 Pruebas que deben pasar

- [ ] Las casillas cargan sin marcar.
- [ ] Sin (a) y (b) el botón [Empezar] no se activa, y `POST /assessments` responde 403 aunque se llame directo a la API.
- [ ] Cada finalidad aceptada genera una fila con versión y hora del servidor.
- [ ] Al crear la cuenta, los consentimientos de la sesión quedan con su `parent_id`.
- [ ] Retirar (e) excluye esas evaluaciones del siguiente extracto de entrenamiento.
- [ ] La API no puede borrar filas de `app.consents` (probar con su usuario de base de datos).
- [ ] Cambiar `text_version` de una finalidad necesaria obliga a aceptar de nuevo.

---

## 3. Seguridad de la base de datos

**Requisito:** sin acceso público, con verificación en dos pasos para el equipo, permisos mínimos y claves en Key Vault. Se configura **al crear** los recursos, porque algunas opciones no se pueden cambiar después.

### 3.1 Pasos en Azure

1. **Grupo de recursos aparte para producción** (`rg-conecta-prod`) en **Brazil South**. Desarrollo y pruebas, en otro grupo y solo con datos ficticios.
2. **Red privada:** crear una VNet con una subred para Container Apps y otra delegada a PostgreSQL.
3. **PostgreSQL Flexible Server** en Brazil South:
    - Conectividad: **acceso privado (integración con VNet)**. Se elige al crear el servidor y no se puede cambiar después.
    - Respaldos: redundancia **local o por zona**, **sin respaldo geo-redundante** (también se elige al crear). Retención de 14 días.
    - Autenticación: **Microsoft Entra ID** activado. La contraseña del administrador se guarda en Key Vault y solo se usa en emergencias.
    - Parámetros: `require_secure_transport = on` y `ssl_min_protocol_version = TLSv1.2`.
    - Auditoría: agregar `pgaudit` en `azure.extensions` y `shared_preload_libraries`, con `pgaudit.log = 'ddl,role'`. Enviar los logs a Log Analytics con una configuración de diagnóstico.
    - Activar **Microsoft Defender** para bases de datos relacionales de código abierto.
4. **Key Vault** en el mismo grupo:
    - Modelo de permisos **RBAC**, con eliminación temporal y **protección contra purga**.
    - Acceso solo desde la VNet (*private endpoint* o firewall).
    - La API lee los secretos con su **identidad administrada** y el rol "Key Vault Secrets User". Ninguna clave va en el código ni en variables de entorno sin Key Vault.
5. **Identidad de la API:** la Container App usa una identidad administrada, registrada como usuario de Entra en PostgreSQL. La API se conecta **sin contraseña**.
6. **Usuarios de la base de datos**, cada uno con lo mínimo:

    | Usuario | Permisos |
    |---|---|
    | API (identidad administrada) | Leer y escribir en los esquemas `app` y `catalog`; en `app.consents` solo `INSERT` y `UPDATE (revoked_at)`; sin permisos para cambiar la estructura |
    | Migraciones | Cambiar la estructura; se usa solo en el despliegue |
    | Analítica | Solo lectura de vistas anonimizadas |

7. **Acceso del equipo:**
    - Verificación en dos pasos **obligatoria** para todas las cuentas de Entra ID (valores predeterminados de seguridad o acceso condicional).
    - Nadie con rol de propietario permanente en producción. El día a día, con rol de lector. Los cambios, con un rol temporal: Privileged Identity Management si se tiene Entra ID P2, o un procedimiento equivalente (pedir, aprobar, quitar al terminar).
    - Una cuenta de emergencia con contraseña larga guardada fuera de línea.

### 3.2 Cómo comprobar que quedó bien

- [ ] `az postgres flexible-server show -g rg-conecta-prod -n <servidor> --query "{red:network.publicNetworkAccess, geo:backup.geoRedundantBackup, region:location}"` devuelve `Disabled`, `Disabled` y `brazilsouth`.
- [ ] Desde una computadora fuera de la VNet, la conexión a PostgreSQL falla.
- [ ] La API funciona sin ninguna contraseña de base de datos en su configuración.
- [ ] Un usuario del equipo sin rol temporal no puede leer secretos de Key Vault.
- [ ] Al iniciar sesión en Azure, todo el equipo pasa por la verificación en dos pasos.
- [ ] Los logs de `pgaudit` llegan a Log Analytics.
- [ ] Se hizo una restauración de prueba desde un respaldo.

Con estos puntos verificados, la inscripción ante la ANPD puede declarar las medidas de seguridad tal como están.
