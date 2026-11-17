# Plan de redirecciones 301
*01-web · Entregable 9 (adelantado) · Responsables: experto-seo + programador · Revisión: qa · Fecha: 17/11/2026*
*Mapa completo: [`redirecciones-301.csv`](redirecciones-301.csv)*

## 1. Inventario de origen
Se rastreó la web el 17/11/2026 de tres formas:
- **Sitemaps de Yoast:** `post-sitemap.xml` (9 entradas) y `page-sitemap.xml` (11 páginas). En total, 20 URLs indexables.
- **Enlaces internos:** las 5 categorías del blog (`/category/*`), `feed`, `comments/feed` y la paginación.
- **Comprobación de URLs típicas de WordPress:** `/author/admin/` ya redirige a `/`. Aviso legal, privacidad y cookies dan **404**.

| Resultado | URLs |
|---|---|
| Se mantienen sin cambio (200) | 3: `/`, `/blog/`, `/contacto/` |
| 301 1:1 a su equivalente | 8 |
| 301 por fusión (contenido que canibalizaba una categoría o ficha) | 4 |
| 301 de posts a `/blog/{slug}/` | 5 |
| 301 de archivos, paginación, feed y autor | 9 |
| 410 / 404 intencionado | 3 + patrones |

**Ninguna URL actual acaba en 404 sin decisión explícita.**

## 2. Reglas de implementación
1. **Redirección directa, sin cadenas:** origen → destino final en un solo salto. Hay que revisar que `/author/admin/` no quede como `/author/admin/` → `/` → `/equipo/…`.
2. **Normalización canónica en un único salto:**
   - versión: `https://rosaondono.com/` (sin `www`);
   - `http` → `https`, `www` → sin `www`;
   - sin `/` final → con `/` final;
   - mayúsculas → minúsculas.

   Hoy `www` ya devuelve 301. `http` devolvió 429 durante el rastreo: hay que verificarlo.
3. **Ubicación:**
   - si el stack es Astro en Netlify o Cloudflare: archivo `_redirects`, generado desde el CSV;
   - si es WordPress: el plugin Redirection o reglas de servidor.
4. **Parámetros:** se conservan los UTM en la redirección.
5. **Contenido fusionado:** antes de redirigir un post a una categoría o ficha, se migra su contenido útil (FAQ de depilación, guía corporal). Si no, se pierde la relevancia que justifica la 301.
6. **Las 301 se mantienen al menos 12 meses,** idealmente de forma indefinida.

## 3. Checklist de migración
**Antes del lanzamiento:**
- [ ] Exportar de Search Console (cuando haya acceso) las páginas con clics y enlaces externos de los últimos 16 meses. Añadir al CSV cualquier URL que falte, incluidas las imágenes con tráfico.
- [ ] Rastrear la web actual con Screaming Frog o similar para confirmar que no hay más URLs: adjuntos de WordPress, `?p=`, etiquetas.
- [ ] Hacer una copia de seguridad completa de WordPress (contenido + `uploads`) y guardarla.
- [ ] Hacer un benchmark: posiciones de las keywords de prioridad 1, tráfico orgánico y Core Web Vitals.

**Lanzamiento:**
- [ ] Desplegar las redirecciones a la vez que la web nueva.
- [ ] Probar el CSV automáticamente: cada origen devuelve 301 y un solo salto, y cada destino devuelve 200.
- [ ] Subir el sitemap nuevo a Search Console.
- [ ] Mantener el sitemap antiguo 2–4 semanas para acelerar el reprocesado.
- [ ] Actualizar los enlaces de GBP, Instagram, Facebook, Doctoralia y otros directorios.

**Después (30 días, con el project-manager):**
- [ ] Revisar semanalmente los errores 404 en Search Console y en los logs.
- [ ] Comparar el tráfico y las posiciones con el benchmark.
- [ ] Corregir las redirecciones que lleven a páginas poco relevantes.

---
**Qué he hecho:**
- Inventario completo de las URLs descubribles.
- Mapa 301 de las 34 entradas, más los patrones.
- Reglas técnicas.
- Checklist de migración.

**Qué falta:**
- Cruzar el mapa con los datos de Search Console y con un rastreo exhaustivo.
- Confirmar las URLs finales cuando se cierre el stack.

**Bloqueos:**
- Acceso a Search Console.
- Acceso al WordPress actual, para la copia de seguridad y para revisar los adjuntos.
