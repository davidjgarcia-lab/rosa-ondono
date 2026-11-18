// Vercel: misma función que netlify/functions/huecos.mjs (GET /api/huecos)
import manejar from "../netlify/functions/huecos.mjs";
export const GET = (req) => manejar(req);
