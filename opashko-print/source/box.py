"""Opashko mailer box print files: dieline (cut / crease / perforation) + 2-ink artwork on kraft.

Box style: tuck-front mailer with double side walls (similar to FEFCO 0427).
All units are millimetres. Inner dimensions L x W x H (length along the front, depth, height).
The dieline is ORIENTATIVE: the box maker supplies the exact template for their board and machine;
the artwork per panel is then placed on it.
"""
import math
import textpath as tp
import geom
import logo

TEAL = '#1D5C63'; APRICOT = '#F4895F'
CUT = '#E4002B'; CREASE = '#0077C8'; PERF = '#00A651'; INFO = '#555555'
LW = 0.35  # line width of technical lines

SIZES = {
    'S': dict(L=300, W=200, H=110, kg='до 1 кг'),
    'M': dict(L=450, W=300, H=200, kg='до 3 кг'),
    'L': dict(L=520, W=350, H=260, kg='до 5 кг'),
}


def T(s, size, x, y, anchor='start', font='nunito900', fill=TEAL, tracking=0):
    d, _ = tp.path(s, font, size, x, y, anchor, tracking)
    return f'<path d="{d}" fill="{fill}"/>'


def TW(s, size, font='nunito900'):
    return tp.width(s, font, size)


def fit(s, max_w, size, font='nunito900'):
    w = TW(s, size, font)
    return size if w <= max_w else size * max_w / w


class Panel:
    """Collects art / perforation / crease / cut drawn in the panel's own viewer coordinates."""
    def __init__(self, transform):
        self.t = transform; self.art = []; self.perf = []; self.crease = []; self.cut = []

    def groups(self):
        g = lambda items: f'<g transform="{self.t}">{"".join(items)}</g>' if items else ''
        return g(self.art), g(self.perf), g(self.crease), g(self.cut)


def line(x1, y1, x2, y2):
    return f'<path d="M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f}"/>'


def paw_art(cx, cy, s, fill):
    return ''.join(f'<path d="{d}" fill="{fill}"/>' for d in geom.paw_d(cx, cy, s))


def small_tail(x, y, h, fill=TEAL):
    """Little wagging-tail icon (dog) of height h with its base at (x, y)."""
    k = h / 60
    pts = geom.sample(geom.parse_cubic(f'M{x},{y} C{x+18*k},{y-2*k} {x+30*k},{y-16*k} {x+30*k},{y-36*k} '
                                        f'C{x+30*k},{y-48*k} {x+26*k},{y-56*k} {x+20*k},{y-58*k}'), 16)
    body = geom.poly_d(geom.tail_outline(pts, 12*k, 7*k, cap_end=True, cap_start=True))
    wag = (f'<path d="M{x+38*k},{y-50*k} Q{x+45*k},{y-40*k} {x+40*k},{y-30*k}" fill="none" stroke="{fill}" '
           f'stroke-width="{3*k:.2f}" stroke-linecap="round"/>')
    return f'<path d="{body}" fill="{fill}"/>' + wag


# ----------------------------------------------------------------------------------------------
# Artwork per panel (viewer coordinates: u to the right, v downwards, origin = panel top-left
# as a person sees that face of the closed box)
# ----------------------------------------------------------------------------------------------

def lid(p, L, W, size, pet):
    # --- tear strip with the tail-shaped pull tab (opens the box) ---
    v1, v2 = W - 40, W - 20; vm = (v1 + v2) / 2
    p.art.append(f'<rect x="56" y="{v1}" width="{L-56+3}" height="{v2-v1}" fill="{APRICOT}"/>')
    msg = 'дръпни опашката  »  дръпни опашката  »'
    fs = fit(msg, L - 90, 10.5, 'nunito900')
    p.art.append(T(msg, fs, 70, vm + fs * 0.36, font='nunito900', fill=TEAL))
    p.perf += [line(56, v1, L, v1), line(56, v2, L, v2)]
    ks = min(1.0, W / 300)
    pts = geom.sample(geom.parse_cubic(
        f'M60,{vm} C{60-18*ks},{vm} {60-34*ks},{vm-2*ks} {60-41*ks},{vm-20*ks} '
        f'C{60-46*ks},{vm-33*ks} {60-39*ks},{vm-46*ks} {60-29*ks},{vm-44*ks}'), 18)
    outline = geom.tail_outline(pts, 19, 11 * ks + 2, cap_end=True)
    fillpart = geom.tail_outline(pts[:int(len(pts)*0.72)], 19, 13.5 * ks + 2, cap_end=False)
    p.art.append(f'<path d="{geom.poly_d(fillpart)}" fill="{APRICOT}"/>')
    p.art.append(f'<path d="{geom.poly_d(outline, close=False)}" fill="none" stroke="{TEAL}" stroke-width="1.6" stroke-linejoin="round"/>')
    p.cut.append(f'<path d="{geom.poly_d(outline, close=False)}"/>')
    p.art.append(T('дръпни ме!', 9 * ks, 60 - 26 * ks, vm - 50 * ks, font='caveat700', fill=TEAL))

    lw = 0.6 * L
    if pet == 'dog':
        g, h = logo.place((L - lw) / 2, 0.40 * W - lw * 0.103, lw, 'kraft2')
        p.art.append(g)
        p.art.append(T('Бау. Мяу. Уау!', fit('Бау. Мяу. Уау!', 0.4 * L, 0.05 * L), L / 2, 0.40 * W + lw * 0.103 + 0.07 * L, 'middle'))
        s = max(0.045 * L, 16)
        for (cu, cv) in [(0.13, 0.26), (0.87, 0.26), (0.13, 0.62), (0.87, 0.62)]:
            p.art.append(paw_art(cu * L, cv * W, s, APRICOT))
            p.perf += [f'<path d="{d}"/>' for d in geom.paw_d(cu * L, cv * W, s)]
    else:
        cy = 0.5 * W if size == 'S' else 0.56 * W
        g, h = logo.place((L - lw) / 2, cy - lw * 0.103, lw, 'kraft2')
        p.art.append(g)
        # pop-up ears near the back edge: perforated sides, creased base; tip points to the back so the
        # printed face looks forward once the ear stands up
        eb, eh = 0.16 * L, 0.13 * L; base_v = 15 + eh + 5
        for cu in (L / 2 - 0.18 * L, L / 2 + 0.18 * L):
            a = (cu - eb / 2, base_v); b = (cu + eb / 2, base_v); tip = (cu, base_v - eh)
            inner = [(cu - eb * 0.28, base_v - 4), (cu, base_v - eh * 0.68), (cu + eb * 0.28, base_v - 4)]
            p.art.append(f'<path d="{geom.poly_d([a, tip, b])}" fill="none" stroke="{TEAL}" stroke-width="2.2" stroke-linejoin="round"/>')
            p.art.append(f'<path d="{geom.poly_d(inner)}" fill="{APRICOT}"/>')
            p.perf.append(f'<path d="{geom.poly_d([a, tip, b], close=False)}"/>')
            p.crease.append(line(a[0], a[1], b[0], b[1]))
        if size == 'S':  # paw-in-the-hole game holes
            r = 16
            for cu, cv in [(0.12 * L, cy), (0.88 * L, cy), (L / 2, 0.2 * W)]:
                p.art.append(f'<circle cx="{cu}" cy="{cv}" r="{r+4}" fill="none" stroke="{APRICOT}" stroke-width="3"/>')
                p.perf.append(f'<path d="{geom.ellipse_d(cu, cv, r, r)}"/>')
        else:
            p.art.append(T('Бау. Мяу. Уау!', fit('Бау. Мяу. Уау!', 0.4 * L, 0.05 * L), L / 2, cy + lw * 0.103 + 0.07 * L, 'middle'))


def front(p, L, H, size, pet, kg):
    big = 'Бау. Мяу. Уау!'
    if pet == 'cat' and size != 'S':
        dw = min(0.36 * L, 170); dh = min(H - 40, dw * 1.15); sill = H - 10
        cx = L / 2; top = sill - dh; r = dw / 2
        arch = f'M{cx-r:.1f},{sill} L{cx-r:.1f},{top+r:.1f} A{r:.1f},{r:.1f} 0 0 1 {cx+r:.1f},{top+r:.1f} L{cx+r:.1f},{sill} Z'
        p.perf.append(f'<path d="{arch}"/>')
        rr = r + 7
        p.art.append(f'<path d="M{cx-rr:.1f},{sill} L{cx-rr:.1f},{top+r:.1f} A{rr:.1f},{rr:.1f} 0 0 1 {cx+rr:.1f},{top+r:.1f} L{cx+rr:.1f},{sill}" '
                     f'fill="none" stroke="{APRICOT}" stroke-width="5" stroke-dasharray="10 7"/>')
        p.art.append(T('натисни тук', fit('натисни тук', dw * 0.8, 0.06 * H, 'caveat700'), cx, top + r + 0.04 * H, 'middle', font='caveat700'))
        # name plaque (write the cat's name)
        pw = min(0.26 * L, (L - dw) / 2 - 40); ph = 0.3 * H; px = (L / 2 - r - 14 - pw); py = 0.3 * H
        px = max(px, 18)
        p.art.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{pw:.1f}" height="{ph:.1f}" rx="{ph*0.18:.1f}" fill="{APRICOT}" stroke="{TEAL}" stroke-width="2.2"/>')
        fsz = ph * 0.32
        p.art.append(T('вила', fsz, px + pw / 2, py + ph * 0.42, 'middle', font='caveat700'))
        p.art.append(f'<path d="M{px+pw*0.12:.1f},{py+ph*0.8:.1f} L{px+pw*0.88:.1f},{py+ph*0.8:.1f}" stroke="{TEAL}" stroke-width="1.6"/>')
        # paw trail to the door on the right
        s = 0.035 * H
        for i, (u, vv) in enumerate([(0.92, 0.85), (0.86, 0.72), (0.8, 0.86), (0.74, 0.73)]):
            p.art.append(paw_art(u * L, vv * H, s, TEAL))
        fs = fit(big, (L / 2 - r - 30), 0.075 * H)
        p.art.append(T(big, fs, L - 18, 0.25 * H, 'end'))
    else:
        fs = fit(big, 0.72 * L, 0.24 * H)
        x0 = L / 2 - TW(big, fs) / 2
        p.art.append(T('Бау. Мяу. ', fs, x0, 0.5 * H + fs * 0.25))
        p.art.append(T('Уау!', fs, x0 + TW('Бау. Мяу. ', fs), 0.5 * H + fs * 0.25, fill=APRICOT))
        sub = 'храна + изненади за кучета и котки'
        fs2 = fit(sub, 0.6 * L, 0.075 * H, 'nunito700')
        p.art.append(T(sub, fs2, L / 2, 0.5 * H + fs * 0.25 + fs2 * 1.5, 'middle', font='nunito700'))
        s = 0.045 * H
        for k in range(5):
            p.art.append(paw_art(L * (0.1 + 0.2 * k), 0.15 * H, s, APRICOT if k % 2 else TEAL))


def back(p, L, H, size, pet):
    if pet == 'cat' and size != 'S':
        # flip-up tail: drawn upside-down under a crease near the top edge
        hh = H - 40; u0 = 0.78 * L; vc = 14
        final = f'M0,0 C4,{0.35*hh} -10,{0.55*hh} -4,{0.78*hh} C0,{0.95*hh} -16,{1.02*hh} -24,{0.9*hh}'
        pts = [(u0 + x, vc + y) for x, y in geom.sample(geom.parse_cubic(final), 22)]
        w0, w1 = 0.17 * hh, 0.1 * hh
        outline = geom.tail_outline(pts, w0, w1, cap_end=True)
        p.perf.append(f'<path d="{geom.poly_d(outline, close=False)}"/>')
        p.crease.append(line(u0 - w0 / 2, vc, u0 + w0 / 2, vc))
        for i in range(3, len(pts) - 4, 9):
            p.art.append(f'<path d="{geom.poly_d(geom.band(pts, i, i + 3, w0 * 1.02 - (w0 - w1) * i / len(pts)))}" fill="{TEAL}"/>')
        p.art.append(f'<path d="{geom.poly_d(outline)}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
        tx = u0 + w0 / 2 + 8
        cs = fit('опашката!', L - tx - 10, 0.08 * H, 'caveat700')
        p.art.append(T('изправи', cs, tx, 0.45 * H, font='caveat700'))
        p.art.append(T('опашката!', cs, tx, 0.45 * H + cs * 1.1, font='caveat700'))
        textw = u0 - w0 / 2 - 0.07 * L - 20
    else:
        textw = 0.86 * L
    lines = [('опашко', 'nunito900', 0.16 * H, TEAL),
             ('[сайт]  ·  [инстаграм]', 'nunito700', 0.065 * H, TEAL),
             ('Рециклирай ме — след като ' + ('котката се изнесе.' if pet == 'cat' else 'играта свърши.'), 'nunito700', 0.055 * H, TEAL)]
    v = 0.3 * H
    for s, f, sz, c in lines:
        sz = fit(s, textw, sz, f)
        p.art.append(T(s, sz, 0.07 * L, v, font=f, fill=c)); v += sz * 1.45


def side_info(p, W, H, size, pet, kg):
    k = min(W / 200, H / 110)
    if pet == 'dog':
        title = 'ИГРА НА НЮХ'
        rows = ['1  Извади храната и изненадите.', '2  Пробий лапичките на капака.',
                '3  Скрий лакомства в хартията и затвори.', '4  Нека кучето души и рови!']
        note = 'Играйте под наблюдение. Картонът не е за ядене.'
    elif size == 'S':
        title = 'ИГРА „ЛАПА В ДУПКАТА“'
        rows = ['1  Извади храната и изненадите.', '2  Пробий кръгчетата на капака.',
                '3  Сложи топка или играчка вътре.', '4  Котката лови с лапа!']
        note = 'Играйте под наблюдение. Картонът не е за ядене.'
    else:
        title = 'КОТЕШКА КЪЩА'
        rows = ['1  Извади храната и изненадите.', '2  Натисни вратата и прозорчето.',
                '3  Изправи ушите и опашката.', '4  Сложи одеялце — котката се нанася!']
        note = 'Махни тиксото и лентите преди играта.'
    x = 0.07 * W; v = 0.2 * H
    ts = fit(title, 0.86 * W, 10 * k)
    p.art.append(T(title, ts, x, v + ts * 0.7, fill=APRICOT, tracking=30)); v += ts * 0.7 + 9 * k
    rs = min(fit(r, 0.86 * W, 6.4 * k, 'nunito700') for r in rows)
    for r in rows:
        p.art.append(T(r, rs, x, v + rs * 0.7, font='nunito700')); v += rs * 1.4
    ns = fit(note, 0.86 * W, 4.6 * k, 'nunito700')
    p.art.append(T(note, ns, x, v + ns * 1.2, font='nunito700'))


def side_label(p, W, H, size, pet, kg):
    k = min(W / 200, H / 110)
    if pet == 'cat' and size != 'S':
        d = min(0.42 * W, 0.5 * H, 120); cx, cy = W / 2, 0.47 * H
        p.perf.append(f'<path d="{geom.ellipse_d(cx, cy, d/2, d/2)}"/>')
        p.art.append(f'<circle cx="{cx}" cy="{cy}" r="{d/2+7}" fill="none" stroke="{APRICOT}" stroke-width="5" stroke-dasharray="10 7"/>')
        p.art.append(T(f'{size}  ·  {kg}  ·  за котки', 5.5 * k, cx, H - 0.1 * H, 'middle', font='nunito700'))
    else:
        p.art.append(T(size, 34 * k, 0.12 * W, 0.62 * H, fill=APRICOT))
        p.art.append(T(kg, 9 * k, 0.12 * W + TW(size, 34 * k) + 6 * k, 0.45 * H, font='nunito900'))
        p.art.append(T('за кучета' if pet == 'dog' else 'за котки', 7 * k, 0.12 * W + TW(size, 34 * k) + 6 * k, 0.6 * H, font='nunito700'))
        p.art.append(small_tail(0.76 * W, 0.78 * H, 0.5 * H, TEAL))


def bottom(p, L, W, size, pet, kg):
    k = min(L / 300, W / 200)
    p.art.append(T('опашко', 9 * k, L / 2, W / 2 - 2 * k, 'middle'))
    p.art.append(T(f'OP-{size}-{"DOG" if pet == "dog" else "CAT"}  ·  велпапе, рециклируем', 4.2 * k, L / 2, W / 2 + 6 * k, 'middle', font='nunito700'))


# ----------------------------------------------------------------------------------------------
# Dieline
# ----------------------------------------------------------------------------------------------

def build(size, pet):
    S = SIZES[size]; L, W, H, kg = S['L'], S['W'], S['H'], S['kg']
    Tk = H - 10  # tuck flap depth
    cut = []; crease = []

    # bottom B [0,L]x[0,W]: all edges are creases
    crease += [line(0, 0, L, 0), line(0, W, L, W), line(0, 0, 0, W), line(L, 0, L, W)]
    # back wall K [0,L]x[-H,0]; ears on both ends
    crease.append(line(0, -H, L, -H))
    for x, sgn in ((0, -1), (L, 1)):
        cut += [line(x, -H, x, -H + 3), line(x, -3, x, 0)]
        crease.append(line(x, -H + 3, x, -3))
        e = W - 15
        cut.append(f'<path d="M{x},{-H+3} L{x+sgn*e},{-H+15} L{x+sgn*e},{-12} L{x},{-3}" fill="none"/>')
    # lid D [0,L]x[-H-W,-H]; side dust flaps
    for x, sgn in ((0, -1), (L, 1)):
        cut += [line(x, -H - W, x, -H - W + 5), line(x, -H - 5, x, -H)]
        crease.append(line(x, -H - W + 5, x, -H - 5))
        d = H - 15
        cut.append(f'<path d="M{x},{-H-W+5} L{x+sgn*d},{-H-W+25} L{x+sgn*d},{-H-25} L{x},{-H-5}" fill="none"/>')
    # tuck flap
    crease.append(line(0, -H - W, L, -H - W))
    y0 = -H - W
    cut.append(f'<path d="M0,{y0} L4,{y0-Tk+16} Q6,{y0-Tk} 22,{y0-Tk} L{L-22},{y0-Tk} Q{L-6},{y0-Tk} {L-4},{y0-Tk+16} L{L},{y0}" fill="none"/>')
    # front outer Fo [0,L]x[W,W+H] + inner Fi [0,L]x[W+H, W+2H-2] with lock tabs
    crease.append(line(0, W + H, L, W + H))
    for x, sgn in ((0, -1), (L, 1)):
        cut += [line(x, W, x, W + 3), line(x, W + H - 3, x, W + H)]
        crease.append(line(x, W + 3, x, W + H - 3))
        e = W - 15
        cut.append(f'<path d="M{x},{W+3} L{x+sgn*e},{W+15} L{x+sgn*e},{W+H-12} L{x},{W+H-3}" fill="none"/>')
        cut.append(line(x, W + H, x, W + 2 * H - 2))
    yb = W + 2 * H - 2
    tabs = ''.join(f' L{c-15},{yb} L{c-12},{yb+8} L{c+12},{yb+8} L{c+15},{yb}' for c in (L * 0.25, L * 0.75))
    cut.append(f'<path d="M0,{yb}{tabs} L{L},{yb}" fill="none"/>')
    # side walls (double) with lock tabs
    for sgn, x0 in ((-1, 0), (1, L)):
        xo = x0 + sgn * H; xi = x0 + sgn * (2 * H - 2)
        crease.append(line(xo, 0, xo, W))
        cut += [line(x0, 0, xi, 0), line(x0, W, xi, W)]
        tb = ''.join(f' L{xi},{c-15} L{xi+sgn*8},{c-12} L{xi+sgn*8},{c+12} L{xi},{c+15}' for c in (W * 0.25, W * 0.75))
        cut.append(f'<path d="M{xi},0{tb} L{xi},{W}" fill="none"/>')

    # panels with artwork (transforms map viewer coords into the flat net, printed side up)
    P = {
        'lid': Panel(f'translate({L} {-H}) scale(-1 -1)'),
        'front': Panel(f'translate({L} {W+H}) scale(-1 -1)'),
        'back': Panel(f'translate(0 {-H})'),
        'left': Panel(f'translate({-H} {W}) rotate(-90)'),
        'right': Panel(f'translate({L+H} 0) rotate(90)'),
        'bottom': Panel('translate(0 0)'),
    }
    lid(P['lid'], L, W, size, pet)
    front(P['front'], L, H, size, pet, kg)
    back(P['back'], L, H, size, pet)
    side_info(P['left'], W, H, size, pet, kg)
    side_label(P['right'], W, H, size, pet, kg)
    bottom(P['bottom'], L, W, size, pet, kg)

    art = []; perf = []; cr = []; ct = []
    for pn in P.values():
        a, pf, c, k = pn.groups(); art.append(a); perf.append(pf); cr.append(c); ct.append(k)

    # extents
    x_min = -(2 * H - 2) - 8 - 10; x_max = L + (2 * H - 2) + 8 + 10
    x_min = min(x_min, -(W - 15) - 10); x_max = max(x_max, L + (W - 15) + 10)
    y_min = -H - W - Tk - 12; y_max = W + 2 * H - 2 + 8 + 12
    info_h = 70
    vb_w = x_max - x_min; vb_h = y_max - y_min + info_h

    name = f'Опашко · кутия {size} ({kg}) · {"куче" if pet == "dog" else "котка"}'
    info = [T(name, 14, x_min + 10, y_max + 22, fill='#222'),
            T(f'Вътрешни размери: {L} × {W} × {H} мм  ·  велпапе крафт, E или B вълна  ·  печат флексо 2 цвята',
              6.5, x_min + 10, y_max + 36, font='nunito700', fill='#333'),
            T('Цвят 1: петролено (близо до Pantone 7476 C)  ·  Цвят 2: кайсия (близо до Pantone 1575 C) — уточнете по мостра с печатницата',
              6.5, x_min + 10, y_max + 47, font='nunito700', fill='#333')]
    lx = x_min + 10; ly = y_max + 60
    for col, dash, lab in ((CUT, '', 'рязане'), (CREASE, '6 3', 'биговане (сгъване)'), (PERF, '1.5 2.5', 'перфорация (натисни / пробий)')):
        info.append(f'<path d="M{lx},{ly} L{lx+22},{ly}" stroke="{col}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
        info.append(T(lab, 6, lx + 26, ly + 2, font='nunito700', fill='#333'))
        lx += 26 + TW(lab, 6, 'nunito700') + 18
    info.append(T('Ориентировъчна щанца — производителят дава точния шаблон за своя картон; дизайнът се поставя по панели.',
                  5.5, lx + 10, ly + 2, font='nunito700', fill='#666'))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{vb_w:.1f}mm" height="{vb_h:.1f}mm" viewBox="{x_min:.1f} {y_min:.1f} {vb_w:.1f} {vb_h:.1f}">
<title>{name}</title>
<g id="ПЕЧАТ_ARTWORK">{''.join(art)}</g>
<g id="РЯЗАНЕ_CUT" fill="none" stroke="{CUT}" stroke-width="{LW}">{''.join(cut)}{''.join(ct)}</g>
<g id="БИГОВАНЕ_CREASE" fill="none" stroke="{CREASE}" stroke-width="{LW}" stroke-dasharray="6 3">{''.join(crease)}{''.join(cr)}</g>
<g id="ПЕРФОРАЦИЯ_PERF" fill="none" stroke="{PERF}" stroke-width="{LW*1.3}" stroke-dasharray="1.5 2.5">{''.join(perf)}</g>
<g id="ИНФО_INFO">{''.join(info)}</g>
</svg>'''
    return svg, (vb_w, vb_h)


def preview(size, pet):
    """Same file with a kraft background, for looking at it on screen."""
    svg, dims = build(size, pet)
    return svg.replace('<g id="ПЕЧАТ_ARTWORK">', '<rect x="-5000" y="-5000" width="10000" height="10000" fill="#FFFFFF"/>'
                       '<g id="ПЕЧАТ_ARTWORK">', 1), dims


def kraft_preview(size, pet):
    S = SIZES[size]; L, W, H = S['L'], S['W'], S['H']; Tk = H - 10
    svg, dims = build(size, pet)
    k = '#E2C39A'
    rects = [(0, -H - W - Tk + 2, L, Tk - 2), (0, -H - W, L, W), (0, -H, L, H), (0, 0, L, W), (0, W, L, H), (0, W + H, L, H - 2),
             (-2 * H + 2, 0, 2 * H - 2, W), (L, 0, 2 * H - 2, W)]
    bg = '<rect x="-5000" y="-5000" width="10000" height="10000" fill="#FFFFFF"/>' + ''.join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{k}"/>' for x, y, w, h in rects)
    return svg.replace('<g id="ПЕЧАТ_ARTWORK">', bg + '<g id="ПЕЧАТ_ARTWORK">', 1), dims
