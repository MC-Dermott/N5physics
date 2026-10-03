"""Side-view diagrams of light-gate experiments (SVG), matched to a question's wording.

- A trolley carrying a card, or a ball bearing, rolling down a ramp through one or two light gates
  (labelled X and Y when the question names them), wired to a timer or computer.
- A coin dropped vertically through a light gate.
Optional extras: the release point and a stop-clock.

light_gate_diagram(text) reads the question's own text (never its answer options, which could give
the answer away) and returns an SVG, or None if it doesn't mention a light gate.
"""
import math
import re

from utils.circuit_diagram import INK, _arrow, _circle, _line, _rect, _svg, _text

_BEAM = "#cf222e"
_FILL = "#dbe7f5"


def _gate(x, y_track, label):
    """An upright light gate straddling the track at x; the beam crosses at card height."""
    top, low = y_track - 82, y_track - 18
    return (_wire_path([(x - 16, low), (x - 16, top), (x + 16, top), (x + 16, low)], width=5)
            + f'<line x1="{x - 16:.1f}" y1="{y_track - 42:.1f}" x2="{x + 16:.1f}" y2="{y_track - 42:.1f}" stroke="{_BEAM}" '
              f'stroke-width="2" stroke-dasharray="4 3"/>'
            + _text(x - 4, top - 14, label, anchor="end"))


def _wire_path(pts, width=2, dash=False):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    extra = ' stroke-dasharray="5 4"' if dash else ""
    return f'<polyline points="{d}" stroke="{INK}" stroke-width="{width}" fill="none" stroke-linejoin="round"{extra}/>'


def _timer(x, y, name):
    return _rect(x, y, 96, 36) + _text(x + 48, y + 18, name)


def _stopclock(x, y):
    return (_circle(x, y, 13) + _line(x, y, x, y - 8, 1.6) + _line(x, y, x + 6, y + 3, 1.6)
            + _rect(x - 3, y - 19, 6, 5) + _text(x + 22, y, "stop-clock", anchor="start", weight="500"))


def ramp_setup(gates=1, labels=None, blocker="trolley", timer="timer", release=False, stopclock=False):
    """A ramp with the moving object and its light gate(s)."""
    W, H = 640, 300
    ax, ay, bx, by = 40, 120, 600, 255          # ramp from A (top) to B (bottom)
    ang = math.atan2(by - ay, bx - ax)
    deg = math.degrees(ang)

    def at(s):
        return ax + s * (bx - ax), ay + s * (by - ay)

    out = [_line(20, by + 15, W - 20, by + 15, 2),
           f'<rect x="{ax - 10}" y="{ay}" width="40" height="{by + 15 - ay}" fill="#e6e6e6" stroke="{INK}" stroke-width="1.5"/>',
           _line(ax, ay, bx, by, 4)]

    s0 = 0.10
    px, py = at(s0)
    if blocker == "ball bearing":
        out.append(f'<g transform="translate({px:.1f} {py:.1f}) rotate({deg:.1f})"><circle cx="0" cy="-9" r="9" fill="#9aa4b1" stroke="{INK}" stroke-width="2"/></g>')
        out.append(_text(px, py - 40, "ball bearing"))
    else:
        out.append(f'<g transform="translate({px:.1f} {py:.1f}) rotate({deg:.1f})">'
                   f'<rect x="-34" y="-27" width="68" height="16" rx="3" fill="white" stroke="{INK}" stroke-width="2"/>'
                   f'<circle cx="-20" cy="-6" r="6" fill="white" stroke="{INK}" stroke-width="2"/>'
                   f'<circle cx="20" cy="-6" r="6" fill="white" stroke="{INK}" stroke-width="2"/>'
                   f'<rect x="-15" y="-51" width="30" height="24" fill="{_FILL}" stroke="{INK}" stroke-width="2"/></g>')
        out.append(_text(px + 6, py - 78, "card on trolley"))
    if release:
        out.append(_text(px - 2, py + 34, "released from rest", weight="500"))

    positions = [0.58] if gates == 1 else [0.45, 0.80]
    labels = labels or (["light gate"] if gates == 1 else ["light gate", "light gate"])
    tx, ty = W - 130, 14
    out.append(_timer(tx, ty, timer))
    for s, label in zip(positions, labels):
        gx, gy = at(s)
        out.append(_gate(gx, gy, label))
        out.append(_wire_path([(gx + 16, gy - 82), (gx + 16, ty + 18), (tx, ty + 18)]))
    (x1, y1), (x2, y2) = at(0.22), at(0.34)
    out.append(_arrow(x1, y1 + 26, x2, y2 + 26) + _text((x1 + x2) / 2 + 10, (y1 + y2) / 2 + 50, "motion", weight="500"))
    if stopclock:
        out.append(_stopclock(250, 40))
    return _svg(W, H, "".join(out))


def falling_setup(blocker="coin", timer="timer"):
    """An object dropped vertically through a light gate."""
    W, H = 360, 330
    cx = 140
    out = [f'<ellipse cx="{cx}" cy="60" rx="16" ry="5" fill="#d4a017" stroke="{INK}" stroke-width="2"/>',
           _text(cx + 30, 60, blocker, anchor="start"),
           _text(cx + 30, 80, "dropped from rest", anchor="start", weight="500"),
           _arrow(cx, 82, cx, 140)]
    gy = 200
    # gate seen side-on: two arms either side of the path, beam across
    out.append(_wire_path([(cx - 40, gy - 30), (cx - 40, gy + 16), (cx - 20, gy + 16)], width=5)
               + _wire_path([(cx + 40, gy - 30), (cx + 40, gy + 16), (cx + 20, gy + 16)], width=5)
               + f'<line x1="{cx - 40:.1f}" y1="{gy:.1f}" x2="{cx + 40:.1f}" y2="{gy:.1f}" stroke="{_BEAM}" stroke-width="2" stroke-dasharray="4 3"/>'
               + _text(cx - 52, gy, "light gate", anchor="end", weight="500"))
    out.append(_timer(W - 116, gy + 60, timer) + _wire_path([(cx + 40, gy - 30), (cx + 40, gy - 50), (W - 68, gy - 50), (W - 68, gy + 60)]))
    out.append(_line(30, H - 30, W - 30, H - 30, 2))
    return _svg(W, H, "".join(out))


def light_gate_diagram(text):
    """A set-up diagram matched to the question's wording, or None if no light gate is mentioned."""
    t = text.lower()
    if "light gate" not in t:
        return None
    timer = "computer" if "computer" in t else "timer"
    if "coin" in t and ("dropped" in t or "falls" in t):
        return falling_setup("coin", timer)
    named = re.search(r"light gate[s]? x\b|gate x\b", t) is not None
    two = named or "two light gates" in t or "light gates" in t or "between the gates" in t
    labels = (["light gate X", "light gate Y"] if named else None) if two else None
    blocker = "ball bearing" if "ball bearing" in t else "trolley"
    return ramp_setup(gates=2 if two else 1, labels=labels, blocker=blocker, timer=timer,
                      release="from rest" in t, stopclock="stop-clock" in t or "stop clock" in t)
