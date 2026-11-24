import os, logo, box, tape
OUT = '/home/user/Repone/opashko-print'
for d in ('01-logo', '02-tiksо-tape'.replace('о', 'o'), '03-kutii-boxes', 'previews'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
jobs = []  # (svg_path, pdf_path or None, png_path or None, width_mm, height_mm)

def logo_file(name, mode, ink, bg, background):
    x0, y0, x1, y1 = logo.BBOX; pad = 12
    w = x1 - x0 + 2 * pad; h = y1 - y0 + 2 * pad
    s = logo.standalone(mode, ink=ink, bg=bg, pad=pad, background=background)
    mm = 200 / w  # 200 mm wide artwork
    s = s.replace('<svg ', f'<svg width="{w*mm:.1f}mm" height="{h*mm:.1f}mm" ', 1)
    p = os.path.join(OUT, '01-logo', name)
    open(p + '.svg', 'w').write(s)
    jobs.append((p + '.svg', p + '.pdf', p + '.png', w * mm, h * mm))

logo_file('opashko-logo-color', 'color', '#1D5C63', '#FFF7EC', None)
logo_file('opashko-logo-color-on-cream', 'color', '#1D5C63', '#FFF7EC', '#FFF7EC')
logo_file('opashko-logo-kraft-2-colors', 'kraft2', '#1D5C63', '#E2C39A', None)
logo_file('opashko-logo-1-color-teal', 'mono', '#1D5C63', '#FFFFFF', None)
logo_file('opashko-logo-reverse-on-teal', 'mono', '#FFF7EC', '#1D5C63', '#1D5C63')

p = os.path.join(OUT, '02-tikso-tape', 'opashko-tape-48mm-repeat-300mm')
open(p + '.svg', 'w').write(tape.svg(1))
jobs.append((p + '.svg', p + '.pdf', None, tape.W, tape.H))
pp = os.path.join(OUT, 'previews', 'tape-preview')
open(pp + '.svg', 'w').write(tape.svg(3, background='#FFD166'))
jobs.append((pp + '.svg', None, pp + '.png', tape.W * 3, tape.H))

for size in ('S', 'M', 'L'):
    for pet in ('dog', 'cat'):
        name = f'opashko-box-{size}-{pet}-{box.SIZES[size]["L"]}x{box.SIZES[size]["W"]}x{box.SIZES[size]["H"]}'
        svg, (w, h) = box.build(size, pet)
        p = os.path.join(OUT, '03-kutii-boxes', name)
        open(p + '.svg', 'w').write(svg)
        jobs.append((p + '.svg', p + '.pdf', None, w, h))
        pv, _ = box.kraft_preview(size, pet)
        pp = os.path.join(OUT, 'previews', name + '-preview')
        open(pp + '.svg', 'w').write(pv)
        jobs.append((pp + '.svg', None, pp + '.png', w, h))

import json
json.dump(jobs, open('/tmp/claude-0/-home-user-Repone/13b07cc7-08b3-5f9a-a40b-488bceaf092a/scratchpad/jobs.json', 'w'))
print(len(jobs), 'files')
