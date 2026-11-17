/* Rosa Ondoño · prototipo web
   Lee el catálogo de Supabase (REST + RLS de solo lectura). Si no hay conexión
   (p. ej. en la vista previa de Claude, que bloquea peticiones externas), usa la
   copia local datos/catalogo.json exportada de la misma base de datos.
   Las solicitudes de reserva se insertan en Supabase; nunca se dan por enviadas
   si la base de datos no confirma la inserción. */
(() => {
  "use strict";
  const CFG = window.RO_CONFIG || {};
  const TABLAS = ["pilares", "programas", "categorias", "profesionales", "tratamientos", "faqs"];
  const FOTOS = {
    hero: "img/fotos/02-recepcion-ventana-patio.jpg",
    recepcion: "img/fotos/01-recepcion.jpg",
    pasillo: "img/fotos/03-pasillo-cabinas.jpg",
    cabina: "img/fotos/06-cabina-hornacina-lavabo.jpg",
    cenador: "img/fotos/08-patio-jardin-cenador.jpg",
    patio: "img/fotos/10-patio-plantas.jpg"
  };
  const main = document.getElementById("contenido");
  const etiquetaFuente = document.getElementById("fuente-datos");
  let D = null;          // catálogo
  let fuente = "local";  // "vivo" | "local"
  const reserva = { paso: 1, slug: "", fecha: "", franja: "", nombre: "", telefono: "", email: "", acepta: false, errores: {}, resultado: null };

  /* ---------- utilidades ---------- */
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const por = (lista, campo) => Object.fromEntries(lista.map((x) => [x[campo], x]));
  const hoyMas = (dias) => { const d = new Date(); d.setDate(d.getDate() + dias); return d.toISOString().slice(0, 10); };
  const fechaLarga = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" });
  const icono = (nombre, etiqueta = "") => `<span class="icono" ${etiqueta ? `role="img" aria-label="${esc(etiqueta)}"` : 'aria-hidden="true"'}><i style="-webkit-mask-image:url('img/iconos/icono-${esc(nombre)}.svg');mask-image:url('img/iconos/icono-${esc(nombre)}.svg')"></i></span>`;
  const precio = (t) => t.tipo === "medico" ? "Precio tras consulta médica" : (t.precio_desde != null ? `Desde ${Number(t.precio_desde).toLocaleString("es-ES")} €` : '<span class="pendiente">Precio pendiente</span>');
  const duracion = (t) => t.duracion_min ? `${t.duracion_min} min` : '<span class="pendiente">Duración pendiente</span>';

  async function conTiempo(url, opciones = {}) {
    const ctl = new AbortController();
    const id = setTimeout(() => ctl.abort(), CFG.tiempoMaximoMs || 4000);
    try { return await fetch(url, { ...opciones, signal: ctl.signal }); } finally { clearTimeout(id); }
  }
  const cabecerasApi = () => ({ apikey: CFG.supabaseKey, Authorization: `Bearer ${CFG.supabaseKey}` });

  async function cargarCatalogo() {
    if (CFG.supabaseUrl && CFG.supabaseKey) {
      try {
        const respuestas = await Promise.all(TABLAS.map((t) => conTiempo(`${CFG.supabaseUrl}/rest/v1/${t}?select=*`, { headers: cabecerasApi() })));
        if (respuestas.every((r) => r.ok)) {
          const datos = await Promise.all(respuestas.map((r) => r.json()));
          fuente = "vivo";
          return Object.fromEntries(TABLAS.map((t, i) => [t, datos[i]]));
        }
      } catch (_) { /* sin conexión: seguimos con la copia local */ }
    }
    const r = await fetch("datos/catalogo.json");
    if (!r.ok) throw new Error("No se pudo leer datos/catalogo.json");
    fuente = "local";
    return r.json();
  }

  function preparar(d) {
    d.tratamientos.sort((a, b) => a.prioridad - b.prioridad || a.nombre.localeCompare(b.nombre, "es"));
    d.pilares.sort((a, b) => a.orden - b.orden);
    d.programas.sort((a, b) => a.orden - b.orden);
    d.categorias.sort((a, b) => a.orden - b.orden);
    d.idx = { t: por(d.tratamientos, "slug"), cat: por(d.categorias, "slug"), pil: por(d.pilares, "slug"), prog: por(d.programas, "slug"), prof: por(d.profesionales, "slug") };
    return d;
  }

  /* ---------- piezas ---------- */
  function tarjeta(t) {
    const cat = D.idx.cat[t.categoria_slug];
    return `<a class="tarjeta" href="#t-${esc(t.slug)}">
      <div style="display:flex;justify-content:space-between;align-items:start;gap:8px">${icono(cat?.icono || "valoracion")}${t.tipo === "medico" ? '<span class="chip chip--medico">Médico</span>' : ""}</div>
      <h3>${esc(t.nombre)}</h3>
      <p>${esc(t.resumen)}</p>
      <div class="tarjeta__pie"><span>${esc(cat?.nombre || "")}</span><span>${precio(t)}</span></div>
    </a>`;
  }
  const superIso = (color) => `<img class="pilar__super" src="img/isotipo-color.svg" alt="" aria-hidden="true" data-color="${color}">`;

  function bloquePilares() {
    return `<div class="pilares">${D.pilares.map((p) => {
      const progs = D.programas.filter((x) => x.pilar_slug === p.slug);
      return `<a class="pilar pilar--${esc(p.color)}" href="#${esc(p.slug)}">
        ${superIso(p.color)}
        <h3>${esc(p.nombre)}</h3>
        <p class="lema">${esc(p.lema)}</p>
        <ul>${progs.map((x) => `<li>${esc(x.nombre)}</li>`).join("")}${p.slug === "cuidate" ? "<li>Medicina estética</li>" : ""}${p.slug === "siente" ? "<li>Tarjeta regalo</li>" : ""}</ul>
        <span class="pilar__ir">Ver ${esc(p.nombre)} →</span>
      </a>`;
    }).join("")}</div>`;
  }

  /* ---------- vistas ---------- */
  function vistaInicio() {
    const destacados = D.tratamientos.filter((t) => t.destacado && t.slug !== "valoracion-integral");
    return `
    <section class="portada"><div class="envoltura portada__rejilla">
      <div class="portada__texto">
        <p class="lema">Cuídate · Conecta · Siente</p>
        <h1>Estética, manos expertas y medicina estética en el centro de Alicante</h1>
        <p class="entrada">Más de 30 años cuidando a personas en Av. Maisonnave. Empezamos escuchándote y te decimos lo que necesitas, y lo que no.</p>
        <div class="botonera"><a class="boton boton--primario" href="#reservar-valoracion-integral">Reservar valoración integral</a><a class="boton boton--secundario" href="#tratamientos">Ver tratamientos</a></div>
        <div class="prueba-social"><span><b>4,9 ★</b> en Google</span><span><b>+30 años</b> de oficio</span><span><b>Supervisión médica</b> en medicina estética</span></div>
      </div>
      <div class="portada__foto"><img src="${FOTOS.hero}" alt="Recepción del centro con luz natural y la puerta abierta al patio" width="1600" height="900"></div>
    </div></section>

    <section class="seccion seccion--blanca"><div class="envoltura">
      <div class="cabeza-seccion"><div><p class="antetitulo">Por necesidad</p><h2>¿Qué te gustaría hoy?</h2></div><p>Tres caminos para encontrar lo que buscas. Si ya sabes el nombre del tratamiento, <a href="#tratamientos">búscalo en el listado</a>.</p></div>
      ${bloquePilares()}
    </div></section>

    <section class="seccion seccion--morada"><div class="envoltura bloque-dos">
      <div>
        <p class="antetitulo" style="color:var(--lila)">Empieza aquí</p>
        <h2>Una valoración integral antes de decidir nada</h2>
        <ol class="pasos"><li>Nos cuentas qué te gustaría mejorar.</li><li>Analizamos piel, cuerpo y hábitos.</li><li>Te llevas un plan personalizado por escrito.</li></ol>
        <p>Sin compromiso. <span class="pendiente">Condiciones pendientes de confirmar</span></p>
        <div class="botonera"><a class="boton boton--claro" href="#reservar-valoracion-integral">Reservar mi valoración</a><a class="boton boton--secundario" style="color:#fff;border-color:#fff" href="#t-valoracion-integral">Saber más</a></div>
      </div>
      <img src="${FOTOS.recepcion}" alt="Mostrador de recepción con vitrina de productos y flores" width="1600" height="900" loading="lazy">
    </div></section>

    <section class="seccion"><div class="envoltura">
      <div class="cabeza-seccion"><div><p class="antetitulo">Los más pedidos</p><h2>Tratamientos destacados</h2></div><a class="boton boton--secundario" href="#tratamientos">Ver los ${D.tratamientos.length} tratamientos</a></div>
      <div class="rejilla">${destacados.map(tarjeta).join("")}</div>
    </div></section>

    <section class="seccion seccion--arena"><div class="envoltura">
      <div class="cabeza-seccion"><div><p class="antetitulo">Quién te cuida</p><h2>Personas con nombre y apellidos</h2></div><a href="#equipo">Conoce al equipo →</a></div>
      <div class="pilares" style="grid-template-columns:1fr 1fr">${D.profesionales.map(persona).join("")}</div>
    </div></section>

    <section class="seccion"><div class="envoltura">
      <div class="cabeza-seccion"><div><p class="antetitulo">El centro</p><h2>Un espacio tranquilo en pleno centro</h2></div><p>Av. Maisonnave 38, con patio ajardinado interior.</p></div>
      <div class="galeria">
        <figure><img src="${FOTOS.cenador}" alt="Patio ajardinado con cenador y plantas"><figcaption>Patio</figcaption></figure>
        <figure><img src="${FOTOS.recepcion}" alt="Recepción del centro"><figcaption>Recepción</figcaption></figure>
        <figure><img src="${FOTOS.pasillo}" alt="Pasillo interior con luz cálida y vitrinas"><figcaption>Pasillo</figcaption></figure>
        <figure><img src="${FOTOS.cabina}" alt="Una de las cabinas del centro"><figcaption>Una de nuestras cabinas</figcaption></figure>
        <figure><img src="${FOTOS.patio}" alt="Patio interior con plantas"><figcaption>Patio</figcaption></figure>
      </div>
    </div></section>

    <section class="seccion seccion--lila"><div class="envoltura bloque-dos">
      <div><p class="antetitulo">Siente · Regala</p><h2>Regala un momento para cuidarse</h2><p class="texto-corto">Una experiencia o un importe libre, para que la otra persona elija. Las tarjetas no incluyen tratamientos médicos.</p><a class="boton boton--primario" href="#regala">Ver tarjetas regalo</a></div>
      <img src="${FOTOS.patio}" alt="Patio interior con plantas" loading="lazy">
    </div></section>`;
  }

  function persona(p) {
    return `<article class="persona">
      <div class="retrato"><img src="img/isotipo-color.svg" alt="" aria-hidden="true"><span>Retrato pendiente de la sesión de fotos</span></div>
      <div><h3 style="font-size:1.6rem;font-weight:300">${esc(p.nombre)}</h3><p class="antetitulo">${esc(p.cargo)}</p>
      <p>${esc(p.bio)}</p>
      ${p.sanitario ? `<p>Nº de colegiado: ${p.num_colegiado ? esc(p.num_colegiado) : '<span class="pendiente">pendiente</span>'}</p>` : ""}</div>
    </article>`;
  }

  function vistaPilar(slug) {
    const p = D.idx.pil[slug];
    const progs = D.programas.filter((x) => x.pilar_slug === slug);
    const fondo = { marfil: "seccion--blanca", arena: "seccion--arena", lila: "seccion--lila" }[p.color];
    return `
    <section class="seccion ${fondo}" style="position:relative;overflow:hidden"><div class="envoltura">
      <img src="img/isotipo-color.svg" alt="" aria-hidden="true" style="position:absolute;right:-6%;top:-30%;height:170%;transform:rotate(-8deg);pointer-events:none">
      <nav class="migas" aria-label="Migas de pan" style="padding:0 0 18px"><ol><li><a href="#inicio">Inicio</a></li><li aria-current="page">${esc(p.nombre)}</li></ol></nav>
      <h1 style="position:relative">${esc(p.nombre)}</h1>
      <p class="lema" style="position:relative">${esc(p.lema)}</p>
      <p class="texto-corto" style="position:relative;max-width:52ch">${esc(p.descripcion)}</p>
      ${slug === "cuidate" ? '<a class="boton boton--primario" style="position:relative" href="#medicina-estetica">Medicina estética</a>' : ""}
    </div></section>
    ${progs.map((pr) => {
      const lista = D.tratamientos.filter((t) => t.programa_slug === pr.slug);
      return `<section class="seccion" id="prog-${esc(pr.slug)}"><div class="envoltura">
        <div class="cabeza-seccion"><div><p class="antetitulo">Programa</p><h2>${esc(pr.nombre)}</h2></div><p>${esc(pr.descripcion)}</p></div>
        <div class="rejilla">${lista.map(tarjeta).join("")}</div>
      </div></section>`;
    }).join("")}
    ${slug === "siente" ? '<section class="seccion seccion--lila"><div class="envoltura"><h2>¿Es para regalar?</h2><a class="boton boton--primario" href="#regala">Ver tarjetas regalo</a></div></section>' : ""}
    ${bloqueValoracion()}`;
  }

  const bloqueValoracion = () => `<section class="seccion seccion--morada"><div class="envoltura" style="display:flex;flex-wrap:wrap;gap:20px;justify-content:space-between;align-items:center">
    <div><h2 style="margin:0">¿No sabes por dónde empezar?</h2><p style="margin:.4rem 0 0">La valoración integral te orienta sin compromiso.</p></div>
    <a class="boton boton--claro" href="#reservar-valoracion-integral">Reservar valoración</a></div></section>`;

  function vistaTratamientos() {
    const opcCat = D.categorias.map((c) => `<option value="${esc(c.slug)}">${esc(c.nombre)}</option>`).join("");
    const opcPil = D.pilares.map((p) => `<option value="${esc(p.slug)}">${esc(p.nombre)}</option>`).join("");
    return `<section class="seccion"><div class="envoltura">
      <nav class="migas" aria-label="Migas de pan" style="padding:0 0 18px"><ol><li><a href="#inicio">Inicio</a></li><li aria-current="page">Tratamientos</li></ol></nav>
      <h1>Todos los tratamientos</h1>
      <p class="texto-corto">Busca por nombre o filtra por técnica y por pilar. Cada tratamiento tiene su propia ficha.</p>
      <div class="filtros" role="search">
        <div><label for="f-buscar">Buscar</label><input id="f-buscar" class="campo" type="search" placeholder="Ej.: drenaje, láser, labios"></div>
        <div><label for="f-cat">Técnica</label><select id="f-cat" class="campo"><option value="">Todas</option>${opcCat}</select></div>
        <div><label for="f-pil">Pilar</label><select id="f-pil" class="campo"><option value="">Todos</option>${opcPil}</select></div>
      </div>
      <p class="contador" id="contador" aria-live="polite"></p>
      <div class="rejilla" id="lista"></div>
    </div></section>`;
  }
  function activarFiltros() {
    const b = document.getElementById("f-buscar"), c = document.getElementById("f-cat"), p = document.getElementById("f-pil");
    const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
    const pintar = () => {
      const q = norm(b.value.trim());
      const lista = D.tratamientos.filter((t) => (!c.value || t.categoria_slug === c.value) && (!p.value || t.pilar_slug === p.value) && (!q || norm(t.nombre + " " + t.resumen).includes(q)));
      document.getElementById("lista").innerHTML = lista.map(tarjeta).join("") || '<p>No hay tratamientos con esos filtros. Prueba con otra palabra o <a href="#reservar-valoracion-integral">reserva una valoración</a> y te orientamos.</p>';
      document.getElementById("contador").textContent = `${lista.length} ${lista.length === 1 ? "tratamiento" : "tratamientos"}`;
    };
    [b, c, p].forEach((el) => el.addEventListener("input", pintar));
    pintar();
  }

  function vistaFicha(slug) {
    const t = D.idx.t[slug];
    if (!t) return vistaNoEncontrada();
    const cat = D.idx.cat[t.categoria_slug], pil = D.idx.pil[t.pilar_slug], prog = D.idx.prog[t.programa_slug], prof = D.idx.prof[t.profesional_slug];
    const faqs = D.faqs.filter((f) => f.tratamiento_slug === slug).sort((a, b) => a.orden - b.orden);
    const rel = D.tratamientos.filter((x) => x.slug !== slug && x.programa_slug && x.programa_slug === t.programa_slug).slice(0, 3);
    const medico = t.tipo === "medico";
    const cta = medico
      ? `<a class="boton boton--primario" href="#reservar-consulta-medica">Pedir consulta médica</a>`
      : t.reservable ? `<a class="boton boton--primario" href="#reservar-${esc(slug)}">Reservar este tratamiento</a>` : `<a class="boton boton--primario" href="https://wa.me/34691315622">Consultar por WhatsApp</a>`;
    return `<div class="envoltura">
      <nav class="migas" aria-label="Migas de pan"><ol><li><a href="#inicio">Inicio</a></li><li><a href="#${medico ? "medicina-estetica" : "tratamientos"}">${medico ? "Medicina estética" : "Tratamientos"}</a></li>${medico ? "" : `<li>${esc(cat?.nombre)}</li>`}<li aria-current="page">${esc(t.nombre)}</li></ol></nav>
      <div class="ficha__cabeza">
        <div>
          <p style="display:flex;gap:8px;flex-wrap:wrap"><a class="chip" href="#${esc(pil.slug)}">${esc(pil.nombre)}</a>${prog ? `<a class="chip" href="#${esc(pil.slug)}">${esc(prog.nombre)}</a>` : ""}${medico ? '<span class="chip chip--medico">Tratamiento médico</span>' : ""}</p>
          <h1>${esc(t.nombre)} <span style="display:block;font-size:.45em;color:var(--gris-texto);margin-top:.4em">en Alicante</span></h1>
          <p style="font-size:1.15rem" class="texto-corto">${esc(t.resumen)}</p>
          <div class="botonera" style="margin-top:22px">${cta}<a class="boton boton--secundario" href="https://wa.me/34691315622">WhatsApp</a></div>
          ${t.revision_pendiente ? `<p class="aviso-interno" style="margin-top:22px"><strong>Nota interna del prototipo:</strong> ${esc(t.revision_pendiente)}. No se publica hasta resolverlo.</p>` : ""}
        </div>
        <aside class="ficha__datos" aria-label="Datos clave">
          <div style="display:flex;gap:12px;align-items:center">${icono(cat?.icono || "valoracion")}<strong>${esc(cat?.nombre)}</strong></div>
          <dl style="margin:0">
            <div class="dato"><dt>Duración</dt><dd>${duracion(t)}</dd></div>
            <div class="dato"><dt>Sesiones</dt><dd>${esc(t.sesiones || "")}</dd></div>
            <div class="dato"><dt>Precio</dt><dd>${precio(t)}</dd></div>
            <div class="dato"><dt>Lo realiza</dt><dd>${prof ? `<a href="#equipo">${esc(prof.nombre)}</a>` : '<span class="pendiente">Profesional por confirmar</span>'}</dd></div>
          </dl>
          ${medico ? `<div class="aviso-medico">Tratamiento médico realizado por ${esc(prof?.nombre || "el médico del centro")}${prof?.num_colegiado ? `, nº col. ${esc(prof.num_colegiado)}` : ' (<span class="pendiente">nº de colegiado pendiente</span>)'}. Requiere valoración médica previa. Los resultados varían según cada persona.</div>` : ""}
        </aside>
      </div>
    </div>
    ${faqs.length ? `<section class="seccion seccion--blanca"><div class="envoltura" style="max-width:860px"><h2>Preguntas frecuentes</h2>${faqs.map((f) => `<details class="faq"><summary>${esc(f.pregunta)}</summary><p>${esc(f.respuesta)}</p></details>`).join("")}</div></section>` : ""}
    ${rel.length ? `<section class="seccion"><div class="envoltura"><h2>También te puede interesar</h2><div class="rejilla">${rel.map(tarjeta).join("")}</div></div></section>` : ""}
    ${slug !== "valoracion-integral" ? bloqueValoracion() : ""}`;
  }

  function vistaMedicina() {
    const lista = D.tratamientos.filter((t) => t.tipo === "medico" && t.slug !== "consulta-medica");
    const dr = D.idx.prof["dr-roberth-bravo-pardo"];
    return `<section class="seccion seccion--blanca"><div class="envoltura bloque-dos" style="align-items:start">
      <div>
        <nav class="migas" aria-label="Migas de pan" style="padding:0 0 18px"><ol><li><a href="#inicio">Inicio</a></li><li><a href="#cuidate">Cuídate</a></li><li aria-current="page">Medicina estética</li></ol></nav>
        <h1>Medicina estética con criterio médico</h1>
        <p class="texto-corto">Todos los tratamientos médicos empiezan con una consulta. El médico valora tu caso, te explica opciones, riesgos y alternativas, y decidís juntos si hay indicación. Buscamos resultados naturales, sin prisas ni promesas.</p>
        <a class="boton boton--primario" href="#reservar-consulta-medica">Pedir consulta médica</a>
      </div>
      ${persona(dr)}
    </div></section>
    <section class="seccion"><div class="envoltura">
      <div class="cabeza-seccion"><h2>Tratamientos médicos</h2><p>Información sanitaria. Ningún tratamiento se reserva sin consulta previa.</p></div>
      <div class="rejilla">${lista.map(tarjeta).join("")}</div>
      <p style="margin-top:28px;font-size:.9rem;color:var(--gris-texto)">Centro sanitario · <span class="pendiente">Nº de registro sanitario pendiente</span></p>
    </div></section>`;
  }

  const vistaEquipo = () => `<section class="seccion"><div class="envoltura">
      <nav class="migas" aria-label="Migas de pan" style="padding:0 0 18px"><ol><li><a href="#inicio">Inicio</a></li><li aria-current="page">Rosa y el equipo</li></ol></nav>
      <h1>Rosa y el equipo</h1><p class="lema">Manos expertas y criterio médico, bajo el mismo techo.</p>
      <div style="display:grid;gap:18px;margin-top:28px">${D.profesionales.map(persona).join("")}</div>
    </div></section>`;

  const vistaRegala = () => `<section class="seccion seccion--lila"><div class="envoltura bloque-dos">
      <div>
        <nav class="migas" aria-label="Migas de pan" style="padding:0 0 18px"><ol><li><a href="#inicio">Inicio</a></li><li><a href="#siente">Siente</a></li><li aria-current="page">Tarjeta regalo</li></ol></nav>
        <h1>Tarjeta regalo</h1>
        <p class="texto-corto">Elige una experiencia, como un ritual en pareja o un circuito spa, o un importe libre para que la otra persona decida.</p>
        <ul><li>Validez: <span class="pendiente">pendiente del centro</span></li><li>No incluye tratamientos de medicina estética (actos médicos).</li><li>Compra online: depende del sistema de reservas elegido.</li></ul>
        <div class="botonera"><a class="boton boton--primario" href="https://wa.me/34691315622">Pedirla por WhatsApp</a><a class="boton boton--secundario" href="#siente">Ver rituales</a></div>
      </div>
      <img src="${FOTOS.cenador}" alt="Patio ajardinado con cenador" loading="lazy">
    </div></section>`;

  /* ---------- reserva ---------- */
  function vistaReservar(slugInicial) {
    if (slugInicial && D.idx.t[slugInicial]?.reservable && reserva.slug !== slugInicial && reserva.paso === 1) reserva.slug = slugInicial;
    return `<section class="seccion"><div class="envoltura reserva">
      <nav class="migas" aria-label="Migas de pan" style="padding:0 0 18px"><ol><li><a href="#inicio">Inicio</a></li><li aria-current="page">Reservar</li></ol></nav>
      <h1>Reserva tu cita</h1>
      <p class="texto-corto">Tres pasos. Si lo prefieres, llámanos al <a href="tel:+34965120300">965 120 300</a> o escríbenos por <a href="https://wa.me/34691315622">WhatsApp</a>.</p>
      <div id="reserva"></div>
    </div></section>`;
  }

  function pintarReserva() {
    const caja = document.getElementById("reserva");
    if (!caja) return;
    const r = reserva, t = D.idx.t[r.slug];
    const pasos = ["Tratamiento", "Día y franja", "Tus datos"];
    const progreso = `<ol class="progreso" aria-label="Progreso">${pasos.map((n, i) => `<li class="${i + 1 < r.paso ? "hecho" : ""}" ${i + 1 === r.paso ? 'aria-current="step"' : ""}>${i + 1}. ${n}</li>`).join("")}</ol>`;
    const err = (k) => r.errores[k] ? `<p class="error" id="err-${k}">${r.errores[k]}</p>` : "";
    let cuerpo = "";

    if (r.resultado) {
      cuerpo = r.resultado.ok
        ? `<div class="estado estado--ok" role="status"><h2>Solicitud recibida</h2><p>${esc(t.nombre)} · ${esc(fechaLarga(r.fecha))} · por la ${r.franja === "manana" ? "mañana" : "tarde"}.</p><p>Se ha guardado en la base de datos del prototipo. En la web real, el centro la confirmaría por teléfono o email.</p><a class="boton boton--secundario" href="#inicio" data-reiniciar>Volver al inicio</a></div>`
        : r.resultado.demo
          ? `<div class="estado estado--demo" role="status"><h2>Vista previa sin conexión</h2><p>La solicitud <strong>no se ha enviado</strong>: esta vista no puede conectar con la base de datos. En la versión del repositorio, el mismo formulario la guarda en Supabase.</p><p class="resumen">${esc(t.nombre)} · ${esc(fechaLarga(r.fecha))} · ${r.franja === "manana" ? "mañana" : "tarde"} · ${esc(r.nombre)}</p><button class="boton boton--secundario" type="button" data-reiniciar>Empezar de nuevo</button></div>`
          : `<div class="estado estado--demo" role="alert"><h2>No se ha podido enviar</h2><p>${esc(r.resultado.mensaje)}</p><button class="boton boton--secundario" type="button" data-volver>Revisar los datos</button></div>`;
      caja.innerHTML = progreso + cuerpo;
      return;
    }

    if (r.paso === 1) {
      const grupos = D.categorias.map((c) => {
        const ops = D.tratamientos.filter((x) => x.reservable && x.categoria_slug === c.slug).sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
        return ops.length ? `<optgroup label="${esc(c.nombre)}">${ops.map((x) => `<option value="${esc(x.slug)}" ${x.slug === r.slug ? "selected" : ""}>${esc(x.nombre)}</option>`).join("")}</optgroup>` : "";
      }).join("");
      cuerpo = `<form class="panel" data-paso="1" novalidate>
        <label for="r-trat">¿Qué quieres reservar?</label>
        <select id="r-trat" class="campo" aria-describedby="r-trat-ayuda${r.errores.slug ? " err-slug" : ""}"><option value="">Elige un tratamiento</option>${grupos}</select>
        <p class="ayuda" id="r-trat-ayuda">Los tratamientos médicos se reservan como <strong>Consulta de medicina estética</strong>. Si dudas, elige <strong>Valoración integral</strong>.</p>
        ${err("slug")}
        ${t ? `<p class="resumen" style="margin-top:16px">${esc(t.resumen)}<br><span style="font-size:.88rem">${duracion(t)} · ${precio(t)}</span></p>` : ""}
        <div class="botonera" style="margin-top:22px"><button class="boton boton--primario" type="submit">Continuar</button></div>
      </form>`;
    } else if (r.paso === 2) {
      cuerpo = `<form class="panel" data-paso="2" novalidate>
        <p class="resumen"><strong>${esc(t.nombre)}</strong> · <button type="button" class="boton-menu" style="min-height:32px;border-color:var(--linea)" data-ir="1">Cambiar</button></p>
        <label for="r-fecha">Día preferido</label>
        <input id="r-fecha" class="campo" type="date" min="${hoyMas(1)}" max="${hoyMas(120)}" value="${esc(r.fecha)}" ${r.errores.fecha ? 'aria-describedby="err-fecha"' : ""}>
        ${err("fecha")}
        <fieldset style="border:0;padding:0;margin:16px 0 0"><legend style="font-weight:400;margin-bottom:8px">Franja</legend>
          <div class="opciones">
            <label class="opcion"><input type="radio" name="franja" value="manana" ${r.franja === "manana" ? "checked" : ""}><span>Mañana</span></label>
            <label class="opcion"><input type="radio" name="franja" value="tarde" ${r.franja === "tarde" ? "checked" : ""}><span>Tarde</span></label>
          </div>${err("franja")}
        </fieldset>
        <p class="ayuda">En la web definitiva aquí se verán los huecos reales del sistema de reservas.</p>
        <div class="botonera" style="margin-top:22px"><button class="boton boton--secundario" type="button" data-ir="1">Atrás</button><button class="boton boton--primario" type="submit">Continuar</button></div>
      </form>`;
    } else {
      cuerpo = `<form class="panel" data-paso="3" novalidate>
        <p class="resumen"><strong>${esc(t.nombre)}</strong> · ${esc(fechaLarga(r.fecha))} · ${r.franja === "manana" ? "mañana" : "tarde"}</p>
        <label for="r-nombre">Nombre y apellidos</label><input id="r-nombre" class="campo" autocomplete="name" value="${esc(r.nombre)}" ${r.errores.nombre ? 'aria-describedby="err-nombre"' : ""}>${err("nombre")}
        <label for="r-tel">Teléfono</label><input id="r-tel" class="campo" type="tel" autocomplete="tel" value="${esc(r.telefono)}" ${r.errores.telefono ? 'aria-describedby="err-telefono"' : ""}>${err("telefono")}
        <label for="r-email">Email</label><input id="r-email" class="campo" type="email" autocomplete="email" value="${esc(r.email)}" ${r.errores.email ? 'aria-describedby="err-email"' : ""}>${err("email")}
        <label class="casilla"><input id="r-acepta" type="checkbox" ${r.acepta ? "checked" : ""}><span>He leído la política de privacidad y acepto que se usen mis datos para gestionar esta cita.</span></label>${err("acepta")}
        <p class="ayuda">Prototipo: usa datos de prueba. No pedimos datos de salud en el formulario; los hablamos en persona.</p>
        <div class="botonera" style="margin-top:22px"><button class="boton boton--secundario" type="button" data-ir="2">Atrás</button><button class="boton boton--primario" type="submit">Enviar solicitud</button></div>
      </form>`;
    }
    caja.innerHTML = progreso + cuerpo;
    const primerError = caja.querySelector(".error");
    if (primerError) primerError.previousElementSibling?.focus?.();
  }

  function leerFormulario(paso) {
    const r = reserva; r.errores = {};
    if (paso === 1) { r.slug = document.getElementById("r-trat").value; if (!r.slug) r.errores.slug = "Elige un tratamiento para continuar."; }
    if (paso === 2) {
      r.fecha = document.getElementById("r-fecha").value; r.franja = document.querySelector('input[name="franja"]:checked')?.value || "";
      if (!r.fecha || r.fecha < hoyMas(1) || r.fecha > hoyMas(120)) r.errores.fecha = "Elige un día entre mañana y los próximos 4 meses.";
      else if ([0, 6].includes(new Date(r.fecha + "T12:00:00").getDay())) r.errores.fecha = "Abrimos de lunes a viernes: elige un día laborable.";
      if (!r.franja) r.errores.franja = "Elige mañana o tarde.";
    }
    if (paso === 3) {
      r.nombre = document.getElementById("r-nombre").value.trim(); r.telefono = document.getElementById("r-tel").value.trim();
      r.email = document.getElementById("r-email").value.trim(); r.acepta = document.getElementById("r-acepta").checked;
      if (r.nombre.length < 2) r.errores.nombre = "Escribe tu nombre.";
      if (!/^[+0-9 ]{9,16}$/.test(r.telefono)) r.errores.telefono = "Revisa el teléfono: solo números, mínimo 9.";
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(r.email)) r.errores.email = "Revisa el email: falta la @ o el dominio.";
      if (!r.acepta) r.errores.acepta = "Necesitamos tu consentimiento para gestionar la cita.";
    }
    return Object.keys(r.errores).length === 0;
  }

  async function enviarReserva() {
    const r = reserva;
    const cuerpo = { tratamiento_slug: r.slug, fecha: r.fecha, franja: r.franja, nombre: r.nombre, telefono: r.telefono, email: r.email, acepta_privacidad: true };
    try {
      const resp = await conTiempo(`${CFG.supabaseUrl}/rest/v1/solicitudes_reserva`, {
        method: "POST", headers: { ...cabecerasApi(), "Content-Type": "application/json", Prefer: "return=minimal" }, body: JSON.stringify(cuerpo)
      });
      r.resultado = resp.status === 201 ? { ok: true } : { ok: false, mensaje: "La base de datos ha rechazado la solicitud. Revisa los datos o llámanos al 965 120 300." };
    } catch (_) {
      r.resultado = { ok: false, demo: true };
    }
    pintarReserva();
  }

  main.addEventListener("submit", (e) => {
    const f = e.target.closest("form[data-paso]"); if (!f) return;
    e.preventDefault();
    const paso = Number(f.dataset.paso);
    if (!leerFormulario(paso)) { pintarReserva(); return; }
    if (paso < 3) { reserva.paso = paso + 1; pintarReserva(); document.getElementById("reserva").scrollIntoView({ block: "start" }); return; }
    const boton = f.querySelector('button[type="submit"]'); boton.disabled = true; boton.textContent = "Enviando…";
    enviarReserva();
  });
  main.addEventListener("click", (e) => {
    const ir = e.target.closest("[data-ir]");
    if (ir) { reserva.paso = Number(ir.dataset.ir); reserva.errores = {}; pintarReserva(); return; }
    if (e.target.closest("[data-volver]")) { reserva.resultado = null; reserva.paso = 3; pintarReserva(); return; }
    if (e.target.closest("[data-reiniciar]")) { Object.assign(reserva, { paso: 1, slug: "", fecha: "", franja: "", nombre: "", telefono: "", email: "", acepta: false, errores: {}, resultado: null }); pintarReserva(); }
  });
  main.addEventListener("change", (e) => {
    if (e.target.id === "r-trat") { reserva.slug = e.target.value; reserva.errores = {}; pintarReserva(); document.getElementById("r-trat").focus(); }
  });

  /* ---------- enrutado por hash ---------- */
  const vistaNoEncontrada = () => `<section class="seccion"><div class="envoltura"><h1>No encontramos esta página</h1><p><a href="#inicio">Volver al inicio</a> o <a href="#tratamientos">ver todos los tratamientos</a>.</p></div></section>`;

  function enrutar() {
    const ruta = (location.hash || "#inicio").slice(1);
    let html, tituloPagina = "Rosa Ondoño · Prototipo web", activa = ruta;
    if (ruta === "inicio" || ruta === "") html = vistaInicio();
    else if (D.idx.pil[ruta]) { html = vistaPilar(ruta); tituloPagina = `${D.idx.pil[ruta].nombre} · Rosa Ondoño`; }
    else if (ruta === "tratamientos") html = vistaTratamientos();
    else if (ruta.startsWith("t-")) { html = vistaFicha(ruta.slice(2)); const t = D.idx.t[ruta.slice(2)]; if (t) tituloPagina = `${t.nombre} en Alicante · Rosa Ondoño`; activa = t?.tipo === "medico" ? "medicina-estetica" : "tratamientos"; }
    else if (ruta === "medicina-estetica") html = vistaMedicina();
    else if (ruta === "equipo") html = vistaEquipo();
    else if (ruta === "regala") html = vistaRegala();
    else if (ruta === "reservar" || ruta.startsWith("reservar-")) { html = vistaReservar(ruta.slice(9)); activa = ""; }
    else html = vistaNoEncontrada();
    main.innerHTML = html;
    document.title = tituloPagina;
    document.querySelectorAll(".menu a").forEach((a) => { if (a.dataset.ruta === activa) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
    if (ruta === "tratamientos") activarFiltros();
    if (ruta === "reservar" || ruta.startsWith("reservar-")) pintarReserva();
    menu.classList.remove("abierto"); botonMenu.setAttribute("aria-expanded", "false");
    window.scrollTo(0, 0);
    if (location.hash) main.focus({ preventScroll: true });
  }

  const menu = document.getElementById("menu-principal");
  const botonMenu = document.querySelector(".boton-menu");
  botonMenu.addEventListener("click", () => { const abierto = menu.classList.toggle("abierto"); botonMenu.setAttribute("aria-expanded", String(abierto)); });

  cargarCatalogo().then((d) => {
    D = preparar(d);
    etiquetaFuente.textContent = fuente === "vivo" ? "Datos en vivo · Supabase" : `Copia local del catálogo de Supabase (${d.exportado ? String(d.exportado).slice(0, 10) : "sin fecha"})`;
    etiquetaFuente.classList.toggle("local", fuente !== "vivo");
    window.addEventListener("hashchange", enrutar);
    enrutar();
  }).catch(() => {
    etiquetaFuente.textContent = "Sin datos";
    main.innerHTML = '<div class="envoltura cargando">No se ha podido cargar el catálogo. Abre el prototipo desde un servidor local (ver LEEME.md).</div>';
  });
})();
