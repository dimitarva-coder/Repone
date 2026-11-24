"""Opashko wordmark: the first 'о' is a cat from behind, the last 'о' a dog from behind."""
import textpath as tp
import geom

TEAL = '#1D5C63'; APRICOT = '#F4895F'; EAR = '#D9693F'; BUTTER = '#FFD166'; CREAM = '#FFF7EC'

# Geometry in units where the font size is 100 and the baseline is y=0.
CAT_EARS = ['M10,-40 L12.5,-68 L29,-49.5 Z', 'M33,-49.5 L49.5,-68 L52,-40 Z']
CAT_TAIL = 'M11,-7 C-4,-1 -19,-10 -19,-31 C-19,-53 -8,-62 -12,-77 C-15,-88 -28,-88 -29,-78'
DOG_EARS = ['M345,-46 C339,-61 323,-61 320,-48 C318,-38 323,-27 330,-28 C336,-29 337,-40 343,-41 Z',
            'M378,-46 C384,-61 400,-61 403,-48 C405,-38 400,-27 393,-28 C387,-29 386,-40 380,-41 Z']
# bushy dog tail as a filled plume, plus a cream tip
DOG_TAIL = ('M380,-3 C404,-1 425,-22 426,-46 C427,-64 416,-77 403,-75 '
            'C396,-74 395,-66 401,-65 C409,-64 414,-56 413,-46 C412,-30 400,-18 384,-17 Z')
DOG_TIP = 'M403,-75 C396,-74 395,-66 401,-65 C405,-64.7 409,-63.5 411,-62 L417,-72 C413,-74.5 408,-75.5 403,-75 Z'
WAG = ['M435,-38 Q442,-28 435,-17', 'M440,-62 Q450,-50 444,-36']
BBOX = (-36, -95, 455, 6)  # x0, y0, x1, y1 (incl. outline strokes)

def _letters():
    word = 'опашко'
    boxes = tp.char_boxes(word, 'nunito900', 100)
    d_all, _ = tp.path(word, 'nunito900', 100)
    d_first, _ = tp.path('о', 'nunito900', 100, 0, 0)
    # last 'о' starts at the advance of 'опашк'
    adv = tp.width('опашк', 'nunito900', 100)
    d_last, _ = tp.path('о', 'nunito900', 100, adv, 0)
    d_mid, _ = tp.path('пашк', 'nunito900', 100, tp.width('о', 'nunito900', 100), 0)
    return d_first, d_mid, d_last

def group(mode='color', ink=TEAL, bg=CREAM):
    """mode: 'color' (full colour), 'mono' (one ink colour, for flexo/tape)."""
    d_first, d_mid, d_last = _letters()
    o = []
    if mode == 'color':
        ow = 4.2  # outline width
        # tails behind letters
        o.append(f'<path d="{CAT_TAIL}" fill="none" stroke="{ink}" stroke-width="{9+ow}" stroke-linecap="round"/>')
        o.append(f'<path d="{CAT_TAIL}" fill="none" stroke="{BUTTER}" stroke-width="9" stroke-linecap="round"/>')
        o.append(f'<path d="{CAT_TAIL}" fill="none" stroke="{ink}" stroke-width="9" stroke-dasharray="4.5 8" stroke-dashoffset="-6"/>')
        o.append(f'<path d="{DOG_TAIL}" fill="{APRICOT}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
        o.append(f'<path d="{DOG_TIP}" fill="{bg}" stroke="{ink}" stroke-width="{ow*0.8}" stroke-linejoin="round"/>')
        for w in WAG:
            o.append(f'<path d="{w}" fill="none" stroke="{ink}" stroke-width="3.4" stroke-linecap="round"/>')
        for e in CAT_EARS:
            o.append(f'<path d="{e}" fill="{BUTTER}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
        for e in DOG_EARS:
            o.append(f'<path d="{e}" fill="{EAR}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
        o.append(f'<path d="{d_first}" fill="{BUTTER}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round" paint-order="stroke"/>')
        o.append(f'<path d="{d_last}" fill="{APRICOT}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round" paint-order="stroke"/>')
        o.append(f'<path d="{d_mid}" fill="{ink}"/>')
        # dog ears drawn again on top so they hang over the 'о'
        for e in DOG_EARS:
            o.append(f'<path d="{e}" fill="{EAR}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
    elif mode == 'kraft2':
        ow = 4.2
        pts = geom.sample(geom.parse_cubic(CAT_TAIL), 30)
        ring = geom.tail_outline(pts, 9, 9, cap_end=True, cap_start=True)
        stripes = ''.join(f'<path d="{geom.poly_d(geom.band(pts, i, i+5, 9.2))}" fill="{ink}"/>' for i in range(4, len(pts)-6, 13))
        o.append(stripes)
        o.append(f'<path d="{geom.poly_d(ring)}" fill="none" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
        o.append(f'<path d="{DOG_TAIL}" fill="{APRICOT}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
        o.append(f'<path d="{DOG_TIP}" fill="none" stroke="{ink}" stroke-width="{ow*0.8}" stroke-linejoin="round"/>')
        for w in WAG:
            o.append(f'<path d="{w}" fill="none" stroke="{ink}" stroke-width="3.4" stroke-linecap="round"/>')
        for e in CAT_EARS:
            o.append(f'<path d="{e}" fill="{ink}"/>')
        o.append(f'<path d="{d_last}" fill="{APRICOT}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="round"/>')
        o.append(f'<path d="{d_first} {d_mid}" fill="{ink}"/>')
        for e in DOG_EARS:
            o.append(f'<path d="{e}" fill="{ink}" stroke="{ink}" stroke-width="1" stroke-linejoin="round"/>')
    else:
        o.append(f'<path d="{CAT_TAIL}" fill="none" stroke="{ink}" stroke-width="9" stroke-linecap="round"/>')
        o.append(f'<path d="{DOG_TAIL}" fill="{ink}"/>')
        o.append(f'<path d="{DOG_TIP}" fill="{bg}" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>')
        for w in WAG:
            o.append(f'<path d="{w}" fill="none" stroke="{ink}" stroke-width="3.4" stroke-linecap="round"/>')
        for e in CAT_EARS + DOG_EARS:
            o.append(f'<path d="{e}" fill="{ink}"/>')
        o.append(f'<path d="{d_first} {d_mid} {d_last}" fill="{ink}"/>')
        # dog ears: knock a thin gap so they read as separate from the 'о'
        for e in DOG_EARS:
            o.append(f'<path d="{e}" fill="{ink}" stroke="{bg}" stroke-width="2.2" stroke-linejoin="round"/>')
    return '\n'.join(o)

def place(x, y, width, mode='color', ink=TEAL, bg=CREAM):
    """Place the logo so its bbox starts at (x,y) and is `width` wide. Returns (svg, height)."""
    x0, y0, x1, y1 = BBOX
    s = width / (x1 - x0)
    g = f'<g transform="translate({x - x0*s:.3f} {y - y0*s:.3f}) scale({s:.5f})">{group(mode, ink, bg)}</g>'
    return g, (y1 - y0) * s

def standalone(mode='color', ink=TEAL, bg=CREAM, pad=12, background=None):
    x0, y0, x1, y1 = BBOX
    vb = f'{x0-pad} {y0-pad} {x1-x0+2*pad} {y1-y0+2*pad}'
    rect = f'<rect x="{x0-pad}" y="{y0-pad}" width="{x1-x0+2*pad}" height="{y1-y0+2*pad}" fill="{background}"/>' if background else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{rect}{group(mode, ink, bg)}</svg>'
