// Vercel: misma función que netlify/functions/regalo.mjs (POST /api/regalo)
import manejar from "../netlify/functions/regalo.mjs";
export const POST = (req) => manejar(req);
