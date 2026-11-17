# Proyecto Rosa Ondoño — Rebranding y rediseño web

Idioma de trabajo: **español (España)**. Todos los entregables, comentarios y textos en español.

## La marca
- **Nombre:** Rosa Ondoño
- **Lema:** *Cuídate · Conecta · Siente*
- **Ubicación:** Av. Maisonnave 38, Alicante · rosaondono.com · @rosaondono
- **Actividad:** centro de estética, terapias complementarias y medicina estética.
- **Objetivo del proyecto:** rebranding completo + rediseño integral de la web.

## Reglas inamovibles
1. **El icono (isotipo) NO se modifica.** Se puede reordenar su relación con el logotipo, definir versiones (horizontal, vertical, reducida), áreas de respeto y tamaños mínimos, pero nunca redibujar, deformar, recolorear ni añadir efectos.
2. **El color corporativo NO se modifica.** Se documenta con precisión (Pantone, CMYK, RGB, HEX) y se construye la paleta secundaria *alrededor* de él.
3. Los valores exactos del icono y del color están en `00-nucleo-marca/fuente-de-verdad.md`. Si figuran como PENDIENTE, ningún agente puede inventarlos: se pide el dato al cliente vía ejecutivo de cuentas.
4. Comunicación sanitaria responsable: la medicina estética es actividad sanitaria. Ver `00-nucleo-marca/cumplimiento-legal.md` antes de publicar cualquier texto, imagen o campaña.

## Estructura (un apartado por línea de trabajo)
| Carpeta | Línea de trabajo | Responsable principal |
|---|---|---|
| `00-nucleo-marca/` | Fuente de verdad, cumplimiento e `investigacion/` (auditoría web y competencia) | project-manager |
| `01-web/` | Rediseño completo de la web | disenador-web |
| `02-imagen-y-manual/` | Identidad visual y manual de marca | director-arte |
| `03-redes-sociales/` | Estrategia y contenido en redes | experto-redes-sociales |
| `04-campanas/` | Campañas publicitarias | experto-marketing-comunicacion |

Cada carpeta tiene su propio `CLAUDE.md` (contexto del apartado) y `BRIEF.md` (encargo, entregables, estado).

## Orden de dependencias
`02-imagen-y-manual` define la plataforma de marca (arquetipo, tono, paleta, tipografía). `01-web`, `03-redes-sociales` y `04-campanas` **consumen** el manual: si aún no está aprobado, trabajan sobre la versión borrador y lo marcan.

## Equipo de agentes (`.claude/agents/`)
director-arte · fotografo · disenador-grafico · disenador-web · programador · experto-ux-ui · qa · project-manager · ejecutivo-cuentas · experto-seo · experto-marketing-comunicacion · experto-redes-sociales

Flujo estándar: **project-manager** planifica → especialistas producen → **director-arte** valida coherencia visual → **qa** revisa → **ejecutivo-cuentas** prepara la presentación al cliente.
