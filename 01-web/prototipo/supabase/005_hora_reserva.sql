-- 005 · Web v3: la reserva pide hora exacta (de 09:00 a 19:00, lunes a viernes).
-- La franja (mañana/tarde) se mantiene y la calcula la web a partir de la hora.
alter table public.solicitudes_reserva
  add column if not exists hora time
  check (hora is null or (hora >= time '09:00' and hora < time '19:00'));
grant insert (hora) on public.solicitudes_reserva to anon;
