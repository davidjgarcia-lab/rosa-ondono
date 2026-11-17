# Manual de marca · Rosa Ondoño · v2.1
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

## Pendiente
1. Pantone y CMYK del #7D1F73, con una prueba de color.
2. Validar el vector reconstruido.
3. Tilde y contenido del descriptor.
4. Nº de registro sanitario y nº de colegiado.
5. Sesión de fotos propia.
