"""Round 2 lockups: watercolour symbols + classical caps, centred like the references."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from glyphs import Face, path_bounds, union
from shapes import SYMBOLS, leaf, petal, circle, OFF, BROWN, PEACH, OLIVE, SAND
from render import layers_svg, FIO

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(HERE), "ronda-2"))
os.makedirs(OUT, exist_ok=True)

caps = Face("CormorantGaramond[wght].ttf", {"wght": 500})
ital = Face("CormorantGaramond-Italic[wght].ttf", {"wght": 500})
sans = Face("AlbertSans[wght].ttf", {"wght": 500})

WORD = caps.run("EQUILIBRA", 50, 0.2)
NAMES = ital.run("Com Lisa Bompastor e Sara Lucas", 21, 0.03)
TAG_TEXT = "NUTRIÇÃO  •  PSICOLOGIA  •  MOVIMENTO"

BOX = {"e-flor": (-4, -6, 148, 116), "f-selo": (-2, -2, 124, 124), "g-horizonte": (0, 0, 160, 86), "h-encontro": (8, 4, 112, 112)}


def tagline(width):
    probe = sans.run(TAG_TEXT, 10, 0.18)
    return sans.run(TAG_TEXT, max(7.5, min(12, 10 * width / probe.width)), 0.18)


def ornament(cid, mode):
    """Small mark for the divider, centred on (0,0), about 12 units tall."""
    ink = BROWN if mode != "inverso" else OFF
    op = FIO if mode == "cor" else 1
    sw = 0.7 if mode == "cor" else 0.9
    line = lambda d: f'<path d="{d}" fill="none" stroke="{ink}" stroke-opacity="{op}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
    fill = lambda d, c: f'<path d="{d}" fill="{c if mode == "cor" else ink}"/>'
    if cid == "e-flor":
        return "".join(line(leaf(0, 6, deg, l, w, 0, 0.9)[0]) for deg, l, w in ((-48, 9, 3.2), (48, 9, 3.2), (0, 12, 3.6)))
    if cid == "f-selo":
        return fill(leaf(-0.6, 6, -38, 11, 3.6, 0, 1)[0], OLIVE) + fill(leaf(0.6, 6, 38, 11, 3.6, 0, 1)[0], OLIVE)
    if cid == "g-horizonte":
        return fill("M-5.2,3.6A5.2,5.2 0 0,1 5.2,3.6Z", PEACH) + line("M-8.5,3.6H8.5")
    if cid == "h-encontro":
        return "".join(line(petal(0, 1.5, deg, 8, 3.4, -2)) for deg in (0, 120, 240))


def symbol(cid, mode, prefix, height, x, y, anchor="top-centre"):
    """Place the symbol so its box has given height; anchor top-centre at (x,y) or left-middle."""
    bx0, by0, bx1, by1 = BOX[cid]
    k = height / (by1 - by0)
    w = (bx1 - bx0) * k
    if anchor == "top-centre":
        tx, ty = x - w / 2 - bx0 * k, y - by0 * k
    else:  # left-middle
        tx, ty = x - bx0 * k, y - height / 2 - by0 * k
    inner = layers_svg(SYMBOLS[cid](), prefix, mode, texture=(mode == "cor"))
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({k:.4f})">{inner}</g>', w


def text(t, x, y, colour, op=1):
    o = f' fill-opacity="{op}"' if op != 1 else ""
    return f'<path d="{t.d}" fill="{colour}"{o} transform="translate({x:.2f} {y:.2f})"/>'


def doc(inner, box, pad, label):
    x0, y0, x1, y1 = box
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}" '
            f'width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" role="img" aria-label="{label}"><title>{label}</title>{inner}</svg>')


SYM_H = {"e-flor": 205, "f-selo": 196, "g-horizonte": 150, "h-encontro": 180}
LABEL = "Equilibra — Nutrição, Psicologia e Movimento, com Lisa Bompastor e Sara Lucas"


def vertical(cid, mode):
    ink = OFF if mode == "inverso" else BROWN
    p = f"{cid}-v-{mode}-"
    sym, sw = symbol(cid, mode, p, SYM_H[cid], 0, 0)
    ww = WORD.width
    y = SYM_H[cid] + 34
    parts = [sym, text(WORD, -(WORD.bounds[0] + WORD.bounds[2]) / 2, y - WORD.bounds[1], ink)]
    y += WORD.bounds[3] - WORD.bounds[1] + 18
    tag = tagline(ww)
    parts.append(text(tag, -(tag.bounds[0] + tag.bounds[2]) / 2, y - tag.bounds[1], ink))
    y += tag.bounds[3] - tag.bounds[1] + 24
    # divider: line, ornament, line
    half = ww * 0.36
    lo = 22
    op = FIO if mode == "cor" else 1
    parts.append(f'<path d="M{-half:.2f},{y + 6:.2f}H{-lo:.2f}M{lo:.2f},{y + 6:.2f}H{half:.2f}" stroke="{ink}" stroke-opacity="{op}" stroke-width=".8"/>')
    parts.append(f'<g transform="translate(0 {y + 6:.2f}) scale(1.5)">{ornament(cid, mode)}</g>')
    y += 18 + 18
    parts.append(text(NAMES, -(NAMES.bounds[0] + NAMES.bounds[2]) / 2, y - NAMES.bounds[1], ink))
    y += NAMES.bounds[3] - NAMES.bounds[1]
    half_w = max(sw, ww, tag.width, NAMES.width) / 2
    return doc("".join(parts), (-half_w, 0, half_w, y), 12, LABEL)


def horizontal(cid, mode, compact=False):
    ink = OFF if mode == "inverso" else BROWN
    p = f"{cid}-{'c' if compact else 'h'}-{mode}-"
    wh = WORD.bounds[3] - WORD.bounds[1]
    sh = (wh * 3.4 if compact else 124) * (0.8 if cid == "g-horizonte" else 1)
    sym, sw = symbol(cid, mode, p, sh, 0, 0, "left-middle")
    gap = 0.45 * wh if compact else 28
    x = sw + gap
    parts = [sym]
    if compact:
        parts.append(text(WORD, x - WORD.bounds[0], -(WORD.bounds[1] + WORD.bounds[3]) / 2, ink))
        return doc("".join(parts), (0, -sh / 2, x + WORD.width, sh / 2), 6, "Equilibra")
    tag = tagline(WORD.width)
    block = wh + 16 + (tag.bounds[3] - tag.bounds[1])
    wy = -block / 2 - WORD.bounds[1]
    ty = -block / 2 + wh + 16 - tag.bounds[1]
    parts.append(text(WORD, x - WORD.bounds[0], wy, ink))
    parts.append(text(tag, x - tag.bounds[0], ty, ink))
    return doc("".join(parts), (0, -sh / 2, x + max(WORD.width, tag.width), sh / 2), 8, "Equilibra — Nutrição, Psicologia e Movimento")


def symbol_only(cid, mode):
    bx0, by0, bx1, by1 = BOX[cid]
    inner = layers_svg(SYMBOLS[cid](), f"{cid}-s-{mode}-", mode, texture=(mode == "cor"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bx0} {by0} {bx1 - bx0} {by1 - by0}" width="{bx1 - bx0}" height="{by1 - by0}" role="img" aria-label="Equilibra"><title>Equilibra</title>{inner}</svg>'


if __name__ == "__main__":
    manifest = {}
    for cid in SYMBOLS:
        m = manifest[cid] = {
            "vertical-cor": vertical(cid, "cor"),
            "vertical-mono": vertical(cid, "mono"),
            "horizontal-cor": horizontal(cid, "cor"),
            "horizontal-mono": horizontal(cid, "mono"),
            "horizontal-inverso": horizontal(cid, "inverso"),
            "compacto-cor": horizontal(cid, "cor", True),
            "simbolo-cor": symbol_only(cid, "cor"),
            "simbolo-plano": symbol_only(cid, "plano"),
            "simbolo-mono": symbol_only(cid, "mono"),
        }
        for k, v in m.items():
            open(os.path.join(OUT, f"{cid}-{k.replace('-cor', '')}.svg"), "w").write(v)
    print(sorted(os.listdir(OUT)))
