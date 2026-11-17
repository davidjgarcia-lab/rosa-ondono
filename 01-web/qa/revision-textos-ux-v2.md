# Revisión de textos, solapes y UX · prototipo v1 → v2
*01-web · qa + experto-ux-ui + director-arte (criterios del manual v2.1) · 17/11/2026*

## Solapes con el icono (supergráfico)
| v1 | Problema | v2 |
|---|---|---|
| Tarjetas de pilar (inicio) | El isotipo pasaba por debajo del lema y de la lista | Los pilares dejan de ser tarjetas con supergráfico. El isotipo solo aparece en zonas sin texto: detrás de la foto de la portada, en el borde de la banda del método y en la tarjeta regalo |
| Cabecera de las páginas de pilar | El isotipo cruzaba el titular | Sin isotipo: cabecera con foto en arco |
| Retrato del equipo | El isotipo tapaba el texto «Retrato pendiente» | Bloque eliminado. El aviso de retratos pendientes pasa al texto de la sección |
| Tarjetas gráficas de tratamiento (nuevas) | Primera versión con el icono encima del isotipo | El icono va abajo a la izquierda y el isotipo recortado a la derecha. Comprobación automática: **0 solapes en 6 tarjetas** |
| Portada v2 (primera versión) | El isotipo invadía la columna del texto | Movido a la derecha, detrás de la foto |

Reglas del manual que se mantienen:
- El isotipo no se redibuja ni se recolorea; solo se usa en morado o en blanco.
- Se gira menos de ±12°.
- No va junto al logotipo grande.
- **Corrección:** en v1 llevaba opacidad (efecto no permitido). Ya no la lleva.

## Textos que quedaban raros
| v1 | Problema | v2 |
|---|---|---|
| «Personas con nombre y apellidos» | Frase hecha y fría | «Personas con nombre y formación» (solo en Conócenos) |
| H1 «Aumento de labios» + subtítulo suelto «en Alicante» | El subtítulo parecía un error de maquetación | H1 único: «Aumento de labios en Alicante» |
| Doble miga «Medicina estética · Medicina estética» | Duplicado | Corregido |
| Pastillas rojas de «Precio pendiente» y «Duración pendiente» en cada tarjeta | La web parecía rota | «Precio a consultar», y la duración no se muestra mientras falte. Los datos pendientes se listan en la barra del prototipo y en este documento |
| «Nota interna del prototipo» visible en las fichas | Mezclaba la revisión interna con la cara pública | Retirada de la web. Las revisiones siguen en la base de datos (`revision_pendiente`) y en la lista de abajo |
| Inicio: «Más de 30 años cuidando…» seguido de una bio que empieza igual | Repetición | Texto propio para la home |
| «Tres caminos para encontrar lo que buscas. Si ya sabes el nombre… búscalo en el listado» | Remitía al buscador, que se elimina | Mosaico de cuatro especialidades con fotografía |
| Hero v1: «Estética, manos expertas y medicina estética en el centro de Alicante» | Correcto pero frío | Propuesta del cliente: **«Tu bienestar empieza por ti.»** La keyword va en el antetítulo del H1: «Centro de estética y bienestar en Alicante» |
| «Muy agradable para la sensación de piernas cansadas» (presoterapia) | Aceptable | Se mantiene, sin promesas de resultado |

## Experiencia de usuario: cambios clave
1. **Sin buscador ni filtros.** Navegación por 4 especialidades. Cada área tiene un índice de categorías en pastillas y fichas con foto.
2. **Más gráfica:**
   - fotografía grande en arco;
   - mosaico de áreas;
   - tarjetas con foto, más tarjetas gráficas de marca intercaladas para no repetir imagen;
   - galería real del centro;
   - tarjeta regalo dibujada que se actualiza mientras escribes.
3. **Reservar y Regalar separados:**
   - en la cabecera, en cada ficha (Regalar solo en no médicos) y en el pie;
   - formularios distintos, guardados en tablas distintas de Supabase.
4. **Reserva en una sola pantalla** con tres bloques numerados, en lugar de un asistente por pasos. Más sencillo y funciona aunque falle JavaScript.
5. **WhatsApp pequeño y elegante:** círculo blanco con el icono en morado que se despliega a «WhatsApp». Se oculta mientras está abierto el aviso de cookies, para que no se superpongan.
6. **Aviso de cookies** con «Rechazar» y «Aceptar» al mismo nivel, más «Configurar» por categorías. Se puede reabrir desde el pie.
7. **Pie completo:**
   - Instagram y Facebook;
   - Google Maps (icono y enlace «Cómo llegar»);
   - horario;
   - contacto;
   - especialidades;
   - legales;
   - nº de registro sanitario (pendiente).

## Pendientes que no se pueden resolver sin el cliente
- **Datos de servicio:** precios, duraciones, condiciones de la valoración y validez de las tarjetas.
- **Datos sanitarios y de horario:** nº de colegiado, nº de registro sanitario y horario de invierno.
- **Profesionales sin confirmar** (no reservables en la web): fisioterapia, osteopatía y arañas vasculares.
- **Claims a retirar de la web actual:** radiofrecuencia «seguro», magnetoterapia «curación» y flores de Bach con ansiedad y depresión.
- **Fotos:**
  - Las de tratamientos son provisionales (Unsplash).
  - Falta la sesión propia y los retratos de Rosa y del médico.
  - Créditos en `../prototipo/LEEME.md`.
- **Textos legales:** aviso legal, privacidad y cookies los redacta el asesor legal.
