import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from glyphs import Face, path_bounds, circle_d, union

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF, CREAM, SAND, PEACH, GREIGE, OLIVE, BROWN = "#FAF7F2", "#F1E6D8", "#DDC3A8", "#D8AB94", "#C9BEB2", "#9DA17A", "#76543E"
PALETTES = {
    "cor":     {"ink": BROWN, "peach": PEACH, "olive": OLIVE, "sand": SAND},
    "mono":    {"ink": BROWN, "peach": BROWN, "olive": BROWN, "sand": BROWN},
    "inverso": {"ink": OFF,   "peach": OFF,   "olive": OFF,   "sand": OFF},
}

cormorant = Face("CormorantGaramond[wght].ttf", {"wght": 500})
cormorant_it = Face("CormorantGaramond-Italic[wght].ttf", {"wght": 500})
fraunces = Face("Fraunces[SOFT,WONK,opsz,wght].ttf", {"SOFT": 100, "WONK": 0, "opsz": 72, "wght": 360})
albert = Face("AlbertSans[wght].ttf", {"wght": 500})
albert_light = Face("AlbertSans[wght].ttf", {"wght": 300})
albert_reg = Face("AlbertSans[wght].ttf", {"wght": 400})

TAGLINE = "NUTRIÇÃO · PSICOLOGIA · MOVIMENTO"
NAMES = "com Sara Lucas e Lisa Bompastor"

# ---------------------------------------------------------------- symbols
# Each shape: (d, role, kind, stroke_width)  kind = "fill" | "stroke"

def sym_lotus():
    B = (60, 92)
    return [
        ("M60,92C47,76 46,50 60,28C74,50 73,76 60,92Z", "ink", "stroke", 2.6),
        ("M60,92C44,87 31,71 32,49C47,55 57,70 60,92Z", "ink", "stroke", 2.6),
        ("M60,92C76,87 89,71 88,49C73,55 63,70 60,92Z", "ink", "stroke", 2.6),
        ("M60,92C41,96 22,89 13,73C33,69 50,77 60,92Z", "ink", "stroke", 2.6),
        ("M60,92C79,96 98,89 107,73C87,69 70,77 60,92Z", "ink", "stroke", 2.6),
        ("M26,104H94", "ink", "stroke", 2.6),
        (circle_d(60, 15, 4), "peach", "fill", 0),
    ]

def sym_stones():
    return [
        ("M23,94C22,84 39,78.5 59,78C80,77.5 97,83 97,91.5C97,100.5 82,106 61,106C40,106 24,102.5 23,94Z", "ink", "fill", 0),
        ("M36,67.5C35,59.5 46,55 58,54.5C72,54 84,57 85,64C86,71 74,74.5 60,75C47,75.5 37,74 36,67.5Z", "olive", "fill", 0),
        ("M50,42.5C49,35 55,30 62,30C69.5,30 75,34.5 74.5,41.5C74,48 68.5,51.5 61.5,51.5C54.5,51.5 50.5,48.5 50,42.5Z", "peach", "fill", 0),
    ]


def _catmull(pts, closed=True):
    """Catmull-Rom through pts -> cubic bezier path string."""
    n = len(pts)
    d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n]; p1 = pts[i]; p2 = pts[(i + 1) % n]; p3 = pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}"
    return d + "Z"

def arc_leaf(a0, a1, R=40, W=6.4, cx=60, cy=60, n=16, drift=3):
    """A leaf whose midrib follows a slowly widening spiral from angle a0 to a1 (degrees)."""
    outer, inner = [], []
    for k in range(n + 1):
        t = k / n
        w = W * math.sin(math.pi * t) ** 1.1 * (1.15 - 0.3 * t)
        r = R - drift / 2 + drift * t
        a = math.radians(a0 + (a1 - a0) * t)
        outer.append((cx + (r + w) * math.cos(a), cy + (r + w) * math.sin(a)))
        inner.append((cx + (r - w) * math.cos(a), cy + (r - w) * math.sin(a)))
    pts = outer + inner[::-1][1:-1]
    return _catmull(pts)

def leaf(a0, a1, R, W, bend, taper, n=16, cx=60, cy=60):
    A0, A1 = math.radians(a0), math.radians(a1)
    p0 = (cx + R*math.cos(A0), cy + R*math.sin(A0)); p1 = (cx + R*math.cos(A1), cy + R*math.sin(A1))
    am = (A0 + A1) / 2
    nrm = (math.cos(am), math.sin(am))
    sag = R * (1 - math.cos((A1 - A0) / 2))
    outer, inner = [], []
    for k in range(n + 1):
        t = k / n
        mx = p0[0] + (p1[0]-p0[0])*t + nrm[0]*sag*bend*math.sin(math.pi*t)
        my = p0[1] + (p1[1]-p0[1])*t + nrm[1]*sag*bend*math.sin(math.pi*t)
        # local normal of the midrib
        dx = (p1[0]-p0[0]) + nrm[0]*sag*bend*math.pi*math.cos(math.pi*t)
        dy = (p1[1]-p0[1]) + nrm[1]*sag*bend*math.pi*math.cos(math.pi*t)
        L = math.hypot(dx, dy); nx, ny = dy/L, -dx/L
        w = W * math.sin(math.pi*t)**0.95 * (1 + taper*(0.5 - t))
        outer.append((mx - nx*w, my - ny*w)); inner.append((mx + nx*w, my + ny*w))
    return _catmull(outer + inner[::-1][1:-1])

def sym_leaves():
    shapes = []
    for i, role in enumerate(["olive", "peach", "ink"]):
        s = -90 + i * 120 + 6
        shapes.append((leaf(s, s + 112, 40, 5.4, 1.0, 0.7), role, "fill", 0))
    return shapes

def sym_e():
    t = cormorant_it.run("e", 120)
    x0, y0, x1, y1 = t.bounds
    # centre the e in a 120 box, dot top right
    dx = 60 - (x0 + x1) / 2 - 6
    dy = 96
    return [
        (t.d, "ink", "fill", 0, f"translate({dx:.2f} {dy:.2f})"),
        (circle_d(dx + x1 + 9, dy + y0 + 4, 7.5), "peach", "fill", 0),
    ]


def sym_ili():
    t = cormorant_it.run("ılı", 92, 0.02)
    texts, dots = _dots_for(t, 92)
    x0, y0, x1, y1 = path_bounds(t.d)
    dx = 60 - (x0 + x1) / 2 + 2
    dy = 60 - (y0 + y1) / 2 + 1
    tr = f"translate({dx:.2f} {dy:.2f})"
    return [(circle_d(60, 60, 52), "ink", "stroke", 2.2), (t.d, "ink", "fill", 0, tr)] + \
           [(d, role, "fill", 0, tr) for d, role in dots]

def _dots_for(t, size):
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    gs = cormorant_it.gs
    s = t.scale
    rec = DecomposingRecordingPen(gs)
    gs["i"].draw(rec)
    contours, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op in ("closePath", "endPath"):
            contours.append(cur); cur = []
    best = None
    for c in contours:
        pts = [p for op, args in c for p in args]
        ys = [p[1] for p in pts]; xs = [p[0] for p in pts]
        if best is None or min(ys) > best[1]:
            best = ((min(xs) + max(xs)) / 2, min(ys), (min(ys) + max(ys)) / 2, (max(xs) - min(xs)))
    dot_cx, _, dot_cy, dot_w = best
    roles = iter(["olive", "peach"])
    dots = []
    for g, x in t.glyphs:
        if g == "dotlessi":
            dots.append((circle_d(x + dot_cx * s, -dot_cy * s, dot_w * s * 0.62), next(roles)))
    return [(t, "ink")], dots

# ---------------------------------------------------------------- wordmarks

def word_A():
    return [(cormorant.run("EQUILIBRA", 46, 0.2), "ink")], None

def word_B():
    return [(fraunces.run("equilibra", 60, -0.005), "ink")], None

def word_C():
    return [(albert_light.run("EQUILIBRA", 38, 0.34), "ink")], None

def word_D():
    t = cormorant_it.run("equılıbra", 70, 0.015)
    return _dots_for(t, 70)

# ---------------------------------------------------------------- svg assembly

def shapes_svg(shapes, pal, transform=""):
    out = []
    for sh in shapes:
        d, role, kind, sw = sh[:4]
        tr = sh[4] if len(sh) > 4 else ""
        attrs = f' transform="{tr}"' if tr else ""
        col = pal[role]
        if kind == "fill":
            out.append(f'<path d="{d}" fill="{col}"{attrs}/>')
        else:
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{attrs}/>')
    g = "".join(out)
    return f'<g transform="{transform}">{g}</g>' if transform else g

def shapes_bounds(shapes):
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    bs = []
    for sh in shapes:
        d, role, kind, sw = sh[:4]
        tr = sh[4] if len(sh) > 4 else ""
        m = (1, 0, 0, 1, 0, 0)
        if tr.startswith("rotate"):
            a, cx, cy = [float(v) for v in tr[7:-1].split()]
            r = math.radians(a); c, s_ = math.cos(r), math.sin(r)
            m = (c, s_, -s_, c, cx - c * cx + s_ * cy, cy - s_ * cx - c * cy)
        elif tr.startswith("translate"):
            tx, ty = [float(v) for v in tr[10:-1].split()]
            m = (1, 0, 0, 1, tx, ty)
        bp = BoundsPen(None)
        parse_path(d, TransformPen(bp, m))
        x0, y0, x1, y1 = bp.bounds
        h = sw / 2
        bs.append((x0 - h, y0 - h, x1 + h, y1 + h))
    return union(*bs)

def word_svg(word, pal, tx, ty):
    texts, dots = word
    parts = [f'<path d="{t.d}" fill="{pal[role]}"/>' for t, role in texts]
    if dots:
        parts += [f'<path d="{d}" fill="{pal[role]}"/>' for d, role in dots]
    return f'<g transform="translate({tx:.2f} {ty:.2f})">{"".join(parts)}</g>'

def word_bounds(word):
    texts, dots = word
    bs = [t.bounds for t, _ in texts]
    if dots:
        bs += [path_bounds(d) for d, _ in dots]
    return union(*bs)

def svg_doc(inner, box, pad, title):
    x0, y0, x1, y1 = box
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}"><title>{title}</title>{inner}</svg>')

def tagline_for(width, face=albert, min_size=7.0, max_size=13):
    # size the tagline so it spans the given width
    probe = face.run(TAGLINE, 10, 0.22)
    size = 10 * width / probe.width
    size = max(min_size, min(max_size, size))
    return face.run(TAGLINE, size, 0.22)

CONCEPTS = {
    "a-lotus":   dict(sym=sym_lotus,  word=word_A, sym_h=118, gap=30, tag_gap=16, compact_k=1.9, compact_gap=0.45),
    "b-pedras":  dict(sym=sym_stones, word=word_B, sym_h=112, gap=28, tag_gap=16, compact_k=1.0, compact_gap=0.3),
    "c-ciclo":   dict(sym=sym_leaves, word=word_C, sym_h=112, gap=30, tag_gap=16, compact_k=1.9, compact_gap=0.5),
    "d-ili":     dict(sym=sym_ili,      word=word_D, sym_h=112, gap=26, tag_gap=14, compact_k=1.0, compact_gap=0.3),
}

def build(cid, cfg, pal_name, layout):
    pal = PALETTES[pal_name]
    shapes = cfg["sym"]()
    sb = shapes_bounds(shapes)
    word = cfg["word"]()
    wb = word_bounds(word)
    title = "Equilibra — Nutrição, Psicologia e Movimento"
    if layout == "simbolo":
        return svg_doc(shapes_svg(shapes, pal), sb, 6, "Equilibra")
    if layout == "palavra":
        return svg_doc(word_svg(word, pal, 0, 0), wb, 6, "Equilibra")
    # scale symbol to target height
    k = cfg["sym_h"] / (sb[3] - sb[1])
    ww = wb[2] - wb[0]
    if layout == "horizontal":
        tag = tagline_for(ww)
        word_h = wb[3] - wb[1]
        block_h = word_h + cfg["tag_gap"] + (tag.bounds[3] - tag.bounds[1])
        sym_w = (sb[2] - sb[0]) * k
        # symbol occupies x 0..sym_w, y centred on 0
        sym_tr = f"translate({-sb[0]*k:.2f} {-(sb[1]+sb[3])/2*k:.2f}) scale({k:.4f})"
        wx = sym_w + cfg["gap"] - wb[0]
        wy = -block_h / 2 - wb[1]
        tx = sym_w + cfg["gap"] - tag.bounds[0]
        ty = wy + wb[3] + cfg["tag_gap"] - tag.bounds[1]
        inner = shapes_svg(shapes, pal, sym_tr) + word_svg(word, pal, wx, wy) + \
            f'<path d="{tag.d}" fill="{pal["ink"]}" transform="translate({tx:.2f} {ty:.2f})"/>'
        box = (0, min(-cfg["sym_h"] / 2, wy + wb[1]), max(sym_w + cfg["gap"] + ww, tx + tag.bounds[2]),
               max(cfg["sym_h"] / 2, ty + tag.bounds[3]))
        return svg_doc(inner, box, 8, title)
    if layout == "compacto":
        wh = wb[3] - wb[1]
        sh = cfg["compact_k"] * wh
        kk = sh / (sb[3] - sb[1])
        sym_w = (sb[2] - sb[0]) * kk
        sym_tr = f"translate({-sb[0]*kk:.2f} {-(sb[1]+sb[3])/2*kk:.2f}) scale({kk:.4f})"
        gap = cfg["compact_gap"] * wh
        wx = sym_w + gap - wb[0]
        wy = -(wb[1] + wb[3]) / 2 + cfg.get("compact_dy", 0) * wh
        inner = shapes_svg(shapes, pal, sym_tr) + word_svg(word, pal, wx, wy)
        box = (0, min(-sh / 2, wy + wb[1]), sym_w + gap + ww, max(sh / 2, wy + wb[3]))
        return svg_doc(inner, box, 4, "Equilibra")
    if layout == "vertical":
        tag = tagline_for(ww)
        names = albert_reg.run(NAMES, tag.bounds[3] - tag.bounds[1] + 3.2, 0.02)
        sym_w = (sb[2] - sb[0]) * k
        sym_tr = f"translate({-(sb[0]+sb[2])/2*k:.2f} {-sb[1]*k:.2f}) scale({k:.4f})"
        wy = cfg["sym_h"] + cfg["gap"] * 0.9 - wb[1]
        wx = -(wb[0] + wb[2]) / 2
        ty = wy + wb[3] + cfg["tag_gap"] - tag.bounds[1]
        tx = -(tag.bounds[0] + tag.bounds[2]) / 2
        ny = ty + tag.bounds[3] + 14 - names.bounds[1]
        nx = -(names.bounds[0] + names.bounds[2]) / 2
        inner = shapes_svg(shapes, pal, sym_tr) + word_svg(word, pal, wx, wy) + \
            f'<path d="{tag.d}" fill="{pal["ink"]}" transform="translate({tx:.2f} {ty:.2f})"/>' + \
            f'<path d="{names.d}" fill="{pal["ink"]}" transform="translate({nx:.2f} {ny:.2f})"/>'
        half = max(sym_w, ww, tag.width, names.width) / 2
        box = (-half, 0, half, ny + names.bounds[3])
        return svg_doc(inner, box, 8, title)

if __name__ == "__main__":
    manifest = {}
    for cid, cfg in CONCEPTS.items():
        manifest[cid] = {}
        for pal in PALETTES:
            for layout in ("horizontal", "compacto", "vertical", "simbolo", "palavra"):
                svg = build(cid, cfg, pal, layout)
                manifest[cid][f"{layout}-{pal}"] = svg
                if pal == "cor" or (pal != "cor" and layout in ("horizontal", "simbolo")):
                    name = f"{cid}-{layout}" + ("" if pal == "cor" else f"-{pal}") + ".svg"
                    with open(os.path.join(OUT, name), "w") as f:
                        f.write(svg)
    print("built", sorted(os.listdir(OUT)))
