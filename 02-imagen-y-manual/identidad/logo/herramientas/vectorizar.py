"""Compone el logotipo en vector: isotipo SVG ORIGINAL + calco (potrace) del texto del raster maestro.

Uso: python3 vectorizar.py <raster> <salida.svg> <color> <isotipo.svg> [--tilde]
--tilde añade el acento de «estética» en el descriptor (aprobado por el cliente el 17/11/2026).
"""
import sys, re, numpy as np, potrace
from PIL import Image
src, out, color = sys.argv[1], sys.argv[2], sys.argv[3]
iso_svg = open(sys.argv[4]).read()
ISO_D = re.search(r' d="([^"]+)"', iso_svg).group(1); VBW, VBH = 171.2, 237.53
im = Image.open(src).convert('RGBA'); a = np.array(im.getchannel('A'))
ys, xs = np.where(a > 128); a = a[ys.min():ys.max()+1, xs.min():xs.max()+1]; H, W = a.shape
mask = a > 128
# componentes: isotipo = bloque conectado más a la izquierda (horizontal) o más arriba (vertical)
from scipy import ndimage
lab, n = ndimage.label(mask, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
sizes = ndimage.sum(mask, lab, range(1, n+1))
iso_i = int(np.argmax(sizes)) + 1          # el isotipo es la mancha más grande
sl = objs[iso_i-1]; iy0, iy1, ix0, ix1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
texto = mask & (lab != iso_i)
if '--tilde' in sys.argv:
    from PIL import ImageDraw
    alto = [o[0].stop - o[0].start for o in objs]
    # descriptor: componentes pequeños pegados a la línea inferior del logotipo
    pequenos = [o for o in objs if (o[0].stop - o[0].start) < H * 0.12]
    from collections import Counter
    base = Counter(o[0].stop for o in pequenos).most_common(1)[0][0]
    letras = sorted([o for o in pequenos if abs(o[0].stop - base) <= 3 and (o[0].stop - o[0].start) > H * 0.012], key=lambda o: o[1].start)
    # «centro de estetica»: c e n t r o d e e s t [e] -> índice 11
    e = letras[11]
    x0, x1, y0, y1 = e[1].start, e[1].stop, e[0].start, e[0].stop
    w, xh = x1 - x0, y1 - y0; cx = (x0 + x1) / 2; g = 0.17 * xh
    p1 = (cx - 0.10 * w, y0 - 0.16 * xh); p2 = (cx + 0.30 * w, y0 - 0.58 * xh)
    import math
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0]); nx, ny = -math.sin(ang) * g / 2, math.cos(ang) * g / 2
    img = Image.fromarray(texto.astype('uint8') * 255)
    ImageDraw.Draw(img).polygon([(p1[0] + nx, p1[1] + ny), (p2[0] + nx, p2[1] + ny), (p2[0] - nx, p2[1] - ny), (p1[0] - nx, p1[1] - ny)], fill=255)
    texto = np.array(img) > 127
    print('tilde añadida sobre la «e» en', (x0, y0, x1, y1))
bm = potrace.Bitmap(~texto)
path = bm.trace(turdsize=4, alphamax=1.0, opticurve=True, opttolerance=0.2)
d = []
for curve in path:
    s = curve.start_point; d.append(f"M{s.x:.1f},{s.y:.1f}")
    for seg in curve.segments:
        if seg.is_corner: d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        else: d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
    d.append("Z")
sc = (iy1 - iy0) / VBH
tx = ix0 + ((ix1 - ix0) - VBW * sc) / 2
svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">\n'
       f'<!-- Isotipo: vector original del cliente (sin modificar). Texto: calco vectorial del archivo maestro LOGO_2023.psd -->\n'
       f'<g fill="{color}"><path transform="translate({tx:.2f} {iy0}) scale({sc:.5f})" d="{ISO_D}"/>\n<path fill-rule="evenodd" d="{"".join(d)}"/></g>\n</svg>\n')
open(out, 'w').write(svg)
print(out, W, H, 'curvas texto:', len(path), 'escala iso', round(sc, 4), 'ancho iso px', ix1-ix0, 'vs', round(VBW*sc,1))
