"""Text-to-outline helpers: shape with HarfBuzz, draw outlines with fontTools."""
import io
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"


class Face:
    def __init__(self, filename, axes):
        var = TTFont(FONTS + filename)
        inst = instancer.instantiateVariableFont(var, axes, inplace=False)
        buf = io.BytesIO()
        inst.save(buf)
        data = buf.getvalue()
        self.tt = TTFont(io.BytesIO(data))
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upm = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(data))

    def shape(self, text, features=None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, features or {"kern": True, "liga": True})
        return [
            (self.order[i.codepoint], p.x_advance, p.x_offset, p.y_offset)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)
        ]

    def run(self, text, size, tracking=0.0, features=None):
        """Return Text object: baseline at y=0, y grows downward, x starts at 0."""
        s = size / self.upm
        x = 0.0
        d_parts, glyphs = [], []
        bp = BoundsPen(self.gs)
        items = self.shape(text, features)
        for n, (g, adv, xo, yo) in enumerate(items):
            pen = SVGPathPen(self.gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
            t = (s, 0, 0, -s, x + xo * s, -yo * s)
            self.gs[g].draw(TransformPen(pen, t))
            self.gs[g].draw(TransformPen(bp, t))
            d_parts.append(pen.getCommands())
            glyphs.append((g, x + xo * s))
            x += adv * s
            if n < len(items) - 1:
                x += tracking * size
        return Text("".join(d_parts), bp.bounds, x, glyphs, s, self)


class Text:
    def __init__(self, d, bounds, advance, glyphs, scale, face):
        self.d, self.bounds, self.advance, self.glyphs, self.scale, self.face = d, bounds, advance, glyphs, scale, face

    @property
    def width(self):
        return self.bounds[2] - self.bounds[0]


def path_bounds(d, stroke=0.0):
    bp = BoundsPen(None)
    parse_path(d, bp)
    x0, y0, x1, y1 = bp.bounds
    h = stroke / 2
    return (x0 - h, y0 - h, x1 + h, y1 + h)


def circle_d(cx, cy, r):
    return (f"M{cx - r:.2f},{cy:.2f}a{r:.2f},{r:.2f} 0 1,0 {2 * r:.2f},0"
            f"a{r:.2f},{r:.2f} 0 1,0 {-2 * r:.2f},0Z")


def union(*bs):
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
