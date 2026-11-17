"""Genera el set de iconos de servicios de Rosa Ondoño (SVG) y los tokens de color.

Reglas de construcción (capítulo 7 del manual):
- Retícula de 24 × 24 con 2 px de margen interior.
- Trazo único de 1,5 px, extremos y uniones redondeados y sin relleno, salvo el punto final.
- Color: currentColor (por defecto #701B78 o tinta).
- Los iconos NO reproducen ni imitan el isotipo: son un sistema auxiliar.

Uso: python3 generar.py  (escribe los SVG en esta carpeta y los tokens en ../tokens/)
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))

ICONOS = {
    # Cuídate
    "valoracion": ('Valoración integral',
        '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><path d="M8.5 12.5l2.2 2.2 4.8-4.8"/>'),
    "facial": ('Tratamientos faciales',
        '<path d="M12 3c4 0 6.5 3 6.5 7.5S15.5 21 12 21s-6.5-6-6.5-10.5S8 3 12 3z"/><path d="M8.8 10.5q1.2 1 2.4 0M12.8 10.5q1.2 1 2.4 0"/><path d="M10.5 16q1.5 1 3 0"/>'),
    "corporal": ('Tratamientos corporales',
        '<path d="M8 3c0 4 2 5 2 9s-2 5-2 9"/><path d="M16 3c0 4-2 5-2 9s2 5 2 9"/>'),
    "laser": ('Depilación láser',
        '<circle cx="12" cy="12" r="2.5"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>'),
    "medicina": ('Medicina estética (supervisión médica)',
        '<path d="M6 3v5a4 4 0 0 0 8 0V3"/><path d="M10 12v3a4.5 4.5 0 0 0 9 0v-2"/><circle cx="19" cy="11" r="2"/>'),
    # Conecta
    "masaje": ('Masajes',
        '<path d="M7 20v-6.5L4.8 9.6a1.3 1.3 0 0 1 2.2-1.3L9 11.5V5.5a1.3 1.3 0 0 1 2.6 0V11"/><path d="M11.6 10V4.3a1.3 1.3 0 0 1 2.6 0V11"/><path d="M14.2 10.5V5.8a1.3 1.3 0 0 1 2.6 0v8.7c0 3-2 5.5-5 5.5H7"/>'),
    "drenaje": ('Drenaje linfático',
        '<path d="M12 3s5 5.5 5 9.5a5 5 0 0 1-10 0C7 8.5 12 3 12 3z"/><path d="M9.8 13.5a2.3 2.3 0 0 0 2.2 2"/>'),
    "fisioterapia": ('Fisioterapia y osteopatía',
        '<rect x="9" y="3" width="6" height="3.2" rx="1.6"/><rect x="9" y="8" width="6" height="3.2" rx="1.6"/><rect x="9" y="13" width="6" height="3.2" rx="1.6"/><rect x="9" y="18" width="6" height="3" rx="1.5"/>'),
    "acupuntura": ('Acupuntura y terapias complementarias',
        '<path d="M6 18L18 6"/><circle cx="18.5" cy="5.5" r="1.2"/><path d="M4 20l2-2"/><circle cx="7" cy="8" r=".6"/><circle cx="16" cy="17" r=".6"/>'),
    # Siente
    "ritual": ('Rituales',
        '<path d="M4 13h16a8 8 0 0 1-16 0z"/><path d="M9.5 9.5c-1-1.2 1-2.3 0-3.5M14.5 9.5c-1-1.2 1-2.3 0-3.5"/>'),
    "regalo": ('Tarjeta regalo',
        '<rect x="4" y="9" width="16" height="11" rx="1"/><path d="M3 9h18M12 9v11"/><path d="M12 9c-1.5-3-5-3.5-5-1.5S10 9 12 9zM12 9c1.5-3 5-3.5 5-1.5S14 9 12 9z"/>'),
    # Servicio
    "cita": ('Pedir cita',
        '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M8.5 3v4M15.5 3v4"/><circle cx="12" cy="15" r="1.2"/>'),
    "ubicacion": ('Cómo llegar',
        '<path d="M12 21s6.5-6.2 6.5-11a6.5 6.5 0 0 0-13 0c0 4.8 6.5 11 6.5 11z"/><circle cx="12" cy="10" r="2.3"/>'),
    "telefono": ('Llamar / WhatsApp',
        '<path d="M6.5 3.5h3l1.5 4-2 1.3a10 10 0 0 0 6.2 6.2l1.3-2 4 1.5v3a2 2 0 0 1-2 2A16 16 0 0 1 4.5 5.5a2 2 0 0 1 2-2z"/>'),
}

def svg(cuerpo, titulo):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
            'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round" role="img" aria-label="{titulo}"><title>{titulo}</title>{cuerpo}</svg>\n')

PALETA = {
    "corporativo": {"morado": {"hex": "#7D1F73", "rgb": [125, 31, 115], "fuente": "LOGO_2023.psd (propuesto, pendiente de confirmar)", "fijo": True,
                    "pantone": "PANTONE 255 C", "cmyk": [53, 96, 10, 24]}},
    "ruta_a_secundaria": {
        "marfil": "#F7F2EB", "arena": "#E9DCCB", "lila-empolvado": "#E8DAE6",
        "arcilla-rosada": "#B7897A", "ciruela-tinta": "#2E1A2C"},
    "ruta_b_secundaria": {
        "blanco-roto": "#FAF9F7", "niebla": "#ECEAEE", "lavanda": "#D9CFE2",
        "salvia": "#A9B7A4", "salvia-profunda": "#56664F", "grafito": "#1E1C21"},
}

if __name__ == "__main__":
    for nombre, (titulo, cuerpo) in ICONOS.items():
        with open(os.path.join(AQUI, f"icono-{nombre}.svg"), "w") as f:
            f.write(svg(cuerpo, titulo))
    tok = os.path.join(AQUI, "..", "tokens"); os.makedirs(tok, exist_ok=True)
    with open(os.path.join(tok, "color.json"), "w") as f:
        json.dump(PALETA, f, ensure_ascii=False, indent=2)
    css = [":root {", "  /* Color corporativo · NO MODIFICABLE (Pantone/CMYK: PENDIENTE) */",
           "  --ro-morado: #7D1F73; /* del logotipo maestro LOGO_2023.psd · confirmar */", "", "  /* Ruta A «Piel y luz» (base recomendada · borrador) */"]
    css += [f"  --ro-{k}: {v};" for k, v in PALETA["ruta_a_secundaria"].items()]
    css += ["", "  /* Ruta B «Criterio sereno» (apoyo en medicina estética · borrador) */"]
    css += [f"  --ro-{k}: {v};" for k, v in PALETA["ruta_b_secundaria"].items()]
    css += ["", "  /* Tipografía */",
            "  --ro-fuente-titulares: 'Cormorant Garamond', Georgia, 'Times New Roman', serif;",
            "  --ro-fuente-texto: 'Jost', 'Helvetica Neue', Arial, sans-serif;", "}"]
    with open(os.path.join(tok, "tokens.css"), "w") as f:
        f.write("\n".join(css) + "\n")
    print(f"{len(ICONOS)} iconos y tokens generados")
