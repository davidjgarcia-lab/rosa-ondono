"""Genera 002_semilla.sql con el catálogo de Rosa Ondoño (fuente: arquitectura-informacion.md §4-5).
Precios y duraciones: NULL (PENDIENTES del cliente). Textos con lenguaje de bienestar, sin promesas
de resultado ni claims de curación (cumplimiento-legal.md)."""
from pathlib import Path

def q(v):
    if v is None: return "null"
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"

def ins(tabla, cols, filas):
    vals = ",\n".join("(" + ", ".join(q(f.get(c)) for c in cols) + ")" for f in filas)
    return f"insert into public.{tabla} ({', '.join(cols)}) values\n{vals};\n"

pilares = [
 dict(slug="cuidate", nombre="Cuídate", color="marfil", orden=1, lema="Piel, cuerpo y medicina estética con criterio.",
      descripcion="Tratamientos faciales y corporales, depilación y belleza, y medicina estética con valoración médica. Te decimos lo que te conviene y lo que no."),
 dict(slug="conecta", nombre="Conecta", color="arena", orden=2, lema="Manos expertas para el cuerpo y la emoción.",
      descripcion="Masajes, drenaje linfático y terapias manuales y complementarias. Más de 30 años de oficio al servicio de tu bienestar."),
 dict(slug="siente", nombre="Siente", color="lila", orden=3, lema="Rituales para parar, y para regalar.",
      descripcion="Rituales individuales y en pareja, circuito spa y experiencias para desconectar en pleno centro de Alicante."),
]
programas = [
 dict(slug="rejuvenecimiento-facial", pilar_slug="cuidate", orden=1, nombre="Rejuvenecimiento facial", descripcion="Una piel cuidada en cada etapa, con resultados naturales: limpieza, luminosidad, firmeza y, si lo necesitas, medicina estética."),
 dict(slug="silueta-y-piernas-ligeras", pilar_slug="cuidate", orden=2, nombre="Silueta y piernas ligeras", descripcion="Tratamientos corporales sin cirugía para la retención de líquidos, la flacidez y la sensación de piernas cansadas."),
 dict(slug="belleza-esencial", pilar_slug="cuidate", orden=3, nombre="Belleza esencial", descripcion="Depilación láser, micropigmentación, manos y pies y maquillaje de ceremonia."),
 dict(slug="dolor-y-tension", pilar_slug="conecta", orden=1, nombre="Dolor y tensión", descripcion="Para la espalda, las cervicales y las contracturas del día a día: masaje terapéutico, terapia manual y técnicas de apoyo."),
 dict(slug="pre-y-postoperatorio", pilar_slug="conecta", orden=2, nombre="Pre y postoperatorio", descripcion="Acompañamos tu recuperación tras una cirugía estética con drenaje linfático manual, coordinado con las indicaciones de tu cirujano."),
 dict(slug="equilibrio-emocional", pilar_slug="conecta", orden=3, nombre="Equilibrio emocional", descripcion="Terapias complementarias para parar, escucharte y sentirte mejor. Complementan, nunca sustituyen, la atención médica o psicológica."),
 dict(slug="rituales-y-desconexion", pilar_slug="siente", orden=1, nombre="Rituales y desconexión", descripcion="Experiencias pensadas para bajar el ritmo, solo o en compañía."),
]
areas = [
 dict(slug="estetica", nombre="Estética", orden=1, titular="Tu piel y tu cuerpo, en buenas manos", descripcion="Tratamientos faciales y corporales, depilación láser y belleza. Te recomendamos lo que de verdad necesitas."),
 dict(slug="medicina-estetica", nombre="Medicina estética", orden=2, titular="Resultados naturales, con criterio médico", descripcion="Cada tratamiento empieza con una consulta con el médico, que valora tu caso y te explica opciones, riesgos y alternativas."),
 dict(slug="terapias", nombre="Terapias", orden=3, titular="Manos expertas para el cuerpo y la emoción", descripcion="Masajes, drenaje linfático y terapias manuales y complementarias, con más de 30 años de oficio."),
 dict(slug="bienestar", nombre="Bienestar", orden=4, titular="Rituales para parar", descripcion="Experiencias para desconectar, solo o en compañía, en pleno centro de Alicante."),
]
categorias = [
 dict(slug="faciales", nombre="Faciales", icono="facial", orden=1, area_slug="estetica"),
 dict(slug="corporales", nombre="Corporales", icono="corporal", orden=2, area_slug="estetica"),
 dict(slug="masajes", nombre="Masajes y drenaje", icono="masaje", orden=3, area_slug="terapias"),
 dict(slug="terapias-complementarias", nombre="Terapias complementarias", icono="acupuntura", orden=4, area_slug="terapias"),
 dict(slug="depilacion", nombre="Depilación", icono="laser", orden=5, area_slug="estetica"),
 dict(slug="belleza", nombre="Belleza", icono="facial", orden=6, area_slug="estetica"),
 dict(slug="medicina-estetica", nombre="Medicina estética", icono="medicina", orden=7, area_slug="medicina-estetica"),
 dict(slug="rituales", nombre="Rituales", icono="ritual", orden=8, area_slug="bienestar"),
 dict(slug="valoracion", nombre="Valoración", icono="valoracion", orden=0, area_slug=None),
]
profesionales = [
 dict(slug="rosa-ondono", nombre="Rosa Ondoño", cargo="Fundadora · esteticista y terapeuta", sanitario=False,
      bio="Más de 30 años de oficio. Empezó en el Hotel Sidi San Juan y se formó en Llongueras (Barcelona) y en naturopatía y terapias manuales en Madrid. Médicos de Alicante, Madrid y Barcelona le han confiado durante años a sus pacientes para el drenaje postquirúrgico."),
 dict(slug="dr-roberth-bravo-pardo", nombre="Dr. Roberth Bravo Pardo", cargo="Médico estético y nutricionista", sanitario=True, num_colegiado=None,
      bio="Responsable de la medicina estética del centro. Cada tratamiento médico empieza con una consulta en la que valora tu caso, te explica opciones, riesgos y alternativas, y decide contigo si está indicado."),
]

# (slug, nombre, cat, pilar, programa, tipo, prof, prioridad, destacado, resumen, revision)
R, D = "rosa-ondono", "dr-roberth-bravo-pardo"
T = [
 ("valoracion-integral","Valoración integral","valoracion","cuidate",None,"estetica",R,1,True,"Empieza por aquí. Hablamos de lo que te gustaría mejorar, analizamos piel, cuerpo y hábitos, y te llevas un plan personalizado por escrito.",None),
 ("limpieza-facial-profunda","Limpieza facial profunda","faciales","cuidate","rejuvenecimiento-facial","estetica",R,1,True,"Limpieza en profundidad adaptada a tu tipo de piel, con extracción cuidadosa, mascarilla e hidratación final.",None),
 ("tratamiento-facial-antiedad","Tratamiento facial antiedad","faciales","cuidate","rejuvenecimiento-facial","estetica",R,2,False,"Protocolo de cabina para una piel más luminosa y con mejor aspecto, combinando activos y técnicas según tu piel.",None),
 ("hidratacion-facial","Hidratación facial","faciales","cuidate","rejuvenecimiento-facial","estetica",R,3,False,"Tratamiento de cabina para pieles deshidratadas o apagadas, con mascarilla y masaje facial.",None),
 ("peeling-facial","Peeling facial","faciales","cuidate","rejuvenecimiento-facial","estetica",R,2,False,"Renovación de la capa superficial de la piel para mejorar textura y luminosidad. Siempre tras valorar tu piel.",None),
 ("microdermoabrasion","Microdermoabrasión","faciales","cuidate","rejuvenecimiento-facial","estetica",R,3,False,"Exfoliación mecánica suave que ayuda a afinar la textura de la piel.",None),
 ("radiofrecuencia-facial","Radiofrecuencia facial","faciales","cuidate","rejuvenecimiento-facial","estetica",R,1,False,"Aparatología que calienta las capas profundas de la piel para trabajar la firmeza. Te explicamos sus contraindicaciones antes de empezar.","Retirar el claim «seguro» de la web actual"),
 ("dermapen","Dermapen","faciales","cuidate","rejuvenecimiento-facial","estetica",R,1,True,"Microneedling con dispositivo para estimular la renovación de la piel y mejorar su textura.",None),
 ("tratamiento-reductor","Tratamiento reductor","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,2,False,"Plan corporal sin cirugía que combina técnicas manuales y aparatología según la zona y tus objetivos.",None),
 ("tratamiento-anticelulitico","Tratamiento anticelulítico","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,1,False,"Protocolo para mejorar el aspecto de la piel con celulitis, combinando drenaje, aparatología y pautas de hábitos.",None),
 ("reafirmacion-corporal","Reafirmación corporal","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,2,False,"Tratamiento para trabajar la flacidez de abdomen, brazos o piernas.",None),
 ("presoterapia","Presoterapia","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,1,True,"Botas de presión secuencial que favorecen el retorno venoso y linfático. Muy agradable para la sensación de piernas cansadas.",None),
 ("vacumterapia","Vacumterapia","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,3,False,"Técnica de succión controlada que se combina con otros tratamientos corporales.",None),
 ("cavitacion","Cavitación","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,1,False,"Ultrasonidos de baja frecuencia aplicados a zonas concretas, dentro de un plan corporal.",None),
 ("radiofrecuencia-corporal","Radiofrecuencia corporal","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,2,False,"Calor profundo para trabajar la firmeza de la piel del cuerpo.",None),
 ("lipolaser","Lipoláser","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,3,False,"Láser de baja potencia que se integra en planes corporales.",None),
 ("detox-integral","Detox integral","corporales","cuidate","silueta-y-piernas-ligeras","estetica",R,3,False,"Combinación de drenaje, exfoliación y envoltura para una sensación de ligereza.",None),
 ("aranas-vasculares","Arañas vasculares","corporales","cuidate","silueta-y-piernas-ligeras","estetica",None,3,False,"Tratamiento de pequeñas venitas superficiales en piernas o rostro.","Confirmar técnica: si es esclerosis o láser vascular, pasa a medicina estética"),
 ("masaje-relajante","Masaje relajante","masajes","siente","rituales-y-desconexion","terapia",R,2,False,"Masaje de ritmo lento para soltar tensión y desconectar.",None),
 ("masaje-terapeutico","Masaje terapéutico","masajes","conecta","dolor-y-tension","terapia",R,2,False,"Masaje enfocado en las zonas con más carga, adaptado a lo que te cuentes al empezar.",None),
 ("masaje-descontracturante","Masaje descontracturante","masajes","conecta","dolor-y-tension","terapia",R,1,True,"Trabajo profundo sobre contracturas de espalda, cuello y hombros.",None),
 ("masaje-ayurvedico","Masaje ayurvédico","masajes","conecta","equilibrio-emocional","terapia",R,3,False,"Masaje con aceites templados inspirado en la tradición ayurvédica.",None),
 ("drenaje-linfatico","Drenaje linfático manual","masajes","conecta","pre-y-postoperatorio","terapia",R,1,False,"Técnica manual suave que favorece la circulación linfática. Indicado, por ejemplo, para la retención de líquidos.",None),
 ("drenaje-linfatico-postoperatorio","Drenaje linfático postoperatorio","masajes","conecta","pre-y-postoperatorio","terapia",R,1,True,"Acompañamos tu recuperación tras una cirugía estética con drenaje linfático manual, coordinado con las indicaciones de tu cirujano.",None),
 ("linfodrenaje-energetico","Linfodrenaje energético","masajes","conecta","equilibrio-emocional","terapia",R,3,False,"Drenaje suave con un enfoque de relajación profunda.",None),
 ("reflexologia","Reflexología podal y craneofacial","masajes","conecta","equilibrio-emocional","terapia",R,3,False,"Presiones en pies o rostro para una sesión de relajación profunda.",None),
 ("fisioterapia","Fisioterapia","terapias-complementarias","conecta","dolor-y-tension","terapia",None,3,False,"Valoración y tratamiento por fisioterapeuta colegiado.","Confirmar el fisioterapeuta colegiado que la realiza (profesión sanitaria)"),
 ("osteopatia","Osteopatía","terapias-complementarias","conecta","dolor-y-tension","terapia",None,2,False,"Terapia manual global para la movilidad y la tensión.","Confirmar quién la realiza"),
 ("acupuntura","Acupuntura","terapias-complementarias","conecta","equilibrio-emocional","terapia",R,1,False,"Terapia de la medicina tradicional china con agujas finas, como complemento de bienestar.",None),
 ("moxibustion","Moxibustión","terapias-complementarias","conecta","equilibrio-emocional","terapia",R,3,False,"Aplicación de calor con moxa, de la medicina tradicional china.",None),
 ("terapia-somatoemocional","Terapia somatoemocional","terapias-complementarias","conecta","equilibrio-emocional","terapia",R,3,False,"Trabajo corporal suave que ayuda a tomar conciencia de la relación entre tensión y emoción.",None),
 ("terapia-craneosacral","Terapia craneosacral","terapias-complementarias","conecta","equilibrio-emocional","terapia",R,3,False,"Técnica manual muy suave orientada a la relajación profunda.",None),
 ("terapia-miofascial","Terapia miofascial","terapias-complementarias","conecta","dolor-y-tension","terapia",R,3,False,"Trabajo manual sobre la fascia para liberar tensiones.",None),
 ("terapia-manual","Terapia manual","terapias-complementarias","conecta","dolor-y-tension","terapia",R,3,False,"Técnicas manuales adaptadas a cada persona.",None),
 ("magnetoterapia","Magnetoterapia","terapias-complementarias","conecta","dolor-y-tension","terapia",R,3,False,"Aparatología de campos magnéticos como apoyo en sesiones de bienestar.","Retirar el claim «estimula la curación» de la web actual"),
 ("electroestimulacion","Electroestimulación","terapias-complementarias","conecta","dolor-y-tension","terapia",R,3,False,"Estimulación eléctrica muscular como apoyo a otros tratamientos.",None),
 ("onda-corta","Onda corta","terapias-complementarias","conecta","dolor-y-tension","terapia",R,3,False,"Calor profundo mediante aparatología.",None),
 ("balneoterapia","Balneoterapia","terapias-complementarias","siente","rituales-y-desconexion","terapia",R,3,False,"Sesiones con agua y temperatura para relajarte.",None),
 ("flores-de-bach","Flores de Bach","terapias-complementarias","conecta","equilibrio-emocional","terapia",R,3,False,"Acompañamiento con esencias florales como complemento de bienestar. No sustituye la atención médica ni psicológica.","Retirar el claim sobre ansiedad y depresión de la web actual"),
 ("depilacion-laser","Depilación láser","depilacion","cuidate","belleza-esencial","estetica",R,1,True,"Láser de alejandrita y diodo según tu tipo de piel y vello. Valoramos tu caso antes de la primera sesión.",None),
 ("depilacion-skins-brazilian","Depilación Skin's Brazilian","depilacion","cuidate","belleza-esencial","estetica",R,3,False,"Depilación con cera de baja temperatura.",None),
 ("micropigmentacion","Micropigmentación","belleza","cuidate","belleza-esencial","estetica",R,1,False,"Cejas, labios o ojos con un resultado natural, diseñado contigo antes de empezar.",None),
 ("micropigmentacion-oncologica","Micropigmentación oncológica","belleza","cuidate","belleza-esencial","estetica",R,1,False,"Reconstrucción de cejas o areola tras un tratamiento oncológico, con calma y en un espacio privado.",None),
 ("manicura-y-pedicura","Manicura y pedicura","belleza","cuidate","belleza-esencial","estetica",R,3,False,"Cuidado de manos y pies.",None),
 ("maquillaje-de-ceremonia","Maquillaje de ceremonia","belleza","cuidate","belleza-esencial","estetica",R,2,False,"Maquillaje para bodas y eventos, con prueba previa.",None),
 ("consulta-medica","Consulta de medicina estética","medicina-estetica","cuidate",None,"medico",D,1,True,"El primer paso de cualquier tratamiento médico. El médico valora tu caso, te explica opciones, riesgos y alternativas, y decide contigo si hay indicación.",None),
 ("armonizacion-facial","Armonización facial","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,2,False,"Abordaje global del rostro con varias técnicas médicas, planificado tras la consulta.",None),
 ("hilos-tensores","Hilos tensores","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,1,False,"Procedimiento médico con hilos reabsorbibles para la flacidez facial leve o moderada.",None),
 ("aumento-de-pomulos","Pómulos","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,2,False,"Tratamiento médico para proyectar o recuperar volumen en el pómulo.",None),
 ("rinomodelacion","Rinomodelación","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,1,False,"Corrección médica de pequeñas irregularidades de la nariz sin cirugía.",None),
 ("menton","Mentón","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,2,False,"Tratamiento médico para definir o proyectar el mentón.",None),
 ("marcado-mandibular","Marcado mandibular","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,2,False,"Definición médica del contorno mandibular.",None),
 ("flacidez-facial","Flacidez facial","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,2,False,"Opciones médicas para la pérdida de firmeza del rostro, valoradas en consulta.",None),
 ("flacidez-corporal","Flacidez corporal","medicina-estetica","cuidate","silueta-y-piernas-ligeras","medico",D,2,False,"Opciones médicas para la flacidez de abdomen, brazos o muslos.",None),
 ("hidratacion-facial-medica","Hidratación facial médica","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,3,False,"Infiltraciones hidratantes realizadas por el médico.",None),
 ("bioestimulacion-de-colageno","Bioestimulación de colágeno","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,1,False,"Tratamiento médico que estimula la producción propia de colágeno.",None),
 ("aumento-de-labios","Aumento de labios","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,1,True,"Tratamiento médico para hidratar, perfilar o dar volumen a los labios buscando un resultado natural.",None),
 ("arrugas-de-expresion","Arrugas de expresión","medicina-estetica","cuidate","rejuvenecimiento-facial","medico",D,1,False,"Tratamiento médico de las arrugas dinámicas del tercio superior del rostro. Información sanitaria, sin marcas comerciales.","Validación legal previa a publicar (medicamento de prescripción)"),
 ("ritual-en-pareja","Ritual en pareja","rituales","siente","rituales-y-desconexion","terapia",R,1,True,"Una experiencia para dos en el mismo espacio, a vuestro ritmo.",None),
 ("ritual-individual","Ritual individual","rituales","siente","rituales-y-desconexion","terapia",R,2,False,"Un tiempo solo para ti que combina masaje y cuidado de la piel.",None),
 ("circuito-spa","Circuito spa","rituales","siente","rituales-y-desconexion","terapia",R,2,False,"Agua, calor y descanso para desconectar.",None),
 ("experiencia-beauty","Experiencia Beauty","rituales","siente","rituales-y-desconexion","estetica",R,3,False,"Facial y cuidado de manos en una misma visita.",None),
]
cols = ["slug","nombre","categoria_slug","pilar_slug","programa_slug","tipo","profesional_slug","prioridad","destacado","resumen","revision_pendiente","reservable","sesiones"]
trat = []
for s,n,c,p,pr,t,prof,prio,dest,res,rev in T:
    trat.append(dict(slug=s,nombre=n,categoria_slug=c,pilar_slug=p,programa_slug=pr,tipo=t,profesional_slug=prof,prioridad=prio,
        destacado=dest,resumen=res,revision_pendiente=rev,reservable=(t!="medico" and prof is not None) or s=="consulta-medica",
        sesiones="Tras la consulta médica" if t=="medico" else "Orientativo: se concreta en tu valoración"))

faqs = [
 ("drenaje-linfatico-postoperatorio","¿Cuándo puedo empezar después de la operación?","Cuando lo indique tu cirujano. Tráenos su pauta y organizamos las sesiones con ella.",1),
 ("drenaje-linfatico-postoperatorio","¿Cuántas sesiones voy a necesitar?","Depende de la cirugía y de cómo evoluciones. Te damos una pauta orientativa en la primera sesión y la revisamos contigo.",2),
 ("drenaje-linfatico-postoperatorio","¿Es doloroso?","Es una técnica manual suave. Si alguna zona está sensible, adaptamos la presión.",3),
 ("depilacion-laser","¿Cuántas sesiones se necesitan?","Varía según la zona, el tipo de vello y la piel. Lo valoramos antes de empezar y te damos una estimación orientativa.",1),
 ("depilacion-laser","¿Sirve para todo tipo de piel?","Trabajamos con alejandrita y diodo para adaptarnos a distintos fototipos. En la valoración vemos cuál conviene en tu caso.",2),
 ("depilacion-laser","¿Duele?","Se nota una sensación de calor breve. Depende de la zona y de cada persona.",3),
 ("aumento-de-labios","¿Puedo reservar el tratamiento directamente?","No. Como todo acto médico, empieza con una consulta en la que el médico valora si está indicado y te explica riesgos y alternativas.",1),
 ("aumento-de-labios","¿Se va a notar?","El objetivo es un resultado natural y proporcionado. Lo hablaréis en la consulta antes de decidir nada.",2),
 ("aumento-de-labios","¿Tiene riesgos?","Sí, como cualquier tratamiento médico. El médico te los explica en consulta y firmarás un consentimiento informado.",3),
 ("valoracion-integral","¿Qué incluye?","Una conversación sobre lo que te gustaría mejorar, un análisis de piel, cuerpo y hábitos, y un plan por escrito.",1),
 ("valoracion-integral","¿Tengo que contratar algo después?","No. Es sin compromiso: te explicamos lo que te conviene y lo que no.",2),
 ("valoracion-integral","¿Cuánto cuesta?","Las condiciones están pendientes de confirmar por el centro.",3),
]
sql = "-- Generado por generar_semilla.py · no editar a mano\n"
sql += ins("pilares", ["slug","nombre","lema","descripcion","color","orden"], pilares)
sql += ins("programas", ["slug","pilar_slug","nombre","descripcion","orden"], programas)
sql += ins("categorias", ["slug","nombre","icono","orden"], categorias)  # area_slug: ver 003_areas_y_regalos.sql
sql += ins("profesionales", ["slug","nombre","cargo","bio","num_colegiado","sanitario"], profesionales)
sql += ins("tratamientos", cols, trat)
sql += ins("faqs", ["tratamiento_slug","pregunta","respuesta","orden"], [dict(tratamiento_slug=a,pregunta=b,respuesta=c,orden=d) for a,b,c,d in faqs])
Path(__file__).with_name("002_semilla.sql").write_text(sql)
print(len(trat), "tratamientos")

# Copia local del catálogo (mismo contenido que la base de datos) para el modo sin conexión.
import json, datetime
def completa(t):
    base = dict(para_quien=None, duracion_min=None, precio_desde=None)
    return {**base, **t}
catalogo = dict(
    exportado=datetime.date.today().isoformat(),
    areas=areas, pilares=pilares, programas=programas, categorias=sorted(categorias, key=lambda c: c["orden"]),
    profesionales=[{**dict(num_colegiado=None), **p} for p in profesionales],
    tratamientos=[completa(t) for t in sorted(trat, key=lambda t: (t["prioridad"], t["nombre"]))],
    faqs=[dict(tratamiento_slug=a, pregunta=b, respuesta=c, orden=d) for a, b, c, d in faqs],
)
Path(__file__).parent.parent.joinpath("datos", "catalogo.json").write_text(json.dumps(catalogo, ensure_ascii=False, indent=1))
print("datos/catalogo.json escrito")
