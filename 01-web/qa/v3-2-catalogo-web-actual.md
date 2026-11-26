# Web v3.2 · catálogo de la web actual + pulido con skills
*01-web · 26/11/2026* · **Enlace:** https://rosa-ondono-prototipo.vercel.app

## Contenido traído de rosaondono.com (descarga del 26/11/2026)
- **Fuente:** API pública de WordPress de la web actual:
  - las 8 páginas de servicios;
  - la home (listado completo y opiniones de Google);
  - «Sobre mí».
- **Tratamientos nuevos (8)**, migración `prototipo/supabase/006_catalogo_web_actual.sql`, generada con `generar_006.py`:
  - **Faciales:** reafirmación facial, piel sensible, higiene facial detox, ojeras y párpados, pieles con tendencia acneica.
  - **Corporales:** remodelación corporal.
  - **Masajes:** masaje deportivo y reflexología craneofacial.
- **Nombres alineados con la web actual:**
  - «Rejuvenecimiento facial»;
  - «Masaje relajante sedativo»;
  - «Reflexología podal»;
  - «Full face»;
  - «Depilación láser diodo y alejandrita», con sesiones orientativas sacadas de su FAQ.
- **Preguntas frecuentes por área:** 21, de faciales, corporales, masajes, terapias, depilación y medicina estética. Se muestran en cada página de área, con datos estructurados `FAQPage`.
- **Opiniones reales de Google:** 5, con nombre e inicial, solo sobre trato y ambiente.
- **Cita real de Rosa:** «Mi gran satisfacción es la expresión de mis clientes: su alegría y su felicidad.» Sustituye a una frase que no era suya.
- **Afirmaciones de la web actual que no se han copiado** (según `cumplimiento-legal.md`):
  - «resultados garantizados»;
  - «eliminación permanente»;
  - «refuerza el sistema inmunológico»;
  - «trata la ansiedad y la depresión»;
  - «estimula la curación»;
  - opiniones sobre tratamientos médicos.
- **Errores de la web actual que no se arrastran:** en su página de Belleza las descripciones de micropigmentación y maquillaje están copiadas de acupuntura, fisioterapia y magnetoterapia.

## Skills aplicadas
| Skill | Qué cambió |
|---|---|
| impeccable | Selección de texto, cursor de escritura, barra de desplazamiento y casillas con la paleta; cifras tabulares; flechas en SVG en lugar del carácter «→»; ficha sin el dato «Sesiones» vacío; titulares sin guiones de corte |
| web-design-guidelines | Sin `transition: all`; imagen de la carta con medidas; `autocomplete` en el campo «para quién»; `spellcheck="false"` en emails; `overscroll-behavior` en el menú; `theme-color` igual a la franja superior |
| emil-design-eng | Pulsación `scale(.97)` en 160 ms; efectos de hover solo con ratón; entrada de 240 ms del menú móvil |
| review-animations | Vista previa de la carta a 300 ms; con «reducir movimiento», las secciones aparecen con un fundido sin desplazamiento |
| break-ui | 78 páginas a 320 px sin desbordes; texto al 200 % sin recortes; día completo con su mensaje («Ese día ya está completo»); una sola hora libre; nombre y email larguísimos: todo resiste |

## Incidencia resuelta
El proyecto de Supabase se pausó solo el 26/11 tras 7 días sin actividad (plan gratuito), así que la web no podía guardar reservas. Se reactivó. Volverá a pausarse si pasa otra semana sin uso: en producción conviene el plan de pago o una visita periódica.

## Pruebas
- 27 pruebas funcionales en local: reserva rápida, validación, envío, carrusel, cabecera, escena fija, «reducir movimiento», sin JavaScript, 320 px y vista previa. Todas correctas.
- Pruebas de casos extremos (break-ui) correctas.
