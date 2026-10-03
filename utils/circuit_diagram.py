"""Circuit diagrams (SVG) drawn with the SQA circuit symbols, for questions that describe a circuit.

Three layouts:
- loop_circuit: components in series along the top of a loop (any element can be a parallel group),
  with the supply on the bottom wire — e.g. a lamp and resistor in series with a battery.
- network: a resistor network between two terminals X and Y, with no supply.
- divider: a vertical potential divider between two supply rails, optionally switching a transistor
  whose collector (drain) circuit contains an output device.

Components are dicts made with comp(kind, label); kinds: resistor, variable, thermistor, ldr, lamp,
led, ammeter, voltmeter, switch, fuse, heater. A parallel group is par([branch, branch, ...]) where
each branch is a list of components. comp(..., voltmeter="V") also draws a voltmeter across it.

Pure string-building — no randomness — so generators seeded for worked examples stay reproducible.
The SVG has its own white background so it reads in both light and dark themes.
"""
import html

from utils.diagrams import with_diagram  # noqa: F401  (re-exported for the circuit generators)

INK = "#24292f"
_U = 80          # length of wire one component occupies
_GAP_Y = 78      # spacing between parallel branches
_STROKE = 'stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round"'.format(c=INK)


def comp(kind, label="", voltmeter=None):
    return {"kind": kind, "label": label, "voltmeter": voltmeter}


def par(*branches):
    return {"kind": "parallel", "branches": [list(b) for b in branches]}


# ── primitives ──────────────────────────────────────────────────────────────

def _line(x1, y1, x2, y2, width=2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="{width}" stroke-linecap="round"/>'


def _wire(*pts):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{d}" {_STROKE}/>'


def _dot(x, y):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{INK}"/>'


def _terminal(x, y):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="white" stroke="{INK}" stroke-width="2"/>'


def _text(x, y, s, anchor="middle", size=13, weight="600"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{INK}" font-size="{size}" font-weight="{weight}" font-family="sans-serif" '
            f'text-anchor="{anchor}" dominant-baseline="middle">{html.escape(s)}</text>')


def _arrow(x1, y1, x2, y2, head=6):
    """A short line with an open arrowhead at (x2, y2)."""
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
    p2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
    return (_line(x1, y1, x2, y2, 1.6)
            + f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{INK}"/>')


def _rect(x, y, w, h):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="white" stroke="{INK}" stroke-width="2"/>'


def _circle(x, y, r):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="white" stroke="{INK}" stroke-width="2"/>'


# ── symbols (drawn horizontally, centred on (x, y), spanning x ± _U/2) ─────────

def _leads(x, y, half_body):
    return _line(x - _U / 2, y, x - half_body, y) + _line(x + half_body, y, x + _U / 2, y)


def _symbol(kind, x, y):
    """SVG for one component drawn horizontally. Returns (shapes, upright_text) — text that must
    not be rotated when the symbol is drawn vertically."""
    if kind in ("resistor", "heater"):
        return _leads(x, y, 22) + _rect(x - 22, y - 9, 44, 18), ""
    if kind == "variable":
        return _leads(x, y, 22) + _rect(x - 22, y - 9, 44, 18) + _arrow(x - 18, y + 16, x + 20, y - 17), ""
    if kind == "thermistor":
        return (_leads(x, y, 22) + _rect(x - 22, y - 9, 44, 18) + _line(x - 18, y + 16, x + 18, y - 16, 1.6)
                + _line(x - 28, y + 16, x - 18, y + 16, 1.6)), ""
    if kind == "ldr":
        return (_leads(x, y, 22) + _circle(x, y, 22) + _rect(x - 14, y - 6, 28, 12)
                + _arrow(x - 30, y - 34, x - 14, y - 19) + _arrow(x - 16, y - 40, x - 1, y - 24)), ""
    if kind == "lamp":
        d = 10
        return (_leads(x, y, 15) + _circle(x, y, 15) + _line(x - d, y - d, x + d, y + d) + _line(x - d, y + d, x + d, y - d)), ""
    if kind == "led":
        return (_leads(x, y, 17) + _circle(x, y, 17) + _line(x - 17, y, x + 17, y)
                + f'<polygon points="{x - 7:.1f},{y - 9:.1f} {x - 7:.1f},{y + 9:.1f} {x + 6:.1f},{y:.1f}" fill="{INK}"/>'
                + _line(x + 7, y - 9, x + 7, y + 9) + _arrow(x - 2, y - 19, x + 9, y - 31) + _arrow(x + 7, y - 17, x + 18, y - 29)), ""
    if kind in ("ammeter", "voltmeter"):
        return _leads(x, y, 14) + _circle(x, y, 14), _text(x, y + 1, "A" if kind == "ammeter" else "V", size=14)
    if kind == "switch":
        return (_line(x - _U / 2, y, x - 16, y) + _line(x + 16, y, x + _U / 2, y) + _dot(x - 16, y) + _dot(x + 16, y)
                + _line(x - 16, y, x + 13, y - 14)), ""
    if kind == "fuse":
        return _leads(x, y, 20) + _rect(x - 20, y - 6, 40, 12) + _line(x - 20, y, x + 20, y), ""
    if kind == "cell":
        return (_line(x - _U / 2, y, x - 4, y) + _line(x + 4, y, x + _U / 2, y)
                + _line(x - 4, y - 16, x - 4, y + 16) + _line(x + 4, y - 8, x + 4, y + 8, 5)), ""
    if kind == "battery":
        return (_line(x - _U / 2, y, x - 12, y) + _line(x + 12, y, x + _U / 2, y)
                + _line(x - 12, y - 16, x - 12, y + 16) + _line(x - 5, y - 8, x - 5, y + 8, 5)
                + _line(x - 5, y, x + 5, y)
                + _line(x + 5, y - 16, x + 5, y + 16) + _line(x + 12, y - 8, x + 12, y + 8, 5)), ""
    raise ValueError(f"unknown component kind {kind!r}")


def _place(kind, x, y, vertical=False):
    shapes, upright = _symbol(kind, x, y)
    if vertical:
        shapes = f'<g transform="rotate(90 {x:.1f} {y:.1f})">{shapes}</g>'
    return shapes + upright


def _svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
            f'viewBox="0 0 {width:.0f} {height:.0f}"><rect width="100%" height="100%" rx="8" fill="white"/>{body}</svg>')


# ── series/parallel chains (loop circuits and networks) ─────────────────────

def _width(el):
    if el["kind"] == "parallel":
        return max(len(b) for b in el["branches"]) * _U + 40
    return _U


def _depth(el):
    return (len(el["branches"]) - 1) * _GAP_Y if el["kind"] == "parallel" else 0


def _label_gap(kind):
    return 50 if kind in ("ldr", "led") else 24


def _chain(elements, x0, y):
    """Draws the elements left to right from x0 along y. Returns (svg, x_end)."""
    out = []
    x = x0
    for el in elements:
        w = _width(el)
        if el["kind"] == "parallel":
            xl, xr = x, x + w
            n = len(el["branches"])
            out.append(_line(xl, y, xl, y + (n - 1) * _GAP_Y) + _line(xr, y, xr, y + (n - 1) * _GAP_Y))
            for i, branch in enumerate(el["branches"]):
                by = y + i * _GAP_Y
                bw = len(branch) * _U
                bx0 = xl + (w - bw) / 2
                out.append(_line(xl, by, bx0, by) + _line(bx0 + bw, by, xr, by))
                for j, c in enumerate(branch):
                    cx = bx0 + j * _U + _U / 2
                    out.append(_place(c["kind"], cx, by))
                    if c["label"]:
                        out.append(_text(cx, by - _label_gap(c["kind"]), c["label"]))
                out.append(_dot(xl, by) + _dot(xr, by))
        else:
            cx = x + _U / 2
            out.append(_place(el["kind"], cx, y))
            if el["label"]:
                out.append(_text(cx, y + 30, el["label"]) if el.get("voltmeter") else _text(cx, y - _label_gap(el["kind"]), el["label"]))
            if el.get("voltmeter"):
                vy = y - 52
                out.append(_wire((cx - 34, y), (cx - 34, vy), (cx - 14, vy)) + _wire((cx + 14, vy), (cx + 34, vy), (cx + 34, y))
                           + _circle(cx, vy, 14) + _text(cx, vy + 1, "V", size=14) + _dot(cx - 34, y) + _dot(cx + 34, y))
                if el["voltmeter"] != "V":
                    out.append(_text(cx + 22, vy - 20, el["voltmeter"], anchor="start", weight="500"))
        x += w
    return "".join(out), x


def _headroom(elements):
    if any(e.get("voltmeter") for e in elements):
        return 92
    kinds = {e["kind"] for e in elements} | {c["kind"] for e in elements if e["kind"] == "parallel" for b in e["branches"] for c in b}
    return 70 if kinds & {"ldr", "led"} else 46


def loop_circuit(elements, supply="battery", supply_label=""):
    """Components along the top of a loop, the supply on the bottom wire."""
    x0 = 50
    top = _headroom(elements)
    chain, chain_end = _chain(elements, x0, top)
    x_end = max(chain_end, x0 + _U + 40)     # room for the supply on the bottom wire
    chain += _line(chain_end, top, x_end, top)
    depth = max([_depth(e) for e in elements] + [0])
    bottom = top + max(depth + 64, 110)
    cx = (x0 + x_end) / 2
    body = (chain
            + _wire((x0, top), (x0, bottom), (cx - _U / 2, bottom)) + _wire((cx + _U / 2, bottom), (x_end, bottom), (x_end, top))
            + _place(supply, cx, bottom))
    if supply_label:
        body += _text(cx, bottom + 30, supply_label)
    return _svg(x_end + 50, bottom + (50 if supply_label else 30), body)


def network(elements, left="X", right="Y"):
    """A resistor network between two terminals."""
    x0 = 50
    top = _headroom(elements)
    chain, x_end = _chain(elements, x0, top)
    depth = max([_depth(e) for e in elements] + [0])
    body = (chain + _line(x0 - 20, top, x0, top) + _line(x_end, top, x_end + 20, top)
            + _terminal(x0 - 20, top) + _terminal(x_end + 20, top)
            + _text(x0 - 20, top - 20, left) + _text(x_end + 20, top - 20, right))
    return _svg(x_end + 50, top + depth + 36, body)


# ── potential divider (vertical) with an optional transistor switch ─────────

def divider(top_kind, top_label, bottom_kind, bottom_label, supply_label="", transistor=None,
            output_kind=None, output_label="", vout_label=None):
    """top/bottom: the divider's two components, top rail to bottom rail. transistor: None, "npn"
    or "mosfet" — its input is connected across the bottom component; output_kind is in its
    collector/drain circuit. vout_label: draw a voltmeter across the bottom component."""
    y_top, y_bot = 40, 280
    xc = 200                     # divider column
    y_mid = (y_top + y_bot) / 2
    y1, y2 = y_top + 60, y_bot - 60
    right = 470 if transistor else (350 if vout_label else 290)
    out = [_line(46, y_top, right, y_top) + _line(46, y_bot, right, y_bot),
           _terminal(40, y_top) + _terminal(40, y_bot),
           _text(40, y_top - 20, supply_label or "+"), _text(40, y_bot + 20, "0 V"),
           _line(xc, y_top, xc, y1 - _U / 2) + _line(xc, y1 + _U / 2, xc, y2 - _U / 2) + _line(xc, y2 + _U / 2, xc, y_bot),
           _place(top_kind, xc, y1, vertical=True), _place(bottom_kind, xc, y2, vertical=True),
           _dot(xc, y_top) + _dot(xc, y_bot) + _dot(xc, y_mid)]
    if top_label:
        out.append(_text(xc - 30, y1, top_label, anchor="end"))
    if bottom_label:
        out.append(_text(xc - 30, y2, bottom_label, anchor="end"))
    if vout_label and not transistor:
        vx = xc + 90
        out.append(_wire((xc, y_mid), (vx, y_mid), (vx, y2 - 14)) + _wire((vx, y2 + 14), (vx, y_bot))
                   + _circle(vx, y2, 14) + _text(vx, y2 + 1, "V", size=14) + _dot(vx, y_bot)
                   + _text(vx + 22, y2, vout_label, anchor="start", weight="500"))
    if transistor:
        tx, ty = 380, y_mid + 20         # transistor centre
        out.append(_circle(tx, ty, 26))
        if transistor == "npn":
            out.append(_line(tx - 10, ty - 14, tx - 10, ty + 14, 3)
                       + _wire((xc, y_mid), (tx - 50, y_mid), (tx - 50, ty), (tx - 10, ty))
                       + _line(tx - 10, ty - 6, tx + 10, ty - 20) + _line(tx + 10, ty - 20, tx + 10, ty - 26)
                       + _arrow(tx - 10, ty + 6, tx + 9, ty + 19, head=8) + _line(tx + 10, ty + 20, tx + 10, ty + 26))
            name = "transistor"
        else:
            out.append(_line(tx - 14, ty - 14, tx - 14, ty + 14, 2.5)
                       + _wire((xc, y_mid), (tx - 50, y_mid), (tx - 50, ty + 10), (tx - 14, ty + 10))
                       + _line(tx - 6, ty - 16, tx - 6, ty - 8, 3) + _line(tx - 6, ty - 4, tx - 6, ty + 4, 3) + _line(tx - 6, ty + 8, tx - 6, ty + 16, 3)
                       + _wire((tx - 6, ty - 12), (tx + 10, ty - 12), (tx + 10, ty - 26))
                       + _wire((tx - 6, ty + 12), (tx + 10, ty + 12), (tx + 10, ty + 26))
                       + _arrow(tx + 10, ty, tx - 4, ty, head=7) + _line(tx + 10, ty, tx + 10, ty + 12))
            name = "MOSFET"
        out.append(_text(tx + 34, ty + 6, name, anchor="start", weight="500"))
        ox = tx + 10
        oy = (y_top + ty - 26) / 2
        out.append(_line(ox, y_top, ox, oy - _U / 2) + _line(ox, oy + _U / 2, ox, ty - 26) + _line(ox, ty + 26, ox, y_bot)
                   + _dot(ox, y_top) + _dot(ox, y_bot))
        if output_kind:
            out.append(_place(output_kind, ox, oy, vertical=True))
        else:
            out.append(_line(ox, oy - _U / 2, ox, oy + _U / 2))
        if output_label:
            out.append(_text(ox + 30, oy, output_label, anchor="start", weight="500"))
    return _svg(right + 30, y_bot + 40, "".join(out))

