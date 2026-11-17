"""Manual de marca de Rosa Ondoño · v2 (A4 horizontal).

Uso:  python3 construir_manual.py   -> manual-de-marca.html
      node exportar_pdf.js          -> manual-de-marca.pdf

- El isotipo se usa SIEMPRE desde el vector original (identidad/logo/), sin redibujar.
- El logotipo completo se usa desde los archivos originales del cliente (PSD 2023).
- Los contrastes WCAG se calculan aquí, no se escriben a mano.
"""
import os, re, sys, math
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "identidad", "iconos"))
from generar import ICONOS, svg as svg_icono  # noqa: E402

LOGO_DIR = "../identidad/logo"
H_LOGO = f"{LOGO_DIR}/logo-horizontal.png"
V_LOGO = f"{LOGO_DIR}/logo-vertical.png"
V_SIN = f"{LOGO_DIR}/logo-vertical-sin-descriptor.png"
FOTO = "img/fotos"
with open(os.path.join(AQUI, "..", "identidad", "logo", "isotipo-negro.svg")) as f:
    ISO_D = re.search(r' d="([^"]+)"', f.read()).group(1)
ISO_VB = "0 0 171.2 237.53"

# ---------------- color ----------------
C = dict(morado="#7D1F73", marfil="#F7F2EB", arena="#E9DCCB", lila="#E8DAE6", arcilla="#B7897A",
         tinta="#2E1A2C", salvia="#A9B7A4", blanco="#FFFFFF")
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + .05) / (y + .05)
def coma(n, d=1): return f"{n:.{d}f}".replace(".", ",")
def rgb(h): h = h.lstrip('#'); return ", ".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
def nivel(r): return "AAA" if r >= 7 else "AA" if r >= 4.5 else "Solo grande" if r >= 3 else "No"

# ---------------- piezas ----------------
def iso(color="var(--morado)", style="", cls="iso"):
    return f'<svg class="{cls}" viewBox="{ISO_VB}" style="{style}" aria-hidden="true"><path fill="{color}" d="{ISO_D}"/></svg>'
def img(src, alt, style="", cls=""):
    return f'<img src="{src}" alt="{alt}" class="{cls}" style="{style}">'
def ico(k, tam=26, color="var(--morado)"):
    t, cuerpo = ICONOS[k]
    return svg_icono(cuerpo, t).replace('width="24" height="24"', f'width="{tam}" height="{tam}" style="color:{color}"')
def pend(t="PENDIENTE"): return f'<span class="pend">{t}</span>'

PAGINAS = []
def pagina(cuerpo, seccion="", fondo="marfil", oscuro=False, clase=""):
    PAGINAS.append((cuerpo, seccion, fondo, oscuro, clase))

def portadilla(num, titulo, fondo, deco, oscuro=False, sub=""):
    pagina(f'''<div class="deco">{deco}</div>
<div class="portadilla"><p class="pnum">{num}</p><h1 class="ptit">{titulo}</h1>{f'<p class="psub">{sub}</p>' if sub else ''}</div>''',
           titulo, fondo, oscuro, "divisor")

def cab(kicker, titulo, intro=""):
    return f'<p class="kicker">{kicker}</p><h2>{titulo}</h2>' + (f'<p class="intro">{intro}</p>' if intro else "")

nombres = dict(morado="Morado", marfil="Marfil", arena="Arena", lila="Lila", salvia="Salvia", tinta="Ciruela tinta", blanco="Blanco", arcilla="Arcilla")

# ======================= PORTADA =======================
pagina(f'''<div class="portada">
<div class="pt-izq">
  <p class="kicker">Manual de marca · v2.0 · Noviembre 2026</p>
  {img(H_LOGO, "Logotipo de Rosa Ondoño", "width:118mm")}
  <p class="lema-xl">Cuídate · Conecta · Siente</p>
  <p class="pt-meta">Estrategia · Identidad · Color · Tipografía<br>Fotografía · Aplicaciones · Accesibilidad</p>
</div>
<div class="pt-der" style="background-image:url({FOTO}/masaje-manos.jpg)"></div>
</div>''', "Portada", "marfil", clase="sin-pie")

# ======================= ÍNDICE =======================
cap = [("01", "Estrategia", "Propósito, valores, posicionamiento y lema"),
       ("02", "Arquetipo y voz", "Personalidad y forma de hablar"),
       ("03", "Logotipo", "Sistema, construcción, versiones y usos"),
       ("04", "Color", "Paleta, procedencia, parejas y proporción"),
       ("05", "Tipografía", "Lettering del logo, familias y jerarquía"),
       ("06", "Elementos gráficos", "Supergráfico, iconos y fotografía"),
       ("07", "Aplicaciones", "Papelería, redes, web y espacio"),
       ("08", "Accesibilidad y archivos", "Contraste, formatos y checklist")]
filas = "".join(f'<div class="ix"><span class="ixn">{n}</span><div><p class="ixt">{t}</p><p class="ixs">{s}</p></div></div>' for n, t, s in cap)
pagina(f'''<div class="g-indice"><div><p class="kicker">Índice</p><h2 class="h-xl">Contenido</h2>
<p class="intro">Todo lo necesario para que Rosa Ondoño se vea, suene y se comporte igual en cualquier lugar: en cabina, en la web, en las redes, en un vale regalo o en la placa del portal.</p>
{iso(style="width:34mm;margin-top:8mm")}</div><div class="ix-col">{filas}</div></div>''', "Índice")

# ======================= CÓMO USARLO =======================
disc = [("01", "Estrategia", "Propósito, valores, posicionamiento y el lema como estructura de la oferta.", C["morado"]),
        ("02", "Identidad verbal", "Arquetipo, personalidad, tono y ejemplos por canal.", C["arcilla"]),
        ("03", "Identidad visual", "Logotipo, color, tipografía, iconos y supergráfico.", C["salvia"]),
        ("04", "Fotografía", "Luz, encuadres, qué sí, qué no y protocolo antes/después.", C["lila"]),
        ("05", "Aplicaciones", "Papelería, redes, web, señalética, uniforme y packaging.", C["arena"])]
cards = "".join(f'<div class="card borde-sup" style="--c:{c}"><p class="cnum">{n}</p><h3>{t}</h3><p>{d}</p></div>' for n, t, d, c in disc)
ficha = [("Marca", "Rosa Ondoño"), ("Categoría", "Estética, terapias y medicina estética"), ("Lema", "Cuídate · Conecta · Siente"),
         ("Arquetipo", "Cuidador + Sabio"), ("Color clave", f'<span class="sw" style="background:{C["morado"]}"></span>#7D1F73'), ("Tipografías", "Jost · Cormorant")]
pagina(f'''{cab("Introducción", "Cómo está hecho este manual", "Reúne el trabajo de cinco disciplinas. Cada sección responde a una pregunta: quiénes somos, cómo hablamos, cómo nos vemos y cómo nos aplicamos.")}
<div class="g5">{cards}</div>
<div class="g2 mt">
<div class="card blanco"><h3>Lo que nunca cambia</h3><p><strong>El isotipo</strong> no se redibuja, deforma, recolorea ni lleva efectos. <strong>El color corporativo</strong> no se modifica: todo lo demás se construye a su alrededor.</p></div>
<div class="card blanco"><h3>Cómo usarlo</h3><p>Las reglas de logotipo, color y legales son <strong>obligatorias</strong>. Lo demás son recomendaciones. Lo marcado {pend()} espera la confirmación del cliente y no se usa en producción.</p></div></div>
<div class="ficha">{"".join(f'<div><p class="fl">{k}</p><p class="fv">{v}</p></div>' for k, v in ficha)}</div>''', "Introducción")

# ======================= 01 · ESTRATEGIA =======================
portadilla("01", "Estrategia", C["morado"], "", oscuro=True, sub="Bienestar integral con criterio")

pagina(f'''<div class="g-2col"><div>{cab("01 · Estrategia", "Qué es Rosa Ondoño")}
<p class="cuerpo">Un centro de estética, terapias manuales y complementarias y medicina estética en la Av. Maisonnave de Alicante, fundado por Rosa Ondoño: más de 30 años de oficio, formación en estética, naturopatía y terapias manuales, y médicos que le confían el drenaje postquirúrgico de sus pacientes.</p>
<p class="cuerpo">Es el único lugar de la zona que reúne bajo un mismo techo la piel, el cuerpo y la emoción, con supervisión médica.</p>
<div class="card" style="background:var(--lila)"><p><strong>El reto de marca.</strong> Hoy la web dice «tu oasis» y «resultados garantizados», como cualquiera. Rosa Ondoño tiene que sonar a lo que dicen sus clientas: trato, calma, sinceridad y oficio.</p></div></div>
<div class="pila">
<div class="card blanco"><h4>Para quién</h4><p>Personas de Alicante, sobre todo mujeres de 35 a 65 años, que quieren cuidarse sin perder naturalidad y buscan a alguien de confianza.</p></div>
<div class="card blanco"><h4>Qué resuelve</h4><p>«No sé por dónde empezar ni en quién confiar.» Respuesta: una valoración y un plan propio.</p></div>
<div class="card blanco"><h4>Qué no es</h4><p>Ni una cadena de bonos y descuentos ni un spa de postal. Tampoco promete milagros.</p></div>
<div class="card blanco"><h4>Posicionamiento</h4><p><strong>Bienestar integral con criterio.</strong></p></div></div></div>''', "Estrategia")

valores = [("Criterio", "Recomendamos solo lo que tiene sentido para ti, aunque sea menos.", "valoracion"),
           ("Cuidado", "Trato cercano, tiempo y atención al detalle.", "masaje"),
           ("Honestidad", "Expectativas realistas, sin promesas ni presión.", "facial"),
           ("Oficio", "Más de 30 años de formación y práctica.", "fisioterapia"),
           ("Integración", "Piel, cuerpo y emoción, tratados juntos.", "drenaje"),
           ("Serenidad", "Calma en el espacio y en la palabra.", "ritual")]
vcards = "".join(f'<div class="card blanco"><span class="circ">{ico(i, 22)}</span><h4>{t}</h4><p>{d}</p></div>' for t, d, i in valores)
pagina(f'''{cab("01 · Estrategia", "Propósito, misión y visión")}
<div class="g3 decl">
<div><p class="dl">Propósito</p><p class="dt">Que cada persona se cuide con conocimiento y con calma, en cada etapa de su vida.</p></div>
<div><p class="dl">Misión</p><p class="dt">Escuchar, valorar y acompañar con un plan propio que une estética, terapias y medicina estética.</p></div>
<div><p class="dl">Visión</p><p class="dt">Ser en Alicante el lugar al que se acude, y se recomienda, para que te cuiden y te digan la verdad.</p></div></div>
<h4 class="mt">Valores</h4><div class="g6">{vcards}</div>''', "Estrategia")

pagina(f'''<div class="g-2col"><div>{cab("01 · Estrategia", "Posicionamiento")}
<div class="card oscuro"><p class="decl-xl">Para quien quiere cuidarse sin perder naturalidad ni confianza, <span class="acento">Rosa Ondoño</span> es el centro de bienestar integral con criterio: estética, terapias y medicina estética supervisada, con una profesional que te dice lo que necesitas, y lo que no.</p></div>
<h4 class="mt">Lo que nos diferencia</h4><ul class="lista">
<li>Más de 30 años de oficio, con nombre y apellidos.</li><li>Supervisión médica identificada (Dr. Roberth Bravo Pardo).</li>
<li>Especialidad histórica en drenaje pre y postquirúrgico.</li><li>4,9★ en Google, con reseñas sobre el trato y la sinceridad.</li></ul></div>
<div class="mapa">
<span class="eje ey1">Rigor médico ↑</span><span class="eje ey2">Sin respaldo médico ↓</span><span class="eje ex1">← Impersonal</span><span class="eje ex2">Cálido, persona →</span>
<div class="punto" style="left:26%;top:24%"><i></i>Clínicas médicas</div>
<div class="punto" style="left:26%;top:66%"><i></i>Cadenas y franquicias</div>
<div class="punto" style="left:74%;top:74%"><i></i>Centros holísticos</div>
<div class="punto rosa" style="left:74%;top:24%"><i></i>Rosa Ondoño</div>
<p class="nota-mapa">Compara categorías, no marcas concretas. Hipótesis a validar con clientas.</p></div></div>''', "Estrategia")

lema = [("Cuídate", "Saber qué necesitas es el primer cuidado.", ["valoracion", "facial", "laser", "medicina"], "Valoración integral · faciales · corporales · láser · medicina estética con supervisión médica", C["blanco"]),
        ("Conecta", "Tu cuerpo te habla. Aquí te ayudamos a escucharlo.", ["masaje", "drenaje", "fisioterapia", "acupuntura"], "Masajes · drenaje pre y postquirúrgico · fisioterapia · osteopatía · terapias complementarias", C["arena"]),
        ("Siente", "Un tiempo solo para ti.", ["ritual", "regalo"], "Rituales individuales y en pareja · circuito spa · tarjeta regalo", C["lila"])]
lp = "".join(f'<div class="lema-panel" style="background:{bg}"><p class="lp-n">0{i+1}</p><p class="lp-v">{v}</p><p class="lp-f">{f}</p><div class="lp-i">{"".join(ico(k, 30) for k in ks)}</div><p class="lp-s">{s}</p></div>' for i, (v, f, ks, s, bg) in enumerate(lema))
pagina(f'''{cab("01 · Estrategia", "El lema como estructura", "Cuídate · Conecta · Siente deja de ser una firma decorativa y pasa a ordenar la oferta, la web y el recorrido de cada clienta.")}
<div class="g3 lema-g">{lp}</div>
<p class="pie-nota">Siempre en este orden, con punto medio ( · ) y mayúscula inicial. No se añaden verbos ni se traduce.</p>''', "Estrategia")

# ======================= 02 · ARQUETIPO Y VOZ =======================
portadilla("02", "Arquetipo y voz", C["lila"], iso(style="position:absolute;right:-10mm;top:-34mm;height:215mm"))

arq = ["Inocente", "Explorador", "Sabio", "Héroe", "Forajido", "Mago", "Persona corriente", "Amante", "Bufón", "Cuidador", "Creador", "Gobernante"]
puntos = ""
for i, a in enumerate(arq):
    ang = -math.pi / 2 + i * 2 * math.pi / 12
    x, y = 50 + 40 * math.cos(ang), 50 + 40 * math.sin(ang)
    puntos += f'<div class="rp{" on" if a in ("Cuidador", "Sabio") else ""}" style="left:{x:.1f}%;top:{y:.1f}%"><i></i><span>{a}</span></div>'
pagina(f'''<div class="g-2col"><div class="rueda"><div class="aro"></div>{puntos}<div class="rc">{iso(style="height:26mm")}</div></div>
<div>{cab("02 · Arquetipo", "El Cuidador que sabe", "Rosa Ondoño es un Cuidador con la voz del Sabio: te acompaña y te protege, y además te explica y te dice la verdad.")}
<div class="barras">
<div class="br"><span>Cuidador</span><b><i style="width:65%;background:var(--morado)"></i></b><em>65 %</em></div>
<div class="br"><span>Sabio</span><b><i style="width:35%;background:var(--arcilla)"></i></b><em>35 %</em></div>
<div class="br"><span>Amante</span><b><i style="width:8%;background:var(--salvia)"></i></b><em>rasgo</em></div></div>
<div class="g2 mini"><div class="card blanco"><h4>Deseo</h4><p>Que la persona esté bien y tranquila.</p></div><div class="card blanco"><h4>Miedo</h4><p>La frialdad, la prisa, el abandono tras el tratamiento.</p></div>
<div class="card blanco"><h4>Don</h4><p>Escuchar y explicar con calma.</p></div><div class="card blanco"><h4>Imagen mental</h4><p>Unas manos expertas y una voz que no te vende nada.</p></div></div>
<div class="card rosa-suave"><p><strong>Arquetipo que evitamos: el Mago.</strong> Su promesa de transformación roza el «resultado garantizado», prohibido en publicidad sanitaria.</p></div></div></div>''', "Arquetipo y voz")

pers = [("Cercana", "Tuteamos y hablamos como Rosa en cabina.", "Confianzuda o con diminutivos"),
        ("Experta", "Explicamos el porqué con palabras sencillas.", "Técnica o fría"),
        ("Honesta", "Expectativas realistas: «puede ayudarte a».", "Promocional o milagrosa"),
        ("Serena", "Frases cortas, ritmo pausado, mucho aire.", "Urgente, con exclamaciones"),
        ("Sensorial", "Texturas y calma en Conecta y Siente.", "Sensual o cliché de spa")]
filas_p = "".join(f'<tr><td class="pn">{a}</td><td><b class="si">Es</b> {b}</td><td><b class="no">No es</b> {c}</td></tr>' for a, b, c in pers)
sl = [("Formal", "Cercano", 72), ("Serio", "Divertido", 30), ("Técnico", "Sencillo", 70), ("Sobrio", "Emotivo", 55)]
sliders = "".join(f'<div class="sl"><span>{a}</span><b><i style="left:{p}%"></i></b><span>{z}</span></div>' for a, z, p in sl)
pagina(f'''{cab("02 · Voz", "Personalidad y tono", "Si Rosa Ondoño fuera una persona, sería una profesional serena y elegante sin ostentación, que te mira a los ojos, te escucha y te dice con cariño lo que de verdad te conviene.")}
<table class="tpers">{filas_p}</table>
<div class="g2 mt"><div><h4>Dimensiones del tono</h4>{sliders}</div>
<div><h4>El tono según la línea</h4><ul class="lista">
<li><strong>Siente:</strong> cercano y evocador.</li><li><strong>Conecta:</strong> equilibrado y sensorial.</li>
<li><strong>Cuídate, estética:</strong> explicativo.</li><li><strong>Medicina estética:</strong> sobrio, experto, con el profesional sanitario identificado.</li></ul></div></div>''', "Arquetipo y voz")

asi = [("Pide tu valoración. Te explicamos qué puedes esperar.", "¡Resultados garantizados en una sesión!"),
       ("El drenaje puede ayudarte a sentir las piernas más ligeras.", "Elimina la retención para siempre."),
       ("Las flores de Bach acompañan tu bienestar emocional.", "Cura la ansiedad y la depresión."),
       ("Que te reconozcas en el espejo, con naturalidad.", "Borra tus arrugas y corrige tus defectos."),
       ("Regala tiempo: tarjetas regalo para rituales.", "¡Últimas plazas! Solo hoy −30 %.")]
si = "".join(f'<div class="bub si-b">{a}</div><div class="bub no-b">{b}</div>' for a, b in asi)
pagina(f'''<div class="g-voz"><div>{cab("02 · Voz", "Cómo hablamos")}
<p class="cuerpo">Como una profesional experta y cariñosa: frases cortas, tuteo, verbos en positivo y nada de jerga.</p>
<h4 class="mt">Palabras que no usamos</h4><p class="vetadas">garantizado · milagro · curativo · perfecto · eliminar para siempre · sin riesgo · oasis · transformación radical</p>
<h4 class="mt">Nuestro vocabulario</h4><p class="cuerpo">cuidar · escuchar · valorar · criterio · oficio · manos · plan · calma · equilibrio · piel · natural · acompañar · tiempo</p></div>
<div><div class="g2 cab-bub"><p class="si">Así sí</p><p class="no">Así no</p></div><div class="g2 bubs">{si}</div></div></div>''', "Arquetipo y voz")

canales = [("Web · portada", "<strong>Cuídate · Conecta · Siente.</strong> Estética, terapias y medicina estética en el centro de Alicante, con más de 30 años de oficio y el criterio de decirte lo que necesitas."),
           ("Ficha de medicina estética", "Antes de cualquier tratamiento, el Dr. Roberth Bravo Pardo valora tu piel y te explica qué puedes esperar. Si no es para ti, te lo diremos."),
           ("Instagram · Conecta", "Esa tensión en los hombros que ya ni notas. Con terapia miofascial trabajamos con las manos para ayudarte a soltar."),
           ("WhatsApp", "Hola, Marta. Gracias por escribirnos. Para recomendarte bien, lo mejor es una valoración de 20 minutos. ¿Te viene bien el jueves a las 17:00?"),
           ("Recepción", "«Centro Rosa Ondoño, buenos días. ¿En qué te puedo ayudar?»"),
           ("Campaña · Navidad", "<strong>Regala tiempo.</strong> Tarjetas regalo para rituales y masajes en Maisonnave.")]
cc = "".join(f'<div class="card blanco canal"><p class="cl">{a}</p><p>{b}</p></div>' for a, b in canales)
pagina(f'''{cab("02 · Voz", "La voz en cada canal", "La personalidad no cambia; el registro se adapta al momento.")}<div class="g3 canales">{cc}</div>''', "Arquetipo y voz")

# ======================= 03 · LOGOTIPO =======================
portadilla("03", "Logotipo", C["blanco"], img(V_LOGO, "", "position:absolute;right:22mm;top:24mm;height:116mm"))

pagina(f'''{cab("03 · Logotipo", "Logotipo principal")}
<div class="lienzo centro" style="height:132mm">{img(H_LOGO, "Logotipo horizontal de Rosa Ondoño", "width:215mm")}</div>
<p class="pie-nota">Archivo maestro: <code>LOGO_2023.psd</code>. Versión horizontal con descriptor: la preferente siempre que haya espacio a lo ancho.</p>''', "Logotipo")

pagina(f'''{cab("03 · Logotipo", "Anatomía")}
<div class="lienzo centro anat" style="height:106mm">{img(H_LOGO, "Anatomía del logotipo", "width:200mm")}
<span class="et" style="left:22mm;top:7mm">1 · Isotipo</span><span class="et" style="left:104mm;top:7mm">2 · Nombre · Bambino Light</span><span class="et" style="left:104mm;bottom:7mm">3 · Descriptor · Biko</span></div>
<div class="g3 mt">
<div class="card blanco"><h4>1 · El isotipo</h4><p>Una figura humana de trazo continuo: cabeza, cuerpo en doble onda y raíz. Es la parte intocable de la marca.</p></div>
<div class="card blanco"><h4>2 · El nombre</h4><p>«Rosa Ondoño» en <strong>Bambino Light</strong>: geométrica, fina, con «O» circular que repite los círculos del isotipo.</p></div>
<div class="card blanco"><h4>3 · El descriptor</h4><p>En <strong>Biko</strong>, muy espaciada. {pend("Revisar")} Falta la tilde de «estética» y no menciona la medicina estética.</p></div></div>''', "Logotipo")

partes = [("La cabeza", "Un círculo abierto: la persona, la mente, la escucha. Es donde empieza el trazo."),
          ("El recorrido", "La doble onda es el cuerpo y la energía que lo recorre: fluidez, equilibrio y conexión."),
          ("La raíz", "El círculo macizo es el peso, la tierra, el centro. La persona que vuelve a sí misma.")]
pagina(f'''<div class="g-simbolo"><div>{cab("03 · Logotipo", "El símbolo", "Un solo trazo que no se interrumpe, de grosor uniforme. Así se cuida en Rosa Ondoño: sin cortes entre piel, cuerpo y emoción.")}
{"".join(f'<div class="card blanco"><h4>{a}</h4><p>{b}</p></div>' for a, b in partes)}</div>
<div class="lienzo centro">{iso(style="height:150mm")}</div></div>''', "Logotipo")

pagina(f'''{cab("03 · Logotipo", "El sistema")}
<div class="sistema">
<div class="sb blanco">{img(H_LOGO, "", "width:88%")}<p class="sl2">A · Horizontal con descriptor · principal</p></div>
<div class="sb blanco s-b">{img(V_LOGO, "", "width:80%")}<p class="sl2">B · Vertical con descriptor</p></div>
<div class="sb lila">{iso(style="height:62%")}<p class="sl2">C · Isotipo</p></div>
<div class="sb blanco">{img(V_SIN, "", "height:70%")}<p class="sl2">D · Vertical sin descriptor</p></div>
<div class="sb arena"><div class="avatar-m">{iso(style="height:62%")}</div><p class="sl2">E · Avatar y favicon</p></div>
</div>
<p class="pie-nota">A para casi todo · B cuando hay espacio vertical (portadas, vales, packaging) · C como sello y supergráfico · D cuando el descriptor no se lee · E en perfiles y pestañas.</p>''', "Logotipo")

pagina(f'''{cab("03 · Logotipo", "Construcción y área de respeto")}
<div class="g2">
<div class="lienzo centro" style="height:110mm;position:relative">
<div class="respeto" style="padding:9mm">{img(H_LOGO, "", "width:140mm;display:block")}</div><span class="cota-t">Área de respeto: 1 x en todo el contorno</span></div>
<div class="lienzo centro" style="height:110mm;position:relative">
<div class="respeto" style="padding:14mm">{iso(style="height:62mm;display:block")}</div><span class="cota-t">x = diámetro del círculo de la cabeza</span></div></div>
<div class="g3 mt">
<div class="card blanco"><h4>Unidad x</h4><p>El diámetro del círculo de la cabeza, igual al de la raíz: ≈ 28 % de la altura del isotipo.</p></div>
<div class="card blanco"><h4>Área de respeto</h4><p>1 x libre alrededor del logotipo y del isotipo: sin texto, imágenes, bordes ni otros logos.</p></div>
<div class="card blanco"><h4>Proporción del isotipo</h4><p>1 : 1,39 (ancho : alto), medida sobre el vector original.</p></div></div>''', "Logotipo")

esc = "".join(f'<div class="esc-i"><div class="esc-c">{iso(style=f"height:{h}mm")}</div><p>{t}</p></div>' for h, t in [(34, "Uso normal"), (15, "15 mm · relieve y bordado"), (10, "10 mm / 32 px · mínimo"), (5, "16 px · solo favicon")])
pagina(f'''{cab("03 · Logotipo", "Tamaños mínimos")}
<div class="g2"><div class="lienzo esc">{esc}</div>
<div class="lienzo centro col" style="height:96mm">{img(H_LOGO, "", "width:110mm")}<p class="pie-nota">Con descriptor: mínimo 40 mm de ancho · 240 px</p>
{img(V_SIN, "", "height:20mm;margin-top:4mm")}<p class="pie-nota">Vertical sin descriptor: mínimo 18 mm de alto · 100 px</p></div></div>
<div class="g3 mt"><div class="card blanco"><h4>Isotipo</h4><p>10 mm impreso · 32 px en pantalla.</p></div><div class="card blanco"><h4>Con descriptor</h4><p>40 mm de ancho · 240 px. Por debajo, el descriptor deja de leerse: usa la versión D.</p></div><div class="card blanco"><h4>Por debajo del mínimo</h4><p>Solo el favicon, exportado desde el vector, nunca ampliando un PNG pequeño.</p></div></div>''', "Logotipo")

fondos = [("Blanco", C["blanco"]), ("Marfil", C["marfil"]), ("Arena", C["arena"]), ("Lila", C["lila"]), ("Salvia", C["salvia"])]
fc = "".join(f'<div class="vc" style="background:{c}">{img(H_LOGO, "", "width:82%")}<p>{n} · {coma(ratio(C["morado"], c), 2)}:1 ✔</p></div>' for n, c in fondos)
pagina(f'''{cab("03 · Logotipo", "Versiones de color y fondos")}
<div class="vcol">{fc}
<div class="vc" style="background:#fff">{iso("#000", "height:30mm")}<p>Monocromo negro · versión oficial del cliente</p></div>
<div class="vc rayas"><p class="grande">Negativo en blanco</p><p>{pend()} Requiere autorización: cambia el color del icono.</p></div>
<div class="vc" style="background:var(--tinta)"><p class="grande" style="color:var(--marfil)">Fondo oscuro</p><p style="color:var(--marfil)">✖ Morado sobre tinta: {coma(ratio(C["morado"], C["tinta"]), 2)}:1. Prohibido.</p></div></div>
<p class="pie-nota">El logotipo es un elemento gráfico: necesita al menos 3:1 con el fondo. Sobre foto, solo en zonas claras y lisas.</p>''', "Logotipo")

malos = [("transform:scaleX(1.45)", "No lo deformes", ""), ("transform:rotate(-14deg)", "No lo gires", ""),
         ("filter:hue-rotate(160deg)", "No cambies su color", ""), ("filter:drop-shadow(5px 6px 3px rgba(0,0,0,.4))", "Sin sombras ni efectos", ""),
         ("opacity:.25", "No uses poco contraste", ""), ("", "No lo pongas sobre fondo oscuro", "background:var(--tinta)"),
         ("", "No lo pongas sobre fotos recargadas", f"background:url({FOTO}/patio.jpg) center/cover"), ("transform:scaleX(-1)", "No lo reflejes", "")]
mc = "".join(f'<div class="mal"><div class="mc" style="{b}">{img(H_LOGO, "Uso incorrecto", "width:76%;" + s)}</div><p>✖ {t}</p></div>' for s, t, b in malos)
pagina(f'''{cab("03 · Logotipo", "Usos incorrectos")}<div class="g4 malos">{mc}</div>
<p class="pie-nota">Tampoco: separar el isotipo del nombre y recolocarlos, cambiar la tipografía del nombre, añadir contornos o encerrarlo en formas.</p>''', "Logotipo")

# ======================= 04 · COLOR =======================
portadilla("04", "Color", C["arena"], iso(style="position:absolute;right:26mm;top:-46mm;height:240mm;transform:rotate(-8deg)"))

pal = [("Morado Rosa Ondoño", C["morado"], "El logotipo maestro (PSD 2023). La firma.", "Isotipo, acentos, botones", True),
       ("Marfil", C["marfil"], "La pared encalada y la luz de la mañana.", "Fondo principal", False),
       ("Arena", C["arena"], "El lino crudo y la baldosa del patio.", "Bloques · «Conecta»", False),
       ("Lila", C["lila"], "El morado de la marca, hecho piel.", "«Siente» y vales", False),
       ("Salvia", C["salvia"], "Las plantas del jardín interior.", "Acento complementario", False),
       ("Arcilla", C["arcilla"], "La terracota de las macetas.", "Solo decorativo", False),
       ("Ciruela tinta", C["tinta"], "El morado llevado a la sombra.", "Texto", False)]
def tarjeta_color(n, h, p, u, fijo):
    claro = lum(h) > 0.3
    return (f'<div class="pc"><div class="pc-s" style="background:{h};color:{"var(--tinta)" if claro else "#fff"}">'
            f'<p>{n}</p>{"<span class=fijo>FIJO</span>" if fijo else ""}</div><div class="pc-d"><p><b>{h}</b></p><p>RGB {rgb(h)}</p>'
            f'<p>CMYK {pend() if fijo else "tras prueba"}</p><p class="proc"><b>Procedencia:</b> {p}</p><p class="uso">{u}</p></div></div>')
pagina(f'''{cab("04 · Color", "Paleta y su procedencia", "Un solo color fijo, el morado del logotipo, y una paleta que sale del propio centro: la cal, el lino, el jardín y la terracota.")}
<div class="paleta">{"".join(tarjeta_color(*p) for p in pal)}</div>
<p class="pie-nota">CMYK y Pantone del morado: {pend()} (dato de la imprenta). Los del resto se fijarán con una prueba de impresión.</p>''', "Color")

mor = [("#7D1F73", "Logotipo maestro LOGO_2023.psd y logos completos", "Propuesto como oficial"),
       ("#701B78", "Favicon e isotipo de la web actual", "Variante"),
       ("#6C2470", "PNG del isotipo y vertical sin descriptor", "Variante"),
       ("#8E1F5C", "CSS de la web actual (49 usos)", "Se retira")]
mc4 = "".join(f'<div class="mor"><div class="mor-s" style="background:{h}"></div><p class="mh">{h}</p><p>{s}</p><p class="mest {"ok" if i == 0 else ""}">{e}</p></div>' for i, (h, s, e) in enumerate(mor))
pagina(f'''{cab("04 · Color", "Un morado, cuatro versiones", "Hoy circulan cuatro morados distintos. Son tan parecidos que, juntos, ensucian la marca: entre ellos el contraste no llega a 1,1:1.")}
<div class="g4">{mc4}</div>
<div class="g2 mt"><div class="card oscuro"><p class="decl-m">Proponemos <span class="acento">#7D1F73</span> como color oficial: es el del archivo maestro del logotipo (2023) y el de los logos completos.</p></div>
<div class="card blanco"><h4>{pend("Decisión del cliente")}</h4><p>Confirmar #7D1F73 y facilitar el Pantone o el CMYK de la imprenta. A partir de ahí, web, papelería y rótulos usan un único valor.</p></div></div>''', "Color")

parejas = [("La firma", "marfil", "morado"), ("El día a día", "marfil", "tinta"), ("Botón", "morado", "blanco"),
           ("Conecta", "arena", "morado"), ("Siente", "lila", "tinta"), ("Jardín", "salvia", "tinta")]
pc6 = ""
for etq, f, t in parejas:
    r = ratio(C[f], C[t])
    pc6 += (f'<div class="par"><div class="par-a" style="background:{C[f]};color:{C[t]}"><p class="pe">«{etq}»</p><p class="pn2">{nombres[f]}</p><p>{C[f]}</p></div>'
            f'<span class="pr">{coma(r)}:1 · {nivel(r)}</span><div class="par-b" style="background:{C[t]};color:{C[f]}"><p class="pn2">{nombres[t]}</p><p>{C[t]}</p></div></div>')
pagina(f'''{cab("04 · Color", "Parejas de color", "Cada pieza usa una sola pareja: un fondo claro y una tinta profunda. Contraste medido con la fórmula WCAG 2.2.")}<div class="parejas">{pc6}</div>''', "Color")

prop = [("Marfil", C["marfil"], 50), ("Arena", C["arena"], 18), ("Morado", C["morado"], 12), ("Lila", C["lila"], 8), ("Tinta", C["tinta"], 7), ("Salvia", C["salvia"], 3), ("Arcilla", C["arcilla"], 2)]
barra = "".join(f'<div style="flex:{p};background:{h};color:{"#fff" if lum(h) < .2 else "var(--tinta)"}"><b style="font-size:{20 if p > 5 else 11}pt">{p} %</b><span>{n if p > 3 else ""}</span></div>' for n, h, p in prop)
pagina(f'''{cab("04 · Color", "Proporción y reglas de uso")}<div class="barra-xl">{barra}</div>
<div class="g3 mt"><div class="card blanco"><h4>El morado es la firma</h4><p>Entre el 10 y el 15 % de cada pieza. Si pasa del 20 %, pierde valor y cansa.</p></div>
<div class="card blanco"><h4>Una pareja por pieza</h4><p>Si se mezclan parejas, la marca pierde calma. Salvia y arcilla, solo en detalles.</p></div>
<div class="card blanco"><h4>Nunca morado sobre oscuro</h4><p>Con la tinta da {coma(ratio(C["morado"], C["tinta"]), 2)}:1: no se lee. Sobre fondo oscuro, el texto va en marfil.</p></div></div>''', "Color")

# ======================= 05 · TIPOGRAFÍA =======================
portadilla("05", "Tipografía", C["tinta"], '<p class="aa">Aa</p>', oscuro=True)

pagina(f'''{cab("05 · Tipografía", "Un lettering y dos familias")}
<div class="g3 tipos">
<div class="card oscuro"><p class="cl" style="color:var(--lila)">Lettering del logotipo</p><div class="lt-n">Rosa Ondoño</div>
<p class="mt">«Rosa Ondoño» está compuesto en <strong>Bambino Light</strong> y el descriptor en <strong>Biko</strong>. Solo viven en el logotipo: no se escribe con ellas.</p><p class="mt">{pend("Licencias por comprobar")}</p></div>
<div class="card blanco"><p class="cl">Jost · titulares, texto e interfaz</p><p class="mega" style="font-family:Jost;font-weight:300">Aa Ññ</p>
<p><b>Light 300 · Regular 400 · Medium 500</b></p><p>Geométrica de «o» circular, prima hermana de Bambino. Es la voz moderna y limpia de la marca.</p><p class="lic">SIL Open Font License · gratuita</p></div>
<div class="card blanco"><p class="cl">Cormorant Garamond · lema y citas</p><p class="mega" style="font-family:'Cormorant Garamond';font-style:italic;font-weight:500">Aa Ññ</p>
<p><b>Italic 500 · SemiBold 600</b></p><p>Serifa editorial para el lema, las citas y los momentos «Siente». Aporta calidez y oficio.</p><p class="lic">SIL Open Font License · gratuita</p></div></div>''', "Tipografía")

jer = [("Titular", "Jost Light · 52/56 · −2 %", '<p style="font-weight:300;font-size:38pt;letter-spacing:-.02em;line-height:1">Bienestar con criterio</p>'),
       ("Título de sección", "Jost Regular · 30/36", '<p style="font-size:21pt">Tratamientos faciales</p>'),
       ("Lema y citas", "Cormorant Italic 500 · 26/32", '<p style="font-family:Cormorant Garamond;font-style:italic;font-size:20pt;color:var(--morado)">Cuídate · Conecta · Siente</p>'),
       ("Antetítulo", "Jost Medium · 11 · +16 % · mayúsculas", '<p style="font-weight:500;font-size:9pt;letter-spacing:.16em;text-transform:uppercase;color:var(--morado)">Cuídate · Medicina estética</p>'),
       ("Texto", "Jost Regular · 17/27", '<p style="font-size:12pt">Antes de cualquier tratamiento te valoramos y te explicamos qué puedes esperar.</p>'),
       ("Legal", "Jost Regular · 12/16", '<p style="font-size:8.5pt">Nº de registro sanitario: PENDIENTE · Supervisión médica: Dr. Roberth Bravo Pardo.</p>')]
pagina(f'''{cab("05 · Tipografía", "Jerarquía")}<div class="jer">{"".join(f'<div class="jr"><div><p class="jn">{a}</p><p class="js">{b}</p></div><div>{c}</div></div>' for a, b, c in jer)}</div>
<p class="pie-nota">En la web, las fuentes se sirven desde el propio servidor (WOFF2), solo en los pesos indicados. En ofimática, si no están instaladas: Century Gothic y Georgia.</p>''', "Tipografía")

# ======================= 06 · ELEMENTOS GRÁFICOS =======================
portadilla("06", "Elementos gráficos", C["lila"], iso(style="position:absolute;left:150mm;top:-60mm;height:300mm;transform:rotate(12deg)"))

tiles = [(C["marfil"], "right:-26mm;bottom:-46mm;height:115mm;transform:rotate(-10deg)", "Cuídate"),
         (C["arena"], "right:-30mm;bottom:-50mm;height:120mm;transform:rotate(8deg)", "Conecta"),
         (C["lila"], "right:-24mm;bottom:-40mm;height:118mm", "Siente"),
         ("#fff", "right:-6mm;bottom:-58mm;height:120mm;transform:rotate(-6deg)", "")]
tl = "".join(f'<div class="tile" style="background:{bg}">{iso(style="position:absolute;" + s)}{f"<p class=tt>{t}</p>" if t else img(H_LOGO, "", "position:absolute;left:7mm;top:7mm;width:44mm")}</div>' for bg, s, t in tiles)
pagina(f'''<div class="g-super"><div>{cab("06 · Elementos", "El supergráfico")}
<p class="cuerpo">El isotipo, a gran escala y recortado por el borde, es el gran recurso de la marca: aporta movimiento y reconocimiento sin añadir nada nuevo.</p>
<div class="card blanco"><h4>Escala</h4><p>Entre el 120 % y el 300 % del alto de la pieza.</p></div>
<div class="card blanco"><h4>Giro</h4><p>Entre −12° y +12°. Nunca boca abajo.</p></div>
<div class="card blanco"><h4>Color</h4><p>Siempre en su morado, sobre marfil, arena, lila o blanco. Nunca junto al logotipo grande.</p></div>
<p class="pie-nota">{pend("Aprobación")} Ampliar y recortar el isotipo no lo redibuja, pero cambia su encuadre: lo debe aprobar el cliente.</p></div><div class="g2 tiles">{tl}</div></div>''', "Elementos gráficos")

icg = "".join(f'<div class="ic"><span class="icc">{ico(k, 24)}</span><p>{v[0]}</p></div>' for k, v in ICONOS.items())
pagina(f'''<div class="g-2col"><div>{cab("06 · Elementos", "Iconografía", "Un set propio de iconos de línea: trazo de 1,5 px, extremos redondeados, dentro de un círculo lila. Acompaña al isotipo, pero no lo imita.")}
<div class="iconos">{icg}</div></div>
<div>{cab("06 · Elementos", "El punto medio")}<p class="cuerpo">El separador del lema es el segundo recurso propio. Separa datos, menús, categorías y firmas, siempre en morado.</p>
<div class="card blanco centro" style="height:38mm"><p class="pm">Faciales <i>·</i> Corporales <i>·</i> Masajes</p></div>
<div class="card blanco centro mt" style="height:38mm"><p class="pm" style="font-size:14pt!important">965 120 300 <i>·</i> Av. Maisonnave 38 <i>·</i> rosaondono.com</p></div>
<p class="pie-nota">Los iconos SVG están en <code>identidad/iconos/</code>.</p></div></div>''', "Elementos gráficos")

pagina(f'''<div class="mood">
<div class="m1" style="background-image:url({FOTO}/masaje-espalda.jpg)"><span>Manos que cuidan</span></div>
<div class="m2" style="background-image:url({FOTO}/retrato.jpg)"><span>Piel real, luz cálida</span></div>
<div class="m3" style="background-image:url({FOTO}/olivo.jpg)"><span>Objetos sencillos</span></div>
<div class="m4" style="background-image:url({FOTO}/patio.jpg)"><span>El jardín interior</span></div>
<div class="m5" style="background-image:url({FOTO}/lino.jpg)"><span>Lino y textura</span></div>
<div class="m6"><p class="kicker">06 · Fotografía</p><h2>La luz de Alicante, sobre piel, lino y manos</h2><p class="cuerpo">Luz natural lateral y cálida, personas reales con textura de piel y materiales naturales. El morado no se fuerza en la foto: lo pone el diseño.</p></div>
</div>''', "Fotografía", clase="sin-pie")

pagina(f'''{cab("06 · Fotografía", "Qué sí y qué no")}
<div class="g2"><div class="card blanco"><h4 class="si">✔ Sí</h4><ul class="lista">
<li>Luz natural de ventana, sombras suaves y grano fino (4.500–5.000 K).</li><li>Manos de Rosa y del equipo trabajando: el oficio es la prueba.</li>
<li>Personas de distintas edades, con piel con textura.</li><li>Lino, cerámica, madera clara, olivo y el jardín del centro.</li>
<li>En medicina estética, la conversación de la valoración, no la aguja.</li></ul></div>
<div class="card blanco"><h4 class="no">✖ No</h4><ul class="lista">
<li>Piedras apiladas, orquídeas, velas y bambú de stock.</li><li>Pieles plastificadas o retoque que borre la textura.</li>
<li>Agujas, jeringas o productos médicos con marca.</li><li>Cuerpos sexualizados o planos que generen inseguridad.</li><li>Filtros de color, viñetas o neones.</li></ul></div></div>
<div class="card oscuro mt"><h4 style="color:var(--lila)">Antes y después: protocolo obligatorio</h4><div class="g5 pasos">
<p><b>1</b>Consentimiento escrito, específico y revocable.</p><p><b>2</b>Misma luz, encuadre, distancia y fondo.</p><p><b>3</b>Sin retoque. Se archivan los RAW.</p>
<p><b>4</b>Tratamiento, sesiones y tiempo, con «resultados variables».</p><p><b>5</b>En medicina estética, revisar la normativa autonómica.</p></div></div>
<p class="pie-nota">Fotos del moodboard: Unsplash (licencia Unsplash), solo como referencia. Las definitivas saldrán de una sesión propia en el centro.</p>''', "Fotografía")

# ======================= 07 · APLICACIONES =======================
portadilla("07", "Aplicaciones", C["morado"], "", oscuro=True, sub="La marca en la vida real")

pagina(f'''{cab("07 · Aplicaciones", "Papelería")}
<div class="pap">
<div class="pap-c"><div class="tv frente">{img(V_SIN, "", "height:28mm")}</div><div class="tv dorso"><p class="tn">Rosa Ondoño</p><p class="tc">Fundadora · Esteticista y terapeuta</p>
<p class="td">965 120 300 <i>·</i> 691 315 622<br>info@rosaondono.com<br>Av. Maisonnave 38, Entlo. Izq.<br>03003 Alicante</p>{iso(style="position:absolute;right:-6mm;bottom:-14mm;height:38mm")}</div><p class="pap-l">Tarjeta de visita · 85 × 55 mm</p></div>
<div class="pap-c"><div class="carta">{img(H_LOGO, "", "width:38mm")}<div class="lineas"><i></i><i></i><i></i><i style="width:70%"></i><br><i></i><i></i><i style="width:55%"></i></div>
<p class="carta-pie">Av. Maisonnave 38 · 03003 Alicante · 965 120 300 · rosaondono.com</p>{iso(style="position:absolute;right:-16mm;bottom:-22mm;height:60mm")}</div><p class="pap-l">Hoja de carta · A4</p></div>
<div class="pap-c"><div class="vale">{iso(style="position:absolute;left:-22mm;top:-16mm;height:70mm")}<div class="vale-t"><p class="kicker">Tarjeta regalo · Siente</p><p class="lema-m">Regala tiempo</p><p class="peq">Para ________ · Ritual ________<br>Válida hasta ________ · Nº ____</p></div></div><p class="pap-l">Tarjeta regalo · 210 × 99 mm</p></div></div>
<p class="pie-nota">Papel de algodón sin estucar, isotipo en tinta directa o relieve en seco. Tarjetas regalo solo para estética, masajes y rituales: nunca para medicina estética.</p>''', "Aplicaciones")

pagina(f'''{cab("07 · Aplicaciones", "Redes sociales")}
<div class="redes2">
<div class="perfil"><div class="avatar-r">{iso(style="height:58%")}</div><p>Perfil</p></div>
<div class="post p-foto" style="background-image:url({FOTO}/masaje-manos.jpg)"><div class="pf-t"><p class="kicker" style="color:var(--marfil)">Conecta</p><p class="pt2">Tu cuerpo te habla.</p></div></div>
<div class="post" style="background:var(--lila)">{iso(style="position:absolute;right:-22mm;bottom:-52mm;height:84mm")}<p class="kicker">Siente</p><p class="pt2" style="color:var(--tinta)">Un tiempo<br>solo para ti.</p></div>
<div class="post" style="background:#fff"><p class="kicker">Cuídate · La valoración</p><p class="pt3">«Tres preguntas que te haré antes de cualquier tratamiento facial.»</p><p class="firma-p">— Rosa</p>{img(H_LOGO, "", "position:absolute;left:6mm;bottom:6mm;width:30mm")}</div>
<div class="story" style="background:var(--arena)">{iso(style="position:absolute;left:4mm;top:-24mm;height:60mm;transform:rotate(-8deg)")}<p class="pt2">Regala tiempo</p><span class="st-btn">Ver tarjetas</span></div></div>
<div class="dest">{"".join(f'<div><span class="icc g">{ico(k, 24)}</span><p>{t}</p></div>' for k, t in [("valoracion", "Valoración"), ("facial", "Facial"), ("masaje", "Masajes"), ("ritual", "Rituales"), ("regalo", "Regalo"), ("ubicacion", "El centro")])}</div>
<p class="pie-nota">Una pareja de color por pieza, titular en Jost Light y el isotipo como supergráfico. El logotipo, pequeño y discreto. Portadas de destacados con el set de iconos.</p>''', "Aplicaciones")

pagina(f'''{cab("07 · Aplicaciones", "Web y digital")}
<div class="g-web"><div class="nav-m"><div class="barra-n"><i></i><i></i><i></i><span>rosaondono.com</span></div>
<div class="web-h">{img(H_LOGO, "", "height:9mm")}<p>Cuídate · Conecta · Siente · Sobre Rosa · Contacto</p><span class="btn">Pide tu valoración</span></div>
<div class="web-hero"><div><p class="kicker">Estética · Terapias · Medicina estética</p><p class="wh1">Bienestar integral,<br>con criterio.</p><p class="peq">Más de 30 años de oficio en el centro de Alicante.</p><span class="btn">Pide tu valoración</span></div>
<div class="web-f" style="background-image:url({FOTO}/masaje-espalda.jpg)"></div></div></div>
<div class="movil"><div class="mv">{img(H_LOGO, "", "width:32mm;margin:5mm auto 3mm;display:block")}<div class="mv-f" style="background-image:url({FOTO}/retrato.jpg)"></div><p class="wh2">Tu piel, con criterio.</p><span class="btn">Reservar</span></div></div></div>
<div class="g2 mt"><div class="firma2">{iso(style="height:16mm")}<div><p class="fn">Nombre Apellido</p><p>Recepción · Rosa Ondoño</p><p>965 120 300 · WhatsApp 691 315 622</p><p class="lema-s">Cuídate · Conecta · Siente</p></div></div>
<div class="card blanco"><h4>Firma de email y WhatsApp</h4><p>Isotipo en PNG a 2×, sin banners. Foto de perfil de WhatsApp: el mismo avatar que en redes. Bienvenida: «Hola, gracias por escribirnos. Si nos cuentas qué te gustaría cuidar, te orientamos.»</p></div></div>''', "Aplicaciones")

pagina(f'''{cab("07 · Aplicaciones", "El espacio")}
<div class="g3 espacio">
<div class="esp"><div class="placa">{img(V_LOGO, "", "height:40mm")}<p class="peq">Entresuelo izquierda · Nº registro sanitario {pend()}</p></div><p class="pap-l">Placa de portal · 300 × 150 mm</p></div>
<div class="esp"><div class="unif-w"><svg viewBox="0 0 200 220" class="unif"><path d="M60 20 L100 34 L140 20 L178 44 L164 92 L146 86 L146 210 L54 210 L54 86 L36 92 L22 44 Z" fill="#E9DCCB" stroke="#d6c6b3"/><path d="M84 26 L100 52 L116 26" fill="none" stroke="#c9b8a4" stroke-width="2"/></svg>
{iso(style="position:absolute;left:58%;top:30%;height:9mm")}</div><p class="pap-l">Túnica de cabina · isotipo bordado 25 mm</p></div>
<div class="esp"><div class="bolsa"><span class="asa"></span>{iso(style="height:34mm")}</div><p class="pap-l">Bolsa de papel kraft · una tinta</p></div></div>
<div class="g3 mt"><div class="card blanco"><h4>Señalética</h4><p>Metacrilato mate o latón, con fondo marfil e isotipo a color. El nº de registro sanitario es obligatorio.</p></div>
<div class="card blanco"><h4>Uniformes</h4><p>Cabina: túnica arena o marfil. Medicina estética: bata blanca con nombre, titulación y nº de colegiado {pend()}.</p></div>
<div class="card blanco"><h4>Packaging</h4><p>Kraft o arena, una sola tinta y sin plastificados brillantes. Cajas en marfil con relieve en seco.</p></div></div>''', "Aplicaciones")

# ======================= 08 · ACCESIBILIDAD Y ARCHIVOS =======================
pares = [("marfil", "tinta"), ("marfil", "morado"), ("morado", "blanco"), ("arena", "morado"), ("lila", "tinta"), ("salvia", "tinta"), ("salvia", "morado"), ("arcilla", "morado"), ("tinta", "morado")]
filas_c = ""
for f, t in pares:
    r = ratio(C[f], C[t]); ok = r >= 4.5
    filas_c += f'<tr><td><span class="chip-c" style="background:{C[f]};color:{C[t]}">Aa 16 px</span></td><td>{nombres[t]} sobre {nombres[f].lower()}</td><td><b>{coma(r)}:1</b></td><td class="{"ok" if ok else "ko"}">{"✔" if ok else "✖"} {nivel(r)}</td></tr>'
pagina(f'''<div class="g-2col"><div>{cab("08 · Accesibilidad", "Contraste comprobado", "Mínimo 4,5:1 en texto normal y 3:1 en texto grande y elementos gráficos (WCAG 2.2 AA).")}<table class="tcontr">{filas_c}</table></div>
<div class="pila mt2"><div class="card rosa-suave"><h4>Nunca morado sobre oscuro</h4><p>Con la tinta da {coma(ratio(C["morado"], C["tinta"]), 2)}:1. Sobre fondo oscuro, el texto va en marfil.</p></div>
<div class="card blanco"><h4>Arcilla y salvia, solo de apoyo</h4><p>Con ellas, el morado no llega a 4,5:1 en texto pequeño. Se usan como fondo con texto en tinta, o en ilustración.</p></div>
<div class="card blanco"><h4>Web</h4><p>Objetivo WCAG 2.2 AA: foco visible, botones de 48 px, textos alternativos y movimiento reducido si el usuario lo pide.</p></div></div></div>''', "Accesibilidad")

pagina(f'''<div class="g-2col"><div>{cab("08 · Archivos", "Formatos válidos")}
<table class="tform"><tr><th>Formato</th><th>Color</th><th>Uso</th></tr>
<tr><td><b>SVG</b></td><td>RGB / HEX</td><td>Web e interfaz. Isotipo disponible; logotipo completo {pend()}</td></tr>
<tr><td><b>PDF vectorial</b></td><td>CMYK + Pantone</td><td>Imprenta, papelería y vales</td></tr>
<tr><td><b>EPS / AI</b></td><td>CMYK + Pantone</td><td>Rotulación, bordado, vinilo y relieve</td></tr>
<tr><td><b>PNG transparente</b></td><td>RGB</td><td>Office, email, redes y presentaciones (2× y 3×)</td></tr>
<tr><td><b>JPG</b></td><td>sRGB</td><td>Solo fotografía, nunca el logotipo</td></tr></table>
<p class="cuerpo"><b>RGB/HEX</b> para todo lo que se ve en pantalla; <b>CMYK o Pantone</b> para todo lo que se imprime. En tarjetas, placa y vales, tinta directa Pantone.</p>
<p class="pie-nota">Archivos en <code>identidad/logo/</code>: isotipo-color.svg · isotipo-negro.svg · logo-horizontal.png · logo-vertical.png · logo-vertical-sin-descriptor.png</p></div>
<div>{cab("08 · Archivos", "Antes de publicar")}<ul class="check">
<li>Logotipo original, sin modificar, sobre fondo claro y con su área de respeto.</li><li>Un único morado: #7D1F73.</li>
<li>Solo Jost y Cormorant en los textos.</li><li>Todo el texto con contraste AA.</li>
<li>Sin garantías, «curar», «seguro», urgencias ni palabras vetadas.</li><li>Medicina estética: profesional identificado y nº de registro sanitario.</li>
<li>Consentimiento escrito de cada persona fotografiada.</li><li>Revisión de QA según la guía de cumplimiento legal.</li></ul></div></div>''', "Archivos")

pend_l = [("Color oficial", "Confirmar #7D1F73 y facilitar Pantone y CMYK de la imprenta."),
          ("Logotipo completo en vector", "Tenemos el isotipo en SVG. Falta el logotipo con el nombre (AI, EPS o PDF)."),
          ("Licencias tipográficas", "Bambino Light y Biko: confirmar la licencia comercial del logotipo."),
          ("Descriptor", "Corregir la tilde de «estética» y valorar incluir la medicina estética."),
          ("Negativo y supergráfico", "Autorizar el isotipo en blanco sobre fondo oscuro y su uso ampliado y recortado."),
          ("Datos sanitarios", "Nº de registro sanitario del centro y nº de colegiado del médico.")]
pagina(f'''{cab("Siguientes pasos", "Lo que necesitamos del cliente", "Sin estos datos, el manual es un borrador: en cuanto lleguen, se actualiza y se exportan los archivos finales.")}<div class="g3">{"".join(f'<div class="card borde-sup" style="--c:var(--morado)"><p class="cnum">{i+1:02d}</p><h4>{a}</h4><p>{b}</p></div>' for i, (a, b) in enumerate(pend_l))}</div>''', "Pendientes")

pagina(f'''<div class="contra">{iso(style="position:absolute;right:-70mm;top:-56mm;height:300mm;transform:rotate(-10deg)")}
<div class="contra-t">{img(V_LOGO, "Logotipo de Rosa Ondoño", "height:62mm")}
<p class="lema-xl" style="margin-top:10mm">Cuídate · Conecta · Siente</p>
<p class="pt-meta">Av. Maisonnave 38, Entlo. Izq. · 03003 Alicante<br>965 120 300 · rosaondono.com · @rosaondono</p></div></div>''', "Contraportada", "marfil", clase="sin-pie")

# ======================= ESTILOS =======================
CSS = """
:root{--morado:#7D1F73;--marfil:#F7F2EB;--arena:#E9DCCB;--lila:#E8DAE6;--arcilla:#B7897A;--tinta:#2E1A2C;--salvia:#A9B7A4}
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#8d8590}
body{font-family:Jost,'Century Gothic',sans-serif;color:var(--tinta);font-size:10.5pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;padding:14mm 18mm 18mm;margin:10mm auto;box-shadow:0 4px 30px rgba(0,0,0,.25);break-after:page}
@media print{html{background:none}.page{margin:0;box-shadow:none}}
.pie{position:absolute;left:18mm;right:18mm;bottom:7mm;display:flex;justify-content:space-between;font-size:7.5pt;opacity:.7}
.oscuro-p .pie,.oscuro-p .kicker{color:var(--marfil)}
.kicker{font-size:8pt;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--morado);margin-bottom:2.5mm}
h2{font-weight:300;font-size:30pt;line-height:1.02;letter-spacing:-.02em;margin-bottom:5mm}
.h-xl{font-size:46pt}
h3{font-weight:500;font-size:13pt;margin-bottom:2mm} h4{font-weight:500;font-size:10.5pt;margin-bottom:1.2mm}
.intro{font-size:12pt;max-width:210mm;margin-top:-1mm;margin-bottom:7mm;color:#5a4a57}
.cuerpo{font-size:11pt;margin-bottom:4mm}
.mt{margin-top:6mm}.mt2{margin-top:24mm}
p{margin-bottom:1mm}
.card{background:var(--marfil);border-radius:5mm;padding:5mm 6mm}
.card.blanco{background:#fff}.card.oscuro{background:var(--tinta);color:var(--marfil)}.card.rosa-suave{background:#F4E1E4}
.card p{font-size:9.5pt}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:5mm}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}.g5{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm}.g6{display:grid;grid-template-columns:repeat(6,1fr);gap:4mm}
.g-2col{display:grid;grid-template-columns:1fr 1fr;gap:12mm;height:100%}
.pila{display:flex;flex-direction:column;gap:4mm}
.centro{display:flex;align-items:center;justify-content:center}.col{flex-direction:column;gap:2mm}
.pend{display:inline-block;background:#FCE8E6;color:#8A1C1C;font-size:7pt;font-weight:500;letter-spacing:.06em;padding:.3mm 2mm;border-radius:10mm;vertical-align:1px}
.pie-nota{font-size:8.5pt;color:#6b5b68;margin-top:4mm}
.lista{padding-left:4mm}.lista li{margin:1.2mm 0;font-size:10pt}
code{font-size:8pt;background:rgba(125,31,115,.08);padding:0 1.5mm;border-radius:1mm}
.ok{color:#1d6b33;font-weight:500}.ko{color:#a3262a;font-weight:500}
.si{color:#1d6b33}.no{color:#a3262a}
.sw{display:inline-block;width:3.5mm;height:3.5mm;border-radius:50%;vertical-align:-.5mm;margin-right:1.5mm}
.portada{position:absolute;inset:0;display:grid;grid-template-columns:1.05fr 1fr}
.pt-izq{padding:18mm 16mm 18mm 20mm;display:flex;flex-direction:column;justify-content:center;gap:9mm}
.pt-der{background-size:cover;background-position:center}
.lema-xl{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:26pt;color:var(--morado)}
.pt-meta{font-size:9pt;letter-spacing:.04em;color:#6b5b68}
.deco{position:absolute;inset:0}
.portadilla{position:absolute;left:18mm;bottom:20mm}
.pnum{font-weight:300;font-size:120pt;line-height:.85;letter-spacing:-.04em}
.ptit{font-weight:300;font-size:40pt;letter-spacing:-.02em;margin-top:2mm}
.psub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:20pt;margin-top:2mm}
.divisor .pnum,.divisor .ptit{color:var(--tinta)}.divisor.oscuro-p .pnum,.divisor.oscuro-p .ptit,.divisor.oscuro-p .psub{color:var(--marfil)}
.aa{position:absolute;right:18mm;top:4mm;font-weight:300;font-size:210pt;line-height:1;color:var(--lila)}
.g-indice{display:grid;grid-template-columns:1fr 1.3fr;gap:16mm;height:100%}
.ix-col{display:grid;grid-template-columns:1fr 1fr;column-gap:10mm;align-content:start;padding-top:8mm}
.ix{display:flex;gap:5mm;border-top:1px solid #e3d8cc;padding:4mm 0}
.ixn{font-size:18pt;font-weight:300;color:var(--morado);width:12mm}.ixt{font-size:13pt;font-weight:500}.ixs{font-size:9pt;color:#6b5b68}
.borde-sup{border-top:1.6mm solid var(--c);background:#fff}.cnum{color:var(--morado);font-weight:500;font-size:9pt}
.ficha{display:grid;grid-template-columns:repeat(6,1fr);gap:4mm;border-top:1px solid #e3d8cc;margin-top:7mm;padding-top:4mm}
.fl{font-size:7pt;letter-spacing:.16em;text-transform:uppercase;color:#7a6a78}.fv{font-weight:500;font-size:10pt}
.decl .dl{color:var(--morado);font-weight:500;font-size:9pt}.decl .dt{font-weight:300;font-size:17pt;line-height:1.18;letter-spacing:-.01em}
.circ{display:inline-flex;width:11mm;height:11mm;border-radius:50%;background:var(--lila);align-items:center;justify-content:center;margin-bottom:3mm}
.decl-xl{font-weight:300;font-size:15pt;line-height:1.32}.decl-m{font-weight:300;font-size:14pt;line-height:1.3}.acento{color:var(--lila);font-weight:500}
.mapa{position:relative;background:#fff;border-radius:5mm;height:170mm}
.mapa::before{content:'';position:absolute;left:50%;top:12mm;bottom:12mm;border-left:1px solid #ddd}
.mapa::after{content:'';position:absolute;top:50%;left:10mm;right:10mm;border-top:1px solid #ddd}
.eje{position:absolute;font-size:7pt;letter-spacing:.12em;text-transform:uppercase;color:#7a6a78}
.ey1{left:52%;top:5mm}.ey2{left:52%;bottom:5mm}.ex1{left:5mm;top:calc(50% + 2mm)}.ex2{right:5mm;top:calc(50% + 2mm)}
.punto{position:absolute;transform:translate(-50%,-50%);text-align:center;font-size:9pt;color:#6b5b68;z-index:1;width:40mm}
.punto i{display:block;width:9mm;height:9mm;border-radius:50%;background:#cfc6cd;margin:0 auto 2mm}
.punto.rosa{color:var(--morado);font-weight:500;font-size:11pt}.punto.rosa i{width:16mm;height:16mm;background:var(--morado)}
.nota-mapa{position:absolute;left:6mm;bottom:5mm;width:44%;font-size:7pt;color:#8a7a88}
.lema-g{height:122mm}
.lema-panel{border-radius:5mm;padding:7mm;display:flex;flex-direction:column}
.lp-n{font-size:9pt;color:var(--morado);font-weight:500}.lp-v{font-weight:300;font-size:40pt;letter-spacing:-.02em;line-height:1.1;color:var(--morado)}
.lp-f{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:16pt;line-height:1.2;margin:2mm 0 auto}
.lp-i{display:flex;gap:4mm;margin:6mm 0 3mm}.lp-s{font-size:9pt}
.rueda{position:relative;width:150mm;height:150mm;align-self:center;justify-self:center}
.aro{position:absolute;left:10%;top:10%;width:80%;height:80%;border:1px solid #d9cfd6;border-radius:50%}
.rp{position:absolute;transform:translate(-50%,-50%);font-size:8pt;color:#8a7a88;text-align:center;width:30mm}
.rp i{display:block;width:3mm;height:3mm;border-radius:50%;background:#cfc6cd;margin:0 auto 1mm}
.rp.on{color:var(--morado);font-weight:500;font-size:10pt}.rp.on i{width:7mm;height:7mm;background:var(--morado)}
.rc{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.barras{margin:2mm 0 5mm}.br{display:grid;grid-template-columns:24mm 1fr 14mm;gap:3mm;align-items:center;margin:2mm 0;font-weight:500}
.br b{height:3.5mm;border-radius:2mm;background:#e8e0e5;position:relative;overflow:hidden}.br b i{position:absolute;top:0;bottom:0;left:0;border-radius:2mm}
.br em{font-style:normal;font-size:9pt;color:#6b5b68}
.mini{margin-bottom:4mm}.mini .card{padding:3.5mm 5mm}
.tpers{width:100%;border-collapse:collapse}.tpers td{border-bottom:1px solid #e3d8cc;padding:2.6mm 2mm;font-size:10pt}
.tpers .pn{font-weight:300;font-size:17pt;width:42mm}.tpers b{font-weight:500;margin-right:2mm}
.sl{display:grid;grid-template-columns:20mm 1fr 20mm;gap:3mm;align-items:center;font-size:9pt;margin:3mm 0}.sl span:last-child{text-align:right}
.sl b{height:1.6mm;border-radius:1mm;background:#e3d8cc;position:relative}.sl b i{position:absolute;top:50%;width:5mm;height:5mm;border-radius:50%;background:var(--morado);transform:translate(-50%,-50%)}
.g-voz{display:grid;grid-template-columns:.8fr 1.4fr;gap:12mm}
.vetadas{font-size:10pt;color:#a3262a;text-decoration:line-through}
.cab-bub p{font-weight:500;font-size:10pt;margin-bottom:2mm}
.bubs{gap:3mm}.bub{border-radius:4mm;padding:4mm 5mm;font-size:10pt;font-weight:500;min-height:21mm;display:flex;align-items:center}
.si-b{background:var(--lila)}.no-b{background:#F4E1E4;color:#6b2a2a;text-decoration:line-through;font-weight:400}
.canal{min-height:48mm}.cl{font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--morado);font-weight:500;margin-bottom:2mm}
.canal p:last-child{font-size:11.5pt;line-height:1.4}
.lienzo{border-radius:5mm;background:#fff}
.anat{position:relative}.et{position:absolute;background:var(--tinta);color:var(--marfil);font-size:8pt;padding:1mm 3mm;border-radius:10mm}
.g-simbolo{display:grid;grid-template-columns:1fr 1.2fr;gap:10mm;height:100%}.g-simbolo .card{margin-bottom:3mm}
.sistema{display:grid;grid-template-columns:1.5fr 1fr 1fr;grid-template-rows:64mm 64mm;gap:4mm}
.sb{border-radius:5mm;position:relative;display:flex;align-items:center;justify-content:center}
.sb.blanco{background:#fff}.sb.lila{background:var(--lila)}.sb.arena{background:var(--arena)}
.s-b{grid-row:span 2;grid-column:2}
.sl2{position:absolute;left:5mm;bottom:3mm;font-size:8pt;font-weight:500}
.avatar-m{width:32mm;height:32mm;border-radius:50%;background:var(--marfil);display:flex;align-items:center;justify-content:center}
.respeto{outline:1.2px dashed var(--arcilla);background:rgba(183,137,122,.08);position:relative}
.cota-t{position:absolute;left:6mm;top:4mm;font-size:8pt;color:var(--arcilla);font-weight:500}
.esc{display:flex;align-items:flex-end;justify-content:space-around;padding:10mm;height:96mm}.esc-i{text-align:center;font-size:8pt}.esc-c{height:38mm;display:flex;align-items:flex-end;justify-content:center;margin-bottom:3mm}
.vcol{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.vc{border-radius:4mm;height:60mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm;border:1px solid #eadfd3;font-size:8pt;padding:4mm;text-align:center}
.vc .grande{font-size:11pt;font-weight:500}
.rayas{background:repeating-linear-gradient(45deg,#fff 0 3mm,#f7eff5 3mm 6mm)}
.malos{gap:4mm}.mc{height:48mm;border-radius:4mm;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden}
.mal p{font-size:9pt;color:#a3262a;font-weight:500;margin-top:2mm}
.paleta{display:grid;grid-template-columns:repeat(7,1fr);gap:3.5mm}
.pc{border-radius:4mm;overflow:hidden;background:#fff}.pc-s{height:50mm;padding:4mm;position:relative}.pc-s p{font-weight:500;font-size:10.5pt;line-height:1.15}
.fijo{position:absolute;left:4mm;bottom:3mm;font-size:6.5pt;letter-spacing:.14em;border:1px solid currentColor;padding:.2mm 1.5mm;border-radius:5mm}
.pc-d{padding:3.5mm 4mm;font-size:8pt;min-height:50mm}.pc-d .proc{margin-top:2mm}.pc-d .uso{color:#6b5b68}
.mor-s{height:58mm;border-radius:4mm;margin-bottom:3mm}.mh{font-weight:500;font-size:13pt}.mor p{font-size:9pt}.mest{font-weight:500;color:#7a6a78}.mest.ok{color:#1d6b33}
.parejas{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}
.par{border-radius:5mm;overflow:hidden;position:relative;height:64mm;display:grid;grid-template-rows:1fr 1fr}
.par-a,.par-b{padding:4mm 6mm;text-align:center;display:flex;flex-direction:column;justify-content:center}.pe{font-size:7.5pt;text-align:left;position:absolute;left:5mm;top:3mm}
.pn2{font-size:14pt;font-weight:500}.par p{font-size:8.5pt;margin:0}
.pr{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#fff;color:var(--tinta);font-size:8pt;font-weight:500;padding:1mm 4mm;border-radius:10mm;white-space:nowrap}
.barra-xl{display:flex;height:84mm;border-radius:5mm;overflow:hidden;border:1px solid #e3d8cc}
.barra-xl div{display:flex;flex-direction:column;justify-content:flex-end;padding:4mm 3mm;font-size:8pt;min-width:0}.barra-xl b{font-weight:300;font-size:20pt;line-height:1}
.tipos .card{height:134mm}.card .mega{font-size:58pt;line-height:1.05;margin:3mm 0}.lic{font-size:8pt;color:#7a6a78;margin-top:3mm}
.lt-n{font-family:Jost;font-weight:300;font-size:30pt;letter-spacing:.01em;color:var(--marfil);margin:6mm 0 0}
.jer{border-top:1px solid #e3d8cc}.jr{display:grid;grid-template-columns:62mm 1fr;align-items:center;border-bottom:1px solid #e3d8cc;padding:2.6mm 0}
.jn{font-weight:500}.js{font-size:8pt;color:#7a6a78}
.g-super{display:grid;grid-template-columns:.85fr 1.3fr;gap:10mm;height:100%}.g-super .card{margin-bottom:3mm;padding:3.5mm 5mm}
.tiles{gap:4mm}.tile{border-radius:5mm;position:relative;overflow:hidden;height:82mm;border:1px solid #eadfd3}
.tt{position:absolute;z-index:2;left:6mm;top:5mm;font-weight:300;font-size:20pt;color:var(--morado)}
.iconos{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm 2mm}.ic{text-align:center;font-size:7pt;line-height:1.2}
.icc{display:inline-flex;width:13mm;height:13mm;border-radius:50%;background:var(--lila);align-items:center;justify-content:center;margin-bottom:1mm}
.icc.g{width:17mm;height:17mm;background:#fff;border:1px solid #e3d8cc}
.card .pm{font-weight:300;font-size:20pt}.pm i{color:var(--morado);font-style:normal;font-weight:600;margin:0 2mm}
.mood{position:absolute;inset:0;display:grid;grid-template-columns:1.15fr 1fr 1fr .95fr;grid-template-rows:1fr 1fr;gap:3mm;padding:3mm}
.mood>div{background-size:cover;background-position:center;border-radius:3mm;position:relative}
.mood span{position:absolute;left:4mm;bottom:3mm;background:rgba(247,242,235,.92);font-size:8pt;padding:.8mm 3mm;border-radius:10mm}
.m1{grid-row:span 2}.m2{grid-column:2;grid-row:1}.m3{grid-column:3;grid-row:1}.m4{grid-column:2;grid-row:2}.m5{grid-column:3;grid-row:2}.m6{grid-column:4;grid-row:1/span 2;background:var(--marfil);padding:9mm;display:flex;flex-direction:column;justify-content:center}.m6 h2{font-size:22pt}
.pasos{gap:4mm;margin-top:2mm}.pasos p{font-size:9pt}.pasos b{display:block;font-weight:300;font-size:20pt;color:var(--lila)}
.pap{display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:8mm;align-items:end;margin-top:4mm}
.pap-c{display:flex;flex-direction:column;align-items:center;gap:4mm}.pap-l{font-size:8.5pt;font-weight:500;text-align:center}
.tv{width:76mm;height:49mm;border-radius:1mm;box-shadow:0 2px 10px rgba(0,0,0,.14);position:relative;overflow:hidden}
.frente{background:#fff;display:flex;align-items:center;justify-content:center}.dorso{background:var(--marfil);padding:5mm 6mm}
.tn{font-weight:500;font-size:11pt}.tc{font-size:7pt;color:var(--morado);margin-bottom:3mm}.td{font-size:7pt;line-height:1.5}.td i{color:var(--morado);font-style:normal}
.carta{width:78mm;height:110mm;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.14);padding:9mm;position:relative;overflow:hidden}
.lineas{margin-top:12mm}.lineas i{display:block;height:1.5mm;background:#eee6e0;margin:2.5mm 0;border-radius:1mm}
.carta-pie{position:absolute;left:9mm;bottom:6mm;font-size:5pt;color:#7a6a78}
.vale{width:104mm;height:49mm;background:var(--lila);box-shadow:0 2px 10px rgba(0,0,0,.14);position:relative;overflow:hidden}
.vale-t{position:absolute;left:38mm;top:8mm;right:5mm}.lema-m{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:21pt;color:var(--morado);line-height:1.1;margin-bottom:2mm}
.peq{font-size:7.5pt}
.redes2{display:flex;gap:5mm;align-items:center}
.perfil{text-align:center;font-size:8pt}.avatar-r{width:30mm;height:30mm;border-radius:50%;background:var(--marfil);border:1px solid #e3d8cc;display:flex;align-items:center;justify-content:center;margin-bottom:2mm}
.post{width:56mm;height:70mm;border-radius:3mm;position:relative;overflow:hidden;padding:6mm;flex-shrink:0;box-shadow:0 1px 6px rgba(0,0,0,.08)}
.p-foto{background-size:cover;background-position:center}.pf-t{position:absolute;left:0;right:0;bottom:0;padding:6mm;background:linear-gradient(transparent,rgba(46,26,44,.78))}
.pt2{font-weight:300;font-size:19pt;line-height:1.1;color:var(--marfil)}.pt3{font-weight:300;font-size:14pt;line-height:1.2;margin-top:3mm}.firma-p{font-family:'Cormorant Garamond',serif;font-style:italic;color:var(--morado);font-size:13pt}
.story{width:40mm;height:71mm;border-radius:3mm;position:relative;overflow:hidden;box-shadow:0 1px 6px rgba(0,0,0,.08)}.story .pt2{color:var(--tinta);position:absolute;left:5mm;bottom:17mm;font-size:14pt}
.st-btn{position:absolute;left:5mm;bottom:7mm;background:var(--morado);color:#fff;font-size:7pt;padding:1mm 3mm;border-radius:10mm}
.dest{display:flex;gap:8mm;margin-top:7mm}.dest div{text-align:center;font-size:8pt}
.g-web{display:grid;grid-template-columns:2.2fr .8fr;gap:8mm;align-items:center}
.nav-m{border-radius:3mm;overflow:hidden;box-shadow:0 3px 14px rgba(0,0,0,.16);background:#fff}
.barra-n{background:#ece6ea;padding:2mm 3mm;display:flex;gap:1.5mm;align-items:center;font-size:7pt;color:#7a6a78}.barra-n i{width:2.5mm;height:2.5mm;border-radius:50%;background:#cfc4cb}.barra-n span{margin-left:4mm}
.web-h{display:flex;align-items:center;gap:6mm;padding:3mm 6mm;font-size:7pt;border-bottom:1px solid #eee}.web-h p{margin:0 0 0 auto}
.btn{display:inline-block;background:var(--morado);color:#fff;font-size:7.5pt;font-weight:500;padding:1.5mm 4mm;border-radius:10mm}
.web-hero{display:grid;grid-template-columns:1fr 1fr;background:var(--marfil);height:72mm}.web-hero>div:first-child{padding:9mm;display:flex;flex-direction:column;justify-content:center;gap:2mm;align-items:flex-start}
.wh1{font-weight:300;font-size:22pt;line-height:1.05;letter-spacing:-.02em}.web-f{background-size:cover;background-position:center}
.movil{display:flex;justify-content:center}.mv{width:52mm;height:100mm;border-radius:7mm;border:2.5mm solid var(--tinta);background:var(--marfil);overflow:hidden;text-align:center}
.mv-f{height:44mm;background-size:cover;background-position:center 20%}.wh2{font-weight:300;font-size:13pt;margin:3mm 0 2mm}
.firma2{display:flex;gap:5mm;background:#fff;border-radius:5mm;padding:5mm 6mm;font-size:8.5pt;align-items:center}.fn{font-weight:500;font-size:11pt}.lema-s{font-family:'Cormorant Garamond',serif;font-style:italic;color:var(--morado);font-size:11pt}
.espacio{align-items:end}.esp{display:flex;flex-direction:column;align-items:center;gap:4mm}
.placa{width:92mm;height:60mm;background:var(--marfil);box-shadow:0 3px 14px rgba(0,0,0,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm;border-radius:1mm;border:1px solid #e3d8cc}
.unif-w{position:relative;height:66mm}.unif{height:66mm}
.bolsa{width:48mm;height:60mm;background:#d9c3a3;position:relative;display:flex;align-items:center;justify-content:center;border-radius:1mm;margin-top:10mm}.asa{position:absolute;top:-10mm;left:13mm;width:22mm;height:14mm;border:2mm solid #b99e7c;border-bottom:none;border-radius:10mm 10mm 0 0}
.tcontr{width:100%;border-collapse:collapse}.tcontr td{border-bottom:1px solid #e3d8cc;padding:2.1mm 2mm;font-size:9.5pt}
.chip-c{display:inline-block;padding:1mm 4mm;border-radius:2mm;font-weight:500;font-size:8.5pt;border:1px solid rgba(0,0,0,.06)}
.tform{width:100%;border-collapse:collapse;margin-bottom:4mm}.tform td,.tform th{border-bottom:1px solid #e3d8cc;padding:2mm;font-size:9pt;text-align:left}.tform th{font-weight:500;font-size:7.5pt;letter-spacing:.12em;text-transform:uppercase}
.check{list-style:none}.check li{padding:2.4mm 0 2.4mm 8mm;border-bottom:1px solid #e3d8cc;position:relative;font-size:10pt}.check li::before{content:'';position:absolute;left:0;top:3mm;width:4mm;height:4mm;border:1.2px solid var(--morado);border-radius:1mm}
.contra{position:absolute;inset:0}.contra-t{position:absolute;left:22mm;top:50%;transform:translateY(-50%)}
.sin-pie .pie{display:none}
"""

def render():
    out = []
    for i, (cuerpo, seccion, fondo, oscuro, clase) in enumerate(PAGINAS, 1):
        bg = C.get(fondo, fondo)
        out.append(f'<section class="page {clase}{" oscuro-p" if oscuro else ""}" style="background:{bg}">{cuerpo}'
                   f'<div class="pie"><span>Rosa Ondoño · Manual de marca · v2.0 · Noviembre 2026</span><span>{seccion}</span><span>{i:02d}</span></div></section>')
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Manual de marca · Rosa Ondoño · v2.0</title>
<!-- Generado por manual/construir_manual.py · no editar a mano -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,400;1,500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(out)}</body></html>"""

with open(os.path.join(AQUI, "manual-de-marca.html"), "w") as f:
    f.write(render())
print("manual-de-marca.html:", len(PAGINAS), "páginas")
