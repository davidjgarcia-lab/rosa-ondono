/* Rosa Ondoño · web v3 · JS (mejora progresiva)
   - Cabecera con sombra al hacer scroll y menú móvil
   - Aviso de cookies (aceptar / rechazar / configurar, mismo nivel)
   - Formularios de reserva y de regalo → Supabase (RLS de solo inserción)
   - Vista previa en un único archivo: enrutado por #ancla */
(() => {
  "use strict";
  const CFG = window.RO_CONFIG || {};
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const almacen = {
    leer(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (_) { return null; } },
    guardar(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) { /* sin almacenamiento */ } }
  };
  const VISTA = document.body.dataset.modo === "vista";
  let RESERVA_PENDIENTE = null; // vista previa: datos elegidos en la reserva rápida de la portada

  /* ---------- Vista previa: una página visible cada vez ---------- */
  function mostrarPagina() {
    if (!VISTA) return;
    let id = decodeURIComponent(location.hash.slice(1)) || "inicio";
    let preseleccion = "";
    for (const pref of ["reservar", "regalar"]) {
      if (id.startsWith(pref + "--")) { preseleccion = id.slice(pref.length + 2); id = pref; }
    }
    let pagina = $(`[data-pagina="${CSS.escape(id)}"]`);
    let destino = null;
    if (!pagina) {
      destino = document.getElementById(id);
      pagina = destino ? destino.closest("[data-pagina]") : $('[data-pagina="no-encontrada"]');
    }
    $$("[data-pagina]").forEach((p) => { p.hidden = p !== pagina; });
    document.title = pagina.dataset.titulo || document.title;
    const ruta = pagina.dataset.menu || "";
    $$(".menu a, .panel-menu a").forEach((a) => a.toggleAttribute("aria-current", a.dataset.menu === ruta && ruta !== ""));
    $$(".menu a[aria-current]").forEach((a) => a.setAttribute("aria-current", "page"));
    if (preseleccion) {
      const sel = $("select[data-preseleccion]", pagina);
      if (sel && [...sel.options].some((o) => o.value === preseleccion)) { sel.value = preseleccion; sel.dispatchEvent(new Event("change")); }
    }
    if (id === "reservar" && RESERVA_PENDIENTE && typeof selReserva !== "undefined" && selReserva) {
      selReserva.preseleccionar(RESERVA_PENDIENTE.fecha, RESERVA_PENDIENTE.hora); RESERVA_PENDIENTE = null;
    }
    cerrarMenu();
    if (destino) destino.scrollIntoView(); else window.scrollTo(0, 0);
  }

  /* ---------- Preselección en la web estática (?servicio=) ---------- */
  if (!VISTA) {
    const servicio = new URLSearchParams(location.search).get("servicio");
    const sel = $("select[data-preseleccion]");
    if (servicio && sel && [...sel.options].some((o) => o.value === servicio)) sel.value = servicio;
  }

  /* ---------- Cabecera y menú ---------- */
  const cabecera = $(".cabecera");
  const alScroll = () => cabecera && cabecera.classList.toggle("con-sombra", window.scrollY > 8);
  window.addEventListener("scroll", alScroll, { passive: true }); alScroll();
  const panel = $("#panel-menu"), botonMenu = $(".boton-menu");
  function cerrarMenu() { if (panel) { panel.classList.remove("abierto"); botonMenu?.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; } }
  botonMenu?.addEventListener("click", () => { panel.classList.add("abierto"); botonMenu.setAttribute("aria-expanded", "true"); document.body.style.overflow = "hidden"; $("a", panel)?.focus(); });
  $("#cerrar-menu")?.addEventListener("click", () => { cerrarMenu(); botonMenu?.focus(); });
  panel?.addEventListener("click", (e) => { if (e.target.closest("a")) cerrarMenu(); });
  document.addEventListener("keydown", (e) => {
    if (!panel?.classList.contains("abierto")) return;
    if (e.key === "Escape") { cerrarMenu(); botonMenu?.focus(); }
    if (e.key === "Tab") { // mantener el foco dentro del menú abierto
      const f = $$("a, button", panel); const primero = f[0], ultimo = f[f.length - 1];
      if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
    }
  });

  /* ---------- Cookies ---------- */
  const aviso = $("#cookies");
  const CLAVE = "ro-consentimiento-v1";
  function abrirCookies(configurar) {
    aviso.hidden = false; document.body.classList.add("con-cookies");
    $("#cookies-opciones").hidden = !configurar; $("#cookies-guardar").hidden = !configurar; $("#cookies-configurar").hidden = !!configurar;
    const previo = almacen.leer(CLAVE);
    if (previo) { $("#ck-analitica").checked = !!previo.analitica; $("#ck-marketing").checked = !!previo.marketing; }
    if (configurar) $("h2", aviso).focus();
  }
  function decidir(analitica, marketing) {
    almacen.guardar(CLAVE, { analitica, marketing, fecha: new Date().toISOString() });
    aviso.hidden = true; document.body.classList.remove("con-cookies");
    // Aquí se cargarían los scripts de analítica solo si analitica === true (no hay ninguno en el prototipo).
  }
  if (aviso) {
    if (!almacen.leer(CLAVE)) abrirCookies(false);
    $("#cookies-aceptar").addEventListener("click", () => decidir(true, true));
    $("#cookies-rechazar").addEventListener("click", () => decidir(false, false));
    $("#cookies-configurar").addEventListener("click", () => abrirCookies(true));
    $("#cookies-guardar").addEventListener("click", () => decidir($("#ck-analitica").checked, $("#ck-marketing").checked));
    $$("[data-abrir-cookies]").forEach((b) => b.addEventListener("click", () => abrirCookies(true)));
  }

  /* ---------- Formularios: servidor (Google Calendar + aviso de WhatsApp) + Netlify Forms (email) + Supabase (copia) ---------- */
  const hoyMas = (d) => { const f = new Date(); f.setDate(f.getDate() + d); return f.toISOString().slice(0, 10); };
  $$('input[type="date"][data-min-dias]').forEach((i) => { i.min = hoyMas(+i.dataset.minDias); i.max = hoyMas(+i.dataset.maxDias); });
  const fechaLarga = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" });
  const telOk = (v) => /^\+?[0-9 ]{9,16}$/.test(v), mailOk = (v) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
  const HAY_SERVIDOR = !VISTA && /^https?:$/.test(location.protocol);

  async function conTiempo(url, opciones, ms) {
    const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), ms || CFG.tiempoMaximoMs || 8000);
    try { return await fetch(url, { ...opciones, signal: ctl.signal }); } finally { clearTimeout(t); }
  }
  const EN_NETLIFY = /netlify\.app$/.test(location.hostname) || !!CFG.netlifyForms; // Netlify Forms solo existe en Netlify
  async function aNetlify(form) {
    if (!HAY_SERVIDOR) return "no-disponible";
    if (!EN_NETLIFY) return "omitido";
    try {
      const r = await conTiempo("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(new FormData(form)).toString() });
      return r.ok ? "ok" : "error";
    } catch (_) { return "error"; }
  }
  async function aSupabase(tabla, datos) {
    try {
      const r = await conTiempo(`${CFG.supabaseUrl}/rest/v1/${tabla}`, { method: "POST",
        headers: { apikey: CFG.supabaseKey, Authorization: `Bearer ${CFG.supabaseKey}`, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify(datos) });
      return r.status === 201 ? "ok" : "error";
    } catch (_) { return "error"; }
  }
  async function aServidor(ruta, datos) { // devuelve { estado HTTP, cuerpo } o null si no hay servidor
    if (!HAY_SERVIDOR) return null;
    try {
      const r = await conTiempo(ruta, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) }, 15000);
      return { estado: r.status, cuerpo: await r.json().catch(() => ({})) };
    } catch (_) { return { estado: 0, cuerpo: {} }; }
  }
  const enlaceWA = (texto) => `https://wa.me/${CFG.whatsapp || "34691315622"}?text=${encodeURIComponent(texto)}`;

  function marcarError(form, nombre, texto) {
    const campo = form.elements[nombre]; const el = campo instanceof RadioNodeList ? campo[0] : campo;
    const caja = (el?.type === "hidden" ? el.closest("[data-campo-hora]") : el?.closest("[data-campo]")); if (!caja) return;
    const p = document.createElement("p"); p.className = "error"; p.id = `err-${form.id}-${nombre}`; p.textContent = texto;
    caja.appendChild(p);
    const foco = el.type === "hidden" ? ($(".hueco:not(:disabled)", caja) || el) : el;
    foco.setAttribute("aria-describedby", p.id); foco.setAttribute("aria-invalid", "true");
  }
  function limpiar(form) { $$(".error", form).forEach((e) => e.remove()); $$("[aria-invalid]", form).forEach((e) => { e.removeAttribute("aria-invalid"); e.removeAttribute("aria-describedby"); }); }
  function validarContacto(form) {
    const f = form.elements; let ok = true;
    const tel = f.telefono.value.trim(), mail = f.email.value.trim();
    if (f.nombre.value.trim().length < 2) { marcarError(form, "nombre", "Escribe tu nombre."); ok = false; }
    if (!tel && !mail) { marcarError(form, "telefono", "Déjanos un teléfono o un email (con uno basta) para poder contestarte."); ok = false; }
    if (tel && !telOk(tel)) { marcarError(form, "telefono", "Revisa el teléfono: solo números, mínimo 9."); ok = false; }
    if (mail && !mailOk(mail)) { marcarError(form, "email", "Revisa el email: falta la @ o el dominio."); ok = false; }
    if (!f.privacidad.checked) { marcarError(form, "privacidad", "Necesitamos tu consentimiento para gestionar la solicitud."); ok = false; }
    return ok;
  }
  const ESTADOS = {
    ok: "✓", error: "✕", "sin-configurar": "…", "no-disponible": "…"
  };
  function mostrarResultado(form, { titulo, texto, lineas, wa, llegó }) {
    const caja = $(".resultado", form.parentElement);
    caja.innerHTML = `<div class="estado ${llegó ? "estado--ok" : "estado--aviso"}" role="status" tabindex="-1">
      <h2>${llegó ? titulo : "No hemos podido enviarla"}</h2><p>${llegó ? texto : "Escríbenos por WhatsApp y te atendemos enseguida. Tu mensaje ya está redactado."}</p>
      <details class="detalle-envio"${llegó ? "" : " open"}><summary>Estado de los avisos (prototipo)</summary><ul class="lista-envios">${lineas.filter(([estado]) => estado !== "omitido").map(([estado, t]) => `<li>${ESTADOS[estado] || "…"} ${t}</li>`).join("")}</ul></details>
      <div class="botonera">${llegó ? "" : `<a class="boton boton--primario" href="${wa}" target="_blank" rel="noopener">Enviar por WhatsApp</a>`}
      <button class="boton boton--secundario" type="button" data-otra>Hacer otra solicitud</button>
      ${llegó ? `<a class="enlace-flecha" href="${wa}" target="_blank" rel="noopener">¿Quieres añadir algo? Escríbenos</a>` : ""}</div></div>`;
    caja.hidden = false; form.hidden = true; $(".estado", caja).focus();
    $("[data-otra]", caja).addEventListener("click", () => { caja.hidden = true; form.hidden = false; form.reset(); form.dispatchEvent(new Event("change")); form.elements[0]?.focus(); });
  }
  const contactoTexto = (f) => [f.telefono.value.trim() && `Teléfono: ${f.telefono.value.trim()}`, f.email.value.trim() && `Email: ${f.email.value.trim()}`].filter(Boolean).join("\n");
  const textoCanal = {
    calendario: { ok: "Petición apuntada en la agenda del centro", error: "No se ha podido apuntar en la agenda", "sin-configurar": "Agenda de Google: pendiente de conectar", "no-disponible": "Agenda: disponible en la web publicada" },
    whatsapp: { ok: "Aviso enviado al WhatsApp del centro", error: "No se ha podido enviar el aviso de WhatsApp", "sin-configurar": "Aviso de WhatsApp: pendiente de conectar", "no-disponible": "Aviso de WhatsApp: disponible en la web publicada" },
    netlify: { ok: "Aviso enviado por email", error: "No se ha podido enviar el email", "no-disponible": "Email: disponible en la web publicada" },
    supabase: { ok: "Solicitud guardada", error: "No se ha podido guardar en la base de datos" }
  };
  const linea = (canal, estado) => [estado, textoCanal[canal][estado] || textoCanal[canal].error];

  /* ---------- Elegir hora: huecos libres según la agenda del centro ---------- */
  const APERTURA = 9 * 60, CIERRE = 19 * 60;
  const hhmm = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
  function huecosLocales(fecha, duracion) {
    const r = []; for (let m = APERTURA; m + duracion <= CIERRE; m += 60) r.push({ hora: hhmm(m), libre: true }); return r;
  }
  function selectorHoras(form) {
    const servicio = $("[data-selector-servicio]", form), fecha = $("[data-selector-fecha]", form);
    const caja = $("[data-huecos]", form), oculto = $("[data-hora]", form);
    if (!servicio || !fecha || !caja) return null;
    let peticion = 0, pendiente = "";
    const duracion = () => +(servicio.selectedOptions[0]?.dataset.duracion || 60);
    const vacio = (t) => { caja.innerHTML = `<p class="huecos__vacio">${t}</p>`; };
    async function cargar() {
      const dia = fecha.value; const yo = ++peticion;
      if (form.elements.duracion) form.elements.duracion.value = duracion();
      if (!pendiente) oculto.value = "";
      if (!servicio.value || !dia) return vacio(servicio.value ? "Elige un día para ver las horas libres." : "Elige tratamiento y día para ver las horas libres.");
      if (dia < fecha.min || dia > fecha.max) return vacio("Elige un día entre mañana y los próximos cuatro meses.");
      if ([0, 6].includes(new Date(dia + "T12:00:00").getDay())) return vacio("Abrimos de lunes a viernes. Elige un día laborable.");
      caja.classList.add("huecos--cargando");
      let lista = huecosLocales(dia, duracion());
      if (HAY_SERVIDOR) {
        try {
          const r = await conTiempo(`/api/huecos?fecha=${dia}&duracion=${duracion()}`, {}, 8000);
          if (r.ok) lista = (await r.json()).huecos;
        } catch (_) { /* sin agenda: se ofrecen todas las horas y el centro confirma */ }
      }
      if (yo !== peticion) return;
      caja.classList.remove("huecos--cargando");
      if (!lista.some((h) => h.libre)) return vacio("Ese día ya está completo. Prueba con otro.");
      caja.innerHTML = lista.map((h) => `<button type="button" class="hueco" data-valor="${h.hora}" aria-pressed="${h.hora === pendiente && h.libre}"${h.libre ? "" : ` disabled aria-label="${h.hora}, ocupado"`}>${h.hora}</button>`).join("");
      if (pendiente) { oculto.value = lista.some((h) => h.hora === pendiente && h.libre) ? pendiente : ""; pendiente = ""; }
    }
    caja.addEventListener("click", (e) => {
      const b = e.target.closest(".hueco"); if (!b || b.disabled) return;
      $$(".hueco", caja).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      oculto.value = b.dataset.valor;
      const err = $(".error", caja.closest("[data-campo-hora]") || form); if (err && caja.closest("[data-campo-hora]")) err.remove();
    });
    servicio.addEventListener("change", cargar); fecha.addEventListener("change", cargar);
    form.addEventListener("reset", () => setTimeout(() => { oculto.value = ""; cargar(); }));
    return { cargar, preseleccionar(dia, hora) { if (dia) fecha.value = dia; pendiente = hora || ""; return cargar(); } };
  }

  /* Reserva rápida de la portada → página de reserva con todo elegido */
  const rapida = $("[data-reserva-rapida]");
  const selRapida = rapida && selectorHoras(rapida);
  rapida?.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = rapida.elements; const datos = { servicio: f.servicio.value, fecha: f.fecha.value, hora: f.hora.value };
    if (VISTA) { RESERVA_PENDIENTE = datos; location.hash = "reservar--" + datos.servicio; return; }
    const q = new URLSearchParams(Object.entries(datos).filter(([, v]) => v));
    location.href = `${rapida.getAttribute("action").split("?")[0]}?${q}`;
  });
  selRapida?.cargar();

  const fReserva = $("#form-reserva");
  const selReserva = fReserva && selectorHoras(fReserva);
  if (fReserva && !VISTA) {
    const q = new URLSearchParams(location.search);
    selReserva.preseleccionar(q.get("fecha") && /^\d{4}-\d{2}-\d{2}$/.test(q.get("fecha")) ? q.get("fecha") : "", q.get("hora") || "");
  }
  fReserva?.addEventListener("submit", async (e) => {
    e.preventDefault(); limpiar(fReserva);
    const f = fReserva.elements; let ok = true;
    if (!f.servicio.value) { marcarError(fReserva, "servicio", "Elige un tratamiento."); ok = false; }
    const dia = f.fecha.value;
    if (!dia || dia < f.fecha.min || dia > f.fecha.max) { marcarError(fReserva, "fecha", "Elige un día entre mañana y los próximos cuatro meses."); ok = false; }
    else if ([0, 6].includes(new Date(dia + "T12:00:00").getDay())) { marcarError(fReserva, "fecha", "Abrimos de lunes a viernes: elige un día laborable."); ok = false; }
    else if (!f.hora.value) { marcarError(fReserva, "hora", "Elige una hora."); ok = false; }
    if (!validarContacto(fReserva) || !ok) { $("[aria-invalid]", fReserva)?.focus(); return; }
    const servicio = f.servicio.selectedOptions[0].textContent.trim();
    f.servicio_nombre.value = servicio;
    f.franja.value = parseInt(f.hora.value, 10) < 14 ? "manana" : "tarde";
    const cuando = `${fechaLarga(dia)} a las ${f.hora.value}`;
    const wa = enlaceWA(`Hola, soy ${f.nombre.value.trim()}. Quiero reservar cita.\n\nTratamiento: ${servicio}\nDía y hora: ${cuando}\n${contactoTexto(f)}\n\n(Enviado desde la web)`);
    const boton = $('button[type="submit"]', fReserva); boton.disabled = true; boton.textContent = "Enviando…";
    const srv = await aServidor("/api/reserva", { servicio: f.servicio.value, servicio_nombre: servicio, fecha: dia, hora: f.hora.value,
      duracion: f.duracion.value, nombre: f.nombre.value.trim(), telefono: f.telefono.value.trim(), email: f.email.value.trim(), "bot-field": f["bot-field"].value });
    if (srv?.estado === 409) {
      boton.disabled = false; boton.textContent = "Enviar solicitud";
      await selReserva.cargar(); marcarError(fReserva, "hora", "Esa hora se acaba de ocupar. Elige otra, por favor."); $("[aria-invalid]", fReserva)?.focus(); return;
    }
    const [netlify, supabase] = await Promise.all([aNetlify(fReserva), aSupabase("solicitudes_reserva", {
      tratamiento_slug: f.servicio.value, fecha: dia, hora: f.hora.value, franja: f.franja.value, nombre: f.nombre.value.trim(),
      telefono: f.telefono.value.trim() || null, email: f.email.value.trim() || null, acepta_privacidad: true })]);
    boton.disabled = false; boton.textContent = "Enviar solicitud";
    const c = srv && srv.estado === 200 ? srv.cuerpo : { calendario: srv ? "error" : "no-disponible", whatsapp: srv ? "error" : "no-disponible" };
    const llegó = [c.calendario, c.whatsapp, netlify, supabase].includes("ok");
    mostrarResultado(fReserva, { titulo: "Petición enviada", texto: `${servicio} · ${cuando}. Te escribimos para confirmarla.`, wa, llegó,
      lineas: [linea("calendario", c.calendario), linea("whatsapp", c.whatsapp), linea("netlify", netlify), linea("supabase", supabase)] });
  });

  const fRegalo = $("#form-regalo");
  if (fRegalo) {
    const f = fRegalo.elements;
    const vista = { para: $("#vr-para"), que: $("#vr-que"), msg: $("#vr-mensaje") };
    const sincronizar = () => {
      const exp = f.modalidad.value !== "importe";
      $("#campo-experiencia").hidden = !exp; $("#campo-importe").hidden = exp;
      vista.para.textContent = f.para_nombre.value.trim() || "Alguien especial";
      vista.que.textContent = exp ? (f.experiencia.value ? f.experiencia.selectedOptions[0].textContent : "Una experiencia a su elección") : (f.importe.value ? `${f.importe.value} € para lo que elija` : "Un importe para lo que elija");
      vista.msg.textContent = f.mensaje.value.trim() ? `«${f.mensaje.value.trim()}»` : "";
    };
    fRegalo.addEventListener("input", sincronizar); fRegalo.addEventListener("change", sincronizar); sincronizar();
    fRegalo.addEventListener("submit", async (e) => {
      e.preventDefault(); limpiar(fRegalo); let ok = true;
      const exp = f.modalidad.value !== "importe";
      if (exp && !f.experiencia.value) { marcarError(fRegalo, "experiencia", "Elige una experiencia."); ok = false; }
      if (!exp && !f.importe.value) { marcarError(fRegalo, "importe", "Elige un importe."); ok = false; }
      if (f.para_nombre.value.trim().length < 2) { marcarError(fRegalo, "para_nombre", "¿Para quién es la tarjeta?"); ok = false; }
      if (!validarContacto(fRegalo) || !ok) { $("[aria-invalid]", fRegalo)?.focus(); return; }
      const regalo = exp ? f.experiencia.selectedOptions[0].textContent.trim() : `${f.importe.value} €`;
      f.regalo_nombre.value = regalo;
      const wa = enlaceWA(`Hola, soy ${f.nombre.value.trim()}. Quiero una tarjeta regalo.\n\nRegalo: ${regalo}\nPara: ${f.para_nombre.value.trim()}${f.mensaje.value.trim() ? `\nMensaje: «${f.mensaje.value.trim()}»` : ""}\n${contactoTexto(f)}\n\n(Enviado desde la web)`);
      const boton = $('button[type="submit"]', fRegalo); boton.disabled = true; boton.textContent = "Enviando…";
      const [srv, netlify, supabase] = await Promise.all([
        aServidor("/api/regalo", { regalo_nombre: regalo, para_nombre: f.para_nombre.value.trim(), mensaje: f.mensaje.value.trim(),
          nombre: f.nombre.value.trim(), telefono: f.telefono.value.trim(), email: f.email.value.trim(), "bot-field": f["bot-field"].value }),
        aNetlify(fRegalo), aSupabase("solicitudes_regalo", {
          modalidad: exp ? "experiencia" : "importe", tratamiento_slug: exp ? f.experiencia.value : null, importe: exp ? null : Number(f.importe.value),
          para_nombre: f.para_nombre.value.trim(), mensaje: f.mensaje.value.trim() || null, nombre: f.nombre.value.trim(),
          telefono: f.telefono.value.trim() || null, email: f.email.value.trim() || null, acepta_privacidad: true })]);
      boton.disabled = false; boton.textContent = "Enviar solicitud";
      const w = srv ? (srv.estado === 200 ? srv.cuerpo.whatsapp : "error") : "no-disponible";
      mostrarResultado(fRegalo, { titulo: "Tarjeta regalo solicitada", texto: `${regalo} para ${f.para_nombre.value.trim()}. Te contactamos para el pago y te enviamos la tarjeta.`, wa,
        llegó: [w, netlify, supabase].includes("ok"), lineas: [linea("whatsapp", w), linea("netlify", netlify), linea("supabase", supabase)] });
    });
  }

  /* ---------- Movimiento ---------- */
  const reducido = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const puntero = matchMedia("(hover: hover) and (pointer: fine)").matches;

  // Portada: escenas con avance automático, pausa al pasar el ratón o enfocar, y botón de pausa (WCAG 2.2.2)
  const escenas = $(".escenas");
  if (escenas) {
    const lista = $$(".escena", escenas), mandos = $$(".escenas__mando", escenas), pausa = $(".escenas__pausa", escenas);
    const DUR = 7000; let actual = 0, temporizador, inicio = 0, restante = DUR, parada = reducido;
    const ir = (n) => {
      const prev = lista[actual]; actual = (n + lista.length) % lista.length; const sig = lista[actual];
      if (prev !== sig) {
        prev.classList.remove("es-activa"); prev.setAttribute("aria-hidden", "true"); $$("a", prev).forEach((a) => a.tabIndex = -1);
        sig.classList.add("es-activa"); sig.removeAttribute("aria-hidden"); $$("a", sig).forEach((a) => a.removeAttribute("tabindex"));
      }
      mandos.forEach((m, i) => { m.removeAttribute("aria-current"); if (i === actual) { void m.offsetWidth; m.setAttribute("aria-current", "true"); } });
      restante = DUR; programar();
    };
    const programar = () => { clearTimeout(temporizador); if (parada || escenas.classList.contains("en-pausa")) return; inicio = Date.now(); temporizador = setTimeout(() => ir(actual + 1), restante); };
    const congelar = () => { if (escenas.classList.contains("en-pausa")) return; escenas.classList.add("en-pausa"); clearTimeout(temporizador); restante = Math.max(400, restante - (Date.now() - inicio)); };
    const seguir = () => { if (!escenas.classList.contains("en-pausa")) return; escenas.classList.remove("en-pausa"); programar(); };
    mandos.forEach((m, i) => m.addEventListener("click", () => ir(i)));
    pausa.addEventListener("click", () => {
      parada = !parada; pausa.setAttribute("aria-pressed", String(parada)); pausa.setAttribute("aria-label", parada ? "Reanudar la presentación" : "Pausar la presentación");
      escenas.classList.toggle("parada", parada); if (!parada) { restante = DUR; ir(actual); } else clearTimeout(temporizador);
    });
    if (puntero) { escenas.addEventListener("mouseenter", congelar); escenas.addEventListener("mouseleave", seguir); }
    escenas.addEventListener("focusin", congelar); escenas.addEventListener("focusout", (e) => { if (!escenas.contains(e.relatedTarget)) seguir(); });
    document.addEventListener("visibilitychange", () => document.hidden ? congelar() : seguir());
    if (parada) { escenas.classList.add("parada"); pausa.setAttribute("aria-pressed", "true"); pausa.setAttribute("aria-label", "Reanudar la presentación"); }
    requestAnimationFrame(() => requestAnimationFrame(() => escenas.classList.add("lista")));
    programar();
    // Cabecera transparente mientras se ve la portada
    const alScrollPortada = () => {
      const visible = !escenas.closest("[hidden]") && window.scrollY < escenas.offsetHeight - cabecera.offsetHeight - 10;
      cabecera.classList.toggle("cabecera--clara", visible);
    };
    window.addEventListener("scroll", alScrollPortada, { passive: true }); window.addEventListener("hashchange", () => setTimeout(alScrollPortada)); alScrollPortada();
  }

  // Marquesina: se detiene con su botón (visible al tabular) o tocándola
  $$(".marquesina").forEach((m) => {
    const b = $(".marquesina__parar", m);
    const alternar = () => { const parada = m.classList.toggle("parada"); b.setAttribute("aria-pressed", String(parada)); b.textContent = parada ? "Reanudar el movimiento" : "Detener el movimiento"; };
    b.addEventListener("click", (e) => { e.stopPropagation(); alternar(); }); m.addEventListener("click", alternar);
  });

  // Entradas al hacer scroll (una sola vez) y contadores
  const contar = (el) => {
    const fin = parseFloat(el.dataset.cuenta), dec = +(el.dataset.decimales || 0), t0 = performance.now(), d = 1400;
    const paso = (t) => { const p = Math.min(1, (t - t0) / d), v = fin * (1 - Math.pow(1 - p, 3)); el.textContent = v.toFixed(dec).replace(".", ","); if (p < 1) requestAnimationFrame(paso); };
    requestAnimationFrame(paso);
  };
  if ("IntersectionObserver" in window && !reducido) {
    const io = new IntersectionObserver((ents) => ents.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("visible"); io.unobserve(en.target);
      $$("[data-cuenta]", en.target).forEach(contar);
    }), { threshold: 0.18, rootMargin: "0px 0px -6% 0px" });
    $$("[data-revela]").forEach((el) => io.observe(el));
  } else $$("[data-revela]").forEach((el) => el.classList.add("visible"));

  // Carta: la foto sigue al cursor (solo con ratón)
  const vistaCarta = $(".vista-carta");
  if (vistaCarta && puntero && !reducido) {
    const img = $("img", vistaCarta); let x = 0, y = 0;
    const mover = () => { vistaCarta.style.transform = `translate3d(${x + 28}px, ${y - 150}px, 0) rotate(-2deg)`; };
    $$(".carta__fila").forEach((a) => {
      a.addEventListener("mouseenter", (e) => { img.src = a.dataset.vista; x = e.clientX; y = e.clientY; mover(); vistaCarta.classList.add("visible"); });
      a.addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; mover(); });
      a.addEventListener("mouseleave", () => vistaCarta.classList.remove("visible"));
    });
    window.addEventListener("scroll", () => vistaCarta.classList.remove("visible"), { passive: true });
  }

  // Tarjeta regalo que se inclina con el ratón
  $$(".inclina").forEach((c) => {
    if (!puntero || reducido) return;
    c.addEventListener("mousemove", (e) => { const r = c.getBoundingClientRect();
      c.style.setProperty("--ry", ((e.clientX - r.left) / r.width - .5) * 10 + "deg"); c.style.setProperty("--rx", -((e.clientY - r.top) / r.height - .5) * 8 + "deg"); });
    c.addEventListener("mouseleave", () => { c.style.setProperty("--rx", "0deg"); c.style.setProperty("--ry", "0deg"); });
  });

  // Método: escena fija ligada al scroll (GSAP ScrollTrigger, solo escritorio y sin «reducir movimiento»)
  const ritual = $(".ritual");
  if (ritual && window.gsap && window.ScrollTrigger && !reducido) {
    gsap.registerPlugin(ScrollTrigger);
    const mm = gsap.matchMedia();
    mm.add("(min-width: 901px) and (min-height: 680px)", () => {
      ritual.classList.add("ritual--escena");
      const pasos = $$(".ritual__paso", ritual), fotos = $$(".ritual__foto", ritual);
      const tl = gsap.timeline({ scrollTrigger: { trigger: $(".ritual__pista", ritual), start: "top top", end: "bottom bottom", scrub: 0.6,
        onUpdate: (st) => { const i = Math.min(pasos.length - 1, Math.floor(st.progress * pasos.length * 0.999)); pasos.forEach((p, n) => p.classList.toggle("es-activo", n === i)); } } });
      tl.to($(".ritual__progreso i", ritual), { scaleY: 1, ease: "none", duration: 3 }, 0);
      fotos.slice(1).forEach((f, n) => tl.fromTo(f, { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", ease: "power2.inOut", duration: 0.7 }, n + 0.65));
      tl.fromTo($(".ritual__iso", ritual), { rotate: 4, yPercent: 8 }, { rotate: 16, yPercent: -6, ease: "none", duration: 3 }, 0);
      return () => { ritual.classList.remove("ritual--escena"); pasos.forEach((p, n) => p.classList.toggle("es-activo", n === 0)); gsap.set(fotos.slice(1), { clearProps: "clipPath" }); };
    });
    // Paralaje suave de la foto de «Conócenos»
    $$("[data-paralaje] img").forEach((img) => gsap.fromTo(img, { yPercent: -10 }, { yPercent: 0, ease: "none",
      scrollTrigger: { trigger: img.closest("[data-paralaje]"), start: "top bottom", end: "bottom top", scrub: true } }));
    if (VISTA) window.addEventListener("hashchange", () => setTimeout(() => ScrollTrigger.refresh(), 50));
  }

  /* ---------- Arranque de la vista previa (al final: usa el menú ya inicializado) ---------- */
  if (VISTA) { window.addEventListener("hashchange", mostrarPagina); mostrarPagina(); }
})();
