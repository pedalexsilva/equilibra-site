"""Round 3: four approaches unlike rounds 1-2 (geometric, typographic, object, pattern)."""
import json, math, os, sys
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from glyphs import Face, Text, path_bounds, circle_d, union

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(HERE), "ronda-3"))
os.makedirs(OUT, exist_ok=True)
OFF, CREAM, SAND, PEACH, GREIGE, OLIVE, BROWN = "#FAF7F2", "#F1E6D8", "#DDC3A8", "#D8AB94", "#C9BEB2", "#9DA17A", "#76543E"
PAL = {
    "cor":     {"ink": BROWN, "peach": PEACH, "olive": OLIVE, "sand": SAND, "cream": CREAM, "off": OFF, "tick": BROWN},
    "mono":    {"ink": BROWN, "peach": BROWN, "olive": BROWN, "sand": BROWN, "cream": "none", "off": OFF, "tick": OFF},
    "inverso": {"ink": OFF,   "peach": OFF,   "olive": OFF,   "sand": OFF,   "cream": "none", "off": "none", "tick": "none"},
}
TAG = "NUTRIÇÃO · PSICOLOGIA · MOVIMENTO"
NAMES = "com Lisa Bompastor e Sara Lucas"

F = lambda name, axes: Face(name, axes)
FACES = {
    "i-construcao": dict(word=F("Jost[wght].ttf", {"wght": 500}), tag=F("Jost[wght].ttf", {"wght": 500}), names=F("Jost[wght].ttf", {"wght": 400})),
    "k-nivel":      dict(word=F("Figtree[wght].ttf", {"wght": 600}), tag=F("Figtree[wght].ttf", {"wght": 600}), names=F("Figtree[wght].ttf", {"wght": 400})),
    "l-azulejo":    dict(word=F("BricolageGrotesque[opsz,wdth,wght].ttf", {"opsz": 96, "wdth": 100, "wght": 600}),
                         tag=F("BricolageGrotesque[opsz,wdth,wght].ttf", {"opsz": 12, "wdth": 100, "wght": 600}),
                         names=F("BricolageGrotesque[opsz,wdth,wght].ttf", {"opsz": 12, "wdth": 100, "wght": 400})),
    "j-aequus":     dict(tag=F("Archivo[wdth,wght].ttf", {"wght": 600, "wdth": 100}), names=F("Archivo[wdth,wght].ttf", {"wght": 400, "wdth": 100})),
}

# ------------------------------------------------------------------ symbols
def rect(x0, y0, x1, y1):
    return f"M{x0},{y0}H{x1}V{y1}H{x0}Z"

def construcao():
    # moments about the rocker's centre (x=60): circle 1134 x 20 = 22680, square 676 x 33.5 = 22646
    return [
        ("M32,84A28,28 0 0,0 88,84Z", "ink", "fill", 0),
        (rect(14, 77, 108, 84), "ink", "fill", 0),
        (circle_d(40, 58, 19), "peach", "fill", 0),
        (rect(80.5, 51, 106.5, 77), "olive", "fill", 0),
    ]

def capsule(x0, y0, x1, y1):
    r = (y1 - y0) / 2
    return f"M{x0 + r},{y0}H{x1 - r}A{r},{r} 0 0,1 {x1 - r},{y1}H{x0 + r}A{r},{r} 0 0,1 {x0 + r},{y0}Z"

def nivel():
    return [
        (capsule(6, 40, 114, 76), "olive", "fill", 0),
        ("M60,42.6C68.5,42.6 74,45.6 74,50C74,54.4 68.5,57.2 60,57.2C51.5,57.2 46,54.4 46,50C46,45.6 51.5,42.6 60,42.6Z", "off", "fill", 0),
        ("M42,43V73M78,43V73", "tick", "stroke", 2.4),
        (capsule(6, 40, 114, 76), "ink", "stroke", 3.2),
    ]

def quarter(cx, cy, r, a0):
    """Quarter disc centred at a tile corner, opening towards the tile."""
    a1 = a0 + 90
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    return f"M{cx},{cy}L{p0[0]:.2f},{p0[1]:.2f}A{r},{r} 0 0,1 {p1[0]:.2f},{p1[1]:.2f}Z"

def quarter_arc(cx, cy, r, a0):
    a1 = a0 + 90
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    return f"M{p0[0]:.2f},{p0[1]:.2f}A{r},{r} 0 0,1 {p1[0]:.2f},{p1[1]:.2f}"

def azulejo():
    s = [(rect(0, 0, 120, 120), "cream", "fill", 0)]
    corners = [((0, 0), 0, "peach"), ((120, 0), 90, "olive"), ((120, 120), 180, "peach"), ((0, 120), 270, "olive")]
    for (cx, cy), a0, col in corners:
        s.append((quarter(cx, cy, 52, a0), col, "fill", 0))
    for (cx, cy), a0, col in corners:
        s.append((quarter_arc(cx, cy, 36, a0), "off", "stroke", 3))
        s.append((circle_d(cx + 14 * math.cos(math.radians(a0 + 45)), cy + 14 * math.sin(math.radians(a0 + 45)), 5), "off", "fill", 0))
    # centre: a small rosette where the four tiles' rhythm meets
    for a in (0, 90, 180, 270):
        x, y = 60 + 13 * math.cos(math.radians(a)), 60 + 13 * math.sin(math.radians(a))
        s.append((circle_d(x, y, 6.5), "ink", "fill", 0))
    s.append((circle_d(60, 60, 6.5), "ink", "fill", 0))
    return s

def igual():
    return [(rect(16, 34, 104, 54), "ink", "fill", 0), (rect(16, 66, 104, 86), "peach", "fill", 0)]

SYMS = {"i-construcao": construcao, "k-nivel": nivel, "l-azulejo": azulejo, "j-aequus": igual}

# ------------------------------------------------------------------ svg helpers
def shapes_svg(shapes, pal, transform=""):
    out = []
    for d, role, kind, sw in shapes:
        col = pal[role]
        if col == "none":
            continue
        if kind == "fill":
            out.append(f'<path d="{d}" fill="{col}"/>')
        else:
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    g = "".join(out)
    return f'<g transform="{transform}">{g}</g>' if transform else g

def shapes_bounds(shapes):
    return union(*[path_bounds(d, sw) for d, role, kind, sw in shapes])

def doc(inner, box, pad, label):
    x0, y0, x1, y1 = box
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}" '
            f'width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" role="img" aria-label="{label}"><title>{label}</title>{inner}</svg>')

def tpath(t, x, y, col):
    return f'<path d="{t.d}" fill="{col}" transform="translate({x:.2f} {y:.2f})"/>'

def fit(face, text, width, tracking=0.2, lo=7, hi=14):
    probe = face.run(text, 10, tracking)
    return face.run(text, max(lo, min(hi, 10 * width / probe.width)), tracking)

LABEL = "Equilibra — Nutrição, Psicologia e Movimento"

# ------------------------------------------------------------------ generic lockups (I, K, L)
WORDS = {
    "i-construcao": FACES["i-construcao"]["word"].run("equilibra", 60, -0.005),
    "k-nivel": FACES["k-nivel"]["word"].run("equilibra", 58, -0.01),
    "l-azulejo": FACES["l-azulejo"]["word"].run("equilibra", 60, -0.015),
}
CFG = {
    "i-construcao": dict(sym_h=104, gap=26, compact_k=1.25, vgap=26),
    "k-nivel":      dict(sym_h=62,  gap=24, compact_k=0.72, vgap=24),
    "l-azulejo":    dict(sym_h=100, gap=26, compact_k=1.05, vgap=26),
}

def lockup(cid, mode, layout):
    pal = PAL[mode]; ink = pal["ink"]
    shapes = SYMS[cid]()
    sb = shapes_bounds(shapes)
    if layout == "simbolo":
        return doc(shapes_svg(shapes, pal), sb, 4, "Equilibra")
    word = WORDS[cid]; wb = word.bounds; ww = wb[2] - wb[0]; wh = wb[3] - wb[1]
    cfg = CFG[cid]; faces = FACES[cid]
    if layout == "compacto":
        sh = cfg["compact_k"] * wh
    else:
        sh = cfg["sym_h"]
    k = sh / (sb[3] - sb[1]); sw = (sb[2] - sb[0]) * k
    if layout in ("horizontal", "compacto"):
        tr = f"translate({-sb[0] * k:.2f} {-(sb[1] + sb[3]) / 2 * k:.2f}) scale({k:.4f})"
        x = sw + (cfg["gap"] if layout == "horizontal" else 0.32 * wh)
        parts = [shapes_svg(shapes, pal, tr)]
        if layout == "compacto":
            parts.append(tpath(word, x - wb[0], -(wb[1] + wb[3]) / 2, ink))
            return doc("".join(parts), (0, min(-sh / 2, -wh / 2), x + ww, max(sh / 2, wh / 2)), 4, "Equilibra")
        tag = fit(faces["tag"], TAG, ww, 0.18)
        block = wh + 14 + (tag.bounds[3] - tag.bounds[1])
        wy = -block / 2 - wb[1]
        ty = -block / 2 + wh + 14 - tag.bounds[1]
        parts += [tpath(word, x - wb[0], wy, ink), tpath(tag, x - tag.bounds[0], ty, ink)]
        return doc("".join(parts), (0, min(-sh / 2, -block / 2), x + max(ww, tag.width), max(sh / 2, block / 2)), 8, LABEL)
    if layout == "vertical":
        tr = f"translate({-(sb[0] + sb[2]) / 2 * k:.2f} {-sb[1] * k:.2f}) scale({k:.4f})"
        y = sh + cfg["vgap"]
        parts = [shapes_svg(shapes, pal, tr), tpath(word, -(wb[0] + wb[2]) / 2, y - wb[1], ink)]
        y += wh + 14
        tag = fit(faces["tag"], TAG, ww, 0.18)
        parts.append(tpath(tag, -(tag.bounds[0] + tag.bounds[2]) / 2, y - tag.bounds[1], ink))
        y += tag.bounds[3] - tag.bounds[1] + 12
        nm = faces["names"].run(NAMES, (tag.bounds[3] - tag.bounds[1]) * 1.75, 0.01)
        parts.append(tpath(nm, -(nm.bounds[0] + nm.bounds[2]) / 2, y - nm.bounds[1], ink))
        y += nm.bounds[3] - nm.bounds[1]
        half = max(sw, ww, tag.width, nm.width) / 2
        return doc("".join(parts), (-half, 0, half, y), 10, LABEL + ", com Lisa Bompastor e Sara Lucas")

# ------------------------------------------------------------------ J: EQUI / LIBRA
def draw_at(face, text, size, tracking, dx, dy):
    t = face.run(text, size, tracking)
    s = size / face.upm
    pen = SVGPathPen(face.gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    bp = BoundsPen(face.gs)
    x = 0.0
    items = face.shape(text)
    for n, (g, adv, xo, yo) in enumerate(items):
        m = (s, 0, 0, -s, dx + x + xo * s, dy - yo * s)
        face.gs[g].draw(TransformPen(pen, m)); face.gs[g].draw(TransformPen(bp, m))
        x += adv * s + (tracking * size if n < len(items) - 1 else 0)
    return pen.getCommands(), bp.bounds

LIBRA_WDTH = 84
_lib = Face("Archivo[wdth,wght].ttf", {"wght": 800, "wdth": LIBRA_WDTH})
_target = _lib.run("LIBRA", 100).width
lo, hi = 62.0, 125.0
for _ in range(18):
    mid = (lo + hi) / 2
    w = Face("Archivo[wdth,wght].ttf", {"wght": 800, "wdth": mid}).run("EQUI", 100).width
    lo, hi = (mid, hi) if w < _target else (lo, mid)
EQUI_WDTH = round((lo + hi) / 2, 2)
_equi = Face("Archivo[wdth,wght].ttf", {"wght": 800, "wdth": EQUI_WDTH})

def aequus_block(size=72):
    """Returns (svg parts fn(pal), bounds). Two lines of identical ink width with a peach beam between."""
    e = _equi.run("EQUI", size); l = _lib.run("LIBRA", size)
    cap = -e.bounds[1]
    gap = size * 0.27
    d1, b1 = draw_at(_equi, "EQUI", size, 0, -e.bounds[0], cap)
    y2 = cap + gap + cap
    d2, b2 = draw_at(_lib, "LIBRA", size, 0, -l.bounds[0], y2)
    w = max(b1[2], b2[2])
    beam_y0, beam_y1 = cap + gap * 0.6, cap + gap * 0.82
    def parts(pal):
        return (f'<path d="{d1}" fill="{pal["ink"]}"/>'
                f'<path d="{rect(0, round(beam_y0, 2), round(w, 2), round(beam_y1, 2))}" fill="{pal["peach"]}"/>'
                f'<path d="{d2}" fill="{pal["ink"]}"/>')
    return parts, (0, min(b1[1], b2[1]), w, max(b1[3], b2[3]))

def aequus(mode, layout):
    pal = PAL[mode]; ink = pal["ink"]; faces = FACES["j-aequus"]
    if layout == "simbolo":
        shapes = igual()
        return doc(shapes_svg(shapes, pal), (0, 0, 120, 120), 0, "Equilibra")
    parts, (x0, y0, x1, y1) = aequus_block()
    w, h = x1 - x0, y1 - y0
    if layout == "compacto":
        return doc(parts(pal), (x0, y0, x1, y1), 4, "Equilibra")
    if layout == "vertical":
        y = y1 + 20
        tag = fit(faces["tag"], TAG, w, 0.12, 6, 12)
        out = parts(pal) + tpath(tag, -tag.bounds[0] + (w - tag.width) / 2, y - tag.bounds[1], ink)
        y += tag.bounds[3] - tag.bounds[1] + 12
        nm = faces["names"].run(NAMES, (tag.bounds[3] - tag.bounds[1]) * 1.75, 0.0)
        out += tpath(nm, -nm.bounds[0] + (w - nm.width) / 2, y - nm.bounds[1], ink)
        y += nm.bounds[3] - nm.bounds[1]
        half_extra = max(0, (max(tag.width, nm.width) - w) / 2)
        return doc(out, (x0 - half_extra, y0, x1 + half_extra, y), 10, LABEL + ", com Lisa Bompastor e Sara Lucas")
    if layout == "horizontal":
        lines = [faces["tag"].run(s, 13, 0.16) for s in ("NUTRIÇÃO", "PSICOLOGIA", "MOVIMENTO")]
        lh = lines[0].bounds[3] - lines[0].bounds[1]
        step = (h - lh) / 2
        x = w + 22
        out = parts(pal) + f'<path d="M{w + 11:.2f},{y0:.2f}V{y1:.2f}" stroke="{pal["peach"]}" stroke-width="1.6"/>'
        for i, t in enumerate(lines):
            out += tpath(t, x - t.bounds[0], y0 + i * step - t.bounds[1], ink)
        return doc(out, (x0, y0, x + max(t.width for t in lines), y1), 8, LABEL)

# ------------------------------------------------------------------ main
if __name__ == "__main__":
    manifest = {}
    order = ["i-construcao", "j-aequus", "k-nivel", "l-azulejo"]
    for cid in order:
        m = manifest[cid] = {}
        for mode in ("cor", "mono", "inverso"):
            for layout in ("horizontal", "compacto", "vertical", "simbolo"):
                svg = aequus(mode, layout) if cid == "j-aequus" else lockup(cid, mode, layout)
                m[f"{layout}-{mode}"] = svg
                if mode == "cor" or layout in ("horizontal", "simbolo") or (mode == "mono" and layout == "vertical"):
                    open(os.path.join(OUT, f"{cid}-{layout}" + ("" if mode == "cor" else f"-{mode}") + ".svg"), "w").write(svg)
    print("EQUI wdth", EQUI_WDTH, "LIBRA wdth", LIBRA_WDTH, "files", len(os.listdir(OUT)))
