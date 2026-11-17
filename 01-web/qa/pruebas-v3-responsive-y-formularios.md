# Pruebas v3 · responsive, mecánicas y formularios
*01-web · qa + programador · 17/11/2026*

**Web publicada (prototipo):** https://rosa-ondono-prototipo.netlify.app
- Lleva `noindex` para que Google no la indexe.
- Las URLs antiguas redirigen con 301.

## Resultado
| Bloque | Resultado |
|---|---|
| Rastreo: 73 páginas, 2.914 enlaces internos y anclas, H1, title, description, JSON-LD y `alt` | ✅ sin incidencias |
| Responsive: 13 tamaños × 12 páginas | ✅ sin scroll horizontal, sin elementos fuera de pantalla, objetivos táctiles ≥ 24 px y letra ≥ 12 px |
| Mecánicas: 77 pruebas automáticas en iPhone 13 táctil y en escritorio | ✅ 77/77 |
| Accesibilidad: axe-core WCAG 2.2 AA en inicio, área, ficha, reservar y regalar | ✅ 0 incidencias |
| Envío real en la web publicada (móvil) | ✅ Llegó a Netlify Forms y a Supabase, y se generó el mensaje de WhatsApp. La prueba se borró después |

**Tamaños probados (px):**
- Móvil: 320×568, 360×740, 375×667, 390×844, 414×896 y 430×932.
- Tableta: 768×1024, 820×1180 y 1024×768.
- Escritorio: 1280×800, 1440×900 y 1920×1080.
- Móvil en horizontal: 844×390.

## Errores encontrados y corregidos
1. **Scroll horizontal en móvil en las páginas de área.** El índice de categorías deslizable ensanchaba la rejilla. Arreglado con `min-width: 0` en las columnas.
2. **Title duplicado** entre la ficha y la landing de la valoración integral. Ahora solo existe la landing y las tarjetas enlazan a ella.
3. **5 meta descriptions por debajo de 70 caracteres.** Se completan automáticamente sin pasar de 160.
4. **Objetivos táctiles por debajo de 24 px** (casillas de privacidad y «Configurar cookies»). Ampliados.
5. **Etiquetas de 11,8 px.** Subidas a 12,8 px.
6. **WhatsApp:** `window.open(..., "noopener")` siempre devuelve `null`, así que la web creía que no se había abierto. Corregido.
7. **Vista previa:** registraba formularios duplicados en Netlify. Ahora solo se registran los de `/reservar/` y `/regalar/`.

## Optimización responsive aplicada
- **Tipografía y botones:**
  - tipografía fluida con `clamp()` y corte de palabras largas (`hyphens`);
  - cabecera más baja en móvil (66 px);
  - botones a ancho completo en móvil.
- **Carruseles deslizables** con *scroll-snap* en móvil para «Nuestro universo» y «Los más pedidos», más el índice de categorías deslizable.
- **Pantallas táctiles y iPhone:**
  - sin efectos *hover* en táctil;
  - zonas seguras del iPhone (`viewport-fit=cover`, `env(safe-area-inset-*)`);
  - campos de 16 px para que iOS no haga zoom.
- **Formulario de regalo:** en móvil, la vista de la tarjeta aparece antes del formulario.
- **Móvil en horizontal:** la portada cabe en una pantalla.
- **Menú móvil:** bloquea el scroll del fondo, se cierra con Escape y mantiene el foco dentro.

## Formularios: cómo llega la información
Para enviar, cada formulario exige **nombre y teléfono o email**, al menos uno de los dos. Lo controlan tanto la web como la base de datos.

Al pulsar «Enviar solicitud» ocurren tres cosas a la vez:
1. **Email (Netlify Forms):**
   - La solicitud queda en Netlify y Netlify envía un aviso por email.
   - ⚠️ **Falta un paso en el panel de Netlify:** Forms → Form notifications → Add notification → Email notification. En el plan gratuito, el destinatario tiene que ser miembro del equipo de Netlify (hoy, la cuenta del titular).
2. **Copia en Supabase:** tablas `solicitudes_reserva` y `solicitudes_regalo`.
3. **WhatsApp:**
   - Se abre WhatsApp con el mensaje ya redactado y dirigido al **691 315 622** (`config.js` → `whatsapp`). La persona solo tiene que pulsar «Enviar».
   - El envío 100 % automático, sin pulsar nada, exige la API de WhatsApp Business (Meta), con una cuenta verificada y un token. Es el siguiente paso si se quiere.

## Cómo volver a lanzar las pruebas
Scripts de Playwright y axe-core usados: `auditoria.js` (rastreo y responsive) y `mecanicas.js` (77 pruebas). Se ejecutan contra `python3 -m http.server` en `prototipo/sitio`.
