"""Schematic (not-to-scale) diagrams of a projectile launched at an angle and landing at a different
height: off a cliff (lands lower) or onto a raised platform (lands higher). Labels carry the given
values only, so the diagram never shows an answer.
"""
import math

from utils.circuit_diagram import INK, _arrow, _svg, _text

_PATH = "#1f6feb"
_GROUND = "#e6e6e6"


def _path(points):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{d}" stroke="{_PATH}" stroke-width="2.5" fill="none" stroke-dasharray="7 5"/>'


def _block(x, y, w, h):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{_GROUND}" stroke="{INK}" stroke-width="2"/>'


def _launch(x, y, u_label, theta_label, theta_deg=40):
    """The launch velocity arrow and its angle above the horizontal."""
    a = math.radians(theta_deg)
    ex, ey = x + 70 * math.cos(a), y - 70 * math.sin(a)
    arc = f'<path d="M {x + 34:.1f} {y:.1f} A 34 34 0 0 0 {x + 34 * math.cos(a):.1f} {y - 34 * math.sin(a):.1f}" stroke="{INK}" stroke-width="1.6" fill="none"/>'
    return (_arrow(x, y, ex, ey, head=9) + f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + 60:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 3"/>'
            + arc + _text(x + 46, y - 12, theta_label, anchor="start", weight="500") + _text(ex + 6, ey - 8, u_label, anchor="start"))


def _height_marker(x, y_top, y_bot, label, side="start"):
    """A double-headed height arrow at x, labelled to its right (side="start") or left ("end")."""
    dx = 8 if side == "start" else -8
    return (_arrow(x, (y_top + y_bot) / 2, x, y_top, head=7) + _arrow(x, (y_top + y_bot) / 2, x, y_bot, head=7)
            + _text(x + dx, (y_top + y_bot) / 2, label, anchor=side))


def cliff_launch(u_label, theta_label, h_label, what="ball"):
    """Launched at an angle from the top of a cliff; lands on the ground (or sea) below."""
    W, H = 560, 320
    cliff_top, ground = 120, 285
    lx = 130
    curve = []
    for i in range(61):
        s = i / 60
        x = lx + s * 360
        y = cliff_top - 260 * s + 420 * s * s       # up, over the top, then down past the cliff height to the ground
        curve.append((x, min(y, ground)))
    out = [_block(20, cliff_top, lx - 20, ground - cliff_top),
           f'<line x1="{lx:.1f}" y1="{ground:.1f}" x2="{W - 20:.1f}" y2="{ground:.1f}" stroke="{INK}" stroke-width="2"/>',
           _path(curve), f'<circle cx="{lx:.1f}" cy="{cliff_top - 6:.1f}" r="6" fill="{INK}"/>',
           _launch(lx, cliff_top - 6, u_label, theta_label),
           _height_marker(40, cliff_top, ground, h_label),
           _text(curve[-1][0], ground + 18, "lands here", weight="500"),
           _text(lx - 12, cliff_top - 24, what, anchor="end", weight="500")]
    return _svg(W, H + 20, "".join(out))


def platform_landing(u_label, theta_label, h_label, what="ball"):
    """Launched at an angle from the ground; lands on a raised platform while coming down."""
    W, H = 560, 250
    ground = 220
    lx = 60
    plat_top = 120
    px0 = 330
    curve = []
    for i in range(61):
        s = i / 60
        x = lx + s * 380
        y = ground - 630 * s * (1 - s)
        curve.append((x, y))
        if x > px0 and y >= plat_top and s > 0.5:
            curve[-1] = (x, plat_top)
            break
    lx_end = curve[-1][0]
    out = [f'<line x1="20" y1="{ground:.1f}" x2="{W - 20:.1f}" y2="{ground:.1f}" stroke="{INK}" stroke-width="2"/>',
           _block(px0 - 10, plat_top, W - 30 - (px0 - 10), ground - plat_top),
           _path(curve), f'<circle cx="{lx:.1f}" cy="{ground - 6:.1f}" r="6" fill="{INK}"/>',
           _launch(lx, ground - 6, u_label, theta_label, theta_deg=55),
           _height_marker(W - 40, plat_top, ground, h_label, side="end"),
           _text(lx_end + 14, plat_top - 14, "lands here", anchor="start", weight="500"),
           _text(lx + 4, ground + 18, what, anchor="start", weight="500")]
    return _svg(W, H + 20, "".join(out))
