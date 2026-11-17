# Especificaciones técnicas de plantillas para redes · BORRADOR v0.1

> **Estado: BORRADOR. No apto para producción.** Fecha: 17/11/2026 · Autor: disenador-grafico · Valida: director-arte → qa.
> El manual de marca **no está aprobado**. Este documento fija solo lo que no depende del manual: formatos, zonas seguras, estructura, reglas y entrega. Todo lo que depende del manual aparece como **[PENDIENTE]** y no puede rellenarse por ningún agente.

## 0. Bloqueos y dependencias

| Dato | Estado | Quién lo resuelve | Afecta a |
|---|---|---|---|
| Vector original del isotipo (SVG/AI/EPS/PDF) | PENDIENTE del cliente | ejecutivo-cuentas | Avatar, firma, todas las plantillas |
| Color corporativo oficial: #701B78 (medido en el icono) frente a #8E1F5C (web actual) | PENDIENTE de confirmar | ejecutivo-cuentas → cliente | Todas |
| Pantone / CMYK del color corporativo | PENDIENTE | cliente / imprenta | Bono regalo impreso |
| Paleta secundaria y neutros (incluidos los fondos de pilar) | PENDIENTE | director-arte | Código de pilar |
| Tipografías (principal y secundaria) y licencias | PENDIENTE | director-arte | Todas |
| Área de respeto y tamaño mínimo del isotipo | PENDIENTE (manual §4) | director-arte + disenador-grafico | Todas |
| Versión monocroma negativa del isotipo | PENDIENTE (manual §4) | director-arte | Cualquier fondo oscuro o foto |
| Nº de colegiado del Dr. Roberth Bravo Pardo | PENDIENTE | cliente | Piezas de medicina estética |
| Nº de registro sanitario del centro | PENDIENTE | cliente | Piezas de medicina estética |
| Necesidad de autorización previa de publicidad sanitaria (Comunitat Valenciana) | PENDIENTE de verificar | cliente / asesor legal | Piezas de medicina estética |
| Condiciones, validez, importes/servicios y datos del emisor del bono regalo | PENDIENTE | cliente | Pieza de diciembre |

**Regla:** mientras sigan PENDIENTES el nº de colegiado y el nº de registro sanitario, **no se publica ninguna pieza de medicina estética**, aunque la plantilla esté lista.

---

## 1. Convenciones

- Unidades: px para piezas digitales (lienzo a 1× = tamaño de exportación); mm para impresión.
- Perfil de color: **sRGB IEC61966-2.1** en todo lo digital; **CMYK Coated FOGRA39** en impresión.
- Margen base del sistema: **90 px** en lienzos de 1080 px de ancho (≈ 8,3 %). Retícula de **6 columnas**, medianil **30 px**. Ritmo vertical en múltiplos de **10 px**. Provisional hasta que el manual fije la retícula.
- Las cifras de interfaz de las plataformas cambian con frecuencia. Valores revisados a noviembre de 2026; **verificar en cada plataforma antes de cada tanda de producción** (lo comprueba qa en una prueba real sin publicar o en una cuenta de pruebas).

---

## 2. Formatos, medidas y zonas seguras

### 2.1 Post de Instagram 4:5 · 1080 × 1350 px
- **Zona segura de contenido:** x 90–990, y 90–1260 (margen 90 px).
- **Vista de rejilla del perfil (3:4):** la rejilla muestra un recorte central vertical 3:4 del post 4:5 → se pierden **≈ 34 px por cada lado** (área visible 1012 × 1350, x 34–1046). Con el margen de 90 px el texto nunca se corta; aun así, **nada esencial a menos de 90 px del borde lateral**.
- La miniatura de rejilla se ve a ≈ 120–140 px de ancho en móvil: el titular de la pieza debe leerse como mancha; la firma no tiene por qué leerse en rejilla.
- Alternativa a evaluar con experto-redes-sociales: publicar directamente en 3:4 (1080 × 1440) para que rejilla y feed coincidan. Por ahora el estándar del encargo es 4:5.

### 2.2 Carrusel de Instagram · 1080 × 1350 px por diapositiva
- Mismas zonas que el post. Todas las diapositivas en la misma proporción (la plataforma impone la de la primera).
- Máximo de diapositivas: el que permita la plataforma en la fecha (hoy hasta 20). Recomendado editorialmente: **5–8**.
- **Diapositiva 1 = portada:** es la que aparece en rejilla → aplica la regla del 2.1.
- Indicador de paginación propio (p. ej. «2/6») en la esquina inferior derecha, dentro de la zona segura; no depender de los puntos de la app.
- Si un elemento cruza de una diapositiva a otra (continuidad), el corte cae exactamente en x = 1080 y nunca atraviesa texto ni el isotipo.

### 2.3 Story · 1080 × 1920 px (9:16)
- **Zona reservada superior: y 0–250 px** (barra de progreso, avatar, nombre, cerrar). Solo fondo/foto.
- **Zona reservada inferior: y 1600–1920 px (320 px)** (campo de respuesta, reacciones, enlace, «Enviar mensaje»). Solo fondo/foto.
- **Zona segura de contenido:** x 90–990, y 250–1600.
- Stickers interactivos (encuesta, enlace, pregunta): reservar un bloque de **≈ 900 × 300 px** dentro de la zona segura, preferiblemente en el tercio inferior (y 1200–1550). La plantilla lo marca como caja vacía.

### 2.4 Portada de reel · 1080 × 1920 px (9:16)
- **Recorte en rejilla del perfil (3:4):** franja central **1080 × 1440 (y 240–1680)**.
- **Recorte en feed (4:5):** franja central **1080 × 1350 (y 285–1635)**.
- **Zona del titular de portada (intersección de ambos recortes + margen):** **x 90–990, y 375–1545**. Todo texto o elemento identificativo de la portada va aquí.
- Durante la reproducción, la interfaz del reel tapa el lateral derecho (iconos) y la franja inferior (texto, audio): para el **primer fotograma y rótulos dentro del vídeo**, zona segura **x 90–890, y 250–1500**.
- La portada puede ser fotograma del vídeo o imagen subida aparte; en ambos casos se diseña sobre esta plantilla.

### 2.5 Facebook (página)
- **Post:** se reutiliza el 1080 × 1350 de Instagram (mismas zonas). Alternativa 1080 × 1080 si se publica solo en Facebook.
- **Story de Facebook:** igual que 2.3.
- **Foto de portada de la página (opcional en este encargo):** exportar a **1640 × 624 px**; contenido esencial en la franja central **≈ 1200 × 500 px**, porque móvil y escritorio recortan distinto. Sin texto pequeño. Avatar superpuesto abajo a la izquierda en escritorio: dejar libre esa esquina.

### 2.6 Google Business Profile
- **Fotos (centro, equipo, ambiente):** JPG o PNG, **10 KB–5 MB**, mínimo 250 × 250 px, recomendado **≥ 720 × 720 px**. Foto real, sin texto superpuesto, sin marcos ni filtros fuertes.
- **Logotipo de la ficha:** cuadrado, ≥ 720 × 720 px. Mismo criterio que el avatar (§5.3); bloqueado por el vector.
- **Portada de la ficha:** 16:9, recomendado **1024 × 576 px** o superior. Google puede mostrar otra foto como principal: no confiar en ella para mensajes.
- **Publicación (Novedades / Ofertas / Eventos):** imagen **4:3, 1200 × 900 px** (mínimo 400 × 300). Google recorta según el dispositivo: **contenido esencial centrado en 900 × 750 px (x 150–1050, y 75–825)**. Texto en imagen mínimo; el mensaje va en el texto de la publicación.
- Las publicaciones de medicina estética llevan el pie legal (§3.3) **en el texto de la publicación**, no solo dentro de la imagen.

### 2.7 Portadas de highlights (historias destacadas) · 1080 × 1920 px
- Se suben como story; el perfil muestra un **círculo** recortado del centro.
- **Círculo de seguridad:** Ø **720 px**, centrado en (540, 960). El pictograma ocupa **Ø ≈ 400 px** como máximo dentro de ese círculo.
- Fondo plano, sin texto (el nombre del destacado lo pone Instagram debajo).
- Miniatura real en perfil ≈ 64 px: trazo del pictograma suficientemente grueso (ver §6.2).

### 2.8 Avatar / foto de perfil
- Exportar **1080 × 1080 px** (Instagram lo muestra a ≈ 110 px; Facebook y GBP, similar). Recorte circular.
- Ver §5.3 para la composición con el isotipo.

---

## 3. Estructura de cada plantilla (jerarquía)

### 3.1 Niveles tipográficos (tamaños en px sobre lienzo de 1080 de ancho)
Tipografías **[PENDIENTE director-arte]**. Tamaños mínimos provisionales, válidos sea cual sea la familia:

| Nivel | Uso | Mín. | Rango orientativo | Máx. líneas |
|---|---|---|---|---|
| T0 · Etiqueta de pilar | CUÍDATE / CONECTA / SIENTE | 28 px, versalitas o mayúsculas espaciadas | 28–32 px | 1 |
| T1 · Titular | Mensaje principal | 64 px | 64–110 px | 3 (post) · 4 (story) |
| T2 · Cuerpo | Desarrollo, pasos, cita | 36 px | 36–44 px | 6 por diapositiva |
| T3 · Firma | «Rosa Ondoño» (logotipo cuando exista; hasta entonces, texto) | 28 px | 28–32 px | 1 |
| T4 · Pie legal | Solo medicina estética | 26 px | 26–28 px | 3 |

### 3.2 Orden y posición (post, carrusel, story)
1. **Etiqueta de pilar (T0)** — arriba a la izquierda, dentro de la zona segura.
2. **Titular (T1)** — tercio superior o centro óptico.
3. **Cuerpo (T2)** — opcional; en carruseles, en las diapositivas interiores.
4. **Firma (T3)** — abajo a la izquierda: «Rosa Ondoño», opcionalmente con el isotipo original cuando haya vector y tamaño mínimo aprobado. En story, por encima de y 1600.
5. **Pie legal (T4)** — solo medicina estética, franja inferior propia, nunca superpuesto a foto sin fondo plano.
6. **Paginación** — solo carrusel, abajo a la derecha.

La firma y el pie legal no se reducen por debajo del mínimo para «hacer sitio»: se acorta el titular o el cuerpo.

### 3.3 Pie legal de medicina estética (obligatorio en esas piezas)
Texto base (redacción final: experto-marketing-comunicacion + revisión legal):

> Tratamiento médico realizado por el Dr. Roberth Bravo Pardo · Nº de colegiado **[PENDIENTE]**
> Centro sanitario Nº de registro **[PENDIENTE]** · Nº de autorización de publicidad sanitaria **[PENDIENTE, si aplica]**

- Aparece en la imagen (post, cada diapositiva de carrusel con contenido médico, story, portada de reel y rótulo final del reel) **y** en el texto de la publicación.
- Contraste ≥ 4,5:1 sobre fondo plano. Tamaño ≥ 26 px.
- Además, se aplica todo `00-nucleo-marca/cumplimiento-legal.md`: sin garantías de resultado, sin minimizar riesgos, sin urgencia de compra, sin nombres comerciales de medicamentos de prescripción, antes/después solo con consentimiento escrito y sin retoque.
- **Testimonios y reseñas:** no se usan reseñas de pacientes como respaldo de tratamientos de medicina estética (la normativa de publicidad sanitaria limita el uso de testimonios). Confirmar el criterio con el asesor legal.

### 3.4 Variantes de plantilla a producir (cuando se desbloquee el manual)
| Código | Formato | Variantes |
|---|---|---|
| POST | 1080×1350 | Solo tipografía · Foto + titular · Cita/reseña · Medicina estética (con pie legal) |
| CAR | 1080×1350 | Portada · Interior texto · Interior foto · Cierre/CTA · Medicina estética |
| STO | 1080×1920 | Foto · Texto · Sticker interactivo · Medicina estética |
| REEL | 1080×1920 | Portada · Rótulo inicial · Rótulo final (firma + pie legal si procede) |
| GBP | 1200×900 | Novedad · Oferta (solo estética/terapias) |
| HL | 1080×1920 | 8 portadas (§6) |
| AV | 1080×1080 | Avatar (§5.3) |

---

## 4. Código de pilar · Cuídate / Conecta / Siente

Objetivo: que se distinga a qué pilar pertenece cada pieza **sin alterar ni sustituir el color corporativo**, que sigue siendo el único color de marca y es común a los tres.

Se diferencian por tres capas redundantes (nunca solo por color, por accesibilidad):

1. **Etiqueta textual (obligatoria):** «CUÍDATE», «CONECTA» o «SIENTE» en T0, siempre en la misma posición (arriba a la izquierda). Es la diferencia principal.
2. **Fondo neutro por pilar:** cada pilar tiene su fondo plano propio dentro de la paleta secundaria de neutros.
   - Cuídate: **[PENDIENTE director-arte]**
   - Conecta: **[PENDIENTE director-arte]**
   - Siente: **[PENDIENTE director-arte]**
   - Condición técnica: cada neutro debe dar ≥ 4,5:1 con el color de texto y ≥ 3:1 con el color corporativo (referencia: #701B78 sobre blanco da 9,9:1; sobre gris claro #E0E0E0, 7,5:1), y no puede ser una variante tintada del color corporativo que se confunda con él.
3. **Pictograma de pilar (opcional):** el de la serie de highlights (§6) a tamaño pequeño junto a la etiqueta.

El color corporativo se usa igual en los tres pilares (acentos, firma, isotipo). No se crean «morado claro para Siente» ni similares: eso sería recolorear la marca.

Reparto de pilares en la rejilla (orden de publicación para que la rejilla alterne fondos): lo define experto-redes-sociales en el calendario.

---

## 5. Isotipo en redes

### 5.1 Reglas inamovibles
- Se usa **solo el archivo original** de `assets/logo-original/` (cuando llegue el vector). Hoy solo hay PNG de 233 × 315 px: **no apto para producción** (se pixela por encima de ≈ 230 px de alto).
- Prohibido: redibujar, deformar o escalar no proporcional, recolorear, rotar, recortar, añadir sombras, brillos, contornos, degradados, transparencias parciales o texturas, ponerlo dentro de formas que lo alteren, usarlo como patrón o marca de agua troceada, animarlo deformándolo.
- No se usa como pictograma de highlight ni se mezcla con los iconos del sistema.
- No se coloca la versión a color sobre fondos oscuros ni fotos con zonas oscuras o recargadas: el color medido (#701B78) da solo 1,3:1 sobre gris oscuro #333333. Sobre esos fondos hace falta la **versión monocroma negativa [PENDIENTE manual]**; hasta entonces, el isotipo solo va sobre fondo claro plano.

### 5.2 Área de respeto y tamaño mínimo
- Área de respeto: **[PENDIENTE del manual]**.
- Tamaño mínimo digital: **[PENDIENTE del manual]**. Provisionalmente, en plantillas se reserva una caja para firma de 80 × 108 px (proporción del PNG) que se ajustará cuando se apruebe el mínimo.

### 5.3 Avatar · propuesta (pendiente del vector)
- Lienzo 1080 × 1080, **fondo plano** claro (blanco o neutro claro de la paleta [PENDIENTE]).
- **Isotipo original centrado**, a color, sin efectos. Como es vertical (≈ 0,74:1), su **alto no supera el 60 % del diámetro** (≈ 650 px) para que el círculo deje margen arriba y abajo; centrado ópticamente (ajuste fino tras ver el vector, sin tocar el icono).
- Sin texto «Rosa Ondoño» en el avatar: a 110 px no se lee; el nombre ya aparece junto al avatar.
- Mismo avatar en Instagram, Facebook, GBP y WhatsApp Business.
- Wireframe: `wireframes/avatar-1080x1080.svg`.

---

## 6. Pictogramas de highlights

### 6.1 Serie propuesta (8)
| # | Nombre del destacado | Pictograma propuesto | Nota |
|---|---|---|---|
| 1 | Bonos regalo | Sobre o lazo | Prioridad en diciembre (primera posición) |
| 2 | Cuídate | Mano abierta | Pilar |
| 3 | Conecta | Dos arcos/trazos que se tocan | Pilar |
| 4 | Siente | Hoja o gota | Pilar |
| 5 | Medicina estética | Cruz médica de trazo o fonendoscopio | Cada story guardada aquí lleva pie legal; bloqueado hasta tener nº de colegiado y registro |
| 6 | Reseñas | Bocadillo con estrella | Solo reseñas de estética y terapias, con permiso; ninguna sobre medicina estética |
| 7 | El centro | Puerta o fachada | Ubicación, cómo llegar, espacios |
| 8 | Rosa | Inicial «R» o retrato de línea | Alternativa: «Equipo», para incluir también al médico. Lo decide el cliente |

Instagram muestra unos 4–5 en pantalla sin desplazar: el orden importa. Orden propuesto: Bonos regalo (dic.), Cuídate, Conecta, Siente, Reseñas, Medicina estética, El centro, Rosa.

### 6.2 Reglas de construcción
- **Derivados del sistema, no del isotipo:** no reproducen ni imitan la figura (círculo + onda + círculo macizo), para no crear variantes del icono.
- Retícula de construcción **24 × 24** con zona viva de 20 × 20; se escala a Ø 400 px en la portada.
- Trazo único lineal, **grosor uniforme 1,5 px sobre 24** (≈ 25 px a Ø 400) — coherente con el trazo uniforme del isotipo; terminaciones y uniones **[PENDIENTE: redondeadas o rectas, se decide al ver el vector]**.
- Sin rellenos, salvo un único punto macizo si el director-arte lo aprueba.
- Color del pictograma: color corporativo sobre el fondo neutro, o neutro oscuro; fondo plano. Contraste no textual ≥ 3:1.
- Entrega: SVG por icono (trazo expandido + versión editable con trazo vivo) y PNG 1080 × 1920 por portada.

---

## 7. Pieza especial de diciembre · Bono / tarjeta regalo

> Solo para **estética y terapias complementarias**. **Excluye la medicina estética** (actividad sanitaria: no se regalan ni promocionan tratamientos médicos). La exclusión figura impresa en el bono.

### 7.1 Formatos
| Pieza | Medida final | Sangrado | Color | Notas |
|---|---|---|---|---|
| Tarjeta física | **85 × 55 mm** | 3 mm por lado (91 × 61 mm de documento) | CMYK Coated FOGRA39 · Pantone del color corporativo **[PENDIENTE]** | Margen interior de seguridad 4 mm. Papel ≥ 350 g. Reverso para datos y condiciones |
| Alternativa física (díptico) | A6 cerrado **105 × 148 mm** (abierto 210 × 148) | 3 mm | Ídem | Para servicios con más texto; sobre C6 |
| Bono digital (envío por email/WhatsApp) | PDF A6 vertical **105 × 148 mm** | Sin sangrado | sRGB | Campos rellenables o generados por pedido |
| Imagen digital | **1080 × 1350 px** | — | sRGB | Para enviar como imagen y para el post/story promocional |
| Story promocional | 1080 × 1920 px | — | sRGB | Zonas del §2.3 |

Archivo de imprenta: PDF/X-4 (o PDF/X-1a si la imprenta lo pide), textos trazados o fuentes incrustadas, imágenes ≥ 300 ppp, negro de texto 100 K. Prueba de color antes de tirada.

### 7.2 Contenido mínimo
**Anverso:** «Bono regalo» · firma Rosa Ondoño (isotipo original + nombre, cuando haya vector) · lema opcional «Cuídate · Conecta · Siente».

**Reverso / segunda página:**
- Para: ______ · De: ______ · Mensaje (opcional)
- Servicio o importe: **[PENDIENTE — sin precios inventados; lo fija el cliente]**
- Código único del bono: [formato PENDIENTE, lo define el cliente según su sistema de caja/reservas]
- Validez: **[PENDIENTE]**
- Condiciones de uso: **[PENDIENTE]** (cambios, cancelación, transferibilidad, uso parcial…). Revisión legal recomendada (normativa de consumo).
- **«No válido para tratamientos de medicina estética.»**
- Cómo reservar: 965 120 300 · WhatsApp 691 315 622 · info@rosaondono.com · rosaondono.com
- Av. Maisonnave 38, Entlo. Izq., 03003 Alicante
- Datos del emisor (razón social, NIF): **[PENDIENTE]**

### 7.3 Comunicación del bono en redes
- Plantillas POST/STO/GBP «Oferta» con imagen de estética o terapias; **nunca imágenes ni menciones de tratamientos médicos**.
- Sin urgencia agresiva ni sorteos que incluyan medicina estética. Si se hace un sorteo de bono, bases legales **[PENDIENTE]** y exclusión expresa.

---

## 8. Accesibilidad

- **Contraste (WCAG 2.2 AA):** texto ≥ **4,5:1** en todos los tamaños (el criterio de «texto grande» a 3:1 no se aplica, porque el lienzo se ve reducido al ≈ 35 % en móvil). Elementos gráficos con significado (pictogramas, iconos) ≥ **3:1**. Referencias medidas: #701B78/blanco 9,9:1 · #8E1F5C/blanco 8,4:1 · ninguno de los dos sirve sobre fondos oscuros.
- **Texto sobre foto:** solo sobre fondo plano o sobre zona de foto uniforme; el contraste se mide en el píxel más desfavorable. Si no llega, caja de fondo plano.
- **Tamaño mínimo en lienzo de 1080 px de ancho:** cuerpo 36 px, pie legal y firma 26–28 px (≈ 9–10 pt en un móvil de 390 pt). Máximo ≈ 40 palabras de texto en imagen por pieza; el resto, al copy.
- **Vídeo (reels y stories):** subtítulos siempre, **incrustados** en el vídeo dentro de la zona segura del §2.4 (x 90–890, por encima de y 1500), máx. 2 líneas, ≈ 42 caracteres por línea, mismo contraste mínimo; además archivo **.srt** para Facebook y YouTube. Sin destellos de más de 3 por segundo.
- **Texto alternativo:** cada imagen publicada lleva alt text personalizado (Instagram: «Configuración avanzada → Escribir texto alternativo»; Facebook y GBP: descripción). Describe la imagen y transcribe el texto incrustado. Máx. ≈ 125 caracteres más la transcripción. Lo redacta experto-redes-sociales junto al copy.
- **Emojis y caracteres especiales:** no sustituir palabras por emojis; no usar letras «de fantasía» Unicode (los lectores de pantalla no las leen).
- **Información no solo por color:** el código de pilar ya lo cumple (etiqueta textual).

---

## 9. Checklist de entrega

### 9.1 Archivos maestros
- [ ] Plantilla editable por formato en **SVG** (capas nombradas: `fondo`, `foto`, `pilar`, `titular`, `cuerpo`, `firma`, `pie-legal`, `zonas-seguras` oculta) y/o **HTML** con variables de texto.
- [ ] Isotipo **enlazado** desde `assets/logo-original/` (vector), nunca incrustado retocado.
- [ ] Guías de zona segura en capa oculta, no exportable.
- [ ] Tipografías con licencia válida para uso en redes **[PENDIENTE]**.

### 9.2 Nomenclatura
`RO_[RED]_[FORMATO]_[PILAR]_[AAAAMMDD]_[tema]_v[NN].[ext]`
- RED: `IG`, `FB`, `GBP`, `WA`
- FORMATO: `POST`, `CAR01…CAR08`, `STO`, `REEL`, `REELPORT`, `HL`, `AV`, `BONO`
- PILAR: `CUI`, `CON`, `SIE`, `MED` (medicina estética), `GEN` (general)
- Ejemplo: `RO_IG_CAR03_CUI_20261201_drenaje-postquirurgico_v02.jpg`
- Sin espacios, tildes ni ñ en nombres de archivo.

### 9.3 Exportación
| Tipo | Formato | Ajustes |
|---|---|---|
| Imagen fija con foto | JPG | sRGB, calidad 85–90 %, 1× tamaño de lienzo, < 1,5 MB |
| Imagen fija solo tipografía/vector | PNG-24 | sRGB, sin transparencia |
| Vídeo | MP4 H.264 | 1080 × 1920, 30 fps, ≈ 8–12 Mbps, audio AAC 48 kHz; subtítulos incrustados + `.srt` |
| Highlights | PNG | 1080 × 1920 |
| Avatar | PNG | 1080 × 1080 |
| Bono impreso | PDF/X-4 | CMYK FOGRA39, sangrado 3 mm, marcas de corte |
| Bono digital | PDF | sRGB, fuentes incrustadas, < 2 MB |

### 9.4 Control antes de entregar
- [ ] Ningún texto ni elemento clave fuera de su zona segura (comprobado con la capa de guías).
- [ ] Rejilla del perfil simulada con las últimas 9 publicaciones.
- [ ] Contraste medido de cada combinación usada (≥ 4,5:1 texto, ≥ 3:1 gráficos).
- [ ] Isotipo: archivo original, sin modificar, sobre fondo permitido, ≥ tamaño mínimo.
- [ ] Color corporativo con el valor oficial confirmado (no #701B78 ni #8E1F5C «a ojo»).
- [ ] Pieza de medicina estética: pie legal completo, sin PENDIENTES, revisada contra `cumplimiento-legal.md`.
- [ ] Alt text y subtítulos preparados.
- [ ] Marcado «BORRADOR» retirado solo tras aprobación del manual (director-arte) y revisión de qa.

---

## 10. Wireframes neutros

En `wireframes/` (gris, sin isotipo ni color de marca; solo zonas y jerarquía):
`post-4x5-1080x1350.svg` · `story-1080x1920.svg` · `reel-portada-1080x1920.svg` · `highlight-1080x1920.svg` · `avatar-1080x1080.svg` · `gbp-publicacion-1200x900.svg` · `bono-regalo-85x55mm.svg`.
Leyenda común: rayado = zona reservada de interfaz o recorte; línea discontinua = zona segura; cajas grises = bloques de contenido.
