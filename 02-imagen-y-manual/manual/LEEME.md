# Manual de marca · Rosa Ondoño · v3.0
*Departamento de Imagen y Manual · 17/11/2026 · A4 horizontal, 44 páginas*

| Archivo | Qué es |
|---|---|
| `manual-de-marca.pdf` | El manual para enviar o presentar. |
| `manual-de-marca.html` | La misma versión, para ver en el navegador. |
| `construir_manual.py` | Genera el HTML. Los contrastes WCAG se calculan, no se escriben a mano. **No edites el HTML a mano.** |
| `exportar_pdf.js` | Exporta el PDF (`node exportar_pdf.js`; con `--png`, saca también miniaturas). |
| `img/fotos/` | Fotos del moodboard (Unsplash, licencia Unsplash). Solo como referencia. |
| `../identidad/logo/` | Logos listos para usar: isotipo SVG (color y negro) y PNG transparentes. |
| `../identidad/iconos/` · `../identidad/tokens/` | 14 iconos SVG y tokens de color y tipografía. |

Originales del cliente en `assets/logo-original/2023/`: el PSD maestro, el SVG del isotipo y los PNG/WEBP de cada versión.

**Para editar:** cambia `construir_manual.py` y ejecuta `python3 construir_manual.py && node exportar_pdf.js`.

## Decisiones del cliente (17/11/2026)
- ✅ Color oficial **#7D1F73**. ✅ Licencias comerciales de Bambino Light y Biko. ✅ Negativo en blanco. ✅ Supergráfico.
- No existe el logotipo en vector. Se ha **reconstruido** en `../identidad/logo/*.svg`:
  - el isotipo es el SVG original del cliente, sin tocar;
  - el texto está calcado del PSD maestro con `herramientas/vectorizar.py` (coincidencia del 97,6 % en el horizontal).
  - Antes de imprenta o rotulación, conviene revisarlo a gran tamaño.

## v3.0 (26/11/2026) · 53 páginas
Revisado con las skills de manual de marca, mensajes, manifiesto, voz e «impeccable» (calidad visual).
- **Nuevas páginas:** Manifiesto · Mensajes (mensaje central, propuesta de valor, 4 mensajes clave con pruebas reales y banco de pruebas) · Reglas de escritura (con ejemplos antes/después sacados de la web actual) · Vocabulario 12 + 12 y cómo nombramos las cosas · Presentaciones y email · Contacto y archivos (con historial de versiones).
- **«Antes de publicar»:** añadidos el tamaño mínimo, el Pantone, el negativo y la regla de emojis.
- **Pulido visual:** iconos SVG en lugar de los caracteres ✔/✖, fuera las barras de color en un solo lado de las tarjetas, e índice al día.

## v2.2 (17/11/2026)
- **Morado en imprenta:** PANTONE 255 C (ΔE00 1,9) y CMYK 53/96/10/24 (Color Bridge, ΔE 3,7). Calculado contra las bibliotecas PANTONE+ en Lab.
- **Descriptor:** tilde añadida («estética») en todas las versiones SVG y PNG (`--tilde` en `herramientas/vectorizar.py`).
- **Nuevo apartado «El centro»:** fotos del recorrido 360° (`assets/fotografia/recorrido-360/`), con los derechos del centro. Por decisión del cliente, no se asigna un uso a cada cabina.
- **Nº de registro sanitario:** retirado del manual, por decisión del cliente.

## Pendiente
1. Prueba de color de PANTONE 255 C y del CMYK sobre el papel final.
2. Nº de colegiado del médico.
3. Sesión de fotos propia para gran formato e impresión.
