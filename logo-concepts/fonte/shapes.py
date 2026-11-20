"""Symbol geometry for round 2 (watercolour direction)."""
import math

OFF, CREAM, SAND, PEACH, GREIGE, OLIVE, BROWN = "#FAF7F2", "#F1E6D8", "#DDC3A8", "#D8AB94", "#C9BEB2", "#9DA17A", "#76543E"


def _xf(pts, ox, oy, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [(ox + x * c - y * s, oy + x * s + y * c) for x, y in pts]


def _fmt(p):
    return f"{p[0]:.2f},{p[1]:.2f}"


def leaf(ox, oy, deg, L, W, curl=0.0, asym=0.85):
    """Leaf with base at (ox,oy) pointing 'up' rotated by deg (clockwise). Returns (outline, midrib)."""
    t = (curl * L, -L)
    pts = [(0, 0), (-W, -0.28 * L), (-0.9 * W + 0.55 * curl * L, -0.74 * L), t,
           (asym * 0.85 * W + 0.55 * curl * L, -0.72 * L), (asym * W, -0.3 * L), (0, 0)]
    p = _xf(pts, ox, oy, deg)
    d = f"M{_fmt(p[0])}C{_fmt(p[1])} {_fmt(p[2])} {_fmt(p[3])}C{_fmt(p[4])} {_fmt(p[5])} {_fmt(p[6])}Z"
    m = _xf([(0, -0.04 * L), (0.35 * curl * L, -0.5 * L), (0.9 * curl * L, -0.9 * L)], ox, oy, deg)
    rib = f"M{_fmt(m[0])}Q{_fmt(m[1])} {_fmt(m[2])}"
    return d, rib


def petal(ox, oy, deg, L, W, start=0.0):
    """Symmetric vesica petal from start..L along the axis."""
    pts = [(0, -start), (-W, -start - 0.3 * (L - start)), (-W, -start - 0.7 * (L - start)), (0, -L),
           (W, -start - 0.7 * (L - start)), (W, -start - 0.3 * (L - start)), (0, -start)]
    p = _xf(pts, ox, oy, deg)
    return f"M{_fmt(p[0])}C{_fmt(p[1])} {_fmt(p[2])} {_fmt(p[3])}C{_fmt(p[4])} {_fmt(p[5])} {_fmt(p[6])}Z"


def circle(cx, cy, r):
    return f"M{cx - r:.2f},{cy:.2f}a{r:.2f},{r:.2f} 0 1,0 {2 * r:.2f},0a{r:.2f},{r:.2f} 0 1,0 {-2 * r:.2f},0Z"


# Every symbol returns a list of layers:
#   ("wash", d, colour)        translucent watercolour fill
#   ("line", d, width)         fine contour line
#   ("dot", d, role)           solid dot; role "ink" or a colour
#   ("solid", d, colour)       flat fill (pans of the balance etc.)

def flor():
    L = []
    base = (70, 100)
    leaves = [(-80, 58, 12, 0.10, SAND), (80, 58, 12, -0.10, OLIVE),
              (-52, 66, 15, 0.06, PEACH), (52, 66, 15, -0.06, OLIVE),
              (-25, 76, 16, 0.02, PEACH), (25, 76, 16, -0.02, SAND),
              (0, 86, 15, 0.0, PEACH)]
    for deg, l, w, c, col in leaves:
        d, rib = leaf(base[0], base[1], deg, l, w, c, 0.9)
        L.append(("wash", d, col))
        L.append(("line", d, 0.55))
        L.append(("line", rib, 0.45))
    for y, r in ((-3, 0.9), (3, 1.1), (9, 1.3)):
        L.append(("dot", circle(70, y, r), "ink"))
    for y, r in ((106, 1.3), (112, 1.0)):
        L.append(("dot", circle(70, y, r), "ink"))
    return L


def selo():
    L = []
    cx, cy = 60, 60
    for deg, col in ((90, SAND), (270, SAND)):
        L.append(("wash", petal(cx, cy, deg, 49, 13, 4), col))
    for deg in (45, 135, 225, 315):
        L.append(("wash", petal(cx, cy, deg, 48, 15, 4), PEACH))
    for deg in (90, 270, 45, 135, 225, 315):
        L.append(("line", petal(cx, cy, deg, 49 if deg in (90, 270) else 48, 13 if deg in (90, 270) else 15, 4), 0.5))
    for oy, deg in ((31, 0), (89, 180)):
        d, rib = leaf(cx, oy, deg, 20, 7, 0, 1.0)
        L.append(("wash", d, OLIVE)); L.append(("wash", d, OLIVE))
        L.append(("line", d, 0.5)); L.append(("line", rib, 0.4))
    L.append(("line", circle(cx, cy, 53), 0.6))
    # balance: axis, beam and two pans
    L.append(("line", "M60,36V86", 0.7))
    L.append(("line", "M41,54Q60,47 79,54", 0.8))
    for x in (41, 79):
        L.append(("line", f"M{x},54L{x-5.5},65M{x},54L{x+5.5},65", 0.45))
        L.append(("solid", f"M{x-7},65C{x-6},70.5 {x+6},70.5 {x+7},65Z", PEACH))
        L.append(("line", f"M{x-7},65C{x-6},70.5 {x+6},70.5 {x+7},65Z", 0.5))
    L.append(("dot", circle(60, 48.5, 1.6), "ink"))
    L.append(("dot", circle(60, 1.5, 1.4), "ink"))
    L.append(("dot", circle(60, 118.5, 1.4), "ink"))
    return L


def _catmull_open(pts):
    d = f"M{_fmt(pts[0])}"
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{_fmt(c1)} {_fmt(c2)} {_fmt(p2)}"
    return d


def horizonte():
    L = []
    sun = circle(64, 38, 29)
    left = "M2,84C2,60 28,46 56,47C82,48 100,62 106,84Z"
    right = "M62,84C68,60 96,41 124,42C147,43 158,62 158,84Z"
    front = "M26,84C48,66 92,61 130,84Z"
    L.append(("wash", sun, PEACH))
    L.append(("washfade", left, SAND))
    L.append(("washfade", right, OLIVE))
    L.append(("washfade", front, PEACH))
    # an open figure-of-eight drawn as one continuous line
    pts = []
    for k in range(0, 61):
        t = math.radians(-150 + k * 5.5)
        x = 82 + 50 * math.cos(t) / (1 + math.sin(t) ** 2)
        y = 40 + 34 * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2)
        pts.append((x, y))
    L.append(("line", _catmull_open(pts), 0.8))
    # contours used only in single-colour versions
    L.append(("mline", sun, 0.55))
    L.append(("mline", "M2,84C2,60 28,46 56,47C82,48 100,62 106,84", 0.55))
    L.append(("mline", "M62,84C68,60 96,41 124,42C147,43 158,62 158,84", 0.55))
    return L


def encontro():
    L = []
    cx, cy = 60, 66
    for deg, col in ((0, PEACH), (120, OLIVE), (240, SAND)):
        d = petal(cx, cy, deg, 50, 19, -12)
        L.append(("wash", d, col))
    for deg in (0, 120, 240):
        L.append(("line", petal(cx, cy, deg, 50, 19, -12), 0.55))
    L.append(("dot", circle(cx, cy, 1.6), "ink"))
    L.append(("dot", circle(60, 7, 1.3), "ink"))
    return L


SYMBOLS = {"e-flor": flor, "f-selo": selo, "g-horizonte": horizonte, "h-encontro": encontro}
