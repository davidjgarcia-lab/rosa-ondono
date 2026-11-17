-- Rosa Ondoño · prototipo v2 · áreas (navegación por especialidad) y solicitudes de regalo
create table public.areas (
  slug text primary key, nombre text not null, titular text not null, descripcion text not null, orden smallint not null default 0
);
alter table public.areas enable row level security;
create policy "lectura publica" on public.areas for select to anon, authenticated using (true);
insert into public.areas (slug, nombre, titular, descripcion, orden) values
('estetica', 'Estética', 'Tu piel y tu cuerpo, en buenas manos', 'Tratamientos faciales y corporales, depilación láser y belleza. Te recomendamos lo que de verdad necesitas.', 1),
('medicina-estetica', 'Medicina estética', 'Resultados naturales, con criterio médico', 'Cada tratamiento empieza con una consulta con el médico, que valora tu caso y te explica opciones, riesgos y alternativas.', 2),
('terapias', 'Terapias', 'Manos expertas para el cuerpo y la emoción', 'Masajes, drenaje linfático y terapias manuales y complementarias, con más de 30 años de oficio.', 3),
('bienestar', 'Bienestar', 'Rituales para parar', 'Experiencias para desconectar, solo o en compañía, en pleno centro de Alicante.', 4);

alter table public.categorias add column area_slug text references public.areas(slug);
create index on public.categorias (area_slug);
update public.categorias set area_slug = case slug
  when 'faciales' then 'estetica' when 'corporales' then 'estetica' when 'depilacion' then 'estetica' when 'belleza' then 'estetica'
  when 'medicina-estetica' then 'medicina-estetica'
  when 'masajes' then 'terapias' when 'terapias-complementarias' then 'terapias'
  when 'rituales' then 'bienestar' else null end;

create table public.solicitudes_regalo (
  id uuid primary key default gen_random_uuid(),
  creada_en timestamptz not null default now(),
  modalidad text not null check (modalidad in ('experiencia','importe')),
  tratamiento_slug text references public.tratamientos(slug),
  importe numeric(7,2) check (importe is null or importe between 20 and 1000),
  para_nombre text not null check (char_length(para_nombre) between 2 and 80),
  mensaje text check (mensaje is null or char_length(mensaje) <= 280),
  nombre text not null check (char_length(nombre) between 2 and 120),
  telefono text not null check (telefono ~ '^[+0-9 ]{9,16}$'),
  email text not null check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' and char_length(email) <= 200),
  acepta_privacidad boolean not null check (acepta_privacidad),
  estado text not null default 'nueva' check (estado in ('nueva','pagada','enviada','cancelada')),
  check ((modalidad = 'experiencia' and tratamiento_slug is not null and importe is null) or (modalidad = 'importe' and importe is not null and tratamiento_slug is null))
);
create index on public.solicitudes_regalo (tratamiento_slug);
alter table public.solicitudes_regalo enable row level security;
-- Solo inserción; nunca tratamientos médicos (no se pueden regalar actos médicos).
create policy "enviar regalo" on public.solicitudes_regalo for insert to anon, authenticated
  with check (estado = 'nueva' and (tratamiento_slug is null or exists (select 1 from public.tratamientos t where t.slug = tratamiento_slug and t.tipo <> 'medico' and t.reservable)));
revoke all on public.solicitudes_regalo from anon, authenticated;
grant insert (modalidad, tratamiento_slug, importe, para_nombre, mensaje, nombre, telefono, email, acepta_privacidad) on public.solicitudes_regalo to anon, authenticated;
