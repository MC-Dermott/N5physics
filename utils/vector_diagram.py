"""Tip-to-tail vector diagrams for two perpendicular vectors, shown as a
{"type": "diagram"} working step. The North/South vector is always drawn
first (from the start point), the East/West vector from its tip, and the
resultant from the start point to the final tip.

Pure string-building — no randomness — so generators seeded for worked
examples stay reproducible."""

import base64
import html

_FIRST_COLOUR = "#1f6feb"
_SECOND_COLOUR = "#1a7f37"
_RESULTANT_COLOUR = "#cf222e"
_INK = "#24292f"

_LONG_SIDE = 190      # px length of the longer of the two component vectors
_MIN_RATIO = 0.3      # shorter component drawn at least this fraction of the longer
_CHAR_W = 8.2        # rough width of one 14px bold character
_PAD_Y = 45


def _marker(colour):
    mid = "arrow" + colour.lstrip("#")
    return mid, (
        f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" '
        f'markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
        f'fill="{colour}"/></marker>'
    )


def _text(x, y, s, colour, anchor="middle", weight="600"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{colour}" font-size="14" font-weight="{weight}" '
            f'font-family="sans-serif" text-anchor="{anchor}" dominant-baseline="middle">'
            f'{html.escape(s)}</text>')


def vector_diagram_svg(first_dir, first_mag, first_label, second_dir, second_mag, second_label,
                       resultant_label="R", theta=False, compass=True):
    """first_dir: "N" or "S" (drawn first, vertically); second_dir: "E" or "W".
    With compass=False (e.g. forward force + crosswind) "N" just means "up the page"
    and no North arrow is drawn."""
    a, b = abs(first_mag), abs(second_mag)
    scale = _LONG_SIDE / max(a, b)
    ly = max(a * scale, _MIN_RATIO * _LONG_SIDE)
    lx = max(b * scale, _MIN_RATIO * _LONG_SIDE)
    sy = -1 if first_dir == "N" else 1     # SVG y grows downwards
    sx = 1 if second_dir == "E" else -1

    # Room either side for the labels (the first vector's label sits beside it).
    pad_x = max(90, _CHAR_W * (len(first_label) + 2) + 25,
                _CHAR_W * (len(second_label) + 2) / 2 - lx / 2 + 15,
                _CHAR_W * len(resultant_label) - lx / 2 + 10)
    width = lx + 2 * pad_x
    height = ly + 2 * _PAD_Y + (30 if compass else 0)
    x0 = pad_x if sx > 0 else pad_x + lx
    top = _PAD_Y + (30 if compass else 0)
    y0 = top + ly if sy < 0 else top
    x1, y1 = x0, y0 + sy * ly           # tip of the first (N/S) vector
    x2, y2 = x1 + sx * lx, y1           # tip of the second (E/W) vector

    parts = []
    defs = []
    ids = {}
    for c in (_FIRST_COLOUR, _SECOND_COLOUR, _RESULTANT_COLOUR, _INK):
        ids[c], d = _marker(c)
        defs.append(d)
    parts.append(f'<defs>{"".join(defs)}</defs>')
    parts.append(f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" rx="10" fill="#ffffff" '
                 f'stroke="#d0d7de"/>')

    def line(xa, ya, xb, yb, colour, dash=False, width_=3):
        dash_attr = ' stroke-dasharray="8 5"' if dash else ""
        return (f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{colour}" '
                f'stroke-width="{width_}"{dash_attr} marker-end="url(#{ids[colour]})"/>')

    # Right-angle marker at the corner between the two components.
    m = 12
    parts.append(f'<path d="M{x1:.1f},{y1 - sy * m:.1f} L{x1 + sx * m:.1f},{y1 - sy * m:.1f} '
                 f'L{x1 + sx * m:.1f},{y1:.1f}" fill="none" stroke="{_INK}" stroke-width="1.5"/>')

    parts.append(line(x0, y0, x1, y1, _FIRST_COLOUR))
    parts.append(line(x1, y1, x2, y2, _SECOND_COLOUR))
    parts.append(line(x0, y0, x2, y2, _RESULTANT_COLOUR, dash=True))

    # Start point and the order the vectors are drawn in.
    parts.append(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="4" fill="{_INK}"/>')
    parts.append(_text(x0 - sx * 8, y0 - sy * 14, "start", _INK,
                       anchor="end" if sx > 0 else "start", weight="400"))

    # First vector: label on the side away from the triangle.
    parts.append(_text(x0 - sx * 10, (y0 + y1) / 2, f"① {first_label}", _FIRST_COLOUR,
                       anchor="end" if sx > 0 else "start"))
    # Second vector: label on the far side of the triangle from the start point.
    parts.append(_text((x1 + x2) / 2, y1 + sy * 16, f"② {second_label}", _SECOND_COLOUR))
    # Resultant: label just beyond its midpoint, away from the right angle.
    parts.append(_text((x0 + x2) / 2 + sx * 14, (y0 + y2) / 2 - sy * 14, resultant_label,
                       _RESULTANT_COLOUR, anchor="start" if sx > 0 else "end"))

    if theta:
        r = 34
        ax, ay = x0, y0 + sy * r
        hyp = (lx ** 2 + ly ** 2) ** 0.5
        bx, by = x0 + sx * r * lx / hyp, y0 + sy * r * ly / hyp
        sweep = 1 if sx * sy < 0 else 0
        parts.append(f'<path d="M{ax:.1f},{ay:.1f} A{r},{r} 0 0 {sweep} {bx:.1f},{by:.1f}" fill="none" '
                     f'stroke="{_INK}" stroke-width="1.5"/>')
        # Label along the bisector of the first vector and the resultant.
        ux, uy = lx / hyp, 1 + ly / hyp
        norm = (ux ** 2 + uy ** 2) ** 0.5
        mx, my = x0 + sx * (r + 12) * ux / norm, y0 + sy * (r + 12) * uy / norm
        parts.append(_text(mx, my, "θ", _INK))

    if compass:
        cx, cy = width - 22, 14
        parts.append(line(cx, cy + 30, cx, cy + 4, _INK, width_=2))
        parts.append(_text(cx - 12, cy + 18, "N", _INK))

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
            f'viewBox="0 0 {width:.0f} {height:.0f}">{"".join(parts)}</svg>')


def vector_diagram_step(*args, **kwargs):
    """A {"type": "diagram"} working step holding the SVG."""
    return {"type": "diagram", "content": vector_diagram_svg(*args, **kwargs)}


def diagram_markdown(svg):
    """Markdown image embedding the SVG, so it renders inside st.markdown text
    (worked examples are built as one markdown string)."""
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"![Vector diagram]({uri})"
