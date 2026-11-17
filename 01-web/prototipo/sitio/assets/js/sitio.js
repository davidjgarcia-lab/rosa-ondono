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
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && panel?.classList.contains("abierto")) { cerrarMenu(); botonMenu?.focus(); } });

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

  /* ---------- Formularios → Supabase ---------- */
  const hoyMas = (d) => { const f = new Date(); f.setDate(f.getDate() + d); return f.toISOString().slice(0, 10); };
  $$('input[type="date"][data-min-dias]').forEach((i) => { i.min = hoyMas(+i.dataset.minDias); i.max = hoyMas(+i.dataset.maxDias); });

  async function insertar(tabla, datos) {
    const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), CFG.tiempoMaximoMs || 6000);
    try {
      const r = await fetch(`${CFG.supabaseUrl}/rest/v1/${tabla}`, {
        method: "POST", signal: ctl.signal,
        headers: { apikey: CFG.supabaseKey, Authorization: `Bearer ${CFG.supabaseKey}`, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify(datos)
      });
      return r.status === 201 ? "ok" : "rechazado";
    } catch (_) { return "sin-conexion"; } finally { clearTimeout(t); }
  }
  function marcarError(form, nombre, texto) {
    const campo = form.elements[nombre]; const caja = campo?.closest?.("[data-campo]") || campo?.[0]?.closest("[data-campo]");
    if (!caja) return;
    const p = document.createElement("p"); p.className = "error"; p.id = `err-${form.id}-${nombre}`; p.textContent = texto;
    caja.appendChild(p);
    (campo.setAttribute ? campo : campo[0]).setAttribute("aria-describedby", p.id);
    (campo.setAttribute ? campo : campo[0]).setAttribute("aria-invalid", "true");
  }
  function limpiar(form) { $$(".error", form).forEach((e) => e.remove()); $$("[aria-invalid]", form).forEach((e) => { e.removeAttribute("aria-invalid"); e.removeAttribute("aria-describedby"); }); }
  const tel = (v) => /^[+0-9 ]{9,16}$/.test(v), mail = (v) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
  function resultado(form, estado, ok) {
    const caja = $(".resultado", form.parentElement);
    const textos = {
      ok,
      "sin-conexion": "<h2>Vista previa sin conexión</h2><p>La solicitud <strong>no se ha enviado</strong>: esta vista no puede conectar con la base de datos. En la web publicada, el mismo formulario la guarda en Supabase.</p>",
      rechazado: '<h2>No se ha podido enviar</h2><p>Revisa los datos o escríbenos por WhatsApp al <a href="https://wa.me/34691315622">691 315 622</a>.</p>'
    };
    caja.innerHTML = `<div class="estado ${estado === "ok" ? "estado--ok" : "estado--aviso"}" role="status" tabindex="-1">${textos[estado]}</div>`;
    caja.hidden = false; $(".estado", caja).focus();
    if (estado === "ok") form.hidden = true;
  }

  const fReserva = $("#form-reserva");
  fReserva?.addEventListener("submit", async (e) => {
    e.preventDefault(); limpiar(fReserva);
    const f = fReserva.elements; let ok = true;
    if (!f.servicio.value) { marcarError(fReserva, "servicio", "Elige un tratamiento."); ok = false; }
    const dia = f.fecha.value;
    if (!dia || dia < f.fecha.min || dia > f.fecha.max) { marcarError(fReserva, "fecha", "Elige un día entre mañana y los próximos cuatro meses."); ok = false; }
    else if ([0, 6].includes(new Date(dia + "T12:00:00").getDay())) { marcarError(fReserva, "fecha", "Abrimos de lunes a viernes: elige un día laborable."); ok = false; }
    if (!f.franja.value) { marcarError(fReserva, "franja", "Elige mañana o tarde."); ok = false; }
    if (f.nombre.value.trim().length < 2) { marcarError(fReserva, "nombre", "Escribe tu nombre."); ok = false; }
    if (!tel(f.telefono.value.trim())) { marcarError(fReserva, "telefono", "Revisa el teléfono: solo números, mínimo 9."); ok = false; }
    if (!mail(f.email.value.trim())) { marcarError(fReserva, "email", "Revisa el email."); ok = false; }
    if (!f.privacidad.checked) { marcarError(fReserva, "privacidad", "Necesitamos tu consentimiento para gestionar la cita."); ok = false; }
    if (!ok) { $("[aria-invalid]", fReserva)?.focus(); return; }
    const boton = $('button[type="submit"]', fReserva); boton.disabled = true; boton.textContent = "Enviando…";
    const estado = await insertar("solicitudes_reserva", { tratamiento_slug: f.servicio.value, fecha: dia, franja: f.franja.value, nombre: f.nombre.value.trim(), telefono: f.telefono.value.trim(), email: f.email.value.trim(), acepta_privacidad: true });
    boton.disabled = false; boton.textContent = "Solicitar cita";
    const nombreServicio = f.servicio.selectedOptions[0].textContent;
    resultado(fReserva, estado, `<h2>Solicitud recibida</h2><p>${nombreServicio} · ${new Date(dia + "T12:00:00").toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" })} · por la ${f.franja.value === "manana" ? "mañana" : "tarde"}.</p><p>Te llamaremos o escribiremos para confirmar la hora exacta.</p>`);
  });

  const fRegalo = $("#form-regalo");
  if (fRegalo) {
    const f = fRegalo.elements;
    const vista = { para: $("#vr-para"), que: $("#vr-que"), msg: $("#vr-mensaje") };
    const sincronizar = () => {
      const exp = f.modalidad.value === "experiencia";
      $("#campo-experiencia").hidden = !exp; $("#campo-importe").hidden = exp;
      vista.para.textContent = f.para_nombre.value.trim() || "Alguien especial";
      vista.que.textContent = exp ? (f.experiencia.value ? f.experiencia.selectedOptions[0].textContent : "Una experiencia a su elección") : (f.importe.value ? `${f.importe.value} € para lo que elija` : "Un importe para lo que elija");
      vista.msg.textContent = f.mensaje.value.trim() ? `«${f.mensaje.value.trim()}»` : "";
    };
    fRegalo.addEventListener("input", sincronizar); fRegalo.addEventListener("change", sincronizar); sincronizar();
    fRegalo.addEventListener("submit", async (e) => {
      e.preventDefault(); limpiar(fRegalo); let ok = true;
      const exp = f.modalidad.value === "experiencia";
      if (exp && !f.experiencia.value) { marcarError(fRegalo, "experiencia", "Elige una experiencia."); ok = false; }
      if (!exp && !f.importe.value) { marcarError(fRegalo, "importe", "Elige un importe."); ok = false; }
      if (f.para_nombre.value.trim().length < 2) { marcarError(fRegalo, "para_nombre", "¿Para quién es?"); ok = false; }
      if (f.nombre.value.trim().length < 2) { marcarError(fRegalo, "nombre", "Escribe tu nombre."); ok = false; }
      if (!tel(f.telefono.value.trim())) { marcarError(fRegalo, "telefono", "Revisa el teléfono: solo números, mínimo 9."); ok = false; }
      if (!mail(f.email.value.trim())) { marcarError(fRegalo, "email", "Revisa el email."); ok = false; }
      if (!f.privacidad.checked) { marcarError(fRegalo, "privacidad", "Necesitamos tu consentimiento para preparar la tarjeta."); ok = false; }
      if (!ok) { $("[aria-invalid]", fRegalo)?.focus(); return; }
      const boton = $('button[type="submit"]', fRegalo); boton.disabled = true; boton.textContent = "Enviando…";
      const estado = await insertar("solicitudes_regalo", {
        modalidad: exp ? "experiencia" : "importe", tratamiento_slug: exp ? f.experiencia.value : null, importe: exp ? null : Number(f.importe.value),
        para_nombre: f.para_nombre.value.trim(), mensaje: f.mensaje.value.trim() || null, nombre: f.nombre.value.trim(), telefono: f.telefono.value.trim(), email: f.email.value.trim(), acepta_privacidad: true
      });
      boton.disabled = false; boton.textContent = "Solicitar tarjeta regalo";
      resultado(fRegalo, estado, "<h2>Tarjeta regalo solicitada</h2><p>Te contactaremos hoy mismo para el pago y te enviaremos la tarjeta por email, lista para imprimir o reenviar.</p>");
    });
  }
  /* ---------- Arranque de la vista previa (al final: usa el menú ya inicializado) ---------- */
  if (VISTA) { window.addEventListener("hashchange", mostrarPagina); mostrarPagina(); }
})();
