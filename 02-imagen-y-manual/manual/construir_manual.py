"""Construye el manual de marca de Rosa Ondoño (HTML navegable y PDF).

Uso:  python3 construir_manual.py          -> manual-de-marca.html
      node exportar_pdf.js                 -> manual-de-marca.pdf

Los contrastes WCAG se calculan aquí, no se escriben a mano.
El isotipo se inserta SIEMPRE como el archivo original, sin modificarlo.
"""
import os, sys, html
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "identidad", "iconos"))
from generar import ICONOS, svg  # noqa: E402

LOGO = "../../assets/logo-original/LOGO-ROSA-ONDONO-solo.png"
FAVICON = "../../assets/logo-original/cropped-LOGO-ROSA-ONDONO-solo-32x32.png"

# ---------- color ----------
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + .05) / (y + .05)
def rgb(h): h = h.lstrip('#'); return ", ".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
def coma(n): return f"{n:.2f}".replace(".", ",")

PALETA = [  # (nombre, hex, rol, uso, proporción)
    ("Morado Rosa Ondoño", "#701B78", "Corporativo · fijo", "Isotipo, titulares de acento, botones, enlaces, sellos", "10–15 %"),
    ("Marfil", "#F7F2EB", "Fondo principal", "Fondo de web, papelería y señalética", "50–60 %"),
    ("Arena", "#E9DCCB", "Fondo secundario", "Bloques, tarjetas y universo «Conecta»", "15–20 %"),
    ("Lila empolvado", "#E8DAE6", "Acento suave", "Universo «Siente», vales regalo", "5–10 %"),
    ("Arcilla rosada", "#B7897A", "Acento decorativo", "Solo líneas, ilustración y fondos de foto. Nunca texto", "≤ 5 %"),
    ("Ciruela tinta", "#2E1A2C", "Texto", "Texto corrido y titulares", "—"),
    ("Blanco", "#FFFFFF", "Neutro", "Fondos de formulario, texto sobre morado", "—"),
]
APOYO = [  # Ruta B: solo para el universo de medicina estética
    ("Niebla", "#ECEAEE", "Fondo de fichas de medicina estética"),
    ("Salvia", "#A9B7A4", "Acento complementario (≤ 5 %), sin texto pequeño encima salvo morado o tinta"),
]

def matriz():
    cols = [p for p in PALETA]
    filas = "".join(
        "<tr><th>" + f'<span class="sw" style="background:{a[1]}"></span>{a[0]}' + "</th>" + "".join(
            (lambda r: f'<td class="{"aaa" if r >= 7 else "aa" if r >= 4.5 else "g" if r >= 3 else "no"}">{coma(r)}</td>')(ratio(a[1], b[1]))
            if a != b else '<td class="x">—</td>' for b in cols) + "</tr>" for a in cols)
    cab = "<tr><th>Texto ↓ / Fondo →</th>" + "".join(f"<th>{c[0]}</th>" for c in cols) + "</tr>"
    return f'<div class="scroll"><table class="matriz">{cab}{filas}</table></div>'

def icono(nombre, tam=40, color="var(--morado)"):
    t, cuerpo = ICONOS[nombre]
    return svg(cuerpo, t).replace('width="24" height="24"', f'width="{tam}" height="{tam}" style="color:{color}"')

def logo(h, alt="Isotipo de Rosa Ondoño", extra=""):
    return f'<img src="{LOGO}" alt="{alt}" style="height:{h}px;width:auto{extra}">'

def marca_vertical(h=150):
    return (f'<div class="lock v">{logo(h)}<div class="nombre" style="font-size:{h*.26:.0f}px">Rosa Ondoño</div>'
            f'<div class="lemaL" style="font-size:{h*.11:.0f}px">Cuídate · Conecta · Siente</div></div>')

def marca_horizontal(h=90):
    return (f'<div class="lock h">{logo(h)}<div><div class="nombre" style="font-size:{h*.42:.0f}px">Rosa Ondoño</div>'
            f'<div class="lemaL" style="font-size:{h*.17:.0f}px">Cuídate · Conecta · Siente</div></div></div>')

# ---------- secciones ----------
S = []
def sec(id_, num, titulo, cuerpo):
    S.append((id_, num, titulo, f'<section id="{id_}"><p class="num">{num}</p><h2>{titulo}</h2>{cuerpo}</section>'))

sec("uso", "00", "Cómo usar este manual", f"""
<p class="lead">Este manual recoge las reglas para que Rosa Ondoño se vea, se escriba y suene igual en todas partes: en la web, en las redes, en cabina, en el papel y en la calle.</p>
<div class="g2">
<div class="card"><h3>Lo que nunca cambia</h3><ul>
<li><strong>El isotipo.</strong> No se redibuja, deforma, recolorea ni lleva efectos.</li>
<li><strong>El color corporativo #701B78.</strong> Todo lo demás se construye a su alrededor.</li></ul></div>
<div class="card estado"><h3>Estado: borrador v1 · 17/11/2026</h3><ul>
<li>Base visual: <strong>Ruta A «Piel y luz»</strong> (la recomendada), con el tratamiento sobrio de la Ruta B en medicina estética. <em>Pendiente de aprobación.</em></li>
<li><span class="pend">PENDIENTE</span> logo vectorial (AI/EPS/SVG/PDF).</li>
<li><span class="pend">PENDIENTE</span> Pantone y CMYK oficiales.</li>
<li><span class="pend">PENDIENTE</span> confirmar el color oficial: #701B78 (icono) o #8E1F5C (web actual).</li>
<li><span class="pend">PENDIENTE</span> autorizar versiones monocromas y en negativo.</li></ul></div>
</div>
<p class="nota">Las piezas marcadas <span class="pend">PENDIENTE</span> o <span class="prop">PROPUESTA</span> no se usan en producción hasta que el cliente las apruebe. Las preguntas al cliente están en <code>estrategia/cuestionario-cliente.md</code>.</p>
""")

sec("esencia", "01", "Esencia", """
<p class="lead">Ayudamos a cada persona a cuidarse con conocimiento y con calma, para que se sienta bien en su cuerpo en cada etapa de su vida.</p>
<div class="g3">
<div class="card"><h3>Misión</h3><p>Escuchar, valorar y acompañar a cada persona con un plan propio que combina estética, terapias manuales y complementarias y medicina estética, explicando siempre qué hacemos, por qué y qué puede esperar.</p></div>
<div class="card"><h3>Visión</h3><p>Ser en Alicante la referencia del <strong>bienestar integral con criterio</strong>: el lugar al que se acude, y se recomienda, cuando se busca que te cuiden de verdad y que te digan la verdad.</p></div>
<div class="card"><h3>Historia</h3><p>Más de 30 años de oficio. Rosa empezó en el Hotel Sidi San Juan y se formó en Llongueras, naturopatía y terapias manuales. Médicos de Alicante, Madrid y Barcelona le han derivado pacientes para el drenaje postquirúrgico. <span class="pend">Validar con Rosa</span></p></div>
</div>
<h3>Valores</h3>
<table><tr><th>Valor</th><th>Significa</th><th>Se demuestra</th></tr>
<tr><td><strong>Criterio</strong></td><td>Recomendamos solo lo que tiene sentido para ti.</td><td>Valoración previa; «esto no lo necesitas».</td></tr>
<tr><td><strong>Cuidado</strong></td><td>Trato cercano, tiempo y detalle.</td><td>Citas sin prisas y seguimiento.</td></tr>
<tr><td><strong>Honestidad</strong></td><td>Expectativas realistas.</td><td>Sin promesas ni presión; precios claros.</td></tr>
<tr><td><strong>Oficio</strong></td><td>Más de 30 años de formación y práctica.</td><td>Profesionales con nombre y formación visible.</td></tr>
<tr><td><strong>Integración</strong></td><td>Piel, cuerpo y emoción, juntos.</td><td>Programas por necesidad.</td></tr>
<tr><td><strong>Serenidad</strong></td><td>Calma en el espacio y en la palabra.</td><td>Diseño con aire, cero urgencias.</td></tr></table>
<h3>Posicionamiento</h3>
<p class="cita">Bienestar integral con criterio: el único centro de Alicante que une estética, terapias manuales y complementarias y medicina estética supervisada, con una profesional con nombre propio que te dice lo que necesitas, y lo que no.</p>
<h3>El lema como estructura</h3>
<div class="g3">
<div class="card verbo"><p class="v">Cuídate</p><p><em>Saber qué necesitas es el primer cuidado.</em></p><p class="peq">Valoración integral · faciales · corporales · láser · medicina estética</p></div>
<div class="card verbo arena"><p class="v">Conecta</p><p><em>Tu cuerpo te habla. Aquí te ayudamos a escucharlo.</em></p><p class="peq">Masajes · drenaje · fisioterapia · osteopatía · terapias complementarias</p></div>
<div class="card verbo lila"><p class="v">Siente</p><p><em>Un tiempo solo para ti.</em></p><p class="peq">Rituales · circuito spa · tarjeta regalo</p></div>
</div>
<p class="nota"><strong>Reglas del lema:</strong> siempre en este orden, con punto medio ( · ) como separador y mayúscula inicial en cada verbo. No se añaden verbos ni se traduce. Cada verbo puede titular una sección o programa por sí solo.</p>
""")

sec("arquetipo", "02", "Arquetipo y personalidad", """
<div class="g2">
<div class="card"><p class="peq">PRIMARIO · ≈65 %</p><h3>El Cuidador</h3><p>Protege, acompaña y antepone la persona a la venta. Es lo que ya dicen las reseñas («como en casa», «Rosa en persona»). Encarna el verbo <em>Cuídate</em>.</p><p class="peq"><strong>Riesgo:</strong> volverse empalagoso. Lo equilibra el Sabio.</p></div>
<div class="card lila"><p class="peq">SECUNDARIO · ≈35 %</p><h3>El Sabio</h3><p>Valora, explica y dice la verdad. Aporta el <em>con criterio</em>, sostiene la credibilidad de la medicina estética y responde a lo que más pide el cliente: «que me expliquen».</p><p class="peq"><strong>Riesgo:</strong> frialdad técnica. Lo equilibra el Cuidador.</p></div>
</div>
<table><tr><th>Descartado</th><th>Por qué</th></tr>
<tr><td>Mago</td><td>Promete transformación: roza el «resultado garantizado», prohibido en publicidad sanitaria.</td></tr>
<tr><td>Amante</td><td>Sensualiza y acerca al cliché de spa. Lo sensorial queda como <em>rasgo</em>, no como arquetipo.</td></tr>
<tr><td>Inocente</td><td>Resta autoridad técnica a la medicina estética.</td></tr></table>
<h3>Personalidad</h3>
<div class="tags"><span>Cálida</span><span>Serena</span><span>Experta</span><span>Honesta</span><span>Sensorial</span><span>Discreta</span></div>
<p>Si Rosa Ondoño fuera una persona, sería una profesional serena y elegante sin ostentación, que te mira a los ojos, te escucha, te explica con palabras sencillas y te dice con cariño lo que de verdad te conviene.</p>
<table><tr><th>Somos</th><th>No somos</th></tr>
<tr><td>Cercanos</td><td>Confianzudos</td></tr><tr><td>Expertos</td><td>Técnicos o fríos</td></tr>
<tr><td>Elegantes</td><td>Ostentosos o «lujo»</td></tr><tr><td>Serenos</td><td>Aburridos</td></tr>
<tr><td>Sensoriales</td><td>Sensuales</td></tr><tr><td>Honestos</td><td>Promocionales</td></tr></table>
""")

sec("tono", "03", "Tono de comunicación", """
<h3>Cinco principios</h3>
<ol class="principios">
<li><strong>Cercana, no confianzuda.</strong> Tuteamos y hablamos como Rosa en cabina. Sin diminutivos, «guapa» ni «cari».</li>
<li><strong>Experta, no técnica.</strong> Cada término técnico va con su explicación sencilla.</li>
<li><strong>Honesta, no promocional.</strong> «Puede ayudarte a» en lugar de «conseguirás». Sin superlativos ni urgencias.</li>
<li><strong>Serena, no fría.</strong> Frases cortas y mucho aire. Ni exclamaciones en cadena ni emojis de cohete.</li>
<li><strong>Sensorial con medida.</strong> Texturas y calma solo en <em>Conecta</em> y <em>Siente</em>, nunca en medicina estética.</li></ol>
<h3>Registro por línea de servicio</h3>
<table><tr><th>Línea</th><th>Registro</th></tr>
<tr><td>Siente · rituales y regalo</td><td><span class="esc" style="--n:4"></span> Cercano y evocador</td></tr>
<tr><td>Conecta · terapias y masajes</td><td><span class="esc" style="--n:3"></span> Equilibrado</td></tr>
<tr><td>Cuídate · estética</td><td><span class="esc" style="--n:2"></span> Explicativo</td></tr>
<tr><td>Cuídate · medicina estética</td><td><span class="esc" style="--n:1"></span> Experto, sobrio, con profesional sanitario identificado</td></tr></table>
<h3>Decimos / No decimos</h3>
<table class="dnd"><tr><th>Decimos</th><th>No decimos</th><th>Motivo</th></tr>
<tr><td>Valoración, un plan para ti</td><td>Oferta, chollo, ¡últimas plazas!</td><td>Sin presión comercial</td></tr>
<tr><td>Puede ayudarte a, contribuye a</td><td>Resultados garantizados, 100 % seguro, sin efectos secundarios</td><td>Prohibido en publicidad sanitaria</td></tr>
<tr><td>Bienestar, alivio, relajación</td><td>Curar, poder curativo, tratar la ansiedad</td><td>Las terapias hablan de bienestar, no de curación</td></tr>
<tr><td>Naturalidad, que te reconozcas</td><td>Antiedad, quitar arrugas, corregir defectos</td><td>No fomentar inseguridad corporal</td></tr>
<tr><td>Cuidarte, tu piel, tu cuerpo</td><td>Oasis, experiencia transformadora, déjate mimar</td><td>Clichés de plantilla</td></tr>
<tr><td>El médico te valorará</td><td>«Tratamiento con [marca de toxina]»</td><td>No se publicitan medicamentos de prescripción</td></tr></table>
<div class="g2">
<div class="card"><h3>Vocabulario propio</h3><p>cuidar · escuchar · valorar · criterio · oficio · manos · plan · ritmo · calma · equilibrio · piel · natural · acompañar · tiempo</p><p class="peq">Con moderación: <em>ritual</em> (solo en Siente) y <em>energía</em> (solo en terapias, sin claims).</p></div>
<div class="card"><h3>Palabras vetadas</h3><p>garantizado · milagro · curativo · perfecto · eliminar para siempre · sin riesgo · oasis · transformación radical</p></div>
</div>
<h3>Ejemplos por canal</h3>
<div class="g2 ej">
<div class="card"><p class="canal">Web · portada</p><p><strong>Cuídate · Conecta · Siente</strong><br>Estética, terapias y medicina estética en el centro de Alicante. Con más de 30 años de oficio y el criterio de decirte lo que necesitas.</p></div>
<div class="card"><p class="canal">Web · ficha de medicina estética</p><p>Antes de cualquier tratamiento, el Dr. Roberth Bravo Pardo (médico estético, nº col. <span class="pend">PENDIENTE</span>) valora tu piel y te explica qué puedes esperar y qué cuidados necesitarás. Si no es para ti, te lo diremos.</p></div>
<div class="card"><p class="canal">Instagram · Conecta</p><p>Esa tensión en los hombros que ya ni notas. En una sesión de terapia miofascial trabajamos con las manos para ayudarte a soltar y a moverte con más libertad.</p></div>
<div class="card"><p class="canal">WhatsApp Business</p><p>Hola, Marta. Gracias por escribirnos. Para recomendarte bien, lo mejor es una valoración de 20 minutos en el centro. ¿Te viene bien el jueves a las 17:00?</p></div>
<div class="card"><p class="canal">Recepción y teléfono</p><p>«Centro Rosa Ondoño, buenos días, te atiende Laura. ¿En qué te puedo ayudar?»</p></div>
<div class="card"><p class="canal">Campaña · Navidad</p><p><strong>Regala tiempo.</strong> Tarjetas regalo para rituales y masajes en Maisonnave. <span class="peq">(Nunca de tratamientos médicos.)</span></p></div>
</div>
""")

x = 150 * 0.27
sec("logo", "04", "Logotipo", f"""
<div class="g2">
<div><h3>El isotipo</h3><p>Una figura humana abstracta de <strong>trazo continuo y grosor uniforme</strong>: círculo superior (cabeza), cuerpo en doble onda y círculo macizo inferior. Se lee como persona, fluidez, equilibrio y energía que recorre el cuerpo. Es la síntesis visual de <em>Cuídate · Conecta · Siente</em>.</p>
<p class="aviso"><strong>Intocable.</strong> El isotipo se usa siempre desde el archivo original. No se redibuja, no se deforma, no se recolorea y no lleva efectos.</p>
<p class="nota"><span class="pend">PENDIENTE</span> Solo existe en PNG de 233 × 315 px (web). Para imprenta, rotulación o tamaños grandes hace falta el vector original o un calco fiel aprobado por el cliente.</p></div>
<div class="fondo-claro centro">{logo(260)}</div></div>

<h3>Proporciones de referencia (medidas sobre el original)</h3>
<table><tr><th>Medida</th><th>Valor</th></tr>
<tr><td>Caja del isotipo (sin margen)</td><td>148 × 206 px en el original → proporción ancho:alto ≈ <strong>1 : 1,39</strong></td></tr>
<tr><td>Diámetro del círculo superior y del inferior</td><td>≈ 56 px en ambos, el <strong>27 % de la altura</strong>. Esta medida es el módulo <strong>x</strong> del sistema.</td></tr>
<tr><td>Grosor del trazo</td><td>≈ 4 % de la altura del isotipo</td></tr></table>

<h3>Versiones</h3>
<div class="g3 versiones">
<div class="card blanco centro">{marca_vertical(130)}<p class="peq"><strong>Principal vertical</strong> · <span class="prop">PROPUESTA</span><br>Para portada, papelería, vales y redes.</p></div>
<div class="card blanco centro">{marca_horizontal(70)}<p class="peq"><strong>Horizontal</strong> · <span class="prop">PROPUESTA</span><br>Para cabecera web, firma de email y rótulos alargados.</p></div>
<div class="card blanco centro">{logo(120)}<p class="peq"><strong>Isotipo solo</strong> · <span class="ok">VÁLIDO</span><br>Avatar de redes, favicon, sellos y relieve en seco.</p></div>
<div class="card blanco centro"><img src="{FAVICON}" alt="Favicon original" style="height:32px;image-rendering:auto"><p class="peq"><strong>Reducida / favicon</strong> · <span class="ok">VÁLIDO</span> (archivo original de 32 px)</p></div>
<div class="card centro pendbox"><p><strong>Monocromo positivo</strong><br>(isotipo en ciruela tinta)</p><p class="peq"><span class="pend">PENDIENTE</span> Cambia el color del icono: requiere autorización del cliente (P8) y el vector.</p></div>
<div class="card centro pendbox"><p><strong>Negativo</strong><br>(isotipo en blanco sobre morado)</p><p class="peq"><span class="pend">PENDIENTE</span> Igual que la anterior. Mientras no se autorice, el isotipo va siempre a color sobre fondo claro.</p></div>
</div>
<p class="nota"><span class="prop">PROPUESTA</span> El nombre «Rosa Ondoño» va compuesto en Cormorant Garamond 600 y el lema en cursiva. Si existe un logotipo tipográfico original (pregunta P3), se sustituye por él. En las composiciones solo cambia la relación entre isotipo y nombre: el isotipo no se altera.</p>

<h3>Área de respeto</h3>
<div class="g2"><div class="fondo-claro centro"><div class="respeto" style="padding:{x:.0f}px">{logo(150)}</div></div>
<div><p>Alrededor del isotipo se deja un margen libre igual a <strong>x</strong>, el diámetro del círculo superior (≈ 27 % de la altura del isotipo). En las versiones con nombre, el área de respeto se mide desde los bordes del conjunto.</p>
<p>Dentro de esa zona no puede haber texto, imágenes, bordes de página ni otros logotipos.</p>
<p>Separación entre isotipo y nombre: en la vertical, <strong>0,5 x</strong>; en la horizontal, <strong>0,75 x</strong>.</p></div></div>

<h3>Tamaños mínimos</h3>
<table><tr><th>Versión</th><th>Pantalla</th><th>Impresión</th></tr>
<tr><td>Isotipo solo</td><td>32 px de alto (el favicon de 16 px es una excepción técnica)</td><td>10 mm de alto</td></tr>
<tr><td>Horizontal</td><td>40 px de alto</td><td>12 mm de alto</td></tr>
<tr><td>Vertical con lema</td><td>120 px de alto (por debajo, sin lema)</td><td>30 mm de alto (por debajo, sin lema)</td></tr></table>
<p class="nota">Por debajo de estos tamaños el trazo pierde definición. El relieve en seco y la serigrafía piden un mínimo de 15 mm. Hay que validarlo en una prueba de imprenta con el vector.</p>

<h3>Fondos permitidos</h3>
<div class="fondos">
{''.join(f'<div class="fondo" style="background:{c}">{logo(70)}<p>{n}<br><span class="{"ok" if ratio("#701B78", c) >= 3 else "ko"}">{coma(ratio("#701B78", c))}:1 {"✔" if ratio("#701B78", c) >= 3 else "✖"}</span></p></div>' for n, c in [("Blanco","#FFFFFF"),("Marfil","#F7F2EB"),("Arena","#E9DCCB"),("Lila empolvado","#E8DAE6"),("Niebla","#ECEAEE")])}
</div>
<p>El isotipo es un elemento gráfico, así que necesita un contraste de al menos <strong>3:1</strong> con el fondo. Sobre fotografía, se coloca solo en zonas claras y uniformes (cielo, pared, lino) y nunca sobre zonas con detalle.</p>
<p class="aviso"><strong>Fondos prohibidos:</strong> ciruela tinta (1,63:1), grafito (1,70:1), salvia profunda (1,61:1), cualquier oscuro y el propio morado. Tampoco sobre el ciruela-magenta #8E1F5C (1,18:1).</p>

<h3>Usos incorrectos</h3>
<div class="incorrectos">
<div><div class="caja">{logo(80, "Uso incorrecto: deformado", ";transform:scaleX(1.6)")}</div><p>Estirar o deformar</p></div>
<div><div class="caja">{logo(80, "Uso incorrecto: girado", ";transform:rotate(25deg)")}</div><p>Girar o inclinar</p></div>
<div><div class="caja">{logo(80, "Uso incorrecto: recoloreado", ";filter:hue-rotate(150deg)")}</div><p>Cambiar el color</p></div>
<div><div class="caja">{logo(80, "Uso incorrecto: con sombra", ";filter:drop-shadow(4px 6px 4px rgba(0,0,0,.45))")}</div><p>Añadir sombras o efectos</p></div>
<div><div class="caja" style="background:#2E1A2C">{logo(80, "Uso incorrecto: fondo oscuro")}</div><p>Colocarlo sobre fondo oscuro</p></div>
<div><div class="caja" style="background:repeating-linear-gradient(45deg,#E9DCCB 0 8px,#B7897A 8px 16px)">{logo(80, "Uso incorrecto: fondo recargado")}</div><p>Colocarlo sobre fondo recargado</p></div>
<div><div class="caja">{logo(80, "Uso incorrecto: transparencia", ";opacity:.35")}</div><p>Aplicar transparencia</p></div>
<div><div class="caja"><div style="border:2px solid #701B78;border-radius:50%;padding:10px">{logo(60, "Uso incorrecto: encerrado")}</div></div><p>Encerrarlo en formas</p></div>
<div><div class="caja" style="position:relative">{logo(80, "Uso incorrecto: texto encima")}<span style="position:absolute;font-family:var(--serif);font-size:22px;color:#2E1A2C">Rosa Ondoño</span></div><p>Superponer texto o invadir el área de respeto</p></div>
<div><div class="caja pix"><img src="{FAVICON}" alt="Uso incorrecto: ampliado desde baja resolución" style="height:90px;image-rendering:pixelated"></div><p>Ampliar un archivo de baja resolución</p></div>
<div><div class="caja"><span style="font-family:var(--serif);font-size:20px;color:#701B78">∫ Rosa Ondoño</span></div><p>Redibujarlo, imitarlo o sustituirlo por un carácter</p></div>
<div><div class="caja">{logo(55, "Uso incorrecto: varios", ";transform:scaleX(-1)")}</div><p>Reflejarlo en espejo</p></div>
</div>
""")

filas_pal = "".join(f'<tr><td><span class="sw big" style="background:{h}"></span></td><td><strong>{n}</strong><br><span class="peq">{r}</span></td><td><code>{h}</code></td><td><code>{rgb(h)}</code></td><td>{"<span class=pend>PENDIENTE</span>" if h=="#701B78" else "Tras prueba de imprenta"}</td><td>{u}</td><td>{p}</td></tr>' for n, h, r, u, p in PALETA)
barra = "".join(f'<span style="background:{h};flex:{f}" title="{n}"></span>' for n, h, f in [("Marfil","#F7F2EB",55),("Arena","#E9DCCB",17),("Morado","#701B78",12),("Lila","#E8DAE6",7),("Ciruela tinta","#2E1A2C",6),("Arcilla","#B7897A",3)])
sec("color", "05", "Color", f"""
<div class="g2">
<div class="ficha-color"><div class="muestra" style="background:#701B78"></div>
<div><p class="peq">COLOR CORPORATIVO · NO MODIFICABLE</p><h3>Morado Rosa Ondoño</h3>
<table class="codigos"><tr><td>HEX</td><td><code>#701B78</code></td></tr><tr><td>RGB</td><td><code>112, 27, 120</code></td></tr>
<tr><td>HSL</td><td><code>295°, 63 %, 29 %</code></td></tr>
<tr><td>CMYK</td><td><span class="pend">PENDIENTE</span> (dato oficial de la imprenta)</td></tr>
<tr><td>Pantone</td><td><span class="pend">PENDIENTE</span> (dato oficial de la imprenta)</td></tr></table>
<p class="peq">HEX y RGB medidos en el PNG original del isotipo. No se publica una conversión CMYK automática porque varía según el papel y la imprenta: el valor de imprenta lo fija el cliente.</p></div></div>
<div class="card estado"><h3>Discrepancia por resolver</h3>
<div class="disc"><div><span style="background:#701B78"></span>#701B78<br>Isotipo · <em>hipótesis oficial</em></div><div><span style="background:#8E1F5C"></span>#8E1F5C<br>Web actual (49 usos)</div></div>
<p class="peq">Contraste entre ambos: <strong>{coma(ratio("#701B78", "#8E1F5C"))}:1</strong>. Juntos se confunden y ensucian la marca. Mientras el cliente no decida, <strong>#8E1F5C no se usa</strong> en piezas nuevas.</p></div></div>

<h3>Paleta completa · Ruta A «Piel y luz»</h3>
<div class="scroll"><table class="paleta"><tr><th></th><th>Color</th><th>HEX</th><th>RGB</th><th>CMYK / Pantone</th><th>Uso</th><th>Proporción</th></tr>{filas_pal}</table></div>

<h3>Apoyo para medicina estética (de la Ruta B)</h3>
<table>{''.join(f'<tr><td><span class="sw big" style="background:{h}"></span></td><td><strong>{n}</strong></td><td><code>{h}</code></td><td><code>{rgb(h)}</code></td><td>{u}</td><td>Morado sobre {n.lower()}: <strong>{coma(ratio("#701B78", h))}:1</strong></td></tr>' for n, h, u in APOYO)}</table>

<h3>Proporción de uso</h3>
<div class="barra">{barra}</div>
<p class="peq">Marfil 55 % · Arena 17 % · Morado 12 % · Lila 7 % · Ciruela tinta (texto) 6 % · Arcilla 3 %. El morado es la firma: si ocupa más del 20 % de una pieza, pierde valor.</p>

<h3>Contraste WCAG 2.2 de todas las combinaciones</h3>
<p class="peq">Leyenda: <span class="lg aaa">≥ 7 AAA</span> <span class="lg aa">≥ 4,5 AA texto</span> <span class="lg g">≥ 3 solo texto grande o gráfico</span> <span class="lg no">&lt; 3 prohibido</span></p>
{matriz()}

<h3>Combinaciones recomendadas</h3>
<div class="combos">
<div style="background:#F7F2EB;color:#2E1A2C">Texto en tinta<br>sobre marfil<br><b>{coma(ratio("#2E1A2C","#F7F2EB"))}</b></div>
<div style="background:#F7F2EB;color:#701B78">Titular en morado<br>sobre marfil<br><b>{coma(ratio("#701B78","#F7F2EB"))}</b></div>
<div style="background:#701B78;color:#fff">Blanco sobre morado<br>(botones y bandas)<br><b>{coma(ratio("#FFFFFF","#701B78"))}</b></div>
<div style="background:#E9DCCB;color:#701B78">Morado sobre arena<br><br><b>{coma(ratio("#701B78","#E9DCCB"))}</b></div>
<div style="background:#E8DAE6;color:#2E1A2C">Tinta sobre lila<br><br><b>{coma(ratio("#2E1A2C","#E8DAE6"))}</b></div>
<div style="background:#2E1A2C;color:#F7F2EB">Marfil sobre tinta<br>(pie de página)<br><b>{coma(ratio("#F7F2EB","#2E1A2C"))}</b></div>
</div>
<p class="nota">Tokens listos para desarrollo: <code>identidad/tokens/tokens.css</code> y <code>identidad/tokens/color.json</code>.</p>
""")

sec("tipografia", "06", "Tipografía", """
<p class="lead">Las seis familias de la web actual se sustituyen por dos.</p>
<div class="g2">
<div class="card blanco"><p class="peq">TITULARES</p><p style="font-family:var(--serif);font-size:56px;line-height:1;color:var(--morado)">Cormorant Garamond</p><p style="font-family:var(--serif);font-size:24px">Aa Bb Cc Ññ 0123456789 · <em>Cuídate · Conecta · Siente</em></p><p class="peq">Pesos: Medium 500 y SemiBold 600, más cursiva 500 para el lema. Es una serifa editorial de curvas amplias que dialoga con la onda del isotipo. <strong>Licencia SIL OFL</strong>: libre para web, impresión y rotulación.</p></div>
<div class="card blanco"><p class="peq">TEXTO E INTERFAZ</p><p style="font-family:var(--sans);font-size:48px;line-height:1.1">Jost</p><p style="font-family:var(--sans);font-size:20px">Aa Bb Cc Ññ 0123456789 · Pide tu valoración</p><p class="peq">Pesos: Regular 400 y Medium 500. Es una sans geométrica: su «o» circular repite los círculos del isotipo. <strong>Licencia SIL OFL</strong>.</p></div></div>
<h3>Jerarquía</h3>
<div class="jer">
<div><span>H1 · Cormorant 600 · 56/60 px (móvil 38)</span><p style="font-family:var(--serif);font-weight:600;font-size:56px;line-height:1.05">Bienestar con criterio</p></div>
<div><span>H2 · Cormorant 600 · 38/44 px (móvil 30)</span><p style="font-family:var(--serif);font-weight:600;font-size:38px">Tratamientos faciales</p></div>
<div><span>H3 · Jost 500 · 22/30 px</span><p style="font-family:var(--sans);font-weight:500;font-size:22px">¿Para quién es?</p></div>
<div><span>Antetítulo · Jost 500 · 13 px · mayúsculas · espaciado 0,16 em · morado</span><p style="font-family:var(--sans);font-weight:500;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--morado)">Cuídate · Medicina estética</p></div>
<div><span>Texto · Jost 400 · 18/29 px (móvil 17) · máximo 70 caracteres por línea</span><p style="font-family:var(--sans);font-size:18px;line-height:1.6;max-width:38em">Antes de cualquier tratamiento te valoramos y te explicamos qué puedes esperar, cuántas sesiones son orientativas y qué cuidados necesitarás después.</p></div>
<div><span>Lema · Cormorant cursiva 500</span><p style="font-family:var(--serif);font-style:italic;font-size:30px;color:var(--morado)">Cuídate · Conecta · Siente</p></div>
<div><span>Pie y legal · Jost 400 · 14 px</span><p style="font-family:var(--sans);font-size:14px">Nº de registro sanitario: PENDIENTE · Supervisión médica: Dr. Roberth Bravo Pardo.</p></div>
</div>
<table><tr><th>Entorno</th><th>Cómo</th></tr>
<tr><td>Web</td><td>WOFF2 servidos <strong>desde el propio servidor</strong> (no desde Google Fonts, por rendimiento y RGPD), solo en los pesos indicados y con <code>font-display: swap</code>.</td></tr>
<tr><td>Ofimática (Word, email, presupuestos)</td><td>Instalar las dos familias. Si no están disponibles: Georgia para titulares y Arial para texto.</td></tr>
<tr><td>Imprenta</td><td>Enviar los PDF con las fuentes incrustadas o el texto trazado.</td></tr>
<tr><td>Reglas</td><td>Cormorant nunca por debajo de 20 px ni en bloques largos. Nada de mayúsculas sostenidas en Cormorant. Sin subrayados decorativos.</td></tr></table>
""")

iconos_html = "".join(f'<div class="ico">{icono(k, 44)}<p>{v[0]}</p><code>icono-{k}.svg</code></div>' for k, v in ICONOS.items())
sec("iconografia", "07", "Iconografía", f"""
<p class="lead">Un set propio de iconos de línea para servicios, navegación y redes. Acompaña al isotipo, pero no lo imita.</p>
<div class="iconos">{iconos_html}</div>
<h3>Reglas de construcción</h3>
<div class="g2"><ul>
<li>Retícula de <strong>24 × 24</strong> con 2 px de margen interior.</li>
<li>Trazo único de <strong>1,5 px</strong> (≈ el 4 % que mide el trazo del isotipo), con extremos y uniones redondeados.</li>
<li>Sin rellenos, salvo puntos de detalle. Esquinas con radio de 2 px.</li>
<li>Color: morado o ciruela tinta. Sobre morado, en blanco.</li></ul>
<ul>
<li>Tamaños: 24 px en la interfaz, 32–48 px en tarjetas de servicio y 64 px en portadas de destacados.</li>
<li>Nunca se combinan con iconos de otros sets ni con emojis en titulares.</li>
<li><strong>Prohibido</strong> crear un icono que reproduzca o se parezca a la figura del isotipo.</li>
<li>En medicina estética no se usan jeringas ni agujas: el icono es el estetoscopio.</li></ul></div>
<p class="nota">Los archivos SVG están en <code>identidad/iconos/</code> y se regeneran con <code>generar.py</code>.</p>
<h3>Iconos por universo del lema</h3>
<div class="g3">
<div class="card"><p class="v2">Cuídate</p>{icono("valoracion",32)}{icono("facial",32)}{icono("corporal",32)}{icono("laser",32)}{icono("medicina",32)}</div>
<div class="card arena"><p class="v2">Conecta</p>{icono("masaje",32)}{icono("drenaje",32)}{icono("fisioterapia",32)}{icono("acupuntura",32)}</div>
<div class="card lila"><p class="v2">Siente</p>{icono("ritual",32)}{icono("regalo",32)}</div></div>
""")

sec("fotografia", "08", "Fotografía", """
<p class="lead">La luz de Alicante entrando por una ventana de Maisonnave a media mañana: piel real, manos que trabajan, materiales naturales.</p>
<div class="g2">
<div class="card"><h3>Sí</h3><ul>
<li>Luz natural lateral y cálida (4.500–5.000 K), con sombras suaves.</li>
<li>Personas reales de distintas edades, con piel con textura, poros y lunares.</li>
<li>Manos de Rosa y del equipo trabajando: el oficio es la prueba.</li>
<li>Lino, cerámica artesana, madera clara, papel de algodón y olivo.</li>
<li>Retratos con nombre de Rosa y del médico, mirando a cámara.</li>
<li>En medicina estética: consulta luminosa y conversación (valoración), no la aguja.</li>
<li>Postproducción: grano fino, saturación baja y blancos cálidos.</li></ul></div>
<div class="card"><h3>No</h3><ul>
<li>Piedras apiladas, orquídeas, velas y bambú de stock.</li>
<li>Pieles plastificadas o retoque que borre la textura.</li>
<li>Primeros planos de agujas, jeringas o productos médicos con marca.</li>
<li>Cuerpos sexualizados o planos que fomenten la inseguridad corporal.</li>
<li>Filtros de color o viñetas. El morado no se fuerza en la foto: lo pone el diseño.</li>
<li>Imágenes de stock reconocibles en portada.</li></ul></div></div>
<h3>Antes y después: protocolo obligatorio</h3>
<ol><li>Consentimiento informado <strong>por escrito</strong>, específico para la publicación y revocable.</li>
<li>Misma luz, encuadre, distancia, postura y fondo; sin maquillaje en ninguna de las dos.</li>
<li><strong>Sin retoque</strong> de ningún tipo. Se archivan los RAW originales.</li>
<li>Indicar el tratamiento, el número de sesiones y el tiempo transcurrido. Añadir «resultados variables según cada persona».</li>
<li>En medicina estética: revisar antes la normativa autonómica de publicidad sanitaria. Si hay dudas, no se publica.</li></ol>
""")

sec("graficos", "09", "Elementos gráficos", """
<div class="g2">
<div><h3>Punto medio</h3><p>El separador del lema ( · ) es el recurso gráfico propio: separa datos, navegación, categorías y firmas. Va siempre en morado.</p>
<p style="font-family:var(--serif);font-size:26px">Faciales <span style="color:var(--morado)">·</span> Corporales <span style="color:var(--morado)">·</span> Masajes</p>
<h3>Línea fina</h3><p>Filetes de 1 px en ciruela tinta al 20 % o en arcilla, para dividir contenido. Nunca hay curvas decorativas: <strong>la curva es solo del isotipo</strong>.</p><hr class="filete">
<h3>Bloques de color</h3><p>Rectángulos planos de marfil, arena o lila, sin degradados ni sombras. Esquinas rectas en el diseño y radio de 2 px solo en botones y tarjetas de interfaz.</p></div>
<div><h3>Retícula y aire</h3><p>Retícula de 12 columnas en la web y márgenes generosos en papel (mínimo 2 x). Como mínimo, el 40 % de cada pieza queda libre.</p>
<h3>Texturas</h3><p>Lino, papel de algodón y pared encalada, siempre <strong>fotografiadas</strong> y nunca generadas como patrón. Opacidad máxima del 15 % si van de fondo.</p>
<h3>Movimiento (web y reels)</h3><p>Transiciones lentas (400–600 ms) con fundidos y desplazamientos suaves. Sin rebotes ni giros. <strong>El isotipo no se anima</strong> ni se dibuja trazo a trazo sin el permiso del cliente. Se respeta <code>prefers-reduced-motion</code>.</p>
<p class="nota"><span class="prop">PROPUESTA</span> Usar el isotipo a gran escala recortado por el borde de la página, como marca de agua. Necesita aprobación expresa del cliente, porque altera su encuadre.</p></div></div>
""")

tarjeta = f"""<div class="tarjeta"><div class="t-front">{logo(70)}<p class="nombre" style="font-size:20px">Rosa Ondoño</p><p class="lemaL" style="font-size:10px">Cuídate · Conecta · Siente</p></div>
<div class="t-back"><p class="tn">Rosa Ondoño</p><p class="tc">Fundadora · Esteticista y terapeuta</p><p class="td">965 120 300 <span>·</span> 691 315 622<br>info@rosaondono.com<br>Av. Maisonnave 38, Entlo. Izq.<br>03003 Alicante<br><b>rosaondono.com</b></p></div></div>"""
vale = f"""<div class="vale"><div>{logo(60)}</div><div><p class="peq" style="letter-spacing:.16em">TARJETA REGALO · SIENTE</p><p style="font-family:var(--serif);font-size:30px;line-height:1.1">Regala tiempo</p><p class="peq">Para: ______________ · Ritual: ______________<br>Válida hasta: ________ · Nº ________</p></div></div>"""
firma = f"""<div class="firma"><img src="{LOGO}" alt="Rosa Ondoño" style="height:56px"><div><p style="font-family:var(--serif);font-size:20px;font-weight:600">Nombre Apellido</p><p>Recepción · Rosa Ondoño</p><p>965 120 300 · WhatsApp 691 315 622</p><p>Av. Maisonnave 38, Alicante · <span style="color:var(--morado)">rosaondono.com</span></p><p class="lemaL" style="font-size:13px">Cuídate · Conecta · Siente</p></div></div>"""
avatar = f'<div class="avatar">{logo(80)}</div>'
post = f"""<div class="post"><p class="peq" style="color:var(--morado);letter-spacing:.16em">CONECTA</p><p style="font-family:var(--serif);font-size:30px;line-height:1.1">Tu cuerpo te habla.<br>Aquí te ayudamos<br>a escucharlo.</p><div class="post-pie">{logo(28)}<span>@rosaondono</span></div></div>"""
story = "".join(f'<div class="dest">{icono(k, 30)}<p>{t}</p></div>' for k, t in [("valoracion","Valoración"),("facial","Facial"),("masaje","Masajes"),("ritual","Rituales"),("regalo","Regalo"),("ubicacion","Centro")])
placa = f"""<div class="placa">{logo(90)}<div><p class="nombre" style="font-size:34px">Rosa Ondoño</p><p class="peq" style="letter-spacing:.16em">ESTÉTICA · TERAPIAS · MEDICINA ESTÉTICA</p><p class="peq">Entresuelo izquierda · L–V 9:30–19:00 (verano; invierno <span class="pend">PENDIENTE</span>)</p><p class="peq">Nº registro sanitario: <span class="pend">PENDIENTE</span></p></div></div>"""
sec("aplicaciones", "10", "Aplicaciones", f"""
<p class="lead">Ejemplos de aplicación del sistema. Las artes finales de imprenta esperan al vector y a los valores CMYK.</p>
<h3>Tarjeta de visita · 85 × 55 mm</h3>{tarjeta}
<p class="peq">Anverso en marfil con el isotipo centrado. Reverso en blanco con los datos en Jost y el nombre en Cormorant. Papel de algodón de 600 g sin estucar, con el isotipo en tinta directa (Pantone <span class="pend">PENDIENTE</span>) o en relieve en seco.</p>
<h3>Tarjeta regalo · 210 × 99 mm</h3>{vale}
<p class="peq">Fondo lila empolvado, con sobre de color arena. <strong>Solo para estética, masajes y rituales</strong>: nunca tratamientos de medicina estética, por normativa sanitaria.</p>
<h3>Firma de email</h3>{firma}
<p class="peq">Nombre de ejemplo. HTML con el isotipo en PNG a 2× (112 px de alto, mostrado a 56 px). Sin banners promocionales ni citas inspiracionales.</p>
<h3>Redes sociales</h3>
<div class="redes">{avatar}{post}<div class="dests">{story}</div></div>
<p class="peq">Avatar: isotipo sobre círculo marfil, con un margen de 1 x. Posts 4:5 sobre marfil, arena o lila según el universo del lema. Portadas de destacados con los iconos del set sobre marfil.</p>
<h3>WhatsApp Business</h3>
<div class="g2"><div class="card"><p><strong>Foto de perfil:</strong> la misma que el avatar.<br><strong>Nombre:</strong> Rosa Ondoño · Estética y bienestar<br><strong>Descripción:</strong> Estética, terapias y medicina estética en Maisonnave, Alicante. Cuídate · Conecta · Siente.<br><strong>Horario:</strong> L–V 9:30–19:00 (invierno: <span class="pend">PENDIENTE</span>)</p></div>
<div class="card"><p><strong>Mensaje de bienvenida:</strong><br>«Hola, gracias por escribirnos. Te respondemos en horario de centro. Si nos cuentas qué te gustaría cuidar, te orientamos.»<br><strong>Fuera de horario:</strong> «Ahora el centro está cerrado; mañana a primera hora te escribimos.»</p></div></div>
<h3>Señalética · placa de portal (300 × 150 mm)</h3>{placa}
<p class="peq">Metacrilato mate o latón con impresión directa, fondo marfil e isotipo a color. El nº de registro sanitario es obligatorio en el exterior y en la publicidad de medicina estética.</p>
<h3>Uniformes</h3>
<div class="g2"><div class="card"><p><strong>Cabina:</strong> túnica de algodón o lino en arena o marfil, con el isotipo bordado en morado (25 mm) en el pecho izquierdo. El nombre de la persona va bordado en tinta debajo, en Jost.</p></div>
<div class="card"><p><strong>Medicina estética:</strong> bata blanca con el isotipo bordado y una placa con el nombre, la titulación y el nº de colegiado (<span class="pend">PENDIENTE</span>).</p></div></div>
<h3>Packaging y bolsa</h3>
<p>Bolsa de papel kraft blanqueado o color arena, con asas de algodón. Isotipo en tinta directa en una sola cara, nombre en la cara opuesta y nada más. Cajas de producto en marfil con etiqueta en relieve seco. Sin plastificados brillantes.</p>
<h3>Web</h3>
<p>Los tokens de color y tipografía están en <code>identidad/tokens/</code>. El capítulo digital completo (componentes, estados y accesibilidad) lo desarrolla <code>01-web</code> sobre este manual. Botón principal: fondo morado, texto blanco en Jost 500 y radio de 2 px. Foco visible: contorno de 2 px en ciruela tinta.</p>
""")

sec("formatos", "11", "Formatos de archivo", """
<table><tr><th>Formato</th><th>Color</th><th>Cuándo usarlo</th><th>Estado</th></tr>
<tr><td><strong>SVG</strong></td><td>RGB / HEX</td><td>Web, aplicaciones e interfaz: escala sin perder calidad</td><td><span class="pend">PENDIENTE</span> del vector</td></tr>
<tr><td><strong>PDF vectorial</strong></td><td>CMYK + tinta directa</td><td>Imprenta, papelería, vales y cartelería</td><td><span class="pend">PENDIENTE</span></td></tr>
<tr><td><strong>EPS / AI</strong></td><td>CMYK + Pantone</td><td>Rotulación, bordado, serigrafía, vinilo de corte y relieve</td><td><span class="pend">PENDIENTE</span></td></tr>
<tr><td><strong>PNG transparente</strong></td><td>RGB</td><td>Office, email, redes y presentaciones. Exportar a 2× y 3×</td><td>Solo el original de 233 × 315 px; los nuevos tamaños dependen del vector</td></tr>
<tr><td><strong>JPG</strong></td><td>RGB (sRGB)</td><td>Solo fotografía. Nunca para el logo (no admite transparencia)</td><td>—</td></tr>
<tr><td><strong>ICO / PNG 16–512</strong></td><td>RGB</td><td>Favicon e iconos de app</td><td>Hay originales de 32, 180, 192 y 270 px</td></tr></table>
<h3>RGB o CMYK</h3>
<p><strong>RGB/HEX</strong> se usa en todo lo que se ve en pantalla. <strong>CMYK o Pantone</strong> se usa en todo lo que se imprime. No se envía nunca a imprenta un archivo RGB, ni se publica en web uno CMYK. El morado es un color de gama difícil en CMYK: para piezas clave (tarjetas, placa, vales) se recomienda tinta directa Pantone.</p>
<h3>Nomenclatura de archivos</h3>
<p><code>rosaondono_[version]_[color]_[formato].[ext]</code> → p. ej. <code>rosaondono_vertical_color_rgb.svg</code>, <code>rosaondono_isotipo_color_cmyk.pdf</code></p>
<h3>Carpeta de entrega (cuando llegue el vector)</h3>
<pre>logo/
  rgb/   svg · png@1x · png@2x · png@3x
  cmyk/  pdf · eps
  pantone/ pdf · eps
  favicon/ ico · png 16–512</pre>
""")

sec("cumplimiento", "12", "Anexo · Checklist antes de publicar", """
<ul class="check">
<li>¿Se ha usado el isotipo original, sin modificar, sobre fondo claro y con su área de respeto?</li>
<li>¿El morado es #701B78 y ocupa menos del 20 %? ¿Se ha evitado el #8E1F5C?</li>
<li>¿Solo hay dos tipografías: Cormorant Garamond y Jost?</li>
<li>¿Todos los textos cumplen contraste AA?</li>
<li>¿El texto evita garantías, «curar», «seguro», urgencias y palabras vetadas?</li>
<li>Si es medicina estética: ¿aparece el profesional sanitario identificado y el nº de registro sanitario? ¿Se evitan las marcas de medicamentos?</li>
<li>¿Hay consentimiento escrito de cada persona que aparece en las fotos?</li>
<li>¿Lo ha revisado QA según <code>00-nucleo-marca/cumplimiento-legal.md</code>?</li></ul>
<h3>Control de versiones</h3>
<table><tr><th>Versión</th><th>Fecha</th><th>Cambios</th></tr>
<tr><td>v1 borrador</td><td>17/11/2026</td><td>Primera versión completa sobre la Ruta A. Pendientes: vector, Pantone/CMYK, color oficial y versiones monocromas.</td></tr></table>
""")

nav = "".join(f'<a href="#{i}"><span>{n}</span>{t}</a>' for i, n, t, _ in S)
CSS = """
:root{--morado:#701B78;--marfil:#F7F2EB;--arena:#E9DCCB;--lila:#E8DAE6;--arcilla:#B7897A;--tinta:#2E1A2C;
--serif:'Cormorant Garamond',Georgia,serif;--sans:'Jost','Helvetica Neue',Arial,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);color:var(--tinta);background:#fff;font-size:16.5px;line-height:1.6}
nav{position:fixed;top:0;left:0;bottom:0;width:250px;background:var(--marfil);padding:28px 22px;overflow:auto;border-right:1px solid #e6ddd2}
nav img{height:70px;margin-bottom:6px}
nav .nm{font-family:var(--serif);font-size:22px;font-weight:600}
nav .sub{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--morado);margin-bottom:22px}
nav a{display:block;color:var(--tinta);text-decoration:none;padding:5px 0;font-size:14.5px}
nav a span{display:inline-block;width:28px;color:var(--morado);font-size:12px}
nav a:hover,nav a:focus{color:var(--morado)}
main{margin-left:250px;max-width:1120px;padding:0 56px 80px}
.portada{min-height:92vh;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid #eee}
.portada h1{font-family:var(--serif);font-weight:600;font-size:64px;line-height:1.05;margin-top:30px}
section{padding:72px 0 40px;border-bottom:1px solid #eee}
.num{font-size:13px;letter-spacing:.18em;color:var(--morado);font-weight:500}
h2{font-family:var(--serif);font-weight:600;font-size:44px;line-height:1.1;margin:6px 0 26px}
h3{font-family:var(--serif);font-weight:600;font-size:26px;margin:34px 0 12px}
.card h3{margin-top:0}
p,ul,ol,table{margin-bottom:14px} ul,ol{padding-left:20px} li{margin:4px 0}
.lead{font-size:21px;max-width:46em}
.peq{font-size:13.5px} .nota{font-size:14px;background:var(--marfil);padding:12px 16px;border-left:3px solid var(--arcilla)}
.aviso{font-size:15px;padding:12px 16px;border-left:3px solid var(--morado);background:#fff}
.cita{font-family:var(--serif);font-size:26px;line-height:1.3;color:var(--morado);max-width:36em}
.g2{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px;margin-bottom:14px}
.g3{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-bottom:14px}
.card{background:var(--marfil);padding:22px 24px} .card.arena{background:var(--arena)} .card.lila{background:var(--lila)} .card.blanco{background:#fff;border:1px solid #eee}
.card.estado{background:#fff;border:1px solid var(--morado)}
.centro{text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
.fondo-claro{background:var(--marfil);padding:30px}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid rgba(0,0,0,.09);vertical-align:top}
th{font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
code{font-size:13px;background:#f3eef4;padding:1px 5px;border-radius:2px}
pre{background:var(--marfil);padding:14px;font-size:13px}
.pend{display:inline-block;background:#FCE8E6;color:#8A1C1C;font-size:11px;font-weight:500;letter-spacing:.06em;padding:1px 6px;border-radius:2px}
.prop{display:inline-block;background:#FFF4D6;color:#6B4E00;font-size:11px;font-weight:500;letter-spacing:.06em;padding:1px 6px;border-radius:2px}
.ok{color:#1d6b33;font-weight:500}.ko{color:#a3262a;font-weight:500}
.verbo .v,.v2{font-family:var(--serif);font-size:34px;font-weight:600;color:var(--morado);line-height:1.1;margin-bottom:6px}
.v2{font-size:26px} .card svg{margin:4px 6px 0 0}
.tags span{display:inline-block;border:1px solid var(--morado);color:var(--morado);padding:3px 12px;margin:0 6px 8px 0;font-size:14px}
.esc{display:inline-block;width:80px;height:8px;background:linear-gradient(90deg,var(--morado) calc(var(--n)*20%),#e6dfe8 0);margin-right:8px}
.ej .canal{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--morado);font-weight:500}
.lock{display:flex;align-items:center;color:var(--morado)} .lock.v{flex-direction:column;gap:6px} .lock.h{gap:18px;text-align:left}
.nombre{font-family:var(--serif);font-weight:600;color:var(--tinta);line-height:1.05;letter-spacing:.01em}
.lemaL{font-family:var(--serif);font-style:italic;color:var(--morado)}
.versiones .card{min-height:250px}
.pendbox{background:repeating-linear-gradient(45deg,#fff 0 10px,#faf6f9 10px 20px);border:1px dashed #c9a9c9}
.respeto{outline:2px dashed var(--arcilla);display:inline-block;background:rgba(183,137,122,.08);position:relative}
.respeto::after{content:'x';position:absolute;top:4px;left:8px;font-size:13px;color:var(--arcilla)}
.fondos{display:flex;gap:12px;flex-wrap:wrap}.fondo{padding:18px;text-align:center;width:160px;font-size:13px;border:1px solid #eee}
.incorrectos{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:16px}
.incorrectos .caja{height:140px;display:flex;align-items:center;justify-content:center;background:var(--marfil);position:relative;overflow:hidden}
.incorrectos .caja::after{content:'';position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - 1.5px),#C62828 calc(50% - 1.5px),#C62828 calc(50% + 1.5px),transparent calc(50% + 1.5px))}
.incorrectos p{font-size:13px;margin-top:6px}
.ficha-color{display:flex;gap:20px}.ficha-color .muestra{width:150px;min-height:240px;flex-shrink:0}
.codigos td{padding:4px 8px}
.disc{display:flex;gap:16px;margin:10px 0;font-size:13px}.disc span{display:block;width:120px;height:60px;margin-bottom:4px}
.sw{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:6px;border:1px solid rgba(0,0,0,.12)}.sw.big{width:44px;height:44px}
.barra{display:flex;height:46px;border:1px solid #eee;margin:8px 0}
.scroll{overflow-x:auto}
.matriz td,.matriz th{font-size:12.5px;text-align:center;padding:6px}.matriz th:first-child,.matriz tr th{text-align:left}
.aaa{background:#dff0e2}.aa{background:#eef6e6}.g{background:#fff4d6}.no{background:#fbe3e1;color:#8A1C1C}.x{background:#f5f5f5}
.lg{padding:2px 8px;margin-right:6px}
.combos{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}.combos div{padding:18px;font-size:14px;min-height:110px}
.combos b{font-size:22px;font-family:var(--serif)}
.jer>div{border-bottom:1px dashed #e5dde5;padding:10px 0}.jer span{font-size:12px;color:#7a6a78}
.iconos{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
.ico{background:var(--marfil);padding:18px 12px;text-align:center}.ico p{font-size:13px;margin:6px 0 2px}.ico code{font-size:10.5px}
hr.filete{border:0;border-top:1px solid rgba(46,26,44,.2);margin:14px 0}
.tarjeta{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:10px}
.t-front,.t-back{width:340px;height:220px;box-shadow:0 1px 6px rgba(0,0,0,.12)}
.t-front{background:var(--marfil);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px}
.t-back{background:#fff;padding:26px 28px}.tn{font-family:var(--serif);font-size:22px;font-weight:600}.tc{font-size:12px;color:var(--morado);margin-bottom:12px}.td{font-size:12px;line-height:1.55}.td span{color:var(--morado)}
.vale{display:flex;gap:28px;align-items:center;background:var(--lila);width:620px;max-width:100%;height:292px;padding:34px;box-shadow:0 1px 6px rgba(0,0,0,.12);margin-bottom:10px}
.firma{display:flex;gap:16px;border:1px solid #eee;padding:18px;max-width:520px;font-size:13px;line-height:1.45;margin-bottom:10px}
.redes{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start;margin-bottom:10px}
.avatar{width:150px;height:150px;border-radius:50%;background:var(--marfil);display:flex;align-items:center;justify-content:center;border:1px solid #eee}
.post{width:270px;height:338px;background:var(--arena);padding:28px;display:flex;flex-direction:column;justify-content:space-between}
.post-pie{display:flex;align-items:center;gap:8px;font-size:12px}
.dests{display:grid;grid-template-columns:repeat(3,84px);gap:12px}.dest{text-align:center;font-size:12px}.dest svg{background:var(--marfil);border-radius:50%;padding:18px;width:72px;height:72px;border:1px solid #eadfd3}
.placa{display:flex;gap:26px;align-items:center;background:var(--marfil);width:600px;max-width:100%;height:300px;padding:40px;box-shadow:0 2px 10px rgba(0,0,0,.15);margin-bottom:10px}
.check li{list-style:'☐  '}
@media (max-width:900px){nav{position:static;width:auto}main{margin-left:0;padding:0 22px}}
@media print{nav{display:none}main{margin:0;max-width:none;padding:0 10mm}section{page-break-before:always;padding-top:10mm}.portada{min-height:auto;padding:40mm 0}
.incorrectos .caja::after{-webkit-print-color-adjust:exact;print-color-adjust:exact}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Manual de marca · Rosa Ondoño (borrador v1)</title>
<!-- Generado por manual/construir_manual.py · no editar a mano -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<nav aria-label="Índice del manual"><img src="{LOGO}" alt="Isotipo de Rosa Ondoño"><p class="nm">Rosa Ondoño</p><p class="sub">Manual de marca · v1</p>{nav}</nav>
<main>
<header class="portada">{marca_vertical(200)}<h1>Manual de marca</h1><p class="lead">Identidad visual, verbal y aplicaciones · Borrador v1 · 17/11/2026</p>
<p class="peq">Departamento de Imagen y Manual: dirección de arte, diseño gráfico, marketing y comunicación, fotografía y QA.</p></header>
{''.join(s for *_, s in S)}
</main></body></html>"""

with open(os.path.join(AQUI, "manual-de-marca.html"), "w") as f:
    f.write(doc)
print("manual-de-marca.html generado:", len(S), "capítulos")
