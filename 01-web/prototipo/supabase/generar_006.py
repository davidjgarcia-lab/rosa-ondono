"""Genera 006_catalogo_web_actual.sql: incorpora al catálogo los servicios de las páginas de
rosaondono.com (descargadas el 26/11/2026) que aún no estaban, alinea nombres y añade las
preguntas frecuentes de cada área. Textos reescritos según cumplimiento-legal.md: sin garantizar
resultados, sin «permanente», sin efectos curativos ni sobre la salud emocional."""
from pathlib import Path
q = lambda v: "null" if v is None else ("true" if v is True else "false" if v is False else "'" + str(v).replace("'", "''") + "'")
R = "rosa-ondono"
nuevos = [  # slug, nombre, categoria, pilar, programa, tipo, resumen, para_quien
 ("reafirmacion-facial", "Reafirmación facial", "faciales", "cuidate", "rejuvenecimiento-facial", "estetica",
  "Un tratamiento de cabina para trabajar la firmeza y el tono de la piel del rostro. La piel se nota más suave y flexible, y lo combinamos con la rutina que necesites en casa.",
  "Si notas la piel del rostro menos firme o con menos tono."),
 ("piel-sensible", "Tratamiento para piel sensible", "faciales", "cuidate", "rejuvenecimiento-facial", "estetica",
  "Un facial suave y sin prisas para pieles que se enrojecen o se irritan con facilidad. Buscamos calmarla y cuidar su barrera protectora con productos elegidos para ella.",
  "Pieles reactivas, con rojeces o que toleran mal los cosméticos."),
 ("higiene-facial-detox", "Higiene facial detox", "faciales", "cuidate", "rejuvenecimiento-facial", "estetica",
  "Una limpieza a fondo que purifica la piel y le devuelve un aspecto fresco y luminoso. Ideal para empezar a cuidarte o para recuperar la piel tras una temporada de estrés.",
  "Pieles apagadas, con poros obstruidos o que piden una limpieza a fondo."),
 ("ojeras-y-parpados", "Ojeras y párpados", "faciales", "cuidate", "rejuvenecimiento-facial", "estetica",
  "Un tratamiento específico para el contorno de los ojos, la zona más fina del rostro. Ayuda a que la mirada se vea más descansada.",
  "Si las ojeras, las bolsas o el párpado cansado te preocupan."),
 ("tratamiento-acne", "Pieles con tendencia acneica", "faciales", "cuidate", "rejuvenecimiento-facial", "estetica",
  "Limpiamos, calmamos y equilibramos la piel con tendencia acneica, y te enseñamos a cuidarla en casa para que esté más limpia y uniforme. Si hace falta, te recomendamos ver a un dermatólogo.",
  "Pieles grasas o con granitos frecuentes."),
 ("remodelacion-corporal", "Remodelación corporal", "corporales", "cuidate", "silueta-y-piernas-ligeras", "estetica",
  "Un plan corporal a medida que combina aparatología y técnicas manuales para trabajar el contorno de tu cuerpo. Antes de empezar valoramos contigo qué es realista y cuántas sesiones tiene sentido hacer.",
  "Si quieres trabajar zonas concretas del contorno corporal sin cirugía."),
 ("masaje-deportivo", "Masaje deportivo", "masajes", "conecta", "dolor-y-tension", "terapia",
  "Un masaje intenso para preparar los músculos antes del esfuerzo o ayudarles a recuperarse después. Adaptamos la presión a tu deporte y a cómo llegas ese día.",
  "Personas que entrenan o hacen deporte con regularidad."),
 ("reflexologia-craneofacial", "Reflexología craneofacial", "masajes", "conecta", "equilibrio-emocional", "terapia",
  "Una técnica suave sobre la cabeza y el rostro para soltar la tensión acumulada. Muy relajante, ideal al final de una semana intensa.",
  "Si acumulas tensión en la cara, la mandíbula o la cabeza."),
]
renombres = {  # slug: (nombre nuevo, resumen nuevo o None)
 "tratamiento-facial-antiedad": ("Rejuvenecimiento facial", None),
 "masaje-relajante": ("Masaje relajante sedativo", None),
 "reflexologia": ("Reflexología podal", "Presión en puntos concretos de los pies, una técnica tradicional para relajar todo el cuerpo. Sales con las piernas ligeras y la cabeza más tranquila."),
 "armonizacion-facial": ("Full face", None),
 "depilacion-laser": ("Depilación láser diodo y alejandrita", "Trabajamos con láser de diodo y de alejandrita y elegimos el más adecuado según tu tipo de piel y de vello. Te explicamos cuántas sesiones calculamos para tu caso antes de empezar."),
}
sesiones = {"depilacion-laser": "Orientativo: entre 6 y 8 sesiones, cada 4 a 6 semanas, según piel, vello y zona"}
faqs = {  # categoría: [(pregunta, respuesta)]
 "faciales": [
  ("¿Cuánto dura un tratamiento facial?", "Entre 60 y 90 minutos, según el tratamiento."),
  ("¿Cuándo se notan los resultados?", "Algunos tratamientos se notan al salir de cabina y otros necesitan varias sesiones. Depende de tu piel y del objetivo, y te lo explicamos antes de empezar."),
  ("¿Cómo sé qué tratamiento es el mío?", "Lo mejor es empezar con una valoración. Miramos tu piel, hablamos de lo que te gustaría mejorar y te recomendamos solo lo que tiene sentido para ti.")],
 "corporales": [
  ("¿Cuánto dura un tratamiento corporal?", "Depende del tratamiento: entre 30 minutos y 2 horas."),
  ("¿Son molestos?", "Buscamos que sean cómodos. Algunos pueden dar una sensación leve de calor o presión, y siempre puedes pedirnos que paremos o ajustemos."),
  ("¿Cuándo empezaré a notar cambios?", "Cada persona es distinta. Hay quien nota la diferencia en las primeras sesiones y tratamientos que necesitan más tiempo. Te lo contamos con honestidad en la valoración."),
  ("¿Hay cuidados después?", "Sí. Según el tratamiento, te damos unas pautas sencillas para casa.")],
 "masajes": [
  ("¿Cuánto dura una sesión de masaje?", "Entre 60 y 90 minutos, según el masaje."),
  ("¿Puedo elegir el aceite o el aroma?", "Sí. Tenemos varios aceites y aromas y eliges el que más te apetezca."),
  ("¿Y si tengo alguna condición médica?", "Cuéntanoslo antes de la sesión. Adaptamos el masaje o, si no es buena idea, te lo diremos."),
  ("¿Hace falta reservar con antelación?", "Te lo recomendamos, sobre todo si quieres una hora concreta.")],
 "terapias-complementarias": [
  ("¿Qué es la acupuntura?", "Es una técnica de la medicina tradicional china que estimula puntos concretos del cuerpo con agujas muy finas. La usamos como apoyo a tu bienestar y no sustituye la atención médica."),
  ("¿En qué consisten las flores de Bach?", "Son esencias florales que se usan como acompañamiento emocional. Si estás pasando por un momento difícil, consulta también con un profesional de la salud."),
  ("¿Qué es la electroestimulación?", "Aplica corrientes de baja intensidad sobre los músculos para trabajarlos y ayudar a su recuperación."),
  ("¿Qué es la terapia manual?", "Técnicas con las manos sobre músculos y tejidos blandos para soltar tensión y ganar movilidad.")],
 "depilacion": [
  ("¿Cómo funciona la depilación láser?", "La luz del láser la absorbe el pigmento del vello y actúa sobre el folículo para reducir su crecimiento. Trabajamos con láser de diodo y de alejandrita."),
  ("¿Duele?", "Se nota algo de calor o un pequeño pinchazo, y la mayoría de personas lo tolera bien. Los equipos tienen sistemas de frío para que sea más cómodo."),
  ("¿Cuántas sesiones hacen falta?", "Depende de tu piel, del vello y de la zona. Como orientación, entre 6 y 8 sesiones cada 4 a 6 semanas."),
  ("¿Qué zonas se pueden tratar?", "Casi todas: piernas, axilas, ingles, espalda, pecho, brazos y rostro, entre otras.")],
 "medicina-estetica": [
  ("¿Por qué empezar con una consulta médica?", "Porque son actos médicos. El Dr. Roberth Bravo Pardo valora tu caso, te explica opciones, riesgos y alternativas, y decide contigo si el tratamiento está indicado."),
  ("¿Los resultados son iguales para todo el mundo?", "No. Cada persona responde de forma distinta y buscamos siempre un resultado natural. Ningún resultado se puede garantizar.")],
}
sql = ["-- 006 · Catálogo alineado con los servicios de rosaondono.com (26/11/2026) y FAQ por categoría",
       "alter table public.faqs alter column tratamiento_slug drop not null;",
       "alter table public.faqs add column if not exists categoria_slug text references public.categorias(slug);",
       "alter table public.faqs drop constraint if exists faqs_un_destino;",
       "alter table public.faqs add constraint faqs_un_destino check ((tratamiento_slug is null) <> (categoria_slug is null));",
       "grant select on public.faqs to anon;"]
for s, n, c, p, pr, t, r, pq in nuevos:
    sql.append(f"insert into public.tratamientos (slug, nombre, categoria_slug, pilar_slug, programa_slug, tipo, resumen, para_quien, profesional_slug, reservable, destacado, prioridad) values ({q(s)}, {q(n)}, {q(c)}, {q(p)}, {q(pr)}, {q(t)}, {q(r)}, {q(pq)}, {q(R)}, true, false, 3) on conflict (slug) do update set nombre = excluded.nombre, resumen = excluded.resumen, para_quien = excluded.para_quien;")
for s, (n, r) in renombres.items():
    sql.append(f"update public.tratamientos set nombre = {q(n)}" + (f", resumen = {q(r)}" if r else "") + f" where slug = {q(s)};")
for s, v in sesiones.items():
    sql.append(f"update public.tratamientos set sesiones = {q(v)} where slug = {q(s)};")
sql.append("delete from public.faqs where categoria_slug is not null;")
for c, lista in faqs.items():
    for i, (pr, re_) in enumerate(lista, 1):
        sql.append(f"insert into public.faqs (categoria_slug, pregunta, respuesta, orden) values ({q(c)}, {q(pr)}, {q(re_)}, {i});")
Path(__file__).with_name("006_catalogo_web_actual.sql").write_text("\n".join(sql) + "\n")
print(len(sql), "sentencias")
