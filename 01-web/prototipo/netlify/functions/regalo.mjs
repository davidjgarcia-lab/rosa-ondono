// POST /api/regalo -> avisa al WhatsApp del centro de una petición de tarjeta regalo.
import { json, limpio, validarContacto, lineaContacto, whatsappConfigurado, avisarWhatsApp } from "../lib/comun.mjs";

export default async (req) => {
  if (req.method !== "POST") return json({ error: "metodo" }, 405);
  let d; try { d = await req.json(); } catch (_) { return json({ error: "json" }, 400); }
  if (d["bot-field"]) return json({ ok: true });
  const c = validarContacto(d); if (c.error) return json({ error: c.error }, 400);
  const regalo = limpio(d.regalo_nombre, 90), para = limpio(d.para_nombre, 80), mensaje = limpio(d.mensaje, 280);
  if (!regalo || para.length < 2) return json({ error: "regalo" }, 400);
  const resultado = { whatsapp: "sin-configurar" };
  if (whatsappConfigurado()) {
    try {
      await avisarWhatsApp(`🎁 *Petición de tarjeta regalo*\n${regalo} para ${para}${mensaje ? `\nMensaje: «${mensaje}»` : ""}\n${c.nombre} · ${lineaContacto(c)}\n_Enviado por la web_`);
      resultado.whatsapp = "ok";
    } catch (err) { console.error(err.message); resultado.whatsapp = "error"; }
  }
  return json(resultado);
};
export const config = { path: "/api/regalo" };
