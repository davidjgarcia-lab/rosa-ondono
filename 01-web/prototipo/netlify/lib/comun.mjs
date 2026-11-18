// Rosa Ondoño · utilidades de servidor (Netlify Functions)
// Google Calendar con cuenta de servicio (JWT firmado con node:crypto, sin dependencias)
// y aviso de WhatsApp al centro con CallMeBot.
// Las claves viven en variables de entorno de Netlify, nunca en el repositorio:
//   GOOGLE_SA_EMAIL, GOOGLE_SA_KEY, GOOGLE_CALENDAR_ID, CALLMEBOT_PHONE, CALLMEBOT_APIKEY
import { createSign } from "node:crypto";

export const ZONA = "Europe/Madrid";
export const APERTURA = 9 * 60, CIERRE = 19 * 60; // minutos desde medianoche
const env = (k) => (globalThis.Netlify?.env.get(k) ?? process.env[k] ?? "").trim();

export const calendarioConfigurado = () => !!(env("GOOGLE_SA_EMAIL") && env("GOOGLE_SA_KEY") && env("GOOGLE_CALENDAR_ID"));
export const whatsappConfigurado = () => !!(env("CALLMEBOT_PHONE") && env("CALLMEBOT_APIKEY"));

export const json = (datos, estado = 200) => new Response(JSON.stringify(datos), {
  status: estado, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });

// ---------- fechas en hora de Madrid
function desfaseMin(epoch) { // minutos que Madrid va por delante de UTC en ese instante
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-GB", { timeZone: ZONA, hourCycle: "h23",
    year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }).formatToParts(new Date(epoch)).map((x) => [x.type, x.value]));
  return (Date.UTC(+p.year, p.month - 1, +p.day, +p.hour, +p.minute) - epoch) / 60000;
}
export function aEpoch(fecha, minutos) { // "2026-11-23", 690 -> ms UTC de las 11:30 en Madrid
  const [a, m, d] = fecha.split("-").map(Number);
  const local = Date.UTC(a, m - 1, d, 0, minutos);
  return local - desfaseMin(local - desfaseMin(local) * 60000) * 60000;
}
export const hhmm = (min) => `${String(Math.floor(min / 60)).padStart(2, "0")}:${String(min % 60).padStart(2, "0")}`;
export const aMin = (h) => { const [a, b] = h.split(":").map(Number); return a * 60 + b; };
export function fechaValida(fecha) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(fecha)) return false;
  const dia = new Date(fecha + "T12:00:00Z");
  if (isNaN(dia) || dia.toISOString().slice(0, 10) !== fecha) return false;
  const sem = dia.getUTCDay(); if (sem === 0 || sem === 6) return false;
  const hoy = Date.now(), t = aEpoch(fecha, APERTURA);
  return t > hoy - 864e5 && t < hoy + 130 * 864e5;
}
export const fechaLarga = (fecha) => new Date(fecha + "T12:00:00Z").toLocaleDateString("es-ES", { timeZone: "UTC", weekday: "long", day: "numeric", month: "numeric" });
export const huecosDelDia = (duracion, paso = 60) => {
  const r = []; for (let m = APERTURA; m + duracion <= CIERRE; m += paso) r.push(m); return r;
};

// ---------- Google
let tokenCache = { valor: "", caduca: 0 };
async function tokenGoogle() {
  if (tokenCache.valor && Date.now() < tokenCache.caduca) return tokenCache.valor;
  const ahora = Math.floor(Date.now() / 1000);
  const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
  const sinFirma = b64({ alg: "RS256", typ: "JWT" }) + "." + b64({ iss: env("GOOGLE_SA_EMAIL"),
    scope: "https://www.googleapis.com/auth/calendar", aud: "https://oauth2.googleapis.com/token", iat: ahora, exp: ahora + 3600 });
  const firma = createSign("RSA-SHA256").update(sinFirma).sign(env("GOOGLE_SA_KEY").replace(/\\n/g, "\n"), "base64url");
  const r = await fetch("https://oauth2.googleapis.com/token", { method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: `${sinFirma}.${firma}` }) });
  if (!r.ok) throw new Error(`Google token ${r.status}`);
  const d = await r.json();
  tokenCache = { valor: d.access_token, caduca: Date.now() + (d.expires_in - 120) * 1000 };
  return d.access_token;
}
async function google(ruta, cuerpo) {
  const r = await fetch(`https://www.googleapis.com/calendar/v3/${ruta}`, { method: "POST",
    headers: { Authorization: `Bearer ${await tokenGoogle()}`, "Content-Type": "application/json" }, body: JSON.stringify(cuerpo) });
  if (!r.ok) throw new Error(`Google ${ruta.split("/")[0]} ${r.status}`);
  return r.json();
}
export async function ocupados(fecha) { // intervalos [inicio, fin] en ms UTC
  const id = env("GOOGLE_CALENDAR_ID");
  const d = await google("freeBusy", { timeMin: new Date(aEpoch(fecha, 0)).toISOString(),
    timeMax: new Date(aEpoch(fecha, 24 * 60)).toISOString(), timeZone: ZONA, items: [{ id }] });
  return (d.calendars?.[id]?.busy || []).map((b) => [Date.parse(b.start), Date.parse(b.end)]);
}
export const solapa = (ini, fin, intervalos) => intervalos.some(([a, b]) => ini < b && fin > a);
export async function crearEvento({ fecha, inicio, duracion, titulo, descripcion }) {
  const id = encodeURIComponent(env("GOOGLE_CALENDAR_ID"));
  const iso = (min) => `${fecha}T${hhmm(min)}:00`;
  const ev = await google(`calendars/${id}/events`, { summary: titulo, description: descripcion, status: "tentative", colorId: "5",
    start: { dateTime: iso(inicio), timeZone: ZONA }, end: { dateTime: iso(inicio + duracion), timeZone: ZONA } });
  return ev.id;
}

// ---------- WhatsApp (CallMeBot)
export async function avisarWhatsApp(texto) {
  const url = "https://api.callmebot.com/whatsapp.php?" + new URLSearchParams({ phone: env("CALLMEBOT_PHONE"), text: texto, apikey: env("CALLMEBOT_APIKEY") });
  const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 9000);
  try {
    const r = await fetch(url, { signal: ctl.signal });
    const cuerpo = await r.text();
    if (!r.ok || /error|apikey is invalid/i.test(cuerpo)) throw new Error(`CallMeBot ${r.status}`);
  } finally { clearTimeout(t); }
}

// ---------- validación común
export const limpio = (v, max = 120) => String(v ?? "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max);
export function validarContacto(d) {
  const nombre = limpio(d.nombre), telefono = limpio(d.telefono, 20), email = limpio(d.email, 200);
  if (nombre.length < 2) return { error: "nombre" };
  if (!telefono && !email) return { error: "contacto" };
  if (telefono && !/^\+?[0-9 ]{9,16}$/.test(telefono)) return { error: "telefono" };
  if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return { error: "email" };
  return { nombre, telefono, email };
}
export const lineaContacto = (c) => [c.telefono && `Tel. ${c.telefono}`, c.email].filter(Boolean).join(" · ");
