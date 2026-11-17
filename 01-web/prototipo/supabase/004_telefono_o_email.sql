-- En todos los formularios basta con teléfono O email (al menos uno de los dos).
alter table public.solicitudes_reserva alter column telefono drop not null, alter column email drop not null;
alter table public.solicitudes_reserva add constraint reserva_telefono_o_email check (telefono is not null or email is not null);
alter table public.solicitudes_regalo alter column telefono drop not null, alter column email drop not null;
alter table public.solicitudes_regalo add constraint regalo_telefono_o_email check (telefono is not null or email is not null);
