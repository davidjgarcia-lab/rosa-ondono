#!/usr/bin/env python3
"""Rosa Ondoño · generador de la web v2 (prototipo).

Lee el catálogo de Supabase (o la copia local datos/catalogo.json) y genera:
  sitio/                 web estática multipágina con URLs limpias (SEO)
  sitio/vista-previa.html todas las páginas en un solo archivo, enrutadas por #ancla
                          (para la vista previa en Claude, que no navega entre archivos)
Además: sitemap.xml, robots.txt, _redirects (301 de la web actual), 404.html.

Uso:  python3 generar_sitio.py            (sirve después con: cd sitio && python3 -m http.server)
"""
import csv, html, json, re, shutil, urllib.request
from datetime import date
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).parent
SALIDA = RAIZ / "sitio"
DOMINIO = "https://rosaondono.com"
HOY = date.today().isoformat()
WA = "https://wa.me/34691315622?text=" + urllib.request.quote("Hola, me gustaría información sobre ")
MAPS = "https://www.google.com/maps/search/?api=1&query=" + urllib.request.quote("Rosa Ondoño, Av. Maisonnave 38, 03003 Alicante")
INSTAGRAM, FACEBOOK = "https://www.instagram.com/rosaondono/", "https://www.facebook.com/RosaOndono"
e = lambda s: html.escape(str(s or ""), quote=True)

# ---------------------------------------------------------------- datos
def cargar():
    cfg = (RAIZ / "fuente" / "config.js").read_text()
    url = re.search(r'supabaseUrl:\s*"([^"]+)"', cfg).group(1)
    key = re.search(r'supabaseKey:\s*"([^"]+)"', cfg).group(1)
    tablas = ["areas", "pilares", "programas", "categorias", "profesionales", "tratamientos", "faqs"]
    try:
        d = {}
        for t in tablas:
            req = urllib.request.Request(f"{url}/rest/v1/{t}?select=*", headers={"apikey": key, "Authorization": f"Bearer {key}"})
            d[t] = json.load(urllib.request.urlopen(req, timeout=8))
        d["origen"] = "Supabase (en vivo)"
        (RAIZ / "datos" / "catalogo.json").write_text(json.dumps({**d, "exportado": HOY}, ensure_ascii=False, indent=1))
    except Exception as err:
        d = json.loads((RAIZ / "datos" / "catalogo.json").read_text())
        d["origen"] = f"copia local datos/catalogo.json ({type(err).__name__} al conectar con Supabase)"
    return d

D = cargar()
AREAS = sorted(D["areas"], key=lambda a: a["orden"])
CATS = sorted(D["categorias"], key=lambda c: c["orden"])
TRAT = sorted(D["tratamientos"], key=lambda t: (t["prioridad"], t["nombre"]))
I = {"t": {t["slug"]: t for t in TRAT}, "c": {c["slug"]: c for c in CATS}, "a": {a["slug"]: a for a in AREAS},
     "p": {p["slug"]: p for p in D["profesionales"]}}
FAQS = {}
for f in sorted(D["faqs"], key=lambda f: f["orden"]):
    FAQS.setdefault(f["tratamiento_slug"], []).append(f)
area_de = lambda t: I["c"][t["categoria_slug"]].get("area_slug")

# ---------------------------------------------------------------- imágenes
FOTO_CAT = {"faciales": "u-facial-mascarilla", "corporales": "u-corporal", "depilacion": "u-corporal", "belleza": "u-manos",
            "medicina-estetica": "u-retrato-natural", "masajes": "u-masaje-espalda", "terapias-complementarias": "u-terapia-agujas",
            "rituales": "u-piedras-flores", "valoracion": "01-recepcion"}
FOTO_AREA = {"estetica": "u-facial-mascarilla", "medicina-estetica": "u-retrato-natural", "terapias": "u-masaje-espalda", "bienestar": "u-piedras-flores"}
POOL = {"faciales": ["u-facial-mascarilla", "u-facial-masaje", "u-retrato-natural"],
        "corporales": ["u-corporal", "u-masaje-espalda", "u-manos"],
        "depilacion": ["u-corporal", "u-manos"],
        "belleza": ["u-manos", "u-retrato-natural"],
        "medicina-estetica": ["u-retrato-natural", "02-recepcion-ventana-patio"],
        "masajes": ["u-masaje-espalda", "u-corporal", "u-piedras-flores"],
        "terapias-complementarias": ["u-terapia-agujas", "u-masaje-espalda"],
        "rituales": ["u-piedras-flores", "08-patio-jardin-cenador"]}
FONDOS = ["f-lila", "f-arena", "f-morado"]
FOTO_TRAT = {"consulta-medica": "01-recepcion", "valoracion-integral": "01-recepcion", "drenaje-linfatico-postoperatorio": "u-masaje-espalda", "presoterapia": "u-corporal", "masaje-relajante": "u-piedras-flores",
             "ritual-en-pareja": "u-piedras-flores", "limpieza-facial-profunda": "u-facial-mascarilla",
             "manicura-y-pedicura": "u-manos"}
ALT = {"u-facial-mascarilla": "Mujer recibiendo un tratamiento facial con mascarilla en cabina",
       "u-facial-masaje": "Manos de terapeuta realizando un masaje facial suave",
       "u-corporal": "Persona tumbada recibiendo un tratamiento corporal",
       "u-manos": "Masaje de manos sobre una toalla",
       "u-retrato-natural": "Retrato de una mujer con la piel natural y luz cálida",
       "u-masaje-espalda": "Manos expertas realizando un masaje de espalda",
       "u-terapia-agujas": "Terapeuta realizando una sesión de terapia complementaria",
       "u-piedras-flores": "Ritual de masaje con piedras calientes y flores blancas",
       "01-recepcion": "Recepción del centro Rosa Ondoño con flores y vitrina",
       "02-recepcion-ventana-patio": "Recepción con luz natural y la puerta abierta al patio",
       "03-pasillo-cabinas": "Pasillo interior del centro con luz cálida",
       "06-cabina-hornacina-lavabo": "Una de las cabinas del centro",
       "08-patio-jardin-cenador": "Patio ajardinado con cenador en el centro",
       "10-patio-plantas": "Patio interior con plantas"}
TAM = {}
VISUAL = {}  # slug -> ("foto", stem) | ("grafica", fondo, icono)
def asignar_visuales():
    for n, c in enumerate(CATS):
        lista = [t for t in TRAT if t["categoria_slug"] == c["slug"]]
        pool = POOL.get(c["slug"], ["01-recepcion"])
        k = 0  # rota las fotos del grupo para que dos tarjetas seguidas no repitan imagen
        for i, t in enumerate(lista):
            if t["slug"] in FOTO_TRAT: VISUAL[t["slug"]] = ("foto", FOTO_TRAT[t["slug"]])
            elif i % 3 == 2: VISUAL[t["slug"]] = ("grafica", FONDOS[(n + i) % 3], c.get("icono") or "valoracion")
            else:
                previo = VISUAL.get(lista[i - 1]["slug"], ("",))[-1] if i else ""
                if pool[k % len(pool)] == previo: k += 1
                VISUAL[t["slug"]] = ("foto", pool[k % len(pool)]); k += 1
        # segunda pasada: ninguna foto igual a la de al lado
        for i, t in enumerate(lista):
            v = VISUAL[t["slug"]]
            if v[0] != "foto" or t["slug"] in FOTO_TRAT: continue
            vecinos = {VISUAL[lista[j]["slug"]][-1] for j in (i - 1, i + 1) if 0 <= j < len(lista)}
            if v[1] in vecinos:
                alternativa = next((x for x in pool if x not in vecinos), v[1])
                VISUAL[t["slug"]] = ("foto", alternativa)
def foto_principal(t):
    v = VISUAL[t["slug"]]
    return v[1] if v[0] == "foto" else POOL.get(t["categoria_slug"], ["01-recepcion"])[0]

def preparar_imagenes():
    dst = SALIDA / "assets" / "img"
    for f in (RAIZ / "img" / "fotos").glob("*.jpg"):
        im = Image.open(f).convert("RGB")
        TAM[f.stem] = im.size
        for w in (800, 1600):
            c = im.copy(); c.thumbnail((w, w * 2))
            c.save(dst / f"{f.stem}-{w}.webp", quality=72, method=5)
        c = im.copy(); c.thumbnail((1600, 3200)); c.save(dst / f"{f.stem}.jpg", quality=74, optimize=True, progressive=True)
        TAM[f.stem] = c.size

# ---------------------------------------------------------------- enlaces (estático / vista previa)
MODO = "estatico"
def pid(ruta):
    """Identificador de página para la vista previa (#ancla) a partir de la ruta."""
    r = ruta.strip("/")
    if not r: return "inicio"
    if r.startswith("tratamientos/") or r.startswith("medicina-estetica/") and r.count("/") == 1:
        return "t-" + r.split("/")[-1]
    return r.replace("/", "-")
def L(ruta, ancla=""):
    if MODO == "vista":
        return "#" + (ancla or pid(ruta))
    return ruta + ("#" + ancla if ancla else "")
def A(ruta):  # recursos
    return ("" if MODO == "vista" else "/") + "assets/" + ruta
def ruta_trat(t):
    if t["slug"] == "valoracion-integral": return "/valoracion-integral/"  # tiene landing propia: sin ficha duplicada
    return f"/medicina-estetica/{t['slug']}/" if t["tipo"] == "medico" else f"/tratamientos/{t['slug']}/"
def ruta_reserva(slug=""):
    if MODO == "vista": return "#reservar" + (f"--{slug}" if slug else "")
    return "/reservar/" + (f"?servicio={slug}" if slug else "")
def ruta_regalo(slug=""):
    if MODO == "vista": return "#regalar" + (f"--{slug}" if slug else "")
    return "/regalar/" + (f"?servicio={slug}" if slug else "")

def foto(stem, clase="", sizes="(max-width: 800px) 100vw, 50vw", carga="lazy", alt=None):
    w, h = TAM.get(stem, (1600, 1067))
    alt = ALT.get(stem, "") if alt is None else alt
    return (f'<picture><source type="image/webp" srcset="{A(f"img/{stem}-800.webp")} 800w, {A(f"img/{stem}-1600.webp")} 1600w" sizes="{sizes}">'
            f'<img src="{A(f"img/{stem}.jpg")}" alt="{e(alt)}" width="{w}" height="{h}" loading="{carga}" decoding="async"{f" class={chr(34)}{clase}{chr(34)}" if clase else ""}{" fetchpriority=" + chr(34) + "high" + chr(34) if carga == "eager" else ""}></picture>')
def iso(clase, color="color"):
    return f'<img class="{clase}" src="{A(f"img/isotipo-{color}.svg")}" alt="" aria-hidden="true" width="171" height="238">'

def precio(t):
    if t["tipo"] == "medico": return "Tras consulta médica"
    return f'Desde {t["precio_desde"]:g} €' if t.get("precio_desde") else "Precio a consultar"
def migas(items):
    li = "".join(f'<li><a href="{L(r)}">{e(n)}</a></li>' if r else f'<li aria-current="page">{e(n)}</li>' for n, r in items)
    return f'<nav class="migas" aria-label="Migas de pan"><ol>{li}</ol></nav>'

def tarjeta(t, cabecera="h3"):
    cat = I["c"][t["categoria_slug"]]
    v = VISUAL[t["slug"]]
    if v[0] == "foto":
        visual = f'<div class="tarjeta__foto">{foto(v[1], sizes="(max-width: 600px) 100vw, 320px", alt="")}</div>'
    else:
        visual = (f'<div class="tarjeta__foto tarjeta__foto--grafica {v[1]}">{iso("super", "blanco" if v[1] == "f-morado" else "color")}'
                  f'<i style="-webkit-mask-image:url({A("img/iconos/icono-" + v[2] + ".svg")});mask-image:url({A("img/iconos/icono-" + v[2] + ".svg")})"></i></div>')
    if t["tipo"] == "medico" and t["slug"] != "consulta-medica":
        boton = f'<a class="boton boton--secundario boton--pequeno" href="{ruta_reserva("consulta-medica")}">Pedir consulta</a>'
    elif t["reservable"]:
        boton = f'<a class="boton boton--secundario boton--pequeno" href="{ruta_reserva(t["slug"])}" aria-label="Reservar {e(t["nombre"])}">Reservar</a>'
    else:
        boton = ""
    return f'''<article class="tarjeta">
  {visual}
  {'<span class="etiqueta etiqueta--medico">Médico</span>' if t["tipo"] == "medico" else ""}
  <div class="tarjeta__cuerpo">
    <span class="tarjeta__cat">{e(cat["nombre"])}</span>
    <{cabecera}><a href="{L(ruta_trat(t))}">{e(t["nombre"])}</a></{cabecera}>
    <p>{e(t["resumen"])}</p>
    <div class="tarjeta__pie"><span>{e(precio(t))}</span>{boton}</div>
  </div>
</article>'''

# ---------------------------------------------------------------- piezas comunes
MENU = [("Estética", "/estetica/", "estetica"), ("Medicina estética", "/medicina-estetica/", "medicina-estetica"),
        ("Terapias", "/terapias/", "terapias"), ("Bienestar", "/bienestar/", "bienestar"), ("Conócenos", "/conocenos/", "conocenos")]
SVG_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.16.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.29Z"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2Zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2.1.4-.5.2-.9.4-1.3.8-.4.4-.6.8-.8 1.3-.2.4-.3 1-.4 2.1C2.6 9.9 2.6 10.3 2.6 12s0 3.5.1 4.7c.1 1.1.2 1.7.4 2.1.2.5.4.9.8 1.3.4.4.8.6 1.3.8.4.2 1 .3 2.1.4 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2.1-.4.5-.2.9-.4 1.3-.8.4-.4.6-.8.8-1.3.2-.4.3-1 .4-2.1.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c-.1-1.1-.2-1.7-.4-2.1-.2-.5-.4-.9-.8-1.3-.4-.4-.8-.6-1.3-.8-.4-.2-1-.3-2.1-.4C15.5 4 15.1 4 12 4Zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8Zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4Zm6.2-8.3a1.1 1.1 0 1 1-2.3 0 1.1 1.1 0 0 1 2.3 0Z"/></svg>'
SVG_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21.9v-7.7h2.6l.4-3h-3V9.3c0-.9.3-1.5 1.5-1.5h1.6V5.1c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6v7.7h3.1Z"/></svg>'
SVG_MAPA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>'

def cabecera(activa):
    items = "".join(f'<li><a href="{L(r)}" data-menu="{m}"{" aria-current=page" if m == activa else ""}>{n}</a></li>' for n, r, m in MENU)
    items_m = "".join(f'<li><a href="{L(r)}" data-menu="{m}">{n}</a></li>' for n, r, m in MENU)
    return f'''<div class="barra-prototipo" role="note"><span class="largo">Prototipo con el manual de marca v2.1 · fotos de tratamientos provisionales (Unsplash) · </span><span class="corto">Prototipo · </span>no introduzcas datos reales</div>
<header class="cabecera">
  <div class="cabecera__fila">
    <a class="cabecera__logo" href="{L("/")}" aria-label="Rosa Ondoño, ir al inicio"><img class="logo-color" src="{A("img/logo-horizontal.svg")}" alt="Rosa Ondoño" width="172" height="57"><img class="logo-blanco" src="{A("img/logo-horizontal-blanco.svg")}" alt="" width="172" height="57"></a>
    <nav aria-label="Principal"><ul class="menu">{items}</ul></nav>
    <div class="cabecera__acciones">
      <a class="boton boton--secundario boton--regalar" href="{ruta_regalo()}">Regalar</a>
      <a class="boton boton--primario" href="{ruta_reserva()}">Reservar</a>
      <button class="boton-menu" type="button" aria-expanded="false" aria-controls="panel-menu">Menú</button>
    </div>
  </div>
</header>
<div class="panel-menu" id="panel-menu" role="dialog" aria-modal="true" aria-label="Menú">
  <div class="panel-menu__cabeza"><img src="{A("img/logo-horizontal-blanco.svg")}" alt="Rosa Ondoño" width="160" height="53"><button class="boton boton--borde-claro boton--pequeno" type="button" id="cerrar-menu">Cerrar</button></div>
  <ul>{items_m}</ul>
  <p class="lema">Cuídate · Conecta · Siente</p>
  <div class="botonera"><a class="boton boton--claro" href="{ruta_reserva()}">Reservar cita</a><a class="boton boton--borde-claro" href="{ruta_regalo()}">Regalar</a></div>
</div>'''

def pie():
    areas = "".join(f'<li><a href="{L("/" + a["slug"] + "/")}">{e(a["nombre"])}</a></li>' for a in AREAS)
    return f'''<footer class="pie">
  <div class="envoltura">
    <div class="pie__rejilla">
      <div>
        <img class="pie__logo" src="{A("img/logo-horizontal-blanco.svg")}" alt="Rosa Ondoño" width="190" height="63" loading="lazy">
        <p class="lema" style="color:var(--lila)">Cuídate · Conecta · Siente</p>
        <p>Centro de estética, terapias y medicina estética en el centro de Alicante desde hace más de 30 años.</p>
        <div class="redes">
          <a href="{INSTAGRAM}" aria-label="Instagram de Rosa Ondoño" rel="noopener">{SVG_IG}</a>
          <a href="{FACEBOOK}" aria-label="Facebook de Rosa Ondoño" rel="noopener">{SVG_FB}</a>
          <a href="{MAPS}" aria-label="Rosa Ondoño en Google Maps" rel="noopener">{SVG_MAPA}</a>
        </div>
      </div>
      <div>
        <h2 class="pie__titulo">Visítanos</h2>
        <p>Av. Maisonnave 38, Entlo. Izq.<br>03003 Alicante</p>
        <p><a href="{MAPS}" rel="noopener">Cómo llegar en Google Maps →</a></p>
        <p>Lunes a viernes, 9:00–19:00<br><span class="pendiente">Horario de invierno: pendiente</span></p>
      </div>
      <div>
        <h2 class="pie__titulo">Contacto</h2>
        <ul><li><a href="tel:+34965120300">965 120 300</a></li><li><a href="{WA}">WhatsApp 691 315 622</a></li><li><a href="mailto:info@rosaondono.com">info@rosaondono.com</a></li></ul>
        <h2 class="pie__titulo" style="margin-top:26px">Tu cita</h2>
        <ul><li><a href="{ruta_reserva()}">Reservar</a></li><li><a href="{ruta_regalo()}">Tarjeta regalo</a></li><li><a href="{L("/valoracion-integral/")}">Valoración integral</a></li></ul>
      </div>
      <div>
        <h2 class="pie__titulo">Especialidades</h2>
        <ul>{areas}<li><a href="{L("/conocenos/")}">Conócenos</a></li></ul>
      </div>
    </div>
    <div class="pie__legal">
      <span>© {date.today().year} Rosa Ondoño · <span class="pendiente">Nº de registro sanitario: pendiente</span></span>
      <ul><li><a href="{L("/aviso-legal/")}">Aviso legal</a></li><li><a href="{L("/privacidad/")}">Privacidad</a></li><li><a href="{L("/cookies/")}">Cookies</a></li><li><button type="button" data-abrir-cookies>Configurar cookies</button></li></ul>
    </div>
  </div>
</footer>'''

def flotantes():
    return f'''<a class="whatsapp" href="{WA}" rel="noopener" aria-label="Escríbenos por WhatsApp">{SVG_WA}<span class="whatsapp__et" aria-hidden="true">Escríbenos</span></a>
<section class="cookies" id="cookies" hidden aria-labelledby="cookies-titulo">
  <h2 id="cookies-titulo" tabindex="-1">Tu privacidad</h2>
  <p>Usamos cookies técnicas, necesarias para que la web funcione. Con tu permiso usaríamos también cookies de analítica para mejorarla. Puedes cambiar tu elección cuando quieras. <a href="{L("/cookies/")}">Política de cookies</a></p>
  <div class="cookies__opciones" id="cookies-opciones" hidden>
    <label><span><b>Necesarias</b>Imprescindibles para la web. Siempre activas.</span><input type="checkbox" checked disabled></label>
    <label for="ck-analitica"><span><b>Analítica</b>Nos ayuda a saber qué páginas se visitan.</span><input type="checkbox" id="ck-analitica"></label>
    <label for="ck-marketing"><span><b>Marketing</b>Para medir campañas en redes sociales.</span><input type="checkbox" id="ck-marketing"></label>
  </div>
  <div class="botonera">
    <button class="boton boton--primario" type="button" id="cookies-rechazar">Rechazar</button>
    <button class="boton boton--primario" type="button" id="cookies-aceptar">Aceptar</button>
  </div>
  <div class="botonera" style="margin-top:10px">
    <button class="boton boton--secundario" type="button" id="cookies-configurar">Configurar</button>
    <button class="boton boton--secundario" type="button" id="cookies-guardar" hidden>Guardar mi elección</button>
  </div>
</section>'''

# ---------------------------------------------------------------- datos estructurados
NEGOCIO = {
    "@context": "https://schema.org", "@type": ["HealthAndBeautyBusiness", "MedicalClinic"], "@id": DOMINIO + "/#centro",
    "name": "Rosa Ondoño", "slogan": "Cuídate · Conecta · Siente", "url": DOMINIO + "/",
    "logo": DOMINIO + "/assets/img/logo-horizontal.svg", "image": DOMINIO + "/assets/img/02-recepcion-ventana-patio.jpg",
    "telephone": "+34965120300", "email": "info@rosaondono.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Maisonnave 38, Entlo. Izq.", "postalCode": "03003", "addressLocality": "Alicante", "addressRegion": "Alicante", "addressCountry": "ES"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "19:00"}],
    "hasMap": MAPS, "sameAs": [INSTAGRAM, FACEBOOK], "areaServed": "Alicante", "priceRange": "€€",
    "founder": {"@type": "Person", "name": "Rosa Ondoño"},
}
def ld(*objs): return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in objs)
def ld_migas(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMINIO + (r or "")} for i, (n, r) in enumerate(items) if r is not None] }

# ---------------------------------------------------------------- páginas
PAGINAS = []  # (ruta, titulo, descripcion, cuerpo, menu, jsonld, imagen_og)
def pagina(ruta, titulo, descripcion, cuerpo, menu="", jsonld="", og="02-recepcion-ventana-patio", indexar=True):
    PAGINAS.append(dict(ruta=ruta, titulo=titulo, desc=descripcion, cuerpo=cuerpo, menu=menu, ld=jsonld, og=og, indexar=indexar))

def bloque_valoracion():
    return f'''<section class="seccion seccion--lila"><div class="envoltura dos">
  <div><span class="antetitulo">¿No sabes por dónde empezar?</span><h2>Empieza por una valoración integral</h2>
  <p class="texto">Hablamos de lo que te gustaría mejorar, valoramos piel, cuerpo y hábitos, y te llevas un plan personalizado por escrito. Sin compromiso.</p>
  <div class="botonera"><a class="boton boton--primario" href="{ruta_reserva("valoracion-integral")}">Reservar valoración</a><a class="enlace-flecha" href="{L("/valoracion-integral/")}">Cómo es la valoración</a></div></div>
  <div class="dos__foto" style="aspect-ratio:16/11">{foto("01-recepcion")}</div>
</div></section>'''

def construir():
    global PAGINAS
    PAGINAS = []
    destacados = [t for t in TRAT if t["destacado"] and t["slug"] != "valoracion-integral"][:6]
    # ---------- Inicio
    rosa = I["p"]["rosa-ondono"]
    escenas = [
        ("Cuídate", "u-retrato-natural", True, "Tu bienestar empieza por ti.",
         "Estética y medicina estética con criterio, en el centro de Alicante.", ("Ver tratamientos", L("/", "universo"))),
        ("Conecta", "u-masaje-espalda", False, "Manos que saben dónde está la tensión.",
         "Masajes, drenaje y terapias con más de 30 años de oficio.", ("Ver terapias", L("/terapias/"))),
        ("Siente", "u-piedras-flores", False, "Una hora solo para ti.",
         "Rituales para parar, también para regalar.", ("Regalar un ritual", ruta_regalo("ritual-en-pareja"))),
    ]
    html_escenas = ""
    for n, (verbo, img, es_h1, titulo, texto, cta) in enumerate(escenas):
        palabras = titulo.split(" ")
        mitad = (len(palabras) + 1) // 2
        lineas = "".join(f'<span class="linea"><span>{e(" ".join(p))}</span></span>' for p in (palabras[:mitad], palabras[mitad:]))
        cabeza = (f'<h1 class="escena__titulo"><span class="oculto-visual">Centro de estética y bienestar en Alicante: </span>{lineas}</h1>'
                  if es_h1 else f'<p class="escena__titulo" aria-hidden="false">{lineas}</p>')
        html_escenas += f'''<div class="escena{" es-activa" if n == 0 else ""}" role="group" aria-roledescription="diapositiva" aria-label="{n + 1} de {len(escenas)}: {verbo}"{"" if n == 0 else ' aria-hidden="true"'}>
    <div class="escena__foto">{foto(img, sizes="100vw", carga="eager" if n == 0 else "lazy", alt="")}</div>
    <div class="envoltura escena__texto">
      <span class="escena__verbo">{verbo}</span>
      {cabeza}
      <p class="escena__entrada">{e(texto)}</p>
      <div class="botonera escena__botones"><a class="boton boton--claro" href="{cta[1]}"{"" if n == 0 else ' tabindex="-1"'}>{cta[0]}</a><a class="boton boton--borde-claro" href="{ruta_reserva()}"{"" if n == 0 else ' tabindex="-1"'}>Reservar cita</a></div>
    </div>
  </div>'''
    mandos = "".join(f'<button type="button" class="escenas__mando"{" aria-current=" + chr(34) + "true" + chr(34) if n == 0 else ""} aria-label="Ver {v}"><span>{v}</span><i></i></button>' for n, (v, *_r) in enumerate(escenas))

    abanico = "".join(f'''<a class="abanico__panel" href="{L("/" + a["slug"] + "/")}">
  {foto(FOTO_AREA[a["slug"]], sizes="(max-width: 800px) 80vw, 50vw", alt="")}
  <span class="abanico__num">0{i + 1}</span>
  <span class="abanico__pie"><span class="abanico__nombre">{e(a["nombre"])}</span><span class="abanico__lema">{e(a["titular"])}</span><span class="abanico__ir">Descubrir</span></span>
</a>''' for i, a in enumerate(AREAS))

    pasos = [("Cuídate", "Piel y cuerpo, con diagnóstico. Y medicina estética solo cuando de verdad hace falta.", "u-facial-mascarilla"),
             ("Conecta", "Manos expertas y terapias para soltar tensión y volver a escucharte.", "u-terapia-agujas"),
             ("Siente", "Rituales para parar, a solas o en compañía. También para regalar.", "08-patio-jardin-cenador")]
    lista_pasos = "".join(f'<li class="ritual__paso{" es-activo" if i == 0 else ""}"><span class="ritual__n">0{i + 1}</span><h3>{v}</h3><p>{t}</p></li>' for i, (v, t, _f) in enumerate(pasos))
    fotos_pasos = "".join(f'<figure class="ritual__foto">{foto(f, sizes="(max-width: 900px) 90vw, 40vw", alt="")}</figure>' for (_v, _t, f) in pasos)

    carta = ""
    for i, t in enumerate(destacados):
        stem = foto_principal(t)
        cat = I["c"][t["categoria_slug"]]["nombre"]
        dur = f'{t["duracion_min"]} min' if t.get("duracion_min") else ""
        carta += f'''<li><a class="carta__fila" href="{L(ruta_trat(t))}" data-vista="{A(f"img/{stem}-800.webp")}">
  <span class="carta__num">{i + 1:02d}</span>
  <span class="carta__mini">{foto(stem, sizes="72px", alt="")}</span>
  <span class="carta__nombre">{e(t["nombre"])}<small>{e(t["resumen"][:96].rsplit(" ", 1)[0])}…</small></span>
  <span class="carta__dato">{e(cat)}{(" · " + dur) if dur else ""}</span>
  <span class="carta__precio">{e(precio(t))}</span>
  <span class="carta__ir" aria-hidden="true">→</span>
</a></li>'''

    opciones_rapidas = "".join(f'<option value="{t["slug"]}" data-duracion="{t.get("duracion_min") or 60}">{e(t["nombre"])}</option>'
                               for t in sorted([t for t in TRAT if t["reservable"]], key=lambda t: (t["slug"] != "valoracion-integral", t["nombre"])))
    temas = ["el trato cercano", "la calma nada más entrar", "que te expliquen cada paso", "el patio", "salir sintiéndote otra", "sin prisas"]
    marquesina = "".join(f"<span>{t}</span>" for t in temas * 2)
    cuerpo = f'''
<section class="escenas" aria-roledescription="carrusel" aria-label="Presentación de Rosa Ondoño">
  {html_escenas}
  <img class="escenas__iso" src="{A("img/isotipo-blanco.svg")}" alt="" aria-hidden="true" width="171" height="238">
  <div class="envoltura escenas__pie">
    <div class="escenas__mandos">{mandos}<button type="button" class="escenas__pausa" aria-label="Pausar la presentación" aria-pressed="false"><span aria-hidden="true"></span></button></div>
    <a class="escenas__tarjeta" href="{L("/valoracion-integral/")}">
      <span class="escenas__tarjeta-et">¿Por dónde empiezo?</span>
      <strong>Valoración integral</strong>
      <span>Hablamos de lo que quieres mejorar y te llevas un plan por escrito.</span>
      <span class="enlace-flecha">Cómo es</span>
    </a>
  </div>
</section>

<div class="confianza" aria-label="Por qué elegirnos"><div class="envoltura confianza__fila">
  <span><b>+30 años</b> de oficio</span><span><b>4,9 ★</b> en Google</span><span><b>Supervisión</b> médica</span><span><b>{len(TRAT)}</b> tratamientos</span>
</div></div>

<section class="seccion universo-v3" id="universo"><div class="envoltura">
  <div class="cabeza-v3" data-revela>
    <span class="antetitulo"><b>01</b>Nuestro universo</span>
    <h2>Cuatro maneras de <em>cuidarte</em></h2>
    <p>Estética, medicina estética, terapias y bienestar bajo un mismo techo. No tienes que elegir entre verte bien y sentirte bien.</p>
  </div>
  <div class="abanico" data-revela>{abanico}</div>
</div></section>

<section class="ritual" id="metodo" aria-labelledby="ritual-titulo"><div class="ritual__pista"><div class="ritual__fijo"><div class="envoltura ritual__rejilla">
  <div class="ritual__texto">
    <span class="antetitulo">Nuestro método</span>
    <h2 id="ritual-titulo">Tres verbos que ordenan todo lo que hacemos</h2>
    <ol class="ritual__pasos">{lista_pasos}</ol>
    <div class="botonera"><a class="boton boton--claro" href="{ruta_reserva("valoracion-integral")}">Empieza con una valoración</a></div>
  </div>
  <div class="ritual__fotos">{iso("ritual__iso", "blanco")}<div class="ritual__marco">{fotos_pasos}</div></div>
  <div class="ritual__progreso" aria-hidden="true"><i></i></div>
</div></div></div></section>

<section class="seccion seccion--blanca carta-v3"><div class="envoltura">
  <div class="cabeza-v3 cabeza-v3--fila" data-revela>
    <div><span class="antetitulo"><b>02</b>Experiencias y tratamientos</span><h2>Los más <em>pedidos</em></h2></div>
    <p>Lo que más nos piden quienes ya nos conocen. Cada uno tiene su ficha con qué incluye, para quién es y cuánto dura.</p>
  </div>
  <ol class="carta" data-revela>{carta}</ol>
  <div class="vista-carta" aria-hidden="true"><img alt=""></div>
  <div class="botonera carta__mas"><a class="boton boton--primario" href="{ruta_reserva()}">Reservar cita</a><a class="enlace-flecha" href="{L("/estetica/")}">Ver todos los tratamientos</a></div>
</div></section>

<section class="seccion seccion--arena historia"><div class="envoltura historia__rejilla">
  <figure class="historia__foto" data-paralaje>{foto("02-recepcion-ventana-patio", sizes="(max-width: 900px) 100vw, 45vw")}</figure>
  <div class="historia__texto" data-revela>
    <span class="antetitulo"><b>03</b>Conócenos</span>
    <blockquote class="historia__cita">«Te recomendamos solo lo que tiene sentido para ti.»<cite>Rosa Ondoño</cite></blockquote>
    <p class="texto">Rosa empezó en el Hotel Sidi San Juan y se formó en Llongueras, en naturopatía y en terapias manuales. Durante años, médicos de Alicante, Madrid y Barcelona le han enviado a sus pacientes para el drenaje después de una cirugía. Hoy todo el centro trabaja así: escuchando primero.</p>
    <dl class="cifras">
      <div><dt><span data-cuenta="30">30</span>+</dt><dd>años de oficio</dd></div>
      <div><dt><span data-cuenta="4.9" data-decimales="1">4,9</span></dt><dd>en Google</dd></div>
      <div><dt><span data-cuenta="{len(TRAT)}">{len(TRAT)}</span></dt><dd>tratamientos</dd></div>
    </dl>
    <a class="enlace-flecha" href="{L("/conocenos/")}">Conoce a Rosa y al equipo</a>
  </div>
</div></section>

<section class="seccion experiencia"><div class="envoltura">
  <div class="cabeza-v3" data-revela>
    <span class="antetitulo"><b>04</b>Tu experiencia</span>
    <h2>Un patio en <em>pleno centro</em></h2>
    <p>Un entresuelo luminoso con un patio ajardinado dentro. La calma empieza en la puerta.</p>
  </div>
  <div class="mosaico" data-revela>
    <figure class="mosaico__a">{foto("08-patio-jardin-cenador", sizes="(max-width: 760px) 100vw, 50vw")}<figcaption>El patio</figcaption></figure>
    <figure class="mosaico__b">{foto("01-recepcion", sizes="(max-width: 760px) 50vw, 25vw")}<figcaption>Recepción</figcaption></figure>
    <figure class="mosaico__c">{foto("03-pasillo-cabinas", sizes="(max-width: 760px) 50vw, 25vw")}<figcaption>El pasillo</figcaption></figure>
    <figure class="mosaico__d">{foto("06-cabina-hornacina-lavabo", sizes="(max-width: 760px) 50vw, 25vw")}<figcaption>Una de las cabinas</figcaption></figure>
    <figure class="mosaico__e">{foto("10-patio-plantas", sizes="(max-width: 760px) 50vw, 25vw")}<figcaption>Plantas del patio</figcaption></figure>
  </div>
</div>
<div class="marquesina" role="group" aria-label="Lo que más repiten en las opiniones de Google: {", ".join(temas)}"><div class="marquesina__pista" aria-hidden="true">{marquesina}</div><button type="button" class="marquesina__parar" aria-pressed="false">Detener el movimiento</button></div>
<div class="envoltura nota-google"><p><b>4,9 ★</b> de media en las opiniones de Google</p><a class="enlace-flecha" href="{MAPS}" rel="noopener">Leer las opiniones</a></div>
</section>

<section class="reserva-v3" id="reserva"><div class="envoltura reserva-v3__rejilla">
  <div class="reserva-v3__form" data-revela>
    <span class="antetitulo"><b>05</b>Reserva tu cita</span>
    <h2>Elige día y hora</h2>
    <p>Te escribimos para confirmarla. Lunes a viernes, de 9:00 a 19:00.</p>
    <form class="reserva-rapida" action="{ruta_reserva()}" method="get" data-reserva-rapida>
      <div data-campo><label for="rr-servicio">Tratamiento</label>
        <select class="campo" id="rr-servicio" name="servicio" data-selector-servicio>{opciones_rapidas}</select></div>
      <div data-campo><label for="rr-fecha">Día</label><input class="campo" type="date" id="rr-fecha" name="fecha" data-min-dias="1" data-max-dias="120" data-selector-fecha></div>
      <div class="huecos" data-huecos aria-live="polite"><p class="huecos__vacio">Elige un día para ver las horas libres.</p></div>
      <input type="hidden" name="hora" data-hora>
      <button class="boton boton--claro" type="submit">Continuar con mis datos</button>
    </form>
    <p class="reserva-v3__otras">¿Prefieres hablar? <a href="{WA}" rel="noopener">WhatsApp 691 315 622</a> · <a href="tel:+34965120300">965 120 300</a></p>
  </div>
  <div class="reserva-v3__regalo" data-revela>
    <div class="inclina">{tarjeta_regalo("Alguien especial", "Un ritual en pareja", "")}</div>
    <h3>¿Es para regalar?</h3>
    <p>Un ritual, un masaje o un importe para que elija. Te la mandamos por email, lista para imprimir o reenviar.</p>
    <a class="boton boton--borde-claro" href="{ruta_regalo()}">Preparar tarjeta regalo</a>
  </div>
</div></section>'''

    pagina("/", "Centro de estética y bienestar en Alicante · Rosa Ondoño",
           "Estética, medicina estética, terapias y rituales de bienestar en Av. Maisonnave 38, Alicante. Más de 30 años de oficio y supervisión médica. Reserva online.",
           cuerpo, "", ld(NEGOCIO, {"@context": "https://schema.org", "@type": "WebSite", "name": "Rosa Ondoño", "url": DOMINIO + "/", "inLanguage": "es-ES"}), "u-facial-masaje")

    # ---------- Áreas
    for a in AREAS:
        cats = [c for c in CATS if c.get("area_slug") == a["slug"]]
        bloques, indice = "", ""
        for c in cats:
            lista = [t for t in TRAT if t["categoria_slug"] == c["slug"]]
            if a["slug"] == "medicina-estetica":
                lista.sort(key=lambda t: t["slug"] != "consulta-medica")
            if not lista: continue
            indice += f'<a href="{L("/" + a["slug"] + "/", "cat-" + c["slug"])}">{e(c["nombre"])}</a>'
            bloques += f'''<section class="bloque-categoria" id="cat-{c["slug"]}" aria-labelledby="t-cat-{c["slug"]}">
  <div class="bloque-categoria__cabeza"><h2 id="t-cat-{c["slug"]}">{e(c["nombre"])}</h2><span>{len(lista)} tratamientos</span></div>
  <div class="rejilla">{"".join(tarjeta(t) for t in lista)}</div>
</section>'''
        extra = ""
        if a["slug"] == "medicina-estetica":
            dr = I["p"]["dr-roberth-bravo-pardo"]
            extra = f'''<div class="aviso-medico"><div><strong>Primero, la consulta médica.</strong> Ningún tratamiento médico se reserva sin una valoración previa del {e(dr["nombre"])} <span class="pendiente" style="color:#8A3A2A">(nº de colegiado pendiente)</span>. Los resultados varían según cada persona.</div></div>'''
        if len(cats) > 1:
            extra += f'<nav class="indice-categorias" aria-label="Ir a una categoría">{indice}</nav>'
        cta2 = f'<a class="boton boton--secundario" href="{ruta_regalo()}">Regalar</a>' if a["slug"] in ("bienestar", "terapias") else ""
        cta1 = f'<a class="boton boton--primario" href="{ruta_reserva("consulta-medica")}">Pedir consulta médica</a>' if a["slug"] == "medicina-estetica" else f'<a class="boton boton--primario" href="{ruta_reserva()}">Reservar cita</a>'
        mig = [("Inicio", "/"), (a["nombre"], None)]
        cuerpo = f'''<section class="cabecera-pagina"><div class="envoltura cabecera-pagina__rejilla">
  <div>{migas(mig)}
  <h1><span class="h1-pre">{e(a["nombre"])} en Alicante</span>{e(a["titular"])}</h1><p class="entrada">{e(a["descripcion"])}</p>
  <div class="botonera" style="margin-top:24px">{cta1}{cta2}</div>{extra}</div>
  <div class="cabecera-pagina__foto cabecera-pagina__foto--arco">{foto(FOTO_AREA[a["slug"]], carga="eager")}</div>
</div></section>
<section class="seccion seccion--blanca" style="padding-top:clamp(48px,6vw,80px)"><div class="envoltura">{bloques}</div></section>
{bloque_valoracion()}'''
        desc = {"estetica": "Tratamientos faciales y corporales, depilación láser, micropigmentación y belleza en el centro de Alicante. Te recomendamos solo lo que necesitas.",
                "medicina-estetica": "Medicina estética en Alicante con valoración médica previa: labios, hilos tensores, bioestimulación de colágeno y más, buscando resultados naturales.",
                "terapias": "Masajes, drenaje linfático postoperatorio, acupuntura y terapias manuales en Alicante, con más de 30 años de oficio.",
                "bienestar": "Rituales individuales y en pareja, circuito spa y masaje relajante en el centro de Alicante. También como tarjeta regalo."}[a["slug"]]
        pagina(f'/{a["slug"]}/', f'{a["nombre"]} en Alicante · Rosa Ondoño', desc, cuerpo, a["slug"], ld(ld_migas([("Inicio", "/"), (a["nombre"], f'/{a["slug"]}/')])), FOTO_AREA[a["slug"]])

    # ---------- Fichas
    for t in TRAT:
        if t["slug"] == "valoracion-integral": continue
        cat = I["c"][t["categoria_slug"]]; ar = I["a"].get(cat.get("area_slug")) if cat.get("area_slug") else None
        prof = I["p"].get(t.get("profesional_slug"))
        medico = t["tipo"] == "medico"
        stem = foto_principal(t)
        if medico and t["slug"] != "consulta-medica":
            botones = f'<a class="boton boton--primario" href="{ruta_reserva("consulta-medica")}">Pedir consulta médica</a>'
        elif t["reservable"]:
            botones = f'<a class="boton boton--primario" href="{ruta_reserva(t["slug"])}">Reservar</a>'
            if not medico and t["slug"] != "valoracion-integral":
                botones += f'<a class="boton boton--secundario" href="{ruta_regalo(t["slug"])}">Regalar</a>'
        else:
            botones = f'<a class="boton boton--primario" href="{WA}" rel="noopener">Consultar por WhatsApp</a>'
        datos = ""
        if t.get("duracion_min"): datos += f'<div><dt>Duración</dt><dd>{t["duracion_min"]} min</dd></div>'
        datos += f'<div><dt>Sesiones</dt><dd>{e(t["sesiones"])}</dd></div><div><dt>Precio</dt><dd>{e(precio(t))}</dd></div>'
        datos += f'<div><dt>Lo realiza</dt><dd>{e(prof["nombre"]) if prof else "Se confirma al reservar"}</dd></div>'
        aviso = ""
        if medico:
            aviso = f'<div class="aviso-medico"><div>Tratamiento médico realizado por {e(prof["nombre"] if prof else "el médico del centro")}. Requiere valoración médica previa. Los resultados varían según cada persona. <span class="pendiente" style="color:#8A3A2A">Nº de colegiado y nº de registro sanitario: pendientes.</span></div></div>'
        if t["slug"] in ("flores-de-bach", "terapia-somatoemocional", "acupuntura"):
            aviso = '<div class="aviso-medico"><div>Terapia complementaria de bienestar. No sustituye el diagnóstico ni el tratamiento médico o psicológico.</div></div>'
        faqs = FAQS.get(t["slug"], [])
        faq_html = "".join(f'<details class="faq"><summary>{e(f["pregunta"])}</summary><p>{e(f["respuesta"])}</p></details>' for f in faqs)
        rel = [x for x in TRAT if x["slug"] != t["slug"] and x["categoria_slug"] == t["categoria_slug"]][:3]
        base_area = ("Medicina estética", "/medicina-estetica/") if medico else ((ar["nombre"], f'/{ar["slug"]}/') if ar else ("Valoración integral", None))
        mig = [("Inicio", "/"), base_area, (t["nombre"], None)] if base_area[1] else [("Inicio", "/"), (t["nombre"], None)]
        cuerpo = f'''<section class="cabecera-pagina"><div class="envoltura cabecera-pagina__rejilla">
  <div>{migas(mig)}
    <span class="antetitulo">{e(cat["nombre"])}{" · tratamiento médico" if medico else ""}</span>
    <h1>{e(t["nombre"])} en Alicante</h1>
    <p class="entrada">{e(t["resumen"])}</p>
    <dl class="ficha-datos">{datos}</dl>
    <div class="botonera">{botones}</div>
    {aviso}
  </div>
  <div class="cabecera-pagina__foto">{foto(stem, carga="eager")}</div>
</div></section>
{f'<section class="seccion seccion--blanca"><div class="envoltura estrecho"><span class="antetitulo">Preguntas frecuentes</span><h2>Lo que más nos preguntan</h2>{faq_html}</div></section>' if faqs else ""}
{f'<section class="seccion"><div class="envoltura"><div class="cabeza-seccion"><h2>También te puede interesar</h2></div><div class="rejilla">{"".join(tarjeta(x) for x in rel)}</div></div></section>' if rel else ""}
{bloque_valoracion() if t["slug"] != "valoracion-integral" else ""}'''
        servicio = {"@context": "https://schema.org", "@type": "MedicalProcedure" if medico else "Service", "name": t["nombre"], "description": t["resumen"],
                    "url": DOMINIO + ruta_trat(t), "provider": {"@id": DOMINIO + "/#centro"}, "areaServed": "Alicante"}
        if not medico: servicio["serviceType"] = cat["nombre"]
        objs = [servicio, ld_migas([(n, r if r else (ruta_trat(t) if n == t["nombre"] else None)) for n, r in mig])]
        if faqs: objs.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["pregunta"], "acceptedAnswer": {"@type": "Answer", "text": f["respuesta"]}} for f in faqs]})
        desc = (t["resumen"][:150].rsplit(" ", 1)[0] + "…") if len(t["resumen"]) > 155 else t["resumen"]
        for extra in (" Reserva online en Rosa Ondoño, Av. Maisonnave 38, Alicante.", " Rosa Ondoño, Av. Maisonnave 38, Alicante.", " En Alicante centro."):
            if len(desc) + len(extra) <= 158: desc += extra; break
        titulo = f'{t["nombre"]} en Alicante · Rosa Ondoño'
        pagina(ruta_trat(t), titulo, desc, cuerpo, "medicina-estetica" if medico else (ar["slug"] if ar else ""), ld(*objs), stem)

    # ---------- Valoración integral (landing propia, además de su ficha)
    vi = I["t"]["valoracion-integral"]
    cuerpo = f'''<section class="cabecera-pagina"><div class="envoltura cabecera-pagina__rejilla">
  <div>{migas([("Inicio", "/"), ("Valoración integral", None)])}<span class="antetitulo">Empieza aquí</span>
  <h1>Valoración integral en Alicante</h1>
  <p class="entrada">{e(vi["resumen"])}</p>
  <div class="botonera" style="margin-top:24px"><a class="boton boton--primario" href="{ruta_reserva("valoracion-integral")}">Reservar mi valoración</a></div></div>
  <div class="cabecera-pagina__foto cabecera-pagina__foto--arco">{foto("01-recepcion", carga="eager")}</div>
</div></section>
<section class="seccion seccion--morada metodo"><div class="envoltura">{iso("metodo__super", "blanco")}<div class="metodo__contenido">
  <span class="antetitulo">Cómo es</span><h2>Una conversación, un análisis y un plan por escrito</h2>
  <ul class="verbos"><li><h3>Escuchamos</h3><p>Qué te gustaría mejorar, qué has probado y qué esperas.</p></li>
  <li><h3>Valoramos</h3><p>Piel, cuerpo y hábitos, con tiempo y sin prisas.</p></li>
  <li><h3>Proponemos</h3><p>Un plan por Cuídate · Conecta · Siente, con lo que necesitas y lo que no.</p></li></ul>
  <p style="color:var(--lila)">Condiciones de la valoración (gratuita o descontable del primer tratamiento): pendientes de confirmar por el centro.</p>
</div></div></section>
<section class="seccion seccion--blanca"><div class="envoltura estrecho"><h2>Preguntas frecuentes</h2>{"".join(f'<details class="faq"><summary>{e(f["pregunta"])}</summary><p>{e(f["respuesta"])}</p></details>' for f in FAQS.get("valoracion-integral", []))}</div></section>'''
    pagina("/valoracion-integral/", "Valoración integral en Alicante · Rosa Ondoño",
           "Empieza por una valoración integral: escuchamos lo que quieres mejorar, valoramos piel, cuerpo y hábitos y te llevas un plan personalizado. Av. Maisonnave 38.",
           cuerpo, "", ld(ld_migas([("Inicio", "/"), ("Valoración integral", "/valoracion-integral/")])), "01-recepcion")

    # ---------- Conócenos
    dr = I["p"]["dr-roberth-bravo-pardo"]
    cuerpo = f'''<section class="cabecera-pagina"><div class="envoltura cabecera-pagina__rejilla">
  <div>{migas([("Inicio", "/"), ("Conócenos", None)])}<span class="antetitulo">Conócenos</span>
  <h1>Rosa Ondoño, más de 30 años cuidando a personas en Alicante</h1>
  <p class="entrada">{e(rosa["bio"])}</p>
  <p class="lema" style="margin-top:20px">«Te decimos lo que necesitas, y también lo que no.»</p></div>
  <div class="cabecera-pagina__foto cabecera-pagina__foto--arco">{foto("02-recepcion-ventana-patio", carga="eager")}</div>
</div></section>
<section class="seccion seccion--blanca"><div class="envoltura">
  <div class="cabeza-seccion"><div><span class="antetitulo">Quién te cuida</span><h2>Personas con nombre y formación</h2></div><p>Retratos pendientes de la sesión de fotos del centro.</p></div>
  <div class="dos" style="align-items:start">
    <article><h3 style="font-size:1.7rem;font-weight:300">{e(rosa["nombre"])}</h3><p class="antetitulo">{e(rosa["cargo"])}</p><p>{e(rosa["bio"])}</p></article>
    <article><h3 style="font-size:1.7rem;font-weight:300">{e(dr["nombre"])}</h3><p class="antetitulo">{e(dr["cargo"])}</p><p>{e(dr["bio"])}</p><p><span class="pendiente" style="color:#8A3A2A">Nº de colegiado: pendiente</span></p></article>
  </div>
</div></section>
<section class="seccion seccion--morada metodo"><div class="envoltura">{iso("metodo__super", "blanco")}<div class="metodo__contenido">
  <span class="antetitulo">Nuestra filosofía</span><h2>Bienestar integral con criterio</h2>
  <ul class="verbos"><li><h3>Cuídate</h3><p>Diagnóstico, estética y medicina estética cuando hace falta.</p></li><li><h3>Conecta</h3><p>Terapias manuales y complementarias.</p></li><li><h3>Siente</h3><p>Rituales y experiencias para parar.</p></li></ul>
</div></div></section>
<section class="seccion"><div class="envoltura">
  <div class="cabeza-seccion"><div><span class="antetitulo">El centro</span><h2>Un entresuelo luminoso con patio ajardinado</h2></div><p><a href="{MAPS}" rel="noopener">Av. Maisonnave 38, Entlo. Izq. · Cómo llegar</a></p></div>
  <div class="galeria">
    <figure>{foto("08-patio-jardin-cenador")}<figcaption>Patio</figcaption></figure>
    <figure>{foto("01-recepcion")}<figcaption>Recepción</figcaption></figure>
    <figure>{foto("03-pasillo-cabinas")}<figcaption>Pasillo</figcaption></figure>
    <figure>{foto("06-cabina-hornacina-lavabo")}<figcaption>Una de nuestras cabinas</figcaption></figure>
    <figure>{foto("10-patio-plantas")}<figcaption>Patio</figcaption></figure>
  </div>
</div></section>'''
    personas = [{"@context": "https://schema.org", "@type": "Person", "name": rosa["nombre"], "jobTitle": rosa["cargo"], "worksFor": {"@id": DOMINIO + "/#centro"}},
                {"@context": "https://schema.org", "@type": "Person", "name": dr["nombre"], "jobTitle": dr["cargo"], "worksFor": {"@id": DOMINIO + "/#centro"}}]
    pagina("/conocenos/", "Conócenos: Rosa Ondoño y el equipo · Alicante", "Rosa Ondoño, esteticista y terapeuta con más de 30 años de oficio, y el Dr. Roberth Bravo Pardo, médico estético. Bienestar integral con criterio en Alicante.",
           cuerpo, "conocenos", ld(*personas, ld_migas([("Inicio", "/"), ("Conócenos", "/conocenos/")])), "02-recepcion-ventana-patio")

    # ---------- Reservar
    opciones = ""
    for c in CATS:
        ops = sorted([t for t in TRAT if t["reservable"] and t["categoria_slug"] == c["slug"]], key=lambda t: t["nombre"])
        if ops: opciones += f'<optgroup label="{e(c["nombre"])}">' + "".join(f'<option value="{t["slug"]}" data-duracion="{t.get("duracion_min") or 60}">{e(t["nombre"])}</option>' for t in ops) + "</optgroup>"
    cuerpo = f'''<section class="cabecera-pagina" style="padding-bottom:clamp(64px,8vw,112px)"><div class="envoltura">
  {migas([("Inicio", "/"), ("Reservar", None)])}
  <div class="columnas-form">
    <div>
      <span class="antetitulo">Reserva tu cita</span><h1>Reservar cita</h1>
      <p class="entrada" style="margin-bottom:32px">Elige tratamiento, día y hora. Te escribimos para confirmarla.</p>
      <form class="formulario" id="form-reserva" name="reserva" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
        <input type="hidden" name="form-name" value="reserva"><input type="hidden" name="subject" value="Nueva solicitud de cita · web Rosa Ondoño"><input type="hidden" name="servicio_nombre" value="">
        <p class="oculto-visual" aria-hidden="true"><label>No rellenar: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <fieldset class="bloque-form"><legend><span>1</span>Tratamiento</legend>
          <div data-campo><label for="r-servicio">¿Qué quieres reservar?</label>
          <select class="campo" id="r-servicio" name="servicio" data-preseleccion data-selector-servicio><option value="">Elige un tratamiento</option>{opciones}</select>
          <p class="ayuda">Los tratamientos médicos empiezan con la <strong>consulta de medicina estética</strong>. Si dudas, elige <strong>valoración integral</strong>.</p></div>
        </fieldset>
        <fieldset class="bloque-form"><legend><span>2</span>Día y hora</legend>
          <div data-campo><label for="r-fecha">Día</label><input class="campo campo--fecha" type="date" id="r-fecha" name="fecha" data-min-dias="1" data-max-dias="120" data-selector-fecha></div>
          <div data-campo data-campo-hora><span class="etiqueta-campo" id="r-hora-et">Hora</span>
            <div class="huecos" data-huecos role="group" aria-labelledby="r-hora-et" aria-live="polite"><p class="huecos__vacio">Elige tratamiento y día para ver las horas libres.</p></div>
            <input type="hidden" name="hora" data-hora><input type="hidden" name="franja"><input type="hidden" name="duracion" value="60"></div>
          <p class="ayuda">De lunes a viernes, de 9:00 a 19:00. Las horas tachadas ya están ocupadas en nuestra agenda.</p>
        </fieldset>
        <fieldset class="bloque-form"><legend><span>3</span>Tus datos</legend>
          <div class="campo-grupo">
            <div data-campo class="ancho-completo"><label for="r-nombre">Nombre y apellidos</label><input class="campo" id="r-nombre" name="nombre" autocomplete="name"></div>
            <p class="ayuda ancho-completo" id="r-contacto-ayuda" style="margin:0">Déjanos un <strong>teléfono o un email</strong>: con uno basta.</p>
            <div data-campo><label for="r-telefono">Teléfono</label><input class="campo" id="r-telefono" name="telefono" type="tel" autocomplete="tel" inputmode="tel" aria-describedby="r-contacto-ayuda"></div>
            <div data-campo><label for="r-email">Email</label><input class="campo" id="r-email" name="email" type="email" autocomplete="email" inputmode="email" aria-describedby="r-contacto-ayuda"></div>
            <div data-campo class="ancho-completo"><label class="casilla"><input type="checkbox" name="privacidad"><span>He leído la <a href="{L("/privacidad/")}">política de privacidad</a> y acepto que se usen mis datos para gestionar esta cita.</span></label></div>
          </div>
          <p class="ayuda">No te pedimos datos de salud en el formulario: los hablamos en persona.</p>
        </fieldset>
        <div class="envio"><button class="boton boton--primario boton--ancho" type="submit">Enviar solicitud</button><p class="ayuda">Al enviar, la petición entra en la agenda del centro y nos llega un aviso por WhatsApp. No tienes que hacer nada más.</p></div>
      </form>
      <div class="resultado" hidden></div>
    </div>
    <aside class="lado-form">
      <div class="via via--destacada"><h2 style="font-size:1.5rem">¿Prefieres hablar con nosotras?</h2><p>WhatsApp 691 315 622 · Teléfono 965 120 300</p><a class="boton boton--claro" href="{WA}" rel="noopener" style="align-self:flex-start;margin-top:10px">Escribir por WhatsApp</a></div>
      <div class="via" style="margin-top:16px"><h2 style="font-size:1.5rem">¿Es para regalar?</h2><p>Prepara una tarjeta regalo con una experiencia o un importe.</p><a class="enlace-flecha" href="{ruta_regalo()}">Regalar</a></div>
    </aside>
  </div>
</div></section>'''
    pagina("/reservar/", "Reservar cita · Rosa Ondoño Alicante", "Reserva tu cita en Rosa Ondoño, Av. Maisonnave 38, Alicante: elige tratamiento, día y hora libre en la agenda y te la confirmamos.", cuerpo, "", "", "01-recepcion")

    # ---------- Regalar
    regalables = sorted([t for t in TRAT if t["reservable"] and t["tipo"] != "medico" and t["slug"] != "valoracion-integral"], key=lambda t: (t["categoria_slug"] != "rituales", t["nombre"]))
    ops = "".join(f'<option value="{t["slug"]}">{e(t["nombre"])}</option>' for t in regalables)
    importes = "".join(f'<option value="{v}">{v} €</option>' for v in (50, 75, 100, 150, 200))
    cuerpo = f'''<section class="cabecera-pagina" style="padding-bottom:clamp(64px,8vw,112px)"><div class="envoltura">
  {migas([("Inicio", "/"), ("Tarjeta regalo", None)])}
  <div class="columnas-form">
    <div>
      <span class="antetitulo">Tarjeta regalo</span><h1>Regala un momento para cuidarse</h1>
      <p class="entrada" style="margin-bottom:32px">Elige una experiencia o un importe, personaliza el mensaje y te la enviamos por email.</p>
      <form class="formulario" id="form-regalo" name="regalo" method="POST" data-netlify="true" netlify-honeypot="bot-field" novalidate>
        <input type="hidden" name="form-name" value="regalo"><input type="hidden" name="subject" value="Nueva tarjeta regalo · web Rosa Ondoño"><input type="hidden" name="regalo_nombre" value="">
        <p class="oculto-visual" aria-hidden="true"><label>No rellenar: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <fieldset class="bloque-form"><legend><span>1</span>¿Qué quieres regalar?</legend>
          <div data-campo class="opciones" style="margin-bottom:18px"><label class="opcion"><input type="radio" name="modalidad" value="experiencia" checked><span>Una experiencia</span></label><label class="opcion"><input type="radio" name="modalidad" value="importe"><span>Un importe</span></label></div>
          <div data-campo id="campo-experiencia"><label for="g-exp">Experiencia</label><select class="campo" id="g-exp" name="experiencia" data-preseleccion><option value="">Elige una experiencia</option>{ops}</select></div>
          <div data-campo id="campo-importe" hidden><label for="g-imp">Importe</label><select class="campo" id="g-imp" name="importe"><option value="">Elige un importe</option>{importes}</select></div>
          <p class="ayuda">Las tarjetas no incluyen tratamientos de medicina estética. Validez: pendiente de confirmar por el centro.</p>
        </fieldset>
        <fieldset class="bloque-form"><legend><span>2</span>Para quién</legend>
          <div class="campo-grupo">
            <div data-campo class="ancho-completo"><label for="g-para">Nombre de quien la recibe</label><input class="campo" id="g-para" name="para_nombre" maxlength="80"></div>
            <div data-campo class="ancho-completo"><label for="g-msg">Mensaje <span style="color:var(--texto-suave)">(opcional)</span></label><textarea class="campo" id="g-msg" name="mensaje" maxlength="280"></textarea></div>
          </div>
        </fieldset>
        <fieldset class="bloque-form"><legend><span>3</span>Tus datos</legend>
          <div class="campo-grupo">
            <div data-campo class="ancho-completo"><label for="g-nombre">Nombre y apellidos</label><input class="campo" id="g-nombre" name="nombre" autocomplete="name"></div>
            <p class="ayuda ancho-completo" id="g-contacto-ayuda" style="margin:0">Déjanos un <strong>teléfono o un email</strong>: con uno basta.</p>
            <div data-campo><label for="g-telefono">Teléfono</label><input class="campo" id="g-telefono" name="telefono" type="tel" autocomplete="tel" inputmode="tel" aria-describedby="g-contacto-ayuda"></div>
            <div data-campo><label for="g-email">Email</label><input class="campo" id="g-email" name="email" type="email" autocomplete="email" inputmode="email" aria-describedby="g-contacto-ayuda"></div>
            <div data-campo class="ancho-completo"><label class="casilla"><input type="checkbox" name="privacidad"><span>He leído la <a href="{L("/privacidad/")}">política de privacidad</a> y acepto que se usen mis datos para preparar la tarjeta.</span></label></div>
          </div>
          <p class="ayuda">El pago se gestiona cuando te contactamos, hasta que el sistema de reservas permita pagar online.</p>
        </fieldset>
        <div class="envio"><button class="boton boton--primario boton--ancho" type="submit">Enviar solicitud</button><p class="ayuda">Al enviar, nos llega un aviso por WhatsApp y por email. Te contactamos para el pago y te enviamos la tarjeta.</p></div>
      </form>
      <div class="resultado" hidden></div>
    </div>
    <aside class="lado-form" aria-label="Vista previa de la tarjeta">
      {tarjeta_regalo(None, None, None, viva=True)}
      <p class="ayuda" style="margin-top:14px">Así se verá la tarjeta que recibirá por email.</p>
    </aside>
  </div>
</div></section>'''
    pagina("/regalar/", "Tarjeta regalo de spa y bienestar en Alicante · Rosa Ondoño", "Regala un ritual en pareja, un masaje o un importe libre en Rosa Ondoño, Alicante. Tarjeta regalo personalizada por email.",
           cuerpo, "", ld(ld_migas([("Inicio", "/"), ("Tarjeta regalo", "/regalar/")])), "u-piedras-flores")

    # ---------- Legales y 404
    for ruta, titulo, puntos in [("/aviso-legal/", "Aviso legal", ["Titular de la web, NIF y domicilio", "Datos de contacto", "Nº de registro sanitario del centro", "Condiciones de uso y propiedad intelectual"]),
                                 ("/privacidad/", "Política de privacidad", ["Responsable del tratamiento", "Finalidades: gestionar citas y tarjetas regalo", "Base jurídica y plazos de conservación", "Encargados del tratamiento (Supabase, UE) y derechos RGPD"]),
                                 ("/cookies/", "Política de cookies", ["Cookies técnicas (necesarias)", "Cookies de analítica (solo con consentimiento)", "Cómo cambiar tu elección en cualquier momento", "Listado de cookies y proveedores"])]:
        cuerpo = f'''<section class="seccion"><div class="envoltura estrecho legal">{migas([("Inicio", "/"), (titulo, None)])}<h1>{titulo}</h1>
<p class="entrada">Texto pendiente de redactar y validar por el asesor legal del centro. Contendrá:</p><ul>{"".join(f"<li>{p}</li>" for p in puntos)}</ul>
{'<p><button class="boton boton--secundario" type="button" data-abrir-cookies>Configurar cookies</button></p>' if ruta == "/cookies/" else ""}</div></section>'''
        pagina(ruta, f"{titulo} · Rosa Ondoño", f"{titulo} de la web de Rosa Ondoño, centro de estética, terapias y medicina estética en Av. Maisonnave 38, Alicante.", cuerpo, "", "", indexar=False)
    pagina("/404", "Página no encontrada · Rosa Ondoño", "La página que buscas no existe.",
           f'<section class="seccion"><div class="envoltura estrecho"><span class="antetitulo">Error 404</span><h1>No encontramos esta página</h1><p class="entrada">Puede que haya cambiado de dirección con la nueva web.</p><div class="botonera"><a class="boton boton--primario" href="{L("/")}">Ir al inicio</a><a class="boton boton--secundario" href="{ruta_reserva()}">Reservar cita</a></div></div></section>', "", "", indexar=False)

def tarjeta_regalo(para, que, msg, viva=False):
    i = ' id="vr-para"' if viva else ""; j = ' id="vr-que"' if viva else ""; k = ' id="vr-mensaje"' if viva else ""
    return f'''<div class="tarjeta-regalo" role="img" aria-label="Tarjeta regalo de Rosa Ondoño">
  {iso("tarjeta-regalo__super", "blanco")}
  <img class="tarjeta-regalo__logo" src="{A("img/logo-horizontal-blanco.svg")}" alt="" width="150" height="50">
  <div class="tarjeta-regalo__para"><small>Tarjeta regalo para</small><strong{i}>{e(para or "Alguien especial")}</strong><em{j}>{e(que or "Una experiencia a su elección")}</em><em{k} style="font-size:.95rem">{e(msg or "")}</em></div>
</div>'''

# ---------------------------------------------------------------- plantilla de documento
def head(p, en_vista=False):
    url = DOMINIO + (p["ruta"] if p["ruta"] != "/404" else "/404")
    og = f'{DOMINIO}/assets/img/{p["og"]}.jpg'
    robots = "index, follow" if p["indexar"] and not en_vista else "noindex, follow"
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p["titulo"])}</title>
<meta name="description" content="{e(p["desc"])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="Rosa Ondoño">
<meta property="og:title" content="{e(p["titulo"])}"><meta property="og:description" content="{e(p["desc"])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#7D1F73">
<link rel="icon" href="{A("img/isotipo-color.svg")}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500&family=Jost:wght@300;400;500&display=swap">
<link rel="stylesheet" href="{A("css/sitio.css")}">
<script>document.documentElement.classList.add("js")</script>'''

def documento(p):
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
{head(p)}
{p["ld"]}
</head>
<body{' class="con-portada"' if p["ruta"] == "/" else ""}>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{cabecera(p["menu"])}
<main id="contenido">{p["cuerpo"]}</main>
{pie()}
{flotantes()}
{scripts(p["ruta"] == "/")}
</body>
</html>'''

def scripts(con_gsap):
    gsap = f'<script src="{A("js/vendor/gsap.min.js")}" defer></script><script src="{A("js/vendor/ScrollTrigger.min.js")}" defer></script>' if con_gsap else ""
    return f'{gsap}<script src="{A("js/config.js")}" defer></script><script src="{A("js/sitio.js")}" defer></script>'

def vista_previa():
    secciones = ""
    for p in PAGINAS:
        ident = "no-encontrada" if p["ruta"] == "/404" else pid(p["ruta"])
        secciones += f'<div data-pagina="{ident}" data-titulo="{e(p["titulo"])}" data-menu="{p["menu"]}"{"" if ident == "inicio" else " hidden"}>{p["cuerpo"]}</div>\n'
    inicio = PAGINAS[0]
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
{head(inicio, en_vista=True)}
</head>
<body data-modo="vista" class="con-portada">
<a class="saltar" href="#contenido">Saltar al contenido</a>
{cabecera("")}
<main id="contenido">
{secciones}</main>
{pie()}
{flotantes()}
{scripts(True)}
</body>
</html>'''

# ---------------------------------------------------------------- SEO: sitemap, robots, redirecciones
def seo_archivos():
    urls = "".join(f"<url><loc>{DOMINIO}{p['ruta']}</loc><lastmod>{HOY}</lastmod></url>" for p in PAGINAS if p["indexar"])
    (SALIDA / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (SALIDA / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /vista-previa.html\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    lineas = ["# Redirecciones 301 de la web actual (generado desde ../seo/redirecciones-301.csv)",
              "https://www.rosaondono.com/* https://rosaondono.com/:splat 301!", "http://rosaondono.com/* https://rosaondono.com/:splat 301!"]
    with open(RAIZ.parent / "seo" / "redirecciones-301.csv") as f:
        for fila in csv.DictReader(f):
            if fila["codigo"] == "301" and "*" not in fila["origen"] and fila["destino"]:
                lineas.append(f'{fila["origen"]} {fila["destino"]} 301')
            elif fila["codigo"] == "410":
                lineas.append(f'{fila["origen"]} /404 410')
    (SALIDA / "_redirects").write_text("\n".join(lineas) + "\n")

# ---------------------------------------------------------------- principal
def main():
    global MODO
    if SALIDA.exists(): shutil.rmtree(SALIDA)
    for sub in ("css", "js", "img"): (SALIDA / "assets" / sub).mkdir(parents=True)
    shutil.copy(RAIZ / "fuente" / "sitio.css", SALIDA / "assets" / "css" / "sitio.css")
    shutil.copy(RAIZ / "fuente" / "sitio.js", SALIDA / "assets" / "js" / "sitio.js")
    shutil.copy(RAIZ / "fuente" / "config.js", SALIDA / "assets" / "js" / "config.js")
    shutil.copytree(RAIZ / "fuente" / "vendor", SALIDA / "assets" / "js" / "vendor")
    for f in (RAIZ / "img").glob("*.svg"): shutil.copy(f, SALIDA / "assets" / "img" / f.name)
    shutil.copytree(RAIZ / "img" / "iconos", SALIDA / "assets" / "img" / "iconos")
    asignar_visuales()
    preparar_imagenes()
    MODO = "estatico"; construir()
    for p in PAGINAS:
        destino = SALIDA / ("404.html" if p["ruta"] == "/404" else p["ruta"].strip("/") + "/index.html" if p["ruta"] != "/" else "index.html")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(documento(p))
    seo_archivos()
    n = len(PAGINAS)
    MODO = "vista"; construir()
    # La vista previa no debe registrar formularios en Netlify (solo /reservar/ y /regalar/)
    (SALIDA / "vista-previa.html").write_text(vista_previa().replace(' data-netlify="true" netlify-honeypot="bot-field"', ''))
    print(f"{n} páginas generadas en {SALIDA} · datos: {D['origen']}")

if __name__ == "__main__":
    main()
