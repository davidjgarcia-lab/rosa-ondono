# Informe de QA · Entrega 1 · Redes sociales

*Fecha: 17/11/2026 · Revisa: qa · Rama: `redes` (sin commit ni push) · Fuentes de control: `../../CLAUDE.md`, `../../00-nucleo-marca/fuente-de-verdad.md`, `../../00-nucleo-marca/cumplimiento-legal.md`, `../../00-nucleo-marca/investigacion/` y `02-imagen-y-manual/espacios/mapa-del-centro.md` (origin/main).*

**Leyenda:** ✅ OK · ⚠️ mejora · ❌ bloqueante. «Corregido» = cambio aplicado por qa en el archivo. «Propuesta» = lo resuelve el responsable o el cliente.

> Todas las piezas siguen siendo **BORRADOR** y contienen `[PENDIENTE]` legítimos (precios, horarios, bonos, equipo, n.º de registro y de colegiado). Eso es correcto: ningún dato pendiente se ha inventado. **Ninguna pieza puede publicarse hasta sustituirlos.**

---

## 1. Resumen de veredictos

| Archivo | Veredicto | Motivo |
|---|---|---|
| `BRIEF.md` | ✅ tras corrección | Cifra de reseñas sin fuente (❌ corregido). |
| `auditoria/plantilla-auditoria-perfiles.md` | ✅ | Plantilla vacía a propósito; sin datos inventados; nombres de competidores coinciden con la investigación. |
| `estrategia/estrategia-por-plataforma.md` | ✅ con ⚠️ menores | Sin metas inventadas; cumplimiento bien recogido. |
| `estrategia/bio-y-highlights.md` | ⚠️ (pasa como borrador; no activar bios con «medicina estética» sin n.º de registro) | Recuentos verificados; añadida variante sin medicina estética. |
| `estrategia/protocolo-comunidad.md` | ✅ tras corrección | Deriva a consulta y al 112; RGPD correcto; eliminado «bótox». |
| `estrategia/shot-list-diciembre-2026.md` | ✅ tras corrección, con ⚠️ de producción | Códigos y plan de sesión actualizados; quedan solapes de horario y una prioridad. |
| `calendario/calendario-diciembre-2026.md` | ✅ tras corrección, con ⚠️ | Fechas y días correctos; códigos existen; dos ❌ de copy corregidos. |
| `plantillas/especificaciones-plantillas.md` | ✅ tras corrección | Medidas y contrastes verificados; alcance de bonos y sorteos alineados. |
| `plantillas/wireframes/*.svg` (7) | ✅ | XML válido (xmllint y ElementTree), grises neutros, sin isotipo ni color de marca. |

**Marca:** ✅ en ningún archivo se redibuja, recolorea ni simula el isotipo; el color corporativo se trata como PENDIENTE (#701B78 frente a #8E1F5C) y no se «fabrica» en foto ni en plantillas. Contrastes comprobados con script: #701B78/blanco 9,92:1 · #701B78/#E0E0E0 7,51:1 · #701B78/#333333 1,27:1 · #8E1F5C/blanco 8,40:1 (coinciden con lo documentado).

---

## 2. Legal (prioridad 1)

| # | Estado | Ubicación | Hallazgo | Corrección |
|---|---|---|---|---|
| L1 | ✅ | Todos | Cero sorteos o regalos de tratamientos médicos; bonos limitados a estética, masajes, rituales y terapias de bienestar; fisioterapia, osteopatía y acupuntura fuera hasta respuesta del asesor. | — |
| L2 | ✅ | Calendario §1 regla 4, D11, D14, D16; shot list §1, F09, F10 | El Dr. Bravo no aparece en ninguna pieza de bonos (F10 siempre «sin el doctor» en diciembre). | — |
| L3 | ✅ | Todos | Sin antes/después en diciembre; protocolo futuro correcto (shot list §9). | — |
| L4 | ✅ | Todos | Sin «resultados garantizados», «seguro», «sin efectos secundarios», claims curativos de terapias ni de aceites esenciales; D09 sin «elimina líquidos/toxinas». | — |
| L5 | ✅ | Calendario §1 regla 10, shot list §5.5, bio §3 | Fotos de Google Maps e imágenes IA explícitamente no publicables. | — |
| L6 | ✅ | Protocolo §5.2, P09b, `/ausencia` | Derivación a consulta y al 112 en urgencias; aviso al responsable sanitario. | — |
| L7 | ✅ | Protocolo §1.4, §8; shot list §7; F12, S05 | RGPD: datos mínimos por WhatsApp, sin datos de salud en el registro, sin pantallas con datos de clientes, cesiones de imagen y consentimientos separados. | — |
| L8 | ❌ → corregido | `protocolo-comunidad.md` §4 (árbol, «¿Es una pregunta de medicina estética…») y título de P12 | Aparecía «bótox» (nombre comercial de un medicamento de prescripción). | Sustituido por «nombre comercial de un medicamento» y «por su nombre comercial (p. ej. de toxina botulínica)». |
| L9 | ❌ → corregido | `calendario…` D13, copy, 2.º párrafo | «Pocas cosas sientan tan bien como salir a él después» prometía el uso del patio tras el tratamiento, que está [PENDIENTE] (incumplía la regla 11 del propio calendario). | Frase sustituida por un marcador [PENDIENTE] que solo la permite si el cliente lo confirma. |
| L10 | ❌ condicional → mitigado | `bio-y-highlights.md` §1.2 (A, B, C), §2 (Facebook), §3 (Google) | Las bios y la introducción citan la medicina estética como servicio sin n.º de registro sanitario; la opción B se activaría el 25/11, previsiblemente antes de tener el dato. | Añadida nota de QA y variante **B-sin-med** (131 caracteres, verificados). No activar ninguna versión con «medicina estética» hasta tener el n.º de registro y el criterio del asesor. |
| L11 | ⚠️ propuesta | Bio §4.1 frame 2, calendario E04 diapositiva 6, fuente de verdad | «Médico estético y nutricionista»: la medicina estética no es especialidad oficial en España y «nutricionista» puede confundirse con la profesión regulada de dietista-nutricionista. | Confirmar con el Dr. Bravo y el asesor la denominación exacta de sus títulos antes de publicar (p. ej. «Médico · Máster en Medicina Estética»). |
| L12 | ⚠️ propuesta | Estrategia §1 y shot list §5.5 | «Pocos centros del centro de Alicante tienen jardín»: afirmación comparativa sin fuente. | Uso solo interno; no trasladarla a ningún copy publicado (hoy ningún copy la usa). |

---

## 3. Datos inventados (prioridad 2)

| # | Estado | Ubicación | Hallazgo | Corrección |
|---|---|---|---|---|
| I1 | ❌ → corregido | `BRIEF.md`, «Punto de partida», 3.ª viñeta | «Más de 15 reseñas de 4,9★ con citas reutilizables (con permiso)»: la cifra no consta en la fuente de verdad ni en la investigación y el permiso no existe aún. | Reescrito: valoración 4,9★, n.º total [PENDIENTE], citas solo con permiso escrito. |
| I2 | ❌ → corregido | `calendario…` D15, texto GBP | «Te lo enviamos al momento» afirmaba un plazo de envío que está [PENDIENTE]. | «Te lo enviamos en [PENDIENTE: plazo]». |
| I3 | ⚠️ → corregido | `calendario…` D09, guion fila 3 | «Es cuando más nos lo piden» presentaba como dato una demanda estacional no medida. | «Hay quien nota las piernas más cargadas». |
| I4 | ⚠️ → corregido | `calendario…` D13, guion fila 3 | «Una hora en la que nadie te pide nada»: duración no confirmada. | «Un rato en el que nadie te pide nada». (D05 conserva «una hora» porque ya lleva [PENDIENTE: confirmar duración].) |
| I5 | ⚠️ → corregido | `estrategia-por-plataforma.md` §1 | «SoKo… con poca presencia digital»: la investigación solo habla de presencia web; sus redes no se han visto. | «Con poca presencia web localizable (sus redes no se han analizado)». |
| I6 | ✅ | Todos | Precios, horarios, n.º de registro y de colegiado, nombres del equipo, citas de reseñas, métricas y seguidores: siempre [PENDIENTE]. La landing `rosaondono.com/bonos-regalo/` figura como no existente con plan B de WhatsApp. Datos de contacto, dirección y biografía de Rosa coinciden con la fuente de verdad. | — |
| I7 | ✅ | D06 | Biografía (Sidi San Juan, Llongueras, naturopatía en Madrid, derivaciones de médicos de Alicante, Madrid y Barcelona) coincide con fuente de verdad y auditoría; la validación de Rosa está prevista. | — |

---

## 4. Coherencia (prioridad 3)

| # | Estado | Ubicación | Hallazgo | Corrección |
|---|---|---|---|---|
| C1 | ✅ | Calendario §2, §2.1, §5 | Comprobadas con script las 25 fechas de diciembre de 2026 y enero de 2027: todos los días de la semana son correctos (1/12 martes, 6/12 domingo, 8/12 martes, 22/12 martes, 24/12 jueves, 6/01 miércoles…). | — |
| C2 | ✅ | Calendario (todas las fichas y §6) | Todos los códigos usados existen en el shot list (R01–R12, F01–F19, S01–S11, G01–G06). | — |
| C3 | ⚠️ → corregido | Calendario §0; shot list cabecera | Ambos documentos declaraban como rango estable R01–R10, F01–F15, S01–S10, G01–G05, pero el calendario usa R11, R12, F16–F19, S11 y G06. | Rangos actualizados en los dos archivos. |
| C4 | ⚠️ → corregido | Shot list, cierre | «40 planos»: son 50 tras la ampliación del 17/11. | Corregido. |
| C5 | ✅ | Calendario §2 | Pilares de diciembre verificados: Cuídate 3, Conecta 6, Siente 6 (20/40/40 %, coincide con estrategia §4); formatos 7 reels, 4 carruseles, 4 posts; reparto semanal 3·3·4·3·2. Medicina estética nunca en Siente (E04 en Cuídate). | — |
| C6 | ⚠️ → corregido | Calendario §2, «Fuera del feed», y cierre | Facebook recibe 15 piezas (todas salvo D10), no 14; Google recibe 4 publicaciones (D01, D08, D12, D15) más horarios especiales, no 5. | Corregido en los dos sitios. |
| C7 | ✅ | `bio-y-highlights.md` | Recuentos verificados con script (Python, NFC, saltos de línea incluidos): nombres 44 y 43; bios A 132, B 140, C 126; Facebook 92; Google 730. Todos coinciden. | — |
| C8 | ⚠️ propuesta | Bio §4 (destacado 5) y plantillas §6.1 (destacado 5) | «Med. estética» tiene 13 caracteres (la propia regla pide ≤ 12) y «Medicina estética» tiene 17 (Instagram corta los nombres de destacado a 15). | Elegir un nombre de ≤ 12 caracteres (p. ej. «Medicina»), decisión de redes y director-arte. |
| C9 | ⚠️ propuesta | Bio §4.2 frente a plantillas §6.1; shot list R11 | Dos criterios de destacados (por servicio o por pilar) y R11 cita la portada de «El centro», que en la propuesta de redes se llama «Info». | Decisión pendiente (director-arte y cliente); después, unificar el nombre en el shot list. |
| C10 | ⚠️ → corregido | Shot list §4 frente a §5.5 | La ampliación movía la fachada a 08:15-09:00 y añadía el patio a 09:00-09:30, pero la tabla del plan seguía con 07:45-08:30 y 08:30-09:30 (solape con el montaje). Además, el ocaso a finales de noviembre en Alicante es hacia las 17:45, no 17:55. | Tabla actualizada (07:45-08:15 montaje, 08:15-09:00 fachada, 09:00-09:30 patio) y hora del ocaso corregida. |
| C11 | ⚠️ propuesta | Shot list §5.5 «Cambios en el plan» | R12 y F17 en el patio de 13:00 a 13:30 se solapan con el bloque de cabina (10:45-13:30). | Fotografo: mover a 13:30-14:15 (antes de comer) o a las 16:00. |
| C12 | ⚠️ propuesta | Shot list F19 (prioridad B) frente a calendario §6, D02 (necesario antes del 30/11) | Las prioridades B se entregan antes del 5/12; F19 y su alternativa F05 no llegarían para D02. | Subir F19 a prioridad A o usar F04 (A) como alternativa en D02. |
| C13 | ⚠️ propuesta | Calendario D02 diapositiva 4 y D05 diapositiva 6 | Se usa F08 (manos de Rosa sobre hombros o espalda) para «tratamientos faciales» y para «masaje de piernas o drenaje». | D02: fotograma de R05 o F06; D05: fotograma de R06 o F14. Alt text de D02 ya ajustado a lo que muestra F08. |
| C14 | ⚠️ propuesta | Plantillas §2.3 (reserva inferior de story 320 px) frente a shot list §3 ZS-S (340 px) | Discrepancia de 20 px. | Unificar en 340 px (y 1580), la opción más conservadora. |
| C15 | ⚠️ → corregido | Calendario §0, «Plantillas» | Decía que el recorte 3:4 de la rejilla quita las franjas superior e inferior; en un 4:5 recorta los laterales (≈ 34 px por lado), como dicen plantillas y shot list. | Corregido. |
| C16 | ⚠️ → corregido | Plantillas §9.3 | Exportación de vídeo a 30 fps frente a rodaje a 25p (red de 50 Hz). Convertir de 25 a 30 fps provoca tirones. | 25 fps. |
| C17 | ⚠️ → corregido | Plantillas §7 (bono) y §7.3 | Alcance del bono «estética y terapias complementarias» incluía de forma implícita fisioterapia, osteopatía y acupuntura; §7.3 contemplaba sorteos de bono sin recoger la recomendación de no hacerlos. | Alineado con estrategia §7 y calendario §1. |
| C18 | ✅ | Plantillas §2 | Medidas verificadas: 1012 × 1350 visible en rejilla (34 px/lado); portada de reel y 240–1680 (3:4) e y 285–1635 (4:5), intersección con margen y 375–1545; GBP 900 × 750 centrado; tarjeta 85 × 55 + 3 mm = 91 × 61; avatar 60 % de 1080 ≈ 650 px; caja de firma 80 × 108 (proporción 0,74 del PNG). | — |

---

## 5. Ortografía, gramática y tono (prioridad 4)

| # | Estado | Ubicación | Hallazgo | Corrección |
|---|---|---|---|---|
| T1 | ⚠️ → corregido | Shot list (11 casos) y plantillas | «Nº» y «nº» sin punto. La abreviatura correcta (RAE) es «n.º» / «N.º». | Corregido en todos los casos. |
| T2 | ⚠️ → corregido | Shot list §2.3, §11, §4 | «postproducción» mezclado con «posproducción» (preferida por la RAE); «Naming de archivos»; «community». | «Posproducción», «Nomenclatura de archivos», «gestora de la comunidad». |
| T3 | ⚠️ → corregido | Calendario D01, fila 1 | Rótulo «Regala tiempo para cuidarte» frente a la voz «tiempo para cuidarse» (quien recibe el regalo es otra persona). | «Regala tiempo para cuidarse». |
| T4 | ⚠️ → corregido | Protocolo P09b | «Lo estamos avisando en este momento»: referente ambiguo. | «Estamos avisando al médico en este momento». |
| T5 | ⚠️ propuesta | Calendario D02 («juntas»), D05 («nosotras»), D11 («Ellas»); protocolo P02 («Encantadas») | Marcas de femenino que excluyen a clientes hombres (el shot list busca ampliar a ese público) y quizá a parte del equipo. | Decisión del cliente ya listada; recomendación de qa: formas neutras («lo vemos contigo», «el equipo», «Qué alegría verte por aquí»). |
| T6 | ⚠️ propuesta | Bio §3 (descripción de Google) | «Rosa Ondoño es un centro… Rosa Ondoño lleva…»: repetición que confunde centro y persona. | «…en la avenida Maisonnave de Alicante. Su fundadora, Rosa, lleva más de 30 años…» (recontar caracteres). |
| T7 | ✅ (opcional) | Calendario D06 («escucharle», «que le escuchen… le traten») | Leísmo de persona masculino singular, admitido por la RAE. | Opcional: «escucharla o escucharlo» si se quiere una norma más estricta. |
| T8 | ✅ | Todos | Tono cercano, experto y sereno; sin clichés de spa (prohibidos expresamente en shot list §2.5); sin exclamaciones en cadena ni emojis. | — |

---

## 6. Accesibilidad (prioridad 5)

| # | Estado | Ubicación | Hallazgo | Corrección |
|---|---|---|---|---|
| A1 | ✅ | Calendario D01–D16 y E04 | Todas las piezas de diciembre llevan texto alternativo. | — |
| A2 | ⚠️ → corregido | Calendario §0 | Los subtítulos solo figuraban en el checklist final, no por pieza. | Añadida regla: reels con voz (D01, D03, D09, D11 si lleva voz, D14, E03) con subtítulos incrustados y .srt; reels sin voz con transcripción en el alt text. |
| A3 | ⚠️ → corregido | Calendario D02 | El alt text describía «un gesto de cuidado facial» sobre F08, que muestra manos en los hombros. | Ajustado a lo que muestra la foto. |
| A4 | ⚠️ propuesta | Calendario §5, E01–E03 | Las piezas de enero aún no tienen alt text ni copy completo. | Redactarlos al cerrar las fichas de enero (antes del 22/12). |
| A5 | ⚠️ propuesta | Wireframes `post-4x5-1080x1350.svg` y `gbp-publicacion-1200x900.svg` | Elementos `<text>` vacíos en las bandas rayadas (inocuos, pero los lectores de SVG los anuncian). | Eliminarlos o rellenarlos con la leyenda («Recorte de rejilla»). |
| A6 | ✅ | Plantillas §8 | Contraste ≥ 4,5:1 en todo texto, ≥ 3:1 en gráficos, subtítulos incrustados de 2 líneas, sin destellos, sin letras Unicode «de fantasía», información no solo por color. | — |

---

## 7. Redes y formatos

| # | Estado | Ubicación | Hallazgo |
|---|---|---|---|
| R1 | ✅ | Plantillas §2, shot list §3 | Medidas por plataforma correctas (4:5 1080 × 1350, 9:16 1080 × 1920, GBP 4:3 1200 × 900, avatar 1080 × 1080, portada FB 1640 × 624). Zonas seguras definidas y coherentes salvo C14. |
| R2 | ✅ | Shot list §7.5 | Música solo con licencia comercial (biblioteca restringida en cuentas de empresa). |
| R3 | ✅ | Estrategia §5.1 | Hashtags sin marcas de medicamentos ni antes/después; de 3 a 5 por pieza. |
| R4 | ✅ | Wireframes | 7 SVG válidos: avatar 1080², bono 91 × 61 mm (viewBox a 10 u/mm), GBP 1200 × 900, highlight, post, portada de reel y story 1080 × 1920; todos con `<title>`. |

---

## Qué he hecho
- He leído `CLAUDE.md`, la fuente de verdad, el checklist legal, la investigación y el mapa del centro (origin/main), y he revisado los 8 documentos y los 7 SVG de `03-redes-sociales/`.
- He verificado con scripts los días de la semana (25 fechas), los recuentos de caracteres de nombres, bios, introducción y descripción, los contrastes de color, la validez XML de los SVG y la correspondencia de códigos entre el calendario y el shot list.
- He corregido directamente 4 bloqueantes (I1, I2, L8, L9), he mitigado L10 con una variante de bio y he aplicado 16 mejoras mecánicas (fechas y horarios del plan de sesión, rangos de códigos, recuentos, abreviaturas, terminología, alt text, regla de subtítulos y alcance del bono). Todo en la rama `redes`, sin commit ni push.

## Qué falta
- Responsables: decidir nombres de destacados ≤ 12 caracteres y criterio (C8, C9); solapes y prioridad del shot list (C11, C12); imágenes de D02 y D05 (C13); zona inferior de story (C14); descripción de Google (T6); alt text y copys de enero (A4); limpiar `<text>` vacíos de los SVG (A5).
- Todos los `[PENDIENTE]` del cliente siguen bloqueando la publicación: catálogo y condiciones de bonos, fechas límite, horario de invierno y festivos, precios, reseñas con permiso, equipo y cesiones, landing de bonos, fecha de la sesión, n.º de registro sanitario y n.º de colegiado.
- Revisión de qa de segunda vuelta sobre cada pieza final (con imagen real, subtítulos y alt text) antes de su programación, y sobre el manual cuando se apruebe (paleta, tipografías, logo).

## Decisiones que necesita el cliente (vía ejecutivo-cuentas)
1. N.º de registro sanitario del centro, n.º de colegiado del Dr. Bravo y si la Comunitat Valenciana exige autorización previa de publicidad sanitaria. Hasta entonces, bio y perfiles **sin** «medicina estética» (variante B-sin-med).
2. Denominación exacta de los títulos del Dr. Bravo («médico estético», «nutricionista») para la información pública (L11).
3. Si el patio se usa después de los tratamientos en invierno (D13, R12).
4. Tono femenino o neutro en copys y respuestas (T5).
5. Criterio de los destacados (por servicio o por pilar) y nombre del de medicina estética.
6. Si fisioterapia, osteopatía y acupuntura pueden ir en bonos (pendiente del asesor).
7. Color corporativo oficial (#701B78 o #8E1F5C), Pantone, CMYK y logo vectorial.
