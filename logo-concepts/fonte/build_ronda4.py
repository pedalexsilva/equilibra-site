"""Round 4: figure-ground faces, signature script, 70s arches, paper cut-outs."""
import io, json, math, os, random, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glyphs
from glyphs import Face, Text, path_bounds, circle_d, union
import build_ronda3 as b3
from build_ronda3 import PAL, OFF, CREAM, SAND, PEACH, GREIGE, OLIVE, BROWN, rect, doc, tpath, fit, shapes_svg, shapes_bounds

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(HERE), "ronda-4"))
os.makedirs(OUT, exist_ok=True)


class StaticFace(Face):
    def __init__(self, filename):
        data = open(glyphs.FONTS + filename, "rb").read()
        self.tt = TTFont(io.BytesIO(data))
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upm = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(data))


albert = Face("AlbertSans[wght].ttf", {"wght": 500})
albert_reg = Face("AlbertSans[wght].ttf", {"wght": 400})
instrument = StaticFace("InstrumentSerif-Regular.ttf")
instrument_it = StaticFace("InstrumentSerif-Italic.ttf")
madi = StaticFace("MsMadi-Regular.ttf")
capra = StaticFace("Caprasimo-Regular.ttf")
syne = Face("Syne[wght].ttf", {"wght": 700})
syne_tag = Face("Syne[wght].ttf", {"wght": 600})


def mirror_x(d, axis=120):
    """Mirror an absolute-coordinate path made of M/C/L/Z commands around x=axis/2."""
    import re
    out, toks = [], re.findall(r"[MCLZ]|-?[\d.]+", d)
    i, cmd, nums = 0, None, []
    res = []
    for t in toks:
        if t in "MCLZ":
            if cmd:
                res.append((cmd, nums))
            cmd, nums = t, []
        else:
            nums.append(float(t))
    res.append((cmd, nums))
    s = ""
    for c, n in res:
        s += c
        pts = [f"{axis - n[k]:.2f},{n[k + 1]:.2f}" for k in range(0, len(n), 2)]
        s += " ".join(pts)
    return s


# ------------------------------------------------------------------ M: two faces / vase
HEAD = ("M44,8C46,14 47,26 49,33C49,36 47,38 48,40L57,48C57,50 53,52 50,52C52,54 53,56 53,58C51,59 50,60 50,61"
        "C52,62 52,64 52,65C50,67 48,68 48,70C50,72 51,75 51,77C49,81 46,83 44,85C43,90 43,94 43,98"
        "C45,104 48,108 52,114L14,114C16,106 20,100 22,96C14,88 8,70 9,52C10,26 24,8 44,8Z")

def leaf_d(ox, oy, deg, L, W):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    pts = [(0, 0), (-W, -0.3 * L), (-0.8 * W, -0.75 * L), (0, -L), (0.8 * W, -0.75 * L), (W, -0.3 * L), (0, 0)]
    p = [(ox + x * c - y * s, oy + x * s + y * c) for x, y in pts]
    f = lambda q: f"{q[0]:.2f},{q[1]:.2f}"
    return f"M{f(p[0])}C{f(p[1])} {f(p[2])} {f(p[3])}C{f(p[4])} {f(p[5])} {f(p[6])}Z"

def faces():
    return [
        (HEAD, "peach", "fill", 0),
        (mirror_x(HEAD), "olive", "fill", 0),
        ("M60,24C60,12 60,2 60,-6", "ink", "stroke", 2.2),
        (leaf_d(60, -2, -48, 13, 4.4), "ink", "fill", 0),
        (leaf_d(60, -5, 44, 11, 3.8), "ink", "fill", 0),
    ]

# ------------------------------------------------------------------ O: 70s arches
def band(cx, cy, r0, r1):
    return (f"M{cx - r1},{cy}A{r1},{r1} 0 0,1 {cx + r1},{cy}H{cx + r0}"
            f"A{r0},{r0} 0 0,0 {cx - r0},{cy}Z")

def arcos():
    cx, cy = 60, 92
    return [
        (band(cx, cy, 43, 56), "peach", "fill", 0),
        (band(cx, cy, 28, 40), "olive", "fill", 0),
        (band(cx, cy, 13, 25), "ink", "fill", 0),
        (circle_d(cx, cy - 1, 7), "peach", "fill", 0),
        (rect(0, 96, 120, 100), "ink", "fill", 0),
    ]

# ------------------------------------------------------------------ P: paper cut-outs
def catmull(pts):
    n = len(pts); f = lambda q: f"{q[0]:.2f},{q[1]:.2f}"
    d = f"M{f(pts[0])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1)} {f(c2)} {f(p2)}"
    return d + "Z"

def blob(cx, cy, r, n=11, jitter=0.07, seed=1):
    rnd = random.Random(seed)
    return catmull([(cx + r * (1 + rnd.uniform(-jitter, jitter)) * math.cos(2 * math.pi * k / n + 0.3),
                     cy + r * (1 + rnd.uniform(-jitter, jitter)) * math.sin(2 * math.pi * k / n + 0.3)) for k in range(n)])

def frond(x, y0, y1, lobes=4, w=17, seed=3):
    """A cut-paper leaf: rounded lobes with clean notches, alternating left and right along a curved stem."""
    H = y1 - y0
    n = 64
    left, right = [], []
    for k in range(n + 1):
        t = k / n
        cx = x + 8 * math.sin(math.pi * t * 0.85) - 2
        y = y1 - t * H
        env = w * math.sin(math.pi * (0.04 + 0.92 * t)) ** 0.75
        lw = env * (0.42 + 0.58 * abs(math.sin(lobes * math.pi * t)))
        rw = env * (0.42 + 0.58 * abs(math.sin(lobes * math.pi * t + math.pi / 2)))
        left.append((cx - lw, y)); right.append((cx + rw, y))
    pts = left + right[::-1]
    f = lambda q: f"{q[0]:.2f},{q[1]:.2f}"
    return "M" + "L".join(f(p) for p in pts) + "Z"

def recortes():
    return [
        (frond(40, 8, 112, lobes=3.5, w=20, seed=5), "olive", "fill", 0),
        (blob(84, 36, 21, n=12, jitter=0.06, seed=8), "peach", "fill", 0),
        (blob(88, 90, 12, n=9, jitter=0.12, seed=2), "ink", "fill", 0),
        (blob(102, 66, 4.2, n=7, jitter=0.15, seed=4), "peach", "fill", 0),
        (blob(70, 70, 3.2, n=7, jitter=0.15, seed=9), "ink", "fill", 0),
    ]

# ------------------------------------------------------------------ N: signature
def signature(size=110):
    t = madi.run("equilibra", size, 0.0)
    x0, y0, x1, y1 = t.bounds
    w = x1 - x0
    # a calligraphic underline: thin ends, fuller in the middle, perfectly level at the centre
    sy = 22
    L, R = x0 + w * 0.06, x1 + w * 0.02
    mid = (L + R) / 2
    sw = (f"M{L:.2f},{sy + 3:.2f}C{L + w * 0.2:.2f},{sy - 0.6:.2f} {mid - w * 0.2:.2f},{sy - 1.6:.2f} {mid:.2f},{sy - 1.6:.2f}"
          f"C{mid + w * 0.22:.2f},{sy - 1.6:.2f} {R - w * 0.12:.2f},{sy - 2.4:.2f} {R:.2f},{sy - 7:.2f}"
          f"C{R - w * 0.1:.2f},{sy - 0.6:.2f} {mid + w * 0.22:.2f},{sy + 0.9:.2f} {mid:.2f},{sy + 0.9:.2f}"
          f"C{mid - w * 0.2:.2f},{sy + 0.9:.2f} {L + w * 0.2:.2f},{sy + 1.4:.2f} {L:.2f},{sy + 3:.2f}Z")
    dot = circle_d(mid, sy + 8.5, 3.4)
    b = union(t.bounds, path_bounds(sw), path_bounds(dot))
    return t.d, sw, dot, b

def sig_doc(mode, layout):
    pal = PAL[mode]; ink = pal["ink"]
    d, sw, dot, (x0, y0, x1, y1) = signature()
    core = f'<path d="{d}" fill="{ink}"/><path d="{sw}" fill="{ink}"/><path d="{dot}" fill="{pal["peach"]}"/>'
    w = x1 - x0
    if layout == "simbolo":
        e = madi.run("e", 150, 0)
        ex0, ey0, ex1, ey1 = e.bounds
        ul = f"M{ex0 + 4:.2f},{ey1 + 10:.2f}H{ex1 + 4:.2f}"
        cx = (ex0 + ex1) / 2 + 4
        inner = (f'<path d="{e.d}" fill="{ink}"/><path d="{ul}" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="{circle_d(cx, ey1 + 19, 4.2)}" fill="{pal["peach"]}"/>')
        return doc(inner, (ex0, ey0, ex1 + 8, ey1 + 24), 6, "Equilibra")
    if layout == "compacto":
        return doc(core, (x0, y0, x1, y1), 6, "Equilibra")
    tag = fit(albert, b3.TAG, w * 0.86, 0.22, 7, 13)
    y = y1 + 16
    parts = core + tpath(tag, -tag.bounds[0] + x0 + (w - tag.width) / 2, y - tag.bounds[1], ink)
    y += tag.bounds[3] - tag.bounds[1]
    label = b3.LABEL
    if layout == "vertical":
        y += 12
        nm = albert_reg.run(b3.NAMES, (tag.bounds[3] - tag.bounds[1]) * 1.75, 0.01)
        parts += tpath(nm, -nm.bounds[0] + x0 + (w - nm.width) / 2, y - nm.bounds[1], ink)
        y += nm.bounds[3] - nm.bounds[1]
        label += ", com Lisa Bompastor e Sara Lucas"
    return doc(parts, (x0, y0, x1, y), 10, label)

# ------------------------------------------------------------------ register M, O, P in the round-3 lockup machinery
b3.SYMS.update({"m-faces": faces, "o-arcos": arcos, "p-recortes": recortes})
b3.FACES.update({
    "m-faces": dict(tag=albert, names=albert_reg),
    "o-arcos": dict(tag=albert, names=albert_reg),
    "p-recortes": dict(tag=syne_tag, names=albert_reg),
})
b3.WORDS.update({
    "m-faces": instrument.run("Equilibra", 70, 0.01),
    "o-arcos": capra.run("equilibra", 60, 0.0),
    "p-recortes": syne.run("equilibra", 56, -0.01),
})
b3.CFG.update({
    "m-faces": dict(sym_h=112, gap=26, compact_k=1.35, vgap=24),
    "o-arcos": dict(sym_h=86, gap=24, compact_k=1.05, vgap=22),
    "p-recortes": dict(sym_h=110, gap=24, compact_k=1.3, vgap=22),
})

ORDER = ["m-faces", "n-assinatura", "o-arcos", "p-recortes"]

if __name__ == "__main__":
    manifest = {}
    for cid in ORDER:
        m = manifest[cid] = {}
        for mode in ("cor", "mono", "inverso"):
            for layout in ("horizontal", "compacto", "vertical", "simbolo"):
                svg = sig_doc(mode, layout) if cid == "n-assinatura" else b3.lockup(cid, mode, layout)
                m[f"{layout}-{mode}"] = svg
                if mode == "cor" or layout in ("horizontal", "simbolo") or (mode == "mono" and layout == "vertical"):
                    open(os.path.join(OUT, f"{cid}-{layout}" + ("" if mode == "cor" else f"-{mode}") + ".svg"), "w").write(svg)
    print("files", len(os.listdir(OUT)))
