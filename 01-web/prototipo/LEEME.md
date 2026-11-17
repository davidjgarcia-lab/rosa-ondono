# Prototipo web · Rosa Ondoño
*01-web · programador + disenador-web · 17/11/2026 · Estado: **PROTOTIPO** (borrador con el manual de marca v2.1, aún sin QA)*

Prototipo navegable del rediseño. Aplica la arquitectura de `../arquitectura/` y los wireframes de baja fidelidad. Lee el catálogo de una base de datos propia en Supabase.

## Qué incluye
- **Inicio:**
  - lema;
  - los tres pilares (Cuídate · Conecta · Siente) con el supergráfico;
  - valoración integral;
  - tratamientos destacados;
  - equipo;
  - el centro, con fotos reales y sin asignar uso a las cabinas;
  - regalo.
- **Páginas de pilar** con sus programas, por necesidad.
- **Listado de los 62 tratamientos**, con buscador y filtros por técnica y por pilar.
- **Ficha por tratamiento.**
  - Contenido: datos clave, profesional, FAQ y relacionados.
  - Variante médica: CTA de consulta, aviso sanitario y nº de colegiado.
- **Medicina estética** (hub), **Rosa y el equipo** y **Tarjeta regalo**.
- **Reserva en 3 pasos:**
  1. tratamiento (llega precargado desde la ficha);
  2. día y franja;
  3. datos y privacidad.

  La solicitud se guarda en Supabase.

**Datos pendientes del cliente.** Se muestran como pendientes y nunca se inventan:
- precios y duraciones;
- nº de colegiado;
- nº de registro sanitario;
- horario de invierno;
- retratos.

## Base de datos (Supabase)
| | |
|---|---|
| Proyecto | `rosa-ondono-web` (ref `prrwekpaphnbqakrwtiz`), región eu-west-3 (París) |
| Esquema | `supabase/001_esquema.sql` |
| Datos | `supabase/002_semilla.sql`, generado con `supabase/generar_semilla.py` |
| Tablas | `pilares`, `programas`, `categorias`, `profesionales`, `tratamientos`, `faqs`, `solicitudes_reserva` |

**Seguridad (RLS):**
- El catálogo es de solo lectura con la clave publicable.
- `solicitudes_reserva` solo admite inserciones:
  - no se puede leer con la clave pública;
  - solo acepta tratamientos reservables: los médicos van a «Consulta de medicina estética»;
  - solo fechas de los próximos 120 días.
- El formulario no tiene campo de texto libre, para no recoger datos de salud.
- Las solicitudes se consultan desde el panel de Supabase.

**Copia local:** `datos/catalogo.json` es una copia del mismo catálogo. Se usa cuando no hay conexión con Supabase, por ejemplo en la vista previa publicada en Claude, que bloquea las peticiones externas.
- En ese modo la reserva **no se envía**, y la página lo dice claramente.
- La barra superior indica siempre de dónde vienen los datos.

## Cómo verlo
```bash
cd 01-web/prototipo
python3 -m http.server 8000   # y abrir http://localhost:8000
```
Abrir `index.html` con doble clic no funciona: el navegador bloquea la lectura de `datos/catalogo.json` desde `file://`.

## Para regenerar la semilla
```bash
python3 supabase/generar_semilla.py   # reescribe 002_semilla.sql y datos/catalogo.json
```
Después hay que aplicar el SQL en Supabase: vaciar las tablas e insertar de nuevo.

## Límites del prototipo
- La disponibilidad es una franja de mañana o tarde. Los huecos reales llegarán del sistema de reservas elegido (ver `../codigo/propuesta-stack-y-reservas.md`).
- Las tipografías se cargan desde Google Fonts. En producción irán autoalojadas (WOFF2).
- El logotipo es el vector reconstruido del manual v2.1, pendiente de validar. El isotipo es el original del cliente y no se modifica.
- La cabina que aparece en la galería no tiene un uso asignado, por decisión del cliente.
