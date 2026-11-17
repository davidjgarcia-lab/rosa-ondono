/* Rosa Ondoño · web v2 · JS mínimo (mejora progresiva)
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

  /* ---------- Formularios: Netlify Forms (email) + Supabase (copia) + WhatsApp (mensaje al centro) ---------- */
  const hoyMas = (d) => { const f = new Date(); f.setDate(f.getDate() + d); return f.toISOString().slice(0, 10); };
  $$('input[type="date"][data-min-dias]').forEach((i) => { i.min = hoyMas(+i.dataset.minDias); i.max = hoyMas(+i.dataset.maxDias); });
  const fechaLarga = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" });
  const telOk = (v) => /^\+?[0-9 ]{9,16}$/.test(v), mailOk = (v) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);

  async function conTiempo(url, opciones) {
    const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), CFG.tiempoMaximoMs || 8000);
    try { return await fetch(url, { ...opciones, signal: ctl.signal }); } finally { clearTimeout(t); }
  }
  async function aNetlify(form) {
    if (VISTA || !/^https?:$/.test(location.protocol)) return "no-disponible";
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
  const enlaceWA = (texto) => `https://wa.me/${CFG.whatsapp || "34691315622"}?text=${encodeURIComponent(texto)}`;

  function marcarError(form, nombre, texto) {
    const campo = form.elements[nombre]; const el = campo instanceof RadioNodeList ? campo[0] : campo;
    const caja = el?.closest("[data-campo]"); if (!caja) return;
    const p = document.createElement("p"); p.className = "error"; p.id = `err-${form.id}-${nombre}`; p.textContent = texto;
    caja.appendChild(p); el.setAttribute("aria-describedby", p.id); el.setAttribute("aria-invalid", "true");
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
  function mostrarResultado(form, titulo, texto, envios, wa, ventanaAbierta) {
    const caja = $(".resultado", form.parentElement);
    const linea = (ok, si, no) => `<li>${ok ? "✓ " + si : "✕ " + no}</li>`;
    const algunEnvio = envios.netlify === "ok" || envios.supabase === "ok";
    caja.innerHTML = `<div class="estado ${algunEnvio ? "estado--ok" : "estado--aviso"}" role="status" tabindex="-1">
      <h2>${algunEnvio ? titulo : "Termina el envío por WhatsApp"}</h2><p>${texto}</p>
      <ul class="lista-envios">
        ${envios.netlify === "no-disponible" ? "<li>Aviso por email: disponible en la web publicada</li>" : linea(envios.netlify === "ok", "Aviso enviado al centro por email", "No se ha podido enviar el aviso por email")}
        ${linea(envios.supabase === "ok", "Solicitud guardada", "No se ha podido guardar en la base de datos (sin conexión)")}
        <li>${ventanaAbierta ? "WhatsApp abierto con tu mensaje: solo falta pulsar «Enviar»." : "Pulsa el botón para mandar el mensaje por WhatsApp."}</li>
      </ul>
      <div class="botonera"><a class="boton boton--primario" href="${wa}" target="_blank" rel="noopener">${ventanaAbierta ? "Abrir WhatsApp de nuevo" : "Enviar por WhatsApp"}</a>
      <button class="boton boton--secundario" type="button" data-otra>Hacer otra solicitud</button></div></div>`;
    caja.hidden = false; form.hidden = true; $(".estado", caja).focus();
    $("[data-otra]", caja).addEventListener("click", () => { caja.hidden = true; form.hidden = false; form.reset(); form.dispatchEvent(new Event("change")); form.elements[0]?.focus(); });
  }
  const contactoTexto = (f) => [f.telefono.value.trim() && `Teléfono: ${f.telefono.value.trim()}`, f.email.value.trim() && `Email: ${f.email.value.trim()}`].filter(Boolean).join("\n");

  const fReserva = $("#form-reserva");
  fReserva?.addEventListener("submit", async (e) => {
    e.preventDefault(); limpiar(fReserva);
    const f = fReserva.elements; let ok = true;
    if (!f.servicio.value) { marcarError(fReserva, "servicio", "Elige un tratamiento."); ok = false; }
    const dia = f.fecha.value;
    if (!dia || dia < f.fecha.min || dia > f.fecha.max) { marcarError(fReserva, "fecha", "Elige un día entre mañana y los próximos cuatro meses."); ok = false; }
    else if ([0, 6].includes(new Date(dia + "T12:00:00").getDay())) { marcarError(fReserva, "fecha", "Abrimos de lunes a viernes: elige un día laborable."); ok = false; }
    if (!f.franja.value) { marcarError(fReserva, "franja", "Elige mañana o tarde."); ok = false; }
    if (!validarContacto(fReserva) || !ok) { $("[aria-invalid]", fReserva)?.focus(); return; }
    const servicio = f.servicio.selectedOptions[0].textContent.trim();
    f.servicio_nombre.value = servicio;
    const texto = `Hola, soy ${f.nombre.value.trim()}. Quiero reservar cita.\n\nTratamiento: ${servicio}\nDía preferido: ${fechaLarga(dia)}\nFranja: ${f.franja.value === "manana" ? "mañana" : "tarde"}\n${contactoTexto(f)}\n\n(Enviado desde la web)`;
    const wa = enlaceWA(texto);
    const ventana = window.open(wa, "_blank"); if (ventana) ventana.opener = null; // mismo gesto del usuario: el navegador no lo bloquea
    const boton = $('button[type="submit"]', fReserva); boton.disabled = true; boton.textContent = "Enviando…";
    const [netlify, supabase] = await Promise.all([aNetlify(fReserva), aSupabase("solicitudes_reserva", {
      tratamiento_slug: f.servicio.value, fecha: dia, franja: f.franja.value, nombre: f.nombre.value.trim(),
      telefono: f.telefono.value.trim() || null, email: f.email.value.trim() || null, acepta_privacidad: true })]);
    boton.disabled = false; boton.textContent = "Enviar solicitud";
    mostrarResultado(fReserva, "Solicitud enviada", `${servicio} · ${fechaLarga(dia)} · por la ${f.franja.value === "manana" ? "mañana" : "tarde"}. Te contactaremos para confirmar la hora exacta.`, { netlify, supabase }, wa, ventana !== null);
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
      const texto = `Hola, soy ${f.nombre.value.trim()}. Quiero una tarjeta regalo.\n\nRegalo: ${regalo}\nPara: ${f.para_nombre.value.trim()}${f.mensaje.value.trim() ? `\nMensaje: «${f.mensaje.value.trim()}»` : ""}\n${contactoTexto(f)}\n\n(Enviado desde la web)`;
      const wa = enlaceWA(texto);
      const ventana = window.open(wa, "_blank"); if (ventana) ventana.opener = null;
      const boton = $('button[type="submit"]', fRegalo); boton.disabled = true; boton.textContent = "Enviando…";
      const [netlify, supabase] = await Promise.all([aNetlify(fRegalo), aSupabase("solicitudes_regalo", {
        modalidad: exp ? "experiencia" : "importe", tratamiento_slug: exp ? f.experiencia.value : null, importe: exp ? null : Number(f.importe.value),
        para_nombre: f.para_nombre.value.trim(), mensaje: f.mensaje.value.trim() || null, nombre: f.nombre.value.trim(),
        telefono: f.telefono.value.trim() || null, email: f.email.value.trim() || null, acepta_privacidad: true })]);
      boton.disabled = false; boton.textContent = "Enviar solicitud";
      mostrarResultado(fRegalo, "Tarjeta regalo solicitada", `${regalo} para ${f.para_nombre.value.trim()}. Te contactaremos para el pago y te enviaremos la tarjeta por email o WhatsApp.`, { netlify, supabase }, wa, ventana !== null);
    });
  }

  /* ---------- Arranque de la vista previa (al final: usa el menú ya inicializado) ---------- */
  if (VISTA) { window.addEventListener("hashchange", mostrarPagina); mostrarPagina(); }
})();
