// GET /api/huecos?fecha=2026-11-23&duracion=60 -> horas libres según el Google Calendar del centro
import { json, fechaValida, huecosDelDia, hhmm, aEpoch, ocupados, solapa, calendarioConfigurado } from "../lib/comun.mjs";

export default async (req) => {
  const u = new URL(req.url);
  const fecha = u.searchParams.get("fecha") || "";
  const duracion = Math.min(Math.max(parseInt(u.searchParams.get("duracion"), 10) || 60, 15), 240);
  if (!fechaValida(fecha)) return json({ error: "fecha" }, 400);
  const horas = huecosDelDia(duracion);
  let busy = [], calendario = "sin-configurar";
  if (calendarioConfigurado()) {
    try { busy = await ocupados(fecha); calendario = "ok"; } catch (err) { console.error(err.message); calendario = "error"; }
  }
  const ahora = Date.now() + 2 * 3600e3; // no ofrecer horas que empiezan en menos de 2 h
  return json({ fecha, duracion, calendario, huecos: horas.map((m) => {
    const ini = aEpoch(fecha, m), fin = ini + duracion * 60000;
    return { hora: hhmm(m), libre: ini > ahora && !solapa(ini, fin, busy) };
  }) });
};
export const config = { path: "/api/huecos" };
