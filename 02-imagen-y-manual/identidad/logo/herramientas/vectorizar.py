"""Compone el logotipo en vector: isotipo SVG ORIGINAL + calco (potrace) del texto del raster maestro."""
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
