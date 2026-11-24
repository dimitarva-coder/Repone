"""Small geometry helpers: cubic bezier sampling, tapered tail outlines, paw shapes."""
import math, re

def parse_cubic(d):
    """Parse 'M x,y C x1,y1 x2,y2 x,y ...' into a list of cubic segments."""
    nums = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', d)]
    p0 = (nums[0], nums[1]); segs = []; i = 2
    while i + 5 < len(nums) + 1 and i + 6 <= len(nums):
        c1 = (nums[i], nums[i+1]); c2 = (nums[i+2], nums[i+3]); p = (nums[i+4], nums[i+5])
        segs.append((p0, c1, c2, p)); p0 = p; i += 6
    return segs

def _bez(s, t):
    (x0,y0),(x1,y1),(x2,y2),(x3,y3) = s; u = 1-t
    return (u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3, u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3)

def sample(segs, n=24):
    pts = []
    for k, s in enumerate(segs):
        for j in range(n + (1 if k == len(segs)-1 else 0)):
            pts.append(_bez(s, j/n))
    return pts

def _normals(pts):
    out = []
    for i in range(len(pts)):
        a = pts[max(i-1, 0)]; b = pts[min(i+1, len(pts)-1)]
        dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
        out.append((-dy/L, dx/L))
    return out

def tail_outline(pts, w0, w1, cap_end=True, cap_start=False):
    """Closed polygon around a centreline whose width tapers from w0 to w1."""
    nrm = _normals(pts); n = len(pts)
    left = []; right = []
    for i, (p, nv) in enumerate(zip(pts, nrm)):
        w = (w0 + (w1-w0) * i/(n-1)) / 2
        left.append((p[0]+nv[0]*w, p[1]+nv[1]*w)); right.append((p[0]-nv[0]*w, p[1]-nv[1]*w))
    poly = left[:]
    if cap_end:
        p = pts[-1]; nv = nrm[-1]; w = w1/2; base = math.atan2(nv[1], nv[0])
        poly += [(p[0]+w*math.cos(base - math.pi*k/10), p[1]+w*math.sin(base - math.pi*k/10)) for k in range(1, 10)]
    poly += right[::-1]
    if cap_start:
        p = pts[0]; nv = nrm[0]; w = w0/2; base = math.atan2(-nv[1], -nv[0])
        poly += [(p[0]+w*math.cos(base - math.pi*k/10), p[1]+w*math.sin(base - math.pi*k/10)) for k in range(1, 10)]
    return poly

def band(pts, i0, i1, w):
    """Quad strip covering centreline points i0..i1 at constant width (for stripes)."""
    nrm = _normals(pts); seg = pts[i0:i1+1]; nn = nrm[i0:i1+1]; h = w/2
    l = [(p[0]+v[0]*h, p[1]+v[1]*h) for p, v in zip(seg, nn)]
    r = [(p[0]-v[0]*h, p[1]-v[1]*h) for p, v in zip(seg, nn)]
    return l + r[::-1]

def poly_d(poly, close=True):
    return 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in poly) + (' Z' if close else '')

def transform(poly, fn):
    return [fn(x, y) for x, y in poly]

def ellipse_d(cx, cy, rx, ry, rot=0):
    pts = []
    for k in range(48):
        a = 2*math.pi*k/48; x = rx*math.cos(a); y = ry*math.sin(a)
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((cx + x*c - y*s, cy + x*s + y*c))
    return poly_d(pts)

def paw_d(cx, cy, s):
    """Paw print of overall width ~ 2.2*s: one main pad + 4 toes. Returns list of path d."""
    return [ellipse_d(cx, cy + 0.35*s, 0.62*s, 0.5*s),
            ellipse_d(cx - 0.78*s, cy - 0.25*s, 0.22*s, 0.28*s, -20),
            ellipse_d(cx - 0.3*s, cy - 0.72*s, 0.22*s, 0.29*s, -6),
            ellipse_d(cx + 0.3*s, cy - 0.72*s, 0.22*s, 0.29*s, 6),
            ellipse_d(cx + 0.78*s, cy - 0.25*s, 0.22*s, 0.28*s, 20)]
