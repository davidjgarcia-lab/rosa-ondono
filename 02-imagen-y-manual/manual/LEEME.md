# Manual de marca · Rosa Ondoño · v2.0
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

## Hallazgos en los archivos del cliente
- **Tipografías del logotipo** (sacadas del PSD): nombre en **Bambino Light** y descriptor en **Biko**.
- **Cuatro morados en uso:**
  - **#7D1F73**: el del PSD maestro y los logos completos. Es el que propone el manual.
  - #701B78: favicon de la web.
  - #6C2470: PNG del isotipo y logo vertical.
  - #8E1F5C: CSS de la web.
- **El descriptor dice «centro de estetica…»**: le falta la tilde y no menciona la medicina estética.
- **El isotipo ya existe en SVG**, y el cliente tiene una versión oficial en negro.

## Pendiente del cliente
1. Confirmar #7D1F73 como color oficial, con su Pantone y su CMYK.
2. Logotipo completo en vector (AI, EPS o PDF).
3. Licencias comerciales de Bambino Light y Biko.
4. Corregir el descriptor.
5. Autorizar la versión negativa del isotipo y su uso como supergráfico.
6. Nº de registro sanitario y nº de colegiado.
