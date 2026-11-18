// Vercel: misma función que netlify/functions/reserva.mjs (POST /api/reserva)
import manejar from "../netlify/functions/reserva.mjs";
export const POST = (req) => manejar(req);
