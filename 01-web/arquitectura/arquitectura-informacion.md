# Arquitectura de información y mapa del sitio
*01-web · Entregable 3 · Responsables: experto-ux-ui + experto-seo · Fecha: 17/11/2026*
*Estado: **BORRADOR v0.1**. Los nombres de los programas son de trabajo y los cerrará el manual de marca (rama `marca`, experto-marketing-comunicacion).*

## 1. Principios
1. **Dos puertas al mismo catálogo:**
   - **por necesidad** («¿Qué necesitas?»): programas agrupados en Cuídate · Conecta · Siente;
   - **por técnica** («Tratamientos»): para quien ya sabe lo que busca.

   Las dos llevan a las mismas fichas.
2. **Una URL = un tratamiento = una intención de búsqueda.** Se acabó agrupar 12 tratamientos médicos en una sola página.
3. **La medicina estética tiene espacio propio.** Es actividad sanitaria, la realiza el médico identificado, lleva sus propios avisos legales y su CTA es la consulta previa.
4. **Tres accesos de conversión fijos:** Valoración integral (empieza aquí) · Regala · Reservar.
5. **Profundidad máxima de 3 clics** desde la home hasta cualquier ficha y **3 pasos** en la reserva.
6. **Fichas consolidadas cuando no hay contenido propio:**
   - Ejemplos: las mascarillas se integran en limpieza o hidratación; la reflexología podal y la craneofacial comparten ficha.
   - Motivo: evitar páginas vacías de una línea, como pasa hoy.

## 2. Mapa del sitio (propuesto)

```
/                                         Home
├── /valoracion-integral/                 Landing «Empieza aquí» (R2)
│
├── /cuidate/                             Pilar CUÍDATE · piel, cuerpo, belleza
│   ├── /cuidate/rejuvenecimiento-facial/ Programa «Piel luminosa / well-aging»
│   ├── /cuidate/silueta-y-piernas-ligeras/ Programa corporal sin cirugía
│   ├── /cuidate/belleza-esencial/        Depilación, manos y pies, micropigmentación, maquillaje
│   └── (enlace destacado a /medicina-estetica/)
├── /conecta/                             Pilar CONECTA · manos expertas y terapias
│   ├── /conecta/dolor-y-tension/         Programa espalda, cervicales, contracturas
│   ├── /conecta/pre-y-postoperatorio/    Landing especialidad (P5) ★ prioridad SEO
│   └── /conecta/equilibrio-emocional/    Programa bienestar emocional (sin claims de curación)
├── /siente/                              Pilar SIENTE · rituales y experiencias
│   ├── /siente/ritual-en-pareja/
│   ├── /siente/ritual-individual/
│   ├── /siente/circuito-spa/
│   └── /siente/experiencia-beauty/
│
├── /tratamientos/                        Índice por técnica (filtrable por categoría y necesidad)
│   ├── /tratamientos/faciales/           Categoría
│   ├── /tratamientos/corporales/         Categoría
│   ├── /tratamientos/masajes/            Categoría
│   ├── /tratamientos/terapias-complementarias/ Categoría
│   ├── /tratamientos/depilacion/         Categoría
│   ├── /tratamientos/belleza/            Categoría (micropigmentación, manos y pies, maquillaje)
│   └── /tratamientos/{slug}/             FICHA (plana: un tratamiento puede estar en varias categorías)
│
├── /medicina-estetica/                   Hub médico (Dr. Roberth Bravo Pardo)
│   ├── /medicina-estetica/consulta-medica/  Consulta previa obligatoria (R2b)
│   └── /medicina-estetica/{slug}/        FICHA médica
│
├── /tarjeta-regalo/                      Compra de tarjeta (R3)
├── /reservar/                            Reserva (R1), acepta ?servicio={slug}
├── /precios/                             Tarifas «desde» (estética, masajes, terapias; médico: «tras consulta»)
├── /equipo/                              Rosa y el equipo
│   ├── /equipo/rosa-ondono/              Fundadora (Person, E-E-A-T)
│   └── /equipo/dr-roberth-bravo-pardo/   Médico (Person/Physician, nº colegiado PENDIENTE)
├── /el-centro/                           Espacio, historia, cómo llegar (Av. Maisonnave 38)
├── /opiniones/                           Reseñas (Google) — opcional fase 2
├── /blog/                                Blog (artículos en /blog/{slug}/)
│   └── /blog/tema/{tema}/                Archivo por tema (piel, cuerpo, bienestar, medicina-estetica)
├── /preguntas-frecuentes/
├── /contacto/
└── Legales: /aviso-legal/ · /privacidad/ · /cookies/ · /accesibilidad/ · /condiciones-tarjeta-regalo/
```

> ⚠️ **Hallazgo:** en el rastreo no se ha localizado ninguna página de aviso legal, privacidad ni cookies: dan 404 y no están enlazadas. Hay que verificarlo con el cliente. Si se confirma, es un incumplimiento de la LSSI y del RGPD que conviene corregir ya en la web actual.

**Slugs reservados** en `/tratamientos/`: `faciales`, `corporales`, `masajes`, `terapias-complementarias`, `depilacion`, `belleza`. Ninguna ficha puede usarlos.

## 3. Navegación

### Cabecera (escritorio)
```
[Logo]  ¿Qué necesitas? ▾   Tratamientos ▾   Medicina estética   Rosa y el equipo   Regala      ☎  WhatsApp  [Reservar]
```
- **¿Qué necesitas?** abre un megamenú de 3 columnas (Cuídate / Conecta / Siente), con los programas de cada pilar. Al pie, una tarjeta «¿No sabes por dónde empezar? → Valoración integral».
- **Tratamientos** abre un megamenú por categoría técnica, con 5–8 enlaces por columna y el enlace «Ver todos».
- **Reservar** es el botón primario y está siempre visible.

### Móvil
- Cabecera con logo, ☰, y el teléfono o WhatsApp como icono.
- **Barra inferior fija:** `[Reservar]` + `[WhatsApp]`. En las fichas médicas cambia a `[Pedir consulta médica]`.
- El menú ☰ es un acordeón con el mismo orden que en escritorio.

### Pie
- NAP completo: Av. Maisonnave 38, Entlo. Izq., 03003 Alicante · 965 120 300 · 691 315 622.
- Horario de verano y de invierno (el de invierno está PENDIENTE).
- Mapa.
- Redes sociales.
- Nº de registro sanitario (PENDIENTE).
- Enlaces legales.
- Lema.

### Migas de pan (en todas las páginas internas)
`Inicio › Tratamientos › Faciales › Dermapen` · `Inicio › Conecta › Pre y postoperatorio`

## 4. Programas por pilar (necesidad → fichas)
| Pilar | Programa (nombre de trabajo) | Para quién | Fichas que agrupa |
|---|---|---|---|
| **Cuídate** | Rejuvenecimiento facial («Piel luminosa») | P1 | Limpieza profunda, hidratación, peeling, microdermoabrasión, radiofrecuencia facial, Dermapen, facial antiedad · + médicos: bioestimulación, hidratación médica |
| Cuídate | Silueta y piernas ligeras | P1, P5 | Tratamiento reductor, anticelulítico, reafirmación, presoterapia, vacumterapia, cavitación, radiofrecuencia corporal, lipoláser, Detox integral, arañas vasculares |
| Cuídate | Belleza esencial | Todos | Depilación láser, Skin's Brazilian, micropigmentación, micropigmentación oncológica, manos y pies, maquillaje de ceremonia |
| Cuídate | → Medicina estética (hub propio) | P2 | 12 fichas médicas (§5) |
| **Conecta** | Dolor y tensión | P3 | Masaje terapéutico, descontracturante, fisioterapia, osteopatía, miofascial, terapia manual, electroestimulación, onda corta, magnetoterapia |
| Conecta | Pre y postoperatorio ★ | P5 | Drenaje linfático pre y postoperatorio, presoterapia, radiofrecuencia corporal (fase de recuperación), masaje miofascial |
| Conecta | Equilibrio emocional | P4 | Somatoemocional, craneosacral, acupuntura, moxibustión, reflexología, flores de Bach, linfodrenaje energético, masaje ayurvédico |
| **Siente** | Rituales y desconexión | P3, P6 | Ritual individual, ritual en pareja, circuito spa, Experiencia Beauty, masaje relajante, balneoterapia |
| Siente | Regala | P6 | Tarjeta regalo (experiencia o importe) |

**Cada programa** es una página con estos bloques:
1. La necesidad, contada en la voz de la clienta.
2. Cómo lo abordamos: Rosa y su método.
3. Fichas recomendadas: 3–6 tarjetas.
4. Un plan orientativo, con sesiones y combinaciones.
5. Testimonios.
6. Preguntas frecuentes.
7. CTA: Valoración integral o Reservar.

## 5. Inventario de fichas (fase 1)
Leyenda: ★ prioridad SEO alta · ⚕️ médica · ⚠️ revisar quién la realiza o el claim antes de publicar.

**Faciales:**
- `limpieza-facial-profunda` ★
- `tratamiento-facial-antiedad`
- `hidratacion-facial`
- `peeling-facial`
- `microdermoabrasion`
- `radiofrecuencia-facial` ★ (retirar el claim «seguro»)
- `dermapen` ★

**Corporales:**
- `tratamiento-reductor`
- `tratamiento-anticelulitico` ★
- `reafirmacion-corporal`
- `presoterapia` ★
- `vacumterapia`
- `cavitacion` ★
- `radiofrecuencia-corporal`
- `lipolaser`
- `detox-integral`
- `aranas-vasculares` ⚠️ (confirmar la técnica; si es esclerosis o láser vascular, pasa a medicina estética)

**Masajes:**
- `masaje-relajante` ★
- `masaje-terapeutico`
- `masaje-descontracturante` ★
- `masaje-ayurvedico`
- `drenaje-linfatico` ★
- `drenaje-linfatico-postoperatorio` ★★
- `linfodrenaje-energetico`
- `reflexologia` (podal y craneofacial)

**Terapias complementarias:**
- `fisioterapia` ⚠️ y `osteopatia` ⚠️: confirmar el fisioterapeuta colegiado que las realiza; la fisioterapia es profesión sanitaria regulada.
- `acupuntura` ★
- `moxibustion`
- `terapia-somatoemocional`
- `terapia-craneosacral`
- `terapia-miofascial`
- `terapia-manual`
- `magnetoterapia` ⚠️ (retirar «curación»)
- `electroestimulacion`
- `onda-corta`
- `balneoterapia`
- `flores-de-bach` ⚠️ (retirar el claim de ansiedad y depresión)

**Depilación y belleza:**
- `depilacion-laser` ★★ (alejandrita y diodo)
- `depilacion-skins-brazilian`
- `micropigmentacion` ★
- `micropigmentacion-oncologica` ★ (nicho de alto valor social; tratar con sensibilidad)
- `manicura-y-pedicura`
- `maquillaje-de-ceremonia`

**Medicina estética** (⚕️, en `/medicina-estetica/{slug}/`). Las fichas se nombran por la **indicación** y no por la marca del producto:
- `consulta-medica`
- `armonizacion-facial` (full-face)
- `hilos-tensores` ★
- `aumento-de-pomulos`
- `rinomodelacion` ★
- `menton`
- `marcado-mandibular`
- `flacidez-facial`
- `flacidez-corporal`
- `hidratacion-facial-medica`
- `bioestimulacion-de-colageno` ★
- `aumento-de-labios` ★★
- `arrugas-de-expresion` ★★ (toxina botulínica: contenido informativo, sin marcas comerciales; validación legal previa)

**Siente:**
- `ritual-en-pareja` ★
- `ritual-individual`
- `circuito-spa`
- `experiencia-beauty`

**Total:** unas 58 fichas. **Fase 1 de lanzamiento:** las 25 marcadas con ★, más las médicas, más los rituales. El resto se publica en las 6 semanas siguientes al lanzamiento, siempre con contenido completo; no se publica una ficha vacía.

## 6. Modelo de contenido de la ficha (para el CMS)
| Campo | Tipo | Obligatorio | Nota |
|---|---|:-:|---|
| Nombre | texto | ✔ | H1 |
| Slug | texto | ✔ | sin «alicante» (la señal local va en title, contenido y GBP) |
| Pilar(es) / Programa(s) | relación | ✔ | navegación por necesidad |
| Categoría técnica | relación | ✔ | navegación por técnica |
| Tipo | enum: estética · terapia · médico | ✔ | si es «médico», activa los avisos, el CTA de consulta y la firma del médico |
| Resumen (lead) | texto 160–220 car. | ✔ | también se usa para la meta description |
| Para quién es / no es | lista | ✔ | |
| Cómo es la sesión | rich text | ✔ | |
| Duración (min) | número | ✔ | |
| Sesiones orientativas | texto | ✔ | «Orientativo: depende de la valoración» |
| Precio desde (€) | número | — | médico: «tras consulta» |
| Profesional | relación (Persona) | ✔ | foto, nombre, cualificación |
| Contraindicaciones / precauciones | rich text | ✔ en médico y aparatología | |
| FAQ | lista P/R | ✔ (mín. 3) | FAQPage |
| Relacionados | relación | — | 3 fichas |
| ID del servicio en el sistema de reservas | texto | ✔ si es reservable | precarga `/reservar?servicio=` |
| Reservable online | booleano | ✔ | `false` en médico, que lleva a consulta |
| Imagen principal + alt | imagen | ✔ | estilo del fotógrafo (manual) |
| Revisión legal | fecha + responsable | ✔ en médico | lo bloquea el flujo de publicación |

## 7. Enlazado interno
- **Ficha →** su programa, su categoría, 3 fichas relacionadas, el profesional, la valoración integral y la reserva.
- **Programa →** sus fichas, el pilar, la valoración integral y los artículos del blog del tema.
- **Blog →** como mínimo 1 ficha y 1 programa en contexto. Cada artículo lleva autor con su página de equipo. Los temas médicos los firma o revisa el médico.
- **Home →** los 3 pilares, la valoración integral, las 6 fichas más demandadas, Rosa y el médico, reseñas y regalo (estacional).

---
**Qué he hecho:**
- Mapa del sitio con doble navegación.
- Programas por pilar.
- Inventario de unas 58 fichas con prioridades.
- Modelo de contenido para el CMS.
- Reglas de enlazado.

**Qué falta:**
- Validar los nombres de los programas con el manual.
- Confirmar quién realiza la fisioterapia, la osteopatía y el tratamiento de arañas vasculares.
- Test de *card sorting* con clientas.

**Bloqueos (PENDIENTE del cliente):**
- Registro sanitario.
- Nº de colegiado.
- Precios.
- Horario de invierno.
- Páginas legales actuales.
