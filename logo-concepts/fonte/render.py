"""Render round-2 layers to SVG fragments with prefixed defs."""
import math
from shapes import OFF, BROWN

FIO = 0.55  # opacity of the fine brown lines (reads as warm gold on light grounds)


def hexid(c):
    return c.lstrip("#").lower()


def defs(prefix, colours, texture=True):
    out = []
    for c in sorted(colours):
        out.append(f'<radialGradient id="{prefix}w{hexid(c)}" cx=".5" cy=".55" r=".6">'
                   f'<stop offset="0" stop-color="{c}" stop-opacity=".3"/>'
                   f'<stop offset=".7" stop-color="{c}" stop-opacity=".46"/>'
                   f'<stop offset="1" stop-color="{c}" stop-opacity=".68"/></radialGradient>')
        out.append(f'<linearGradient id="{prefix}f{hexid(c)}" x1="0" y1="0" x2="0" y2="1">'
                   f'<stop offset="0" stop-color="{c}" stop-opacity=".66"/>'
                   f'<stop offset=".55" stop-color="{c}" stop-opacity=".4"/>'
                   f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>')
    if texture:
        out.append(f'<filter id="{prefix}tx" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
                   '<feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="3" seed="7" result="n"/>'
                   '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G" result="d"/>'
                   '<feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="3" result="g"/>'
                   '<feColorMatrix in="g" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -.55 1.12" result="ga"/>'
                   '<feComposite in="d" in2="ga" operator="in"/></filter>')
    return "<defs>" + "".join(out) + "</defs>"


def layers_svg(layers, prefix, mode="cor", texture=True):
    """mode: cor (watercolour), mono (brown lines only), inverso (off-white lines)."""
    if mode == "cor":
        cols = {c for kind, d, c in layers if kind in ("wash", "washfade")}
        washes = []
        for kind, d, c in layers:
            if kind == "wash":
                washes.append(f'<path d="{d}" fill="url(#{prefix}w{hexid(c)})" style="mix-blend-mode:multiply"/>')
            elif kind == "washfade":
                washes.append(f'<path d="{d}" fill="url(#{prefix}f{hexid(c)})" style="mix-blend-mode:multiply"/>')
        filt = f' filter="url(#{prefix}tx)"' if texture else ""
        out = [defs(prefix, cols, texture), f'<g style="isolation:isolate"{filt}>{"".join(washes)}</g>']
        line_col, line_op, line_k = BROWN, FIO, 1.0
    else:
        out = []
        line_col = BROWN if mode == "mono" else OFF
        line_op, line_k = 1.0, 1.6
    if mode == "plano":
        fills = [f'<path d="{d}" fill="{c}" fill-opacity=".88" style="mix-blend-mode:multiply"/>' for kind, d, c in layers if kind in ("wash", "washfade")]
        fills += [f'<path d="{d}" fill="{v}"/>' for kind, d, v in layers if kind == "solid"]
        return f'<g style="isolation:isolate">{"".join(fills)}</g>'
    for kind, d, v in layers:
        if kind == "mline" and mode != "cor":
            out.append(f'<path d="{d}" fill="none" stroke="{line_col}" stroke-width="{v * line_k:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
        if kind == "line":
            out.append(f'<path d="{d}" fill="none" stroke="{line_col}" stroke-opacity="{line_op}" stroke-width="{v * line_k:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
        elif kind == "dot":
            col = (BROWN if v == "ink" else v) if mode == "cor" else line_col
            op = ' fill-opacity=".8"' if mode == "cor" and v == "ink" else ""
            out.append(f'<path d="{d}" fill="{col}"{op}/>')
        elif kind == "solid":
            out.append(f'<path d="{d}" fill="{v if mode == "cor" else line_col}"/>')
    return "".join(out)
