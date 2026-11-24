"""Packing tape 48 mm, one ink (teal) on yellow tape. One repeat = 300 mm."""
import logo, geom, textpath as tp
from box import T, TW, paw_art, small_tail, TEAL

W, H = 300.0, 48.0  # repeat length x tape width (mm)

def repeat(x0=0.0):
    o = []
    lh = 27.0; lw = lh * (logo.BBOX[2] - logo.BBOX[0]) / (logo.BBOX[3] - logo.BBOX[1])
    g, _ = logo.place(x0 + 10, (H - lh) / 2, lw, 'mono', ink=TEAL, bg='#FFD166')
    o.append(g)
    x = x0 + 10 + lw + 12
    o.append(paw_art(x + 6, H / 2, 5.2, TEAL)); x += 20
    msg = 'бау · мяу · уау!'
    fs = 13.0
    o.append(T(msg, fs, x, H / 2 + fs * 0.25)); x += TW(msg, fs) + 10
    o.append(small_tail(x, H / 2 + 11, 24, TEAL))
    return ''.join(o), x + 20 - x0

def svg(repeats=1, background=None):
    body = ''.join(repeat(i * W)[0] for i in range(repeats))
    bg = f'<rect width="{W*repeats}" height="{H}" fill="{background}"/>' if background else ''
    guides = '' if background else (f'<g id="ИНФО_INFO" fill="none" stroke="#E4002B" stroke-width="0.2" stroke-dasharray="2 2">'
                                    f'<rect x="0" y="0" width="{W*repeats}" height="{H}"/><path d="M0,3 H{W*repeats} M0,{H-3} H{W*repeats}"/></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*repeats}mm" height="{H}mm" viewBox="0 0 {W*repeats} {H}">'
            f'<title>Опашко тиксо 48 мм — раппорт {W:.0f} мм</title>{bg}<g id="ПЕЧАТ_ARTWORK">{body}</g>{guides}</svg>')

if __name__ == '__main__':
    print('content length in one repeat:', round(repeat()[1], 1), 'mm of', W)
