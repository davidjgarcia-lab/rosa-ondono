# Propuesta de stack y de sistema de reservas
*01-web · Entregable 7 · Responsable: programador · Revisión: project-manager, experto-seo, qa · Fecha: 17/11/2026*
*Estado: **PROPUESTA v0.1, pendiente de decidir con el cliente**.*

> **Aviso:** las prestaciones y precios de los proveedores de terceros cambian a menudo. Todo lo marcado con «(verificar en demo)» se confirma en una demo o prueba gratuita antes de decidir. No se han usado tarifas concretas para no dar cifras desactualizadas.

## 1. Requisitos que debe cumplir
Salen de los recorridos y de la arquitectura:

| # | Requisito | Origen |
|---|---|---|
| R1 | Unas 58 fichas con modelo de contenido estructurado, editables por el centro sin depender de la agencia | Arquitectura §6 |
| R2 | Reserva online en ≤ 3 pasos, con **servicio precargado desde cada ficha** (deep link por servicio) | Recorrido R1 |
| R3 | Agenda con **profesionales + recursos** (cabinas, láser, aparatología) para evitar solapes. Es configuración **interna** del software; la web pública no muestra ni asigna usos a las cabinas (decisión del cliente) | Operativa del centro |
| R4 | Bonos de sesiones y **tarjetas regalo vendibles online**, canjeables en la reserva | Recorrido R3 |
| R5 | Datos de salud (postoperatorio, médico): RGPD art. 9, servidores en la UE, contrato de encargado del tratamiento, consentimientos informados firmados | `cumplimiento-legal.md` |
| R6 | Medicina estética: solo se reserva la **consulta médica**; ficha clínica separada | Cumplimiento |
| R7 | Core Web Vitals en verde, Lighthouse ≥ 90 y WCAG 2.2 AA | Brief / programador |
| R8 | Las 301 del plan de migración, sitemap, schema y control total de title, meta y canonical | SEO |
| R9 | Cookies conformes y analítica solo con consentimiento | RGPD / LSSI |
| R10 | Coste de mantenimiento bajo y sin dependencia de un constructor visual (salir de Divi) | Auditoría |

## 2. Web: tres opciones

### Opción A · Astro (estático/híbrido) + CMS headless ← **recomendada**
- **Front:** Astro (HTML estático; JS solo donde haga falta: menú, reserva, filtros).
- **CMS:** hay que elegirlo en una demo con Rosa.
  - **Keystatic** o **Sveltia/Decap CMS**: contenido versionado en el repositorio y sin coste de licencia. El editor es sencillo, pero se edita con formularios, no de forma visual.
  - **Storyblok**: editor visual y vista previa; plan gratuito limitado. Hay que verificar en la demo el número de usuarios y la localización de los datos.
- **Hosting:** Netlify o Cloudflare Pages, con CDN, HTTPS y `_redirects` generado desde `seo/redirecciones-301.csv`.
- **Formularios:** endpoint propio (función serverless) o servicio con almacenamiento en la UE. Nada de enviar datos de salud por un formulario genérico.

| Pros | Contras |
|---|---|
| Rendimiento y CWV excelentes de serie (R7) | Requiere un desarrollador para cambios de plantilla (no de contenido) |
| Superficie de ataque mínima: sin plugins ni panel expuesto | El cliente estrena una herramienta de edición nueva (formación de 1 h) |
| Modelo de contenido a medida, idéntico a la arquitectura (R1) | Tienda de tarjetas regalo y reserva siempre externas (iframe, widget o enlace) |
| Schema, sitemap, 301 y canonical bajo control total (R8) | Vista previa de contenidos menos inmediata en Keystatic o Decap |
| Coste de hosting bajo o nulo; sin licencias de tema ni de builder (R10) | |

### Opción B · WordPress con tema de bloques propio (sin Divi)
- **Base:** WordPress, tema de bloques ligero a medida y CPT «Tratamiento» con campos (ACF o similar).
- **Plugins:** Yoast o Rank Math, y Redirection.
- **Reserva:** plugin (Amelia, Bookly) o widget del SaaS elegido.

| Pros | Contras |
|---|---|
| El cliente ya conoce WordPress; mucha autonomía | Mantenimiento continuo: actualizaciones, seguridad y copias de seguridad (riesgo real si nadie lo hace) |
| Migración de contenido del blog más directa | El rendimiento depende de la disciplina con los plugins; es fácil volver al estado actual |
| Ecosistema enorme (plugins de reservas con tarjetas regalo) | Si la reserva va por plugin, los datos de salud quedan en un hosting compartido: hay que reforzar seguridad y RGPD |
| | Hosting gestionado de calidad = coste mensual mayor |

### Opción C · Constructor SaaS (Webflow, Squarespace, Wix)
| Pros | Contras |
|---|---|
| Edición visual y hosting incluido | Dependencia del proveedor (*lock-in*) y coste recurrente por plan y CMS |
| Rápido de montar | Límites del CMS (colecciones y campos) y peor control de las 301 masivas y del schema |
| | Rendimiento y accesibilidad dependientes de la plataforma |

**Recomendación:** **Opción A.**
- Es la que mejor cumple R7, R8 y R10, y la que evita repetir los problemas de la web actual.
- Si en la demo el centro prefiere seguir con WordPress por autonomía, la **Opción B** es viable con dos condiciones: un contrato de mantenimiento y una lista cerrada de plugins.

## 3. Sistema de reservas

Antes de nada: **¿qué agenda usa hoy el centro?** (dato PENDIENTE en el brief). Si ya usan un software de gestión y les funciona, lo prioritario es **integrarlo** y no cambiarlo.

| Sistema | Tipo | Pros | Contras | Encaje |
|---|---|---|---|---|
| **Koibox** | Software español de gestión para estética y clínicas (SaaS) | Pensado para el sector: agenda por profesional y cabina, bonos, ficha de cliente, recordatorios, reserva online. Soporte en español. Probablemente consentimientos digitales (verificar en demo) | Suscripción mensual. Personalización del widget limitada. Deep link por servicio y venta online de tarjetas regalo: **verificar en demo** | ★★★ |
| **Flowww** | Software español de gestión para clínicas de medicina estética y centros de estética | Fuerte en la parte médica: historia clínica, consentimientos y trazabilidad. Agenda y recursos. Herramientas de marketing | Más orientado a clínicas medianas: coste y curva de aprendizaje mayores. Personalización del widget y deep links: verificar | ★★★ (si la medicina estética pesa mucho) |
| **Fresha** | Plataforma de gestión + marketplace | Software base sin cuota (modelo de comisiones por pagos y por clientes nuevos del marketplace: verificar las condiciones actuales). Widget, bonos y tarjetas regalo online | Marketplace que muestra a la competencia. Marca menos propia. Datos en la plataforma. No pensado para historia clínica | ★★ |
| **Treatwell** | Marketplace + software | Visibilidad y captación de cliente nuevo; muy conocido para regalos | Comisión por cliente nuevo. La clienta «es» de Treatwell. Guerra de precios contraria al posicionamiento | ★ (solo como canal de captación adicional, no como sistema principal) |
| **Doctoralia** | Agenda y directorio médico | Visibilidad para la **consulta médica** (perfil del Dr. Bravo Pardo) y reseñas médicas | Solo cubre la parte médica: obliga a sincronizar dos agendas | Complemento para R6 |
| **Plugin WP (Amelia / Bookly)** | Plugin (solo con la Opción B) | Pago único o anual; datos en tu servidor; muy personalizable | Mantenimiento propio. Datos de salud en WordPress: más responsabilidad de seguridad. Sin ficha clínica | ★★ (solo Opción B) |

### Recomendación de reservas
1. **Lista corta: Koibox y Flowww.** Demo con Rosa (30–45 min cada una) usando esta lista de comprobación:
   - [ ] Enlace o widget que **preselecciona un servicio** (`?servicio=`) → necesario para el CTA de cada ficha.
   - [ ] Agenda con recursos (cabina, láser) y profesionales.
   - [ ] Bonos y **tarjetas regalo vendidas online** con código canjeable en la reserva.
   - [ ] Servicios marcados como «solo consulta» o no reservables online.
   - [ ] Consentimientos informados con firma digital y ficha clínica (medicina estética, postoperatorio).
   - [ ] Datos alojados en la UE, contrato de encargado del tratamiento, exportación de datos (portabilidad y salida del proveedor).
   - [ ] Widget accesible (teclado, contraste) y que no penalice el rendimiento (carga diferida); si no, se usa el enlace a la página de reserva del proveedor.
   - [ ] Recordatorios por SMS, email o WhatsApp y política de cancelación configurable.
   - [ ] API o webhooks para medir la conversión `reserva_completada` (con consentimiento).
   - [ ] Coste total anual (licencia + SMS + pagos) y permanencia.
2. **Fresha** como alternativa de bajo coste si el presupuesto manda, asumiendo las limitaciones médicas.
3. **Doctoralia** opcional para la consulta médica, solo si el sistema elegido no sincroniza agenda o si se busca visibilidad médica.
4. **Treatwell:** no como sistema principal. Como mucho, un canal de captación de regalos, con control de precios.

### Integración en la web (cualquiera de las opciones)
- La página `/reservar/` es **nuestra**: cabecera simplificada, resumen y alternativas de teléfono y WhatsApp. Dentro carga el widget del proveedor con el servicio precargado.
- Si el widget no admite preselección o no es accesible, **plan B:** la ficha enlaza directamente a la URL de reserva de ese servicio en el proveedor (nueva pestaña con aviso), manteniendo el CTA contextual.
- Los wireframes (`arquitectura/wireframes/reserva.html`) describen la experiencia objetivo. El grado de control real sobre los pasos 2 y 3 depende del proveedor.

## 4. Resto del stack
| Pieza | Propuesta | Nota |
|---|---|---|
| Analítica | Plausible o Matomo (sin cookies, UE), o GA4 con Consent Mode v2 | Decidir con el project-manager según la necesidad de Google Ads |
| Cookies | CMP conforme (botones «Aceptar» y «Rechazar» al mismo nivel) | Bloqueo previo de scripts de terceros (mapas, vídeo, widget de reseñas) |
| Reseñas Google | Importación en build o con caché diaria (Places API) y render estático | Sustituye el widget actual, que penaliza el rendimiento |
| Mapa | Imagen estática + enlace «Cómo llegar»; mapa interactivo solo tras consentimiento | |
| Imágenes | Componente `<Image>` de Astro (AVIF/WebP, `srcset`, carga diferida) | Estilo y fotos: fotógrafo |
| Tipografías | Máximo 2 familias, autoalojadas, con `font-display: swap` | Las elige el manual (hoy hay 6) |
| WhatsApp | Enlace `wa.me` directo, sin plugin de chat | |
| Schema | JSON-LD generado desde el CMS | Según el keyword map §10 |
| Calidad | Lighthouse CI + pa11y/axe en cada despliegue y test automático del CSV de 301 | Responsable: qa |

## 5. Próximos pasos
1. **Cliente (vía ejecutivo-cuentas):**
   - Qué agenda usa hoy.
   - Quién editará la web y con qué frecuencia.
   - Presupuesto mensual orientativo para el software de reservas.
   - Acceso al WordPress actual.
2. **Demos de Koibox y Flowww** con la lista de comprobación (programador + Rosa).
3. **Decisión de stack** (project-manager) → prototipo técnico de una ficha y de `/reservar/` con el widget real.
4. **Design system:** el disenador-web lo arranca cuando el manual esté en borrador avanzado (rama `marca`).

---
**Qué he hecho:** requisitos, comparativa de tres stacks y seis sistemas de reservas, recomendación argumentada y lista de comprobación para las demos.

**Qué falta:** demos, precios reales y decisión con el cliente.

**Bloqueos:**
- Sistema de citas actual.
- Presupuesto.
- Accesos al WordPress actual.
