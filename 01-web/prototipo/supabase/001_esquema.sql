-- Rosa Ondoño · prototipo web · esquema (Supabase / Postgres)
-- Catálogo de lectura pública + solicitudes de reserva de solo inserción.
-- Datos PENDIENTES del cliente (precios, duraciones, nº colegiado) se guardan como NULL: nunca se inventan.

create table public.pilares (
  slug text primary key,
  nombre text not null,
  lema text not null,
  descripcion text not null,
  color text not null,            -- token de color del manual (marfil · arena · lila)
  orden smallint not null default 0
);

create table public.programas (
  slug text primary key,
  pilar_slug text not null references public.pilares(slug),
  nombre text not null,
  descripcion text not null,
  orden smallint not null default 0
);

create table public.categorias (
  slug text primary key,
  nombre text not null,
  icono text,                     -- nombre del icono del manual (identidad/iconos)
  orden smallint not null default 0
);

create table public.profesionales (
  slug text primary key,
  nombre text not null,
  cargo text not null,
  bio text not null,
  num_colegiado text,             -- PENDIENTE: null hasta que lo facilite el cliente
  sanitario boolean not null default false
);

create table public.tratamientos (
  slug text primary key,
  nombre text not null,
  categoria_slug text not null references public.categorias(slug),
  pilar_slug text not null references public.pilares(slug),
  programa_slug text references public.programas(slug),
  tipo text not null check (tipo in ('estetica','terapia','medico')),
  resumen text not null,
  para_quien text,
  duracion_min smallint,          -- PENDIENTE
  sesiones text,
  precio_desde numeric(8,2),      -- PENDIENTE
  profesional_slug text references public.profesionales(slug),
  reservable boolean not null default true,
  destacado boolean not null default false,
  prioridad smallint not null default 3,   -- 1 = prioridad SEO alta (keyword map)
  revision_pendiente text         -- aviso interno: claim o profesional por confirmar
);
create index on public.tratamientos (categoria_slug);
create index on public.tratamientos (pilar_slug);
create index on public.tratamientos (programa_slug);
create index on public.tratamientos (profesional_slug);

create table public.faqs (
  id bigint generated always as identity primary key,
  tratamiento_slug text not null references public.tratamientos(slug) on delete cascade,
  pregunta text not null,
  respuesta text not null,
  orden smallint not null default 0
);
create index on public.faqs (tratamiento_slug);

-- Solicitudes de reserva (prototipo). Sin campo de texto libre: así no se recogen datos de salud.
create table public.solicitudes_reserva (
  id uuid primary key default gen_random_uuid(),
  creada_en timestamptz not null default now(),
  tratamiento_slug text not null references public.tratamientos(slug),
  fecha date not null,
  franja text not null check (franja in ('manana','tarde')),
  nombre text not null check (char_length(nombre) between 2 and 120),
  telefono text not null check (telefono ~ '^[+0-9 ]{9,16}$'),
  email text not null check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' and char_length(email) <= 200),
  acepta_privacidad boolean not null check (acepta_privacidad),
  origen text not null default 'prototipo',
  estado text not null default 'nueva' check (estado in ('nueva','confirmada','cancelada'))
);
create index on public.solicitudes_reserva (tratamiento_slug);

-- ===== Seguridad (RLS) =====
alter table public.pilares enable row level security;
alter table public.programas enable row level security;
alter table public.categorias enable row level security;
alter table public.profesionales enable row level security;
alter table public.tratamientos enable row level security;
alter table public.faqs enable row level security;
alter table public.solicitudes_reserva enable row level security;

create policy "lectura publica" on public.pilares for select to anon, authenticated using (true);
create policy "lectura publica" on public.programas for select to anon, authenticated using (true);
create policy "lectura publica" on public.categorias for select to anon, authenticated using (true);
create policy "lectura publica" on public.profesionales for select to anon, authenticated using (true);
create policy "lectura publica" on public.tratamientos for select to anon, authenticated using (true);
create policy "lectura publica" on public.faqs for select to anon, authenticated using (true);

-- Cualquiera puede ENVIAR una solicitud, nadie puede LEERLAS con la clave pública.
-- Solo se admiten tratamientos reservables (los médicos van a «consulta-medica»).
create policy "enviar solicitud" on public.solicitudes_reserva for insert to anon, authenticated
  with check (
    estado = 'nueva' and origen = 'prototipo'
    and fecha between current_date and current_date + 120
    and exists (select 1 from public.tratamientos t where t.slug = tratamiento_slug and t.reservable)
  );

revoke all on public.solicitudes_reserva from anon, authenticated;
grant insert (tratamiento_slug, fecha, franja, nombre, telefono, email, acepta_privacidad) on public.solicitudes_reserva to anon, authenticated;
