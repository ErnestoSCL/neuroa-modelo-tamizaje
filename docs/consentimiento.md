# Textos de consentimiento de Conecta

Versión `consent-2026.1` · Para aprobación del equipo y revisión legal

Textos finales de cada pantalla donde Conecta pide autorización. Base: `datos_y_privacidad.md`, secciones 6.2 a 6.4. Cómo se implementan las casillas: `guia_implementacion_privacidad.md`, sección 2.

**Reglas para todas las pantallas:**

- Una casilla por finalidad, **ninguna marcada de antemano**.
- Las obligatorias dicen "(necesaria)"; las opcionales, "(opcional)".
- El botón para continuar se activa solo cuando las necesarias están marcadas.
- Cualquier cambio de texto crea una versión nueva (`consent-2026.2`, …).

---

## 1. Inicio del tamizaje (`/screening`)

Se muestra antes de la primera pregunta. Finalidades (a) y (b), necesarias.

> **Antes de empezar**
>
> Para calcular el resultado necesitamos sus respuestas sobre el desarrollo de su hijo o hija. Son datos de salud y los protegemos con especial cuidado.
>
> - No le pediremos el nombre de su hijo o hija.
> - Sus respuestas se procesan con inteligencia artificial en servidores de Microsoft Azure ubicados en Brasil.
> - El resultado es orientativo y **no es un diagnóstico**.
> - Para ver el resultado le pediremos crear una cuenta con su correo, donde quedará guardado.
> - No compartiremos sus datos con ningún centro sin que usted lo autorice.
>
> Responsable: Ernesto Saniel Castro Lozano (Neuroa), RUC 10721914548. Contacto: [privacidad@dominio].
>
> ☐ Soy padre, madre o tutor legal del niño o niña y autorizo el uso de mis respuestas para calcular el resultado del tamizaje, con ayuda de inteligencia artificial. *(necesaria)*
>
> ☐ Autorizo que el resultado se guarde en mi cuenta para verlo después. *(necesaria)*
>
> Al continuar, acepto la [Política de privacidad].
>
> **[Empezar]**

## 2. Al terminar el tamizaje (antes de crear la cuenta)

Finalidad (e), opcional.

> ☐ Autorizo usar mis respuestas, **sin datos que me identifiquen**, para mejorar el modelo y para investigación. *(opcional)*

## 3. En la cuenta (`/account`, sección "Mis autorizaciones")

Finalidad (f), opcional. Nunca se pide durante el tamizaje.

> ☐ Quiero recibir novedades de Neuroa por correo. *(opcional)*

La misma sección lista todas las autorizaciones vigentes, con su fecha, y un botón **[Retirar]** junto a cada opcional.

## 4. Vínculo con un centro (`/account/centers`) · Fase 2

Finalidades (c) y (d), opcionales. Solo cuando esta función exista.

> **[Centro]** lo registró como paciente.
>
> ☐ Sí, llegué a este centro gracias a Neuroa.
>
> ☐ Quiero compartir con **[Centro]** el tamizaje del **[fecha]**. *(opcional)*
>
> ☐ Autorizo que **[Centro]** informe a Neuroa el resultado de la evaluación profesional, para mejorar la precisión de la herramienta. *(opcional)*
>
> **[Confirmar]** · [No reconozco este centro]

## 5. Mensajes al retirar una autorización

| Finalidad | Mensaje de confirmación |
|---|---|
| (e) Mejorar el modelo | "Listo. Sus respuestas ya no se usarán en futuros entrenamientos. Las que ya se usaron estaban anonimizadas y no se pueden separar." |
| (f) Novedades | "Listo. Ya no le enviaremos novedades." |
| (c) Vínculo con un centro | "Listo. Ya no compartiremos nada con [Centro]. Si ya le envió su tamizaje, ese dato está en poder del centro; puede pedirle que lo elimine." |
| (d) Resultado profesional | "Listo. Ya no recibiremos resultados de [Centro] y eliminamos los que no estaban anonimizados." |

Las finalidades (a) y (b) no se retiran por separado: se retiran con "Eliminar mi cuenta".

## 6. Aprobación

- [ ] Aprobado por el equipo
- [ ] Revisado por el asesor legal
- [ ] Coincide con la política de privacidad publicada
