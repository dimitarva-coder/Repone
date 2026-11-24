"""Turn text into SVG path outlines (no font needed at print time)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

FD = os.path.join(os.path.dirname(__file__), '..', 'fonts')
_cache = {}
FILES = {
    'nunito900': ['nunito900-cyr.woff2', 'nunito900-lat.woff2'],
    'nunito700': ['nunito700-cyr.woff2', 'nunito700-lat.woff2'],
    'caveat700': ['caveat700-cyr.woff2', 'caveat700-lat.woff2'],
}

def _fonts(name):
    if name not in _cache:
        _cache[name] = [TTFont(os.path.join(FD, f)) for f in FILES[name]]
    return _cache[name]

def _pick(name, ch):
    for f in _fonts(name):
        if ord(ch) in f.getBestCmap():
            return f
    raise KeyError(f'{ch!r} not in {name}')

def glyphs(text, name):
    """Yield (font, glyphname, x_advance_start) in font units."""
    x = 0
    out = []
    for ch in text:
        f = _pick(name, ch)
        g = f.getBestCmap()[ord(ch)]
        out.append((f, g, x))
        x += f['hmtx'][g][0]
    return out, x

def width(text, name, size, tracking=0):
    _, w = glyphs(text, name)
    return w * size / 1000 + tracking * size / 1000 * (len(text) - 1)

def path(text, name, size, x=0, y=0, anchor='start', tracking=0):
    """Return (d, bbox) with baseline at y, size = em in output units. tracking in 1/1000 em."""
    gl, w = glyphs(text, name)
    s = size / 1000
    total = w * s + tracking * s * (len(text) - 1)
    if anchor == 'middle':
        x -= total / 2
    elif anchor == 'end':
        x -= total
    cmds = []
    bounds = None
    for i, (f, g, gx) in enumerate(gl):
        ox = x + (gx + tracking * i) * s
        gs = f.getGlyphSet()
        t = (s, 0, 0, -s, ox, y)
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, t))
        cmds.append(pen.getCommands())
        bp = BoundsPen(gs)
        gs[g].draw(TransformPen(bp, t))
        if bp.bounds:
            b = bp.bounds
            bounds = b if bounds is None else (min(bounds[0], b[0]), min(bounds[1], b[1]), max(bounds[2], b[2]), max(bounds[3], b[3]))
    return ' '.join(c for c in cmds if c), bounds

def char_boxes(text, name, size, x=0, y=0):
    """Per-character bounding boxes (for placing ears/tails on letters)."""
    gl, _ = glyphs(text, name)
    s = size / 1000
    boxes = []
    for f, g, gx in gl:
        bp = BoundsPen(f.getGlyphSet())
        f.getGlyphSet()[g].draw(TransformPen(bp, (s, 0, 0, -s, x + gx * s, y)))
        boxes.append(bp.bounds)
    return boxes
