// POST /api/reserva -> crea la petición en Google Calendar y avisa al WhatsApp del centro.
// La propia web envía el aviso: la clienta no tiene que pulsar nada en WhatsApp.
import { json, limpio, validarContacto, lineaContacto, fechaValida, fechaLarga, aMin, hhmm, aEpoch, APERTURA, CIERRE,
  calendarioConfigurado, whatsappConfigurado, ocupados, solapa, crearEvento, avisarWhatsApp } from "../lib/comun.mjs";

export default async (req) => {
  if (req.method !== "POST") return json({ error: "metodo" }, 405);
  let d; try { d = await req.json(); } catch (_) { return json({ error: "json" }, 400); }
  if (d["bot-field"]) return json({ ok: true }); // trampa para bots
  const c = validarContacto(d); if (c.error) return json({ error: c.error }, 400);
  const servicio = limpio(d.servicio_nombre, 90), fecha = limpio(d.fecha, 10), hora = limpio(d.hora, 5);
  const duracion = Math.min(Math.max(parseInt(d.duracion, 10) || 60, 15), 240);
  if (!servicio) return json({ error: "servicio" }, 400);
  if (!fechaValida(fecha)) return json({ error: "fecha" }, 400);
  if (!/^\d{2}:\d{2}$/.test(hora)) return json({ error: "hora" }, 400);
  const inicio = aMin(hora);
  if (inicio < APERTURA || inicio + duracion > CIERRE) return json({ error: "hora" }, 400);

  const resultado = { calendario: "sin-configurar", whatsapp: "sin-configurar" };
  if (calendarioConfigurado()) {
    try {
      const ini = aEpoch(fecha, inicio);
      if (solapa(ini, ini + duracion * 60000, await ocupados(fecha))) return json({ error: "ocupado" }, 409);
      await crearEvento({ fecha, inicio, duracion, titulo: `Petición de reserva · ${servicio} · ${c.nombre}`,
        descripcion: `Pendiente de confirmar con la clienta.\n\n${servicio}\n${c.nombre}\n${lineaContacto(c)}\n\nEnviado desde la web.` });
      resultado.calendario = "ok";
    } catch (err) { console.error(err.message); resultado.calendario = "error"; }
  }
  if (whatsappConfigurado()) {
    try {
      await avisarWhatsApp(`📅 *Petición de reserva*\n${servicio}\n${fechaLarga(fecha)} a las ${hhmm(inicio)}\n${c.nombre} · ${lineaContacto(c)}\n_Enviado por la web${resultado.calendario === "ok" ? " · ya está en el calendario como pendiente" : ""}_`);
      resultado.whatsapp = "ok";
    } catch (err) { console.error(err.message); resultado.whatsapp = "error"; }
  }
  return json(resultado);
};
export const config = { path: "/api/reserva" };
