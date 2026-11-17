# Benchmark web de competencia y referentes
*01-web · experto-ux-ui + experto-seo · 17/11/2026 · Base del rediseño v2 del prototipo*

## Alcance y límites
| Web | Estado del análisis |
|---|---|
| dragarrigos.es (Dra. Eva Garrigós) | ✅ HTML descargado y analizado (estructura, menú, CTA, SEO, datos estructurados) |
| maeli.es (Maeli, Dra. Vanessa Herrera) | ✅ HTML y capturas en escritorio y móvil (las imágenes de su CDN no cargaron) |
| beaire.com · aesop.es · hammamalandalus.com · thebeautyconcept.com · eltemplobyzenestetic.es · sokoexperience.com | ❌ **Pendiente.** Se añadieron al entorno de red, pero el proxy de esta sesión siguió rechazando la conexión. No se ha inventado nada sobre ellas. |

También se tiene en cuenta la propuesta conceptual del cliente: hero «Tu bienestar empieza por ti», bloques 01–05 y las referencias AIRE / TACHA / Crear·t.

## Lo que hemos observado

### Dra. Garrigós
**Estructura de la home:**
1. Hero con H1 «Clínica de medicina estética y well aging en Alicante».
2. La doctora.
3. Manifiesto: «Una estética que no compite con el tiempo, aprende a convivir con él».
4. «Cuatro ateliers, una sola mirada»: Medicina estética · Corporal · Facial · Capilar.
5. «No los llamamos boxes. Los llamamos ateliers».
6. Reseñas.
7. Financiación.
8. Laboratorios.
9. Tecnología.
10. Antes y después.
11. Blog.
12. CTA final: «Aquí empieza tu mejor versión».

**Menú:** Medicina estética · Corporal · Facial · Capilar · Rituales Wellness · Blog · EN · **Pedir cita**.

**SEO:**
- Title y meta description con keyword y ciudad.
- JSON-LD con `Person`, dirección, geo y horario.
- Fichas por tratamiento enlazadas desde el megamenú.

**Pie:** Instagram, Facebook, TikTok y enlace a Google Maps.

### Maeli
- **Menú mínimo:** botón «MENÚ» más un CTA fijo «Reservar valoración médica sin coste».
- **Método con nombre propio** (Maeli BluePrint™) contado en un acordeón de 9 pasos.
- **Botón flotante de WhatsApp** con el texto «Reservar mi valoración».
- **Dos vías de entrada:** «Una estrategia diseñada para lo que necesitas» (programas) y «También puedes comenzar por lo que estás buscando» (técnicas).
- **Carencias técnicas:**
  - Sin meta description.
  - Sin datos estructurados.
  - Varios H1 repetidos en el HTML: Framer duplica las versiones de escritorio y móvil.

## Qué adoptamos (y qué no)
| Patrón | Decisión en el prototipo v2 |
|---|---|
| Navegación por **especialidades** con foto (los «ateliers» de Garrigós; TACHA en la propuesta del cliente) | ✅ Menú: Estética · Medicina estética · Terapias · Bienestar · Conócenos, más el mosaico «01 / Nuestro universo» |
| CTA de cita siempre visible | ✅ **Reservar** y **Regalar** como botones separados en la cabecera |
| Método con nombre propio (Maeli) | ✅ «Cuídate · Conecta · Siente» como método en una banda morada, con la **valoración integral** como puerta de entrada |
| WhatsApp flotante | ✅ Pero pequeño y discreto: icono en morado de marca que se despliega al pasar el ratón. El verde de WhatsApp choca con la paleta |
| Buscador y filtros | ❌ Eliminados, como pide el cliente. Se navega por área, categoría y fichas, con índice de categorías en cada área |
| Antes/después y financiación en portada (Garrigós) | ❌ Riesgo legal en actos médicos (`cumplimiento-legal.md`). No se usa |
| «Valoración sin coste» como gancho (Maeli) | ⏸ Pendiente: el cliente aún no ha confirmado las condiciones de la valoración |
| Varios H1 o sin meta description (Maeli) | ❌ Un H1 por página, title ≤ 60 caracteres y meta description en todas |

## Siguiente paso
Cuando el proxy permita el acceso, completar el análisis de las 6 webs pendientes. Prioridades:
- **Hammam Al Ándalus y Be Aire:** flujo de regalo y reserva.
- **Aesop:** tono y tipografía.
- **SoKo:** competidor en Maisonnave 41.
