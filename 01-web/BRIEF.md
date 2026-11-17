# BRIEF · Rediseño web
**Objetivo:** web nueva que transmita la marca renovada, genere reservas/consultas y mejore el posicionamiento local.

| # | Entregable | Responsable | Estado |
|---|---|---|---|
| 1 | Auditoría de la web actual (UX, contenido, SEO, rendimiento) + inventario de URLs | experto-ux-ui + experto-seo | Pendiente |
| 2 | Perfiles de cliente y flujos de reserva | experto-ux-ui | Borrador v0.1 → `investigacion/perfiles-y-recorridos.md` |
| 3 | Mapa del sitio y arquitectura SEO | experto-ux-ui + experto-seo | Borrador v0.1 → `arquitectura/arquitectura-informacion.md` · `seo/keyword-map-alicante.md` (volúmenes pendientes) |
| 4 | Wireframes páginas clave | experto-ux-ui | Baja fidelidad v0.1 (home, ficha, reserva) → `arquitectura/wireframes/` |
| 5 | Design system web (tokens + componentes) | disenador-web | Bloqueado por manual |
| 6 | Maquetas alta fidelidad | disenador-web | Bloqueado por manual |
| 7 | Propuesta de stack y reservas | programador | Propuesta v0.1 → `codigo/propuesta-stack-y-reservas.md` (pendiente de demos) |
| 8 | Desarrollo + contenidos + datos estructurados | programador + experto-seo | — |
| 9 | QA completo y plan de redirecciones 301 | qa + experto-seo | Plan 301 v0.1 → `seo/plan-redirecciones-301.md` + `.csv` · QA: — |
| 10 | Lanzamiento y seguimiento 30 días | project-manager | — |

**Necesitamos del cliente:** URL actual y accesos, listado de tratamientos y precios, sistema de citas actual, fotos disponibles.

## Punto de partida (investigación 17/11/2026)
- Ver `../00-nucleo-marca/investigacion/auditoria-web-actual.md` (WordPress + Divi, 25 URLs, más de 60 servicios sin jerarquía, sin reserva online).
- Prioridades:
  - Reserva online.
  - Navegación por necesidad y por técnica.
  - Una ficha por tratamiento.
  - Rosa y el médico en primer plano.
  - Landing de «Valoración integral».
  - Mapa 301 de las URLs actuales.
- Retirar los claims de riesgo legal («Resultados garantizados», «poder curativo», flores de Bach para depresión).

## Avance 17/11/2026 (rama `web`)
Recomendaciones (pendientes de decisión):
- **Web:** Astro + CMS headless.
- **Reservas:** demo de Koibox y Flowww.

Nuevos pendientes del cliente:
- **Agenda actual.**
- Quién edita la web.
- Presupuesto del software de reservas.
- Condiciones de la valoración integral.
- Validez de las tarjetas regalo.
- Política de cancelación.
- Quién realiza la fisioterapia y la osteopatía (profesión sanitaria).
- Técnica de arañas vasculares.
- Accesos a Search Console, GBP y WordPress.

⚠️ No se localizan páginas de aviso legal, privacidad ni cookies en la web actual (404): hay que avisar al cliente ya.
