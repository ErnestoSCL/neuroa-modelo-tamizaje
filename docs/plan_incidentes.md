# Plan de respuesta a incidentes de seguridad

Versión 1.0 · Conecta · Una página para tener a mano

**Incidente** = cualquier acceso, pérdida, cambio o divulgación no autorizada de datos personales, o la sospecha de que ocurrió. Ejemplos: base de datos expuesta, credencial filtrada, correo enviado a quien no debía, laptop perdida con acceso a producción.

**Regla de oro:** ante la duda, se trata como incidente. El reloj de **48 horas** empieza cuando alguien del equipo se entera.

## Quién hace qué

| Rol | Persona | Contacto | Hace |
|---|---|---|---|
| Coordinador y oficial de datos | Ernesto Saniel Castro Lozano | Celular en la página de Notion · correo de privacidad pendiente hasta tener dominio | Decide si es incidente, notifica a la ANPD y a los padres, lleva el registro |
| Líder técnico | Zahir Mauricio Aredo Vejarano | Celular en la página de Notion | Contiene, investiga y corrige |
| Respaldo | Jania Cecilia Salirrosas Morillo | Celular en la página de Notion | Reemplaza a cualquiera de los dos si no responde en 1 hora |

Cualquiera que detecte algo avisa **de inmediato** al coordinador por llamada, no solo por mensaje.

## Pasos

| Hora | Paso | Qué hacer |
|---|---|---|
| 0–4 | **1. Contener** | Cortar el acceso: rotar la credencial o clave filtrada en Key Vault, bloquear la cuenta afectada, cerrar la regla de red o detener el servicio. **No borrar** registros ni evidencia |
| 4–24 | **2. Evaluar** | Qué datos, de cuántas cuentas, si incluye datos de salud de niños, desde cuándo, si los datos salieron o solo quedaron expuestos. Usar los logs de Azure y de `pgaudit` |
| antes de 48 | **3. Notificar a la ANPD** | Siempre que haya datos personales afectados, aunque ya esté resuelto. Canal: [verificar: mesa de partes virtual del Ministerio de Justicia o el canal que indique la ANPD]. Contenido abajo |
| antes de 48 | **4. Avisar a los padres** | Si el incidente puede afectar sus derechos (siempre que haya datos de salud). Correo individual, sin datos de salud en el texto |
| antes de 24 | **5. Avisar a los centros** | Si se afectaron datos del SGT: como encargado, Neuroa avisa al centro en 24 horas (cláusula 6.2 del convenio) |
| después | **6. Cerrar** | Corregir la causa, registrar el incidente y lo aprendido, y actualizar este plan si hace falta |

## Qué decir en la notificación a la ANPD

1. Responsable: Ernesto Saniel Castro Lozano (Neuroa), RUC 10721914548, banco "Usuarios y evaluaciones de Conecta" ([código]).
2. Qué pasó, cuándo ocurrió y cuándo se detectó.
3. Datos afectados y número aproximado de titulares; si hay datos sensibles de menores.
4. Posibles consecuencias para los titulares.
5. Medidas tomadas y previstas.
6. Contacto: oficial de datos, [privacidad@dominio].

## Correo a los padres (modelo)

> **Asunto:** Aviso de seguridad sobre su cuenta de Conecta
>
> El [fecha] detectamos [qué pasó, en una frase]. Los datos que pudieron verse afectados son [datos]. Ya [medida tomada].
>
> Le recomendamos [cambiar su contraseña / estar atento a correos que pidan sus datos]. Neuroa nunca le pedirá su contraseña.
>
> Si tiene preguntas, escríbanos a [privacidad@dominio]. Lamentamos lo ocurrido.

## Registro

Todo incidente, aunque no se notifique, se anota en el registro de incidentes (fecha, qué pasó, datos, decisión de notificar y por qué, medidas). Se guarda al menos [plazo, verificar con el asesor].

**Ensayo:** una vez al año, simular un incidente y seguir este plan.
