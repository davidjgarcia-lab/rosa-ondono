# Web v3.1 · construcción y pruebas
*01-web · 18/11/2026 · sobre la dirección de arte v3 aprobada (`../diseno/direccion-arte-v3/`)*
**Enlace:** https://rosa-ondono-prototipo.netlify.app

## Qué cambia
- **Cabecera:**
  - tres columnas a todo el ancho: logo a la izquierda, menú centrado y Regalar/Reservar a la derecha;
  - transparente sobre la portada y marfil al bajar.
- **Portada:**
  - tres escenas (Cuídate, Conecta, Siente), cada una con foto, titular que entra línea a línea y botones;
  - avanza cada 7 s y se para con el ratón encima, con el foco o con el botón de pausa;
  - el isotipo entra con una cortinilla;
  - sin recuadro de dirección: en su lugar va una tarjeta «¿Por dónde empiezo? · Valoración integral».
- **Secciones, cada una con su forma:**
  - acordeón de áreas;
  - método en escena fija ligada al scroll (GSAP ScrollTrigger, solo en escritorio);
  - carta editorial con foto que sigue al cursor;
  - Conócenos con cita grande, paralaje y contadores;
  - mosaico del centro y marquesina de opiniones;
  - reserva rápida en panel oscuro con tarjeta regalo que se inclina.
- **WhatsApp:** botón morado de 44 px con la etiqueta «Escríbenos» al pasar el ratón.
- **Insignia «Powered by Netlify»:** la inyecta el plan gratuito y queda oculta por CSS (`#nl-badge-frame`).
- **Reserva con hora exacta:**
  - de lunes a viernes, de 9:00 a 19:00;
  - huecos de 60 minutos o lo que dure el tratamiento si figura en el catálogo;
  - las horas ocupadas en el Google Calendar del centro salen tachadas.
- **Avisos que manda la propia web** (funciones de Netlify en `../prototipo/netlify/`):

| Ruta | Qué hace |
|---|---|
| `/api/huecos` | Lee la disponibilidad del calendario (freeBusy) |
| `/api/reserva` | Comprueba que la hora sigue libre, crea el evento «Petición de reserva · tratamiento · nombre» como *pendiente* y manda el WhatsApp «📅 Petición de reserva · día X a las xx:xx» |
| `/api/regalo` | Manda el WhatsApp de la petición de tarjeta regalo |

  - El email (Netlify Forms) y la copia en Supabase se mantienen.
  - La clienta ya no tiene que pulsar «Enviar» en WhatsApp. Si fallan todos los canales, se le ofrece WhatsApp como alternativa.
- **Supabase:** migración `005_hora_reserva.sql`, que añade la columna `hora`.

## Pruebas (Playwright, 18/11/2026)
| Prueba | Resultado |
|---|---|
| 1440 · 1024 · 768 · 390 px: capturas por sección (`capturas-v3-*.jpg`) | Sin scroll horizontal ni errores de JS |
| 320 px en inicio, reservar, regalar, área, ficha y conócenos | Sin scroll horizontal |
| Reserva rápida → `/reservar/?servicio&fecha&hora` | Día y hora llegan preseleccionados |
| Enviar vacío | Errores en nombre, contacto y privacidad |
| Envío completo (con nombre muy largo) | «Petición enviada · Presoterapia · lunes 30 de noviembre a las 11:00» |
| Carrusel | Avanza Cuídate → Conecta → Siente → Cuídate; se para con ratón, foco y botón (WCAG 2.2.2) |
| Escenas ocultas | Sus enlaces quedan fuera del tabulador |
| Marquesina | Se detiene al tocarla o con su botón (visible al tabular) |
| «Reducir movimiento» | Sin avance automático, sin escena fija y contenido visible sin animación |
| Sin JavaScript | Portada y secciones visibles |
| Vista previa en un solo archivo | La reserva rápida pasa la hora al formulario |
| En vivo: `/api/huecos` | Devuelve las horas; domingo → 400 |
| En vivo: `/api/reserva` | Valida datos (400 si faltan) |
| En vivo: insignia de Netlify | `display: none` |

**Revisión de animaciones:**
- Solo se animan `transform`, `opacity` y `clip-path`, con una excepción consciente: el ancho de los paneles del acordeón (`flex-grow`, cuatro elementos).
- La carta pasó de animar el `padding` a usar `transform`.
- Duraciones: 160, 260, 700 y 1200 ms, más 7 s por escena.
- Nada bloquea la interacción.
- GSAP (unos 45 KB comprimido) se carga solo en la home. Sin Three.js.

## Pendiente para activar los avisos (variables de entorno en Netlify)
| Variable | Valor |
|---|---|
| `CALLMEBOT_PHONE` | `34650202315` (prueba) → número del centro en producción |
| `CALLMEBOT_APIKEY` | Clave que CallMeBot envía al activar ese número |
| `GOOGLE_SA_EMAIL` · `GOOGLE_SA_KEY` · `GOOGLE_CALENDAR_ID` | Cuenta de servicio de Google con acceso al calendario profesional del centro |

Mientras falten, la web funciona igual: muestra las horas sin consultar la agenda y avisa por email y Supabase. En el resultado del prototipo pone «pendiente de conectar».
