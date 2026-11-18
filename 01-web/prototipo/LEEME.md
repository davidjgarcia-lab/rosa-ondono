# Prototipo web v3.1 · Rosa Ondoño

**Enlace para compartir (móvil y escritorio):** https://rosa-ondono-prototipo.netlify.app · Netlify, proyecto `rosa-ondono-prototipo`. Configuración en `netlify.toml`: se publica `sitio/`, con cabeceras de seguridad y `noindex`. Pruebas y funcionamiento de los formularios: `../qa/pruebas-v3-responsive-y-formularios.md`.
*01-web · 18/11/2026 · Estado: **PROTOTIPO v3.1** (dirección de arte v3 aprobada; construcción y pruebas en `../qa/pruebas-v3-1-web-nueva.md`). Aplica el manual de marca v2.1; pendiente de QA final y de la validación del director de arte.*

Web estática multipágina generada a partir del catálogo de Supabase:
- con URLs limpias y SEO completo;
- con su vista previa en un solo archivo (`sitio/vista-previa.html`), que es la que se publica como artefacto en Claude.

## Estructura
| Ruta | Qué es |
|---|---|
| `generar_sitio.py` | Generador. Lee Supabase (o la copia `datos/catalogo.json` si no hay conexión) y escribe `sitio/` |
| `fuente/` | `sitio.css` (tokens del manual), `sitio.js` (menú, cookies, formularios) y `config.js` (Supabase) |
| `img/` | Logotipos e isotipo del manual v2.1, iconos del manual y fotos (`fotos/`) |
| `netlify/` | Funciones de servidor: `/api/huecos`, `/api/reserva` (Google Calendar + aviso de WhatsApp con CallMeBot) y `/api/regalo`. Claves solo en variables de entorno de Netlify |
| `fuente/vendor/` | GSAP 3 + ScrollTrigger (solo en la home, para la escena fija del método) |
| `supabase/` | `001_esquema.sql`, `002_semilla.sql` (con `generar_semilla.py`) y `003_areas_y_regalos.sql` |
| `sitio/` | **Salida generada** (no editar a mano): 75 páginas, `sitemap.xml`, `robots.txt`, `_redirects` y `404.html` |

```bash
cd 01-web/prototipo
python3 generar_sitio.py                 # regenera sitio/
cd sitio && python3 -m http.server 8000  # http://localhost:8000
```

## Páginas
- **Inicio:**
  1. Hero «Tu bienestar empieza por ti».
  2. 01 Nuestro universo.
  3. Método Cuídate · Conecta · Siente.
  4. 02 Los más pedidos.
  5. 03 Conócenos.
  6. 04 Tu experiencia.
  7. 05 Reserva tu cita.
  8. Tarjeta regalo.
- **4 áreas:** `/estetica/`, `/medicina-estetica/`, `/terapias/` y `/bienestar/`.
- **62 fichas:**
  - `/tratamientos/{slug}/`;
  - las médicas en `/medicina-estetica/{slug}/`, con CTA de consulta y aviso sanitario.
- **Otras páginas:** `/valoracion-integral/`, `/conocenos/`, `/reservar/` (acepta `?servicio=`) y `/regalar/` (también acepta `?servicio=`).
- **Legales**, con texto pendiente del asesor: `/aviso-legal/`, `/privacidad/` y `/cookies/`.

## Base de datos (Supabase `rosa-ondono-web`, eu-west-3)
- **Lectura pública:** `areas`, `categorias` (con `area_slug`), `tratamientos`, `faqs`, `profesionales`, `pilares` y `programas`.
- **Formularios:** exigen teléfono **o** email (migración `004_telefono_o_email.sql`). Cada envío va a Netlify Forms (email), a Supabase y a WhatsApp, con el mensaje ya redactado para el número del centro.
- **Solo inserción** (no se pueden leer con la clave pública):
  - `solicitudes_reserva`: solo tratamientos reservables;
  - `solicitudes_regalo`: nunca tratamientos médicos.
- Sin campos de texto libre de salud.
- Asesor de seguridad de Supabase: sin avisos.

## SEO incluido
- **Etiquetas:** un H1 por página; `title` de 60 caracteres o menos; meta description; canonical; Open Graph y Twitter; `lang="es"`.
- **Datos estructurados (JSON-LD):**
  - `HealthAndBeautyBusiness` + `MedicalClinic` (NAP, horario, mapa, redes);
  - `Service` / `MedicalProcedure` por ficha;
  - `FAQPage`, `BreadcrumbList` y `Person`.
- **Archivos:**
  - `sitemap.xml` sin legales ni 404;
  - `robots.txt` (bloquea la vista previa);
  - `_redirects` en formato Netlify, generado desde `../seo/redirecciones-301.csv`, con las URLs actualizadas a la v2.
- **Rendimiento:**
  - imágenes WebP de 800 y 1600 px con `srcset`, `width`/`height` y carga diferida;
  - foto principal con `fetchpriority="high"`;
  - JS mínimo y diferido.
- **Pendiente:**
  - tipografías autoalojadas en WOFF2 para producción;
  - el blog, al que apuntan las 301 de los artículos actuales, aún no está construido.

## Fotografía
- **Del centro** (derechos del cliente): `01-recepcion`, `02-recepcion-ventana-patio`, `03-pasillo-cabinas`, `06-cabina-hornacina-lavabo`, `08-patio-jardin-cenador` y `10-patio-plantas`.
  - Las cabinas no llevan uso asignado.
  - `09-patio-puerta-icono` no se usa porque se ve la alarma.
- **Provisionales de Unsplash** (licencia Unsplash, uso comercial permitido; descarga registrada). Se sustituyen por la sesión propia:

| Archivo | Autoría |
|---|---|
| `u-facial-masaje` | Dominique Rivas |
| `u-facial-mascarilla` | Rosa Rafael |
| `u-retrato-natural` | Štefan Štefančík |
| `u-masaje-espalda` | Toa Heftiba |
| `u-piedras-flores` | engin akyurt |
| `u-terapia-agujas` | Antonika Chanel |
| `u-corporal` | THLT LCX |
| `u-manos` | THLT LCX |

## Límites del prototipo
- **Vista previa en Claude:** no puede conectar con Supabase. Los formularios lo indican y **no** dan la solicitud por enviada. Los datos salen de `datos/catalogo.json`, copia de la misma base.
- **Disponibilidad:** la reserva pide día y hora (lunes a viernes, 9:00–19:00). Las horas ocupadas salen del Google Calendar del centro cuando estén configuradas las variables `GOOGLE_*`.
- **Tarjeta regalo:** el pago se gestiona por contacto hasta tener pasarela.
